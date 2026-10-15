"""Map layers for the presentation animation (storyline v3, slides 3-5): transparent PNGs + one JSON for Remotion.

Standalone, NOT wired into main.py: it reads git-ignored inputs (data_intermediate/zones_mdd.tif, the MapBiomas Peru
Col 4 yearly rasters, SERNANP / INGEMMET / RAISG vectors). Run:  uv run python code/slides_map_export.py

Plan v3: ONE measure, net mining additions = new land + re-mined − stopped (definitions.py). The timeline animation
shows the three flows as pixels on the map, with the same definitions as code/raster_zones.py:
  new land  mining at t, never mining in any earlier year since 1985        (brown)
  re-mined  mining at t, not at t-1, mining in some year before t-1         (amber)
  stopped   mining at t-1, not at t                                          (teal)
They are derived here by streaming data_raw/mapbiomas_peru_raster/peru_coverage-col4_{y}.tif (class 30) over the map
window, 1985-2025. The per-year numbers on screen (net and parts, La Pampa sector and the corridor across the road) come
from zonedata.region_units() (the same table as output/numbers.csv); the pixel counts here are a check only.

Zones: data_intermediate/zones_mdd.tif (band 1 zone code per definitions.ZONES, band 2 first-mined year, band 3
tenure). La Pampa sector = code 3 (Tambopata buffer zone, 70.15-69.80 W); corridor across the road = code 8. The
buffer zones are drawn whole from the SERNANP polygons (Tambopata BZ incl. Kotsimba).

Every layer is drawn on ONE extent (EXTENT, lon/lat, plate carrée stretched so a degree of longitude has its true
ground width at the map centre) into a 3840 x 2160 transparent PNG, so the layers stack exactly in the video.
Outputs (presentation/animation/public/):
  layer_base / layer_rivers / layer_zones / layer_highway / layer_corridor   background layers
  layer_lapampa.png, layer_across.png        orange / blue outlines (map build, part A)
  layer_lapampa_w.png, layer_across_w.png    white / light-blue outlines (timeline: no orange next to the flows)
  mining_by2018.png                          land mapped as mining by 2018 (grey)
  stock_YYYY.png                             land mapped as mining in year YYYY (grey), 2009-2025
  flows_YYYY.png                             that year's three flows (brown / amber / teal, with a soft glow)
  map_data.json                              extent, label anchors, events, per-year net + parts for both units
"""
from __future__ import annotations
import json

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import ROOT, C, PERU_EVENTS
import definitions as D
import zonedata as Z

RAW, INTER = ROOT / "data_raw", ROOT / "data_intermediate"
RASTER = RAW / "mapbiomas_peru_raster" / "peru_coverage-col4_{y}.tif"
ZONES_TIF = INTER / "zones_mdd.tif"
OUTDIR = ROOT / "presentation" / "animation" / "public"
W_PX, H_PX = 3840, 2160                       # rendered layers; the video shows them at 1920 x 1080
LAT0, LAT1 = -13.36, -12.36                   # 1.0 degree of latitude
LAT_C = (LAT0 + LAT1) / 2
LON_C = -69.98
LON_SPAN = (LAT1 - LAT0) * (W_PX / H_PX) / np.cos(np.radians(LAT_C))   # true ground aspect at the centre
EXTENT = (LON_C - LON_SPAN / 2, LON_C + LON_SPAN / 2, LAT0, LAT1)        # lon0, lon1, lat0, lat1
FIRST_RASTER = 1985
YEARS = list(range(2010, 2026))               # the timeline ("2010-2025 in one minute")
MINING = 30
CODE_LP, CODE_ACROSS = D.ZONE_CODE["lapampa"], D.ZONE_CODE["corridor_across"]

LAND, WATER, OLD = "#2b434a", "#6f9fb6", "#9aa5a2"
# Flow colours for the DARK map: the same hue families as common.C (new brown, re-mined amber, stopped teal), stepped
# lighter for the slate surface. dataviz validate_palette.js on #2b434a: CVD worst 14.1, normal-vision 17.1 (pass);
# amber sits just above the dark lightness band, so the flows always carry a legend with words.
FLOW = {"new": "#b5683a", "remined": "#dba21a", "stopped": "#1fa595"}


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


def _window(path):
    import rasterio
    from rasterio.windows import from_bounds
    with rasterio.open(path) as r:
        w = from_bounds(EXTENT[0], EXTENT[2], EXTENT[1], EXTENT[3], r.transform).round_offsets().round_lengths()
        return w, r.window_transform(w)


def _read(path, band=1, win=None):
    import rasterio
    with rasterio.open(path) as r:
        w = win or _window(path)[0]
        return r.read(band, window=w, boundless=True, fill_value=0)


