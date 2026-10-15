"""Slide figures for the FZS talk, storyline v3.1 (docs/presentation/STORYLINE.md): output/slides/*.png + slide_titles.json.

Plan v3 (docs/PLAN_v3.md): ONE measure on every chart, net mining additions (ha/yr) = new land + re-mined − stopped,
from the MapBiomas Peru Collection 4 rasters on one zone registry, read ONLY through zonedata.py. Parts use the fixed
colours of common.C (new brown, re-mined amber, stopped teal below zero) and net is drawn in INK.

Lean by rule (STORYLINE v3.1): one message per chart, years 2014–2025 unless the slide needs otherwise (2016–2022 for
the 2019 zoom), on-chart event labels only for Mercurio and the April 2023 emergency, one callout per chart, fonts sized
for a projector (figure 12.2 x 5.0 in = the deck's plate, so 1 pt here is 1 pt on the slide). The Tambopata buffer zone
is the zone of every time series; La Pampa appears only on "across the road".

The takeaway title and the measure/unit/zone/period subtitle go to slide_titles.json (the deck draws them). Every
number written on a slide is registered as `sl_*` with measure/zone/period, and asserted equal to the canonical number
where one exists. All DESCRIPTION except s18_placebo and b_estimates (the tests behind the one CONDITIONAL claim).
"""
from __future__ import annotations
import json
import textwrap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

from common import OUT, C, INK, INK2, MUTED, AXIS, GRID, SURFACE, style_axes, PERU_EVENTS, SRC_PRICE, placebo_rank
import definitions as D
import zonedata as Z

SL = OUT / "slides"
W, H, DPI = 12.2, 5.0, 200          # = the deck's figure plate (12.23 x 5.05 in)
TITLES: dict = {}                   # slide name -> title / subtitle / source (the PPT slide carries the title)
FS = dict(body=17, tick=16, label=17, small=15, source=11.5)
RC = {"font.size": FS["body"], "xtick.labelsize": FS["tick"], "ytick.labelsize": FS["tick"],
      "axes.titlesize": FS["label"], "axes.labelsize": FS["label"], "xtick.major.size": 4}
PRE, DUR, LATER = "pre", "during", "later"
PSHORT = {p: D.period_label(p) for p in (PRE, DUR, LATER)}
TB = D.TREATED_ZONE
Y0, Y1 = D.YEARS                    # 2014–2025
BAND = "#ebe6dc"
SRC = "MapBiomas Peru Collection 4 (30 m, class 4.2 mining, legal and illegal), our pixel accounting."
NO_SEE = "Satellites cannot see river dredges or mercury."
PART_LAB = {"new": "New land", "remined": "Re-mined", "stopped": "Stopped (below zero)", "net": "Net additions"}
EV_LABEL = {"Mercurio": "Mercurio, Feb 2019", "Emergency": "Emergency, Apr 2023"}   # the only events labelled on charts


# --------------------------------------------------------------------------- data helpers (zonedata only)
def _w(col: str) -> pd.DataFrame:
    return Z.wide(Z.region_units(), D.COLS[col] if col in D.COLS else col)

def _pm(unit: str, m: str, p) -> float:
    return Z.period_mean(_w(m)[unit], p)

def _later_ex(unit: str, m: str) -> float:
    a, b = D.PERIODS[LATER]
    return float(_w(m)[unit].loc[a:b].drop(D.LATER_EX).mean())

def _add(reg, id, v, unit, desc, measure, zone, period, claim="description", src=D.SOURCE, check=None, tol=0.5):
    """Register a slide number (sl_*) with measure/zone/period; assert it equals the canonical id if given."""
    if check is not None and check in reg.rows:
        assert abs(float(v) - reg.get(check)) <= tol, f"{id} = {v} differs from {check} = {reg.get(check)}"
    reg.add(id, v, unit, desc, claim, src, measure=measure, zone=zone, period=period)
    return float(v)

def _fmt(v, d=0):
    return f"{v:,.{d}f}".replace("-", "−")

def _ordinal(n):
    n = int(n)
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"

def _fold(r):
    words = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}
    k = int(np.floor(r))
    return ("more than " if r - k >= 0.2 else "") + f"{words.get(k, str(k))}-fold"


# --------------------------------------------------------------------------- drawing helpers
def _fig(nrows=1, ncols=1, **kw):
    with plt.rc_context(RC):
        fig, axes = plt.subplots(nrows, ncols, figsize=(W, H), **kw)
    return fig, axes

def _head(fig, title, sub):
    """Takeaway title (<= 10 words) + subtitle (measure, unit, zone, period) go to slide_titles.json."""
    assert len(title.split()) <= 10, f"slide title over 10 words: {title}"
    fig._slide_title = (title, sub)

def _ticks(ax, years, step=1):
    years = list(years)
    ax.set_xticks(years[::step])
    ax.set_xticklabels([str(y) if i == 0 or y % 5 == 0 or y == years[-1] else f"'{str(y)[2:]}"
                        for i, y in enumerate(years)][::step])
    ax.tick_params(axis="x", labelsize=FS["tick"], length=0, pad=6)

def _events(ax, label=True):
    """Only Mercurio (solid) and the April 2023 emergency (dashed), drawn at Y − 0.5 (common.py convention)."""
    lo, hi = ax.get_xlim()
    for ev in PERU_EVENTS:
        x = ev["year"] - 0.5
        if ev["short"] not in EV_LABEL or not lo + 0.2 <= x <= hi - 0.2:
            continue
        solid = ev["style"] == "solid"
        ax.axvline(x, color=INK if solid else INK2, ls="-" if solid else (0, (4, 3)), lw=1.6 if solid else 1.3, zorder=0.5)
        if label:
            ax.annotate(EV_LABEL[ev["short"]], xy=(x, 1.0), xycoords=("data", "axes fraction"), xytext=(0, 6),
                        textcoords="offset points", ha="center", va="bottom", fontsize=FS["small"],
                        color=INK if solid else INK2, fontweight="bold" if solid else "normal", annotation_clip=False)
    ax.set_xlim(lo, hi)

def _band(ax, key=DUR):
    a, b = D.PERIODS[key]
    ax.axvspan(a - 0.5, b + 0.5, color=BAND, zorder=-1, lw=0)

def _label(ax, x, y, text, dx=10, dy=0, fs=None, weight="bold", ha="left", va="center", color=INK):
    ax.annotate(text, xy=(x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va,
                fontsize=fs or FS["body"], color=color, fontweight=weight, annotation_clip=False, linespacing=1.2)

def _callout(ax, xy, xytext, text, ha="left", va="center"):
    """The one callout per chart: boxed text with a thin leader to the mark."""
    ax.annotate(text, xy=xy, xytext=xytext, textcoords="data", ha=ha, va=va, fontsize=FS["small"], color=INK,
                linespacing=1.35, zorder=9, annotation_clip=False,
                bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=AXIS, lw=0.8),
                arrowprops=dict(arrowstyle="-", color=INK2, lw=1.0, shrinkA=0, shrinkB=6))

