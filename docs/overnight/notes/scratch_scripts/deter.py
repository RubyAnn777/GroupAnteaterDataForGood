import sys, json, geopandas as gpd, pandas as pd
R="/Users/sebastianschmid/Projects/uni/DataForGood/GroupAnteaterDataForGood/"
raw=R+"data_raw/inpe_deter/"; out=R+"docs/overnight/notes/"
d=gpd.read_file(raw+"deter_amz_mineracao.geojson")
print(d.shape, d.crs, d.columns.tolist())
d["view_date"]=pd.to_datetime(d["view_date"])
d["ym"]=d.view_date.dt.to_period("M").astype(str); d["year"]=d.view_date.dt.year
# check vs dashboard (biome dashboard, class MINERACAO)
db=json.load(open(raw+"dashboard_deter-amazon-month_biome.json"))
db=pd.DataFrame([f["properties"] for f in db["features"]]); m=db[db.cl=="MINERACAO"].copy()
m["year"]=2000+m.y.astype(int); m["month"]=m.m.astype(int)
print("dashboard years", m.groupby("year").ar.sum().round(2).to_dict())
print("dashboard Aug-Jul DETER yrs (calendar sums above). total", m.ar.sum().round(2), "np", m.np.sum())
d["area_km2_geom"]=d.to_crs(5880).area/1e6
print("sum areamunkm",d.areamunkm.sum(), "geom",d.area_km2_geom.sum())
t=gpd.read_file(raw+"funai_tis_selected.geojson")[["terrai_nome","superficie_perimetro_ha","geometry"]]
t=t[t.terrai_nome.isin(["Yanomami","Munduruku","Kayapó","Sai-Cinza","Munduruku-Taquara"])].to_crs(5880)
d5=d.to_crs(5880); d5["geometry"]=d5.geometry.buffer(0); t["geometry"]=t.geometry.buffer(0)
j=gpd.overlay(d5[["gid","view_date","ym","year","geometry"]],t,how="intersection")
j["km2"]=j.area/1e6
j["ti"]=j.terrai_nome
j.loc[j.ti.isin(["Sai-Cinza","Munduruku-Taquara"]),"ti"]="Munduruku (incl. Sai-Cinza, Taquara)"
j.loc[j.ti=="Munduruku","ti"]="Munduruku (incl. Sai-Cinza, Taquara)"
# separate keep exact Munduruku alone too
jm=j.copy()
mon=jm.groupby(["ti","ym"]).km2.sum().unstack(0).fillna(0)
full=pd.period_range("2016-08","2026-09",freq="M").astype(str)
mon=mon.reindex(full,fill_value=0).round(4); mon.index.name="month"
mon.to_csv(out+"deter_mining_ti_monthly_km2.csv")
ann=jm.groupby(["ti","year"]).km2.sum().unstack(0).fillna(0).round(3); ann.index.name="calendar_year"
ann.to_csv(out+"deter_mining_ti_annual_km2.csv")
sep=j[j.terrai_nome.isin(["Munduruku","Sai-Cinza","Munduruku-Taquara"])].groupby(["terrai_nome","year"]).km2.sum().unstack(0).fillna(0).round(3)
print(ann); print(sep)
# state-year totals legal Amazon
d.groupby(["uf","year"]).areamunkm.sum().unstack(0).fillna(0).round(2).to_csv(out+"deter_mining_uf_annual_km2.csv")
# monthly Yanomami sample around Feb 2023
print(mon.loc["2022-09":"2023-12","Yanomami"])
# overlap check: do TIs overlap each other
print(j.groupby("gid").size().max())
