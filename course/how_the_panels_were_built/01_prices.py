# %% [markdown]
# # 01 · Commodity prices from the World Bank Pink Sheet
#
# **What this script does.** Reads the World Bank's monthly commodity price file
# ("Pink Sheet"), keeps gold and a handful of comparison commodities, and writes two
# tidy tables (monthly and annual) plus one figure. Everything downstream (mining area
# vs. price) merges onto the annual table by `year`.
#
# **Why comparison commodities.** If mining area in the Amazon tracks silver and copper
# as closely as it tracks gold, then "the gold price" is standing in for a general
# commodity or macro cycle and cannot be given a gold-specific reading. Silver is the
# "too close" comparison (it co-moves with gold as a monetary metal); copper is the
# industrial-cycle comparison; iron ore and crude oil are unrelated to gold mining and
# serve as controls for the general cycle.
#
# **How to run.** In Google Colab: File → Upload notebook, then upload
# `CMO-Historical-Data-Monthly.xlsx` with the folder icon on the left, and run the cells
# top to bottom (Runtime → Run all). Locally (VS Code or JupyterLab): put the xlsx in a
# `data/` folder next to this file and run the cells.
#
# **Stata translation for the instructor.** `pd.read_excel` = `import excel`;
# `df[cols]` = `keep`; `.replace('..', np.nan)` = `destring, replace ignore("..")`;
# `.groupby('year').mean()` = `collapse (mean) ..., by(year)`; `.to_csv` = `export delimited`.

# %%
import pandas as pd            # tables ("dataframes"): the pandas equivalent of a Stata dataset
import numpy as np             # numeric helpers (NaN, log)
import matplotlib.pyplot as plt  # figures
from pathlib import Path       # file paths that work on Mac and Windows

# ---- Settings you may change -------------------------------------------------------
DATA_FILE = Path("data/CMO-Historical-Data-Monthly.xlsx")   # where the Pink Sheet is
OUT_DIR   = Path("output")                                  # where results are written
OUT_DIR.mkdir(exist_ok=True)

# Columns to keep, as they are spelled in row 5 of the sheet "Monthly Prices".
# The dictionary maps the Pink Sheet name -> a short name we use from here on.
KEEP = {
    "Gold":               "gold",       # $/troy oz
    "Silver":             "silver",     # $/troy oz
    "Platinum":           "platinum",   # $/troy oz
    "Copper":             "copper",     # $/mt
    "Tin":                "tin",        # $/mt  (note: tin IS mined artisanally in Rondônia, so not a clean placebo)
    "Iron ore, cfr spot": "iron_ore",   # $/dmtu
    "Crude oil, average": "oil",        # $/bbl
}
BASE_YEAR = 2018   # index year: 2018 = 100, chosen because AMW detections start in 2018

# %% [markdown]
# ## 1. Read the file
#
# The sheet "Monthly Prices" has a fixed layout: rows 1–4 are titles, row 5 has the
# commodity names, row 6 the units, row 7 the World Bank codes, and data start in row 8.
# The first column holds the month as text like `1960M01`. Missing values are written
# as `..`. We tell pandas to use row 5 as the header (`header=4`, because pandas counts
# from 0) and to skip the two rows below it.

# %%
raw = pd.read_excel(
    DATA_FILE,
    sheet_name="Monthly Prices",
    header=4,              # row 5 in Excel = index 4 in pandas
    skiprows=[5, 6],       # drop the units row and the code row (Excel rows 6 and 7)
    na_values=[".."],      # treat '..' as missing
)
raw = raw.rename(columns={raw.columns[0]: "month"})   # first column has no name; call it 'month'
raw = raw.dropna(subset=["month"])                    # drop empty trailing rows
print("Rows read:", len(raw), "| first month:", raw["month"].iloc[0], "| last month:", raw["month"].iloc[-1])

# Sanity check: every column we asked for must exist. If the World Bank renames a
# column this will fail loudly here rather than silently later.
missing = [c for c in KEEP if c not in raw.columns]
assert not missing, f"Columns not found in the file: {missing}"

# %% [markdown]
# ## 2. Keep what we need and tidy it
#
# We keep only the chosen commodities, convert the month text into a real date, and add
# a `year` column for the annual merge later.

# %%
monthly = raw[["month"] + list(KEEP)].rename(columns=KEEP).copy()