def _fmt_y(ax, pct=False):
    style_axes(ax)
    ax.yaxis.set_major_formatter(FuncFormatter((lambda v, p: f"{v:.0%}") if pct else (lambda v, p: _fmt(v))))
    ax.tick_params(axis="y", labelsize=FS["tick"])

def _parts_bars(ax, x, new, rem, stp, width=0.66):
    """Stacked parts: new + re-mined above zero, stopped below zero, a surface gap between segments."""
    ax.bar(x, new, width=width, color=C["new"], lw=0, zorder=2)
    ax.bar(x, rem, bottom=new, width=width, color=C["remined"], lw=0, zorder=2)
    ax.bar(x, -np.asarray(stp), width=width, color=C["stopped"], lw=0, zorder=2)
    ax.bar(x, np.zeros(len(np.atleast_1d(x))), bottom=new, width=width, color=SURFACE, edgecolor=SURFACE, lw=1.5, zorder=3)
    ax.axhline(0, color=INK2, lw=1.0, zorder=3)

def _net_line(ax, x, net, ms=8):
    ax.plot(x, net, "-", color=INK, lw=2.6, zorder=5)
    ax.plot(x, net, "o", color=INK, ms=ms, mec="white", mew=1.4, zorder=6)

def _parts_legend(ax, loc="upper left", ncol=4):
    h = [Patch(color=C["new"], label=PART_LAB["new"]), Patch(color=C["remined"], label=PART_LAB["remined"]),
         Patch(color=C["stopped"], label=PART_LAB["stopped"]),
         Line2D([], [], color=INK, marker="o", ms=8, mec="white", lw=2.4, label=PART_LAB["net"])]
    ax.legend(handles=h, loc=loc, ncol=ncol, fontsize=FS["small"], frameon=False, handlelength=1.2, columnspacing=1.4,
              borderaxespad=0.1)

def _save(fig, name, source, top=0.88, bottom=None, left=0.085, right=0.97, xlab=False, **adj):
    t, sub = getattr(fig, "_slide_title", ("", ""))
    w_in, h_in = fig.get_size_inches()
    TITLES[name.removesuffix(".png")] = dict(title=t, subtitle=sub.replace("\n", " "), source="Source: " + source,
                                             w_in=round(float(w_in), 2), h_in=round(float(h_in), 2))
    text = "\n".join(textwrap.wrap("Source: " + source, 140))
    n = text.count("\n") + 1
    fig.text(0.012, 0.015, text, fontsize=FS["source"], color=MUTED, va="bottom", ha="left", linespacing=1.3)
    bottom = bottom if bottom is not None else (0.6 + 0.22 * n + (0.35 if xlab else 0)) / H
    fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, **adj)
    SL.mkdir(parents=True, exist_ok=True)
    fig.savefig(SL / name, dpi=DPI)
    plt.close(fig)
    print(f"Saved output/slides/{name}")


# --------------------------------------------------------------------------- slide 9: net additions fell, came back
def s09_net(reg):
    s = _w("net")[TB].loc[Y0:Y1]
    yrs = list(s.index)
    m = {p: _add(reg, f"sl_net_{TB}_{p}", _pm(TB, "net", p), "ha/yr",
                 f"Net mining additions, {D.UNIT_NAME[TB]}, {PSHORT[p]}: mean per year (slide 9)", "net", TB, PSHORT[p],
                 check=f"{TB}_{p}_net") for p in (PRE, DUR, LATER)}
    ex = _add(reg, f"sl_net_{TB}_later_ex2023", _later_ex(TB, "net"), "ha/yr", f"Net mining additions, "
              f"{D.UNIT_NAME[TB]}, 2022, 2024, 2025 (without 2023): mean per year (slide 9)", "net", TB, "2022, 2024, 2025",
              check=f"{TB}_later_ex2023_net")
    fall = _add(reg, f"sl_net_{TB}_fall_share", 1 - m[DUR] / m[PRE], "share", "Fall in mean net mining additions, "
                f"{D.UNIT_NAME[TB]}, 2016–18 to 2019–21 (slide 9)", "net", TB, f"{PSHORT[PRE]} vs {PSHORT[DUR]}")
    fig, ax = _fig()
    _band(ax, DUR)
    ax.axhline(0, color=AXIS, lw=1)
    for p in (PRE, DUR, LATER):
        a, b = D.PERIODS[p]
        ax.plot([a - 0.42, b + 0.42], [m[p]] * 2, color=C["lapampa"], lw=10, alpha=0.30, solid_capstyle="butt", zorder=2)
    ax.plot(yrs, s, "-", color=C["lapampa"], lw=3.2, zorder=3)
    ax.plot(yrs, s, "o", color=C["lapampa"], ms=9, mec="white", mew=1.5, zorder=4)
    ax.set_xlim(Y0 - 0.6, Y1 + 0.6)
    ax.set_ylim(min(s.min(), 0) - 300, s.max() * 1.32)
    for p in (PRE, DUR, LATER):                 # the callout: the three period means, in one row at the top
        a, b = D.PERIODS[p]
        txt = f"{_fmt(m[p])} ha/yr" + (f"\n({_fmt(ex)} without 2023)" if p == LATER else "")
        ax.text((a + b) / 2, 0.97, txt, transform=ax.get_xaxis_transform(), ha="center", va="top",
                fontsize=FS["body"], color=INK, fontweight="bold", linespacing=1.15,
                bbox=dict(boxstyle="round,pad=0.25", fc=SURFACE, ec="none", alpha=0.9), zorder=8)
    _fmt_y(ax); _ticks(ax, yrs); _events(ax)
    ax.set_ylabel("ha/yr", fontsize=FS["small"], color=INK2)
    _head(fig, f"Net mining fell {fall:.0%}, then came back",
          f"Net mining additions, ha/yr · Tambopata buffer zone · {Y0}–{Y1} · thick bars and numbers: means for "
          f"{PSHORT[PRE]}, {PSHORT[DUR]} (shaded) and {PSHORT[LATER]}")
    _save(fig, "slide_09_net.png", f"{SRC} Official SERNANP buffer-zone polygon. {NO_SEE}", top=0.9, right=0.985)


