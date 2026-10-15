"""Slide figures for the FZS talk, storyline v3 (docs/presentation/STORYLINE.md): output/slides/*.png + slide_titles.json.

Plan v3 (docs/PLAN_v3.md): ONE measure on every chart, net mining additions (ha/yr) = new land + re-mined − stopped,
from the MapBiomas Peru Collection 4 rasters on one zone registry, read ONLY through zonedata.py. Where the parts are
shown they use the fixed colours of common.C (new brown, re-mined amber, stopped teal below zero) and net is drawn in
INK; parts are shown as small multiples, one panel per zone (zone named in the panel title), never next to an orange
La Pampa / Tambopata line. Periods come from definitions.PERIODS ("Mercurio and what followed (2019–21)", "later
years (2022–25)").

Same visual system as every other figure (common.py palette, direct labels, source line), scaled for projection:
13 x 5 in at 200 dpi, body text >= 13 pt. The takeaway title and the measure/unit/zone/period subtitle go to
slide_titles.json (the deck draws them); both are computed from the data. Every number written on a slide is
registered as `sl_*` with measure/zone/period, and asserted equal to the canonical number where one exists.
All DESCRIPTION except slide_07 (the tests behind the one CONDITIONAL causal claim).
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

from common import OUT, C, INK, INK2, MUTED, AXIS, GRID, SURFACE, style_axes, PERU_EVENTS, SRC_PRICE
import definitions as D
import zonedata as Z

SL = OUT / "slides"
W, H, DPI = 13.0, 5.0, 200          # full content width under the slide title (deck reads w_in/h_in)
TITLES: dict = {}                   # slide name -> title / subtitle / source (the PPT slide carries the title)
FS = dict(body=15, tick=14, label=15, small=13, source=11)
RC = {"font.size": FS["body"], "xtick.labelsize": FS["tick"], "ytick.labelsize": FS["tick"],
      "axes.titlesize": FS["label"], "axes.labelsize": FS["label"], "xtick.major.size": 4}
PRE, DUR, LATER = "pre", "during", "later"
PNAME = {PRE: "Before (2016–18)", DUR: "Mercurio and what\nfollowed (2019–21)", LATER: "Later years\n(2022–25)"}
PSHORT = {p: D.period_label(p) for p in (PRE, DUR, LATER)}
BAND = "#ebe6dc"
SRC = ("MapBiomas Peru Collection 4 annual maps (30 m, class 4.2 mining, legal and illegal), our pixel accounting on "
       "one zone registry (La Pampa sector = Tambopata buffer zone 70.15–69.80° W; corridor = D.L. 1100).")
NO_SEE = "Satellites cannot see river dredges or mercury."
PARTS_NOTE = "New land = mined for the first time since 1985; re-mined = mined again after a gap; stopped = left the mining class."
PART_COL = {"new": C["new"], "remined": C["remined"], "stopped": C["stopped"]}
PART_LAB = {"new": "New land", "remined": "Re-mined", "stopped": "Stopped (below zero)", "net": "Net additions"}


# --------------------------------------------------------------------------- data helpers (zonedata only)
def _w(col: str) -> pd.DataFrame:
    return Z.wide(Z.region_units(), D.COLS[col] if col in D.COLS else col)

def _pm(unit: str, m: str, p) -> float:
    return Z.period_mean(_w(m)[unit], p)

def _later_ex(unit: str, m: str) -> float:
    a, b = D.PERIODS[LATER]
    s = _w(m)[unit].loc[a:b]
    return float(s.drop(D.LATER_EX).mean())

def _yr(unit: str, m: str, y: int) -> float:
    return float(_w(m)[unit].loc[y])

def _add(reg, id, v, unit, desc, measure, zone, period, claim="description", src=D.SOURCE, check=None, tol=0.5):
    """Register a slide number (sl_*) with measure/zone/period; assert it equals the canonical id if given."""
    if check is not None and check in reg.rows:
        assert abs(float(v) - reg.get(check)) <= tol, f"{id} = {v} differs from {check} = {reg.get(check)}"
    reg.add(id, v, unit, desc, claim, src, measure=measure, zone=zone, period=period)
    return float(v)

def _fmt(v, d=0):
    return f"{v:,.{d}f}".replace("-", "−")


# --------------------------------------------------------------------------- drawing helpers
def _fig(nrows=1, ncols=1, **kw):
    with plt.rc_context(RC):
        fig, axes = plt.subplots(nrows, ncols, figsize=(W, H), **kw)
    return fig, axes

def _head(fig, title, sub):
    """Takeaway title + subtitle (measure, unit, zone, period) go to slide_titles.json, drawn by the PPT."""
    if len(title) > 66:
        print(f"  WARNING slide title over one line at 28 pt ({len(title)} chars): {title}")
    fig._slide_title = (title, sub)

def _ticks(ax, years, step=1):
    ax.set_xticks(years[::step])
    ax.set_xticklabels([str(y) if i == 0 or y % 5 == 0 else f"'{str(y)[2:]}" for i, y in enumerate(years)][::step])
    ax.tick_params(labelsize=FS["tick"])

def _events(ax, label=True, keep=None):
    """Event lines at Y − 0.5 (common.py convention); short labels in two rows above the axes."""
    lo, hi = ax.get_xlim()
    k = 0
    for ev in PERU_EVENTS:
        x = ev["year"] - 0.5
        if not lo <= x <= hi or (keep and ev["short"] not in keep):
            continue
        solid = ev["style"] == "solid"
        ax.axvline(x, color=INK if solid else AXIS, ls="-" if solid else (0, (3, 2)), lw=1.4 if solid else 1.0, zorder=0.5)
        if label:
            ax.annotate(ev["short"], xy=(x, 1.0), xycoords=("data", "axes fraction"), xytext=(0, 4 + 17 * (k % 2)),
                        textcoords="offset points", ha="center", va="bottom", fontsize=FS["small"],
                        color=INK if solid else INK2, fontweight="bold" if solid else "normal", annotation_clip=False)
        k += 1
    ax.set_xlim(lo, hi)

def _band(ax, key=DUR, label=None):
    a, b = D.PERIODS[key]
    ax.axvspan(a - 0.5, b + 0.5, color=BAND, zorder=-1, lw=0)
    if label:
        ax.text((a + b) / 2, 0.02, label, transform=ax.get_xaxis_transform(), ha="center", va="bottom",
                fontsize=FS["small"] - 1, color=INK2, linespacing=1.1)

def _label(ax, x, y, text, dx=10, dy=0, fs=None, weight="bold", ha="left", va="center", color=INK):
    ax.annotate(text, xy=(x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va,
                fontsize=fs or FS["body"], color=color, fontweight=weight, annotation_clip=False, linespacing=1.15)

def _fmt_y(ax, pct=False):
    style_axes(ax)
    ax.yaxis.set_major_formatter(FuncFormatter((lambda v, p: f"{v:.0%}") if pct else (lambda v, p: _fmt(v))))
    ax.tick_params(axis="y", labelsize=FS["tick"])

def _parts_bars(ax, x, new, rem, stp, width=0.74, alpha=1.0):
    """Stacked parts: new + re-mined above zero, stopped below zero. A 1.5-pt surface gap between segments."""
    ax.bar(x, new, width=width, color=C["new"], lw=0, zorder=2, alpha=alpha)
    ax.bar(x, rem, bottom=new, width=width, color=C["remined"], lw=0, zorder=2, alpha=alpha)
    ax.bar(x, -np.asarray(stp), width=width, color=C["stopped"], lw=0, zorder=2, alpha=alpha)
    ax.bar(x, np.zeros(len(np.atleast_1d(x))), bottom=new, width=width, color=SURFACE, edgecolor=SURFACE, lw=1.5, zorder=3)
    ax.axhline(0, color=INK2, lw=1.0, zorder=3)

def _net_line(ax, x, net, ms=8):
    ax.plot(x, net, "-", color=INK, lw=2.6, zorder=5)
    ax.plot(x, net, "o", color=INK, ms=ms, mec="white", mew=1.4, zorder=6)

def _parts_legend(ax, net=True, loc="upper left", ncol=4, anchor=None, net_bar=False):
    h = [Patch(color=C["new"], label=PART_LAB["new"]), Patch(color=C["remined"], label=PART_LAB["remined"]),
         Patch(color=C["stopped"], label=PART_LAB["stopped"])]
    if net_bar:
        h.append(Patch(color=INK, label="Net additions"))
    elif net:
        h.append(Line2D([], [], color=INK, marker="o", ms=7, mec="white", lw=2.4, label="Net additions"))
    kw = dict(bbox_to_anchor=anchor) if anchor else {}
    ax.legend(handles=h, loc=loc, ncol=ncol, fontsize=FS["small"], frameon=False, handlelength=1.2, columnspacing=1.4,
              borderaxespad=0.2, **kw)

def _save(fig, name, source, top=0.88, bottom=None, left=0.07, right=0.97, xlab=False, **adj):
    t, sub = getattr(fig, "_slide_title", ("", ""))
    w_in, h_in = fig.get_size_inches()
    TITLES[name.removesuffix(".png")] = dict(title=t, subtitle=sub.replace("\n", " "), source="Source: " + source,
                                             w_in=round(float(w_in), 2), h_in=round(float(h_in), 2))
    text = "\n".join(textwrap.wrap("Source: " + source, 165))
    n = text.count("\n") + 1
    fig.text(0.015, 0.015, text, fontsize=FS["source"], color=MUTED, va="bottom", ha="left", linespacing=1.3)
    bottom = bottom if bottom is not None else (0.55 + 0.21 * n + (0.3 if xlab else 0)) / H
    fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, **adj)
    SL.mkdir(parents=True, exist_ok=True)
    fig.savefig(SL / name, dpi=DPI)
    plt.close(fig)
    print(f"Saved output/slides/{name}")


# --------------------------------------------------------------------------- slide 6: net, two zones
def s01_net(reg):
    tb, am = D.TREATED_ZONE, "amarakaeri_bz"
    net = _w("net").loc[2010:2025]
    yrs = list(net.index)
    m = {u: {p: _add(reg, f"sl_net_{u}_{p}", _pm(u, "net", p), "ha/yr",
                     f"Net mining additions, {D.UNIT_NAME[u]}, {PSHORT[p]}: mean per year (slide 6)", "net", u, PSHORT[p],
                     check=f"{u}_{p}_net") for p in (PRE, DUR, LATER)} for u in (tb, am)}
    fall = _add(reg, "sl_net_tambopata_bz_fall_share", 1 - m[tb][DUR] / m[tb][PRE], "share",
                "Fall in mean net mining additions, Tambopata buffer zone, 2016–18 to 2019–21 (slide 6)", "net", tb,
                f"{PSHORT[PRE]} vs {PSHORT[DUR]}")
    fig, ax = _fig()
    _band(ax, DUR)
    ax.axhline(0, color=AXIS, lw=1)
    for u, col, nm in ((am, C["buffer"], "Amarakaeri\nbuffer zone"), (tb, C["lapampa"], "Tambopata\nbuffer zone")):
        s = net[u]
        ax.plot(yrs, s, "-", color=col, lw=3, zorder=3)
        ax.plot(yrs, s, "o", color=col, ms=7.5, mec="white", mew=1.4, zorder=4)
        for p in (PRE, DUR, LATER):
            a, b = D.PERIODS[p]
            ax.plot([a - 0.42, b + 0.42], [m[u][p]] * 2, color=col, lw=8, alpha=0.38, solid_capstyle="butt", zorder=2)
        _label(ax, 2025, s.loc[2025], nm, dx=12, fs=FS["small"])
    for p in (PRE, DUR, LATER):                     # period means as a two-row strip at the top of the plot
        a, b = D.PERIODS[p]
        xc = (a + b) / 2
        for row, (u, col) in enumerate(((tb, C["lapampa"]), (am, C["buffer"]))):
            yf = 0.965 - 0.085 * row
            ax.plot([xc - 0.62], [yf], "s", ms=10, color=col, transform=ax.get_xaxis_transform(), clip_on=False, zorder=7)
            ax.text(xc - 0.42, yf, _fmt(m[u][p]), transform=ax.get_xaxis_transform(), ha="left", va="center",
                    fontsize=FS["body"], color=INK if row == 0 else INK2, fontweight="bold")
    ax.set_xlim(2009.4, 2025.6)
    lo = min(net[[tb, am]].min().min(), 0)
    ax.set_ylim(lo * 1.25 - 150, net[[tb, am]].max().max() * 1.42)
    _fmt_y(ax); _ticks(ax, yrs); _events(ax)
    ax.set_ylabel("ha/yr", fontsize=FS["small"], color=INK2)
    _head(fig, f"Net additions in the Tambopata buffer zone fell {fall:.0%} in 2019–21",
          f"Net mining additions, ha/yr · Tambopata buffer zone (orange) vs Amarakaeri buffer zone (green) · 2010–2025 · "
          f"Tambopata {_fmt(m[tb][PRE])} → {_fmt(m[tb][DUR])}, Amarakaeri {_fmt(m[am][PRE])} → {_fmt(m[am][DUR])} "
          f"(2016–18 → 2019–21). Thick bars and numbers at the top: period means.")
    _save(fig, "slide_01_net_two_zones.png", f"{SRC} Both buffer zones whole (official SERNANP polygons). {NO_SEE}",
          top=0.86, right=0.88)


# --------------------------------------------------------------------------- slide 7: parts, small multiples
def s02_parts(reg):
    units = [(D.TREATED_ZONE, "Tambopata buffer zone (targeted)"), ("amarakaeri_bz", "Amarakaeri buffer zone (less treated)")]
    vals = {}
    for u, _ in units:
        for p in (PRE, DUR, LATER):
            for mm in ["net"] + D.PARTS:
                vals[(u, p, mm)] = _add(reg, f"sl_parts_{u}_{p}_{mm}", _pm(u, mm, p), "ha/yr",
                                        f"{D.MEASURE_NAME[mm]}, {D.UNIT_NAME[u]}, {PSHORT[p]}: mean per year (slide 7)",
                                        mm, u, PSHORT[p], check=f"{u}_{p}_{mm}")
    tb = D.TREATED_ZONE
    fall = vals[(tb, PRE, "net")] - vals[(tb, DUR, "net")]
    sh_stop = _add(reg, "sl_fall_share_stopped", (vals[(tb, DUR, "stopped")] - vals[(tb, PRE, "stopped")]) / fall, "share",
                   "Share of the fall in net additions, Tambopata buffer zone, 2016–18 to 2019–21, from more stopped land "
                   "(slide 7)", "stopped", tb, f"{PSHORT[PRE]} vs {PSHORT[DUR]}", check="tambopata_bz_fall_share_stopped", tol=1e-6)
    sh_new = _add(reg, "sl_fall_share_new", (vals[(tb, PRE, "new")] - vals[(tb, DUR, "new")]) / fall, "share",
                  "Share of the fall in net additions, Tambopata buffer zone, 2016–18 to 2019–21, from less new land "
                  "(slide 7)", "new", tb, f"{PSHORT[PRE]} vs {PSHORT[DUR]}", check="tambopata_bz_fall_share_new", tol=1e-6)
    new_ratio = vals[(tb, DUR, "new")] / vals[(tb, PRE, "new")]
    stop_ratio = vals[(tb, DUR, "stopped")] / vals[(tb, PRE, "stopped")]
    fig, axes = _fig(1, 2, sharey=True, gridspec_kw={"wspace": 0.08})
    x = np.arange(3)
    for ax, (u, ttl) in zip(axes, units):
        new = [vals[(u, p, "new")] for p in (PRE, DUR, LATER)]
        rem = [vals[(u, p, "remined")] for p in (PRE, DUR, LATER)]
        stp = [vals[(u, p, "stopped")] for p in (PRE, DUR, LATER)]
        net = [vals[(u, p, "net")] for p in (PRE, DUR, LATER)]
        ax.axvspan(0.5, 1.5, color=BAND, zorder=-1, lw=0)
        xb, xn = x - 0.1, x + 0.27                      # parts bar, and the net bar beside it (never on top)
        _parts_bars(ax, xb, new, rem, stp, width=0.5)
        ax.bar(xn, net, width=0.12, color=INK, lw=0, zorder=4)
        for i in range(3):
            ax.annotate(f"net\n{_fmt(net[i])}", xy=(xn[i], max(net[i], 0)), xytext=(0, 5), textcoords="offset points",
                        ha="center", va="bottom", fontsize=FS["small"], color=INK, fontweight="bold", zorder=7,
                        linespacing=1.0)
            ax.annotate(_fmt(new[i]), xy=(xb[i], new[i] / 2), ha="center", va="center", fontsize=FS["small"] - 1,
                        color="white", fontweight="bold", zorder=7)
            ax.annotate(_fmt(stp[i]), xy=(xb[i], -stp[i] / 2), ha="center", va="center", fontsize=FS["small"] - 1,
                        color="white", fontweight="bold", zorder=7)
            if rem[i] > 250:
                ax.annotate(_fmt(rem[i]), xy=(xb[i], new[i] + rem[i] / 2), ha="center", va="center",
                            fontsize=FS["small"] - 1, color=INK, fontweight="bold", zorder=7)
        ax.set_xticks(x); ax.set_xticklabels([PNAME[p] for p in (PRE, DUR, LATER)], fontsize=FS["small"])
        ax.set_xlim(-0.5, 2.5)
        ax.set_title(ttl, loc="left", fontsize=FS["label"] + 1, color=INK, pad=10, fontweight="medium")
        _fmt_y(ax)
        ax.tick_params(axis="x", length=0)
    axes[0].set_ylabel("ha/yr (period mean)", fontsize=FS["small"], color=INK2)
    lo, hi = axes[0].get_ylim(); axes[0].set_ylim(lo * 1.08, hi * 1.28)
    _parts_legend(axes[1], loc="upper right", ncol=2, net_bar=True)
    word = "halved" if 0.4 <= new_ratio <= 0.6 else f"fell {1 - new_ratio:.0%}"
    so_lo, so_hi = reg.get("tambopata_bz_stopped_share_of_fall_min"), reg.get("tambopata_bz_stopped_share_of_fall_max")
    so_19 = reg.get("tambopata_bz_excess_stopped_share_in_2019")
    for k, v, d in (("lo", so_lo, "lowest"), ("hi", so_hi, "highest")):
        _add(reg, f"sl_stopped_share_of_fall_{k}", v, "share", f"Share of the 2016–18 to 2019–21 fall in net additions, "
             f"Tambopata buffer zone, that is more stopped land: {d} of the variants (raw, excluding land back within 2 "
             "years, excess rate, DiD) (slide 7)", "stopped", tb, f"{PSHORT[PRE]} vs {PSHORT[DUR]}",
             check=f"tambopata_bz_stopped_share_of_fall_{'min' if k == 'lo' else 'max'}", tol=1e-9)
    _add(reg, "sl_excess_stopped_share_in_2019", so_19, "share", "Share of the 2019–21 excess stopped land (vs 2016–18) "
         "that falls in 2019, Tambopata buffer zone (slide 7)", "stopped", tb, "2019", check="tambopata_bz_excess_stopped_share_in_2019",
         tol=1e-9)
    _head(fig, f"Pits going out of use made {so_lo:.0%}–{so_hi:.0%} of the fall, most of it in 2019",
          f"Net mining additions and their parts, ha/yr, period means · Tambopata buffer zone vs Amarakaeri buffer zone · "
          f"Tambopata 2016–18 → 2019–21: new land {_fmt(vals[(tb, PRE, 'new')])} → {_fmt(vals[(tb, DUR, 'new')])}, "
          f"stopped {_fmt(vals[(tb, PRE, 'stopped')])} → {_fmt(vals[(tb, DUR, 'stopped')])} ({stop_ratio:.1f}×). "
          f"Stopped land makes {so_lo:.0%}–{so_hi:.0%} of the fall (four ways of counting map flicker); "
          f"{so_19:.0%} of the extra stopping is in 2019.")
    _save(fig, "slide_02_parts_two_zones.png", f"{SRC} {PARTS_NOTE} Net = new + re-mined − stopped. {NO_SEE}",
          top=0.90, left=0.075, right=0.985)


# --------------------------------------------------------------------------- slide 8: La Pampa, yearly parts
def s03_lapampa_2019(reg):
    u = "lapampa"
    y0, y1 = D.PERIODS[PRE][0], D.PERIODS[LATER][0]
    yrs = list(range(y0, y1 + 1))
    P = {mm: _w(mm)[u].loc[y0:y1] for mm in ["net"] + D.PARTS}
    for y in (D.REF_YEAR, D.FIRST_POST):
        for mm in ["net"] + D.PARTS:
            _add(reg, f"sl_lapampa_{y}_{mm}", P[mm].loc[y], "ha/yr", f"{D.MEASURE_NAME[mm]}, La Pampa sector, {y} (slide 8)",
                 mm, u, str(y), check=f"lapampa_{y}_{mm}")
    fig, ax = _fig()
    _band(ax, DUR)
    _parts_bars(ax, yrs, P["new"].values, P["remined"].values, P["stopped"].values, width=0.62)
    _net_line(ax, yrs, P["net"].values)
    r, f = D.REF_YEAR, D.FIRST_POST
    hi = (P["new"] + P["remined"]).max()
    ax.set_xlim(y0 - 0.6, y1 + 0.6); ax.set_ylim(-P["stopped"].max() * 1.45, hi * 1.32)
    _label(ax, r, P["new"].loc[r] + P["remined"].loc[r], f"new {_fmt(P['new'].loc[r])}", dx=0, dy=8, ha="center",
           va="bottom", fs=FS["small"])
    _label(ax, f, P["new"].loc[f] + P["remined"].loc[f], f"new {_fmt(P['new'].loc[f])}", dx=0, dy=8, ha="center",
           va="bottom", fs=FS["small"])
    _label(ax, f, -P["stopped"].loc[f], f"stopped {_fmt(P['stopped'].loc[f])}", dx=0, dy=-8, ha="center", va="top",
           fs=FS["small"])
    for yy in (r, f):                                    # net labels under the dot, boxed so they read on the bars
        ax.annotate(f"net {_fmt(P['net'].loc[yy])}", xy=(yy, P["net"].loc[yy]), xytext=(0, -16), textcoords="offset points",
                    ha="center", va="top", fontsize=FS["small"], color=INK, fontweight="bold", zorder=8,
                    bbox=dict(boxstyle="round,pad=0.2", fc=SURFACE, ec="none", alpha=0.95))
    _fmt_y(ax); _ticks(ax, yrs); _events(ax, keep={"Mercurio", "COVID", "Restauración"})
    ax.set_ylabel("ha/yr", fontsize=FS["small"], color=INK2)
    _parts_legend(ax, loc="upper right", ncol=2)
    _head(fig, "New pits kept opening in 2019; pits stopped where the patrols were",
          f"Net mining additions and their parts, ha/yr · La Pampa sector (the target) · {y0}–{y1} · "
          f"2019: new land {_fmt(P['new'].loc[f])} (2018: {_fmt(P['new'].loc[r])}), stopped {_fmt(P['stopped'].loc[f])}, "
          f"net {_fmt(P['net'].loc[f])}. Shaded: 2019–21.")
    _save(fig, "slide_03_lapampa_parts.png", f"{SRC} {PARTS_NOTE} {NO_SEE}", top=0.86, right=0.98)


# --------------------------------------------------------------------------- slide 9: across the road + department
def s04_moved(reg):
    u = "corridor_across"
    yrs = list(range(2010, 2026))
    P = {mm: _w(mm)[u].loc[yrs] for mm in ["net"] + D.PARTS}
    across = {p: _add(reg, f"sl_across_{p}_net", _pm(u, "net", p), "ha/yr",
                      f"Net mining additions, corridor across the road, {PSHORT[p]}: mean per year (slide 9)", "net", u,
                      PSHORT[p], check=f"corridor_across_{p}_net") for p in (PRE, DUR, LATER)}
    mdd = {p: _add(reg, f"sl_mdd_{p}_net", _pm("mdd", "net", p), "ha/yr",
                   f"Net mining additions, Madre de Dios (department), {PSHORT[p]}: mean per year (slide 9)", "net", "mdd",
                   PSHORT[p], check=f"mdd_{p}_net") for p in (PRE, DUR, LATER)}
    # department by area (zones inside Madre de Dios; they sum to the department)
    z = Z._zone_year()
    z = z[z.in_mdd == 1]
    grp = {"lapampa": "tbz", "tambopata_bz_rest": "tbz", "corridor_across": "cor", "corridor_rest": "cor"}
    g = z.assign(g=z.zone.map(grp).fillna("other")).groupby(["year", "g"]).net_ha.sum().unstack().fillna(0)
    gm = {p: {k: Z.period_mean(g[k], p) for k in ("tbz", "cor", "other")} for p in (PRE, DUR, LATER)}
    for p in (PRE, DUR, LATER):
        assert abs(sum(gm[p].values()) - mdd[p]) < 1.0
        _add(reg, f"sl_mdd_corridor_outside_bz_{p}_net", gm[p]["cor"], "ha/yr",
             f"Net mining additions, mining corridor outside buffer zones (inside Madre de Dios), {PSHORT[p]}: mean per year "
             "(slide 9)", "net", "corridor_outside_bz", PSHORT[p])
    fig, (a1, a2) = _fig(1, 2, gridspec_kw={"width_ratios": [1.35, 1], "wspace": 0.22})
    _band(a1, DUR)
    _parts_bars(a1, yrs, P["new"].values, P["remined"].values, P["stopped"].values, width=0.66)
    _net_line(a1, yrs, P["net"].values, ms=6.5)
    a1.set_xlim(yrs[0] - 0.6, yrs[-1] + 0.6)
    lo, hi = a1.get_ylim(); a1.set_ylim(lo * 1.1, hi * 1.45)
    _fmt_y(a1); _ticks(a1, yrs, step=3)
    a1.set_title("Corridor across the road (D.L. 1100)", loc="left", fontsize=FS["label"] + 1, color=INK, pad=10, fontweight="medium")
    a1.set_ylabel("ha/yr", fontsize=FS["small"], color=INK2)
    _parts_legend(a1, loc="upper left", ncol=2)
    a1.text(0.02, 0.72, f"Mean net: {PSHORT[PRE]} {_fmt(across[PRE])}/yr → {PSHORT[DUR]} {_fmt(across[DUR])}/yr",
            transform=a1.transAxes, ha="left", va="top", fontsize=FS["small"], color=INK, fontweight="bold", zorder=8,
            bbox=dict(boxstyle="round,pad=0.25", fc=SURFACE, ec="none", alpha=0.95))
    x = np.arange(3); bot = np.zeros(3)
    for k, col, lab in (("tbz", C["lapampa"], "Tambopata buffer zone"), ("cor", C["corridor"], "Mining corridor\n(outside buffer zones)"),
                        ("other", C["other"], "Rest of the department")):
        v = np.array([gm[p][k] for p in (PRE, DUR, LATER)])
        pos = np.clip(v, 0, None)
        a2.bar(x, pos, bottom=bot, width=0.58, color=col, lw=0, zorder=2)
        a2.bar(x, np.zeros(3), bottom=bot + pos, width=0.58, color=SURFACE, edgecolor=SURFACE, lw=1.5, zorder=3)
        _label(a2, 2.32, bot[-1] + pos[-1] / 2, lab, dx=8, fs=FS["small"] - 1, weight="normal")
        bot = bot + pos
    for i, p in enumerate((PRE, DUR, LATER)):
        a2.annotate(_fmt(mdd[p]), xy=(i, bot[i]), xytext=(0, 6), textcoords="offset points", ha="center", va="bottom",
                    fontsize=FS["body"], color=INK, fontweight="bold")
    a2.set_xticks(x); a2.set_xticklabels([PSHORT[p] for p in (PRE, DUR, LATER)], fontsize=FS["small"])
    a2.tick_params(axis="x", length=0)
    a2.set_xlim(-0.5, 2.5); a2.set_ylim(0, bot.max() * 1.15)
    _fmt_y(a2)
    a2.set_title("All of Madre de Dios, by area (period means)", loc="left", fontsize=FS["label"] + 1, color=INK, pad=10,
                 fontweight="medium")
    neg = {p: k for p in (PRE, DUR, LATER) for k in ("tbz", "cor", "other") if gm[p][k] < 0}
    _head(fig, "Mining moved across the road; the department never fell",
          f"Net mining additions (and parts), ha/yr · left: corridor across the road, 2010–2025, "
          f"{_fmt(across[PRE])} → {_fmt(across[DUR])} (2016–18 → 2019–21) · right: Madre de Dios "
          f"{_fmt(mdd[PRE])} → {_fmt(mdd[DUR])} → {_fmt(mdd[LATER])} (2016–18 → 2019–21 → 2022–25).")
    _save(fig, "slide_04_moved.png", f"{SRC} Right: zones inside the department; they sum to the total. "
          f"Legality is by location; the map class can't tell legal from illegal. {NO_SEE}",
          top=0.89, left=0.065, right=0.86)
    return neg


# --------------------------------------------------------------------------- slide 10: it came back on old pits
def s05_later(reg):
    u = D.TREATED_ZONE
    yrs = list(range(2010, 2026))
    P = {mm: _w(mm)[u].loc[yrs] for mm in ["net"] + D.PARTS}
    later = {mm: _add(reg, f"sl_later_{mm}", _pm(u, mm, LATER), "ha/yr",
                      f"{D.MEASURE_NAME[mm]}, Tambopata buffer zone, {PSHORT[LATER]}: mean per year (slide 10)", mm, u,
                      PSHORT[LATER], check=f"tambopata_bz_later_{mm}") for mm in ["net"] + D.PARTS}
    ex = {mm: _add(reg, f"sl_later_ex2023_{mm}", _later_ex(u, mm), "ha/yr",
                   f"{D.MEASURE_NAME[mm]}, Tambopata buffer zone, 2022, 2024, 2025 (without 2023): mean per year (slide 10)",
                   mm, u, "2022, 2024, 2025", check=f"tambopata_bz_later_ex2023_{mm}") for mm in ["net", "new", "remined"]}
    sh = _add(reg, "sl_later_remined_share", later["remined"] / (later["new"] + later["remined"]), "share",
              "Re-mined land as a share of land added (new + re-mined), Tambopata buffer zone, 2022–25 (slide 10)",
              "remined", u, PSHORT[LATER])
    sh_ex = _add(reg, "sl_later_ex2023_remined_share", ex["remined"] / (ex["new"] + ex["remined"]), "share",
                 "Re-mined land as a share of land added (new + re-mined), Tambopata buffer zone, 2022, 2024, 2025 (slide 10)",
                 "remined", u, "2022, 2024, 2025")
    fig, ax = _fig()
    a, b = D.PERIODS[LATER]
    ax.axvspan(a - 0.5, b + 0.5, color=BAND, zorder=-1, lw=0)
    _parts_bars(ax, yrs, P["new"].values, P["remined"].values, P["stopped"].values, width=0.66)
    _net_line(ax, yrs, P["net"].values, ms=7)
    ax.set_xlim(yrs[0] - 0.6, yrs[-1] + 0.6)
    lo, hi = ax.get_ylim(); ax.set_ylim(lo * 1.45, hi * 1.25)
    ax.text((a + b) / 2, 0.03, f"Later years: net {_fmt(later['net'])}/yr\n({_fmt(ex['net'])} without 2023)",
            transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=FS["small"], color=INK, fontweight="bold")
    y23 = D.LATER_EX
    _label(ax, y23, P["new"].loc[y23] + P["remined"].loc[y23], f"2023: re-mined {_fmt(P['remined'].loc[y23])} ha",
           dx=0, dy=6, fs=FS["small"], ha="center", va="bottom")
    _fmt_y(ax); _ticks(ax, yrs); _events(ax)
    ax.set_ylabel("ha/yr", fontsize=FS["small"], color=INK2)
    _parts_legend(ax, loc="upper left", ncol=4)
    _head(fig, f"It came back on old pits: {sh:.0%} of added land was re-mined",
          f"Net mining additions and their parts, ha/yr · Tambopata buffer zone · 2010–2025 · later years (2022–25): "
          f"re-mined {_fmt(later['remined'])}/yr, new land {_fmt(later['new'])}/yr; without the 2023 spike year "
          f"re-mined {_fmt(ex['remined'])}/yr ({sh_ex:.0%}).")
    _save(fig, "slide_05_later_old_pits.png", f"{SRC} {PARTS_NOTE} 2023 is a MapBiomas-only spike (GLAD alerts and "
          f"Amazon Mining Watch are flat): read 2022–25 with and without it. MAAP #193 (2023) reports miners back on "
          f"degraded land. {NO_SEE}", top=0.86, right=0.98)


# --------------------------------------------------------------------------- slide 11: inside the reserve
def s06_reserve(reg):
    u = "tambopata_nr"
    yrs = list(range(2011, 2026))
    s = _w("net")[u].loc[yrs]
    stock = _w("stock")[u]
    v25 = _add(reg, "sl_reserve_2025_net", s.loc[2025], "ha/yr", "Net mining additions, Tambopata National Reserve, 2025 "
               "(slide 11)", "net", u, "2025", check="tambopata_nr_2025_net")
    v17 = _add(reg, "sl_reserve_2017_net", s.loc[2017], "ha/yr", "Net mining additions, Tambopata National Reserve, 2017 "
               "(slide 11)", "net", u, "2017", check="tambopata_nr_2017_net")
    st = _add(reg, "sl_reserve_2025_stock", stock.loc[2025], "ha", "Mining area (stock), Tambopata National Reserve, 2025 "
              "(slide 11)", "stock", u, "2025", check="tambopata_nr_stock_2025")
    dur = _add(reg, "sl_reserve_during_net", _pm(u, "net", DUR), "ha/yr", "Net mining additions, Tambopata National "
               "Reserve, 2019–21: mean per year (slide 11)", "net", u, PSHORT[DUR], check="tambopata_nr_during_net")
    fig, ax = _fig()
    _band(ax, DUR)
    ax.axhline(0, color=INK2, lw=1)
    cols = [C["reserve"] if y == 2025 else "#b9cdb2" for y in yrs]
    ax.bar(yrs, s.values, color=cols, width=0.7, zorder=2)
    _label(ax, 2025, s.loc[2025], f"+{_fmt(v25)} ha\nin 2025", dx=0, dy=8, ha="center", va="bottom")
    _label(ax, 2016.6, s.loc[2017], f"+{_fmt(v17)} ha in 2017:\nan earlier jump", dx=-8, dy=-4, va="top",
           ha="right", fs=FS["small"], weight="normal")
    ax.set_xlim(yrs[0] - 0.6, yrs[-1] + 0.6); ax.set_ylim(min(-80, s.min() * 1.4), max(s.max(), v25) * 1.25)
    _fmt_y(ax); _ticks(ax, yrs); _events(ax)
    ax.set_ylabel("ha/yr", fontsize=FS["small"], color=INK2)
    _head(fig, f"2025: mining inside the reserve jumped {_fmt(v25)} ha after the navy left",
          f"Net mining additions, ha/yr · Tambopata National Reserve (inside the reserve, not the buffer zone) · 2011–2025 · "
          f"2019–21 mean {_fmt(dur)}/yr; mining area 2025: {_fmt(st)} ha. Navy left the Malinowski River posts in 2025 "
          f"(MAAP #241, 2026).")
    _save(fig, "slide_06_reserve.png", f"{SRC} Platform check: 777 ha of mining inside the reserve in 2025 (protected-area "
          f"statistics). MAAP #241 (Pacsi et al., 2026) reports ~500 ha inside the reserve, late 2025 to Feb 2026. {NO_SEE}",
          top=0.86, right=0.96)


# --------------------------------------------------------------------------- slide 12: estimates with parts + ranks
def s07_causal(reg):
    tb = D.TREATED_ZONE
    g = reg.get
    rows = [("2×2 vs Amarakaeri\n(2014–18 base)", "did_base2014"), ("Zone + year effects\n(M1, 15 zones)", "model_m1_during"),
            ("Synthetic DiD\n(15 zones, net only)", "sdid_sdid_ha_during")]
    est = {}
    for lab, k in rows:
        est[k] = {mm: g(f"{k}_{mm}") for mm in ["net"] + D.PARTS if f"{k}_{mm}" in reg.rows}
        for mm, v in est[k].items():
            _add(reg, f"sl_est_{k}_{mm}", v, "ha/yr", f"{D.MEASURE_NAME[mm]}, Tambopata buffer zone, 2019–21: estimate "
                 f"{k} (slide 12; conditional on the comparison zones showing the counterfactual)", mm, tb, PSHORT[DUR],
                 claim="causal", check=f"{k}_{mm}", tol=1e-6)
    lo_ = _add(reg, "sl_causal_range_lo", abs(g("model_m1_during_net")), "ha/yr", "Conditional causal range, low end: "
               "|M1 zone + year effects|, net additions, Tambopata buffer zone, 2019–21 (slide 12)", "net", tb, PSHORT[DUR],
               claim="causal")
    hi_ = _add(reg, "sl_causal_range_hi", abs(g("did_base2014_net")), "ha/yr", "Conditional causal range, high end: "
               "|2×2 vs Amarakaeri, 2014–18 base|, net additions, Tambopata buffer zone, 2019–21 (slide 12)", "net", tb,
               PSHORT[DUR], claim="causal")
    stop_sh = {k: est[k]["stopped"] / -est[k]["net"] for k in ("did_base2014", "model_m1_during")}
    _add(reg, "sl_causal_stopped_share_m1", stop_sh["model_m1_during"], "share", "Share of the M1 estimate (net, 2019–21) "
         "that is more stopped land (slide 12)", "stopped", tb, PSHORT[DUR], claim="causal")
    _add(reg, "sl_causal_stopped_share_2x2", stop_sh["did_base2014"], "share", "Share of the 2×2 estimate (2014–18 base, "
         "net, 2019–21) that is more stopped land (slide 12)", "stopped", tb, PSHORT[DUR], claim="causal")
    scaled = {k: int(g(k)) for k in ("model_m4_rank", "model_m1_rank_scaled", "sdid_sdid_scaled_during_rank",
                                     "placebo_space_rank_scaled")}
    n_raw, n_sc = int(g("model_m1_n")), int(g("model_m4_n"))
    r_raw, r14, r15 = int(g("model_m1_rank")), int(g("placebo_space_rank_raw_preyear_2014")), int(g("placebo_space_rank_raw_preyear_2015"))
    sc_lo, sc_hi = min(scaled.values()), max(scaled.values())
    _add(reg, "sl_rank_scaled_lo", sc_lo, "rank", "Best size-relative placebo rank of the Tambopata buffer zone across "
         "M1, M4, SDID and the event study (slide 12)", "rank", tb, PSHORT[DUR])
    _add(reg, "sl_rank_scaled_hi", sc_hi, "rank", "Worst size-relative placebo rank of the Tambopata buffer zone across "
         "M1, M4, SDID and the event study (slide 12)", "rank", tb, PSHORT[DUR])

    fig, (a1, a2) = _fig(1, 2, gridspec_kw={"width_ratios": [1.55, 1], "wspace": 0.12})
    yy = np.arange(len(rows))[::-1]
    a1.axvspan(-hi_, -lo_, color="#f1d9c8", lw=0, zorder=0)
    a1.text(-(hi_ + lo_) / 2, len(rows) - 0.42, f"conditional range\n{_fmt(lo_)}–{_fmt(hi_)} ha/yr", ha="center",
            va="bottom", fontsize=FS["small"], color=INK, fontweight="bold")
    a1.axvline(0, color=INK2, lw=1.4)
    h = 0.22
    for yv, (lab, k) in zip(yy, rows):
        e = est[k]
        if "new" in e:
            parts = [("new", e["new"], 0.0), ("remined", e["remined"], 0.0), ("stopped", -e["stopped"], 0.0)]
            pos, neg = 0.0, 0.0
            for mm, v, _ in parts:
                left = pos if v >= 0 else neg + v
                a1.barh(yv - 0.08, v, left=pos if v >= 0 else neg, height=h * 1.6, color=PART_COL[mm], lw=0, zorder=2)
                a1.barh(yv - 0.08, 0, left=(pos + v) if v >= 0 else (neg + v), height=h * 1.6, edgecolor=SURFACE, lw=1.5, zorder=3)
                if v >= 0:
                    pos += v
                else:
                    neg += v
            a1.annotate(f"−{_fmt(e['stopped'])} stopped", xy=(neg, yv - 0.08), xytext=(-6, 0), textcoords="offset points",
                        ha="right", va="center", fontsize=FS["small"] - 1, color=INK2)
        a1.plot(e["net"], yv + 0.27, "D", ms=11, color=INK, mec="white", mew=1.5, zorder=5)
        a1.annotate(_fmt(e["net"]), xy=(e["net"], yv + 0.27), xytext=(12, 0), textcoords="offset points", ha="left",
                    va="center", fontsize=FS["body"], color=INK, fontweight="bold")
    a1.set_yticks(yy); a1.set_yticklabels([r[0] for r in rows], fontsize=FS["small"])
    style_axes(a1, fmt=False); a1.yaxis.grid(False); a1.xaxis.grid(True, color=GRID, lw=0.6)
    a1.xaxis.set_major_formatter(FuncFormatter(lambda x, p: _fmt(x)))
    a1.set_xlim(-2650, 700); a1.set_ylim(-0.6, len(rows) + 0.35)
    a1.tick_params(axis="x", labelsize=FS["small"])
    a1.set_xlabel("Estimated change, Tambopata buffer zone, 2019–21, ha/yr (◆ net; bars = parts)", fontsize=FS["small"], color=INK2)
    h_ = [Patch(color=C["new"], label="New land"), Patch(color=C["remined"], label="Re-mined"),
          Patch(color=C["stopped"], label="More stopped (−)"), Line2D([], [], color=INK, marker="D", ls="", ms=9, label="Net")]
    a1.legend(handles=h_, loc="lower left", ncol=4, fontsize=FS["small"] - 1, frameon=False, handlelength=1.0,
              columnspacing=1.0, bbox_to_anchor=(-0.02, -0.02))

    # right: ranks, raw vs scaled
    a2.set_xlim(0, 16.5); a2.set_ylim(-0.6, 3.6); a2.axis("off")
    ladder = [("In hectares, 2019–21", n_raw, {r_raw}, f"{r_raw} of {n_raw}"),
              ("In hectares, 2014 (before)", n_raw, {r14}, f"{r14} of {n_raw}: size"),
              ("Scaled to own size, 2019–21", n_sc, set(range(sc_lo, sc_hi + 1)), f"{sc_lo}–{sc_hi} of {n_sc}")]
    for i, (lab, n, hit, txt) in enumerate(ladder):
        y = 3 - i * 1.25
        a2.text(0.3, y + 0.42, lab, fontsize=FS["small"], color=INK, fontweight="bold", va="bottom")
        a2.text(16.3, y + 0.42, txt, fontsize=FS["small"], color=C["lapampa"] if i != 1 else INK2, fontweight="bold",
                va="bottom", ha="right")
        for k in range(1, n + 1):
            on = k in hit
            a2.plot(k, y, "o", ms=13 if on else 10, color=C["lapampa"] if on else "#d3d1cb",
                    mec="white", mew=1.2, alpha=1 if (on and i != 1) else (0.55 if on else 1))
        a2.text(0.45, y, "1", fontsize=FS["small"] - 2, color=MUTED, ha="right", va="center")
    a2.text(0.3, -0.55, "1 = biggest fall. Raw rank 1 also before 2019: it ranks\nsize as much as effect. Not a significance test.",
            fontsize=FS["small"] - 1, color=INK2, va="bottom", linespacing=1.3)
    _head(fig, "Did Mercurio cause the fall? Only conditionally, in hectares only",
          f"Estimated change in net mining additions and its parts, ha/yr · Tambopata buffer zone · 2019–21 vs before · "
          f"causal only if the comparison zones show what Tambopata would have done; upper bound (spillovers, peak at "
          f"targeting); coincides with COVID. Right: placebo ranks.")
    _save(fig, "slide_07_causal.png", "MapBiomas Peru Collection 4 rasters, national buffer-zone panel on the v3 registry "
          "(15 zones with pre-2019 mining; scaled ranks: 7 zones above 10 ha/yr). 2×2 = Tambopata minus Amarakaeri, "
          "2019–21 vs 2014–18; M1 = zone + year effects 2014–25; synthetic DiD = own weights (peru_sdid.py, net only). "
          "Parts add up to net for the linear estimators.", top=0.90, left=0.15, right=0.985, xlab=True)


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
            ax.text(i, 1.03, f"{back:.0%}", ha="center", va="bottom", fontsize=FS["small"], color=INK, fontweight="bold")
            ax.text(i, -0.06, f"{_fmt(tot[i])}", ha="center", va="top", fontsize=FS["small"] - 2, color=INK2)
        ax.set_xticks(x); ax.set_xticklabels([PSHORT[p] for p in (PRE, DUR, LATER)], fontsize=FS["small"] - 1)
        ax.tick_params(axis="x", pad=26, length=0)
        ax.set_title(ttl, loc="left", fontsize=FS["label"], color=INK, pad=44, fontweight="medium")
        ax.set_ylim(0, 1.0); _fmt_y(ax, pct=True); ax.set_xlim(-0.5, 2.5)
    axes[0].text(-0.5, 1.115, "back within 2 yrs ↓", fontsize=FS["small"] - 2, color=INK2, transform=axes[0].get_xaxis_transform())
    axes[0].set_ylabel("share of stopped land", fontsize=FS["small"], color=INK2)
    axes[-1].legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=FS["small"] - 1, frameon=False, handlelength=1.0)
    _head(fig, "Stopped land: often water, often mined again within 2 years",
          "Stopped land (left the mining class), share by what it became and share mining again within 2 years, "
          "period means · four zones · 2016–18, 2019–21, 2022–25 (small numbers under the bars: stopped ha/yr). Numbers on top: share mining again within 2 years.")
    _save(fig, "slide_b1_stopped_split.png", f"{SRC} Back within 2 years = classifier flicker or re-entry; the last two "
          "years cannot be followed up. No image validation sample (plan v3, V3-5).", top=0.80, left=0.06, right=0.865, xlab=True)


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
    a1.set_title("Before: mining area (stock), index 2018 = 100", loc="left", fontsize=FS["label"], color=INK, pad=10)
    order = [ct.TU] + ids
    a2.barh(range(len(order))[::-1], [pace[k] for k in order], color=[sd["color"][k] for k in order], height=0.6)
    for i, k in zip(range(len(order))[::-1], order):
        _label(a2, pace[k], i, f"{pace[k]:.0f}%", dx=6, fs=FS["body"])
    a2.set_yticks(range(len(order))[::-1]); a2.set_yticklabels([sd["short"][k] for k in order], fontsize=FS["small"])
    style_axes(a2, ygrid=False, fmt=False); a2.set_xticks([]); a2.spines["bottom"].set_visible(False)
    a2.set_title("2019–21: AMW new area per year,\n% of own 2018 area", loc="left", fontsize=FS["label"], color=INK, pad=10)
    a2.set_xlim(0, max(pace.values()) * 1.3)
    p = sd["pretrend_p_max"]
    r_ex = reg.get("top3_ratio_excl_unverified") if "top3_ratio_excl_unverified" in reg.rows else ratio
    _head(fig, f"Twins: Tambopata at {ratio:.0%}–{r_ex:.0%} of their pace; trends differed before",
          f"Left: mining area (stock), index 2018 = 100, 2010–18 (pre-trends rejected, p {'< 0.001' if p < 0.001 else '≤ ' + format(p, '.3f')}). "
          "Right: Amazon Mining Watch new area 2019–21 per year, % of own 2018 area: a different measure, not net additions.")
    _save(fig, "slide_b2_twins.png", f"{sd['source_index']}; {sd['source_pace']}. Twins chosen by fixed rules (rule R*, "
          "control_select.py). Different collections: compared as indices, never subtracted.", top=0.82, left=0.2, right=0.97)


# --------------------------------------------------------------------------- backup: money and gold (context)
def b3_context(pack, reg):
    import v2_tests
    money = v2_tests.mef_series().loc[2015:2025] / 1e6
    gold = pack["prices"].set_index("year")["gold"].loc[2012:2025]
    lp = _w("net")["lapampa"].loc[2012:2025]
    ratio = gold.loc[2025] / gold.loc[D.REF_YEAR]
    _add(reg, "sl_gold_ratio_2025_2018", ratio, "ratio", "Gold price 2025 / 2018 (annual mean, nominal; backup slide)",
         "price", "world", "2018–2025", src=SRC_PRICE, check="gold_price_ratio_2025_2018", tol=1e-6)
    peak = int(money.idxmax()) if len(money) else D.FIRST_POST
    fig, axes = _fig(1, 3, gridspec_kw={"wspace": 0.32})
    a1, a2, a3 = axes
    for ax in axes:
        _band(ax, DUR)
    if len(money):
        a1.bar(money.index, money.values, color=C["buffer"], width=0.7, zorder=2)
        _label(a1, peak - 0.45, money.loc[peak], f"{money.loc[peak]:.0f} M\nin {peak}", dx=-8, dy=-2, fs=FS["small"], ha="right", va="top")
        a1.set_ylim(0, money.max() * 1.25)
    a2.plot(gold.index, gold.values, "-", color=C["gold"], lw=3)
    a2.plot(gold.index, gold.values, "o", color=C["gold"], ms=6, mec="white", mew=1.2)
    _label(a2, 2025, gold.loc[2025], f"${gold.loc[2025]:,.0f}", dx=0, dy=10, fs=FS["small"], ha="right", va="bottom")
    _label(a2, D.REF_YEAR, gold.loc[D.REF_YEAR], f"${gold.loc[D.REF_YEAR]:,.0f}", dx=0, dy=-12, fs=FS["small"], ha="center", va="top")
    a2.set_ylim(0, gold.max() * 1.2)
    a3.axhline(0, color=INK2, lw=1)
    a3.bar(lp.index, lp.values, color=[INK if v >= 0 else MUTED for v in lp.values], width=0.7, zorder=2)
    a3.set_ylim(min(lp.min() * 1.3, -100), lp.max() * 1.2)
    titles = ("Enforcement money,\nMadre de Dios (M soles)", "Gold price\n(US$ per ounce)", "La Pampa sector: net mining\nadditions (ha/yr)")
    for ax, t in zip(axes, titles):
        _fmt_y(ax); ax.set_xlim(2011.4, 2025.6)
        ax.set_xticks([2012, 2015, 2018, 2021, 2024]); ax.set_xticklabels(["2012", "'15", "'18", "'21", "'24"], fontsize=FS["tick"])
        ax.set_title(t, loc="left", fontsize=FS["label"] + 1, color=INK, pad=12, fontweight="medium")
        _events(ax, label=False)
    _head(fig, f"Enforcement money peaked in {peak} and faded; gold rose {ratio:.1f}-fold",
          "Same years in each panel · PP 0128 executed spending, Madre de Dios (lower bound) · gold price, nominal · "
          "net mining additions, La Pampa sector, ha/yr · 2012–2025. Shaded: 2019–21. Context, not a test.")
    _save(fig, "slide_b3_context.png", f"MEF Consulta Amigable, PP 0128 devengado, Madre de Dios; {SRC_PRICE}; {SRC} "
          "Correlation not shown: 11 years, and money follows mining.", top=0.78, left=0.06, right=0.98)


def run(pack, reg):
    print("\n== Slide figures (storyline v3: net additions + parts) ==")
    s01_net(reg)
    s02_parts(reg)
    s03_lapampa_2019(reg)
    s04_moved(reg)
    s05_later(reg)
    s06_reserve(reg)
    s07_causal(reg)
    b1_stopped_split(reg)
    b2_twins(reg)
    b3_context(pack, reg)
    for old in SL.glob("*.png"):                       # remove superseded v2 slide images
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
