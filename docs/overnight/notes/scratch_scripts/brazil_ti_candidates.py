import sys, pandas as pd, geopandas as gpd
xl, gj, out = sys.argv[1:4]
d = pd.read_excel(xl, sheet_name="COVERAGE_INDIGENOUS_TERRITORIES")
m = d[d.class_id == 30]
yrs = [c for c in d.columns if str(c).isdigit()]
g = m.groupby(["geocode", "indigenous_territories"])[yrs].sum().reset_index()
g.columns = [str(c) for c in g.columns]
states = d.groupby("geocode")["state_acronym"].apply(lambda s: "+".join(sorted(set(map(str, s))))).rename("states")
g = g.merge(states, left_on="geocode", right_index=True)
t = gpd.read_file(gj).to_crs(5880)
t["terrai_codigo"] = pd.to_numeric(t["terrai_codigo"], errors="coerce")
yan = t[t.terrai_codigo == 50901]
print("yanomami polys:", len(yan), yan.terrai_nome.tolist())
yg = yan.geometry.union_all()
dist = t.dissolve("terrai_codigo").geometry.distance(yg) / 1000
g["dist_to_yanomami_km"] = g.geocode.map(dist).round(0)
g["add_2019_22_mean"] = ((g["2022"] - g["2018"]) / 4).round(1)
g["add_2023_24_mean"] = ((g["2024"] - g["2022"]) / 2).round(1)
cols = ["geocode", "indigenous_territories", "states", "2018", "2022", "2024", "add_2019_22_mean", "add_2023_24_mean", "dist_to_yanomami_km"]
g = g[cols].sort_values("2022", ascending=False)
for c in ["2018", "2022", "2024"]: g[c] = g[c].round(1)
g.to_csv(out, index=False); print(g.to_string(index=False))