# --------------------------------------------------------------------------- slide 10: 2019, year by year (parts)
def s10_2019(reg):
    y0, y1 = D.PERIODS[PRE][0], D.PERIODS[LATER][0]          # 2016–2022
    yrs = list(range(y0, y1 + 1))
    P = {mm: _w(mm)[TB].loc[y0:y1] for mm in ["net"] + D.PARTS}
    r, f = D.REF_YEAR, D.FIRST_POST
    v = {}
    for y, mm in ((r, "new"), (f, "new"), (f, "stopped"), (f, "net"), (r, "stopped")):
        v[(y, mm)] = _add(reg, f"sl_tbz_{y}_{mm}", P[mm].loc[y], "ha/yr", f"{D.MEASURE_NAME[mm]}, {D.UNIT_NAME[TB]}, {y} "
                          "(slide 10)", mm, TB, str(y), check=f"{TB}_{y}_{mm}")
    lo_, hi_ = (_add(reg, f"sl_stopped_share_of_fall_{k}", reg.get(f"{TB}_stopped_share_of_fall_{c}"), "share",
                     f"Share of the 2016–18 to 2019–21 fall in net additions, {D.UNIT_NAME[TB]}, that is more stopped "
                     f"land: {c} of the four ways of counting map flicker (slide 10)", "stopped", TB,
                     f"{PSHORT[PRE]} vs {PSHORT[DUR]}", check=f"{TB}_stopped_share_of_fall_{c}", tol=1e-9)
                for k, c in (("lo", "min"), ("hi", "max")))
    am = {p: _add(reg, f"sl_amarakaeri_stopped_{p}", _pm("amarakaeri_bz", "stopped", p), "ha/yr",
                  f"Stopped land, Amarakaeri buffer zone, {PSHORT[p]}: mean per year (slide 10)", "stopped", "amarakaeri_bz",
                  PSHORT[p], check=f"amarakaeri_bz_{p}_stopped") for p in (PRE, DUR)}
    fig, ax = _fig()
    _band(ax, DUR)
    _parts_bars(ax, yrs, P["new"].values, P["remined"].values, P["stopped"].values, width=0.6)
    _net_line(ax, yrs, P["net"].values, ms=10)
    top = (P["new"] + P["remined"]).max()
    ax.set_xlim(y0 - 0.6, y1 + 0.6); ax.set_ylim(-P["stopped"].max() * 1.25, top * 1.85)
    _callout(ax, (f + 0.3, P["net"].loc[f]), (f + 0.75, top * 1.78),
             f"2019\nNew land {_fmt(v[(f, 'new')])} ha (2018: {_fmt(v[(r, 'new')])})\n"
             f"Stopped {_fmt(v[(f, 'stopped')])} ha (2018: {_fmt(v[(r, 'stopped')])})\nNet {_fmt(v[(f, 'net')])} ha",
             va="top")
    _fmt_y(ax); _ticks(ax, yrs); _events(ax)
    ax.set_ylabel("ha/yr", fontsize=FS["small"], color=INK2)
    _parts_legend(ax, ncol=2)
    _head(fig, "2019: new pits kept opening, old ones went quiet",
          f"Net mining additions and parts, ha/yr · Tambopata buffer zone · {y0}–{y1} · more stopping explains "
          f"{lo_:.0%}–{hi_:.0%} of the {PSHORT[PRE]} → {PSHORT[DUR]} fall; in Amarakaeri stopped land stayed flat "
          f"({_fmt(am[PRE])} → {_fmt(am[DUR])} ha/yr)")
    _save(fig, "slide_10_2019_parts.png", f"{SRC} New land = mined for the first time since 1985; re-mined = mined again "
          f"after a gap; stopped = left the mining class (water, regrowth). {NO_SEE}", top=0.9, right=0.985)


# --------------------------------------------------------------------------- slide 11: the region, by legal corridor
def s11_region(reg):
    z = Z._zone_year()
    z = z[z.in_mdd == 1]
    cor = z[z.tenure == "corridor"].groupby("year").net_ha.sum()
    tot = z.groupby("year").net_ha.sum()
    tm, cm, sh = {}, {}, {}
    for p in (PRE, DUR, LATER):
        a, b = D.PERIODS[p]
        tm[p] = _add(reg, f"sl_mdd_{p}_net", Z.period_mean(tot, p), "ha/yr", f"Net mining additions, Madre de Dios "
                     f"(department), {PSHORT[p]}: mean per year (slide 11)", "net", "mdd", PSHORT[p], check=f"mdd_{p}_net")
        cm[p] = _add(reg, f"sl_mdd_legal_corridor_{p}_net", Z.period_mean(cor, p), "ha/yr", "Net mining additions on "
                     f"legal-mining-corridor land (all D.L. 1100 land in Madre de Dios, native communities excluded), "
                     f"{PSHORT[p]}: mean per year (slide 11)", "net", "legal_corridor_mdd", PSHORT[p])
        sh[p] = _add(reg, f"sl_corridor_share_{p}_net", cor.loc[a:b].sum() / tot.loc[a:b].sum(), "share",
                     f"Share of Madre de Dios net additions on legal-corridor land, {PSHORT[p]}: period sum / period sum "
                     "(slide 11)", "net", "mdd", PSHORT[p], check=f"v2_corridor_share_{p}_net", tol=1e-9)
    fig, ax = _fig()
    x = np.arange(3)
    c = np.array([cm[p] for p in (PRE, DUR, LATER)]); t = np.array([tm[p] for p in (PRE, DUR, LATER)])
    assert (t - c > 0).all()
    ax.bar(x, c, width=0.56, color=C["corridor"], lw=0, zorder=2)
    ax.bar(x, t - c, bottom=c, width=0.56, color=C["other"], lw=0, zorder=2)
    ax.bar(x, 0, bottom=c, width=0.56, edgecolor=SURFACE, lw=2, zorder=3)
    for i, p in enumerate((PRE, DUR, LATER)):
        ax.text(i, c[i] / 2, f"{sh[p]:.0%}", ha="center", va="center", fontsize=FS["body"] + 3, color="white",
                fontweight="bold", zorder=4)
        ax.annotate(f"{_fmt(t[i])}", xy=(i, t[i]), xytext=(0, 6), textcoords="offset points", ha="center", va="bottom",
                    fontsize=FS["body"], color=INK, fontweight="bold")
    _label(ax, 2.3, c[-1] / 2, "Legal mining corridor\n(all D.L. 1100 land)", dx=4, fs=FS["small"], color=C["corridor"])
    _label(ax, 2.3, c[-1] + (t[-1] - c[-1]) / 2, "Rest of Madre de Dios", dx=4, fs=FS["small"], color=INK2)
    ax.set_xticks(x); ax.set_xticklabels([f"Before\n({PSHORT[PRE]})", f"Mercurio and what\nfollowed ({PSHORT[DUR]})",
                                          f"Later years\n({PSHORT[LATER]})"], fontsize=FS["small"])
    ax.tick_params(axis="x", length=0)
    ax.set_xlim(-0.5, 3.15); ax.set_ylim(0, t.max() * 1.13)
    _fmt_y(ax)
    ax.set_ylabel("ha/yr (period mean)", fontsize=FS["small"], color=INK2)
    _head(fig, "The region kept growing, mostly in the legal corridor",
          f"Net mining additions, ha/yr, period means · Madre de Dios · % = the legal corridor's share of the department's "
          f"net additions (period sums) · legal corridor = all D.L. 1100 land, not only the strip across the road")
    _save(fig, "slide_11_region.png", f"{SRC} Legal mining corridor: D.L. 1100 polygon (INGEMMET), native communities "
          f"excluded; legality is by location, the map class cannot tell legal from illegal. {NO_SEE}",
          top=0.95, left=0.085, right=0.985)


