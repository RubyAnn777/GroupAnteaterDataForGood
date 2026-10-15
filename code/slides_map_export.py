"""Map layers for the presentation animation (STORYLINE.md slides 3-4): transparent PNGs + one JSON for Remotion.

Standalone, NOT wired into main.py: it reads git-ignored inputs (data_intermediate/zones_v2_mdd_full.tif, the
MapBiomas Peru Col 4 raster for 2018, SERNANP / INGEMMET / RAISG vectors). Run:  uv run python code/slides_map_export.py

Every layer is drawn on ONE extent (EXTENT, lon/lat, plate carrée stretched so a degree of longitude has its true
ground width at the map centre) into a 3840 x 2160 transparent PNG, so the layers stack exactly in the video.
Outputs (presentation/animation/public/):
  layer_base.png        land (slate) - the background
  layer_rivers.png      MapBiomas class 33 (river, lake) in 2018
  layer_zones.png       reserves/parks (dark green), buffer zones (green), native communities (raspberry outline)
  layer_highway.png     Interoceanic Highway (RAISG PE-30C)
  layer_corridor.png    D.L. 1100 small-scale mining corridor (blue tint + outline)
  layer_lapampa.png     La Pampa sector outline (our boundary, orange)
  layer_across.png      corridor across the road (zone 5) outline (blue)
  mining_pre2008.png    pixels first mapped as mining before 2008 (grey)
  mining_hot_YYYY.png   pixels first mapped as mining in year YYYY (bright), 2008-2025
  mining_old_YYYY.png   the same pixels in grey (after their year)
  map_data.json         extent, label anchors (pixel coords at 1920 x 1080), events, first-time mining ha per year
                        for La Pampa sector, corridor across the road and all of Madre de Dios (zone_year_v2.csv)
Description only: first-time mining = pixels mapped as mining for the first time since 1985; the class cannot tell
legal from illegal mining.
"""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import ROOT, C, PERU_EVENTS

RAW, INTER = ROOT / "data_raw", ROOT / "data_intermediate"
OUTDIR = ROOT / "presentation" / "animation" / "public"
W_PX, H_PX = 3840, 2160                       # rendered layers; the video shows them at 1920 x 1080
LAT0, LAT1 = -13.36, -12.36                   # 1.0 degree of latitude
LAT_C = (LAT0 + LAT1) / 2
LON_C = -69.98
LON_SPAN = (LAT1 - LAT0) * (W_PX / H_PX) / np.cos(np.radians(LAT_C))   # true ground aspect at the centre
EXTENT = (LON_C - LON_SPAN / 2, LON_C + LON_SPAN / 2, LAT0, LAT1)        # lon0, lon1, lat0, lat1
YEARS = list(range(2008, 2026))
LP_LON = (-70.15, -69.80)

LAND, WATER = "#2b434a", "#6f9fb6"
HOT, OLD = "#ffd23f", "#b9c2bf"


