# %% [markdown]
# # 02 · Mining area from a MapBiomas statistics download
#
# **What this script does.** Reads a CSV downloaded from the MapBiomas platform
# (Statistics tab → download icon → Table (.csv)), turns its class hierarchy into a tidy
# long table, pulls out the gold rows, and writes `output/mining_area.csv`.
#
# **Two download shapes.** The platform offers two CSVs per panel:
# * the *class breakdown for one year* (columns `Level 1..4` and one year column, e.g. `2025`);
# * the *time series* (same `Level` columns and one column per year, `1985` … `2025`).
#
# The code handles both: it finds every column whose name is a four-digit year and
# reshapes them into a `year` column (`melt` = Stata `reshape long`).
#
# **What the hierarchy means (Brazil, Collection 11).** Level 1 = Artisanal Mining vs.
# Industrial; Level 2 = area with exposed soil vs. area with revegetation (old scars that
# have greened over — still mapped as mining); Level 3 = substance group (Metallic,
# Non-metallic, …); Level 4 = the substance (Gold, Tin, Copper, …). A row with an empty
# Level 2 is a subtotal of everything below it. So the file contains totals AND their
# parts: never sum across rows without filtering a level, or you double count.
#
# **Stata translation.** `pd.read_csv` = `import delimited`; `melt` = `reshape long`;
# `query()` = `keep if`; `pivot_table` = `collapse (sum)` + `reshape wide`.

# %%
import pandas as pd
import re
from pathlib import Path

DATA_DIR = Path("data")               # platform CSVs live in data/mapbiomas/, one per territory
OUT_DIR  = Path("output"); OUT_DIR.mkdir(exist_ok=True)

# The MapBiomas CSV does not say which territory it is for, so the file NAME carries it,
# and data/DOWNLOAD_LOG.csv records who downloaded what, when, with which settings, and
# the number seen on screen. That log is the provenance record for every raw file in
# data/; a file that is not in the log is not used. Here we take the platform downloads.
log = pd.read_csv(DATA_DIR / "DOWNLOAD_LOG.csv").query("source == 'mapbiomas_platform'")
print(log[["file", "territory", "check_number"]].to_string(index=False))

# %% [markdown]
# ## 1. Read and reshape to long

# %%
pieces = []
for _, row in log.iterrows():
    raw = pd.read_csv(DATA_DIR / row["file"], encoding="utf-8-sig")   # utf-8-sig strips the invisible BOM before "Level 1"
    level_cols = [c for c in raw.columns if c.startswith("Level")]
    year_cols  = [c for c in raw.columns if re.fullmatch(r"\d{4}", str(c))]
    assert level_cols and year_cols, f"{row['file']}: unexpected columns {list(raw.columns)}"
    part = raw.melt(id_vars=level_cols, value_vars=year_cols, var_name="year", value_name="area_ha")
    part["territory"] = row["territory"]
    pieces.append(part)
    print(f"{row['file']}: {len(year_cols)} years ({year_cols[0]}–{year_cols[-1]}), {len(raw)} class rows")

long = pd.concat(pieces, ignore_index=True)             # stack the territories (Stata: append)
long["year"] = long["year"].astype(int)
long[level_cols] = long[level_cols].fillna("")          # empty cells mark subtotal rows

# 'depth' says how far down the hierarchy a row sits: 1 = Level-1 subtotal, 4 = a substance.
long["depth"] = (long[level_cols] != "").sum(axis=1)

# %% [markdown]
# ## 2. Check the hierarchy adds up
#
# The Level-1 subtotal must equal the sum of its Level-2 rows, and so on. If this fails,
# the download is truncated or the platform changed its layout.

# %%
for terr, d in long[long["year"] == long["year"].max()].groupby("territory"):
    top    = d[d["depth"] == 1].set_index("Level 1")["area_ha"]
    parts  = d[d["depth"] == 2].groupby("Level 1")["area_ha"].sum()
    diff   = (top - parts).abs().max()
    print(f"{terr}: Level-1 totals vs. sum of Level-2 parts, max difference = {diff:.1f} ha")
    assert diff < 1, f"{terr}: hierarchy does not add up"

# %% [markdown]
# ## 3. Gold — and "No Substance"
#
# Gold appears at Level 4 under both Artisanal and Industrial, and under both "exposed
# soil" and "revegetation". For the frontier question we want *artisanal, all soil states*
# (a revegetated scar is still a scar); the split is kept so a team can argue otherwise.
#
# "No Substance" means MapBiomas found no matching mining process in the ANM registry.
# Inside indigenous lands, where mining is prohibited and nothing is registered, most
# garimpo is "No Substance" (27,875 of 39,915 ha in 2025) whatever is being dug. So the
# working measure of *illegal artisanal gold* is Gold + No Substance under Artisanal;
# both are kept so the brief can show how much the definition matters.

# %%
gold = (long.query("`Level 4` == 'Gold'")
            .pivot_table(index=["territory", "year"], columns=["Level 1", "Level 2"],
                         values="area_ha", aggfunc="sum"))
gold.columns = [f"{a.split()[0].lower()}_{'exposed' if 'Exposed' in b else 'reveg'}" for a, b in gold.columns]
gold["gold_artisanal_ha"] = gold.filter(like="artisanal").sum(axis=1)
gold["gold_industrial_ha"] = gold.filter(like="industrial").sum(axis=1)

nosub = (long.query("`Level 4` == 'No Substance' and `Level 1` == 'Artisanal Mining'")
             .groupby(["territory", "year"])["area_ha"].sum().rename("nosubstance_artisanal_ha"))
gold = gold.join(nosub)
gold["gold_or_nosub_artisanal_ha"] = gold["gold_artisanal_ha"] + gold["nosubstance_artisanal_ha"].fillna(0)

# Totals for all mining, all substances (Level-1 subtotals), for the "how much is gold" share.
tot = (long[long["depth"] == 1].pivot_table(index=["territory", "year"], columns="Level 1", values="area_ha"))
tot.columns = ["mining_artisanal_ha", "mining_industrial_ha"]

out = gold.join(tot)
out["gold_share_of_artisanal"] = out["gold_artisanal_ha"] / out["mining_artisanal_ha"]
out.xs(out.index.get_level_values("year").max(), level="year").round(0)

# %% [markdown]
# ## 4. Check against the source
#
# The platform's Statistics panel showed, for Brasil 2025: Artisanal Mining 445,987 ha
# and Industrial 243,865 ha; for all indigenous lands, Artisanal 39,915 ha. Our Level-1
# totals must reproduce the numbers written in DOWNLOAD_LOG.csv for each file.

# %%
last = out.index.get_level_values("year").max()
print(out.xs(last, level="year")[["mining_artisanal_ha", "mining_industrial_ha", "gold_artisanal_ha", "gold_or_nosub_artisanal_ha"]].round(0))

# %%
out.to_csv(OUT_DIR / "mining_area.csv")
print("Written output/mining_area.csv with", len(out), "territory-year rows")
