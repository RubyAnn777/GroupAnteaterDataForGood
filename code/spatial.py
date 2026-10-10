"""Spatial extension (robustness / brief part 4, NOT the core analysis): Amazon Mining Watch (AMW) onset patches
by protected-area zone and distance ring, Madre de Dios (Peru) and the Yanomami / Munduruku / Kayapo territories (Brazil).

Inputs (big, git-ignored, in data_raw/):  amw/amazon_basin_detections.geojson, funai/tis_poligonais.geojson,
sernanp/{anp_definitivas,zonas_amortiguamiento,mineria_ilegal}.geojson, ingemmet/corredor_minero_madre_de_dios_DL1100.geojson.
Outputs (small, committed): data_intermediate/amw_zone_year.csv, amw_rings_year.csv, sernanp_mineria_ilegal_summary.csv,
output/fig_map_madre_de_dios.png, fig_map_yanomami.png, fig_spatial_rings.png, numbers prefixed sp_.
If the big inputs are missing, the intermediates are read instead (figures that need patch geometry are skipped, with a warning).

CRS: area and distance in ESRI:102033 (South America Albers Equal Area Conic) for BOTH countries, one equal-area system.
     Maps are drawn in lon/lat (EPSG:4326) with a cos(latitude) aspect.

HOW TO READ THE AMW NUMBERS (all claims here are DESCRIPTION)
* AMW is a model of mining SCARS on land (Sentinel-2, 480 m patches), not MapBiomas class 4.2. Never compare or subtract
  its hectares with MapBiomas hectares (agent.md rule 6). 480 m half-overlapping patches overstate the mined area.
* onset_year 2018 is a STOCK (all mining present when the series starts), not an addition. Use 2019 onward.
* An onset needs corroboration in the following year (confirmed_in); 2025 and 2026 onsets are PROVISIONAL.
* It cannot see river dredging or mercury, and cannot tell legal from illegal mining.
* Zone definitions use today's boundaries (SERNANP 2025/26, INGEMMET 'referential' corridor), not the 2019 ones.
"""
from __future__ import annotations
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

from common import ROOT, OUT, style_axes, add_event_markers, set_year_ticks, finish_figure, EVENT_TITLE_PAD

RAW = ROOT / "data_raw"
INTER = ROOT / "data_intermediate"
INTER.mkdir(exist_ok=True)
AMW_FILE = RAW / "amw/amazon_basin_detections.geojson"
FUNAI_FILE = RAW / "funai/tis_poligonais.geojson"
Z_FILE, RINGS_FILE = INTER / "amw_zone_year.csv", INTER / "amw_rings_year.csv"

CRS_AREA = "ESRI:102033"                    # South America Albers Equal Area Conic
MDD_BOX = (-72.6, -14.6, -68.6, -10.5)      # lon/lat box around Madre de Dios (no department polygon available)
RING_EDGES = ((0, 10), (10, 25), (25, 50))  # km
YEARS = list(range(2018, 2027))
PROVISIONAL = {2025, 2026}
EV_SHORT = [dict(year=2019, label="Mercurio Feb 2019", color="#B03A2E", style="solid"),
            dict(year=2020, label="COVID-19 2020", color="#6C7A7B", style="dashed"),
            dict(year=2021, label="Restauración 2021", color="#6C7A7B", style="dashed"),
            dict(year=2023, label="Emergency Apr 2023", color="#6C7A7B", style="dashed")]
SRC_AMW = "Amazon Mining Watch (Earth Genome), model 48px_v4.10b ensemble, updated 2026-10-03, CC-BY-4.0"
SRC_SERNANP = "SERNANP (ANP, buffer zones), INGEMMET (D.L. 1100 corridor, referential)"
NOTE_AMW = ("AMW is a model of mining scars on land (480 m patches, upper bound), not MapBiomas hectares; 2018 is a stock, "
            "2025-26 provisional; cannot see river dredging or mercury. Description only.")
