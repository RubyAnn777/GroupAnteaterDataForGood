# %% [markdown]
# # 04 · Spatial panels from the MapBiomas statistics workbooks
#
# **What this script does.** Turns the three bulk statistics workbooks into three tidy
# panels, one row per territory and year, with mining area and (for context) forest area:
#
# | output file | unit | years | source workbook |
# |---|---|---|---|
# | `brazil_municipality_year.csv` | municipality (× biome) | 1985–2024 | Brazil Collection 10.1, Dataverse |
# | `peru_department_year.csv` | department (× biome) | 1985–2025 | Peru Collection 4, peru.mapbiomas.org |
# | `peru_bufferzone_year.csv` | protected-area buffer zone (× department) | 1985–2025 | Peru Collection 4, peru.mapbiomas.org |
#
# **Why these three.** Q2 (enforcement and displacement) needs many small units observed
# before and after a policy date: Brazilian municipalities around the 2019–2022
# enforcement collapse and the 2023 Yanomami operation; Peruvian buffer zones around
# Operation Mercurio (Feb 2019), since La Pampa lies in Tambopata's buffer zone. Q1 and
# Q3 use the department panel.
#
# **What "mining" is here.** The land-cover class *4.3 Mining* (Brazil) / *4.2 Minería*
# (Peru): any mining scar, industrial or artisanal, any substance. These workbooks do not
# carry the substance split; that only exists in the platform download (script 02).
#
# **Layout of the workbooks.** One sheet (`COVERAGE_10.1` / `COVERAGE_4`) in "wide" form:
# one row per territory × class, one column per year. Brazil names its territory columns
# plainly (`state`, `municipality`); Peru uses a generic scheme (`territory_level_2_1`,
# `territory_level_2_2`, …) where `category_1`/`category_2` say what each level is.
#
# **Stata translation.** `read_excel(sheet_name=)` = `import excel, sheet()`; `melt` =
# `reshape long`; `pivot` = `reshape wide`; `groupby().sum()` = `collapse (sum)`.

# %%
import pandas as pd
import re
from pathlib import Path

DATA = Path("data"); OUT = Path("output"); OUT.mkdir(exist_ok=True)
log = pd.read_csv(DATA / "DOWNLOAD_LOG.csv").set_index("file")

BR_FILE = "MAPBIOMAS_BRAZIL-COVERAGE_STATISTICS-COL.10.1-MUNICIPALITIES_STATES_BIOMES.xlsx"
PE_POL  = "MAPBIOMAS-PERU-LULC-COL4-LIMITES-POLITICOS.xlsx"
PE_BUF  = "MAPBIOMAS-PERU-LULC-COL4-ZONA-AMORTIGUAMIENTO.xlsx"
for f in [BR_FILE, PE_POL, PE_BUF]:
    assert f in log.index, f"{f} is not in DOWNLOAD_LOG.csv — log it before using it"


def to_long(df, id_cols, year_pattern):
    """Wide (one column per year) -> long (one row per territory-class-year).
    year_pattern picks the year columns: r'^\\d{4}$' for Brazil (1985, 1986, …),
    r'^y\\d{4}$' for Peru (y1985, y1986, …)."""
    year_cols = [c for c in df.columns if re.fullmatch(year_pattern, str(c))]
    long = df.melt(id_vars=id_cols, value_vars=year_cols, var_name="year", value_name="area_ha")
    long["year"] = long["year"].astype(str).str.extract(r"(\d{4})").astype(int)
    return long


def panel(long, unit_cols, mining_label, forest_label):
    """Collapse the long class table to one row per unit-year with mining and forest area."""
    long = long.assign(
        mining_ha = long["area_ha"].where(long["class_level_4"].eq(mining_label), 0.0),   # area if mining, else 0
        forest_ha = long["area_ha"].where(long["class_level_1"].eq(forest_label), 0.0),
        total_ha  = long["area_ha"],
    )
    return long.groupby(unit_cols + ["year"], as_index=False)[["mining_ha", "forest_ha", "total_ha"]].sum()

# %% [markdown]
# ## 1. Brazil: municipality × year
#
# 78,818 rows × 40 years; reading the sheet takes ~30 s. We keep the identifiers, the
# class labels and the year columns, then collapse. `class_level_1 == '1. Forest'`
# gives forest area for a forest-loss context variable.

# %%
br = pd.read_excel(DATA / BR_FILE, sheet_name="COVERAGE_10.1")
print("Brazil rows:", len(br), "| classes:", br["class_level_4"].nunique(), "| municipalities:", br["municipality"].nunique())
assert "4.3. Mining" in set(br["class_level_4"]), "Mining class label changed?"

br_long = to_long(br, ["biome", "state", "state_acronym", "municipality", "class_level_1", "class_level_4"], r"^\d{4}$")
br_panel = panel(br_long, ["state_acronym", "state", "municipality", "biome"], "4.3. Mining", "1. Forest")
br_panel.to_csv(OUT / "brazil_municipality_year.csv", index=False)
print("brazil_municipality_year.csv:", br_panel.shape)

