# Spatial extension: feasibility (2026-10-10)

Verdict: **feasible, and cheap** (prototype runs in about 20 s). All four layers downloaded with no account, captcha or personal data. Recommendation: **brief part 4 plus one clearly labelled robustness panel, not the core analysis.** The core stays MapBiomas additions (agent.md rules 1 to 8). Reasons below.

## Sources, files, sizes (all in `data_raw/`, git-ignored; sha256 for the key files)

| File | Size | Source / URL | sha256 |
|---|---|---|---|
| `amw/amazon_basin_detections.geojson` | 113,058,621 B (112 MB) | Amazon Mining Watch (Earth Genome), source.coop, updated 2026-10-03, model 48px_v4.10b ensemble, CC-BY-4.0. `https://data.source.coop/earthgenome/amazon-mining-watch/amazon_basin_detections.geojson` | f76555212661a10f9462a430cf91174e3507a872f1bf3e9686fc5465f12a56a8 |
| `amw/README.md` | 5 KB | same folder | 9df9ac0efcdd7ba11b94c4486d1a3d07750d7ebeb7c1304b772891928edbe87b |
| `sernanp/anp_definitivas.geojson` | 10 MB, 104 features | SERNANP ArcGIS REST `servicios_ogc/peru_sernanp_0102/MapServer/0` (query, f=geojson, outSR=4326) | d0d5bcd911ef890bdfef145c7256f2879a78ecc84b02b8711bc91a2ea850912a |
| `sernanp/zonas_amortiguamiento.geojson` | 22 MB, 81 features | SERNANP `gestion_de_anp/peru_sernanp_0214/MapServer/0` | e4fa55520d632fa2c3c735f120251f770de68df890bd7bf8b2589e82b169e3e6 |
| `sernanp/mineria_ilegal.geojson` | 2.4 MB, 179 features | SERNANP `servicios_ogc/peru_sernanp_0201/MapServer/1` (not inspected) | a7df347fae0a1097a0fd22da39af632f5d52273b9568c839a63e53e1ca4058f3 |
| `sernanp/ambito_control.geojson` | 26 MB, 633 features | same service, layer 0 (not inspected) | 12fcc5b36f432ae0b7e78e3d191ad4cbf03c17a53141323433121d610d07ca35 |
| `funai/tis_poligonais.geojson` | 49 MB, 665 TIs | FUNAI geoserver WFS `Funai:tis_poligonais` | 9245569ac9be6eb6709e05592481db99555f6359eb0c41ec0dd467b705a768ac |
| `ingemmet/corredor_minero_madre_de_dios_DL1100.geojson` | 282 KB, 1 polygon | GEOCATMIN `SERV_AREA_RESERVADA/MapServer/8` | 013d824666f8d451fc0d7b001f7fc16d77fccd1660e948a95e8e6aa93f0b111e |

What worked and what did not:
- **AMW.** GitHub repo `earthrise-media/mining-detector` holds only old/regional outputs (up to v3.7, 2023). The current product is on Source Cooperative; `data/outputs/MANIFEST.yaml` points there. One whole-Amazon file with an `onset_year` per patch (2018 to 2026) replaces per-year files. The cumulative/dissolved yearly products are internal, not public.
- **SERNANP.** The WFS/SHAPE-ZIP link in the GeoIDEP metadata (`peru_sernanp_021401`) returns "service not started" / 404. The sibling ArcGIS REST services (`..._0102`, `..._0214`) work and return GeoJSON (maxRecordCount 2000, not exceeded). WDPA not needed (and has no buffer zones), so not attempted.
- **FUNAI.** Geoserver answers 403 to requests without a browser User-Agent, and one run failed even with it; the retry with `maxFeatures=2000` succeeded. SHAPE-ZIP output did not work, GeoJSON did. CRS EPSG:4674. Yanomami is one row (`terrai_nome == "Yanomami"`, RR+AM, 9,664,975 ha).
- **Corridor.** Not in the GEOCATMIN cadastre layers. It is the polygon "ZONAS DE PEQUEÑA MINERIA Y MINERIA ARTESANAL - MADRE DE DIOS - D.L. 1100" in `SERV_AREA_RESERVADA` layer 8 ("Otras areas restringidas"). Area 498,308 ha, matching the 498,296 ha cited by the regional government/MINAM. INGEMMET labels these layers "referential".

## Prototype (`docs/overnight/notes/spatial_prototype.py`, output `spatial_prototype_output.csv`)
Run time about 20 s (AMW load 2 s). CRS: AMW CRS84; EPSG:32719 for Peru; EPSG:5880 (Brazil polyconic) for Yanomami; FUNAI is 4674, no issue. Patches are assigned to zones by centroid; zones overlap, so priority order NR > Tambopata BZ > corridor > other ANP > other BZ > outside. Annual area is the union of that year's onset patches minus earlier years' union (patches overlap by half a width, so summing patch areas would double count). Madre de Dios is cut by bounding box only (no department polygon downloaded).

