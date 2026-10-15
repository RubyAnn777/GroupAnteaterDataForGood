# Feasibility: sub-annual forest-loss alerts and a gold-bearing-land proxy (Madre de Dios)

Checked 2026-10-12 (agent run, no accounts, no logins). Test window for alerts: lon -70.2..-69.8, lat -13.1..-12.7 (La Pampa / Tambopata BZ). Test window for geology: lon -70.4..-69.6, lat -13.2..-12.6.
All numbers below come from the downloaded files (scripts were throwaway, in the session scratchpad). **Status: DRAFT, team must review.**

## Verdict in four lines

| Product | Public, no key? | Pre-2019 period? | Verdict |
|---|---|---|---|
| **GLAD-L (UMD, Landsat 30 m)** | **Yes**, public GCS bucket `earthenginepartners-hansen` | **Yes: 2017 and 2018 files in the bucket** (2015-16 exist on GFW, but only via a key) | **Works. Use this for a monthly pre/post Mercurio series.** |
| GLAD-S2 (UMD, Sentinel-2 10 m) | **Yes**, same bucket | No (starts 2019-01) | Works; post-2019 only, good for 2019-2026 detail |
| RADD (WUR, Sentinel-1 10 m) | **No** public no-key download found (GFW Data API needs a key; GEE needs an account) | No (South America from Jan 2020 per GFW) | Not feasible under our rules; also no pre-period |
| GFW integrated alerts | GFW posts a download link **with an embedded key** on its ArcGIS Hub item; in our environment that request was reset (curl error 35), so it was **not downloaded** | Encoding starts 2015-01-01, but pre-2018 content = GLAD-L only | Not tested end-to-end; not needed, since GLAD-L covers it |
| **INGEMMET geology 1:100k (GEOCATMIN)** | **Yes**, ArcGIS REST MapServer, query → GeoJSON | n/a (static map) | **Works.** `Qh-al` alluvial deposits + `NQ-md/s` Madre de Dios Fm. |
| INGEMMET mineral occurrences | **Yes**, ArcGIS REST | n/a | Works: 79 placer gold points in the MdD bbox (bonus) |
| INGEMMET metallogenic belts | Yes | n/a | No placer/alluvial-gold belt in the layer, so not useful |

## A) Forest-loss alerts

### A1. GLAD-L (Landsat): works, with a pre-period

**Source:** UMD GLAD, public Google Cloud Storage bucket `earthenginepartners-hansen` (listing via the JSON API, no key):
`https://storage.googleapis.com/storage/v1/b/earthenginepartners-hansen/o?prefix=GLADalert/&delimiter=/`

**Tiling:** 10 x 10 degree tiles, named `<W-lon>_<S-lat>_<E-lon>_<N-lat>`. Our test window **straddles lon -70**, so it needs two tiles:
`080W_20S_070W_10S` (lon -80..-70, holds the western part: La Pampa west of -70, Huepetuhe, Amarakaeri) and `070W_20S_060W_10S` (lon -70..-60: Tambopata BZ and NR, Puerto Maldonado). For the whole of Madre de Dios, both tiles are needed.

**Where each year sits (one alert file + one date file per year and tile):**

| Year | Path in the bucket | Collection |
|---|---|---|
| 2017 | `alert/2017/GLADalert_alert17_<tile>.tif`, `alert/2017/GLADalert_alertDate17_<tile>.tif` | Landsat C1 |
| 2018 | `GLADalert/2018/final/alert18_<tile>.tif`, `.../alertDate18_<tile>.tif` (also dated snapshots `GLADalert/2018/MM_DD/`) | C1 |
| 2019 | `GLADalert/2019/final/alert19_...`, `alertDate19_...` | C1 |
| 2020 | `GLADalert/2020/final/alert20_...`, `alertDate20_...` | C1 |
| 2021-2025 | `GLADalert/C2/<year>/final/alertYY_...` and/or `GLADalert/C2/current/alertYY_...` | **Landsat C2** |
| 2026 (running) | `GLADalert/C2/current/alert26_...`, `alertDate26_...` (updated 2026-10-11) | C2 |

