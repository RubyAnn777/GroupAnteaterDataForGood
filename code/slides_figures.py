"""Slide figures for the FZS talk (docs/presentation/STORYLINE.md, slides 5-11 + one backup): output/slides/*.png.

Same visual system as every other figure (common.py palette C, takeaway title + subtitle, direct labels, source line),
scaled for projection: 16:9 (12 x 6.75 in), body text >= 14 pt, title 24 pt, saved at 200 dpi (2400 px wide).
Every number written on a slide is computed here from the same data as the pages and registered as `sl_*`.
All DESCRIPTION; slide 7 shows the tests behind the one conditional causal claim, it does not make a new one.
"""
from __future__ import annotations
import textwrap
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import (ROOT, OUT, C, INK, INK2, MUTED, AXIS, GRID, style_axes, PERU_EVENTS, placebo_rank,
                    SRC_MAPBIOMAS, SRC_PRICE)
import peru
import peru_models
import v2_tests

SL = OUT / "slides"
INTER = ROOT / "data_intermediate"
W, H, DPI = 13.0, 5.0, 200      # full content width under the slide title (deck reads w_in/h_in)
TITLES: dict = {}          # slide name -> title / subtitle / source (the PPT slide carries the title)
FS = dict(title=24, sub=15, body=15, tick=14, label=15, small=13, source=11)
PERIODS = {"2016–18": (2016, 2018), "2019–21": (2019, 2021), "2022–25": (2022, 2025)}
SRC_ZONES = ("MapBiomas Peru Collection 4 annual maps (30 m, class 4.2 mining, legal and illegal), cut to our zones "
             "(La Pampa sector = Tambopata buffer zone 70.15–69.80° W; legal corridor = D.L. 1100, INGEMMET). "
             "First-time mining = pixels mapped as mining for the first time since 1985.")
NO_SEE = "Satellites cannot see river dredges or mercury."
RC = {"font.size": FS["body"], "xtick.labelsize": FS["tick"], "ytick.labelsize": FS["tick"],
      "axes.titlesize": FS["label"], "axes.labelsize": FS["label"], "xtick.major.size": 4}


# --------------------------------------------------------------------------- slide helpers
def _fig(nrows=1, ncols=1, **kw):
    with plt.rc_context(RC):
        fig, axes = plt.subplots(nrows, ncols, figsize=(W, H), **kw)
    return fig, axes

def _head(fig, title, sub=None):
    """Takeaway title + subtitle go to slide_titles.json (drawn by the PPT), not into the image."""
    fig._slide_title = (title, sub or "")

def _ticks(ax, years, step=1):
    ax.set_xticks(years[::step])
    ax.set_xticklabels([str(y) if i == 0 or y % 5 == 0 else f"'{str(y)[2:]}" for i, y in enumerate(years)][::step])
    ax.tick_params(labelsize=FS["tick"])
    ax.tick_params(axis="y", labelsize=FS["tick"])

def _events(ax, label=True, events=None, y_text=1.02):
    """Event lines at Y - 0.5 (common.py convention); short labels alternate between two rows above the axes."""
    events = PERU_EVENTS if events is None else events
    lo, hi = ax.get_xlim()
    k = 0
    for ev in events:
        x = ev["year"] - 0.5
        if not lo <= x <= hi:
            continue
        solid = ev["style"] == "solid"
        ax.axvline(x, color=INK if solid else AXIS, ls="-" if solid else (0, (3, 2)), lw=1.4 if solid else 1.0, zorder=0.5)
        if label:
            ax.annotate(ev["short"], xy=(x, y_text), xycoords=("data", "axes fraction"), xytext=(0, 2 + 17 * (k % 2)),
                        textcoords="offset points", ha="center", va="bottom", fontsize=FS["small"],
                        color=INK if solid else INK2, fontweight="semibold" if solid else "normal", annotation_clip=False)
        k += 1
    ax.set_xlim(lo, hi)

def _band(ax, a, b, color="#ebe6dc"):
    ax.axvspan(a - 0.5, b + 0.5, color=color, zorder=-1, lw=0)

def _means(ax, s, color, fmt="{:,.0f}", dy=10, show=True):
    """Thick translucent segment per period = period mean, value written above it (ink)."""
    out = {}
    for p, (a, b) in PERIODS.items():
        m = float(s.loc[a:b].mean()); out[p] = m
        ax.plot([a - 0.4, b + 0.4], [m, m], color=color, lw=7, alpha=0.45, solid_capstyle="butt", zorder=2)
        if show:
            ax.annotate(fmt.format(m), xy=((a + b) / 2, m), xytext=(0, dy), textcoords="offset points", ha="center",
                        va="bottom", fontsize=FS["body"], color=INK, fontweight="semibold", zorder=6,
                        bbox=dict(boxstyle="round,pad=0.2", fc="#fbfaf7", ec="none", alpha=0.9))
    return out

def _label(ax, x, y, text, dx=10, dy=0, fs=None, weight="semibold", ha="left", va="center"):
    ax.annotate(text, xy=(x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va,
                fontsize=fs or FS["body"], color=INK, fontweight=weight, annotation_clip=False, linespacing=1.15)

def _save(fig, name, source, top=0.88, bottom=None, left=0.07, right=0.97, xlab=False, **adj):
    t, sub = getattr(fig, "_slide_title", ("", ""))
    w_in, h_in = fig.get_size_inches()
    TITLES[name.removesuffix(".png")] = dict(title=t, subtitle=sub.replace("\n", " "), source="Source: " + source,
                                             w_in=round(float(w_in), 2), h_in=round(float(h_in), 2))
    top = min(0.88, top + 0.14)          # no title band inside the image any more
    text = "\n".join(textwrap.wrap("Source: " + source, 150))
    n = text.count("\n") + 1
    fig.text(0.02, 0.015, text, fontsize=FS["source"], color=MUTED, va="bottom", ha="left", linespacing=1.3)
    bottom = bottom if bottom is not None else (0.55 + 0.21 * n + (0.3 if xlab else 0)) / H   # inches: ticks + source (+ x label)
    fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, **adj)
    SL.mkdir(parents=True, exist_ok=True)
    fig.savefig(SL / name, dpi=DPI)
    plt.close(fig)
    print(f"Saved output/slides/{name}")

