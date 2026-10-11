"""Single entry point:  uv run python code/main.py   (from anywhere).

Runs top to bottom: source checks -> Peru core analysis -> hooks for Peru protected areas and Brazil.
Writes figures (PNG) and tables (CSV) to output/, and every citable number to output/numbers.csv.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import Numbers, load_pack
import checks, peru, peru_anp, brazil
import peru_production, brazil_deter, spatial, brief_figure, peru_synth, spatial_zones, peru_models
import control_amw, control_elevation, control_mb_amazonia, control_select, brazil_deter_all, brazil_stagger

def main():
    pack = load_pack()
    checks.run_checks(pack)          # raises if any check fails
    reg = Numbers()
    peru.run(pack, reg)
    peru_anp.run(pack, reg)          # TODO hook: runs when the ANP data is added
    brazil.run(pack, reg)            # TODO hook: runs when the Brazil data is added
    peru_production.run(pack, reg)
    brazil_deter.run(pack, reg)
    spatial.run(reg)                 # AMW robustness (needs data_raw/amw, funai; else reads data_intermediate/)
    peru_synth.run(pack, reg)        # synthetic control, Tambopata BZ (description)
    peru_models.run(pack, reg)       # model ladder: gold price, trends, scaling + placebos
    spatial_zones.run(reg)           # AMW new area by zone (needs data_intermediate/amw_zone_year.csv)
    # Rule-based comparison area (Ruby's design) and Brazil staggered operations, added 2026-10-11.
    # The first four steps rebuild small intermediates from big raw files only if the intermediates are missing.
    control_amw.run(); control_elevation.run(); control_mb_amazonia.run(); brazil_deter_all.run()
    checks.run_new_data_checks()
    control_select.run(reg)          # four rules -> twin (Amana) -> comparison
    brazil_stagger.run(reg)          # each territory vs its own operation date; no-operation pool
    brief_figure.run(pack)           # the ONE figure for the brief (needs peru + peru_anp modules only)
    reg.save()

if __name__ == "__main__":
    main()