PERIODS = [("2018 (stock)", (2018, 2018), "#BDBDBD"), ("2019", (2019, 2019), "#F2B134"),
           ("2020-22", (2020, 2022), "#E4572E"), ("2023-24", (2023, 2024), "#8E1B3F"),
           ("2025-26 (prov.)", (2025, 2026), "#1B1B6B")]

# Zone precedence for Madre de Dios (first match wins; zones overlap, so each patch gets exactly ONE zone):
#   1 reserves (Tambopata NR, Bahuaja-Sonene NP, Amarakaeri RC)  >  2 buffer zones (Tambopata, Bahuaja-Sonene, Amarakaeri)
#   >  3 D.L. 1100 mining corridor (it overlaps buffer zones; a patch in both counts as buffer zone)  >  4 other ANP / other BZ
#   >  5 rest of the box.  The patch's CENTROID decides.
ZONE_ORDER = ["Tambopata NR", "Bahuaja-Sonene NP", "Amarakaeri RC", "Tambopata BZ", "Bahuaja-Sonene BZ", "Amarakaeri BZ",
              "Mining corridor (DL 1100)", "Other ANP and BZ", "Other Madre de Dios box"]


def _gpd():
    import geopandas as gpd
    return gpd


# --------------------------------------------------------------------------- core helpers
def yearly_new_ha(patches) -> dict[int, float]:
    """Hectares per onset year, overlap-free: area(union of that year's patches) minus area already covered by earlier years
    (patches overlap by half a width, so summing patch areas would double count). `patches` must be in CRS_AREA."""
    from shapely.ops import unary_union
    seen, out = None, {}
    for y in sorted(patches.onset_year.unique()):
        u = unary_union(patches.loc[patches.onset_year == y].geometry.values)
        new = u if seen is None else u.difference(seen)
        out[int(y)] = new.area / 1e4
        seen = u if seen is None else seen.union(u)
    return out


def _table(groups, region, col) -> list[dict]:
    rows = []
    for name, d in groups:
        ha = yearly_new_ha(d) if len(d) else {}
        for y in YEARS:
            rows.append({"region": region, col: name, "year": y, "new_ha": round(ha.get(y, 0.0), 1),
                         "n_patches": int((d.onset_year == y).sum()) if len(d) else 0,
                         "is_stock": y == 2018, "provisional": y in PROVISIONAL})
    return rows


def _ring(dist_km: np.ndarray, inside: np.ndarray | None = None) -> np.ndarray:
    lab = np.full(len(dist_km), None, dtype=object)
    for a, b in RING_EDGES:
        lab[(dist_km >= a) & (dist_km < b) & (lab == None)] = f"{a}-{b} km"   # noqa: E711
    if inside is not None:
        lab[inside] = "inside"
    return lab