Also present: `last_<tile>.tif` (1.9 GB, latest image composite) and `obsDate_<tile>.tif` (date of last clear observation, ~99 MB). These are not needed.
**2015 and 2016 are not in the bucket.** GFW's `umd_glad_landsat_alerts` (Data API, key needed) states coverage "from 2015 to the present for select countries in the Amazon", so 2015-16 exist but not under our no-account rule.

**Files downloaded** to `data_raw/glad_alerts/` (byte-exact; the local name is the bucket path with `/` replaced by `_`; base URL `https://storage.googleapis.com/earthenginepartners-hansen/`; downloaded 2026-10-12):

| Local file | Bucket path | Bytes | sha256 |
|---|---|---|---|
| alert_2017_GLADalert_alertDate17_080W_20S_070W_10S.tif | alert/2017/GLADalert_alertDate17_080W_20S_070W_10S.tif | 16,400,471 | eea5d3a7d8a42302d146ffdebe0684455a3d82b2079761e241cf83d552d5305a |
| alert_2017_GLADalert_alert17_080W_20S_070W_10S.tif | alert/2017/GLADalert_alert17_080W_20S_070W_10S.tif | 11,186,611 | 7db614357aebaef6bfe9121aaa8eb43d2147dfb3a1fc5248a62a4b2c77604dee |
| GLADalert_2018_final_alertDate18_080W_20S_070W_10S.tif | GLADalert/2018/final/alertDate18_080W_20S_070W_10S.tif | 15,941,444 | efd2f8ae3005fec9a24438fa04f9cf44731def1177fb179cb9aca84bd7c49d49 |
| GLADalert_2018_final_alert18_080W_20S_070W_10S.tif | GLADalert/2018/final/alert18_080W_20S_070W_10S.tif | 10,911,139 | c361a6c7283781333b6633c98a6ee3ff5f3e1be67df4414dcf4b160402a12e87 |
| GLADalert_2018_final_alertDate18_070W_20S_060W_10S.tif | GLADalert/2018/final/alertDate18_070W_20S_060W_10S.tif | 22,191,085 | c67248525f00e6f1797fc356f875a429ad6dd8c292bb0da13c621e878da0f352 |
| GLADalert_2018_final_alert18_070W_20S_060W_10S.tif | GLADalert/2018/final/alert18_070W_20S_060W_10S.tif | 14,097,272 | 56337be9f1117e7a6626480fa2831d9ea01aea0199524023df45cf320a666fc6 |
| GLADalert_C2_2021_final_alertDate21_080W_20S_070W_10S.tif | GLADalert/C2/2021/final/alertDate21_080W_20S_070W_10S.tif | 20,105,947 | 8a12257c71b8d3fe336131f32adab43b1bcea9c3de7b0019716e7025a37cbfa9 |
| GLADalert_C2_2021_final_alert21_080W_20S_070W_10S.tif | GLADalert/C2/2021/final/alert21_080W_20S_070W_10S.tif | 13,538,271 | d0769aa282781e1bf80efcb14da853df01956c269e2a7e26056d65201ad3fac6 |

**File structure (inspected with rasterio):**
- Single band, GeoTIFF, LZW, EPSG:4326, pixel 0.00025 deg (about 27 x 27 m, about 0.074 ha at 13 S), 40,000 x 40,000 px per tile, no nodata tag (0 = no alert).
- `alertDateYY`: **uint16, day of year within year YY** (1-366; 0 = no alert). Band description `alertDate18` etc. (C1); none (C2).
- `alertYY`: **uint8 confidence** (Hansen et al. 2016: 2 = probable, 3 = confirmed). In the `final` files every alert pixel is 3, and alert > 0 exactly where alertDate > 0.
- Each yearly file holds only alerts first detected in that year, inside the GLAD forest mask. A pixel that is already cleared cannot alert again, so **re-mining of old scars is invisible** (the same limit as the "additions" caveat, only stricter).

**What the test window shows** (alert area, ha, by month; western part lon -70.2..-70.0 = tile 080W):

