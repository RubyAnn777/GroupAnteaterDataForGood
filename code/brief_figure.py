"""The ONE figure for the brief (agent.md §8): output/fig_brief_main.png.

Top panel: annual additions 2014-2025 in the Tambopata buffer zone (targeted), the Amarakaeri buffer zone
(comparison) and inside the Tambopata National Reserve (ANP file). Bottom panel: Madre de Dios total and the
rest of Madre de Dios. Shaded bands = 2016-18 / 2019-21 / 2022-25; short horizontal segments = period means
(Tambopata, Amarakaeri), so the difference-in-differences can be read off. Description only.
All series are MapBiomas Peru Collection 4, class 4.2 Minería (same publisher and collection, so combining is allowed).
"""
from __future__ import annotations
import matplotlib.pyplot as plt

from common import (OUT, x_of, style_axes, add_event_markers, set_year_ticks, finish_figure,
                    EVENT_TITLE_PAD, period_mean)
import peru, peru_anp

C_TAM, C_AMA, C_NR = "#c98a12", "#3b6fb0", "#7a4a9e"
C_TOT, C_REST = "#222222", "#8E7CC3"
PERIODS = {"2016-18": (2016, 2018), "2019-21": (2019, 2021), "2022-25": (2022, 2025)}

def _mean_segments(ax, s, color):
    for a, b in PERIODS.values():
        ax.hlines(period_mean(s, a, b), a - 0.4, b + 0.4, color=color, linewidth=3.2, alpha=0.45, zorder=1)

def run(pack):
    print("\n== Brief figure ==")
    _, adds, _ = peru.build_series(pack)
    _, panel = peru_anp.load_anp()
    nr = peru_anp._series(panel, peru_anp.RES["Tambopata NR"]).diff()
    yrs = list(range(peru.Y0, peru.Y1 + 1))

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 6.3), sharex=True, gridspec_kw={"height_ratios": [1.35, 1]})
    plt.rcParams.update({"font.size": 8})
    for ax in (a1, a2):
        for i, (a, b) in enumerate(PERIODS.values()):
            if i % 2 == 0:
                ax.axvspan(a - 0.5, b + 0.5, color="#000000", alpha=0.045, lw=0, zorder=0)
    series = [(peru.TAM, "Tambopata buffer zone (targeted)", C_TAM, "o", 2.0),
              (peru.AMA, "Amarakaeri buffer zone (comparison)", C_AMA, "s", 2.0)]
    for u, lab, c, m, lw in series:
        a1.plot(x_of(yrs), adds.loc[yrs, u], marker=m, markersize=3.5, color=c, linewidth=lw, label=lab, zorder=3)
        _mean_segments(a1, adds[u], c)
    a1.plot(x_of(yrs), nr.loc[yrs], marker="^", markersize=3.5, color=C_NR, linewidth=1.5, linestyle="--",
            label="Inside Tambopata National Reserve", zorder=3)
    a1.set_ylabel("New mining area\nin the year (ha)")
    a1.set_title("After Mercurio, new mining fell in the Tambopata buffer zone and returned from 2022;\nAmarakaeri and the rest of Madre de Dios rose",
                 loc="left", pad=EVENT_TITLE_PAD, fontsize=10.5, fontweight="bold")
    a1.set_ylim(-150, 4900)
    a1.legend(fontsize=7, frameon=False, loc="upper left", ncol=1, bbox_to_anchor=(0.0, 0.99))
    # period labels at the top of the shaded bands
    for lab, (a, b) in PERIODS.items():
        a1.text((a + b) / 2, 4850, lab, ha="center", va="top", fontsize=6.5, color="#555555")
    a1.text(0.995, 0.93, "Thick bars: period means\n(Tambopata, Amarakaeri)", transform=a1.transAxes,
            ha="right", va="top", linespacing=1.3, fontsize=6.5, color="#555555")

    a2.plot(x_of(yrs), adds.loc[yrs, "Madre de Dios total"], marker="o", markersize=3.5, color=C_TOT, linewidth=1.8,
            label="Madre de Dios total", zorder=3)
    a2.plot(x_of(yrs), adds.loc[yrs, "Rest of Madre de Dios"], marker="o", markersize=3, color=C_REST, linewidth=1.4,
            label="Rest of Madre de Dios (incl. legal corridor)", zorder=3)
    _mean_segments(a2, adds["Madre de Dios total"], C_TOT)
    a2.set_ylabel("New mining area\nin the year (ha)")
    a2.set_ylim(None, 23500)
    a2.legend(fontsize=7, frameon=False, loc="upper left")
    for i, a in enumerate((a1, a2)):
        style_axes(a); add_event_markers(a, label=(i == 0))
        a.tick_params(labelsize=7.5)
    set_year_ticks(a2, yrs)
    a2.set_xlim(peru.Y0 - 0.6, peru.Y1 + 0.6)
    finish_figure(fig, "Source: MapBiomas Peru, Collection 4 (buffer zones; protected areas), class 4.2 Minería (all mining, "
                       "legal and illegal). Description only: no causal claim. Satellites do not see river dredging or mercury. "
                       "Vertical line for year Y sits at Y - 0.5, before the first annual addition that can reflect it.",
                  OUT / "fig_brief_main.png")