def _fmt_y(ax, pct=False):
    from matplotlib.ticker import FuncFormatter
    style_axes(ax)
    ax.yaxis.set_major_formatter(FuncFormatter((lambda v, p: f"{v:.0%}") if pct else (lambda v, p: f"{v:,.0f}".replace("-", "−"))))
    ax.tick_params(axis="y", labelsize=FS["tick"])


# --------------------------------------------------------------------------- 1: Tambopata net additions
def s01_net(pack, reg):
    _, adds, _ = peru.build_series(pack)
    s = adds[peru.TAM].loc[2010:2025]
    yrs = list(s.index)
    fig, ax = _fig()
    _band(ax, 2019, 2021)
    ax.axhline(0, color=AXIS, lw=1)
    ax.plot(yrs, s, "-", color=C["lapampa"], lw=3, zorder=3)
    ax.plot(yrs, s, "o", color=C["lapampa"], ms=8, mec="white", mew=1.5, zorder=4)
    m = _means(ax, s, C["lapampa"], dy=12)
    for p, v in m.items():
        reg.add(f"sl_tam_net_{p.replace('–', '_')}", v, "ha/yr", f"Mean net annual addition, Tambopata BZ (course table), {p}",
                "description", "peru_bufferzone_year.csv")
    fall = 1 - m["2019–21"] / m["2016–18"]
    reg.add("sl_tam_net_fall_share", fall, "share", "Fall in mean net addition, Tambopata BZ, 2016-18 to 2019-21", "description",
            "peru_bufferzone_year.csv")
    assert np.isclose(m["2016–18"], reg.get("mean_add_tambopata_2016_18")) and np.isclose(m["2019–21"], reg.get("mean_add_tambopata_2019_21"))
    ax.set_xlim(2009.4, 2025.6); ax.set_ylim(min(-150, s.min() * 1.2), s.max() * 1.15)
    _fmt_y(ax); _ticks(ax, yrs); _events(ax)
    _label(ax, 2025, s.loc[2025], "Tambopata\nbuffer zone", dx=12)
    ax.text(2019.95, 0.97, "Bars = period means", transform=ax.get_xaxis_transform(), ha="center", va="top",
            fontsize=FS["small"], color=INK2)
    _head(fig, f"Net new mining in the Tambopata buffer zone fell {fall:.0%} in 2019–21, then came back",
          "Net annual addition to mapped mining area (this year minus last year), ha per year. Shaded: 2019–21.")
    _save(fig, "slide_01_tambopata_net.png", f"{SRC_MAPBIOMAS}, course table peru_bufferzone_year.csv (all department rows summed). "
          f"Net additions can hide returns to old pits. {NO_SEE}", right=0.88)


# --------------------------------------------------------------------------- 2: where first-time mining appeared
GROUPS = [  # (label, zone codes, colour) bottom -> top
    ("La Pampa sector", [7], C["lapampa"]),
    ("Corridor across the road", [5], C["corridor"]),
    ("Rest of the legal corridor", [6], C["corridor_rest"]),
    ("Native communities", [3, 4], C["native"]),
    ("Rest of Madre de Dios", [1, 2, 8, 9, 10, 11, 12], C["other"]),
]

def s02_zones(reg):
    z = pd.read_csv(INTER / "zone_year_v2.csv").pivot(index="year", columns="code", values="new_land_ha").fillna(0).loc[2010:2025]
    g = pd.DataFrame({lab: z[codes].sum(axis=1) for lab, codes, _ in GROUPS})
    tot = g.sum(axis=1); yrs = list(g.index)
    pm = lambda s: {p: float(s.loc[a:b].mean()) for p, (a, b) in PERIODS.items()}
    mt, ml, mx = pm(tot), pm(g["La Pampa sector"]), pm(g["Corridor across the road"])
    corr = pm(g["Corridor across the road"] + g["Rest of the legal corridor"])
    for p in PERIODS:
        k = p.replace("–", "_")
        reg.add(f"sl_new_total_{k}", mt[p], "ha/yr", f"Mean first-time mining, all Madre de Dios, {p}", "description", "zone_year_v2.csv")
        reg.add(f"sl_new_lapampa_{k}", ml[p], "ha/yr", f"Mean first-time mining, La Pampa sector, {p}", "description", "zone_year_v2.csv")
        reg.add(f"sl_new_across_{k}", mx[p], "ha/yr", f"Mean first-time mining, corridor across the road, {p}", "description", "zone_year_v2.csv")
        reg.add(f"sl_new_corridor_share_{k}", corr[p] / mt[p], "share", f"Legal corridor share of first-time mining, {p}", "description", "zone_year_v2.csv")
    assert np.isclose(mt["2016–18"], reg.get("v2_new_total_2016_18"))
    lp_ratio = ml["2019–21"] / ml["2016–18"]
    lp_word = "halved" if 0.4 <= lp_ratio <= 0.6 else f"fell {1 - lp_ratio:.0%}"

    for version in ("a", "b"):
        fig, ax = _fig()
        _band(ax, 2019, 2021)
        bottom = np.zeros(len(yrs))
        groups = GROUPS if version == "b" else [GROUPS[0], ("Rest", [], "#d3d1cb")]
        gg = g.assign(Rest=g.drop(columns="La Pampa sector").sum(axis=1))
        for lab, _, col in groups:
            c = col if (version == "b" or lab == "La Pampa sector") else "#d3d1cb"
            ax.bar(yrs, gg[lab], bottom=bottom, color=c, width=0.74, zorder=2)
            ax.bar(yrs, [0] * len(yrs), bottom=bottom + gg[lab], width=0.74, color="white", edgecolor="white", lw=1.5, zorder=3)
            if version == "b" or lab == "La Pampa sector":
                y = bottom[-1] + gg[lab].iloc[-1] / 2
                _label(ax, 2025.4, y, lab, dx=8, fs=FS["small"])
            bottom = bottom + gg[lab].values
        if version == "a":
            _label(ax, 2025.4, bottom[-1] * 0.6, "Rest of\nMadre de Dios", dx=8, fs=FS["small"], weight="normal")
        ax.set_xlim(2009.4, 2025.6); ax.set_ylim(0, tot.max() * 1.12)
        _fmt_y(ax); _ticks(ax, yrs); _events(ax)
        if version == "a":
            _head(fig, f"La Pampa: land mined for the first time {lp_word} in 2019–21",
                  f"Land mined for the first time, ha per year (a new measure: not net additions). La Pampa sector: "
                  f"{ml['2016–18']:,.0f} → {ml['2019–21']:,.0f} → {ml['2022–25']:,.0f} ha/yr (2016–18 → 2019–21 → 2022–25).")
        else:
            _head(fig, "Madre de Dios as a whole didn't fall: new mining grew in the legal corridor",
                  f"Land mined for the first time, ha per year. All Madre de Dios: {mt['2016–18']:,.0f} → {mt['2019–21']:,.0f} → "
                  f"{mt['2022–25']:,.0f} ha/yr; legal corridor share {reg.get('v2_corridor_share_2016_18'):.0f}% → "    # same share as the walkthrough
                  f"{reg.get('v2_corridor_share_2019_21'):.0f}% → {reg.get('v2_corridor_share_2022_25'):.0f}% (mean of yearly shares).")
        _save(fig, f"slide_02{version}_zones.png", f"{SRC_ZONES} Legality is by location; the map class can't tell legal "
              f"from illegal mining. {NO_SEE}", right=0.80)