# %% [markdown]
# ## 2. Peru: department × year, and buffer zone × year
#
# In the Peru workbooks the first territory block (`territory_level_*_1`) is the unit the
# file is about (biome in the political file; buffer zone in the buffer file), the second
# block is the department, the third the country. `category_*` columns confirm this.

# %%
pe = pd.read_excel(DATA / PE_POL, sheet_name="COVERAGE_4")
assert set(pe["category_1"]) == {"BIOMES"} and set(pe["category_2"]) == {"POLITICAL_LEVEL_2"}, pe[["category_1", "category_2"]].drop_duplicates()
pe = pe.rename(columns={"territory_level_2_1": "biome", "territory_level_2_2": "department"})
pe_long = to_long(pe, ["biome", "department", "class_level_1", "class_level_4"], r"^y\d{4}$")
pe_panel = panel(pe_long, ["department", "biome"], "4.2. Minería", "1. Formación boscosa")
pe_panel.to_csv(OUT / "peru_department_year.csv", index=False)
print("peru_department_year.csv:", pe_panel.shape, "| departments:", pe_panel["department"].nunique())

zb = pd.read_excel(DATA / PE_BUF, sheet_name="COVERAGE_4")
assert set(zb["category_1"]) == {"NPA_BUFFER_ZONE"}, zb["category_1"].unique()
zb = zb.rename(columns={"territory_level_2_1": "buffer_zone", "territory_level_3_1": "pa_category", "territory_level_2_2": "department"})
zb_long = to_long(zb, ["buffer_zone", "pa_category", "department", "class_level_1", "class_level_4"], r"^y\d{4}$")
zb_panel = panel(zb_long, ["buffer_zone", "pa_category", "department"], "4.2. Minería", "1. Formación boscosa")
zb_panel.to_csv(OUT / "peru_bufferzone_year.csv", index=False)
print("peru_bufferzone_year.csv:", zb_panel.shape, "| buffer zones:", zb_panel["buffer_zone"].nunique())

# %% [markdown]
# ## 3. Checks against the source
#
# Each number below is also written in DOWNLOAD_LOG.csv (`check_number`) and can be read
# off the publisher's own platform. The third is a *cross-instrument* comparison, not a
# check: MAAP #233 reports 135,939 ha of mining deforestation in Madre de Dios "as of
# mid-2025", counting every hectare ever cleared for mining since 1984; MapBiomas reports
# the area *currently classified as mining*. They should differ, and the brief must say why.

# %%
br_nat_2024 = br_panel.query("year == 2024")["mining_ha"].sum()
mdd_2025    = pe_panel.query("department == 'Madre de Dios' and year == 2025")["mining_ha"].sum()
tam_2025    = zb_panel.query("buffer_zone == 'Tambopata' and year == 2025")["mining_ha"].sum()
print(f"Brazil, class 4.3 Mining, all municipalities, 2024: {br_nat_2024:,.0f} ha   (log: 609,637)")
print(f"Peru, Madre de Dios, class 4.2 Minería, 2025:        {mdd_2025:,.0f} ha   (log: 112,622; MAAP #233 cumulative: 135,939)")
print(f"Peru, Tambopata buffer zone, 2025:                   {tam_2025:,.0f} ha   (log: 20,730)")

# Internal consistency: municipalities must add up to the state total in the same file.
by_state = br_panel.query("year == 2024").groupby("state_acronym")["mining_ha"].sum()
print("Pará 2024 from municipalities:", f"{by_state['PA']:,.0f} ha")

# %% [markdown]
# ## 4. First look at Q2: Operation Mercurio (February 2019)
#
# Annual additions to mining area in the Tambopata buffer zone (where La Pampa is) versus
# the Amarakaeri buffer zone (the other large mining front in Madre de Dios, not targeted
# in 2019). This is the before/after picture that a difference-in-differences would
# formalise. Read it with the caveats from the design note: COVID follows a year later,
# displacement from La Pampa may land in the comparison zone, and a scar rarely shrinks
# (2021 shows a small negative: reclassified old scars), so "reduction" appears mostly as
# smaller additions.

# %%
import matplotlib.pyplot as plt
# A buffer zone can span two departments (one row each), so sum over departments first.
w = (zb_panel.groupby(["year", "buffer_zone"])["mining_ha"].sum()
             .unstack("buffer_zone")[["Tambopata", "Amarakaeri"]])
adds = w.diff().loc[2011:]
fig, ax = plt.subplots(figsize=(7, 4))
adds.plot(kind="bar", ax=ax, color=["#d9a441", "#7a9cc6"], width=0.8)
ax.axvline(list(adds.index).index(2019) - 0.5, color="black", linewidth=0.8, linestyle="--")
ax.text(list(adds.index).index(2019) - 0.4, ax.get_ylim()[1] * 0.92, "Op. Mercurio\n(Feb 2019)", fontsize=8)
ax.set_ylabel("new mining hectares in the year"); ax.set_xlabel("")
ax.set_title("Madre de Dios: annual additions to mining area in two buffer zones")
ax.spines[["top", "right"]].set_visible(False); ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(OUT / "fig_q2_mercurio_bufferzones.png", dpi=150)
print(adds.loc[2016:2025].round(0))