def _canvas():
    fig = plt.figure(figsize=(W_PX / 200, H_PX / 200), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(EXTENT[0], EXTENT[1]); ax.set_ylim(EXTENT[2], EXTENT[3])
    ax.set_aspect("auto"); ax.axis("off")
    fig.patch.set_alpha(0); ax.patch.set_alpha(0)
    return fig, ax


def _save(fig, name):
    fig.savefig(OUTDIR / name, dpi=200, transparent=True)
    plt.close(fig)
    print("saved", name)


def _read_window(path, band=1):
    import rasterio
    from rasterio.windows import from_bounds
    with rasterio.open(path) as r:
        w = from_bounds(EXTENT[0], EXTENT[2], EXTENT[1], EXTENT[3], r.transform).round_offsets().round_lengths()
        a = r.read(band, window=w, boundless=True, fill_value=0)
        t = r.window_transform(w)
    ext = (t.c, t.c + t.a * a.shape[1], t.f + t.e * a.shape[0], t.f)
    return a, ext


def _mask_png(mask, ext, color, name, alpha=1.0):
    """Max-pool the 30 m mask to the output grid (so small pits stay visible), then draw it."""
    fig, ax = _canvas()
    rgba = np.zeros(mask.shape + (4,), np.float32)
    rgba[mask] = matplotlib.colors.to_rgba(color, alpha)
    ax.imshow(rgba, extent=ext, origin="upper", interpolation="antialiased", resample=True, aspect="auto")
    _save(fig, name)


def _hot_png(mask, ext, name):
    """Pixels of the current year: dilated core + soft glow, so a few hectares stay visible when projected."""
    from scipy.ndimage import binary_dilation, gaussian_filter
    core = binary_dilation(mask, iterations=1)
    glow = np.clip(gaussian_filter(binary_dilation(mask, iterations=2).astype(np.float32), 2.5) * 1.4, 0, 1)
    rgb = np.array(matplotlib.colors.to_rgb(HOT), np.float32)
    rgba = np.zeros(mask.shape + (4,), np.float32)
    rgba[..., :3] = rgb
    rgba[..., 3] = np.maximum(glow * 0.45, core.astype(np.float32))
    fig, ax = _canvas()
    ax.imshow(rgba, extent=ext, origin="upper", interpolation="antialiased", aspect="auto")
    _save(fig, name)


def _pool(mask, k=2):
    h, w = (mask.shape[0] // k) * k, (mask.shape[1] // k) * k
    m = mask[:h, :w].reshape(h // k, k, w // k, k).max(axis=(1, 3))
    return m


def _px(lon, lat):
    """lon/lat -> pixel at 1920 x 1080 (the video frame)."""
    x = (lon - EXTENT[0]) / (EXTENT[1] - EXTENT[0]) * 1920
    y = (EXTENT[3] - lat) / (EXTENT[3] - EXTENT[2]) * 1080
    return [round(float(x), 1), round(float(y), 1)]


def run():
    import geopandas as gpd
    from shapely.geometry import box
    import rasterio.features
    from shapely.geometry import shape
    OUTDIR.mkdir(parents=True, exist_ok=True)
    frame = box(EXTENT[0], EXTENT[2], EXTENT[1], EXTENT[3])

    anp = gpd.read_file(RAW / "sernanp/anp_definitivas.geojson").to_crs(4326)
    za = gpd.read_file(RAW / "sernanp/zonas_amortiguamiento.geojson").to_crs(4326)
    cor = gpd.read_file(RAW / "ingemmet/corredor_minero_madre_de_dios_DL1100.geojson").to_crs(4326)
    roads = gpd.read_file(RAW / "raisg/vias_nacionales_mdd_box.geojson")
    ioh = roads[roads.sigla == "PE-30C"].to_crs(4326)
    ti = gpd.read_file(INTER / "native_communities_mdd.geojson").to_crs(4326)
    clip = lambda g: gpd.clip(g, frame)
    anp, za, cor, ioh, ti = clip(anp), clip(za), clip(cor), clip(ioh), clip(ti)

    # base
    fig, ax = _canvas()
    ax.add_patch(plt.Rectangle((EXTENT[0], EXTENT[2]), LON_SPAN, 1.0, color=LAND, zorder=0))
    _save(fig, "layer_base.png")

    # rivers (MapBiomas class 33, 2018)
    lc, ext = _read_window(RAW / "mapbiomas_peru_raster/peru_coverage-col4_2018.tif")
    _mask_png(_pool(lc == 33), (ext[0], ext[0] + (ext[1] - ext[0]) * (_pool(lc == 33).shape[1] * 2 / lc.shape[1]),
                                ext[3] - (ext[3] - ext[2]) * (_pool(lc == 33).shape[0] * 2 / lc.shape[0]), ext[3]),
              WATER, "layer_rivers.png")

    # zones: buffer zones, reserves/parks, native communities
    fig, ax = _canvas()
    za.plot(ax=ax, color=C["buffer"], alpha=0.30, linewidth=0)
    za.boundary.plot(ax=ax, color=C["buffer_tint"], linewidth=2.2, alpha=0.9)
    anp.plot(ax=ax, color=C["reserve"], alpha=0.75, linewidth=0)
    anp.boundary.plot(ax=ax, color=C["buffer_tint"], linewidth=2.6)
    ti.boundary.plot(ax=ax, color="#e26a9c", linewidth=2.4)
    _save(fig, "layer_zones.png")

    fig, ax = _canvas()
    ioh.plot(ax=ax, color="#111a1d", linewidth=11)
    ioh.plot(ax=ax, color="#f3f1ea", linewidth=6)
    _save(fig, "layer_highway.png")

    fig, ax = _canvas()
    cor.plot(ax=ax, color=C["corridor"], alpha=0.45, linewidth=0)
    cor.boundary.plot(ax=ax, color="#8db7d6", linewidth=3)
    _save(fig, "layer_corridor.png")

    # La Pampa sector and the corridor across the road: polygonised from the zone raster (codes 7 and 5)
    zc, zext = _read_window(INTER / "zones_v2_mdd_full.tif", 1)
    fy, _ = _read_window(INTER / "zones_v2_mdd_full.tif", 2)
    import rasterio
    with rasterio.open(INTER / "zones_v2_mdd_full.tif") as r:
        from rasterio.windows import from_bounds
        wt = r.window_transform(from_bounds(EXTENT[0], EXTENT[2], EXTENT[1], EXTENT[3], r.transform)
                                .round_offsets().round_lengths())
    polys = {}
    for code, name, color in ((7, "layer_lapampa.png", C["lapampa"]), (5, "layer_across.png", "#5fa8dc")):
        m = (zc == code).astype(np.uint8)
        geoms = [shape(g).buffer(0) for g, v in rasterio.features.shapes(m, mask=m.astype(bool), transform=wt) if v == 1]
        g = gpd.GeoSeries(geoms, crs=4326).union_all().buffer(0.004).buffer(-0.004).simplify(0.002)
        polys[code] = g
        fig, ax = _canvas()
        gpd.GeoSeries([g]).plot(ax=ax, color=color, alpha=0.18, linewidth=0)
        gpd.GeoSeries([g]).boundary.plot(ax=ax, color=color, linewidth=7)
        _save(fig, name)

    # mining by first-mined year
    pext = (zext[0], zext[0] + (zext[1] - zext[0]) * (_pool(fy > 0).shape[1] * 2 / fy.shape[1]),
            zext[3] - (zext[3] - zext[2]) * (_pool(fy > 0).shape[0] * 2 / fy.shape[0]), zext[3])
    _mask_png(_pool((fy > 0) & (fy < YEARS[0])), pext, OLD, "mining_pre2008.png", 0.6)
    for y in YEARS:
        m = _pool(fy == y)
        _hot_png(m, pext, f"mining_hot_{y}.png")
        _mask_png(m, pext, OLD, f"mining_old_{y}.png", 0.6)

    # numbers: first-time mining per year (zone_year_v2.csv, the same table as the brief figure)
    z = pd.read_csv(INTER / "zone_year_v2.csv")
    piv = z.pivot(index="year", columns="code", values="new_land_ha").fillna(0)
    per_year = {int(y): dict(lapampa=round(float(piv.loc[y, 7])), across=round(float(piv.loc[y, 5])),
                             mdd=round(float(piv.loc[y].sum()))) for y in YEARS}

    def anchor(geom):
        p = geom.representative_point()
        return _px(p.x, p.y)

    tnr = anp[anp.anp_codi == "RN09"].geometry.union_all()
    abz = za[za.anp_codi == "RC03"].geometry.union_all()
    tbz = za[za.anp_codi == "RN09"].geometry.union_all()
    corg = cor.geometry.union_all()
    road = ioh.geometry.union_all()
    rp = road.interpolate(0.30, normalized=True)
    labels = dict(
        lapampa=dict(text="La Pampa sector", pos=anchor(polys[7])),
        across=dict(text="Corridor across the road", pos=anchor(polys[5])),
        reserve=dict(text="Tambopata National Reserve", pos=anchor(tnr.intersection(frame))),
        tambopata_bz=dict(text="Tambopata buffer zone", pos=anchor(tbz.intersection(frame).difference(polys[7].buffer(0.05)))),
        amarakaeri_bz=dict(text="Amarakaeri buffer zone", pos=anchor(abz.intersection(frame))),
        corridor=dict(text="Legal mining corridor (D.L. 1100)", pos=anchor(corg.intersection(frame))),
        highway=dict(text="Interoceanic Highway", pos=_px(rp.x, rp.y)),
    )
    lp_b = polys[7].bounds
    events = [dict(year=e["year"], label=e["label"]) for e in PERU_EVENTS]
    events.insert(0, dict(year=2012, label="Legal corridor, D.L. 1100 (Feb 2012)"))
    nums = pd.read_csv(ROOT / "output" / "numbers.csv").set_index("id")       # registered by peru_anp.py
    data = dict(extent=EXTENT, size=[1920, 1080], years=YEARS, labels=labels, events=events,
                lapampa_bbox=[*_px(lp_b[0], lp_b[3]), *_px(lp_b[2], lp_b[1])],
                lapampa_lon=[_px(LP_LON[0], LAT_C)[0], _px(LP_LON[1], LAT_C)[0]],
                first_time_ha=per_year,
                reserve_addition_2025_ha=round(float(nums.loc["anp_tam_nr_addition_2025", "value"])),
                source="MapBiomas Peru Collection 4 (30 m); SERNANP; INGEMMET; RAISG")
    (OUTDIR / "map_data.json").write_text(json.dumps(data, indent=1))
    print("saved map_data.json")


if __name__ == "__main__":
    run()