# --------------------------------------------------------------------------- 3: share north of the road
def s03_road(reg):
    import raster_zones as rz
    b = pd.read_csv(rz.OUT_BAND)
    w = b.pivot_table(index="year", columns="km_from_road", values="new_land_ha", aggfunc="sum").fillna(0)
    share = (w[[c for c in w if c >= 0]].sum(axis=1) / w.sum(axis=1)).loc[2006:2025]     # same definition as v2_tests.t1_t2
    yrs = list(share.index)
    m = {p: float(share.loc[a:b].mean()) for p, (a, b) in PERIODS.items()}
    for p, v in m.items():
        reg.add(f"sl_road_north_{p.replace('–', '_')}", v, "share", f"North-of-road share of first-time mining (La Pampa longitudes), {p}",
                "description", "road_band_year_v2.csv")
    reg.add("sl_road_north_2008", share.loc[2008], "share", "North-of-road share of first-time mining, 2008", "description", "road_band_year_v2.csv")
    assert np.isclose(m["2016–18"], reg.get("t1_road_north_share_2016_18")) and np.isclose(m["2019–21"], reg.get("t1_road_north_share_2019_21"))
    fig, ax = _fig()
    _band(ax, 2019, 2021)
    ax.axhline(0.5, color=AXIS, lw=1, ls=(0, (3, 2)))
    ax.text(2005.6, 0.5, "half", fontsize=FS["small"], color=INK2, va="bottom", ha="left")
    ax.plot(yrs, share, "-", color=C["corridor"], lw=3, zorder=3)
    ax.plot(yrs, share, "o", color=C["corridor"], ms=8, mec="white", mew=1.5, zorder=4)
    for p, (a, b) in PERIODS.items():                       # period means: thick bands, labelled "period: share"
        v = m[p]
        ax.plot([a - 0.45, b + 0.45], [v, v], color=C["corridor"], lw=11, alpha=0.35, solid_capstyle="butt", zorder=2)
        below = p == "2016–18"
        ax.annotate(f"{p}: {v:.0%}", xy=((a + b) / 2, v), xytext=(0, -14 if below else 14), textcoords="offset points",
                    ha="center", va="top" if below else "bottom", fontsize=FS["body"], color=INK, fontweight="bold", zorder=6,
                    bbox=dict(boxstyle="round,pad=0.25", fc="#fbfaf7", ec=C["corridor_rest"], lw=1))
    ax.annotate(f"{share.loc[2008]:.0%} in 2008:\nthe Guacamayo boom,\nnorth of the road", xy=(2008, share.loc[2008]), xytext=(2011.3, 0.80),
                textcoords="data", fontsize=FS["small"], color=INK2, va="top", ha="left",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))
    ax.set_xlim(2005.4, 2025.6); ax.set_ylim(0, 1.05)
    _fmt_y(ax, pct=True); _ticks(ax, yrs); _events(ax)
    _label(ax, 2025, share.loc[2025], "North of\nthe highway\n(legal corridor\nside)", dx=12, fs=FS["small"])
    _head(fig, f"New mining near La Pampa moved north of the highway: {m['2016–18']:.0%} → {m['2019–21']:.0%} of first-time mining",
          "Share of land mined for the first time that lies north of the Interoceanic Highway, within La Pampa's longitudes (±30 km).\n"
          "The road had been crossed before: most new mining was north of it in 2008–10.")
    _save(fig, "slide_03_road_share.png", f"{SRC_ZONES} North = legal corridor side; south = Tambopata buffer zone. {NO_SEE}",
          top=0.74, right=0.86)