# --------------------------------------------------------------------------- geometry builders
def build_peru(amw):
    gpd = _gpd()
    from shapely.geometry import Point
    from shapely.ops import unary_union
    anp = gpd.read_file(RAW / "sernanp/anp_definitivas.geojson").to_crs(CRS_AREA)
    za = gpd.read_file(RAW / "sernanp/zonas_amortiguamiento.geojson").to_crs(CRS_AREA)
    cor = gpd.read_file(RAW / "ingemmet/corredor_minero_madre_de_dios_DL1100.geojson").to_crs(CRS_AREA)
    g = lambda df, code: unary_union(df[df.anp_codi == code].geometry)
    nr = {"Tambopata NR": g(anp, "RN09"), "Bahuaja-Sonene NP": g(anp, "PN08"), "Amarakaeri RC": g(anp, "RC03")}
    bz = {"Tambopata BZ": g(za, "RN09"), "Bahuaja-Sonene BZ": g(za, "PN08"), "Amarakaeri BZ": g(za, "RC03")}
    named = ["RN09", "PN08", "RC03"]
    raw_geoms = {**nr, **bz, "Mining corridor (DL 1100)": unary_union(cor.geometry),
                 "Other ANP and BZ": unary_union(list(anp[~anp.anp_codi.isin(named)].geometry) +
                                                 list(za[~za.anp_codi.isin(named)].geometry))}
    zones, taken = {}, None
    for name in ZONE_ORDER[:-1]:
        gm = raw_geoms[name] if taken is None else raw_geoms[name].difference(taken)
        zones[name] = gm
        taken = gm if taken is None else taken.union(gm)
    box = gpd.GeoSeries([_box(MDD_BOX)], crs=4326).to_crs(CRS_AREA).iloc[0]
    zones["Other Madre de Dios box"] = box.difference(taken)
    p = amw.cx[MDD_BOX[0]:MDD_BOX[2], MDD_BOX[1]:MDD_BOX[3]].to_crs(CRS_AREA).copy()
    cent = p.geometry.centroid
    zlab = np.full(len(p), ZONE_ORDER[-1], dtype=object)
    done = np.zeros(len(p), bool)
    for name in ZONE_ORDER[:-2]:
        hit = (~done) & cent.within(zones[name]).values
        zlab[hit] = name; done |= hit
    hit = (~done) & cent.within(zones["Other ANP and BZ"]).values
    zlab[hit] = "Other ANP and BZ"
    p["zone"] = zlab
    # La Pampa: data-derived centre (see la_pampa_centre)
    lp = la_pampa_centre(p, cent, zones["Tambopata BZ"])
    d = cent.distance(lp).values / 1e3
    p["ring"] = _ring(d)
    return p, zones, lp, raw_geoms


def _box(b):
    from shapely.geometry import box
    return box(*b)


def la_pampa_centre(p, cent, tam_bz):
    """La Pampa has no official coordinate. DATA-DERIVED centre: the centroid of the densest cluster of AMW patches that were
    already mined by 2019 (onset <= 2019) INSIDE the Tambopata buffer zone (candidate grid 2.5 km, window +-5 km, then the
    centroid of patches within 5 km of the best cell). Using the 2018-19 stock to locate the treated site is deliberate:
    La Pampa IS where mining was concentrated when Mercurio started (MAAP #130). The earlier hand-typed guess
    (-70.42, -12.95) lay 10.5 km OUTSIDE the buffer zone and was dropped. Verification is saved in the numbers (sp_lp_*)."""
    from shapely.geometry import Point
    m = (p.onset_year.values <= 2019) & cent.within(tam_bz).values
    xs, ys = cent.x.values[m], cent.y.values[m]
    best = (-1, None)
    for cx in np.arange(xs.min(), xs.max(), 2500):
        for cy in np.arange(ys.min(), ys.max(), 2500):
            k = int(((abs(xs - cx) < 5000) & (abs(ys - cy) < 5000)).sum())
            if k > best[0]:
                best = (k, (cx, cy))
    cx, cy = best[1]
    sel = (abs(xs - cx) < 5000) & (abs(ys - cy) < 5000)
    return Point(xs[sel].mean(), ys[sel].mean())


def peru_zone_table(p):
    return pd.DataFrame(_table(p.groupby("zone"), "Madre de Dios zone", "unit"))


def peru_ring_table(p):
    return pd.DataFrame(_table(p.dropna(subset=["ring"]).groupby("ring"), "La Pampa ring", "unit"))


def build_brazil(amw, names=("Yanomami", "Munduruku", "Kayapó")):
    gpd = _gpd()
    from shapely.ops import unary_union
    ti = gpd.read_file(FUNAI_FILE)
    out, geoms = {}, {}
    for nm in names:
        sel = ti[ti.terrai_nome == nm].to_crs(CRS_AREA)
        assert len(sel), nm
        tg = unary_union(sel.geometry)
        bb = gpd.GeoSeries([tg.buffer(55e3)], crs=CRS_AREA).to_crs(4326).total_bounds
        p = amw.cx[bb[0]:bb[2], bb[1]:bb[3]].to_crs(CRS_AREA).copy()
        cent = p.geometry.centroid
        inside = cent.within(tg).values
        p["ring"] = _ring(cent.distance(tg).values / 1e3, inside)
        out[nm], geoms[nm] = p, tg
    return out, geoms