# --------------------------------------------------------------------------- slide 12: across the road
def s12_across(reg):
    u, lp = "corridor_across", "lapampa"
    net = _w("net").loc[Y0:Y1]
    yrs = list(net.index)
    a = {p: _add(reg, f"sl_across_{p}_net", _pm(u, "net", p), "ha/yr", f"Net mining additions, corridor across the "
                 f"road (D.L. 1100 strip ≤ 10 km north of the highway, La Pampa longitudes), {PSHORT[p]}: mean per year "
                 "(slide 12)", "net", u, PSHORT[p], check=f"{u}_{p}_net") for p in (PRE, DUR, LATER)}
    l = {p: _add(reg, f"sl_lapampa_{p}_net", _pm(lp, "net", p), "ha/yr", f"Net mining additions, La Pampa sector, "
                 f"{PSHORT[p]}: mean per year (slide 12)", "net", lp, PSHORT[p], check=f"{lp}_{p}_net")
         for p in (PRE, DUR, LATER)}
    ratio = _add(reg, "sl_across_ratio_during_pre", a[DUR] / a[PRE], "ratio", "Net mining additions, corridor across the "
                 f"road: {PSHORT[DUR]} mean / {PSHORT[PRE]} mean (slide 12)", "net", u, f"{PSHORT[PRE]} vs {PSHORT[DUR]}")
    fig, ax = _fig()
    _band(ax, DUR)
    ax.axhline(0, color=AXIS, lw=1)
    for k, col, nm in ((lp, C["lapampa"], "La Pampa"), (u, C["corridor"], "Corridor across\nthe road")):
        ax.plot(yrs, net[k], "-", color=col, lw=3.2 if k == u else 2.4, zorder=4 if k == u else 3)
        ax.plot(yrs, net[k], "o", color=col, ms=8, mec="white", mew=1.4, zorder=4 if k == u else 3)
        _label(ax, Y1, net[k].loc[Y1], nm, dx=12, fs=FS["small"], color=col)
    for p in (PRE, DUR):
        b0, b1 = D.PERIODS[p]
        ax.plot([b0 - 0.42, b1 + 0.42], [a[p]] * 2, color=C["corridor"], lw=10, alpha=0.3, solid_capstyle="butt", zorder=2)
    ax.set_xlim(Y0 - 0.6, Y1 + 0.6)
    hi = net[[u, lp]].max().max()
    ax.set_ylim(min(net[[u, lp]].min().min(), 0) - 250, hi * 1.15)
    b0, b1 = D.PERIODS[DUR]
    _callout(ax, ((b0 + b1) / 2, a[DUR]), ((b0 + b1) / 2 - 0.2, hi * 0.95),
             f"Across the road: {_fmt(a[PRE])} → {_fmt(a[DUR])} ha/yr\n(means, {PSHORT[PRE]} → {PSHORT[DUR]})",
             ha="center", va="top")
    _fmt_y(ax); _ticks(ax, yrs); _events(ax)
    ax.set_ylabel("ha/yr", fontsize=FS["small"], color=INK2)
    _head(fig, f"Across the road, net mining rose {_fold(ratio)}",
          f"Net mining additions, ha/yr · corridor across the road (legal strip ≤ 10 km north of the highway) vs "
          f"La Pampa sector ({_fmt(l[PRE])} → {_fmt(l[DUR])} ha/yr) · {Y0}–{Y1} · thick bars: means")
    _save(fig, "slide_12_across.png", f"{SRC} La Pampa sector = Tambopata buffer zone 70.15–69.80° W (our boundary); "
          f"corridor across the road = D.L. 1100 land at the same longitudes. We cannot show it was the same miners. "
          f"{NO_SEE}", top=0.9, right=0.86)


# --------------------------------------------------------------------------- slide 13: money and gold (context)
def s13_money(pack, reg):
    import v2_tests
    money = v2_tests.mef_series().loc[Y0:Y1] / 1e6
    gold = pack["prices"].set_index("year")["gold"].loc[Y0:Y1]
    net = _w("net")[TB].loc[Y0:Y1]
    ratio = _add(reg, "sl_gold_ratio_2025_2018", gold.loc[Y1] / gold.loc[D.REF_YEAR], "ratio", "Gold price 2025 / 2018 "
                 "(annual mean, nominal; slide 13)", "price", "world", "2018–2025", src=SRC_PRICE,
                 check="gold_price_ratio_2025_2018", tol=1e-6)
    peak = int(money.idxmax())
    for y in sorted({D.REF_YEAR, peak, Y1}):
        _add(reg, f"sl_pp0128_{y}_msoles", money.loc[y], "million soles", f"PP 0128 executed spending (devengado) booked "
             f"in Madre de Dios, {y} (lower bound; slide 13)", "spending", "mdd", str(y), src="MEF Consulta Amigable")
    fig, axes = _fig(1, 3, gridspec_kw={"wspace": 0.3})
    a1, a2, a3 = axes
    a1.bar(money.index, money.values, color=C["buffer"], width=0.7, zorder=2)
    _label(a1, peak - 0.45, money.loc[peak], f"{money.loc[peak]:.0f} M\nin {peak}", dx=-6, dy=-4, fs=FS["small"], va="top",
           ha="right")
    _label(a1, Y1, money.loc[Y1], f"{money.loc[Y1]:.0f} M", dx=0, dy=6, fs=FS["small"], ha="center", va="bottom")
    a1.set_ylim(0, money.max() * 1.25)
    a2.plot(gold.index, gold.values, "-", color=C["gold"], lw=3.2)
    a2.plot(gold.index, gold.values, "o", color=C["gold"], ms=7, mec="white", mew=1.2)
    _label(a2, Y1, gold.loc[Y1], f"${gold.loc[Y1]:,.0f}", dx=0, dy=10, fs=FS["small"], ha="right", va="bottom")
    _label(a2, D.REF_YEAR, gold.loc[D.REF_YEAR], f"${gold.loc[D.REF_YEAR]:,.0f}", dx=0, dy=-12, fs=FS["small"],
           ha="center", va="top")
    a2.set_ylim(0, gold.max() * 1.22)
    a3.axhline(0, color=INK2, lw=1)
    a3.bar(net.index, net.values, color=[C["lapampa"] if v >= 0 else MUTED for v in net.values], width=0.7, zorder=2)
    a3.set_ylim(min(net.min() * 1.3, -150), net.max() * 1.2)
    titles = ("Enforcement money,\nMadre de Dios (M soles)", "Gold price\n(US$ per ounce)",
              "Net mining additions,\nTambopata buffer zone")
    for ax, t in zip(axes, titles):
        _band(ax, DUR)
        _fmt_y(ax); ax.set_xlim(Y0 - 0.6, Y1 + 0.6)
        ticks = [Y0 + 1, D.REF_YEAR, D.REF_YEAR + 3, Y1 - 1]
        ax.set_xticks(ticks); ax.set_xticklabels([str(ticks[0])] + [f"'{str(y)[2:]}" for y in ticks[1:]], fontsize=FS["tick"])
        ax.tick_params(axis="x", length=0)
        ax.set_title(t, loc="left", fontsize=FS["label"], color=INK, pad=12, fontweight="medium")
        _events(ax, label=False)
    _head(fig, f"Money faded after {peak}, while gold rose {ratio:.1f}-fold",
          f"Same years in each panel, {Y0}–{Y1} · PP 0128 executed spending booked in Madre de Dios (a lower bound) · "
          f"gold price, nominal · net mining additions, Tambopata buffer zone · shaded: {PSHORT[DUR]} · context, not a test")
    _save(fig, "slide_13_money.png", f"MEF Consulta Amigable, PP 0128 devengado, Madre de Dios; {SRC_PRICE}; {SRC} "
          "No correlation shown: 11 years, and money follows mining.", top=0.84, left=0.055, right=0.985)