# --------------------------------------------------------------------------- 3b: road bands, north vs south (mirror)
def s03b_road_bands(reg):
    import raster_zones as rz
    b = pd.read_csv(rz.OUT_BAND)
    w = b.pivot_table(index="year", columns="km_from_road", values="new_land_ha", aggfunc="sum").fillna(0)
    KM = 15
    fig, axes = _fig(1, 3, sharey=True, gridspec_kw={"wspace": 0.12})
    means = {p: w.loc[a:c].mean() for p, (a, c) in PERIODS.items()}
    xmax = max(float(mm.loc[-KM:KM - 1].max()) for mm in means.values()) * 1.15
    for ax, (p, mm) in zip(axes, means.items()):
        a, c = PERIODS[p]                                            # same definition as v2_tests: mean of yearly shares (all bands)
        share = float((w[[k for k in w if k >= 0]].sum(axis=1) / w.sum(axis=1)).loc[a:c].mean())
        key = p.replace("–", "_")
        reg.add(f"sl_band_north_{key}", share, "share", f"North-of-road share of first-time mining (La Pampa longitudes, ±30 km), {p}",
                "description", "road_band_year_v2.csv")
        if f"t1_road_north_share_{key}" in reg.rows:
            assert np.isclose(share, reg.get(f"t1_road_north_share_{key}"))
        sel = mm.loc[-KM:KM - 1]
        y = sel.index.values + 0.5                                   # band k = [k, k+1) km, north positive
        ax.barh(y, sel.values, height=0.85, color=[C["corridor"] if k >= 0 else C["lapampa"] for k in sel.index], zorder=2)
        ax.axhline(0, color=INK, lw=4, zorder=3)
        ax.set_xlim(0, xmax); ax.set_ylim(-KM, KM)
        style_axes(ax, fmt=False); ax.yaxis.grid(False); ax.xaxis.grid(True, color=GRID, lw=0.6)
        ax.tick_params(axis="x", labelsize=FS["small"])
        ax.set_title(p, loc="left", fontsize=FS["title"] - 4, color=INK, pad=8, fontweight="medium")
        ax.text(0.97, 0.95, f"{share:.0%} north", transform=ax.transAxes, ha="right", va="top", fontsize=FS["label"] + 2,
                color=C["corridor"], fontweight="bold", bbox=dict(boxstyle="round,pad=0.2", fc="#fbfaf7", ec="none", alpha=0.9))
        ax.text(0.97, 0.05, f"{1 - share:.0%} south", transform=ax.transAxes, ha="right", va="bottom", fontsize=FS["label"],
                color=C["lapampa"], fontweight="bold", bbox=dict(boxstyle="round,pad=0.2", fc="#fbfaf7", ec="none", alpha=0.9))
        ax.set_xlabel("ha/yr per 1-km band", fontsize=FS["small"], color=INK2)
    a0 = axes[0]
    a0.set_yticks([-15, -7.5, 0, 7.5, 15])
    a0.set_yticklabels(["15 km", "South:\nbuffer zone", "road", "North:\nlegal corridor", "15 km"], fontsize=FS["small"])
    for t, col in zip(a0.get_yticklabels(), [INK2, C["lapampa"], INK, C["corridor"], INK2]):
        t.set_color(col); t.set_fontweight("semibold" if col != INK2 else "normal")
    a0.text(xmax * 0.97, 0.6, "Interoceanic Highway", ha="right", va="bottom", fontsize=FS["small"], color=INK, fontweight="semibold",
            bbox=dict(boxstyle="round,pad=0.15", fc="#fbfaf7", ec="none", alpha=0.9))
    m1, m2 = reg.get("sl_band_north_2016_18"), reg.get("sl_band_north_2019_21")
    _head(fig, "In 2019–21 new mining near La Pampa piled up just north of the road",
          f"Land mined for the first time per year, by 1-km band from the Interoceanic Highway within La Pampa's longitudes. "
          f"North share {m1:.0%} → {m2:.0%}.")
    _save(fig, "slide_03b_road_bands.png", f"{SRC_ZONES} Bands shown to ±15 km; shares use all bands to ±30 km. {NO_SEE}",
          top=0.84, left=0.12, right=0.98, xlab=True)


# --------------------------------------------------------------------------- 4: context: money, gold, La Pampa
def s04_context(pack, reg):
    money = v2_tests.mef_series().loc[2015:2025] / 1e6
    gold = pack["prices"].set_index("year")["gold"].loc[2012:2025]
    z = pd.read_csv(INTER / "zone_year_v2.csv")
    lp = z[z.code == 7].set_index("year")["new_land_ha"].loc[2012:2025]
    ratio = gold.loc[2025] / gold.loc[2018]
    reg.add("sl_gold_ratio_2025_2018", ratio, "ratio", "Gold price 2025 / 2018 (annual mean, nominal)", "description", "prices_annual.csv")
    reg.add("sl_gold_2018", gold.loc[2018], "USD/oz", "Gold price 2018", "description", "prices_annual.csv")
    reg.add("sl_gold_2025", gold.loc[2025], "USD/oz", "Gold price 2025", "description", "prices_annual.csv")
    peak = int(money.idxmax())
    for y in (2018, peak, 2021, 2025):
        if f"sl_pp0128_{y}_msoles" not in reg.rows:
            reg.add(f"sl_pp0128_{y}_msoles", money.loc[y], "million soles", f"PP 0128 spending booked in Madre de Dios, {y}", "description", "MEF Consulta Amigable")
    fig, axes = _fig(1, 3, gridspec_kw={"wspace": 0.32})
    a1, a2, a3 = axes
    for ax in axes:
        _band(ax, 2019, 2021)
    a1.bar(money.index, money.values, color=C["buffer"], width=0.7, zorder=2)
    _label(a1, peak - 0.45, money.loc[peak], f"{money.loc[peak]:.0f} M\nin {peak}", dx=-8, dy=-2, fs=FS["small"], ha="right", va="top")
    _label(a1, 2025, money.loc[2025], f"{money.loc[2025]:.0f} M", dx=0, dy=6, fs=FS["small"], ha="center", va="bottom")
    a2.plot(gold.index, gold.values, "-", color=C["gold"], lw=3)
    a2.plot(gold.index, gold.values, "o", color=C["gold"], ms=6, mec="white", mew=1.2)
    _label(a2, 2025, gold.loc[2025], f"${gold.loc[2025]:,.0f}", dx=0, dy=10, fs=FS["small"], ha="right", va="bottom")
    _label(a2, 2018, gold.loc[2018], f"${gold.loc[2018]:,.0f}", dx=0, dy=-12, fs=FS["small"], ha="center", va="top")
    a3.bar(lp.index, lp.values, color=C["lapampa"], width=0.7, zorder=2)
    titles = ("Enforcement money,\nMadre de Dios (M soles)", "Gold price\n(US$ per ounce)", "La Pampa: land mined for\nthe first time (ha)")
    for ax, t in zip(axes, titles):
        _fmt_y(ax); ax.set_xlim(2011.4, 2025.6)
        ax.set_xticks([2012, 2015, 2018, 2021, 2024]); ax.set_xticklabels(["2012", "'15", "'18", "'21", "'24"], fontsize=FS["tick"])
        ax.set_title(t, loc="left", fontsize=FS["label"] + 1, color=INK, pad=12, fontweight="medium")
    a1.set_ylim(0, money.max() * 1.25); a2.set_ylim(0, gold.max() * 1.2); a3.set_ylim(0, lp.max() * 1.2)
    for ax in axes:
        _events(ax, label=False)
    a3.text(2018.4, lp.max() * 1.17, "Mercurio", ha="right", va="top", fontsize=FS["small"], color=INK, fontweight="semibold")
    _head(fig, f"Enforcement money peaked in {peak} and faded, while gold rose {ratio:.1f}-fold (2018–25)",
          "Same years in each panel. Solid line: Mercurio (Feb 2019); shaded: 2019–21; dashed: COVID, Restauración, emergency, navy out. Spending is a lower bound.")
    _save(fig, "slide_04_context.png", "MEF Consulta Amigable, PP 0128 executed spending (devengado), Madre de Dios; World Bank Pink Sheet "
          f"(nominal); {SRC_ZONES} Correlation is not shown: 11 years, and money follows mining.", top=0.70, left=0.06, right=0.98)


