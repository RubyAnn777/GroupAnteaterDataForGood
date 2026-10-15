# Map animation (slides 3–4)

Two Remotion compositions, 1920×1080, 30 fps. Description only: "first-time mining" = 30 m pixels mapped as
mining for the first time since 1985 (MapBiomas Peru Collection 4); the class cannot tell legal from illegal.

| Composition | Length | Shows |
|---|---|---|
| `MapLayers` | 26 s (780 frames) | 5 steps × 5 s: 1 protected areas + native communities → 2 Interoceanic Highway → 3 rivers + land mapped as mining by 2018 → 4 D.L. 1100 legal corridor (legality by location) → 5 La Pampa sector (our boundary) + corridor across the road |
| `MiningTimeline` | 45.6 s (1,368 frames) | 2008→2025: each year's first-time mining glows yellow, then fades to grey; timeline with event pins (D.L. 1100 2012, Mercurio Feb 2019, COVID-19 Mar 2020, Restauración 2021, emergency Apr 2023, navy out 2025); counter of first-time ha in La Pampa vs across the road; closing "Satellites can't see river dredges or mercury" |

Layout (both videos): the map sits in a box on the left (scaled 0.745), captions and the counter in a side panel
on the right, the timeline in a band below; nothing is drawn over the map except its own labels.

Outputs: `out/MapLayers.mp4`, `out/MiningTimeline.mp4`, stills in `out/stills/`:
`map_step1–5.png` (with side panel), `map_step1–5_clean.png` (full-bleed map, no captions: for the flippable
"Where we are" slides; render with `--props='{"clean":true}'`), `timeline_2018/2020/2025.png` (frames 570, 723, 1173).

## Rebuild

```bash
uv run python code/slides_map_export.py      # from the repo root: layers + map_data.json -> public/ (needs git-ignored rasters)
cd presentation/animation && npm i
npx remotion studio                          # preview
npx remotion render MapLayers out/MapLayers.mp4
npx remotion render MiningTimeline out/MiningTimeline.mp4
npx remotion still MapLayers out/stills/map_step1.png --frame=125   # steps at 125, 275, 425, 575, 770
npx remotion still MapLayers out/stills/map_step1_clean.png --frame=125 --props='{"clean":true}'
```

All numbers on screen come from `public/map_data.json`, written by `code/slides_map_export.py` from
`data_intermediate/zone_year_v2.csv` (first-time ha) and `output/numbers.csv` (`anp_tam_nr_addition_2025`).
Map label positions are set by hand in `src/*.tsx` (checked against the SERNANP polygons).
