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
# Event timeline marked on every time-series figure (agent.md §10). Decimal years: Feb 2019 = 2019.1.
EVENTS = [
    (2019.1,  "Mercurio\nFeb 2019", "#B03A2E"),
    (2020.2,  "COVID-19\n2020",      "#7F8C8D"),
    (2021.0,  "Plan\nRestauración",  "#7F8C8D"),
    (2023.27, "State of emergency\nfrom Apr 2023", "#7F8C8D"),
]
# Convention for ALL time-series plots: the value for year t is drawn at x = t + 0.5 (the year
# spans [t, t+1)), so that decimal-dated events sit in the right year.

def x_of(years):
    return pd.Series(years, dtype=float) + 0.5

def style_axes(ax):
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, color="#E8EEF0"); ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: f"{v:,.0f}"))

def add_event_markers(ax, label: bool = False):
    """Vertical lines for the four enforcement/shock events. label=True writes small labels at the top."""
    for x, text, col in EVENTS:
        ax.axvline(x, color=col, linestyle="--" if col != "#B03A2E" else "-", linewidth=0.9, alpha=0.8, zorder=0)
        if label:
            ax.annotate(text, xy=(x, 1.0), xycoords=("data", "axes fraction"), xytext=(2, -2),
                        textcoords="offset points", fontsize=6.5, color=col, va="top", ha="left")

def set_year_ticks(ax, years):
    years = list(years)
    step = 1 if len(years) <= 14 else 2
    ax.set_xticks([y + 0.5 for y in years][::step])
    ax.set_xticklabels([str(y) for y in years][::step])

def finish_figure(fig, source: str, path: Path, rect_bottom: float = 0.04):
    """Source line under the figure, tight layout, save at 200 dpi."""
    fig.text(0.01, 0.01, source, fontsize=7.5, color="#555555")
    fig.tight_layout(rect=(0, rect_bottom, 1, 1))
    fig.savefig(path, dpi=200)
    plt.close(fig)
    print(f"Saved {path.relative_to(ROOT)}")

SRC_MAPBIOMAS = "MapBiomas Peru, Collection 4 (class 4.2 Minería)"
SRC_PRICE = "World Bank Pink Sheet (nominal gold price, annual mean)"