# --------------------------------------------------------------------------- 5: old pits
def s05_old_pits(reg):
    z = pd.read_csv(INTER / "zone_year_v2.csv")
    lp = z[z.code == 7].set_index("year").loc[2014:2025, ["new_land_ha", "remined_ha"]]
    sh23 = lp.loc[2023, "remined_ha"] / lp.loc[2023].sum()
    reg.add("sl_lp_oldpit_share_2023", sh23, "share", "Share of La Pampa sector's 2023 new mining (first-time + returns) on old pits", "description", "zone_year_v2.csv")
    reg.add("sl_lp_oldpit_ha_2023", lp.loc[2023, "remined_ha"], "ha", "La Pampa sector, returns to old pits, 2023", "description", "zone_year_v2.csv")
    reg.add("sl_lp_newland_ha_2023", lp.loc[2023, "new_land_ha"], "ha", "La Pampa sector, first-time mining, 2023", "description", "zone_year_v2.csv")
    reg.add("sl_lp_oldpit_ha_2016_18", lp.loc[2016:2018, "remined_ha"].mean(), "ha/yr", "La Pampa sector, returns to old pits, mean 2016-18 (flicker floor)", "description", "zone_year_v2.csv")
    yrs = list(lp.index)
    fig, ax = _fig()
    _band(ax, 2019, 2021)
    ax.bar(yrs, lp["new_land_ha"], color=C["lapampa"], width=0.72, zorder=2)
    ax.bar(yrs, lp["remined_ha"], bottom=lp["new_land_ha"], color=C["lapampa_tint"], width=0.72, zorder=2)
    ax.bar(yrs, [0] * len(yrs), bottom=lp["new_land_ha"], color="white", edgecolor="white", lw=1.5, width=0.72, zorder=3)
    _label(ax, 2025.4, lp.loc[2025, "new_land_ha"] / 2, "New land\n(first time)", dx=8, fs=FS["small"])
    _label(ax, 2025.4, lp.loc[2025, "new_land_ha"] + lp.loc[2025, "remined_ha"] / 2, "Old pits\nmined again", dx=8, fs=FS["small"])
    tot23 = lp.loc[2023].sum()
    ax.annotate(f"2023: {lp.loc[2023, 'remined_ha']:,.0f} of {tot23:,.0f} ha\non old pits ({sh23:.0%})", xy=(2023, tot23 * 0.8),
                xytext=(-40, -6), textcoords="offset points", ha="right", va="top", fontsize=FS["body"], color=INK,
                fontweight="semibold", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))
    ax.set_xlim(2013.4, 2025.6); ax.set_ylim(0, tot23 * 1.12)
    _fmt_y(ax); _ticks(ax, yrs); _events(ax)
    _head(fig, f"In 2023, {sh23:.0%} of new mining in La Pampa was on old pits",
          "La Pampa sector, ha per year: land mined for the first time vs land mined before (not last year) and mined again.\n"
          "Forest-loss alerts and net additions miss most of this.")
    _save(fig, "slide_05_old_pits.png", f"{SRC_ZONES} Old-pit counts include some year-to-year map flicker ({lp.loc[2016:2018, 'remined_ha'].mean():,.0f} ha/yr already in "
          f"2016–18): trust the 2023 jump, not small changes. MAAP #193 (2023) reports miners back on degraded land. {NO_SEE}",
          top=0.78, right=0.86)


