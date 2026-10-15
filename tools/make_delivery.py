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


PAGES = {"docs/walkthrough/EXPLAINER.html": "EXPLAINER.html", "docs/walkthrough/METHODS.html": "METHODS.html",
         "docs/brief/BRIEF.html": "BRIEF.html"}
INDEX = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Group Giant Anteater, Question 2: pages</title>
<style>body{font-family:Roboto,system-ui,-apple-system,Segoe UI,Arial,sans-serif;background:#f2efea;color:#22383f;margin:0}
main{max-width:760px;margin:0 auto;padding:48px 20px}h1{font-weight:300;font-size:2rem;margin:0 0 6px}p{line-height:1.6}
a.card{display:block;background:#fbfaf7;border:1px solid #d9d2c7;border-top:3px solid #3c7d2c;padding:16px 18px;margin:14px 0;color:#22383f;text-decoration:none}
a.card b{display:block;font-weight:500;font-size:1.1rem;margin-bottom:4px}a.card span{color:#4a5b60}small{color:#6c7b80}</style></head>
<body><main><h1>When the patrols leave</h1>
<p>Data for Good, Question 2 (Operation Mercurio, Peru) · Group Giant Anteater: Ruby Ann Grambauer, Sebastian Schmid, Laurens van der Lely, Omkar Mate, Dhruv Chaudhari.</p>
<a class="card" href="BRIEF.html"><b>The brief</b><span>The two-page brief with references and appendix (also as PDF and Word in deliverables/).</span></a>
<a class="card" href="EXPLAINER.html"><b>Walkthrough</b><span>Every analysis and figure, in the order of the brief and the talk.</span></a>
<a class="card" href="METHODS.html"><b>Methods</b><span>Each method: the question it answers, how it works, what it can't do, where the code lives.</span></a>
<p><small>Offline copies; images are embedded, no internet needed. Online versions: walkthrough https://claude.ai/artifact/VT9wkZqxhH8WAHU4v36mg6 · methods https://claude.ai/artifact/83ZeCu4frkocBDJ46RV1pA · brief https://claude.ai/artifact/NRjV7R75F8Wvogn6Bs3ycJ</small></p>
</main></body></html>
"""


def pages():
    """deliverables/pages/: the three pages side by side, with their local cross-links rewritten, plus index.html."""
    out = DELIV / "pages"
    out.mkdir(parents=True, exist_ok=True)
    for src, dst in PAGES.items():
        html = (ROOT / src).read_text(encoding="utf-8")
        for old in ("../brief/BRIEF.html", "../walkthrough/EXPLAINER.html", "../walkthrough/METHODS.html"):
            html = html.replace(old, old.rsplit("/", 1)[1])
        (out / dst).write_text(html, encoding="utf-8")
    (out / "index.html").write_text(INDEX, encoding="utf-8")


def main():
    DELIV.mkdir(exist_ok=True)
    pages()
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