# --------------------------------------------------------------------------- slide 14: it came back (parts)
def s14_back(reg):
    yrs = list(range(Y0, Y1 + 1))
    P = {mm: _w(mm)[TB].loc[Y0:Y1] for mm in ["net"] + D.PARTS}
    later = {mm: _add(reg, f"sl_later_{mm}", _pm(TB, mm, LATER), "ha/yr", f"{D.MEASURE_NAME[mm]}, {D.UNIT_NAME[TB]}, "
                      f"{PSHORT[LATER]}: mean per year (slide 14)", mm, TB, PSHORT[LATER], check=f"{TB}_later_{mm}")
             for mm in ["net"] + D.PARTS}
    ex = {mm: _add(reg, f"sl_later_ex2023_{mm}", _later_ex(TB, mm), "ha/yr", f"{D.MEASURE_NAME[mm]}, {D.UNIT_NAME[TB]}, "
                   "2022, 2024, 2025 (without 2023): mean per year (slide 14)", mm, TB, "2022, 2024, 2025",
                   check=f"{TB}_later_ex2023_{mm}") for mm in ["net", "new", "remined"]}
    sh = _add(reg, "sl_later_remined_share", later["remined"] / (later["new"] + later["remined"]), "share",
              f"Re-mined land as a share of land added (new + re-mined), {D.UNIT_NAME[TB]}, {PSHORT[LATER]} (slide 14)",
              "remined", TB, PSHORT[LATER], check=f"{TB}_later_remined_share_added", tol=1e-9)
    sh_ex = _add(reg, "sl_later_ex2023_remined_share", ex["remined"] / (ex["new"] + ex["remined"]), "share",
                 f"Re-mined land as a share of land added (new + re-mined), {D.UNIT_NAME[TB]}, 2022, 2024, 2025 "
                 "(without 2023; slide 14)", "remined", TB, "2022, 2024, 2025",
                 check=f"{TB}_later_ex2023_remined_share_added", tol=1e-9)
    lo_, hi_ = sorted([sh, sh_ex])
    assert 0.28 <= lo_ and hi_ <= 0.55, f"title 'a third to a half' no longer fits: {lo_:.0%}–{hi_:.0%}"
    fig, ax = _fig()
    _band(ax, LATER)
    _parts_bars(ax, yrs, P["new"].values, P["remined"].values, P["stopped"].values)
    _net_line(ax, yrs, P["net"].values)
    top = (P["new"] + P["remined"]).max()
    ax.set_xlim(Y0 - 0.6, Y1 + 0.6); ax.set_ylim(-P["stopped"].max() * 1.25, top * 1.9)
    a, b = D.PERIODS[LATER]
    _callout(ax, (a + 0.2, top * 1.02), (D.REF_YEAR + 0.6, top * 1.86),
             f"Later years ({PSHORT[LATER]})\nNet {_fmt(later['net'])} ha/yr ({_fmt(ex['net'])} without 2023)\n"
             f"Re-mined: {sh:.0%} of added land ({sh_ex:.0%} without 2023)", va="top")
    _fmt_y(ax); _ticks(ax, yrs); _events(ax)
    ax.set_ylabel("ha/yr", fontsize=FS["small"], color=INK2)
    _parts_legend(ax, ncol=2)
    _head(fig, "It came back, partly on old pits (33–46%)",
          f"Net mining additions and parts, ha/yr · Tambopata buffer zone · {Y0}–{Y1} · shaded: later years "
          f"({PSHORT[LATER]}) · share = re-mined ÷ (new + re-mined)")
    _save(fig, "slide_14_came_back.png", f"{SRC} 2023 is a spike in MapBiomas only (forest-loss alerts and Amazon Mining "
          f"Watch are flat), so later years are shown with and without it. MAAP #193 (2023) reports miners back on "
          f"degraded land. {NO_SEE}", top=0.9, right=0.985)


# --------------------------------------------------------------------------- slide 15: inside the reserve
def s15_reserve(reg):
    u = "tambopata_nr"
    s = _w("net")[u].loc[Y0:Y1]
    yrs = list(s.index)
    v25 = _add(reg, "sl_reserve_2025_net", s.loc[Y1], "ha/yr", "Net mining additions, Tambopata National Reserve, 2025 "
               "(slide 15)", "net", u, str(Y1), check="tambopata_nr_2025_net")
    _add(reg, "sl_reserve_2017_net", s.loc[2017], "ha/yr", "Net mining additions, Tambopata National Reserve, 2017 "
         "(slide 15 notes)", "net", u, "2017", check="tambopata_nr_2017_net")
    dur = _add(reg, "sl_reserve_during_net", _pm(u, "net", DUR), "ha/yr", "Net mining additions, Tambopata National "
               f"Reserve, {PSHORT[DUR]}: mean per year (slide 15 notes)", "net", u, PSHORT[DUR], check="tambopata_nr_during_net")
    fig, ax = _fig()
    ax.axhline(0, color=INK2, lw=1)
    ax.bar(yrs, s.values, color=[C["reserve"] if y == Y1 else "#c4d6bd" for y in yrs], width=0.68, zorder=2)
    _label(ax, Y1, s.loc[Y1], f"+{_fmt(v25)} ha\nin {Y1}", dx=0, dy=8, ha="center", va="bottom")
    _label(ax, 2017, s.loc[2017], "an earlier jump", dx=0, dy=6, ha="center", va="bottom", fs=FS["small"],
           weight="normal", color=INK2)
    ax.set_xlim(Y0 - 0.6, Y1 + 0.6); ax.set_ylim(min(-80, s.min() * 1.4), max(s.max(), v25) * 1.3)
    _fmt_y(ax); _ticks(ax, yrs); _events(ax)
    ax.set_ylabel("ha/yr", fontsize=FS["small"], color=INK2)
    _head(fig, f"In {Y1}, mining inside the reserve jumped {_fmt(v25)} ha",
          f"Net mining additions, ha/yr · Tambopata National Reserve (inside the reserve, not the buffer zone) · {Y0}–{Y1}")
    _save(fig, "slide_15_reserve.png", f"{SRC} Platform check: 777 ha of mining inside the reserve in 2025 (protected-area "
          f"statistics). MAAP #241 (Pacsi et al., 2026) reports ~500 ha inside the reserve, late 2025 to Feb 2026. {NO_SEE}",
          top=0.9, right=0.985)