# --------------------------------------------------------------------------- 6: inside the reserve
def s06_reserve(reg):
    lv = pd.read_csv(OUT / "peru_anp_mining_levels_2010_2025.csv").set_index("year")["Tambopata NR"]
    ad = lv.diff().loc[2011:2025]
    reg.add("sl_reserve_add_2025", ad.loc[2025], "ha", "Net addition to mining inside Tambopata National Reserve, 2025", "description", "MapBiomas Peru Col 4 ANP")
    reg.add("sl_reserve_level_2025", lv.loc[2025], "ha", "Mining area inside Tambopata National Reserve, 2025", "description", "MapBiomas Peru Col 4 ANP")
    reg.add("sl_reserve_add_2017", ad.loc[2017], "ha", "Net addition inside Tambopata National Reserve, 2017 (partly reclassification)", "description", "MapBiomas Peru Col 4 ANP")
    assert np.isclose(ad.loc[2025], reg.get("anp_tam_nr_addition_2025"), atol=0.2)
    yrs = list(ad.index)
    fig, ax = _fig()
    ax.axhline(0, color=AXIS, lw=1)
    cols = [C["reserve"] if y == 2025 else "#b9cdb2" for y in yrs]
    ax.bar(yrs, ad.values, color=cols, width=0.72, zorder=2)
    _label(ax, 2025, ad.loc[2025], f"+{ad.loc[2025]:,.0f} ha\nin 2025", dx=0, dy=8, ha="center", va="bottom")
    _label(ax, 2016.6, ad.loc[2017], f"+{ad.loc[2017]:,.0f} ha in 2017:\npartly a map\nreclassification", dx=-8, dy=-4, va="top", ha="right",
           fs=FS["small"], weight="normal")
    ax.set_xlim(2010.4, 2025.6); ax.set_ylim(min(-60, ad.min() * 1.3), ad.max() * 1.2)
    _fmt_y(ax); _ticks(ax, yrs); _events(ax)
    _head(fig, f"In 2025, mining inside Tambopata National Reserve jumped by {ad.loc[2025]:,.0f} ha",
          f"Net annual addition to mapped mining area inside the reserve itself (not the buffer zone), ha. "
          f"Total inside in 2025: {lv.loc[2025]:,.0f} ha.\nThe 2025 jump follows the navy's withdrawal from the Malinowski River posts (MAAP #241, 2026).")
    _save(fig, "slide_06_reserve.png", "MapBiomas Peru Collection 4, protected-area statistics (class 4.2 Minería; platform check 777 ha, "
          f"2025). MAAP #241 (Pacsi et al., 2026) reports ~500 ha inside the reserve, late 2025 to Feb 2026. {NO_SEE}",
          top=0.74, right=0.95)


# --------------------------------------------------------------------------- 7: causal tests
def _short(u):
    n = u.split("|")[0]
    for pre in ("del ", "de "):
        n = n.removeprefix(pre)
    return n[0].upper() + n[1:]