| Year | First / last date | Total ha | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2017 (C1) | 2017-01-06 / 2017-12-08 | 1,152 | 31 | 8 | 0 | 226 | 24 | 87 | 1 | 309 | 318 | 99 | 40 | 9 |
| 2018 (C1) | 2018-01-09 / 2018-11-01 | 1,185 | 65 | 8 | 3 | 47 | 241 | 189 | 300 | 177 | 121 | 26 | 7 | 0 |
| 2021 (C2) | 2021-01-09 / 2021-12-03 | 582 | 6 | 4 | 1 | 13 | 15 | 42 | 40 | 152 | 38 | 268 | 0 | 3 |

Eastern part (lon -70.0..-69.8, tile 070W), 2018: 880 ha, 2018-01-09 to 2018-11-09.
These are **descriptive** feasibility numbers only, not brief numbers. Months bunch up in the dry season (May-Oct), because cloud-free Landsat views are rare in the wet season. **A "monthly" series is really "date of first clear view after the loss"**, so use quarters or dry/wet season, not single months.

**Limits:**
1. The **collection break** C1 (2017-2020) → C2 (2021+): different processing, so a level shift at 2021 is possible. Don't read a 2020 → 2021 jump as an effect.
2. Alerts are designed to be conservative, and UMD says they "should not be used to provide area estimates". Use them for **timing** (when did clearing near La Pampa drop, month by month around Feb 2019), not for hectares.
3. Forest loss is not the same as mining: the alerts include agriculture, roads and river migration. Intersect them with the MapBiomas mining mask or the AMW polygons.
4. Pre-period = 2017-2018 only (two years); with 2015-16 from GFW it would be four.

### A2. GLAD-S2 (Sentinel-2): works, post-2019 only

**Source:** same bucket, `S2alert/` with sub-folders `alert/`, `alertDate/`, `obsDate/`, `forestMask/`, `last_N/`, `last_R/`, `last_S1/`, plus `S2alert/uploadDate.txt` ("Updated Fri Oct 9 19:44:58 2026 UTC"). Each folder holds one cumulative file per tile (all years in one file).
**Downloaded:** `S2alert_alertDate_080W_20S_070W_10S.tif` ← `S2alert/alertDate/080W_20S_070W_10S.tif`, 128,069,730 bytes, sha256 `3aafa409697bae02aeac5a141869bb536601b4ff420a70700fc9d43dd85bccf0` (plus `S2alert_uploadDate.txt`, 37 bytes, sha256 `6aee42ee...29b5`). **Over 50 MB**: it should be git-ignored and linked in DOWNLOAD_LOG (I did not edit `.gitignore`). The eastern tile `070W_20S_060W_10S` is 710 MB (alertDate) / 303 MB (alert); not downloaded.
**Structure:** uint16, 0.0001 deg (about 11 m, about 0.012 ha), EPSG:4326, LZW; 0 = no alert. **Date = days since 2018-12-31** (inferred from the data: min 5 → 2019-01-05, max 2837 → 2026-10-07, two days before the upload date; a 2019-01-01 origin would give 2026-10-08, so the origin is ±1 day uncertain and should be checked against the UMD GEE example script). `S2alert/alert/` (read remotely via `/vsicurl/`, not downloaded) = uint8 confidence 1-4 in the window (counts 21k / 337k / 351k / 573k px), present exactly where alertDate > 0.
**Test window (west part), alert area by year (ha):** 2019 1,302 · 2020 1,511 · 2021 1,622 · 2022 1,341 · 2023 1,484 · 2024 2,153 · 2025 3,134 · 2026 (to 7 Oct) 2,947. These are not comparable with GLAD-L hectares (10 m vs 30 m, a different forest mask: primary humid forest only, with 2001-2018 Hansen loss removed).
**Limit:** it starts in January 2019, so it **cannot give a pre-Mercurio baseline**. Use it for post-2019 dynamics (2021 Restauración, 2023 emergency, 2025-26 Malinowski).