# --------------------------------------------------------------------------- slide 18: placebo dots, raw vs scaled
def _placebo_sets(pack):
    import peru_models as PM
    ad = PM._zone_adds()
    gold = pack["prices"].set_index("year")["gold"]
    poolB, big, _, _ = PM.pools(ad)
    res = {}
    for m, units in (("M1", poolB), ("M4", big)):
        noT = [v for v in units if v != TB]
        g = {u: PM.fit(ad, noT, u, m, *PM.EST, PM.REAL, gold)["post_during"] for u in noT}
        g[TB] = PM.fit(ad, units, TB, m, *PM.EST, PM.REAL, gold)["post_during"]
        res[m] = pd.Series(g).sort_values()
    return res

def s18_placebo(pack, reg):
    res = _placebo_sets(pack)
    r1 = placebo_rank(res["M1"][TB], res["M1"].drop(TB)); n1 = len(res["M1"])
    r4 = placebo_rank(res["M4"][TB], res["M4"].drop(TB)); n4 = len(res["M4"])
    assert r1 == reg.get("model_m1_rank") and n1 == reg.get("model_m1_n")
    assert r4 == reg.get("model_m4_rank") and n4 == reg.get("model_m4_n")
    assert abs(res["M1"][TB] - reg.get("model_m1_during_net")) < 1e-6
    sc_lo, sc_hi = int(reg.get("sl_rank_scaled_lo")), int(reg.get("sl_rank_scaled_hi"))
    _add(reg, "sl_placebo_rank_ha", r1, "rank", f"Rank of the Tambopata buffer zone's 2019–21 change in net additions among "
         f"{n1} Peruvian buffer zones, hectares (1 = biggest fall; slide 18)", "rank", TB, PSHORT[DUR], claim="causal",
         check="model_m1_rank", tol=0)
    _add(reg, "sl_placebo_rank_scaled", r4, "rank", f"Same rank, scaled to each zone's own pre-2019 size, among {n4} zones "
         "(slide 18)", "rank", TB, PSHORT[DUR], claim="causal", check="model_m4_rank", tol=0)
    fig, axes = _fig(2, 1, gridspec_kw={"hspace": 1.15})
    rows = [(res["M1"], "In hectares", f"Tambopata: {_ordinal(r1)} of {n1}",
             f"change in net additions in {PSHORT[DUR]}, ha/yr, vs the other zones", lambda x, p: _fmt(x)),
            (res["M4"], "Relative to its own size", f"Tambopata: {_ordinal(r4)} of {n4} ({_ordinal(sc_lo)}–{_ordinal(sc_hi)} "
             "depending on the scaling)", "same change, in multiples of each zone's normal pre-2019 year",
             lambda x, p: _fmt(x, 1))]
    rng = np.random.default_rng(3)
    for i, (ax, (ser, lab, rank_txt, unit, fmt)) in enumerate(zip(axes, rows)):
        others = ser.drop(TB)
        jit = rng.uniform(-0.16, 0.16, len(others))
        ax.axvline(0, color=AXIS, lw=1.2, zorder=1)
        ax.scatter(others.values, jit, s=260, color="#bdb9b0", edgecolor="white", lw=1.5, zorder=2)
        ax.scatter([ser[TB]], [0], s=560, color=C["lapampa"], edgecolor="white", lw=2, zorder=3)
        ax.annotate(f"Tambopata {fmt(ser[TB], None)}", xy=(ser[TB], 0), xytext=(0, -24), textcoords="offset points",
                    ha="left" if i == 0 else "center", va="top", fontsize=FS["small"], color=C["lapampa"], fontweight="bold")
        ax.annotate(f"{len(others)} other zones, each given a fake operation", xy=(others.median(), 0), xytext=(0, -24),
                    textcoords="offset points", ha="center", va="top", fontsize=FS["small"], color=INK2)
        ax.set_ylim(-1.0, 0.45); ax.set_yticks([])
        for sp in ("left", "right", "top"):
            ax.spines[sp].set_visible(False)
        ax.spines["bottom"].set_color(AXIS)
        ax.xaxis.set_major_formatter(FuncFormatter(fmt)); ax.tick_params(axis="x", labelsize=FS["tick"], colors=INK2)
        ax.set_xlabel(unit, fontsize=FS["small"], color=INK2)
        lo_x, hi_x = min(ser.min(), 0), max(ser.max(), 0)
        pad = (hi_x - lo_x) * 0.1
        ax.set_xlim(lo_x - pad, hi_x + pad)
        ax.text(0.0, 1.12, lab, transform=ax.transAxes, fontsize=FS["label"] + 1, color=INK, fontweight="bold", ha="left")
        ax.text(1.0, 1.12, rank_txt, transform=ax.transAxes, fontsize=FS["label"] + 1, ha="right",
                color=C["lapampa"] if i == 0 else INK2, fontweight="bold")
    _head(fig, "The fall stands out in hectares, not for its size",
          f"Each grey dot: one Peruvian buffer zone given a fake operation in 2019 · orange: the Tambopata buffer zone's "
          f"real {PSHORT[DUR]} change · net mining additions, after each zone's level and each year's shared change")
    _save(fig, "slide_18_placebo.png", f"{SRC} {n1} Peruvian buffer zones with mining before 2019 (scaled: {n4} with more "
          f"than 10 ha/yr). Tambopata removed from each fake zone's comparison pool. A rank shows whether the real result "
          "stands out; with one target it is not a significance test.", top=0.84, left=0.03, right=0.97, xlab=True)


