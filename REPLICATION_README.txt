REPLICATION FILES: Group Giant Anteater, Question 2 ("How does mining move with enforcement?"), Peru and Brazil
(Goes into the replication zip as README.txt.)

Software:      Python 3.13 with pandas 3.0, matplotlib 3.11, pyfixest 0.60, geopandas, rasterio, rdrobust, statsmodels;
               exact versions pinned in uv.lock. Install: `uv sync` in the project folder.
To reproduce:  uv run python code/main.py   (from the project folder or anywhere; paths are relative to the repo).
               Run time: about 3 minutes on a laptop. Random draws (bootstrap, placebos) use fixed seeds.
Output:        output/fig_brief_main.png   the one figure in the brief (code/brief_figure.py)
               output/numbers.csv          every number in the brief: id, value, unit, description, claim type
                                           (description / prediction / causal), producing function, source data.
                                           The brief source docs/brief/brief_content.md cites numbers by id
                                           ({{id}}), in order of appearance; build with
                                           uv run python docs/overnight/build_report.py
               output/checks.csv           our number vs the publisher's number, one row per dataset
Raw data:      data_raw/ contains every file exactly as downloaded. DOWNLOAD_LOG.csv has one row per file
               (URL, access date, collection, sha256, check number).

Left out (each is in DOWNLOAD_LOG.csv with its link). The code does not need them: it reads the small
intermediates in data_intermediate/ that were built from them, and rebuilds those only if they are missing.
  Over 50 MB:
    data_raw/mapbiomas_peru_raster/peru_coverage-col4_YYYY.tif   MapBiomas Peru Col 4 rasters, 41 files, ~85 MB each
    data_raw/mapbiomas_amazonia/statistics_amazonia_col6_*.xlsx  MapBiomas Amazonia Col 6 statistics, ~250 MB each
    data_raw/mapbiomas_amazonia/INDIGENOUS_TERRITORIES.zip       59 MB; Madre de Dios subset kept in
                                                                 data_intermediate/native_communities_mdd.geojson
    data_raw/amw/amazon_basin_detections.geojson                 Amazon Mining Watch, 108 MB
    data_raw/amw_github/illegality_v2_areas_simplified.geojson   66 MB
    data_raw/ibama/auto_infracao_csv.zip                         IBAMA infraction notices, 117 MB
    data_raw/glad_alerts/S2alert_alertDate_*.tif                 GLAD-S2 tile, 122 MB; its 3 numbers (s2_lp_west_*)
                                                                 are kept in data_intermediate/raw_only_numbers.csv
    data_raw/ingemmet/geologia_100k_mdd_tiles/                   INGEMMET geology tiles, 316 MB in total
    data_raw/anm_cfem/*.csv                                      61 MB (and a 29 MB companion file)
  Many files, large in total (each under 50 MB): GLAD-L alert tiles (data_raw/glad_alerts/*.tif), RAISG protected
    areas (data_raw/raisg/anp_nacionales_part*.geojson), FUNAI territories (47 MB), ANM SIGMINE chunks,
    MININTER police production CSV, MINEM .7z archives.
  Personal data (names, tax IDs; kept local): data_raw/reinfo/, data_raw/ingemmet/catastro_*/.
  The La Pampa location check (sp_lp_*) needs the AMW file; its 4 numbers are also kept in
  data_intermediate/raw_only_numbers.csv.

Folder structure
  README.txt            this file
  DOWNLOAD_LOG.csv      one row per raw file
  data_raw/             every file as downloaded (except the ones listed above)
  data_intermediate/    small tables built from the large raw files (rebuilt by code/ if missing)
  code/                 main.py runs everything top to bottom; one module per step
  output/               the figure, numbers.csv, checks.csv and the tables behind every number