def s07_causal(pack, reg):
    ad = peru_models._zone_adds(pack)
    gold = pack["prices"].set_index("year")["gold"]
    TU = peru_models.TU
    pre = ad.loc[2014:2018].mean()
    poolB = sorted(u for u in ad.columns if ad.loc[2014:2018, u].abs().sum() > 0)
    pool_big = sorted(u for u in poolB if pre[u] > 10)
    REAL = {"during": (2019, 2021), "after": (2022, 2025)}
    res = {}
    for m, units in (("M1", poolB), ("M4", pool_big)):
        g = {u: peru_models.fit(ad, [v for v in units if v != TU], u, m, 2014, 2025, REAL, gold)["post_during"] for u in units if u != TU}
        g[TU] = peru_models.fit(ad, units, TU, m, 2014, 2025, REAL, gold)["post_during"]
        res[m] = pd.Series(g).sort_values()
    r1 = placebo_rank(res["M1"][TU], res["M1"].drop(TU)); r4 = placebo_rank(res["M4"][TU], res["M4"].drop(TU))
    n1, n4 = len(res["M1"]), len(res["M4"])
    assert r1 == reg.get("model_m1_rank") if "model_m1_rank" in reg.rows else True
    assert r4 == reg.get("model_m4_rank") and n4 == reg.get("model_m4_n")
    reg.add("sl_causal_rank_ha", r1, "rank", f"Tambopata rank among {n1} zones, 2019-21 gap in ha (M1, 1 = biggest fall)", "description", "peru_bufferzone_year.csv")
    reg.add("sl_causal_n_ha", n1, "count", "Zones in the hectare placebo pool", "description", "peru_bufferzone_year.csv")
    reg.add("sl_causal_rank_scaled", r4, "rank", f"Tambopata rank among {n4} zones, 2019-21 gap scaled to own size (M4)", "description", "peru_bufferzone_year.csv")
    reg.add("sl_causal_n_scaled", n4, "count", "Zones in the scaled placebo pool", "description", "peru_bufferzone_year.csv")
    reg.add("sl_causal_p_ha", r1 / n1, "p-value", "Placebo-in-space p, hectares (rank / n)", "description", "peru_bufferzone_year.csv")
    reg.add("sl_causal_p_scaled", r4 / n4, "p-value", "Placebo-in-space p, scaled (rank / n)", "description", "peru_bufferzone_year.csv")
    est = {"Synthetic\ncontrol": reg.get("sdid_sc_ha_during"), "M1 zone +\nyear effects": reg.get("model_m1_during"),
           "M2 + gold\nprice × size": reg.get("model_m2_during"), "M3 + own\ntrends": reg.get("model_m3_during")}
    reg.add("sl_causal_range_lo", max(est.values()), "ha/yr", "Smallest estimated 2019-21 fall (synthetic control), net additions", "causal",
            "peru_bufferzone_year.csv (conditional on comparison zones being a fair counterfactual)")
    reg.add("sl_causal_range_hi", min(est.values()), "ha/yr", "Largest estimated 2019-21 fall (M3), net additions", "causal",
            "peru_bufferzone_year.csv (conditional on comparison zones being a fair counterfactual)")

    # Two rows, one question each: is the real fall bigger than the fake ones? Grey = every other zone given a fake
    # operation; orange = Tambopata's real 2019-21 gap. Hectares on top (it stands out), scaled to size below (it doesn't).
    from matplotlib.ticker import FuncFormatter
    fig, axes = _fig(2, 1, gridspec_kw={"hspace": 1.1})
    rows = [(res["M1"], "In hectares", f"{_ordinal(r1)} of {n1}", "ha/yr vs the other zones",
             lambda x, p: f"{x:,.0f}".replace("-", "−")),
            (res["M4"], "Relative to its own size", f"{_ordinal(r4)} of {n4}", "multiples of each zone's normal year",
             lambda x, p: f"{x:.1f}".replace("-", "−"))]
    rng = np.random.default_rng(3)
    for ax, (ser, lab, rank_txt, unit, fmt) in zip(axes, rows):
        others = ser.drop(TU)
        jit = rng.uniform(-0.18, 0.18, len(others))
        ax.axvline(0, color=AXIS, lw=1.2, zorder=1)
        ax.scatter(others.values, jit, s=230, color="#bdb9b0", edgecolor="white", lw=1.5, zorder=2)
        ax.scatter([ser[TU]], [0], s=520, color=C["lapampa"], edgecolor="white", lw=2, zorder=3)
        ax.annotate(f"Tambopata {fmt(ser[TU], None)}", xy=(ser[TU], 0), xytext=(0, -24), textcoords="offset points",
                    ha="center", va="top", fontsize=FS["label"], color=C["lapampa"], fontweight="bold")
        ax.annotate(f"{len(others)} other zones,\neach given a fake operation", xy=(others.median(), 0), xytext=(0, 26),
                    textcoords="offset points", ha="center", va="bottom", fontsize=FS["small"], color=INK2)
        ax.set_ylim(-0.9, 0.7); ax.set_yticks([])
        for sp in ("left", "right", "top"):
            ax.spines[sp].set_visible(False)
        ax.spines["bottom"].set_color(AXIS)
        ax.xaxis.set_major_formatter(FuncFormatter(fmt)); ax.tick_params(axis="x", labelsize=FS["tick"], colors=INK2)
        ax.set_xlabel(unit, fontsize=FS["small"], color=INK2)
        lo_x = min(ser.min(), 0); hi_x = max(ser.max(), 0); pad = (hi_x - lo_x) * 0.12
        ax.set_xlim(lo_x - pad, hi_x + pad)
        ax.text(-0.01, 1.32, lab, transform=ax.transAxes, fontsize=FS["label"] + 2, color=INK, fontweight="bold", ha="left")
        ax.text(1.0, 1.32, f"Tambopata: {rank_txt}", transform=ax.transAxes, fontsize=FS["label"] + 2, ha="right",
                color=C["lapampa"] if ax is axes[0] else INK2, fontweight="bold")
    _head(fig, f"In hectares, Tambopata's 2019–21 fall is the largest of {n1} Peruvian buffer zones",
          "Each dot: one buffer zone's 2019–21 change after zone and year effects. Left = bigger fall.")
    _save(fig, "slide_07_causal.png", "MapBiomas Peru Collection 4, peru_bufferzone_year.csv; 15 Peruvian buffer zones with mining before 2019 "
          "(scaled: 7 with > 10 ha/yr). Tambopata removed from each fake zone's comparison pool. Placebo p = rank / n.",
          top=0.86, left=0.04, right=0.98, xlab=True)

    # ---- 7b: range of estimates
    est7 = {"Synthetic control": reg.get("sdid_sc_ha_during"), "Difference-in-differences (M1)": reg.get("model_m1_during"),
            "Synthetic DiD": reg.get("sdid_sdid_ha_during"), "+ gold price × size (M2)": reg.get("model_m2_during"),
            "+ each zone's own trend (M3)": reg.get("model_m3_during")}
    est7 = dict(sorted(est7.items(), key=lambda kv: -kv[1]))
    lo, hi = reg.get("sl_causal_range_lo"), reg.get("sl_causal_range_hi")
    assert np.isclose(lo, max(est7.values())) and np.isclose(hi, min(est7.values()))
    fig, ax = _fig()
    yy = np.arange(len(est7))[::-1]
    ax.axvspan(hi, lo, color=C["lapampa_tint"], alpha=0.35, lw=0, zorder=0)
    ax.text((hi + lo) / 2, len(est7) - 0.35, "our conditional range", ha="center", va="bottom", fontsize=FS["label"], color=INK, fontweight="bold")
    ax.axvline(0, color=INK2, lw=1.5)
    ax.annotate("no effect", xy=(0, len(est7) - 0.35), xytext=(-6, 0), textcoords="offset points", ha="right", va="bottom",
                fontsize=FS["small"], color=INK2)
    for yv, (k, v) in zip(yy, est7.items()):
        ax.plot([v, 0], [yv, yv], color="#d3d1cb", lw=2, zorder=1)
        ax.plot(v, yv, "o", ms=16, color=C["lapampa"], mec="white", mew=2, zorder=3)
        ax.annotate(f"{v:,.0f}".replace("-", "−"), xy=(v, yv), xytext=(0, 14), textcoords="offset points", ha="center", va="bottom",
                    fontsize=FS["body"], color=INK, fontweight="semibold")
    ax.set_yticks(yy); ax.set_yticklabels(list(est7), fontsize=FS["label"])
    style_axes(ax, fmt=False); ax.yaxis.grid(False); ax.xaxis.grid(True, color=GRID, lw=0.6)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: f"{x:,.0f}".replace("-", "−")))
    ax.set_xlim(hi * 1.15, 250); ax.set_ylim(-0.6, len(est7) + 0.2)
    ax.set_xlabel("Change in net new mining, Tambopata buffer zone, 2019–21, ha/yr", fontsize=FS["small"], color=INK2)
    _head(fig, f"The estimates range from about {_round_to(abs(lo), 100):,} to {_round_to(abs(hi), 100):,} ha a year less net new mining",
          "Causal only if the other Peruvian buffer zones show what Tambopata would otherwise have done. In hectares only; coincides with COVID.")
    _save(fig, "slide_07b_estimates.png", "MapBiomas Peru Collection 4, peru_bufferzone_year.csv; zone + year effects (M1–M3), synthetic "
          "control and synthetic DiD on the same 15-zone panel (peru_models.py, peru_sdid.py).", top=0.86, left=0.27, right=0.97, xlab=True)


def _ordinal(n):
    n = int(n)
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"

def _round_to(x, k):
    return int(round(x / k) * k)


