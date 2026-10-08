ILLEGAL GOLD MINING IN THE AMAZON: DATA PACK
Data for Good, Lessons 3 to 5

START HERE
1. Read the assignment brief and your question card (course page).
2. Run starter/gold_starter.py (Python) or starter/gold_starter.R (R) from inside the
   starter folder. It should print six lines that start with OK and save one figure.
3. Fill in templates/TEAM_PLAN.docx and submit it by the end of the day.

CONTENTS
data/                       six tables, one row per place (or month) and year
  prices_annual.csv         world commodity prices by year (gold in $ per troy ounce)
  prices_monthly.csv        the same by month, to August 2026
  peru_department_year.csv  Peru: department x biome x year; mining and forest area in hectares
  peru_bufferzone_year.csv  Peru: buffer zone of a protected area x department x year
  brazil_municipality_year.csv  Brazil: municipality x state x biome x year
  mining_area.csv           Brazil as a whole, and all indigenous territories combined:
                            mining area by type (artisanal, industrial) and substance
DATA_DICTIONARY.pdf         every variable in every table: definition and unit
DOWNLOAD_LOG.csv            the source of each table, with the publisher's check number.
                            The last row is an example: replace it with your own downloads.
starter/                    gold_starter.py, gold_starter.ipynb, gold_starter.R
templates/                  TEAM_PLAN.docx, REPLICATION_README.txt
how_the_panels_were_built/  the four scripts that produced the tables in data/ from the
                            publishers' raw files. You do not need to run them. They show
                            how each variable was constructed.

VARIABLES
DATA_DICTIONARY.pdf lists every variable in every table, with its definition and unit.
The three you will use most:
mining_ha    hectares in the land-cover class "mining" in that place and year. This includes
             all mining: legal and illegal, artisanal and industrial, gold and other minerals.
forest_ha    hectares in the class group "forest"
total_ha     total hectares of the place (all classes)

NOTES (see "Notes on the data" in the assignment brief)
- Peru: keep biome == "Amazonía". The other biomes contain large industrial mines.
- Brazil: for the Amazon, keep biome == "Amazônia". Identify a municipality by state and
  name together. Where a municipality borders another state, there can be a second row
  for it under that state with a few hectares: drop units with a very small total_ha.
- The tables report levels (area classified as mining in that year). Use annual additions:
  this year's level minus last year's.
- A place can have more than one row per year (one per biome or department). Add up first.

SOURCES
World Bank Commodity Price Data (the "Pink Sheet"), September 2026.
MapBiomas Peru, Collection 4 (1985 to 2025), peru.mapbiomas.org.
MapBiomas Brazil, Collection 10.1 statistics (1985 to 2024) and platform, Collection 11
(1985 to 2025), brasil.mapbiomas.org.
In your brief, cite the publisher and the collection, not this pack.
