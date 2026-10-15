"""Build the delivery: deliverables/ (brief PDF + Word, slides, videos) and two zips in replication/.

Run (after `uv run python code/main.py`, `uv run python docs/walkthrough/build_report.py`, the brief PDF/Word and the
deck build):   uv run python tools/make_delivery.py

1. replication/GroupAnteater_Q2_replication.zip: THE graded replication files, course structure at the root
   (README.txt, DOWNLOAD_LOG.csv, data/, data_raw/, data_intermediate/, code/, output/ + pyproject.toml, uv.lock,
   tests/). Course rule: "Leave out files above 50 MB and give the link in the data log". So every raw file under
   50 MB is included, even if git ignores it for repository size; personal data (names, tax IDs) is never included.
2. replication/GroupAnteater_Q2_all_materials.zip: everything we made (replication files + deliverables/, docs/,
   presentation sources, archive/), without the course's own files (course/), caches, node_modules, files above
   50 MB or personal data.
"""
from __future__ import annotations
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "replication"
DELIV = ROOT / "deliverables"
MAX = 50 * 1024 * 1024
PERSONAL = ("data_raw/reinfo/", "data_raw/ingemmet/catastro_")          # names / tax IDs: never shipped
SKIP_PARTS = {"__pycache__", "node_modules", ".venv", ".git", ".claude", ".pytest_cache", "_artifact", ".ipynb_checkpoints"}
SKIP_NAMES = {".DS_Store"}
REPLICATION = ["README.txt", "DOWNLOAD_LOG.csv", "pyproject.toml", "uv.lock", "data", "data_raw", "data_intermediate",
               "code", "output", "tests"]
ALL = REPLICATION + ["README.md", "agent.md", "CLAUDE.md", "deliverables", "docs", "presentation", "tools", "archive"]

DELIVERABLES = {   # source -> name in deliverables/
    "docs/brief/BRIEF.pdf": "GroupAnteater_Q2_brief.pdf",
    "docs/brief/BRIEF.docx": "GroupAnteater_Q2_brief.docx",
    "presentation/deck/GroupAnteater_FZS_talk.pptx": "GroupAnteater_Q2_slides.pptx",
    "presentation/deck/GroupAnteater_FZS_talk.pdf": "GroupAnteater_Q2_slides.pdf",
    "presentation/animation/out/MapLayers.mp4": "video_map_layers.mp4",
    "presentation/animation/out/MiningTimeline.mp4": "video_mining_timeline.mp4",
}


def keep(p: Path) -> bool:
    rel = p.relative_to(ROOT).as_posix()
    return (p.is_file() and p.name not in SKIP_NAMES and not (SKIP_PARTS & set(p.parts))
            and not rel.startswith(PERSONAL) and p.stat().st_size <= MAX and p.suffix != ".pyc"
            and not rel.startswith("replication/"))


def walk(items):
    for it in items:
        p = ROOT / it
        if p.is_file():
            if keep(p):
                yield p
        elif p.is_dir():
            yield from (q for q in sorted(p.rglob("*")) if keep(q))


def left_out():
    """Raw files we do not ship (for the console report; the README lists them by group)."""
    big = [p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "data_raw").rglob("*")) if p.is_file() and p.stat().st_size > MAX]
    pers = [p for p in PERSONAL if any((ROOT / "data_raw").rglob("*"))]
    return big, pers


def write_zip(name: str, items) -> None:
    OUT.mkdir(exist_ok=True)
    path = OUT / name
    path.unlink(missing_ok=True)
    n = 0
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in walk(items):
            z.write(p, p.relative_to(ROOT).as_posix()); n += 1
    print(f"wrote {path.relative_to(ROOT)}: {n} files, {path.stat().st_size / 1e6:,.0f} MB")


def main():
    DELIV.mkdir(exist_ok=True)
    for src, dst in DELIVERABLES.items():
        s = ROOT / src
        if s.exists():
            shutil.copy2(s, DELIV / dst)
        else:
            print(f"MISSING deliverable: {src}")
    big, _ = left_out()
    print(f"left out (> 50 MB, linked in DOWNLOAD_LOG.csv): {len(big)} files; personal data folders: {', '.join(PERSONAL)}")
    write_zip("GroupAnteater_Q2_replication.zip", REPLICATION)
    write_zip("GroupAnteater_Q2_all_materials.zip", ALL)


if __name__ == "__main__":
    main()