def brazil_ring_table(pats):
    rows = []
    for nm, p in pats.items():
        rows += _table(p.dropna(subset=["ring"]).groupby("ring"), f"{nm} TI ring", "unit")
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- SERNANP illegal-mining layer
def mineria_ilegal_summary(zones):
    """SERNANP 'mineria_ilegal' (179 features): descrip (free text), idtipact (type), ubiref (place), estado (Activo/Pasivo),
    objectid. NO date or year column, so it cannot be an enforcement time series. Summarise by type x status and, for the
    features in the Madre de Dios box, list them."""
    gpd = _gpd()
    m = gpd.read_file(RAW / "sernanp/mineria_ilegal.geojson")
    mm = m.to_crs(CRS_AREA)
    m["ha"] = mm.area / 1e4
    m["in_mdd_box"] = m.geometry.centroid.within(_box(MDD_BOX))
    s = (m.groupby(["idtipact", "estado"]).agg(n=("objectid", "size"), polygon_ha=("ha", "sum"),
                                              n_in_madre_de_dios_box=("in_mdd_box", "sum")).round(1).reset_index())
    s.to_csv(INTER / "sernanp_mineria_ilegal_summary.csv", index=False)
    print("SERNANP mineria_ilegal (no date field):\n", s.to_string(index=False), "\n in Madre de Dios box:")
    print(m[m.in_mdd_box][["idtipact", "estado", "ubiref", "ha"]].round(1).to_string(index=False))
    return s


# --------------------------------------------------------------------------- figures
def _aspect(ax, lat):
    ax.set_aspect(1 / np.cos(np.radians(lat)))


def _plot_patches(ax, p4326, size_note=None):
    for lab, (a, b), col in PERIODS:
        d = p4326[(p4326.onset_year >= a) & (p4326.onset_year <= b)]
        if len(d):
            d.plot(ax=ax, color=col, linewidth=0, zorder=2)


def _legend_periods(ax, loc="lower left", extra=()):
    h = [Patch(color=c, label=l) for l, _, c in PERIODS] + list(extra)
    ax.legend(handles=h, loc=loc, fontsize=7, frameon=True, framealpha=0.9, title="AMW onset year", title_fontsize=7)


