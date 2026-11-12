#!/usr/bin/env python3
"""Review explicit Wiki reads from selected Codex records and update a local ledger."""
import argparse
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import tempfile
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

RULE = 'wiki_read_reference_v3'
WIKI_LINK = re.compile(r'`(03_Wiki/[^`\n]+\.md)`|\[\[(03_Wiki/[^|#\\\]\n]+)(?:#[^|\\\]\n]*)?(?:\\?\|[^\]\n]*)?\]\]')
SEPARATOR = re.compile(r':?-+:?')
WRAPPED_EXEC = re.compile(
    r'\s*(?:const|let|var)\s+(\w+)\s*=\s*await\s+tools\.exec_command\(\s*\{(.*?)\}\s*\)'
    r'\s*;\s*text\(\s*\1\.output\s*\)\s*;?\s*', re.DOTALL)
ARGUMENT = re.compile(r'\s*"?([a-z_]+)"?\s*:\s*')


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as file:
        temporary = Path(file.name)
        try:
            file.write(text)
            file.flush()
            os.fsync(file.fileno())
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def write_json(path, data):
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def event_id(call, note):
    encoded = json.dumps([RULE, 'codex', call, note], ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()[:32]


def wiki_path(match):
    relative = match.group(1) or match.group(2)
    return relative if relative.endswith('.md') else relative + '.md'


def table_cells(line):
    escaped = re.sub(r'\[\[[^\]\n]+\]\]',
                     lambda link: re.sub(r'(?<!\\)\|', r'\\|', link[0]), line)
    return [cell.strip() for cell in re.split(r'(?<!\\)\|', escaped.strip().strip('|'))]


def indexed_notes(vault, original):
    notes = {}
    for match in WIKI_LINK.finditer(original):
        relative = wiki_path(match)
        note = (vault / relative).resolve()
        if note.is_relative_to(vault / '03_Wiki') and note.is_file():
            notes[note] = relative
    return notes


def references(command, cwd, notes):
    """Support literal single-file cat calls. Other reads require separate review."""
    try:
        words = shlex.split(command)
    except ValueError:
        return None
    if len(words) == 3 and words[1] == '--':
        words.pop(1)
    if len(words) != 2 or words[0] not in ('cat', '/bin/cat'):
        return None
    target = (cwd / words[1]).resolve()
    return notes.get(target)


def execution_arguments(payload):
    if payload['type'] == 'function_call' and payload.get('name', '').split('__')[-1] == 'exec_command':
        return json.loads(payload.get('arguments', '{}'))
    if payload['type'] != 'custom_tool_call' or payload.get('name') != 'exec':
        return {}
    match = WRAPPED_EXEC.fullmatch(payload.get('input', ''))
    if not match:
        return {}
    # Accept a literal object with JSON values. Never evaluate recorded code.
    source = match[2].strip()
    arguments = {}
    while source:
        key = ARGUMENT.match(source)
        if not key or key[1] in arguments:
            return {}
        value, end = json.JSONDecoder().raw_decode(source[key.end():])
        arguments[key[1]] = value
        source = source[key.end() + end:].strip()
        if source and not source.startswith(','):
            return {}
        source = source.removeprefix(',').strip()
    return arguments


def collect_record(path, vault, notes, target_day, zone):
    candidates, gaps, pending = [], [], {}
    thread, cwd, task = None, None, None
    with path.open(encoding='utf-8') as record:
        for number, line in enumerate(record, 1):
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                gaps.append(f'{path.name}:{number}: invalid record')
                continue
            payload = item.get('payload', {})
            if item.get('type') == 'session_meta':
                thread = payload.get('id')
                cwd = Path(payload['cwd']) if payload.get('cwd') else None
                continue
            if item.get('type') != 'response_item':
                continue
            kind = payload.get('type')
            if kind == 'message' and payload.get('role') == 'user':
                message = '\n'.join(c.get('text', '') for c in payload.get('content', []))
                if message.startswith(('# AGENTS', '<environment_context>', '<skills_instructions>', '<skill>')):
                    continue
                task = number
            elif kind in ('function_call', 'custom_tool_call'):
                try:
                    arguments = execution_arguments(payload)
                except (TypeError, json.JSONDecodeError):
                    continue
                command = arguments.get('cmd', '')
                workdir = Path(arguments['workdir']) if arguments.get('workdir') else cwd
                if workdir and payload.get('call_id') and isinstance(command, str):
                    relative = references(command, workdir, notes)
                    if relative:
                        pending[payload['call_id']] = (relative, number, task)
            elif kind in ('function_call_output', 'custom_tool_call_output') and payload.get('call_id') in pending:
                call = payload['call_id']
                relative, request_line, task_line = pending.pop(call)
                try:
                    timestamp = datetime.fromisoformat(item['timestamp'])
                    if timestamp.tzinfo is None:
                        raise ValueError('timestamp has no timezone')
                except (KeyError, ValueError):
                    gaps.append(f'{path.name}:{number}: missing a valid response timestamp')
                    continue
                if timestamp.astimezone(zone).date() != target_day:
                    continue
                body = (vault / relative).read_text(encoding='utf-8')
                output = payload.get('output', '')
                if isinstance(output, list):
                    output = '\n'.join(part.get('text', '') for part in output if isinstance(part, dict))
                output = str(output)
                substantive = [line.strip() for line in body.splitlines()
                               if len(line.strip()) >= 14 and not line.lstrip().startswith(('#', '<', '|', '>'))]
                failed = re.search(r'\b(?:Process exited with code|Exit code:)\s*[1-9]', output)
                if not thread or not task_line or failed or not any(line in output for line in substantive):
                    gaps.append(f'{path.name}:{number}: task or returned body could not be verified')
                    continue
                candidates.append({'id': event_id(call, relative), 'wiki': relative, 'call_id': call,
                                   'task': f'{thread}:{task_line}', 'record': str(path), 'task_line': task_line,
                                   'request_line': request_line, 'return_line': number,
                                   'returned_at': timestamp.isoformat()})
    for _, request_line, _ in pending.values():
        gaps.append(f'{path.name}:{request_line}: no matching tool response')
    return candidates, gaps


def render_counts(original, counts, notes):
    result = []
    in_wiki, header, adding = False, None, False
    valid_paths = set(notes.values())
    for line in original.splitlines(keepends=True):
        if line.startswith('## '):
            in_wiki, header = line.startswith('## 03_Wiki'), None
        if not in_wiki or not line.startswith('|'):
            result.append(line)
            continue
        cells = table_cells(line)
        if 'Path' in cells and 'Topic' in cells:
            adding = 'Reuse count' not in cells
            header = cells.copy()
            column = header.index('Reuse count') if not adding else (1 if header[0] == 'Date' else 0)
            if adding:
                cells.insert(column, 'Reuse count')
        elif header:
            if len(cells) != len(header):
                raise ValueError('Check INDEX.md for inconsistent Wiki table columns')
            link = WIKI_LINK.search(line)
            relative = wiki_path(link) if link else None
            if all(SEPARATOR.fullmatch(cell) for cell in cells):
                value = '---:'
            elif relative in valid_paths:
                value = str(counts[relative])
            elif adding:
                value = '—'
            else:
                result.append(line)
                continue
            if adding:
                cells.insert(column, value)
            else:
                cells[column] = value
        else:
            result.append(line)
            continue
        result.append('| ' + ' | '.join(cells) + ' |' + ('\n' if line.endswith('\n') else ''))
    return ''.join(result)


def has_existing_counts(original):
    column = None
    for line in original.splitlines():
        if line.startswith('## '):
            column = None
        if not line.startswith('|'):
            continue
        cells = table_cells(line)
        if 'Path' in cells and 'Reuse count' in cells:
            column = cells.index('Reuse count')
        elif column is not None and WIKI_LINK.search(line) and column < len(cells):
            if cells[column] not in ('0', '', '—', '-'):
                return True
    return False


def review(vault, state_path, timezone, batch_path, review_path, apply):
    batch, selection = load(batch_path), load(review_path)
    if batch['vault'] != str(vault) or batch['timezone'] != timezone or batch['rule'] != RULE:
        raise ValueError('The candidate file uses a different vault, time zone, or counting rule')
    candidates = {row['id']: row for row in batch['candidates']}
    approved = {}
    for key, choice in selection.items():
        if key not in candidates:
            raise ValueError(f'The candidate file lacks this read: {key}')
        purpose = choice if isinstance(choice, str) else choice['purpose']
        if not purpose.strip():
            raise ValueError('Every verified read requires a concrete purpose')
        row = candidates[key]
        if key != event_id(row['call_id'], row['wiki']):
            raise ValueError('Candidate event identifiers do not match')
        if not isinstance(choice, str) and choice.get('task'):
            row = {**row, 'task': choice['task']}
        approved[key] = {**row, 'purpose': purpose.strip()}
    index = vault / 'INDEX.md'
    original = index.read_text(encoding='utf-8')
    notes = indexed_notes(vault, original)
    for row in approved.values():
        if row['wiki'] not in notes.values():
            raise ValueError(f'Verified notes must appear in the current index: {row["wiki"]}')
    state = load_state(state_path, vault, timezone)
    if not state_path.exists() and has_existing_counts(original):
        raise ValueError('Existing reuse counts have no matching ledger. Keep the original vault and use a separate vault or migrate the ledger.')
    new = len(approved.keys() - state['events'].keys())
    state['events'].update(approved)
    day = batch['day']
    previous = state['days'].get(day, {})
    covered = list(dict.fromkeys(previous.get('records', []) + batch['records']))
    gaps = list(dict.fromkeys(previous.get('gaps', []) + batch['gaps']))
    pending = sorted((set(previous.get('unreviewed', [])) | set(candidates)) - set(state['events']))
    state['days'][day] = {'records': covered, 'gaps': gaps, 'unreviewed': pending, 'coverage': 'partial'}
    counts = Counter(row['wiki'] for row in state['events'].values())
    updated = render_counts(original, counts, notes)
    if apply:
        if index.is_symlink() or index.read_text(encoding='utf-8') != original:
            raise ValueError('INDEX.md changed during review. Preview again before applying.')
        # The ledger is authoritative. A retry regenerates the index after an interrupted write.
        write_json(state_path, state)
        if updated != original:
            atomic_write(index, updated)
    zone = ZoneInfo(timezone)
    rows = [row for row in state['events'].values()
            if datetime.fromisoformat(row['returned_at']).astimezone(zone).date().isoformat() == day]
    return {'mode': 'applied' if apply else 'preview', 'new': new, 'total': sum(counts.values()),
            'day': day, 'reads': rows, 'coverage': state['days'][day]}


def load_state(path, vault, timezone):
    if not path.exists():
        return {'rule': RULE, 'vault': str(vault), 'timezone': timezone, 'events': {}, 'days': {}}
    state = load(path)
    if state['vault'] != str(vault) or state['timezone'] != timezone or state['rule'] != RULE:
        raise ValueError('The ledger uses a different vault, time zone, or counting rule')
    return state


def weekly(state, week, zone):
    year, number = week.split('-W')
    start = date.fromisocalendar(int(year), int(number), 1)
    end = start + timedelta(days=7)
    groups = defaultdict(list)
    for row in state['events'].values():
        day = datetime.fromisoformat(row['returned_at']).astimezone(zone).date()
        if start <= day < end:
            groups[row['wiki']].append(row)
    return {'week': week, 'start': str(start), 'end_exclusive': str(end),
            'coverage': {day: detail for day, detail in state['days'].items() if str(start) <= day < str(end)},
            'notes': [{'wiki': wiki, 'reads': len(rows), 'independent_tasks': len({row['task'] for row in rows}),
                       'evidence': rows} for wiki, rows in sorted(groups.items())]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--timezone', required=True)
    parser.add_argument('--state-dir', type=Path)
    actions = parser.add_subparsers(dest='action', required=True)
    collect = actions.add_parser('collect')
    collect.add_argument('--day', type=date.fromisoformat, required=True)
    collect.add_argument('--record', type=Path, action='append', default=[])
    collect.add_argument('--sessions', type=Path, action='append', default=[])
    collect.add_argument('--out', type=Path, required=True)
    confirm = actions.add_parser('review')
    confirm.add_argument('batch', type=Path)
    confirm.add_argument('selection', type=Path)
    confirm.add_argument('--apply', action='store_true')
    week = actions.add_parser('week')
    week.add_argument('--week', required=True)
    args = parser.parse_args()
    vault = args.vault.expanduser().resolve()
    zone = ZoneInfo(args.timezone)
    index = vault / 'INDEX.md'
    if not index.is_file() or index.is_symlink():
        raise ValueError('Choose a vault with a regular INDEX.md file')
    state_dir = args.state_dir.expanduser().resolve() if args.state_dir else vault / '.lifeos'
    if (vault / '.lifeos').is_symlink():
        raise ValueError('The vault .lifeos path must be a regular directory')
    state_path = state_dir / 'reuse-ledger.json'
    if args.action == 'collect':
        files = {record.expanduser().resolve() for record in args.record}
        gaps = []
        if not args.record and not args.sessions:
            parser.error('Provide an authorized --record or --sessions path')
        for supplied in args.sessions:
            source = supplied.expanduser().resolve()
            if not source.is_dir():
                gaps.append(f'Cannot read record directory: {source}')
                continue
            files.update(p for p in source.rglob('*.jsonl') if not p.is_symlink())
            if any(source.rglob('*.jsonl.zst')):
                gaps.append(f'{source.name}: provide authorized decompressed record files')
        notes = indexed_notes(vault, index.read_text(encoding='utf-8'))
        candidates = {}
        for file in sorted(files):
            try:
                found, omissions = collect_record(file, vault, notes, args.day, zone)
                for event in found:
                    candidates.setdefault(event['id'], event)
                gaps.extend(omissions)
            except (OSError, UnicodeError) as error:
                gaps.append(f'{file.name}: could not read the complete file: {error}')
        gaps.append('Coverage is limited to selected local records and matching single-file cat calls. Other tools and platforms require separate review.')
        batch = {'rule': RULE, 'vault': str(vault), 'timezone': args.timezone, 'day': str(args.day),
                 'records': [str(file) for file in sorted(files)], 'gaps': gaps, 'candidates': list(candidates.values())}
        output = args.out.expanduser().resolve()
        if output.suffix != '.json' or output in files or output == state_path:
            raise ValueError('Choose a separate output file for the candidate JSON')
        write_json(output, batch)
        result = {'candidates': len(candidates), 'gaps': len(gaps), 'output': str(output)}
    elif args.action == 'week':
        result = weekly(load_state(state_path, vault, args.timezone), args.week, zone)
    elif args.apply:
        lock = vault / '.lifeos/reuse.lock'
        lock.parent.mkdir(exist_ok=True)
        with lock.open('a') as file:
            fcntl.flock(file, fcntl.LOCK_EX)
            result = review(vault, state_path, args.timezone, args.batch, args.selection, True)
    else:
        result = review(vault, state_path, args.timezone, args.batch, args.selection, False)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, AttributeError, ZoneInfoNotFoundError) as error:
        raise SystemExit(f'LifeOS：{error}') from None
