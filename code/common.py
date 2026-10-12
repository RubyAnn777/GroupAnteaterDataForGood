"""Shared helpers: paths, loaders, additions, numbers registry, figure style, event markers.

All paths are resolved relative to this file, so `uv run python code/main.py` works from any cwd.
"""
from __future__ import annotations
import inspect
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")                      # no display needed
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"                       # the six pack tables (read-only)
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

# Keys used to identify a buffer zone (agent.md rule 3): name + protected-area category.
BZ_KEY = ["buffer_zone", "pa_category"]

# --------------------------------------------------------------------------- loaders
def load_pack() -> dict[str, pd.DataFrame]:
    """Load the six pack tables, exactly as the starter does."""
    return {
        "prices_m": pd.read_csv(DATA / "prices_monthly.csv"),
        "prices": pd.read_csv(DATA / "prices_annual.csv"),
        "substance": pd.read_csv(DATA / "mining_area.csv"),
        "br": pd.read_csv(DATA / "brazil_municipality_year.csv"),
        "pe": pd.read_csv(DATA / "peru_department_year.csv"),
        "zb": pd.read_csv(DATA / "peru_bufferzone_year.csv"),
    }

# --------------------------------------------------------------------------- additions
def additions(levels: pd.DataFrame, unit: str, value: str = "mining_ha", year: str = "year") -> pd.DataFrame:
    """addition(t) = level(t) - level(t-1) within a unit.

    `levels` MUST already have one row per unit-year (aggregate first, rule 2). We assert that
    and that years are consecutive, so a gap can never be differenced silently.
    """
    d = levels.sort_values([unit, year]).copy()
    assert not d.duplicated([unit, year]).any(), "aggregate to one row per unit-year before differencing"
    d["addition_ha"] = d.groupby(unit)[value].diff()
    gap = d.groupby(unit)[year].diff().dropna()
    assert (gap == 1).all(), "non-consecutive years"
    return d

def period_mean(adds: pd.Series, y0: int, y1: int) -> float:
    """Mean annual addition over years y0..y1 inclusive. `adds` is indexed by year."""
    s = adds.loc[y0:y1]
    assert len(s) == y1 - y0 + 1 and s.notna().all(), f"missing years in {y0}-{y1}"
    return float(s.mean())

# --------------------------------------------------------------------------- numbers registry
class Numbers:
    """Every number we might cite goes through add(). Written to output/numbers.csv.
    produced_by is the name of the calling function (taken automatically)."""
    COLS = ["id", "value", "unit", "description", "claim_type", "produced_by", "source_data"]
    CLAIMS = {"description", "prediction", "causal"}

    def __init__(self):
        self.rows: dict[str, dict] = {}

    def add(self, id: str, value: float, unit: str, description: str,
            claim_type: str, source_data: str):
        assert claim_type in self.CLAIMS, claim_type
        assert id not in self.rows, f"duplicate number id {id}"
        self.rows[id] = dict(id=id, value=float(value), unit=unit, description=description,
                             claim_type=claim_type, produced_by=inspect.stack()[1].function,
                             source_data=source_data)

    def get(self, id: str) -> float:
        return self.rows[id]["value"]

    def save(self, path: Path = OUT / "numbers.csv"):
        pd.DataFrame(self.rows.values(), columns=self.COLS).to_csv(path, index=False)
        print(f"Saved {path.relative_to(ROOT)} ({len(self.rows)} numbers)")

# --------------------------------------------------------------------------- figure style
# ONE visual system for every figure, in the colour world of the partner (FZS: burnt orange, steel blue,
# raspberry, forest green, mustard on warm off-white; Roboto). Checked with the dataviz skill's validate_palette.js
# (adjacent pairs pass CVD >= 8 on the light surface; tints are same-family companions and always carry direct labels).
# Colour follows the ENTITY, never its rank, and families encode meaning:
#   orange = Tambopata buffer zone / the target,  blue = legal mining corridor,  green = protected land,
#   raspberry = native communities,  violet = twins,  mustard = gold,  grey = rest / pools.
# Text is always ink/grey, never the series colour.
INK, INK2, MUTED = "#1f2d33", "#4f5b60", "#858d90"       # titles + values / subtitles + labels / ticks + sources
GRID, AXIS, SURFACE = "#e4e1da", "#c4c0b6", "#fbfaf7"    # hairline grid / baseline / figure background
C = dict(
    lapampa="#d0692f",        # La Pampa sector / Tambopata buffer zone (the target, treated)
    lapampa_tint="#eeb48f",   # rest of the Tambopata buffer zone
    corridor="#2b74a6",       # legal corridor across the road
    corridor_rest="#8db7d6",  # rest of the legal mining corridor
    native="#c4417a",         # native communities
    buffer="#4e9a3a",         # other buffer zones, Amarakaeri (the course comparison)
    buffer_tint="#a9d19a",    # other buffer zones when reserves are shown too
    reserve="#2f6e2a",        # reserves and parks (inside protected areas)
    twin="#6a5acd",           # rule-based / synthetic twins
    gold="#d4a12a",           # gold price, gold-bearing land
    other="#a9a8a2",          # rest / other / pools (deliberately grey: folds, not a series)
    brazil="#d0692f",         # Brazil treated territory (Yanomami): treated = orange, as in Peru
)
FONT_DIR = Path(__file__).resolve().parent / "fonts"     # Roboto (Apache 2.0), the face of the pages and of FZS

