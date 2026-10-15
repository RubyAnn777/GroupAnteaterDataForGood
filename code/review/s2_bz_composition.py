"""Review S2 (docs/methods/02_did_2x2.md), test T6b: where the mined land inside the Amarakaeri and Tambopata buffer-zone
polygons lies in our raster zones. Reads data_raw/sernanp/zonas_amortiguamiento.geojson and
data_intermediate/zones_v2_mdd_full.tif (band 1 = zone, band 2 = first-mined year). Writes nothing.
Run from the repo root: uv run python code/review/s2_bz_composition.py"""
import geopandas as gpd, rasterio, numpy as np, pandas as pd
from rasterio.features import geometry_mask
zb = gpd.read_file("data_raw/sernanp/zonas_amortiguamiento.geojson")
print(zb.columns.tolist()[:10])
namecol = [c for c in zb.columns if zb[c].astype(str).str.contains("Amarakaeri", case=False).any()][0]
r = rasterio.open("data_intermediate/zones_v2_mdd_full.tif")
NAMES = {1:"Tambopata reserve",2:"Other reserves/parks",3:"Kotsimba",4:"Other communities",5:"Corridor across road",6:"Rest of corridor",7:"La Pampa sector",8:"Rest of Tambopata BZ",9:"Amarakaeri BZ",10:"Bahuaja BZ",11:"Other BZ",12:"Rest of MdD"}
for nm in ["Amarakaeri", "Tambopata"]:
    poly = zb[zb[namecol].astype(str).str.contains(nm, case=False)].to_crs(r.crs)
    win = rasterio.windows.from_bounds(*poly.total_bounds, transform=r.transform).round_offsets().round_lengths()
    zone = r.read(1, window=win); first = r.read(2, window=win); tr = r.window_transform(win)
    inside = ~geometry_mask(poly.geometry, out_shape=zone.shape, transform=tr)
    lat = tr.f + tr.e * (np.arange(zone.shape[0]) + 0.5)
    px_ha = (abs(tr.a) * 111320 * np.cos(np.radians(lat)))[:, None] * (abs(tr.e) * 110574) / 1e4
    m18 = inside & (first > 0) & (first <= 2018)
    df = pd.DataFrame({"zone": zone[m18], "ha": np.broadcast_to(px_ha, zone.shape)[m18]})
    out = df.groupby("zone").ha.sum().rename(index=NAMES)
    print(f"\n{nm} BZ polygon: ever-mined by 2018 = {out.sum():,.0f} ha, by raster zone:\n", (out.round(0)).to_string())
    m1921 = inside & (first >= 2019) & (first <= 2021)
    df2 = pd.DataFrame({"zone": zone[m1921], "ha": np.broadcast_to(px_ha, zone.shape)[m1921]})
    print(f" first-mined 2019-21 by zone:\n", df2.groupby("zone").ha.sum().rename(index=NAMES).round(0).to_string())
