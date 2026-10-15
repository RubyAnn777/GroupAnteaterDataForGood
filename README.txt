REPLICATION FILES: Group Giant Anteater, Data for Good, Question 2 ("How does mining move with enforcement?")
Peru, Operation Mercurio (from February 2019), with Brazil (Yanomami, 2023) as a backup case.

Software:      Python 3.13, managed with uv (https://docs.astral.sh/uv/). Packages and exact versions: pyproject.toml
               and uv.lock (pandas, numpy, matplotlib, pyfixest, geopandas, rasterio, pyproj, scipy, statsmodels,
               rdrobust, openpyxl, markdown). Install once:  uv sync
To reproduce:  uv run python code/main.py        (from this folder; paths are relative to code/)
               Run time: about 3 minutes on a laptop (Apple M-series, 16 GB). Random draws use fixed seeds.
               code/main.py is the ONE file to run. The other .py files in code/ are modules that main.py calls in
               order (definitions, zonedata, checks, peru, ..., slides_figures); do not run them separately.
               Optional check: uv run pytest tests -q  (guards for the shared definitions; 140+ tests).
Output:        output/fig_brief_main.png    the one figure in the brief
               output/brief_numbers.csv     every number in the brief, IN THE ORDER IN WHICH IT APPEARS, with its
                                            measure, zone, period and claim type (written when the brief is built:
                                            uv run python docs/walkthrough/build_report.py --brief)
               output/numbers.csv           every number the code produces (id, value, unit, measure, zone, period,
                                            description, claim type, producing function, source data)
               output/checks.csv            our numbers vs the publishers' numbers (main.py stops if one fails)
               output/peru_levels_and_additions.csv   the required table: mining area (levels) and annual
                                            additions (net, new, re-mined, stopped) by unit and year, 2014-2025
               other output/*.csv and *.png: the tables and figures behind the walkthrough and the slides
Definitions:   code/definitions.py (one place): outcome = net mining additions, ha/yr = new land + re-mined -
               stopped (MapBiomas Peru Collection 4, class 4.2, our pixel accounting); one zone registry (official
               SERNANP buffer zones kept whole); treatment = start of Operation Mercurio, first treated year 2019.
Raw data:      data/              the six course data-pack tables (unchanged)
               data_raw/          every file we added, exactly as downloaded (except the files listed below)
               DOWNLOAD_LOG.csv   one row per raw file (or per set of same-format files): publisher, dataset,
                                  collection, URL, access date, settings, our check number
               data_intermediate/ small tables built by code/ from the large raw files (e.g. zone_year.csv, the
                                  pixel accounting by zone and year); code/ rebuilds them only if they are missing
Left out:      Not in this folder; each has its link in DOWNLOAD_LOG.csv. main.py runs without them, from
               data_intermediate/.
  Over 50 MB:  data_raw/mapbiomas_peru_raster/peru_coverage-col4_YYYY.tif (41 files, ~85 MB each), MapBiomas
               Amazonia Col 6 statistics workbooks and INDIGENOUS_TERRITORIES.zip, Amazon Mining Watch detections,
               AMW illegality areas, IBAMA infraction notices, GLAD-S2 tile, INGEMMET geology tiles, ANM CFEM,
               RAISG protected-area part 300, FUNAI territories.
  Personal data (names, tax IDs): data_raw/reinfo/, data_raw/ingemmet/catastro_*/ (not republished).
  To rebuild data_intermediate/ from scratch, download these into the same paths and delete the intermediates.

Folder structure
  README.txt            this file
  DOWNLOAD_LOG.csv      data log, one row per raw file
  pyproject.toml, uv.lock
  data/                 course data pack
  data_raw/             our downloads, as downloaded
  data_intermediate/    small derived tables
  code/                 main.py + the modules it calls (+ fonts/ for the figures; review/ = teammate's read-only checks)
  output/               the figure, brief_numbers.csv, numbers.csv, checks.csv, all tables and figures
  tests/                guards for the shared definitions
