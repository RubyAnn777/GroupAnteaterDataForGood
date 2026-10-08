These four scripts turned the publishers' raw files into the tables in data/.
They are here so that you can read exactly how each variable was built. You do not need to run them.
To run them you would need the raw files listed in DOWNLOAD_LOG.csv, saved in a folder called data/ next to the scripts.
  01_prices.py              World Bank Pink Sheet        -> prices_annual.csv, prices_monthly.csv
  02_mapbiomas.py           MapBiomas Brazil platform    -> mining_area.csv
  03_merge_and_describe.py  a first national description for Brazil (not needed for the pack)
  04_panels.py              MapBiomas statistics workbooks -> brazil_municipality_year.csv,
                            peru_department_year.csv, peru_bufferzone_year.csv
