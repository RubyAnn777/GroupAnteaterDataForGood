# Map animation (storyline v3, slides 3–5)

Two Remotion compositions, 1920×1080, 30 fps. Description only. One measure (plan v3): **net mining additions =
new land + re-mined − stopped**, MapBiomas Peru Collection 4 (30 m, class 4.2 mining, legal and illegal alike).

| Composition | Length | Shows |
|---|---|---|
| `MapLayers` | 21 s (630 frames) | 4 steps × 5 s: 1 protected areas (buffer zones whole; Tambopata's incl. Kotsimba) + native communities → 2 Interoceanic Highway (+ rivers) → 3 D.L. 1100 legal corridor (legality by location) → 4 La Pampa sector (Tambopata buffer zone, 70.15–69.80° W) + corridor across the road + land mined by 2018 |
| `MiningTimeline` | 49.5 s (1,485 frames) | 2010→2025: each year's three flows on the map (new land brown, re-mined amber, stopped teal; grey = mining that year); event pins (Mercurio Feb 2019, COVID-19, Restauración, emergency Apr 2023, navy out 2025); counter of net additions and parts per year for La Pampa sector and the corridor across the road; closing "Satellites can't see river dredges or mercury" |

Flow colours on the dark map are the same hue families as `code/common.py` C, stepped lighter for the slate surface
(`code/slides_map_export.py` FLOW; checked with the dataviz palette validator). La Pampa and the corridor across the
road are drawn as white / light-blue dashed outlines in the timeline, so no orange sits next to the flows.

Outputs: `out/MapLayers.mp4`, `out/MiningTimeline.mp4`, stills in `out/stills/`: `map_step1–4.png` (with side panel),
`map_step1–4_clean.png` (full-bleed map; render with `--props='{"clean":true}'`), `map_zones_clean.png` (= step 4
clean, the zone map on the definition slide), `timeline_2019/2023/2025.png` (frames 660, 1080, 1290).

## Rebuild

```bash
uv run python code/slides_map_export.py      # from the repo root (~1 min): layers + flows + map_data.json -> public/
cd presentation/animation && npm i
npx remotion studio                          # preview
npx remotion render MapLayers out/MapLayers.mp4
npx remotion render MiningTimeline out/MiningTimeline.mp4
for k in 1 2 3 4; do f=$(( (k-1)*150 + 140 )); npx remotion still MapLayers out/stills/map_step$k.png --frame=$f; \
  npx remotion still MapLayers out/stills/map_step${k}_clean.png --frame=$f --props='{"clean":true}'; done
cp out/stills/map_step4_clean.png out/stills/map_zones_clean.png
npx remotion still MiningTimeline out/stills/timeline_2019.png --frame=660   # also 1080 (2023), 1290 (2025)
```

`slides_map_export.py` needs git-ignored inputs: `data_intermediate/zones_mdd.tif` (band 1 zone code per
`definitions.ZONES`, band 2 first-mined year, band 3 tenure), the yearly MapBiomas rasters
`data_raw/mapbiomas_peru_raster/peru_coverage-col4_{y}.tif` (streamed 1985–2025 over the map window to derive the
flows with the definitions of `code/raster_zones.py`), and the SERNANP / INGEMMET / RAISG vectors. All numbers on
screen come from `public/map_data.json`, written from `zonedata.region_units()` (the same table as
`output/numbers.csv`; the streamed pixel counts are asserted to match within 2%) and `output/numbers.csv`
(`tambopata_nr_2025_net`). Map label positions are set by hand in `src/*.tsx`.