def fig_map_mdd(p, zones, lp):
    gpd = _gpd()
    fig, ax = plt.subplots(figsize=(9, 6.4))
    ll = lambda g: gpd.GeoSeries([g], crs=CRS_AREA).to_crs(4326)
    style = {"Mining corridor (DL 1100)": ("#7F8C8D", "-", 1.0), "Tambopata BZ": ("#2E7D32", "-", 1.2),
             "Bahuaja-Sonene BZ": ("#2E7D32", ":", 1.0), "Amarakaeri BZ": ("#2E7D32", ":", 1.0)}
    for nm, (c, ls, lw) in style.items():
        ll(zones[nm]).boundary.plot(ax=ax, color=c, linestyle=ls, linewidth=lw, zorder=3)
    for nm in ("Tambopata NR", "Bahuaja-Sonene NP", "Amarakaeri RC"):
        g = ll(zones[nm])
        g.plot(ax=ax, facecolor="#D8EBD3", edgecolor="#1B5E20", linewidth=1.6 if nm == "Tambopata NR" else 1.0, zorder=1)
    p4 = p.to_crs(4326)
    _plot_patches(ax, p4)
    # rings and marker
    lpg = gpd.GeoSeries([lp], crs=CRS_AREA)
    for r in (10, 25, 50):
        ll(lp.buffer(r * 1e3)).boundary.plot(ax=ax, color="black", linestyle="--", linewidth=0.7, zorder=4)
    q = lpg.to_crs(4326).iloc[0]
    ax.plot(q.x, q.y, marker="*", color="black", markersize=13, markeredgecolor="white", zorder=5)
    ax.annotate("La Pampa (data-derived\ncentre; rings 10/25/50 km)", (q.x, q.y), xytext=(-69.45, -12.15),
                fontsize=7.5, arrowprops=dict(arrowstyle="-", color="black", lw=0.6), zorder=6)
    for nm, xy in [("Tambopata NR", (-69.55, -13.75)), ("Bahuaja-Sonene NP", (-69.4, -13.35)), ("Amarakaeri RC", (-71.2, -12.65))]:
        pass
    ax.set_xlim(-71.4, -68.6); ax.set_ylim(-14.35, -12.0)
    _aspect(ax, -12.5)
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    extra = [Patch(facecolor="#D8EBD3", edgecolor="#1B5E20", label="Reserve / national park (SERNANP)"),
             Line2D([], [], color="#2E7D32", label="Buffer zones (Tambopata solid)"),
             Line2D([], [], color="#7F8C8D", label="D.L. 1100 mining corridor"),
             Line2D([], [], color="black", linestyle="--", lw=0.7, label="La Pampa rings")]
    _legend_periods(ax, "lower left", extra)
    ax.set_title("Madre de Dios: new mining detected by satellite, by year of first detection", fontsize=11, loc="left")
    finish_figure(fig, f"Source: {SRC_AMW}; {SRC_SERNANP}. " + NOTE_AMW, OUT / "fig_map_madre_de_dios.png")


def fig_map_br(pats, geoms):
    gpd = _gpd()
    names = list(pats)
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.4))
    for ax, nm in zip(axes, names):
        g = gpd.GeoSeries([geoms[nm]], crs=CRS_AREA)
        p4 = pats[nm].to_crs(4326)
        _plot_patches(ax, p4)
        g.to_crs(4326).boundary.plot(ax=ax, color="#1B5E20", linewidth=1.3, zorder=3)
        for r in (10, 25, 50):
            gpd.GeoSeries([geoms[nm].buffer(r * 1e3)], crs=CRS_AREA).to_crs(4326).boundary.plot(
                ax=ax, color="black", linestyle="--", linewidth=0.5, zorder=4)
        b = gpd.GeoSeries([geoms[nm].buffer(55e3)], crs=CRS_AREA).to_crs(4326).total_bounds
        ax.set_xlim(b[0], b[2]); ax.set_ylim(b[1], b[3])
        _aspect(ax, (b[1] + b[3]) / 2)
        ax.set_title(f"{nm} TI (green): new mining by first-detection year", fontsize=9, loc="left")
        ax.tick_params(labelsize=7); ax.set_xlabel(""); ax.set_ylabel("")
        for s in ("top", "right"): ax.spines[s].set_visible(False)
    _legend_periods(axes[2], "lower left", [Line2D([], [], color="black", linestyle="--", lw=0.5, label="10 / 25 / 50 km outside")])
    import textwrap
    txt = "\n".join(textwrap.wrap(f"Source: {SRC_AMW}; FUNAI, tis_poligonais (WFS, accessed 2026-10). " + NOTE_AMW, 200))
    fig.text(0.01, 0.01, txt, fontsize=7.5, color="#555555", va="bottom")
    fig.tight_layout(rect=(0, 0.07, 1, 0.97))
    fig.savefig(OUT / "fig_map_yanomami.png", dpi=200); plt.close(fig)
    print("Saved output/fig_map_yanomami.png")


