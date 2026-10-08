# %% [markdown]
# # Gold mining in the Amazon: starter
#
# Data for Good, Sessions 3 to 5. Run this once, top to bottom, before you do anything else.
#
# It does four things:
#
# 1. loads the six shared tables and reproduces the numbers the publishers show (if a
#    check fails, stop and find out why before you go on);
# 2. shows the difference between a **level** (hectares classified as mining in a year)
#    and an **addition** (the change from the year before);
# 3. builds a **before/after table with a comparison group**;
# 4. draws **one figure** in a plain style.
#
# Needs only `pandas` and `matplotlib`. Run it from the `starter` folder. Use any software
# you like for your own work; `gold_starter.R` does the same steps in R.

# %%
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

DATA = Path("../data") if Path("../data").exists() else Path("data")

prices_m = pd.read_csv(DATA / "prices_monthly.csv")           # world prices, one row per month
prices   = pd.read_csv(DATA / "prices_annual.csv")            # world prices, one row per year
substance = pd.read_csv(DATA / "mining_area.csv")             # Brazil: mining by type and substance
br = pd.read_csv(DATA / "brazil_municipality_year.csv")       # Brazil: municipality x biome x year
pe = pd.read_csv(DATA / "peru_department_year.csv")           # Peru: department x biome x year
zb = pd.read_csv(DATA / "peru_bufferzone_year.csv")           # Peru: buffer zone x department x year

for name, df in [("prices_monthly", prices_m), ("prices_annual", prices), ("mining_area", substance),
                 ("brazil_municipality_year", br), ("peru_department_year", pe), ("peru_bufferzone_year", zb)]:
    print(f"{name:28s} {len(df):>8,} rows   {list(df.columns)[:8]}")

# %% [markdown]
# ## 1. Check against the source
#
# Each number below can be read off the publisher's own screen (see `DOWNLOAD_LOG.csv`).
# Your brief reports one such check for every dataset you use, including the ones you add.

# %%
def check(label, value, expected):
    ok = abs(value - expected) < 1
    print(f"{'OK  ' if ok else 'FAIL'} {label:62s} {value:>12,.0f}   (publisher: {expected:,.0f})")
    assert ok, f"{label}: got {value:,.0f}, expected {expected:,.0f}"

check("Gold price, August 2026, $ per troy ounce",
      prices_m["gold"].iloc[-1], 4411)
check("Brazil, mining class, all municipalities, 2024, ha",
      br.loc[br["year"] == 2024, "mining_ha"].sum(), 609637)
check("Peru, Madre de Dios, mining class, 2025, ha",
      pe.loc[(pe["department"] == "Madre de Dios") & (pe["year"] == 2025), "mining_ha"].sum(), 112622)
check("Peru, Tambopata buffer zone, mining class, 2025, ha",
      zb.loc[(zb["buffer_zone"] == "Tambopata") & (zb["year"] == 2025), "mining_ha"].sum(), 20730)
check("Brazil, artisanal mining (garimpo), 2025, ha",
      substance.loc[(substance["territory"] == "Brasil") & (substance["year"] == 2025), "mining_artisanal_ha"].sum(), 445987)
check("Brazil, artisanal mining in all indigenous lands, 2025, ha",
      substance.loc[(substance["territory"] == "all indigenous lands combined") & (substance["year"] == 2025),
                    "mining_artisanal_ha"].sum(), 39915)

# %% [markdown]
# ## 2. Levels and additions
#
# The satellite product records the area **currently classified as mining**. That is a stock.
# It almost never falls, so it trends upwards, and so does the gold price. Two series that
# both trend upwards are correlated whatever the truth is. The quantity that answers "how
# much new mining was there this year?" is the **addition**: this year's level minus last
# year's.
#
# A department can appear in several rows per year (one per biome), so add up first.

# %%
mdd = (pe[pe["department"] == "Madre de Dios"]
       .groupby("year", as_index=False)["mining_ha"].sum()      # one row per year
       .merge(prices[["year", "gold"]], on="year"))             # add the gold price
mdd["addition_ha"] = mdd["mining_ha"].diff()                    # level minus last year's level
print(mdd[mdd["year"] >= 2010].round(0).to_string(index=False))

# %% [markdown]
# ## 3. Before and after, with a comparison group
#
# Operation Mercurio (February 2019) targeted La Pampa, which lies in the buffer zone of the
# Tambopata National Reserve. The Amarakaeri buffer zone, the other large mining front in
# Madre de Dios, was not targeted. Four numbers: the mean annual addition in each zone,
# in the three years before and the three years after.
#
# The last line is a difference in differences computed by hand. It is a description.
# See "Why it could mislead" on the Question 2 card before you interpret it.

# %%
zones = (zb[zb["buffer_zone"].isin(["Tambopata", "Amarakaeri"])]
         .groupby(["buffer_zone", "year"], as_index=False)["mining_ha"].sum())   # a zone can span two departments
zones["addition_ha"] = zones.groupby("buffer_zone")["mining_ha"].diff()
zones["period"] = pd.cut(zones["year"], bins=[2015, 2018, 2021], labels=["2016-18", "2019-21"])

table = zones.dropna(subset=["period"]).pivot_table(index="buffer_zone", columns="period",
                                                    values="addition_ha", aggfunc="mean", observed=True)
table["change"] = table["2019-21"] - table["2016-18"]
print(table.round(0))
print("Change in Tambopata minus change in Amarakaeri:",
      round(table.loc["Tambopata", "change"] - table.loc["Amarakaeri", "change"]), "ha per year")

# %% [markdown]
# ## 4. One figure
#
# Two panels with a common time axis (not two y-axes in one panel), a title, and the
# source underneath. Your brief has one figure, which should make your main point.

# %%
plot = mdd[mdd["year"] >= 2001]
fig, (top, bottom) = plt.subplots(2, 1, figsize=(8, 5.5), sharex=True, gridspec_kw={"height_ratios": [1, 1.4]})

top.plot(plot["year"], plot["gold"], color="#234A76", linewidth=2)
top.set_ylabel("Gold price\n($ per troy ounce)")
top.set_ylim(0, None)
top.set_title("Madre de Dios: the gold price and the new mining area each year", loc="left")

bottom.bar(plot["year"], plot["addition_ha"], color="#F28E2B", edgecolor="#E67E22", width=0.8)
bottom.set_ylabel("New mining area\nin the year (ha)")

for ax in (top, bottom):                      # two panels, one x-axis: never two y-axes on one panel
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, color="#E8EEF0"); ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: f"{v:,.0f}"))

fig.text(0.01, 0.01, "Sources: MapBiomas Peru, Collection 4 (class 4.2 Mineria); World Bank Pink Sheet, September 2026.",
         fontsize=8, color="#555555")
fig.tight_layout(rect=(0, 0.04, 1, 1))
Path("output").mkdir(exist_ok=True)
fig.savefig("output/starter_figure.png", dpi=200)
print("Saved output/starter_figure.png")

# %% [markdown]
# ## What next
#
# - Open your question card. Do the "Describe" step for your own units and years.
# - Download the table your card asks you to add. Add one row for it to `DOWNLOAD_LOG.csv`
#   and write a `check(...)` line for it like the ones above.
# - Keep everything in one script or notebook that runs from top to bottom. That file,
#   the log and your raw downloads are your replication folder.
