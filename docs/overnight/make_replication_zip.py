"""Build replication/GroupAnteater_Q2_replication.zip in the course structure.
Run:  uv run python docs/overnight/make_replication_zip.py
"""
import re, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "replication" / "GroupAnteater_Q2_replication.zip"
BIG = {  # not included (> 50 MB); linked in DOWNLOAD_LOG.csv
    "data_raw/amw/amazon_basin_detections.geojson",
    "data_raw/ibama/auto_infracao_csv.zip",
    "data_raw/funai/tis_poligonais.geojson",
}
SKIP_NAMES = {".DS_Store"}


def files(sub):
    for p in sorted((ROOT / sub).rglob("*")):
        rel = p.relative_to(ROOT).as_posix()
        if (not p.is_file() or p.name in SKIP_NAMES or "__pycache__" in p.parts
                or rel in BIG or p.suffix == ".pyc"):
            continue
        yield p, rel


def lock_version(pkg):
    txt = (ROOT / "uv.lock").read_text()
    m = re.search(rf'name = "{pkg}"\nversion = "([^"]+)"', txt)
    return m.group(1) if m else "?"


def describe(name):
    n = name
    if n == "numbers.csv": return "every number cited in the brief (id, value, source/definition), in order of appearance"
    if n == "checks.csv" or n.endswith("_check.csv") or n == "brazil_checks.csv":
        return "source checks: our number vs the publisher's number"
    if n == "fig_brief_main.png": return "THE figure in the brief"
    if n.startswith("fig_") and n.endswith(".png"):
        return "supporting figure (" + n[4:-4].replace("_", " ") + ")"
    if n.startswith("fig_") and n.endswith(".csv"): return "table behind a figure (" + n[4:-4].replace("_", " ") + ")"
    if n.endswith(".csv"): return "table: " + n[:-4].replace("_", " ")
    return "output file"


def readme():
    py = f"{sys.version_info.major}.{sys.version_info.minor}"
    pk = ", ".join(f"{p} {lock_version(p)}" for p in
                   ["pandas", "matplotlib", "pyfixest", "geopandas", "scipy", "openpyxl", "markdown"])
    outs = "\n".join(f"               output/{rel.split('/',1)[1]:<44} {describe(p.name)}"
                     for p, rel in files("output"))
    big = "\n".join(f"               {b}" for b in sorted(BIG))
    return f"""REPLICATION FILES: Group Giant Anteater, Question 2, Peru (Operation Mercurio) and Brazil (Yanomami / indigenous territories)

Software:      Python {py} managed with uv (https://docs.astral.sh/uv/). Key packages (exact versions in uv.lock):
               {pk}
               The full dependency list is in pyproject.toml; uv.lock pins every version.
To reproduce:  from the root of this folder (the one containing code/), run
                   uv sync
                   uv run python code/main.py
               Run time: about 1 minute.
               code/main.py is the ONE script. The other .py files in code/ are modules that main.py imports
               (common, checks, peru, peru_anp, peru_robust, peru_synth, peru_production, brazil, brazil_deter,
               brazil_ibama, spatial, spatial_zones, brief_figure); do not run them separately.
               Paths are resolved relative to code/, so keep code/, data/, data_raw/, data_intermediate/ and
               output/ side by side at the root.
Output:        output/fig_brief_main.png   the figure in the brief
               output/numbers.csv          every number in the brief, in the order in which it appears
               All files written to output/ by main.py:
{outs}
Raw data:      data/ holds the six course data-pack tables (the course's raw inputs, unchanged).
               data_raw/ contains every file we added, exactly as downloaded. DOWNLOAD_LOG.csv has one row per file.
               data_intermediate/ holds small tables derived from the three large files below.
Left out:      three raw files above 50 MB, not included; each is linked in DOWNLOAD_LOG.csv:
{big}
               Without them main.py still runs to the end: it reads the precomputed tables in data_intermediate/
               (AMW rings and zones, IBAMA annual counts) and skips the two maps
               (output/fig_map_madre_de_dios.png, output/fig_map_yanomami.png), which are then kept
               as shipped in output/ (not regenerated). To regenerate everything, download the three files from the
               links in DOWNLOAD_LOG.csv into the same paths under data_raw/.

Folder structure
  README.txt
  DOWNLOAD_LOG.csv
  pyproject.toml, uv.lock       software environment
  data/                         course data pack (six tables)
  data_raw/                     files added by us, as downloaded
  data_intermediate/            small derived tables (from the large files)
  code/                         main.py (entry point) + modules
  output/                       the figure + every number in the brief
  docs/overnight/notes/         two small reference tables that code/ reads as cross-checks
"""


def main():
    OUT.parent.mkdir(exist_ok=True)
    OUT.unlink(missing_ok=True)
    n = 0
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.txt", readme())
        for f in ["DOWNLOAD_LOG.csv", "pyproject.toml", "uv.lock"]:
            z.write(ROOT / f, f); n += 1
        # cross-check reference tables that code/ reads from docs/overnight/notes/
        for name in ["deter_mining_ti_annual_km2.csv", "ibama_annual.csv"]:
            f = ROOT / "docs" / "overnight" / "notes" / name
            if f.exists():
                z.write(f, f"docs/overnight/notes/{name}"); n += 1
        for sub in ["data", "data_raw", "data_intermediate", "code", "output"]:
            for p, rel in files(sub):
                z.write(p, rel); n += 1
    print(f"wrote {OUT} ({OUT.stat().st_size/1e6:.1f} MB, {n+1} files)")


if __name__ == "__main__":
    main()