# --------------------------------------------------------------------------- 8: Brazilian twins (backup)
def s08_twins(reg):
    import control_top3 as ct
    m = pd.read_csv(INTER / "mb_amazonia_col6_mining.csv")
    w = pd.read_csv(INTER / "amw_candidates_year.csv").pivot(index="unit_id", columns="year", values="new_ha")
    zb = pd.read_csv(ROOT / "data" / "peru_bufferzone_year.csv")
    tam = zb[(zb.buffer_zone == "Tambopata") & (zb.pa_category == "Reserva Nacional")].groupby("year").mining_ha.sum()
    idx = {"Tambopata buffer zone": 100 * tam / tam.loc[2018]}
    pace = {"Tambopata buffer zone": 100 * w.loc[ct.TU, [2019, 2020, 2021]].mean() / w.loc[ct.TU, 2018]}
    for uid, (nm, gc) in ct.TWINS.items():
        s = m[m.geocode == gc].groupby("year").mining_ha.sum()
        idx[nm] = 100 * s / s.loc[2018]
        pace[nm] = 100 * w.loc[uid, [2019, 2020, 2021]].mean() / w.loc[uid, 2018]
    I = pd.DataFrame(idx).loc[2010:2018]
    t = pd.read_csv(OUT / "control_top3_tests.csv").set_index("twin")
    for nm, v in pace.items():
        reg.add(f"sl_twin_pace_{nm.split()[0].lower()}", v, "% of 2018 stock", f"New mining 2019-21 per year as % of 2018 stock (AMW), {nm}",
                "description", "amw_candidates_year.csv")
    for nm in t.index:
        reg.add(f"sl_twin_index2010_{nm.split()[0].lower()}", I.loc[2010, nm], "index 2018=100", f"Mining area index 2010 (2018 = 100), {nm}", "description", "mb_amazonia_col6_mining.csv")
    reg.add("sl_twin_index2010_tambopata", I.loc[2010, "Tambopata buffer zone"], "index 2018=100", "Mining area index 2010 (2018 = 100), Tambopata BZ", "description", "peru_bufferzone_year.csv")
    ptr = t["pre_trend_p"].max()
    reg.add("sl_twin_pretrend_p_max", ptr, "p-value", "Largest pre-trend test p across the two twins (all reject parallel trends)", "description", "control_top3_tests.csv")
    cols = {"Tambopata buffer zone": C["lapampa"], **{v[0]: ct.TCOL[v[0]] for v in ct.TWINS.values()}}
    names = {"Tambopata buffer zone": "Tambopata\nbuffer zone", "Amana National Forest": "Amanã National\nForest (Brazil)",
             "Tapajos protection area": "Tapajós protection\narea (Brazil)"}
    fig, (a1, a2) = _fig(1, 2, gridspec_kw={"width_ratios": [1.5, 1], "wspace": 0.45})
    yrs = list(I.index)
    a1.axhline(100, color=AXIS, lw=1)
    short = {"Tambopata buffer zone": "Tambopata", "Amana National Forest": "Amanã (Brazil)", "Tapajos protection area": "Tapajós (Brazil)"}
    for nm in I:
        a1.plot(yrs, I[nm], "-o", color=cols[nm], lw=3, ms=7, mec="white", mew=1.2)
        _label(a1, 2010, I.loc[2010, nm], f"{short[nm]}  {I.loc[2010, nm]:.0f}", dx=-12, ha="right", fs=FS["small"])
    a1.set_xlim(2009.6, 2018.4); a1.tick_params(axis="y", labelleft=False)
    _label(a1, 2018, 100, "2018 = 100", dx=-6, dy=12, ha="right", fs=FS["small"], weight="normal"); a1.set_ylim(0, 112)
    _fmt_y(a1); _ticks(a1, yrs)
    a1.set_title("Before: mining area, index 2018 = 100", loc="left", fontsize=FS["label"], color=INK, pad=10)
    order = list(pace)
    a2.barh(range(len(order))[::-1], [pace[k] for k in order], color=[cols[k] for k in order], height=0.6)
    for i, k in zip(range(len(order))[::-1], order):
        _label(a2, pace[k], i, f"{pace[k]:.0f}%", dx=6, fs=FS["body"])
    a2.set_yticks(range(len(order))[::-1]); a2.set_yticklabels([short[k] for k in order], fontsize=FS["small"])
    style_axes(a2, ygrid=False, fmt=False); a2.yaxis.grid(False); a2.set_xticks([]); a2.spines["bottom"].set_visible(False)
    a2.set_title("2019–21: new mining per year,\n% of own 2018 area", loc="left", fontsize=FS["label"], color=INK, pad=10)
    a2.set_xlim(0, max(pace.values()) * 1.3)
    _head(fig, "Tambopata grew faster than its Brazilian twins before 2019, so they can't show the counterfactual",
          f"Left: parallel pre-trends are rejected for both twins (p {'< 0.001' if ptr < 0.001 else '≤ ' + format(ptr, '.3f')}). Right: in 2019–21 Tambopata grew more slowly than both.\n"
          "A second check only, never the main comparison. Brazil 2019–22 also had weak federal enforcement.")
    _save(fig, "slide_08_brazil_twins.png", "MapBiomas Peru Col 4 (Tambopata) and MapBiomas Amazonía Col 6 (twins) before 2019; Amazon Mining "
          "Watch (480 m) for 2019–21. Different collections: compared as indices, never subtracted. Twins chosen by fixed rules (control_select.py).",
          top=0.74, left=0.2, right=0.97)


def run(pack, reg):
    print("\n== Slide figures ==")
    if not (INTER / "zone_year_v2.csv").exists():
        warnings.warn("slides_figures: zone_year_v2.csv missing; skipping"); return
    s01_net(pack, reg)
    s02_zones(reg)
    s03_road(reg)
    s03b_road_bands(reg)
    s04_context(pack, reg)
    s05_old_pits(reg)
    s06_reserve(reg)
    s07_causal(pack, reg)
    s08_twins(reg)
    import json
    (SL / "slide_titles.json").write_text(json.dumps(TITLES, ensure_ascii=False, indent=2))
    print("Saved output/slides/slide_titles.json")