def _apply_style():
    from matplotlib import font_manager
    for f in sorted(FONT_DIR.glob("*.ttf")):
        font_manager.fontManager.addfont(str(f))
    plt.rcParams.update({
        "font.family": ["Roboto", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 9.5, "axes.titlesize": 10.5, "axes.titleweight": "medium", "axes.titlelocation": "left",
        "axes.titlepad": 8, "axes.titlecolor": INK, "axes.labelsize": 9, "axes.labelcolor": INK2,
        "axes.edgecolor": AXIS, "axes.linewidth": 0.8, "axes.facecolor": SURFACE, "figure.facecolor": SURFACE,
        "savefig.facecolor": SURFACE, "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK2,
        "ytick.labelcolor": INK2, "xtick.labelsize": 8.5, "ytick.labelsize": 8.5, "xtick.major.size": 3,
        "ytick.major.size": 0, "legend.fontsize": 8.5, "legend.frameon": False, "legend.labelcolor": INK2,
        "lines.linewidth": 2.0, "lines.markersize": 4.5, "lines.solid_capstyle": "round",
        "patch.linewidth": 0, "grid.color": GRID, "grid.linewidth": 0.6, "text.color": INK,
        "axes.prop_cycle": matplotlib.cycler(color=[C["corridor"], C["lapampa"], C["buffer"], C["gold"],
                                                    C["native"], C["twin"], C["other"]]),
    })
_apply_style()

# Event markers. CONVENTION (all time-series figures): the value for year t is plotted at x = t
# (addition(t) = map(t) - map(t-1)), and an event in calendar year Y is drawn as a vertical line at
# x = Y - 0.5, i.e. between the Y-1 and Y points: just before the first annual addition that can reflect it.
# (State of emergency = DS 046-2023-PCM, 7 Apr 2023.)
# An event is a dict: year, label (month + year), color, style ("solid" = emphasised, else dashed).
PERU_EVENTS = [
    dict(year=2019, label="Mercurio Feb 2019",           color=INK,   style="solid"),
    dict(year=2020, label="COVID-19 Mar 2020",           color=MUTED, style="dashed"),
    dict(year=2021, label="Plan Restauración 2021",      color=MUTED, style="dashed"),
    dict(year=2023, label="State of emergency Apr 2023", color=MUTED, style="dashed"),
]
EVENTS = PERU_EVENTS      # backwards-compatible alias
EVENT_TITLE_PAD = 30      # points of space above an axes whose event labels are drawn (title pad)
EVENT_NOTE = ("Vertical lines: an event in year Y is drawn at Y - 0.5, just before the first annual "
              "addition that can reflect it (addition(Y) = map(Y) - map(Y-1)).")

def x_of(years):
    """x position of year t's value: t itself (see the event convention above)."""
    return pd.Series(years, dtype=float)

def style_axes(ax, ygrid: bool = True, fmt: bool = True):
    """Plain axes: no top/right spines, recessive hairline y-grid, thousands separators."""
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.yaxis.grid(ygrid, color=GRID, linewidth=0.6); ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0, pad=4)
    if fmt:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: f"{v:,.0f}".replace("-", "−")))

def headline(fig, title: str, subtitle: str | None = None, x: float = 0.012):
    """Takeaway title (what the reader should conclude) + subtitle (what is measured, unit), left-aligned
    to the figure edge. Call BEFORE finish_figure; it reserves the top band in tight_layout."""
    fig.text(x, 0.995, title, fontsize=14, fontweight="medium", color=INK, va="top", ha="left")
    if subtitle:
        fig.text(x, 0.995, "\n" + subtitle, fontsize=9.5, color=INK2, va="top", ha="left", linespacing=1.9)
    fig._headline_lines = 1 + (subtitle.count("\n") + 1 if subtitle else 0)

