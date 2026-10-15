"""Single entry point:  uv run python code/main.py   (from anywhere).

Runs top to bottom: source checks -> Peru core analysis -> hooks for Peru protected areas and Brazil.
Writes figures (PNG) and tables (CSV) to output/, and every citable number to output/numbers.csv.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import Numbers, load_pack
import checks, peru, peru_robust, peru_anp, brazil
import peru_production, brazil_deter, spatial, brief_figure, peru_synth, spatial_zones, peru_models
import control_amw, control_elevation, control_mb_amazonia, control_select, brazil_deter_all, brazil_stagger
import raster_zones, raster_layers, raster_gold, glad_alerts, v2_tests, v2_stats, v2_extra, control_top3
import brazil_raster, brazil_v2, v2_legality, peru_gold_minem, v2_products_check
import v2_rdd, peru_context_models, placebo_explainer, control_psm, peru_sdid, v2_economics, slides_figures

def main():
    pack = load_pack()
    raster_zones.run()               # v3 zone registry + pixel accounting (rebuilds from rasters only if missing)
    checks.run_checks(pack)          # raises if any check fails
    reg = Numbers()
    peru.run(pack, reg)              # v3: raster net additions + parts, 2x2, displacement, event study
    peru_robust.run(pack, reg)       # alternative controls, drop the largest unit
    peru_anp.run(pack, reg)          # Peru protected areas (our ANP download)
    brazil.run(pack, reg)            # Brazil course tables + indigenous territories
    peru_production.run(pack, reg)
    peru_gold_minem.run(reg)          # correction: official series = declared + artisanal estimate until 2019
    brazil_deter.run(pack, reg)
    spatial.run(reg)                 # AMW robustness (needs data_raw/amw, funai; else reads data_intermediate/)
    peru_synth.run(pack, reg)        # synthetic control, Tambopata BZ (description)
    peru_models.run(pack, reg)       # model ladder: gold price, trends, scaling + placebos
    peru_sdid.run(pack, reg)         # synthetic difference-in-differences on the same 15-zone panel
    spatial_zones.run(reg)           # AMW new area by zone (needs data_intermediate/amw_zone_year.csv)
    # Rule-based comparison area (Ruby's design) and Brazil staggered operations, added 2026-10-11.
    # The first four steps rebuild small intermediates from big raw files only if the intermediates are missing.
    control_amw.run(); control_elevation.run(); control_mb_amazonia.run(); brazil_deter_all.run()
    checks.run_new_data_checks()
    control_select.run(reg)          # four rules -> twin (Amana) -> comparison
    control_psm.run(reg)             # matching estimators (propensity score, Mahalanobis, CEM, entropy balancing)
    brazil_stagger.run(reg)          # each territory vs its own operation date; no-operation pool
    # Plan v2 (2026-10-12): one raster backbone, layered zones (rebuilds from rasters only if intermediates are missing)
    raster_layers.run(reg)           # zone map, stream, Sankey, road bands, corridor share
    raster_gold.run(reg)             # gold-left proxy (geology x first-mined year)
    glad_alerts.run(reg)             # quarterly forest-loss alerts on mining land
    v2_tests.run(pack, reg)          # fake dates, 2012 wave, boundary sensitivity, products, illegal share, spending
    v2_stats.run(reg)                # 1-km cell panel: zone x period DiD, event studies, road gradient (clustered SEs)
    v2_rdd.run(reg)                  # spatial RD (difference in discontinuities) at the road and the reserve border
    peru_context_models.run(pack, reg)   # chapter Context as controls: COVID exposure, enforcement money (2015-25)
    placebo_explainer.run(pack, reg) # one picture of how the placebo tests work
    v2_economics.run(pack, reg)      # gold, taxes, social cost, enforcement money (informed speculation, cited parameters)
    v2_extra.run(reg)                # AMW robustness, old pits by zone, zone profile, risk map, timeline, declared output
    control_top3.run(reg)            # Ruby's three best twins + pre-trend and gap tests
    v2_legality.run(reg)             # MAAP #235 legality levels x first-time mining
    v2_products_check.run(reg)       # why MapBiomas and AMW disagree in the corridor (densification)
    brazil_raster.run(); brazil_v2.run(reg)   # Brazil, same pixel method (Col 11 rasters) + staggered DiD + RI
    brief_figure.run(pack, reg)      # the ONE figure for the brief (v3: net additions + parts)
    slides_figures.run(pack, reg)    # 16:9 slide figures + slide_titles.json for the FZS talk (output/slides/)
    reg.save()

if __name__ == "__main__":
    main()
