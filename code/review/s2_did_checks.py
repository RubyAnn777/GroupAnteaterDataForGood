"""Review session S2 (docs/methods/02_did_2x2.md): read-only checks of the 2x2 DiD, Tambopata vs Amarakaeri.

Run from the repo root:  uv run python code/review/s2_did_checks.py   (writes nothing)
T1 reproduce, T2 pre-window choices, T3 fake start years, T4 scale (logs, % of stock), T5 component split (raster),
T6 spillover bounds, T7 MdD-rows-only units, T8 persistence with and without 2023.
"""
import numpy as np, pandas as pd
bz = pd.read_csv("data/peru_bufferzone_year.csv")
key = bz.buffer_zone + "|" + bz.pa_category
lv = bz.assign(u=key).groupby(["u", "year"]).mining_ha.sum().unstack("u")
T, A = "Tambopata|Reserva Nacional", "Amarakaeri|Reserva Comunal"
ad = lv.diff()
m = lambda s, a, b: s.loc[a:b].mean()
def did(y, pre, post, t=T, c=A):
    dt, dc = m(y[t], *post) - m(y[t], *pre), m(y[c], *post) - m(y[c], *pre)
    return dt, dc, dt - dc

print("T1 reproduce: Tambopata, Amarakaeri means 2016-18 / 2019-21:",
      [round(m(ad[u], *p)) for u in (T, A) for p in ((2016, 2018), (2019, 2021))], "DiD", round(did(ad, (2016, 2018), (2019, 2021))[2], 1))
print("annual additions 2010-2025:\n", ad.loc[2010:2025, [T, A]].round(0).T.to_string())

print("\nT2 pre-window choices (post 2019-21):")
for pre in [(2016, 2018), (2014, 2018), (2016, 2017), (2015, 2017), (2017, 2018), (2011, 2018), (2014, 2016)]:
    dt, dc, d = did(ad, pre, (2019, 2021)); print(f"  pre {pre}: dT {dt:7.0f}  dC {dc:6.0f}  DiD {d:7.0f}")

print("\nT3 fake start years s (pre s-3..s-1, post s..s+2), clean = post window ends by 2018:")
fake = {s: did(ad, (s - 3, s - 1), (s, s + 2))[2] for s in range(2003, 2019)}
real = fake.pop(2019, None) or did(ad, (2016, 2018), (2019, 2021))[2]
clean = {s: v for s, v in fake.items() if s + 2 <= 2018}
for s, v in fake.items(): print(f"  {s}: {v:7.0f}{'' if s in clean else '  (overlaps 2019)'}")
r = 1 + sum(v <= real for v in clean.values()); n = len(clean) + 1
print(f"  real {real:.0f}: rank {r} of {n} clean (p = {r/n:.2f}); two-sided rank {1 + sum(abs(v) >= abs(real) for v in clean.values())}")
pre_sd = np.std(list(clean.values()), ddof=1); print(f"  sd of clean fakes {pre_sd:.0f}; real / sd = {real/pre_sd:.1f}")

print("\nT4 scale")
lg = np.log1p(ad.clip(lower=0))
print("  log(1+add) DiD (negatives clipped to 0):", round(did(lg, (2016, 2018), (2019, 2021))[2], 2))
stock15 = lv.loc[2015]
pct = ad.div(lv.shift(1)) * 100
print("  additions as % of last year's stock, means 2016-18 / 2019-21:", {u.split('|')[0]: [round(m(pct[u], 2016, 2018), 1), round(m(pct[u], 2019, 2021), 1)] for u in (T, A)},
      "DiD pts", round(did(pct, (2016, 2018), (2019, 2021))[2], 1))
rel = ad / ad.loc[2016:2018].mean()
print("  additions relative to own 2016-18 mean: DiD", round(did(rel, (2016, 2018), (2019, 2021))[2], 2),
      "| Tambopata", round(m(rel[T], 2019, 2021), 2), "Amarakaeri", round(m(rel[A], 2019, 2021), 2))

print("\nT5 component split (raster zones; Tambopata = La Pampa sector + rest of Tambopata BZ, Amarakaeri BZ zone)")
z = pd.read_csv("data_intermediate/zone_year_v2.csv")
g = lambda units, col: z[z.unit.isin(units)].groupby("year")[col].sum()
TU, AU = ["La Pampa sector", "Rest of Tambopata buffer zone"], ["Amarakaeri buffer zone"]
comp = {}
for col in ["new_land_ha", "remined_ha", "stopped_ha"]:
    y = pd.DataFrame({T: g(TU, col), A: g(AU, col)})
    comp[col] = did(y, (2016, 2018), (2019, 2021))
y = pd.DataFrame({T: g(TU, "mining_ha").diff(), A: g(AU, "mining_ha").diff()})
comp["net"] = did(y, (2016, 2018), (2019, 2021))
for k, (dt, dc, d) in comp.items(): print(f"  {k:12s} dT {dt:7.0f} dC {dc:6.0f} DiD {d:7.0f}")
print("  check new + remined - stopped =", round(comp["new_land_ha"][2] + comp["remined_ha"][2] - comp["stopped_ha"][2]), "vs net", round(comp["net"][2]))
print("  NB raster Amarakaeri zone mining 2018 (ha):", round(g(AU, "mining_ha").loc[2018]), "vs workbook", round(lv.loc[2018, A]))

print("\nT6 spillover bounds")
dt, dc, d = did(ad, (2016, 2018), (2019, 2021))
print(f"  if Amarakaeri's whole rise (+{dc:.0f}) is spillover from Tambopata: true effect on Tambopata = dT - counterfactual change; "
      f"with no-spillover counterfactual change 0 -> {dt:.0f}; DiD {d:.0f} is the bound away from zero")
others = [u for u in ad.columns if u not in (T, A) and ad.loc[2014:2018, u].abs().sum() > 0]
dco = m(ad[others].sum(axis=1), 2019, 2021) - m(ad[others].sum(axis=1), 2016, 2018)
print(f"  change in the other {len(others)} zones combined: {dco:.0f} ha/yr")

print("\nT7 MdD rows only (agent.md §10 numbers)")
md = bz[bz.department == "Madre de Dios"].assign(u=key).groupby(["u", "year"]).mining_ha.sum().unstack("u").diff()
print("  DiD MdD rows only:", round(did(md, (2016, 2018), (2019, 2021))[2]), "| Amarakaeri non-MdD rows:",
      bz[(bz.buffer_zone == "Amarakaeri") & (bz.year == 2025)][["department", "mining_ha"]].values.tolist())

print("\nT8 persistence (2016-18 vs later years)")
for post, lab in [((2022, 2025), "2022-25"), (None, "2022, 2024, 2025 (no 2023)"), ((2022, 2022), "2022"), ((2024, 2025), "2024-25")]:
    if post is None:
        yrs = [2022, 2024, 2025]; dt = ad.loc[yrs, T].mean() - m(ad[T], 2016, 2018); dc = ad.loc[yrs, A].mean() - m(ad[A], 2016, 2018); d = dt - dc
    else:
        dt, dc, d = did(ad, (2016, 2018), post)
    print(f"  {lab:28s} dT {dt:7.0f} dC {dc:6.0f} DiD {d:7.0f}")
