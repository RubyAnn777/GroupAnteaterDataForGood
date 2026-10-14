"""Review session S1 (docs/methods/01_data_outcomes.md): read-only checks of the outcome measures and zones.

Run from the repo root:  uv run python code/review/s1_data_checks.py
Reads data/, data_intermediate/ and data_raw/bcrp/ only; writes nothing. Not part of main.py.
T0 accounting identity, T1 gross vs net flows, T2 the 2023 spike across products, T3 MINEM vs BCRP every year,
T4 what lies outside the buffer zones, T5 Bahuaja-Sonene rows, T6 statistics workbook vs raster zones.
"""
import json, pandas as pd, numpy as np
pd.set_option("display.width", 200)
P = {"2016-18": (2016, 2018), "2019-21": (2019, 2021), "2022-25": (2022, 2025)}
z = pd.read_csv("data_intermediate/zone_year_v2.csv").sort_values(["unit", "year"])
z["net"] = z.groupby("unit")["mining_ha"].diff()
z["ident_err"] = z["net"] - (z.new_land_ha + z.remined_ha - z.stopped_ha)
print("T0 identity max |net-(new+rem-stop)|, 1986+:", z[z.year > 1986].ident_err.abs().max().round(6))

print("\nT1 gross vs net, mean ha/yr")
rows = []
for u, g in z.groupby("unit"):
    g = g.set_index("year")
    for p, (a, b) in P.items():
        s = g.loc[a:b]
        rows.append(dict(unit=u, period=p, net=s.net.mean(), new=s.new_land_ha.mean(), remined=s.remined_ha.mean(), stopped=s.stopped_ha.mean()))
t1 = pd.DataFrame(rows)
keep = ["La Pampa sector", "Rest of Tambopata buffer zone", "Amarakaeri buffer zone", "Corridor across the road", "Rest of mining corridor", "Tambopata reserve"]
print(t1[t1.unit.isin(keep)].round(0).to_string(index=False))

print("\nT2 the 2023 spike: 2023 / mean(2022, 2024)")
def spike(s): return s.loc[2023] / ((s.loc[2022] + s.loc[2024]) / 2)
tot = z.groupby("year")[["new_land_ha", "remined_ha", "stopped_ha", "net"]].sum()
print("MapBiomas MdD box, all zones:", {c: round(spike(tot[c]), 2) for c in tot}, "| values 2021-25:\n", tot.loc[2021:2025].round(0))
gl = pd.read_csv("data_intermediate/glad_zone_quarter_v2.csv")
gly = gl[gl.mining].groupby("year").ha.sum(); glall = gl.groupby("year").ha.sum()
print("GLAD alerts on (ever-)mined pixels, ha:", gly.round(0).to_dict(), "spike", round(spike(gly), 2))
print("GLAD all alerts, ha:", glall.round(0).to_dict(), "spike", round(spike(glall), 2))
amw = pd.read_csv("data_intermediate/amw_v2_zone_year.csv").groupby("year").new_ha.sum()
print("AMW new area all v2 zones, ha:", amw.round(0).to_dict(), "spike", round(spike(amw), 2))
for u in keep[:5]:
    g = z[z.unit == u].set_index("year")
    print(f"  {u:32s} new spike {spike(g.new_land_ha):.2f} remined spike {spike(g.remined_ha):.2f}")

print("\nT3 MINEM rebuild vs BCRP (kg; BCRP series is in grams)")
j = json.load(open("data_raw/bcrp/bcrp_annual_gold_series_2001_2025.json"))
names = [s["name"] for s in j["config"]["series"]]
mdd = [i for i, n in enumerate(names) if "Madre de Dios" in n or "MADRE" in n.upper()]
print("series:", [names[i][:110] for i in mdd])
per = j["periods"]
bc = pd.Series({int(p["name"]): float(p["values"][mdd[0]]) / 1000 for p in per if p["values"][mdd[0]] not in ("n.d.", "")})
m = pd.read_csv("data_intermediate/minem_mdd_gold.csv").set_index("year")
cmp_ = pd.DataFrame({"minem_total": m.total_kg, "declared": m.declared_kg, "bcrp": bc}).dropna()
cmp_["diff_pct"] = (cmp_.minem_total / cmp_.bcrp - 1) * 100
print(cmp_.loc[2005:].round(1).to_string())

print("\nT4 what 'rest of Madre de Dios' contains (raster zones, first-time ha/yr)")
outside_bz = ["Tambopata reserve", "Other reserves and parks", "Kotsimba (native community)", "Other native communities",
              "Corridor across the road", "Rest of mining corridor", "Rest of Madre de Dios"]
r = t1[t1.unit.isin(outside_bz)].pivot(index="unit", columns="period", values="new")
r.loc["TOTAL"] = r.sum(); print((r).round(0)); print((r / r.loc["TOTAL"] * 100).round(1))

print("\nT5 Bahuaja-Sonene BZ rows by department, total_ha 2025 and mining 2025")
bz = pd.read_csv("data/peru_bufferzone_year.csv")
print(bz[(bz.buffer_zone.str.contains("Bahuaja")) & (bz.year == 2025)][["buffer_zone", "department", "total_ha", "mining_ha"]])
print("\nT6 pack (statistics workbook) vs raster: Tambopata BZ net additions")
tb = bz[(bz.buffer_zone == "Tambopata")].groupby("year").mining_ha.sum().diff()
rz = z[z.unit.isin(["La Pampa sector", "Rest of Tambopata buffer zone"])].groupby("year").net.sum()
print(pd.DataFrame({"pack": tb, "raster_LP+restTBZ": rz}).loc[2014:2025].round(0).T.to_string())