def label_end(ax, x, y, text, color, dx: float = 6, dy: float = 0, weight: str = "semibold", ha: str = "left",
              va: str = "center", fontsize: float = 8.5):
    """Direct label next to a line end / mark: a small colour key dot is the mark itself, text stays ink."""
    ax.annotate(text, xy=(x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va,
                fontsize=fontsize, color=INK, fontweight=weight, annotation_clip=False)

def callout(ax, x, y, text, dx: float = 0, dy: float = 14, ha: str = "center", arrow: bool = True,
            fontsize: float = 8.5, color: str = INK):
    """Annotation of one key value on the chart (number + few words), with a thin leader line."""
    ax.annotate(text, xy=(x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va="bottom" if dy >= 0 else "top",
                fontsize=fontsize, color=color, linespacing=1.25, annotation_clip=False,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7, shrinkA=1, shrinkB=2) if arrow else None)

def period_band(ax, x0, x1, label: str | None = None, color: str = "#efece5"):
    """Light background band for a period (e.g. the operation years), label at the top inside the axes."""
    ax.axvspan(x0, x1, color=color, zorder=-1, lw=0)
    if label:
        ax.text((x0 + x1) / 2, 0.985, label, transform=ax.get_xaxis_transform(), ha="center", va="top",
                fontsize=7.5, color=INK2)

def add_event_markers(ax, label: bool = False, events=None):
    """Vertical lines at x = year - 0.5 for each event (default: PERU_EVENTS; Brazil passes its own list).
    label=True writes the labels in a strip ABOVE the axes, alternating two rows so neighbours never
    overlap; leave room with ax.set_title(..., pad=EVENT_TITLE_PAD)."""
    events = PERU_EVENTS if events is None else events
    xmin, xmax = ax.get_xlim()
    fig_w = ax.figure.get_size_inches()[0]
    in_per_x = 0.86 * fig_w / (xmax - xmin)            # rough inches per x-unit (axes ~86% of figure width)
    placed: list[list[tuple[float, float]]] = []        # per row: occupied [x0, x1] intervals (data units)
    for ev in sorted(events, key=lambda e: e["year"]):
        x = ev["year"] - 0.5
        solid = ev["style"] == "solid"
        ax.axvline(x, color=ev["color"] if solid else AXIS, linestyle="-" if solid else (0, (3, 2)),
                   linewidth=1.1 if solid else 0.8, zorder=0.5)
        if not label:
            continue
        half = 0.5 * len(ev["label"]) * 0.056 / in_per_x + 0.1   # half text width in data units, + gap
        row = 0
        while row < len(placed) and any(x - half < b and x + half > a for a, b in placed[row]):
            row += 1
        if row == len(placed):
            placed.append([])
        placed[row].append((x - half, x + half))
        ax.annotate(ev["label"], xy=(x, 1.0), xycoords=("data", "axes fraction"),
                    xytext=(0, 3 + 9 * row), textcoords="offset points", fontsize=7,
                    color=INK if solid else INK2, va="bottom", ha="center", annotation_clip=False,
                    fontweight="semibold" if solid else "normal")
    ax.set_xlim(xmin, xmax)

def set_year_ticks(ax, years, short: bool = False):
    years = list(years)
    step = 1 if len(years) <= 14 else 2
    ax.set_xticks([y for y in years][::step])
    ax.set_xticklabels([(f"'{str(y)[2:]}" if short else str(y)) for y in years][::step])

def _fit_vertically(fig, bottom: float, top: float):
    """tight_layout misses some artists (axes text above titles, maps); squeeze all axes so their full extent
    (titles, labels, annotations) sits between bottom and top."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    axes = [a for a in fig.axes if a.get_visible()]
    if not axes:
        return
    inv = fig.transFigure.inverted()
    hi = max(inv.transform(a.get_tightbbox(r))[1][1] for a in axes)
    lo = min(inv.transform(a.get_tightbbox(r))[0][1] for a in axes)
    if hi <= top + 1e-3 and lo >= bottom - 1e-3:
        return
    p_lo = min(a.get_position().y0 for a in axes); p_hi = max(a.get_position().y1 for a in axes)
    new_lo = p_lo + max(0, bottom - lo); new_hi = p_hi - max(0, hi - top)
    k = (new_hi - new_lo) / (p_hi - p_lo)
    for a in axes:
        b = a.get_position()
        a.set_position([b.x0, new_lo + (b.y0 - p_lo) * k, b.width, b.height * k])

FIG_DPI = 170   # 9-inch figure -> ~1530 px: sharp at page width on a retina screen

def finish_figure(fig, source: str, path: Path, rect_bottom: float = 0.04, event_note: bool = False):
    """Source line under the figure (+ optional event-convention footnote), tight layout, save.
    If headline() was called, the top band is reserved for it."""
    import textwrap
    text = "Source: " + source if not source.lower().startswith(("source", "sources")) else source
    text = text + ("\n" + EVENT_NOTE if event_note else "")
    w_in, h_in = fig.get_size_inches()
    wrap = int(w_in * 19)                               # ~19 characters per inch at 7 pt
    text = "\n".join("\n".join(textwrap.wrap(l, wrap)) or "" for l in text.split("\n"))
    n = text.count("\n") + 1
    rect_bottom = max(rect_bottom, (0.10 + 0.125 * n) / h_in)       # inches -> figure fraction
    fig.text(0.012, 0.008, text, fontsize=7, color=MUTED, va="bottom", linespacing=1.35)
    top = 1.0
    if getattr(fig, "_headline_lines", 0):
        top = 1 - (0.16 + 0.30 + 0.30 * (fig._headline_lines - 1)) / h_in
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig.tight_layout(rect=(0, rect_bottom, 1, top))
    _fit_vertically(fig, rect_bottom, top)
    fig.savefig(path, dpi=FIG_DPI)
    plt.close(fig)
    print(f"Saved {path.relative_to(ROOT)}")

SRC_MAPBIOMAS = "MapBiomas Peru, Collection 4 (class 4.2 Minería)"
SRC_PRICE = "World Bank Pink Sheet (nominal gold price, annual mean)"