### A3. RADD (Sentinel-1): not feasible under our rules
- GFW Data API `dataset/wur_radd_alerts` metadata is public (versions, citation Reiche et al. 2021, ERL, doi:10.1088/1748-9326/abd0a8, CC BY 4.0), but `.../download/geotiff` returns **403 "Request is missing valid API key"**. The GFW S3 data lake (`s3://gfw-data-lake/...`) returns 403 without credentials. Native distribution is a GEE asset (needs an account).
- GFW documents RADD coverage for South America **from January 2020**, so there is no pre-period anyway. The advantage is radar: it sees through clouds, so wet-season timing is better.

### A4. GFW integrated alerts
- Data API `dataset/gfw_integrated_alerts` (latest v20261010): `download/geotiff?grid=10/100000&tile_id=10S_080W&pixel_meaning=date_conf` → **403 without a key**.
- GFW's public ArcGIS Hub item (ArcGIS Online id `bac1e89b8d1c4d57b0cf15764b07c26f`, FeatureServer `https://services2.arcgis.com/g8WusZB13b9OegfU/arcgis/rest/services/Integrated_deforestation_alerts/FeatureServer/0`) lists per-tile download links that **include an API key published by GFW** (tile `10S_080W` covers our window). In this environment the request was reset by the network (curl error 35), so it is **not verified**. A team member could try the link in a browser. Whether using a key that GFW embeds publicly is acceptable is a team call.
- **Encoding** (from the item description): one integer per pixel; the leading digit is confidence (2 low, 3 high, 4 highest = several systems), followed by **days since 2014-12-31** (e.g. 21847 = low confidence, 2020-01-21); 0 = no alert; 10 m; "date represents the earliest detection". Coverage: GLAD-L tropics from 2018, and "from 2015 for select countries in the Amazon"; GLAD-S2 from Jan 2019; RADD from Jan 2020 (South America). So **before 2019 the integrated layer is just resampled GLAD-L**, and A1 already gives that.
- The GFW tile cache (`tiles.globalforestwatch.org/<dataset>/latest/default/z/x/y.png`) redirected and then failed; these are display PNGs anyway, not analysis data.

## B) Gold-bearing land proxy: INGEMMET geology (GEOCATMIN)

**Service:** `https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_GEOLOGIA_100K_INTEGRADA/MapServer/6` ("Geología", 1:100,000 integrated geological map), ArcGIS 10.91, polygons, native SR 3857, maxRecordCount 1000, query supports `f=geojson` and `outSR=4326`. A 1:50k layer also exists (`SERV_GEOLOGIA_50K_INTEGRADA/MapServer/7` "Litologia", 478 polygons in the test bbox; not downloaded; coverage of 50k sheets in MdD is probably partial).

**Downloaded:** `data_raw/ingemmet/geologia_100k_bbox_70.4W_69.6W_13.2S_12.6S.geojson`, 19,039,182 bytes, sha256 `36f2828ec423a58bbf2315c7ff57f3db1084c956e7ea53b0311ec512958abea4`, 2026-10-12, 611 features (count query = 611, under the 1000 cap, so complete). URL:
`https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_GEOLOGIA_100K_INTEGRADA/MapServer/6/query?geometry=-70.4,-13.2,-69.6,-12.6&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&where=1%3D1&outFields=*&returnGeometry=true&outSR=4326&f=geojson`

**Fields:** `OBJECTID`, `CODI` (int unit code, e.g. 3 = Qh-al), `NAME` (unit symbol), `UNIDAD` (unit name), `DESCRIP` (lithology), `HOJA` (1:100k sheet: 26v, 26x, 27v, 27x), `SHAPE.AREA`, `SHAPE.LEN` (in 3857 units; ignore them and recompute). Geometries are all valid.

**Units in the test bbox** (area clipped to the bbox, UTM 19S; total 576,014 ha = the full bbox, so coverage is complete):

| NAME | UNIDAD | ha | polygons |
|---|---|---|---|
| NQ-md/s | Formación Madre de Dios, Miembro superior (Plio-Pleistocene) | 273,160 | 28 |
| **Qh-al** | **Depósito aluvial** (Holocene; "grava, arena, limo y arcilla") | **213,380** | 458 |
| Nmp-i | Formación Ipururo | 51,870 | 25 |
| (null) | Río | 22,209 | 5 |
| PN-ch | Formación Chambira | 8,328 | 2 |
| Kis-ch | Formación Chonta | 2,044 | 7 |
| (null) | Laguna | 1,686 | 80 |
| P-y, P-poz, Ki-o, Ks-v | Yahuarango, Pozo, Grupo Oriente, Vivian | 3,339 | 6 |

