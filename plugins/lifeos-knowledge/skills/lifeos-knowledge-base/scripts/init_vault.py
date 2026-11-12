"""Initialize a Markdown vault from the packaged template, keeping existing files."""
import argparse
from pathlib import Path
from shutil import copyfileobj


def initialize(destination):
    skill_dir = Path(__file__).resolve().parents[1]
    source = skill_dir / "assets" / "vault"
    root = destination.expanduser().resolve()
    if root == skill_dir or skill_dir in root.parents:
        raise ValueError("Choose a vault folder outside the Skill directory.")
    entries = sorted(source.rglob("*"))
    # Preflight the full tree before creating anything in an existing vault.
    if root.exists() and not root.is_dir():
        raise ValueError(f"Destination is not a folder: {root}")
    for item in entries:
        target = root / item.relative_to(source)
        if target.is_symlink() or (target.exists() and (
            (item.is_dir() and not target.is_dir()) or
            (item.is_file() and not target.is_file())
        )):
            raise ValueError(f"Resolve the path conflict: {target}")
    root.mkdir(parents=True, exist_ok=True)
    added, kept = [], []
    for item in entries:
        relative = item.relative_to(source)
        target = root / relative
        if item.is_dir():
            target.mkdir(exist_ok=True)
            continue
        try:
            output = target.open("xb")
        except FileExistsError:
            kept.append(str(relative))
            continue
        try:
            with output, item.open("rb") as input_file:
                copyfileobj(input_file, output)
        except BaseException:
            target.unlink(missing_ok=True)
            raise
        added.append(str(relative))
    print(f"Vault: {root}\nAdded {len(added)} file(s). Kept {len(kept)} existing file(s).")
    if kept:
        print("Kept: " + ", ".join(kept))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="Vault folder chosen by the user")
    args = parser.parse_args()
    try:
        initialize(args.destination)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
