# %% [markdown]
# # 03 · Merge mining area with prices and describe (Q1, first pass)
#
# **What this script does.** Joins `output/mining_area.csv` (from 02) to
# `output/prices_annual.csv` (from 01) on `year`, then produces the descriptive
# objects Q1 needs: the level series side by side, annual *additions* to mining area
# against the annual *change* in the gold price, and the same for the comparison
# commodities. Ends with a small regression table, clearly labelled as description.
#
# **Why additions, not levels.** MapBiomas mining area is close to a cumulative footprint:
# a scar usually stays classified as mining (or "revegetated mining"), so the level mostly
# rises and falls only when an old scar is reclassified. What can respond to price is the
# *flow* — new hectares this year. Regressing a level on a
# rising price gives a spurious fit; regressing additions on price changes is at least
# the right object. It is still a description: eight to forty annual points, one
# country, no counterfactual.
#
# **Stata translation.** `merge(on="year")` = `merge 1:1 year using`; `.diff()` = `D.`;
# `smf.ols("y ~ x", df).fit()` = `regress y x`; `.shift(1)` = `L.`.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from pathlib import Path

OUT_DIR   = Path("output")
TERRITORY = "Brasil"     # mining_area.csv holds several territories; this notebook describes one
mining = pd.read_csv(OUT_DIR / "mining_area.csv").query("territory == @TERRITORY")
prices = pd.read_csv(OUT_DIR / "prices_annual.csv")
assert len(mining) > 0, f"No rows for territory {TERRITORY!r}; check DOWNLOAD_LOG.csv for the exact spelling"

# %% [markdown]
# ## 1. Merge and build the flow variables

# %%
df = mining.merge(prices, on="year", how="inner", validate="1:1")   # validate: stops if year is not unique on either side (e.g. two territories left in)
print("Merged years:", df["year"].min(), "to", df["year"].max(), "|", len(df), "rows")

df = df.sort_values("year").reset_index(drop=True)
df["gold_add_ha"]   = df["gold_artisanal_ha"].diff()          # new artisanal-gold hectares this year
df["ln_gold_add"]   = np.log(df["gold_add_ha"].clip(lower=1))  # log of additions (clip guards against 0/negative)
for c in ["gold", "silver", "copper", "oil"]:
    df[f"dln_{c}"]    = df[f"ln_{c}"].diff()                    # annual log change in price
    df[f"dln_{c}_l1"] = df[f"dln_{c}"].shift(1)                 # lagged one year: miners respond with delay

# %% [markdown]
# ## 2. Figure: levels, then flows

# %%
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))

# Left: cumulative artisanal-gold area (bars) with the gold price (line, right axis).
ax[0].bar(df["year"], df["gold_artisanal_ha"] / 1000, color="#d9a441", label="artisanal gold area (kha)")
ax0b = ax[0].twinx()
ax0b.plot(df["year"], df["gold"], color="black", linewidth=1.5, label="gold price ($/oz)")
ax[0].set_title("Brazil: artisanal gold mining area and the gold price")
ax[0].set_ylabel("thousand ha (cumulative)"); ax0b.set_ylabel("$/troy oz")

# Right: additions vs. price change. Each point is a year.
ax[1].scatter(df["dln_gold"], df["gold_add_ha"] / 1000, color="#d9a441")
for _, r in df.dropna(subset=["dln_gold"]).iterrows():
    if r["year"] % 5 == 0 or r["year"] >= 2019:
        ax[1].annotate(int(r["year"]), (r["dln_gold"], r["gold_add_ha"] / 1000), fontsize=7, xytext=(3, 3), textcoords="offset points")
ax[1].axvline(0, color="grey", linewidth=0.6)
ax[1].set_xlabel("annual change in log gold price"); ax[1].set_ylabel("new artisanal-gold hectares (thousand)")
ax[1].set_title("Additions vs. price change, one point per year")

for a in ax:
    a.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(OUT_DIR / "fig_q1_brazil.png", dpi=150)

# %% [markdown]
# ## 3. Description in numbers
#
# Three regressions of log additions on price changes: gold alone; gold with one lag;
# gold together with silver and copper (the comparison commodities). Read the R² and
# the sign, not the p-values: there are ~40 points, they are serially correlated, and
# nothing here is identified. The question for the brief is whether gold survives the
# inclusion of silver, and what the lag says about how fast miners respond.

# %%
d = df.dropna(subset=["dln_gold_l1", "dln_silver", "dln_copper"])
models = {
    "gold, same year":         smf.ols("ln_gold_add ~ dln_gold", d).fit(),
    "gold, same year + lag":   smf.ols("ln_gold_add ~ dln_gold + dln_gold_l1", d).fit(),
    "gold + silver + copper":  smf.ols("ln_gold_add ~ dln_gold + dln_gold_l1 + dln_silver + dln_copper", d).fit(),
}
rows = []
for name, m in models.items():
    for term in m.params.index:
        if term != "Intercept":
            rows.append({"model": name, "term": term, "coef": round(m.params[term], 2), "se": round(m.bse[term], 2)})
    rows.append({"model": name, "term": "R²", "coef": round(m.rsquared, 2), "se": ""})
table = pd.DataFrame(rows)
print(table.to_string(index=False))
table.to_csv(OUT_DIR / "table_q1_brazil.csv", index=False)

# %% [markdown]
# ## 4. Check against the source
#
# Additions over 2018–2025 summed must equal the 2025 level minus the 2018 level in the
# platform's own time series (a merge or diff error would break this).

# %%
s = df.set_index("year")
print("Sum of additions 2019–2025:", round(s.loc[2019:2025, "gold_add_ha"].sum()),
      "| level 2025 − level 2018:", round(s.loc[2025, "gold_artisanal_ha"] - s.loc[2018, "gold_artisanal_ha"]))
df.to_csv(OUT_DIR / "panel_brazil_year.csv", index=False)
