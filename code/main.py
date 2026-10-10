"""Single entry point:  uv run python code/main.py   (from anywhere).

Runs top to bottom: source checks -> Peru core analysis -> hooks for Peru protected areas and Brazil.
Writes figures (PNG) and tables (CSV) to output/, and every citable number to output/numbers.csv.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import Numbers, load_pack
import checks, peru, peru_anp, brazil

def main():
    pack = load_pack()
    checks.run_checks(pack)          # raises if any check fails
    reg = Numbers()
    peru.run(pack, reg)
    peru_anp.run(pack, reg)          # TODO hook: runs when the ANP data is added
    brazil.run(pack, reg)            # TODO hook: runs when the Brazil data is added
    reg.save()

if __name__ == "__main__":
    main()