def _pool(mask, k=2):
    h, w = (mask.shape[0] // k) * k, (mask.shape[1] // k) * k
    return mask[:h, :w].reshape(h // k, k, w // k, k).max(axis=(1, 3))


def _to_png(rgba: np.ndarray, name: str):
    """RGBA float array on the raster window (pooled) -> 3840 x 2160 PNG on EXTENT (the window IS the extent)."""
    from PIL import Image
    im = Image.fromarray((np.clip(rgba, 0, 1) * 255).astype(np.uint8), "RGBA").resize((W_PX, H_PX), Image.BILINEAR)
    im.save(OUTDIR / name, optimize=True)
    print("saved", name)


def _flat(mask, color, alpha=1.0):
    rgba = np.zeros(mask.shape + (4,), np.float32)
    rgba[mask] = matplotlib.colors.to_rgba(color, alpha)
    return rgba


def _glow(masks: list[tuple[np.ndarray, str]]):
    """Flows of one year: dilated core + soft glow per flow, drawn in order (later on top), so a few hectares stay
    visible when projected."""
    from scipy.ndimage import binary_dilation, gaussian_filter
    out = np.zeros(masks[0][0].shape + (4,), np.float32)
    for m, col in masks:
        if not m.any():
            continue
        core = binary_dilation(m, iterations=1).astype(np.float32)
        glow = np.clip(gaussian_filter(binary_dilation(m, iterations=2).astype(np.float32), 2.5) * 1.4, 0, 1)
        a = np.maximum(glow * 0.45, core)
        rgb = np.array(matplotlib.colors.to_rgb(col), np.float32)
        out[..., :3] = out[..., :3] * (1 - a[..., None]) + rgb * a[..., None]
        out[..., 3] = np.maximum(out[..., 3], a)
    return out


def _px(lon, lat):
    """lon/lat -> pixel at 1920 x 1080 (the video frame)."""
    x = (lon - EXTENT[0]) / (EXTENT[1] - EXTENT[0]) * 1920
    y = (EXTENT[3] - lat) / (EXTENT[3] - EXTENT[2]) * 1080
    return [round(float(x), 1), round(float(y), 1)]


def flow_layers(zone_win):
    """Stream the yearly rasters 1985-2025 over the window; write stock_YYYY.png and flows_YYYY.png for YEARS.
    Returns pixel-count checks (ha) per year for La Pampa and the corridor across the road."""
    import rasterio
    win, t = _window(str(RASTER).format(y=2018))
    lat = t.f + (np.arange(int(win.height)) + 0.5) * t.e                      # pixel area by row (ha)
    row_ha = (abs(t.a) * 111_320 * np.cos(np.radians(lat))) * (abs(t.e) * 110_574) / 1e4
    ever = prev = before_prev = None
    check = {}
    for y in range(FIRST_RASTER, YEARS[-1] + 1):
        mine = _read(str(RASTER).format(y=y), win=win) == MINING
        if ever is None:
            ever = np.zeros_like(mine); prev = np.zeros_like(mine); before_prev = np.zeros_like(mine)
        if y >= YEARS[0] - 1:
            if y >= YEARS[0]:
                new = mine & ~ever
                rem = mine & ~prev & before_prev
                stp = prev & ~mine
                for code, key in ((CODE_LP, "lapampa"), (CODE_ACROSS, "corridor_across")):
                    z = zone_win == code
                    check.setdefault(key, {})[y] = {k: float((m & z).sum(axis=1) @ row_ha)
                                                    for k, m in (("new", new), ("remined", rem), ("stopped", stp))}
                _to_png(_glow([(_pool(stp), FLOW["stopped"]), (_pool(rem), FLOW["remined"]), (_pool(new), FLOW["new"])]),
                        f"flows_{y}.png")
            _to_png(_flat(_pool(mine), OLD, 0.55), f"stock_{y}.png")
        before_prev |= prev
        ever |= mine
        prev = mine
        if y % 10 == 0:
            print(f"  streamed {y}")
    return check


def run():
    import geopandas as gpd
    from shapely.geometry import box, shape
    import rasterio
    import rasterio.features
    OUTDIR.mkdir(parents=True, exist_ok=True)
    for old in list(OUTDIR.glob("mining_hot_*.png")) + list(OUTDIR.glob("mining_old_*.png")) + [OUTDIR / "mining_pre2008.png"]:
        old.unlink(missing_ok=True)                    # superseded v2 layers (first-time mining only)
    frame = box(EXTENT[0], EXTENT[2], EXTENT[1], EXTENT[3])

    anp = gpd.read_file(RAW / "sernanp/anp_definitivas.geojson").to_crs(4326)
    za = gpd.read_file(RAW / "sernanp/zonas_amortiguamiento.geojson").to_crs(4326)
    cor = gpd.read_file(RAW / "ingemmet/corredor_minero_madre_de_dios_DL1100.geojson").to_crs(4326)
    roads = gpd.read_file(RAW / "raisg/vias_nacionales_mdd_box.geojson")
    ioh = roads[roads.sigla == "PE-30C"].to_crs(4326)
    ti = gpd.read_file(INTER / "native_communities_mdd.geojson").to_crs(4326)
    clip = lambda g: gpd.clip(g, frame)
    anp, za, cor, ioh, ti = clip(anp), clip(za), clip(cor), clip(ioh), clip(ti)

    fig, ax = _canvas()
    ax.add_patch(plt.Rectangle((EXTENT[0], EXTENT[2]), LON_SPAN, 1.0, color=LAND, zorder=0))
    _save(fig, "layer_base.png")

    lc = _read(str(RASTER).format(y=2018))
    _to_png(_flat(_pool(np.isin(lc, (33,))), WATER), "layer_rivers.png")

    fig, ax = _canvas()                                # buffer zones whole (SERNANP), reserves/parks, communities
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

    # La Pampa sector and the corridor across the road, polygonised from the v3 zone raster
    zwin, zt = _window(ZONES_TIF)
    zc = _read(ZONES_TIF, 1, zwin)
    fy = _read(ZONES_TIF, 2, zwin)
    polys = {}
    for code, stem, color, white in ((CODE_LP, "lapampa", C["lapampa"], "#f3f1ea"), (CODE_ACROSS, "across", "#5fa8dc", "#9fd0f2")):
        m = (zc == code).astype(np.uint8)
        geoms = [shape(g).buffer(0) for g, v in rasterio.features.shapes(m, mask=m.astype(bool), transform=zt) if v == 1]
        g = gpd.GeoSeries(geoms, crs=4326).union_all().buffer(0.004).buffer(-0.004).simplify(0.002)
        polys[code] = g
        for name, col, fill in ((f"layer_{stem}.png", color, 0.18), (f"layer_{stem}_w.png", white, 0.0)):
            fig, ax = _canvas()
            if fill:
                gpd.GeoSeries([g]).plot(ax=ax, color=col, alpha=fill, linewidth=0)
            gpd.GeoSeries([g]).boundary.plot(ax=ax, color=col, linewidth=7 if fill else 5,
                                             linestyle="-" if fill else (0, (4, 2)))
            _save(fig, name)

    _to_png(_flat(_pool((fy > 0) & (fy <= D.REF_YEAR)), OLD, 0.6), "mining_by2018.png")

    # the three flows, year by year (pixel streaming, same definitions as raster_zones.py)
    check = flow_layers(zc)

    # numbers on screen: the registry table (same as numbers.csv), checked against our streamed pixel counts
    ru = Z.region_units()
    per_year = {}
    for y in YEARS:
        rec = {}
        for u in ("lapampa", "corridor_across"):
            r = ru[(ru.unit == u) & (ru.year == y)].iloc[0]
            rec[u] = {m: round(float(r[D.COLS[m]])) for m in ["net"] + D.PARTS}
            for m in D.PARTS:
                diff = abs(check[u][y][m] - float(r[D.COLS[m]]))
                assert diff <= max(2.0, 0.02 * float(r[D.COLS[m]])), f"{u} {y} {m}: stream {check[u][y][m]:.0f} vs registry {r[D.COLS[m]]:.0f}"
        per_year[str(y)] = rec

    def anchor(geom):
        p = geom.representative_point()
        return _px(p.x, p.y)

    tnr = anp[anp.anp_codi == "RN09"].geometry.union_all()
    labels = dict(lapampa=dict(text="La Pampa sector", pos=anchor(polys[CODE_LP])),
                  across=dict(text="Corridor across the road", pos=anchor(polys[CODE_ACROSS])),
                  reserve=dict(text="Tambopata National Reserve", pos=anchor(tnr.intersection(frame))))
    nums = pd.read_csv(ROOT / "output" / "numbers.csv").set_index("id")
    events = [dict(year=e["year"], label=e["label"]) for e in PERU_EVENTS]
    data = dict(extent=EXTENT, size=[1920, 1080], years=YEARS, labels=labels, events=events,
                flows=per_year, flow_colors=FLOW,
                reserve_net_2025_ha=round(float(nums.loc["tambopata_nr_2025_net", "value"])),
                measure=D.OUTCOME_LABEL,
                source="MapBiomas Peru Collection 4 (30 m, class 4.2 mining); SERNANP; INGEMMET; RAISG")
    (OUTDIR / "map_data.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print("saved map_data.json")


if __name__ == "__main__":
    run()