# --------------------------------------------------------------------------- backup: estimates, one causal range
def b_estimates(reg):
    g = reg.get
    lo_, hi_ = abs(g("model_m1_during_net")), abs(g("did_base2014_net"))
    _add(reg, "sl_causal_range_lo", lo_, "ha/yr", "Conditional causal range, low end: |zone + year effects (M1), 15 zones|, "
         f"net additions, {D.UNIT_NAME[TB]}, {PSHORT[DUR]}", "net", TB, PSHORT[DUR], claim="causal")
    _add(reg, "sl_causal_range_hi", hi_, "ha/yr", "Conditional causal range, high end: |Tambopata vs Amarakaeri buffer zone, "
         f"2014–18 baseline|, net additions, {D.UNIT_NAME[TB]}, {PSHORT[DUR]}", "net", TB, PSHORT[DUR], claim="causal")
    rows = [("Zone + year effects, 15 zones", "model_m1_during_net", "low end of the range"),
            ("Synthetic DiD, 15 zones", "sdid_sdid_ha_during_net", "inside"),
            ("+ gold price × zone size", "model_m2_during_net", "inside"),
            ("Tambopata vs Amarakaeri,\n2014–18 baseline", "did_base2014_net", "high end of the range"),
            ("+ each zone's own trend", "model_m3_during_net",
             f"left out: fails the fake-2016 test ({_fmt(g('model_m3_placebo_net'))} ha/yr)"),
            ("Synthetic control", "sdid_sc_ha_during_net", "left out: all weight on Amarakaeri, no pre-2019 fit")]
    rows = sorted(rows, key=lambda r: g(r[1]))
    fig, ax = _fig()
    yy = np.arange(len(rows))[::-1]
    ax.axvspan(-hi_, -lo_, color="#f1d9c8", lw=0, zorder=0)
    ax.text(-(hi_ + lo_) / 2, len(rows) - 0.6, f"the one causal range: {_fmt(lo_)}–{_fmt(hi_)} ha/yr", ha="center",
            va="bottom", fontsize=FS["small"], color=INK, fontweight="bold")
    ax.axvline(0, color=INK2, lw=1.4)
    for yv, (lab, k, why) in zip(yy, rows):
        v = g(k)
        inside = -hi_ - 1e-6 <= v <= -lo_ + 1e-6
        assert inside == (not why.startswith("left out")), f"{k} = {v} vs range"
        _add(reg, f"sl_est_{k}", v, "ha/yr", f"Estimate {lab.replace(chr(10), ' ')}, net additions, {D.UNIT_NAME[TB]}, "
             f"{PSHORT[DUR]} (backup estimates slide; conditional)", "net", TB, PSHORT[DUR], claim="causal", check=k, tol=1e-6)
        ax.plot([v, 0], [yv, yv], color="#d3d1cb", lw=2, zorder=1)
        ax.plot(v, yv, "o", ms=15, color=C["lapampa"] if inside else "#a9a8a2", mec="white", mew=2, zorder=3)
        ax.annotate(_fmt(v), xy=(v, yv), xytext=(-16, 0), textcoords="offset points", ha="right", va="center",
                    fontsize=FS["small"], color=INK, fontweight="bold")
        if not inside:
            right = v < -lo_
            ax.annotate(why, xy=(v, yv), xytext=(14 if right else -14, -12), textcoords="offset points",
                        ha="left" if right else "right", va="top", fontsize=FS["small"] - 1, color=INK2)
    ax.set_yticks(yy); ax.set_yticklabels([r[0] for r in rows], fontsize=FS["small"])
    style_axes(ax, fmt=False); ax.yaxis.grid(False); ax.xaxis.grid(True, color=GRID, lw=0.6)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: _fmt(x)))
    ax.tick_params(axis="x", labelsize=FS["tick"])
    ax.set_xlim(-2250, 150); ax.set_ylim(-0.75, len(rows) - 0.1)
    ax.set_xlabel(f"Estimated change in net mining additions, Tambopata buffer zone, {PSHORT[DUR]}, ha/yr",
                  fontsize=FS["small"], color=INK2)
    _head(fig, f"One causal range: {_fmt(lo_)}–{_fmt(hi_)} ha a year",
          f"Estimated change in net mining additions, ha/yr · Tambopata buffer zone · {PSHORT[DUR]} · causal only if the "
          f"comparison zones show what Tambopata would have done; an upper bound; part of it is pits stopping")
    _save(fig, "slide_b0_estimates.png", f"{SRC} 15 Peruvian buffer zones, 2014–25 (zone + year effects and synthetic DiD); "
          "Tambopata vs Amarakaeri on the 2014–18 baseline. Fake-2016 test: same model with a fake start in 2016.",
          top=0.97, left=0.25, right=0.985, xlab=True)


# --------------------------------------------------------------------------- backup: stopped split
def b1_stopped_split(reg):
    ru = Z.region_units()
    units = [(D.TREATED_ZONE, "Tambopata buffer zone"), ("lapampa", "La Pampa sector"),
             ("corridor_across", "Corridor across the road"), ("amarakaeri_bz", "Amarakaeri buffer zone")]
    dest = [("stopped_to_water_ha", "became water", "#6f9fb6"), ("stopped_to_forest_ha", "became forest", C["reserve"]),
            ("stopped_to_natural_ha", "other natural", C["buffer_tint"]), ("stopped_to_bare_ha", "bare ground", "#d9c7a7"),
            ("stopped_to_other_ha", "other (farm,\nurban, ...)", C["other"])]
    fig, axes = _fig(1, 4, sharey=True, gridspec_kw={"wspace": 0.1})
    for ax, (u, ttl) in zip(axes, units):
        d = ru[ru.unit == u].set_index("year")
        x = np.arange(3); bot = np.zeros(3)
        tot = np.array([Z.period_mean(d["stopped_ha"], p) for p in (PRE, DUR, LATER)])
        assert np.allclose(sum(np.array([Z.period_mean(d[c], p) for p in (PRE, DUR, LATER)]) for c, _, _ in dest), tot, rtol=1e-6)
        for col, lab, c in dest:
            v = np.array([Z.period_mean(d[col], p) for p in (PRE, DUR, LATER)]) / tot
            ax.bar(x, v, bottom=bot, width=0.62, color=c, lw=0, zorder=2, label=lab)
            ax.bar(x, 0, bottom=bot + v, width=0.62, edgecolor=SURFACE, lw=1.4, zorder=3)
            bot += v
        for i, p in enumerate((PRE, DUR, LATER)):
            a, b = D.PERIODS[p]
            sl = d.loc[a:b]
            back = sl["stopped_back_2y_ha"].sum(min_count=1) / sl.loc[sl["stopped_back_2y_ha"].notna(), "stopped_ha"].sum()
            _add(reg, f"sl_stopped_back2y_{u}_{p}", back, "share", f"Share of stopped land mining again within 2 years, "
                 f"{D.UNIT_NAME[u]}, {PSHORT[p]} (years with 2 years of follow-up; backup slide)", "stopped", u, PSHORT[p])
            ax.text(i, 1.03, f"{back:.0%}", ha="center", va="bottom", fontsize=13, color=INK, fontweight="bold")
            ax.text(i, -0.06, f"{_fmt(tot[i])}", ha="center", va="top", fontsize=11, color=INK2)
        ax.set_xticks(x); ax.set_xticklabels([PSHORT[p] for p in (PRE, DUR, LATER)], fontsize=11)
        ax.tick_params(axis="x", pad=24, length=0)
        ax.tick_params(axis="y", labelsize=12)
        ax.set_title(ttl, loc="left", fontsize=14, color=INK, pad=40, fontweight="medium")
        ax.set_ylim(0, 1.0); _fmt_y(ax, pct=True); ax.set_xlim(-0.5, 2.5)
    axes[0].text(-0.5, 1.115, "back within 2 yrs ↓", fontsize=11, color=INK2, transform=axes[0].get_xaxis_transform())
    axes[0].set_ylabel("share of stopped land", fontsize=13, color=INK2)
    axes[-1].legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=12, frameon=False, handlelength=1.0)
    _head(fig, "Stopped land: often water, often mined again within 2 years",
          "Stopped land (left the mining class), share by what it became and share mining again within 2 years, "
          "period means · four zones · 2016–18, 2019–21, 2022–25 (small numbers under the bars: stopped ha/yr). Numbers on top: share mining again within 2 years.")
    _save(fig, "slide_b1_stopped_split.png", f"{SRC} Back within 2 years = classifier flicker or re-entry; the last two "
          "years cannot be followed up. No image validation sample.", top=0.80, left=0.075, right=0.85, xlab=True)