# '1960M01' -> a date. pandas needs a format string: %Y = 4-digit year, %m = 2-digit month.
monthly["date"] = pd.to_datetime(monthly["month"], format="%YM%m")
monthly["year"] = monthly["date"].dt.year
monthly = monthly.drop(columns="month").set_index("date").sort_index()

# All price columns should now be numbers. If one is still 'object' (text), something
# in the file changed. (A column with no missing values may be read as integer; that is fine.)
assert all(pd.api.types.is_numeric_dtype(monthly[c]) for c in KEEP.values()), monthly.dtypes
price_cols = list(KEEP.values())                 # the short names, used from here on
monthly[price_cols] = monthly[price_cols].astype(float)

monthly.tail(3)

# %% [markdown]
# ## 3. Annual averages and an index
#
# The mining data are annual, so we average the twelve months of each year. We also
# express each series as an index (2018 = 100) so that gold at ~$1,300/oz and copper at
# ~$6,500/mt can be drawn on one axis, and we take logs because the questions are about
# proportional changes ("a 10 % higher price").

# %%
annual = monthly.groupby("year")[price_cols].mean()

# Drop the current, incomplete year: an average over 3 months is not comparable.
n_months = monthly.groupby("year").size()
annual = annual[n_months == 12]

# Index: divide each column by its value in BASE_YEAR and multiply by 100.
index = annual.div(annual.loc[BASE_YEAR]) * 100
index.columns = [c + "_idx" for c in price_cols]

# Logs of nominal prices. Note: NOMINAL. Real prices would divide by a US price index;
# the annual Pink Sheet file has real series if a team wants them.
logs = np.log(annual)
logs.columns = ["ln_" + c for c in price_cols]

annual_out = pd.concat([annual, index, logs], axis=1)
annual_out.loc[2015:2020, ["gold", "gold_idx", "ln_gold", "copper_idx"]]

# %% [markdown]
# ## 4. Check against the source
#
# Before using any number, compare one of ours with one the publisher prints. The Pink
# Sheet's own annual file reports annual averages; the April 2026 CMO precious-metals
# figure indexes gold to December 2024 = 100. Here we print two values to compare by
# hand. (September 2026 file: last observation 2026M08.)

# %%
print("Gold, monthly, last observation:", monthly["gold"].dropna().index[-1].strftime("%Y-%m"),
      "=", round(monthly["gold"].dropna().iloc[-1], 2), "$/troy oz")
print("Gold, annual average", BASE_YEAR, "=", round(annual.loc[BASE_YEAR, "gold"], 2), "$/troy oz")

# %% [markdown]
# ## 5. Figure: gold against its comparison commodities
#
# Left: index levels since 1985 (the MapBiomas start year). Right: year-on-year log
# change, which is what a "supply response to price" regression actually uses. If the
# right-hand lines move together, the price series cannot separate a gold story from a
# commodity-cycle story.

# %%
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
show = ["gold", "silver", "copper", "oil"]

sub = index.loc[1985:]
for c in show:
    ax[0].plot(sub.index, sub[c + "_idx"], label=c, linewidth=2 if c == "gold" else 1.2)
ax[0].axhline(100, color="grey", linewidth=0.6)
ax[0].set_title(f"Annual average price, index {BASE_YEAR} = 100")
ax[0].legend(frameon=False)

dl = logs.loc[1985:].diff()
for c in show:
    ax[1].plot(dl.index, dl["ln_" + c], label=c, linewidth=2 if c == "gold" else 1.2)
ax[1].axhline(0, color="grey", linewidth=0.6)
ax[1].set_title("Year-on-year change in log price")

for a in ax:
    a.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(OUT_DIR / "fig_prices.png", dpi=150)

# Print the correlation of annual log changes: the number behind the picture.
print("Correlation of annual log changes, 1985 onward:")
print(dl[["ln_" + c for c in show]].corr().round(2))

# %% [markdown]
# ## 6. Save the tidy tables
#
# `prices_annual.csv` is the file the other notebooks merge on `year`.

# %%
monthly.to_csv(OUT_DIR / "prices_monthly.csv")
annual_out.to_csv(OUT_DIR / "prices_annual.csv")
print("Written:", [p.name for p in OUT_DIR.iterdir()])