In the whole MdD bbox (-72.6..-68.6 / -14.6..-10.5) the Quaternary/Neogene symbols present include `Qh-al`, `Q-al`, `Q-alfl` (aluvial, fluvial), `Q-fl` (fluvial), `NQ-md`, `NQ-md/s`, `NQ-md/i`, plus Andean units in the SW corner (`Q-gl`, `Q-glfl`, `Q-cl`, `Grupo Barroso`, `Qp-ss`...). **There is no explicit `Qp-al` or "terraza" unit** in the 1:100k map here. The gold-bearing terraces of the Huepetuhe/Colorado/Inambari area are mapped inside `NQ-md/s` (the Madre de Dios Formation) and `Qh-al`.

**Proxy suggestion:** "gold-bearing land" = `Qh-al` ∪ `Q-al` ∪ `Q-alfl` ∪ `Q-fl` (narrow, river-bound: the floodplain placers where La Pampa and the dredges are) as the strict version, plus `NQ-md/s` as a broad version (it covers about half the bbox, so on its own it does not discriminate much). This proxy is pre-determined geology, not an outcome, so it is legitimate for selecting or matching control units on pre-treatment characteristics (see the §11 review in agent.md).

**Bonus, placer occurrences:** `SERV_OCURRENCIA_MINERAL/MapServer/0` ("Metálico") has a field `TIPO_DEPOS`. In the MdD bbox, 317 metallic occurrences, of which 79 are `Placer` (78 `Au`; FORMACION mostly "Cuaternario", "Depósito Aluvial", "Terraza"; ESTADO 60 Inactiva, 18 Activa). Saved: `data_raw/ingemmet/ocurrencias_placer_mdd_bbox.geojson`, 37,931 bytes, sha256 `648b4a4c31e593b7cc50edd89c55b5ae704842e4077696855055ae8508dc71fd`, URL
`https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_OCURRENCIA_MINERAL/MapServer/0/query?geometry=-72.6,-14.6,-68.6,-10.5&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&where=TIPO_DEPOS%3D%27Placer%27&outFields=*&returnGeometry=true&outSR=4326&f=geojson`.
Caveat: text has legacy encoding errors (e.g. "Met\xa0lico", "Nø"), and the points are an inventory of known sites, not a survey (selection: known because mined).

**Metallogenic belts** (`SERV_METALOGENETICO/MapServer/4`, fields `ID, TIPO, FRANJA, ETIQUETA`): 9 belts intersect the MdD bbox, all Andean bedrock types (e.g. "Franja de Au en rocas meta-sedimentarias del Ordovícico y Silúrico-Devónico", FRANJA I). There is **no placer/alluvial belt** (a query on `TIPO LIKE '%PLACER%'` returned nothing). Not a useful proxy for lowland Madre de Dios.

## Limits that apply to B
- 1:100k means about 50-100 m positional accuracy, and polygons were drawn from older field mapping and images. Fine for zone-level shares, too coarse for pixel matching.
- The REST cap is 1000 features per request. For the whole department, page by `resultOffset` or split the bbox (the layer supports query; pagination support was not tested on this layer; the occurrences layer said "Pagination is not supported").
- INGEMMET marks GEOCATMIN layers as reference information. Cite "INGEMMET, GEOCATMIN, Mapa geológico integrado 1:100 000 (servicio SERV_GEOLOGIA_100K_INTEGRADA), accessed 2026-10-12".

## Not done / for the team
- No rows were added to `DOWNLOAD_LOG.csv` and `.gitignore` was not changed (out of scope for this run). Add rows for the files above. Git-ignore `data_raw/glad_alerts/S2alert_*.tif` (128 MB).
- If GLAD-L is adopted: download `alertDate17..26` for both tiles (about 20 MB each, about 400 MB in total), clip to MdD, and intersect with the mining mask.

Firecrawl calls used: 5 (3 searches, 2 scrapes, one of which failed).
