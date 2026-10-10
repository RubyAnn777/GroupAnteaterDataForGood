"""Feasibility prototype: AMW onset patches x SERNANP zones / distance rings (Peru) and FUNAI Yanomami rings (Brazil).
Reads data_raw/ only; writes nothing to data/. Prints tables; saves CSVs next to this script.
Run (repo root): uv run --with geopandas --with shapely --with pyogrio python -I docs/overnight/notes/spatial_prototype.py

CAVEATS
* AMW = 480 m patches (half-overlapping), 'onset_year' = year mining first confirmed (Recipe A, needs corroboration in
  the following year, so 2025 onsets are only 'provisional'). Not MapBiomas ha: do not mix/compare numbers.
* Annual area = area(union of patches with onset==Y) minus area already covered by earlier-year patches (removes overlap).
* La Pampa point is an ASSUMPTION: approx. centre of La Pampa along the Interoceanica Highway km 98-115,
  about -12.95, -70.42 (read off MAAP #130 maps; not an official coordinate). Verify against AMW patches before use.
"""
import time, pathlib
import geopandas as gpd, pandas as pd
from shapely.geometry import Point
from shapely.ops import unary_union
t0 = time.time()
HERE = pathlib.Path(__file__).resolve().parent
R = HERE.parents[2] / "data_raw"
UTM19S, BRPOLY = 32719, 5880          # Peru/MdD metric CRS; Brazil polyconic (SIRGAS 2000)

amw = gpd.read_file(R / "amw/amazon_basin_detections.geojson")   # CRS84
print("AMW patches", len(amw), amw.crs, "onset years:", sorted(amw.onset_year.unique()),
      "\nstatus:", amw.status.value_counts().to_dict(), f"load {time.time()-t0:.0f}s")

def yearly_increment(patches):
    """ha per onset year, overlap-free."""
    seen, out = None, {}
    for y in sorted(patches.onset_year.unique()):
        u = unary_union(patches.loc[patches.onset_year == y].geometry.values)
        new = u if seen is None else u.difference(seen)
        out[int(y)] = new.area / 1e4
        seen = u if seen is None else seen.union(u)
    return out

# ---------------- Peru ----------------
box = (-72.6, -14.6, -68.6, -10.5)   # Madre de Dios + surroundings (no department polygon downloaded)
mdd = amw.cx[box[0]:box[2], box[1]:box[3]].to_crs(UTM19S)
anp = gpd.read_file(R / "sernanp/anp_definitivas.geojson").to_crs(UTM19S)
za = gpd.read_file(R / "sernanp/zonas_amortiguamiento.geojson").to_crs(UTM19S)
cor = gpd.read_file(R / "ingemmet/corredor_minero_madre_de_dios_DL1100.geojson").to_crs(UTM19S)
tam_nr = unary_union(anp[anp.anp_codi == "RN09"].geometry)
tam_bz = unary_union(za[za.anp_codi == "RN09"].geometry).difference(tam_nr)
corr = unary_union(cor.geometry)
other_anp = unary_union(anp[anp.anp_codi != "RN09"].geometry)
other_bz = unary_union(za[za.anp_codi != "RN09"].geometry)
# priority order (zones overlap; first match wins)
zones, taken = {}, None
for name, geom in [("Tambopata NR (core)", tam_nr), ("Tambopata buffer zone", tam_bz), ("Mining corridor (DL 1100)", corr),
                   ("Other ANP", other_anp), ("Other buffer zones", other_bz)]:
    g = geom if taken is None else geom.difference(taken)
    zones[name] = g; taken = g if taken is None else taken.union(g)
print("zone areas km2:", {k: round(v.area/1e6) for k, v in zones.items()}, f"{time.time()-t0:.0f}s")
cent = mdd.copy(); cent["geometry"] = mdd.centroid       # assign each patch by centroid
rows = []
def zone_of(pt):
    for k, g in zones.items():
        if g.contains(pt): return k
    return "Outside all (rest of box)"
cent["zone"] = cent.geometry.apply(zone_of)
mdd["zone"] = cent["zone"].values
for z, d in mdd.groupby("zone"):
    for y, ha in yearly_increment(d).items(): rows.append(dict(region="Peru zone", unit=z, year=y, new_ha=round(ha)))
# rings around La Pampa
lp = gpd.GeoSeries([Point(-70.42, -12.95)], crs=4326).to_crs(UTM19S).iloc[0]
def ring_of(c, rings=((0,10),(10,25),(25,50))):
    d = c.distance(lp)/1e3
    for a, b in rings:
        if a <= d < b: return f"{a}-{b} km"
mdd["ring"] = cent.geometry.apply(ring_of)
for z, d in mdd.dropna(subset=["ring"]).groupby("ring"):
    for y, ha in yearly_increment(d).items(): rows.append(dict(region="Peru La Pampa ring", unit=z, year=y, new_ha=round(ha)))
print(f"Peru done {time.time()-t0:.0f}s")

# ---------------- Brazil ----------------
ti = gpd.read_file(R / "funai/tis_poligonais.geojson")        # SIRGAS 2000 (EPSG:4674)
print("FUNAI", len(ti), ti.crs, "Yanomami rows:", ti[ti.terrai_nome.str.contains("Yanomami", case=False, na=False)][["terrai_nome","uf_sigla","superficie_perimetro_ha"]].to_dict("records"))
yan = ti[ti.terrai_nome.str.contains("^Yanomami$", case=False, regex=True, na=False)].to_crs(BRPOLY)
yg = unary_union(yan.geometry)
bb = gpd.GeoSeries([yg.buffer(60e3)], crs=BRPOLY).to_crs(4326).total_bounds
br = amw.cx[bb[0]:bb[2], bb[1]:bb[3]].to_crs(BRPOLY)
bc = br.centroid
def bring(c):
    if yg.contains(c): return "inside Yanomami TI"
    d = c.distance(yg)/1e3
    for a, b in ((0,10),(10,25),(25,50)):
        if a <= d < b: return f"outside {a}-{b} km"
br["ring"] = bc.apply(bring)
for z, d in br.dropna(subset=["ring"]).groupby("ring"):
    for y, ha in yearly_increment(d).items(): rows.append(dict(region="Yanomami ring", unit=z, year=y, new_ha=round(ha)))
out = pd.DataFrame(rows)
out.to_csv(HERE / "spatial_prototype_output.csv", index=False)
print(out.pivot_table(index=["region","unit"], columns="year", values="new_ha").to_string())
print(f"total runtime {time.time()-t0:.0f}s")
