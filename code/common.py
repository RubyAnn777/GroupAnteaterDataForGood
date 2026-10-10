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
# Event markers. CONVENTION (all time-series figures): the value for year t is plotted at x = t
# (addition(t) = map(t) - map(t-1)), and an event in calendar year Y is drawn as a vertical line at
# x = Y - 0.5, i.e. between the Y-1 and Y points: just before the first annual addition that can reflect it.
# (State of emergency = DS 046-2023-PCM, 7 Apr 2023.)
# An event is a dict: year, label (month + year), color, style ("solid" = emphasised, else dashed).
PERU_EVENTS = [
    dict(year=2019, label="Mercurio Feb 2019",                color="#B03A2E", style="solid"),
    dict(year=2020, label="COVID-19 Mar 2020",                color="#6C7A7B", style="dashed"),
    dict(year=2021, label="Plan Restauración 2021",           color="#6C7A7B", style="dashed"),
    dict(year=2023, label="State of emergency Apr 2023", color="#6C7A7B", style="dashed"),
]
EVENTS = PERU_EVENTS      # backwards-compatible alias
EVENT_TITLE_PAD = 30      # points of space above an axes whose event labels are drawn (title pad)
EVENT_NOTE = ("Vertical lines: an event in year Y is drawn at Y - 0.5, just before the first annual "
              "addition that can reflect it (addition(Y) = map(Y) - map(Y-1)).")

def x_of(years):
    """x position of year t's value: t itself (see the event convention above)."""
    return pd.Series(years, dtype=float)

def style_axes(ax):
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, color="#E8EEF0"); ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: f"{v:,.0f}"))

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
        ax.axvline(x, color=ev["color"], linestyle="-" if ev["style"] == "solid" else "--",
                   linewidth=1.6 if ev["style"] == "solid" else 0.9, alpha=0.9, zorder=0)
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
                    xytext=(0, 3 + 8.5 * row), textcoords="offset points", fontsize=6.5,
                    color=ev["color"], va="bottom", ha="center", annotation_clip=False,
                    fontweight="bold" if ev["style"] == "solid" else "normal")
    ax.set_xlim(xmin, xmax)

def set_year_ticks(ax, years):
    years = list(years)
    step = 1 if len(years) <= 14 else 2
    ax.set_xticks([y for y in years][::step])
    ax.set_xticklabels([str(y) for y in years][::step])

def finish_figure(fig, source: str, path: Path, rect_bottom: float = 0.04, event_note: bool = False):
    """Source line under the figure (+ optional event-convention footnote), tight layout, save at 200 dpi."""
    import textwrap
    text = source + ("\n" + EVENT_NOTE if event_note else "")
    wrap = int(fig.get_size_inches()[0] * 17)          # ~16 characters per inch at 7.5 pt
    text = "\n".join("\n".join(textwrap.wrap(l, wrap)) or "" for l in text.split("\n"))
    rect_bottom = max(rect_bottom, 0.012 + 0.0225 * (text.count("\n") + 1) * (7.5 / 7.5))
    fig.text(0.01, 0.01, text, fontsize=7.5, color="#555555", va="bottom")
    fig.tight_layout(rect=(0, rect_bottom, 1, 1))
    fig.savefig(path, dpi=200)
    plt.close(fig)
    print(f"Saved {path.relative_to(ROOT)}")

SRC_MAPBIOMAS = "MapBiomas Peru, Collection 4 (class 4.2 Minería)"
SRC_PRICE = "World Bank Pink Sheet (nominal gold price, annual mean)"