def fig_rings(rings, zone_tab):
    """AMW new area per onset year: three La Pampa rings + Tambopata NR core. 2019 onward (2018 is a stock)."""
    panels = [("La Pampa, 0-10 km", rings[rings.unit == "0-10 km"]), ("La Pampa, 10-25 km", rings[rings.unit == "10-25 km"]),
              ("La Pampa, 25-50 km", rings[rings.unit == "25-50 km"]),
              ("Inside Tambopata National Reserve", zone_tab[zone_tab.unit == "Tambopata NR"])]
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.6), sharex=True)
    for i, (ax, (ttl, d)) in enumerate(zip(axes.ravel(), panels)):
        d = d[d.year >= 2019].sort_values("year")
        col = "#E4572E" if i < 3 else "#1B5E20"
        ok, pv = d[~d.provisional], d[d.provisional]
        ax.plot(ok.year, ok.new_ha, marker="o", color=col, lw=1.6, ms=4)
        if len(pv):
            ax.plot([ok.year.iloc[-1]] + list(pv.year), [ok.new_ha.iloc[-1]] + list(pv.new_ha), color=col, lw=1.2, ls=":")
            ax.plot(pv.year, pv.new_ha, marker="o", mfc="white", color=col, lw=0, ms=4.5)
        ax.set_ylim(0, None); ax.set_title(ttl, fontsize=9.5, loc="left")
        style_axes(ax); set_year_ticks(ax, range(2019, 2027)); ax.set_xlim(2018.4, 2026.4)
        add_event_markers(ax, label=False, events=EV_SHORT)
        if i % 2 == 0: ax.set_ylabel("New AMW area (ha)")
    fig.suptitle("Satellite-detected new mining by year of first detection (hollow dots and dotted line = provisional)",
                 fontsize=10.5, x=0.01, ha="left", y=0.995)
    fig.legend(handles=[Line2D([], [], color=e["color"], ls="-" if e["style"] == "solid" else "--", label=e["label"]) for e in EV_SHORT],
               loc="upper center", ncol=4, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.965))
    finish_figure(fig, f"Source: {SRC_AMW}; {SRC_SERNANP}. Rings are measured from a data-derived La Pampa centre and overlap "
                  "the mining corridor and other buffer zones. " + NOTE_AMW, OUT / "fig_spatial_rings.png", event_note=True)


# --------------------------------------------------------------------------- numbers
def register(reg, z, r, rb, lp_info):
    src = "Amazon Mining Watch (AMW) onset patches x SERNANP / INGEMMET / FUNAI geometry (data_intermediate/amw_*.csv)"
    zz = z.set_index(["unit", "year"]).new_ha
    for y in (2019, 2024, 2025, 2026):
        reg.add(f"sp_amw_tambopata_nr_new_ha_{y}", zz[("Tambopata NR", y)], "ha",
                f"AMW area with first detection in {y} inside Tambopata National Reserve (AMW model hectares, not MapBiomas)"
                + (" PROVISIONAL" if y in PROVISIONAL else ""), "description", src)
    reg.add("sp_amw_tambopata_nr_new_ha_2019_2024", sum(zz[("Tambopata NR", y)] for y in range(2019, 2025)), "ha",
            "AMW new area inside Tambopata NR, sum of onset years 2019-2024 (confirmed)", "description", src)
    reg.add("sp_amw_tambopata_nr_new_ha_2025_2026", zz[("Tambopata NR", 2025)] + zz[("Tambopata NR", 2026)], "ha",
            "AMW new area inside Tambopata NR, onset 2025 + 2026 (PROVISIONAL)", "description", src)
    reg.add("sp_amw_tambopata_bz_new_ha_2019_2024", sum(zz[("Tambopata BZ", y)] for y in range(2019, 2025)), "ha",
            "AMW new area in the Tambopata buffer zone (excl. reserve), onset 2019-2024", "description", src)
    rr = r[r.region == "La Pampa ring"].set_index(["unit", "year"]).new_ha
    tot = lambda y0, y1: {u: sum(rr[(u, y)] for y in range(y0, y1 + 1)) for u in ("0-10 km", "10-25 km", "25-50 km")}
    for lab, (y0, y1) in {"2019_21": (2019, 2021), "2022_24": (2022, 2024)}.items():
        t = tot(y0, y1); s = sum(t.values())
        for u, v in t.items():
            k = u.split(" ")[0].replace("-", "_")
            reg.add(f"sp_lp_ring_{k}km_share_{lab}", 100 * v / s, "percent",
                    f"Share of AMW new area within 50 km of La Pampa that falls in the {u} ring, onset {y0}-{y1}", "description", src)
        reg.add(f"sp_lp_ring_0_50km_ha_{lab}", s, "ha", f"AMW new area within 50 km of La Pampa, onset {y0}-{y1}, per year mean: see /{y1-y0+1}",
                "description", src)
    for k, v in lp_info.items():
        reg.add(k, v, "deg" if "lat" in k or "lon" in k else "km", f"La Pampa centre verification: {k}", "description", src)
    yb = rb[rb.region == "Yanomami TI ring"].set_index(["unit", "year"]).new_ha
    for lab, (y0, y1) in {"2019_22": (2019, 2022), "2023_24": (2023, 2024)}.items():
        reg.add(f"sp_yanomami_inside_new_ha_{lab}", sum(yb[("inside", y)] for y in range(y0, y1 + 1)), "ha",
                f"AMW new area inside the Yanomami territory, onset {y0}-{y1}", "description", src)
        reg.add(f"sp_yanomami_outside_0_50km_new_ha_{lab}",
                sum(yb[(u, y)] for u in ("0-10 km", "10-25 km", "25-50 km") for y in range(y0, y1 + 1)), "ha",
                f"AMW new area 0-50 km outside the Yanomami territory, onset {y0}-{y1}", "description", src)