# --------------------------------------------------------------------------- backup: twins (other measure)
def b2_twins(reg):
    import control_top3 as ct
    import control_select as cs
    sd = ct.slide_data()
    I, pace, ids = sd["index"].loc[2010:D.REF_YEAR], sd["pace"], sd["ids"]
    tam_idx = cs.tambopata_index(2010, D.REF_YEAR)
    assert np.allclose(I[ct.TU].values, tam_idx.values)
    for u in [ct.TU] + ids:
        nm = sd["short"][u]
        _add(reg, f"sl_twin_pace_{u.replace('-', '_').lower()}", pace[u], "% of 2018 AMW area",
             f"AMW new area per year 2019–21 as % of own 2018 AMW area, {nm} (other measure: comparable to first-time "
             f"mining, not net; backup slide)", "amw_new_area", nm, "2019–21")
    ratio = pace[ct.TU] / np.mean([pace[u] for u in ids])
    _add(reg, "sl_twin_ratio", ratio, "ratio", "Tambopata's 2019–21 AMW pace / mean of the twins' paces (backup slide)",
         "amw_new_area", D.TREATED_ZONE, "2019–21", check="top3_ratio", tol=1e-6)
    fig, (a1, a2) = _fig(1, 2, gridspec_kw={"width_ratios": [1.5, 1], "wspace": 0.45})
    yrs = list(I.index)
    a1.axhline(100, color=AXIS, lw=1)
    ys = I.loc[yrs[0]].sort_values()                    # start labels, spread so they never overlap
    pos, last = {}, -1e9
    for u, v in ys.items():
        pos[u] = max(v, last + 9); last = pos[u]
    for u in I:
        a1.plot(yrs, I[u], "-o", color=sd["color"][u], lw=3, ms=7, mec="white", mew=1.2)
        a1.annotate(f"{sd['short'][u]}  {I.loc[yrs[0], u]:.0f}", xy=(yrs[0], I.loc[yrs[0], u]), xytext=(yrs[0] - 0.25, pos[u]),
                    textcoords="data", ha="right", va="center", fontsize=FS["small"], color=INK, fontweight="bold",
                    annotation_clip=False)
    a1.set_xlim(yrs[0] - 0.4, yrs[-1] + 0.4); a1.tick_params(axis="y", labelleft=False)
    a1.set_ylim(0, 115)
    _fmt_y(a1); _ticks(a1, yrs)
    a1.set_title("Before: mining area (stock), index 2018 = 100", loc="left", fontsize=FS["small"], color=INK, pad=10)
    order = [ct.TU] + ids
    a2.barh(range(len(order))[::-1], [pace[k] for k in order], color=[sd["color"][k] for k in order], height=0.6)
    for i, k in zip(range(len(order))[::-1], order):
        _label(a2, pace[k], i, f"{pace[k]:.0f}%", dx=6, fs=FS["body"])
    a2.set_yticks(range(len(order))[::-1]); a2.set_yticklabels([sd["short"][k] for k in order], fontsize=FS["small"])
    style_axes(a2, ygrid=False, fmt=False); a2.set_xticks([]); a2.spines["bottom"].set_visible(False)
    a2.set_title("2019–21: AMW new area per year,\n% of own 2018 area", loc="left", fontsize=FS["small"], color=INK, pad=10)
    a2.set_xlim(0, max(pace.values()) * 1.3)
    p = sd["pretrend_p_max"]
    r_ex = reg.get("top3_ratio_excl_unverified") if "top3_ratio_excl_unverified" in reg.rows else ratio
    _head(fig, f"Twins: Tambopata at {ratio:.0%}–{r_ex:.0%} of their pace; trends differed before",
          f"Left: mining area (stock), index 2018 = 100, 2010–18 (pre-trends rejected, p {'< 0.001' if p < 0.001 else '≤ ' + format(p, '.3f')}). "
          "Right: Amazon Mining Watch new area 2019–21 per year, % of own 2018 area: a different measure, not net additions.")
    _save(fig, "slide_b2_twins.png", f"{sd['source_index']}; {sd['source_pace']}. Twins chosen by fixed rules (Ruby's "
          "four rules). Different collections: compared as indices, never subtracted.", top=0.82, left=0.2, right=0.97)



def run(pack, reg):
    print("\n== Slide figures (storyline v3.1: net additions + parts, lean) ==")
    s09_net(reg)
    s10_2019(reg)
    s11_region(reg)
    s12_across(reg)
    s13_money(pack, reg)
    s14_back(reg)
    s15_reserve(reg)
    for k, c in (("lo", min), ("hi", max)):        # scaled placebo rank across M1, M4, synthetic DiD and the event study
        v = c(int(reg.get(i)) for i in ("model_m4_rank", "model_m1_rank_scaled", "sdid_sdid_scaled_during_rank",
                                         "placebo_space_rank_scaled"))
        _add(reg, f"sl_rank_scaled_{k}", v, "rank", f"{'Best' if k == 'lo' else 'Worst'} size-relative placebo rank of the "
             "Tambopata buffer zone across M1, M4, synthetic DiD and the event study (slides 17-18)", "rank", TB, PSHORT[DUR])
    s18_placebo(pack, reg)
    b_estimates(reg)
    b1_stopped_split(reg)
    b2_twins(reg)
    for old in SL.glob("*.png"):                       # remove superseded slide images
        if old.stem not in TITLES:
            old.unlink()
    (SL / "slide_titles.json").write_text(json.dumps(TITLES, ensure_ascii=False, indent=2))
    print("Saved output/slides/slide_titles.json")


if __name__ == "__main__":       # quick rebuild from the last output/numbers.csv (main.py registers the sl_* ids)
    from common import Numbers, load_pack
    reg = Numbers()
    n = pd.read_csv(OUT / "numbers.csv").fillna("")
    for r in n[~n.id.str.startswith("sl_")].itertuples():
        reg.rows[r.id] = dict(id=r.id, value=float(r.value), unit=r.unit)
    run(load_pack(), reg)
    sl = pd.DataFrame([v for k, v in reg.rows.items() if k.startswith("sl_")])
    print(f"{len(sl)} slide numbers registered (main.py writes them to numbers.csv)")