**La Pampa point (assumption):** -12.95, -70.42, my approximate reading of the centre of La Pampa along the Interoceanica km 98 to 115 (MAAP #130 maps). Not an official coordinate; check against AMW patches before use.

New AMW mining, ha (onset year; **2018 is a stock, not an addition**; 2025 and 2026 are provisional):

| Unit | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| Tambopata NR (core) | 1463 | 64 | 46 | 46 | 6 | 12 | 35 | 640 | 1458 |
| Tambopata buffer zone (excl. NR) | 21352 | 2370 | 1708 | 985 | 675 | 1147 | 1708 | 2057 | 3218 |
| Mining corridor | 59424 | 15746 | 17298 | 14624 | 11943 | 11464 | 10012 | 8979 | 6655 |
| Other buffer zones | 5299 | 1157 | 1183 | 811 | 1036 | 1479 | 1356 | 879 | 1038 |
| La Pampa 0-10 km | 2064 | 991 | 767 | 772 | 772 | 524 | 776 | 84 | 79 |
| La Pampa 10-25 km | 27866 | 5241 | 3966 | 2997 | 1608 | 1907 | 872 | 1024 | 927 |
| La Pampa 25-50 km | 35915 | 7853 | 9399 | 7371 | 6108 | 7748 | 7895 | 4951 | 5599 |
| Inside Yanomami TI | 1537 | 2324 | 1093 | 3054 | 8683 | 4012 | 502 | 193 | 41 |
| Yanomami outside 0-10 km | 1294 | 70 | 87 | 380 | 925 | 439 | 252 | 53 | 175 |
| Yanomami outside 10-25 km | 1806 | 87 | 245 | 348 | 152 | 355 | 152 | 462 | 274 |
| Yanomami outside 25-50 km | 4232 | 519 | 139 | 450 | 152 | 128 | 181 | 661 | 338 |

All numbers are description only. They are not MapBiomas hectares and must not be compared with them (rule 6). Sanity: Tambopata NR core 640 ha in 2025 and 1,458 ha in 2026 is in line with MAAP #241 (about 500 ha H2 2025 to Feb 2026). Yanomami peak of 8,683 ha in 2022 and drop afterwards is in line with the story, but see below.

## Caveats
1. **Edge effect:** onset needs corroboration in the following year (Recipe A), so 2025 and 2026 are provisional and the last confirmable year is 2024. The post-2023 fall inside Yanomami could be partly an artefact of removed miners or of the detector missing re-vegetating/abandoned sites; the quarterly data would be needed.
2. **Pre-trend:** there are only 2018 (stock) and 2019 (Feb 2019 is when Mercurio starts), so no clean pre-period for Peru. The MapBiomas series remains the only usable pre-trend.
3. **What AMW sees:** 480 m patches of mine scars on land, not river dredges, not mercury. The patch is an upper bound on mined area, not a hectare count of disturbance.
4. **Zone definitions** depend on a boundary snapshot of today (SERNANP, corridor from INGEMMET, "referential"), not on the 2019 boundaries. Corridor and buffer zone overlap, so priority rules change the split. Corridor includes legal mining (cannot separate).
5. Tambopata NR in SERNANP is 2,776 km2 (FZS says 2,746 km2); close enough for a cross-check note.
6. Three layers (`mineria_ilegal`, `ambito_control`) are unexamined; unknown vintage, may be useful as a second view on enforcement areas.

## What is missing
Department/district boundaries (Madre de Dios, Roraima), a Munduruku/Kayapo comparison run (the script handles any TI by name; not run), AMW quarterly files for 2025 to 2026, validation of AMW area against MapBiomas class 4.2 in the same polygons (the natural "check" per dataset), and an official La Pampa polygon (could use the AMW patch cluster near km 98-115 instead of a point).

## Recommendation
Use as **brief part 4 / robustness**, not core. It directly speaks to part 4(b) "what satellites can't see" and part 4(c), adds the spatial gradient (rings) for displacement that the aggregate MapBiomas buffer-zone table cannot show, and the Tambopata core panel answers the "inside the reserve" gap without the ANP xlsx. But AMW has 2018 as a stock year, no pre-period, a different detector, and provisional last years, so it cannot carry the DiD. If the team has an evening: add one panel (rings around La Pampa, 2019 to 2024 only, 2018 excluded) to the figure or appendix, and log the check (e.g. AMW 2018 to 2024 vs MapBiomas mining area in the same Tambopata BZ).