# --------------------------------------------------------------------------- entry point
def run(reg):
    t0 = time.time()
    have_raw = AMW_FILE.exists() and FUNAI_FILE.exists()
    lp_info = {}
    if have_raw:
        gpd = _gpd()
        amw = gpd.read_file(AMW_FILE)[["onset_year", "status", "geometry"]]
        print(f"spatial: AMW loaded ({len(amw)} patches) in {time.time()-t0:.0f}s")
        p, zones, lp, raw_geoms = build_peru(amw)
        ztab, rtab = peru_zone_table(p), peru_ring_table(p)
        pats, geoms = build_brazil(amw)
        btab = brazil_ring_table(pats)
        ztab.to_csv(Z_FILE, index=False)
        pd.concat([rtab, btab]).to_csv(RINGS_FILE, index=False)
        q = gpd.GeoSeries([lp], crs=CRS_AREA).to_crs(4326).iloc[0]
        lp_info = {"sp_lp_lon": q.x, "sp_lp_lat": q.y,
                   "sp_lp_dist_to_tambopata_bz_km": lp.distance(zones["Tambopata BZ"]) / 1e3,
                   "sp_lp_dist_to_tambopata_nr_km": lp.distance(zones["Tambopata NR"]) / 1e3}
        mineria_ilegal_summary(zones)
        print(f"spatial: tables done {time.time()-t0:.0f}s; zone areas km2:",
              {k: round(v.area / 1e6) for k, v in zones.items()})
        fig_map_mdd(p, zones, lp); fig_map_br(pats, geoms)
    else:
        if not (Z_FILE.exists() and RINGS_FILE.exists()):
            warnings.warn("spatial: raw inputs AND intermediates missing; skipping spatial step"); return
        warnings.warn("spatial: big raw inputs missing (data_raw/amw, data_raw/funai); using committed intermediates in "
                      "data_intermediate/, skipping map figures")
        ztab, allr = pd.read_csv(Z_FILE), pd.read_csv(RINGS_FILE)
        rtab, btab = allr[allr.region == "La Pampa ring"], allr[allr.region != "La Pampa ring"]
    allr = pd.concat([rtab, btab]) if have_raw else pd.concat([rtab, btab])
    fig_rings(rtab, ztab)
    if not have_raw:
        lp_info = {}
    register(reg, ztab, allr, allr, lp_info)
    print(f"spatial: done in {time.time()-t0:.0f}s")
