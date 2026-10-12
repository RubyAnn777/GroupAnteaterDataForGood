<!--
Source of docs/overnight/METHODS.html (how everything is built). Build: `uv run python docs/overnight/build_report.py`.
Same placeholder and claim-tag rules as explainer_content.md. Written in smart-brevity style for the team (Ruby first).
-->

# How the analysis is built: data, measures, models

> One page per method: what it answers, how it works, what it controls for, what it can't, where the code is. Every number on the walkthrough comes from one script, `code/main.py`. Version: plan v2 (12 Oct 2026). Section 12 covers everything added after Ruby's review.

## 1. The bottom line

**Everything runs from one command.** `uv run python code/main.py` checks the data against the publishers, builds every measure, fits every model, draws every figure and writes every number to `output/numbers.csv`.

**Three building blocks:**
- **Data:** satellite maps of mining (MapBiomas, Amazon Mining Watch, INPE alerts), boundaries (parks, buffer zones, corridor, communities), and context (gold price, gold output, fines).
- **Measures:** how much *new* mining appears each year, per area.
- **Comparisons:** the targeted area against areas that tell us what might have happened without the operation.

**Why it matters:** Any number in the brief can be traced back: brief → `numbers.csv` → the function that made it → the raw file → the publisher.

<pre class="mermaid">
flowchart LR
  A[Raw files<br/>data_raw/] --> B[Checks against<br/>publisher numbers]
  B --> C[Measures<br/>new mining per area-year]
  C --> D[Comparisons<br/>DiD, event study,<br/>models, twin]
  D --> E[Figures + tables<br/>output/]
  D --> F[numbers.csv<br/>every cited number]
  F --> G[Walkthrough<br/>+ brief]
</pre>

## 2. The data

**One rule first:** we never add or subtract numbers from different sources or collections. Different products measure different things.

| Data | What it measures | Years | Used for | Check against publisher |
|---|---|---|---|---|
| **MapBiomas Peru, Collection 4** (course tables + our raster download) | Land class of every 30 m pixel each year; class 30 = mining (legal and illegal) | 1985–2025 | Main outcome, Peru | Tambopata buffer zone 2025 = 20,730 ha ✔ |
| **MapBiomas Peru rasters** *(v2)* | Same product, as maps, so we can use our own boundaries | 1985–2025 | All Peru zones in v2 | Raster gives 20,716 ha vs 20,730 ✔ |
| **Amazon Mining Watch (AMW)** | Gold-mining scars found by a machine-learning model, in 480 m squares | 2018–2026 | Twin search, Brazil, robustness | No published totals |
| **MapBiomas Amazonía, Collection 6** | Same idea as MapBiomas, all nine Amazon countries | 1985–2023 | Pre-2019 trend of candidate twins | Amazon mining 2023 = 0.78 Mha ✔ |
| **MapBiomas Brazil, Collections 10.1 and 11** | Mining per indigenous territory and per municipality | 1985–2025 | Brazil | Garimpo 2025 = 445,987 ha ✔ |
| **INPE DETER alerts** | Monthly alerts of new mining, Brazil | 2016–2026 | Brazil timing | 2019 total within 0.2% ✔ |
| **Boundaries** | SERNANP parks and buffer zones; INGEMMET legal corridor; RAISG roads and protected areas; MapBiomas Amazonía native communities; FUNAI territories | current | Zones | — |
| **Context** | World Bank gold price; Peru central bank gold output; IBAMA fines | various | Context only | Gold Aug 2026 = $4,411/oz ✔ |

**Why it matters:** The instructor will trace one number back to the publisher. Each dataset has one check, logged in `output/checks.csv` and `DOWNLOAD_LOG.csv`.

## 3. The main measure: new mining per year

**We count change, not stock.** Total mining area only grows, like the gold price, so totals correlate with almost anything.

- **Addition** (the course measure) = mining area this year − mining area last year, per area, in hectares.
- **Rule:** add up all rows of an area *first*, then take the difference.

**v2 splits the addition into its parts** (pixel by pixel, from the rasters):

| Part | A pixel that is… | Tells us |
|---|---|---|
| **New land** | mining now, never mining before | expansion into forest or new ground |
| **Re-mined** | mining now, not last year, but mining in some earlier year | miners returning to old pits |
| **Stopped** | mining last year, not now | abandoned, regrowing, or reclassified |
| **From forest** | mining now, forest last year | forest lost to mining |

`addition = new land + re-mined − stopped` (checked in code for every area and year).

**Why it matters:** A small addition can hide a big return to old pits. Ruby's re-mining question needs the split.

**What it can't see:** river dredges, mercury, who mines, and whether a site is legal. Satellites see bare ground and ponds.

## 4. The places (zones)

**v1 used whole buffer zones** from the course tables (Tambopata, Amarakaeri and 13 others).

**v2 draws one zone map on the raster grid.** Each pixel belongs to exactly one zone, in this order (first match wins):

1. Tambopata reserve
2. Other reserves and parks
3. Kotsimba (native community)
4. Other native communities
5. **Corridor across the road:** the legal corridor directly north of the Interoceanic Highway, opposite La Pampa, within 10 km
6. Rest of the legal corridor
7. **La Pampa sector:** the Tambopata buffer zone between longitudes 70.15° and 69.80° W
8. Rest of the Tambopata buffer zone
9. Amarakaeri buffer zone
10. Bahuaja-Sonene buffer zone
11. Other buffer zones
12. Rest of Madre de Dios

**Two zones have no official boundary:** La Pampa and "across the road". We define them by longitude and test a narrower and a wider version.

**Road bands:** in the La Pampa longitudes, every pixel gets its distance to the highway (north = positive). That lets us ask directly: did new mining jump from the south side to the north side?

**Why it matters:** "Tambopata buffer zone" mixes La Pampa (shut down) with new fronts like Mangote. The zone map separates the stories.

## 5. Comparison 1: before and after, against a neighbour (2×2)

**Question:** Did the targeted zone change more than a comparison zone?

**How:** gap change = (targeted after − before) − (comparison after − before). Before = 2016–18, during = 2019–21, after = 2022–25.

**Controls for:** anything that moved both zones equally (gold price, COVID, national policy).

**Can't control for:** anything that hit only one zone. Spillovers into the comparison zone make the gap look bigger.

**Code:** `code/peru.py` (`describe_and_compare`). **Result:** {{did_main}} ha/yr against Amarakaeri.

## 6. Comparison 2: year by year, against many zones (event study)

**Question:** Is the fall bigger than normal year-to-year noise?

**Model:** new mining in zone *z*, year *t* = zone effect + year effect + one Tambopata term per year (2018 left out).
`y_zt = α_z + γ_t + Σ_k β_k · [z = Tambopata] · [t = k] + ε_zt`

- **Zone effect (α):** each zone's normal level.
- **Year effect (γ):** each year's shock shared by all zones: gold price, COVID.
- **β_k:** how far Tambopata sits from the others in year *k*, relative to 2018.

**Fake place test:** give the "operation" to each other zone in turn. Tambopata should be the most extreme. It ranks 1 of {{placebo_space_n_units}}.

**Why no error bars:** with one treated zone, standard errors are not trustworthy (Conley and Taber, 2011). The rank is our honest substitute.

**Code:** `code/peru.py` (`run_event_study`), estimated with `pyfixest`.

## 7. Comparison 3: harder controls (model ladder)

**Question:** Does the fall survive stronger controls?

| Model | Adds | What it rules out |
|---|---|---|
| **M1** | zone + year effects | shared shocks (gold price, COVID) |
| **M2** | + each zone's pre-2019 size × log gold price | big zones reacting more to a price rise |
| **M3** | + a straight-line trend per zone | zones that were already drifting apart |
| **M4** | outcome scaled to each zone's own 2014–18 average | Tambopata's size driving the result |

Each model also runs with a **fake 2016 date** on 2011–18 data. A trustworthy model shows a big real effect and a small fake one.

**Result:** the 2019–21 gap is {{model_m1_during}} to {{model_m3_during}} ha/yr; fake dates are 4–9 times smaller; Tambopata ranks first every time.

**Code:** `code/peru_models.py`. The numpy fit is checked against `pyfixest`.

## 8. Comparison 4: a synthetic twin (add-on)

**Question:** Can a weighted mix of other zones copy Tambopata before 2019?

**How:** find weights (≥ 0, summing to 1) on other zones so the mix tracks Tambopata in 2010–18. After 2019, the gap between Tambopata and the mix is the estimated effect.

**Why it fails here:** Tambopata added more mining than any other zone. A weighted average of small numbers can't reach a big one. It only works after scaling each zone to its own size.

**Code:** `code/peru_synth.py`.

## 9. Comparison 5: one real twin, by rules (Ruby's design)

**Question:** Is there one existing area that looks like La Pampa but had no operation?

**Rules, applied to {{ctl_n_areas}} areas across the Amazon:**
1. **R1** mining before 2019 (≥ 500 ha seen by AMW by 2018)
2. **R2** no operation reported 2017–25 (documented web search, every query logged)
3. **R3** outside Madre de Dios
4. **R4** lowland mining (< 500 m) of similar scale (≥ ⅕ of Tambopata); the closest match wins

**Result:** no area passes. Relaxing R2 to "no operation in 2017–21" gives **Amanã National Forest** (Brazil).

**Comparison:** new mining per year as a share of each area's own 2018 mining, same product (AMW) for both. The pre-2019 trend comes from each area's own MapBiomas collection, shown side by side, never subtracted.

**Code:** `code/control_amw.py`, `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py`.

## 10. Brazil: staggered operations

**Question:** Do territories fall after *their own* operation?

**How:** AMW new mining per territory, 2019–25. Each territory is compared with its own first operation date. A pool of territories with no operation found shows the background trend.

**Logic:** if operations cause falls, each territory should fall after its own date, not before. Munduruku fell before, so the timing alone can't credit the operations.

**Code:** `code/brazil_stagger.py`, `brazil_deter_all.py`.

## 11. How we label claims

| Label | Means | Example |
|---|---|---|
| [[D]] description | what happened | "new mining fell from 1,640 to 163 ha/yr" |
| [[P]] prediction | what we expect next time | "a rebound within ~3 years" |
| [[C]] causal | what caused it | used once, *conditional* on the comparison areas being a fair counterfactual |

**Why it matters:** The grading puts 30% on honesty about the claim. A causal claim by accident is the main way to lose points.

## 12. Plan v2 methods (built 12 Oct 2026)

**Displacement layers** (`code/raster_layers.py`):
- **Stream chart:** land mined for the first time, per zone and year. First-time mining ignores year-to-year map flicker.
- **Sankey:** per period, new mining split into new land vs old pits, flowing into zones. Flows are pixels, not people.
- **Road bands:** 1-km strips north and south of the highway, inside the La Pampa longitudes.
- **Corridor share:** first-time mined land inside the legal corridor, as a share of Madre de Dios.

**Fake start dates for the road** (`code/v2_tests.py`, T1): the north share's change, 3 years after minus 3 years before, for every start year 2008–2022. The 2019 move ranks 3 of 15; 2008 (Guacamayo boom) moved more.

**Quarterly timing** (`code/glad_alerts.py`): University of Maryland GLAD-L forest-loss alerts, each pixel dated to the day, 2017–2026. We keep alerts on land MapBiomas maps as mining. Compare the same quarter across years (clouds); data version break in 2021.

**Gold left** (`code/raster_gold.py`): gold-bearing land = INGEMMET geology units (river deposits plus Madre de Dios Formation terraces). Validation: 90% of all land ever mined lies on them. Depletion = share of a zone's gold-bearing land mined by a year.

**Enforcement intensity** (`code/v2_tests.py`, T8): Peru's anti-illegal-mining programme (PP 0128), executed spending booked in Madre de Dios, 2015–2025. Department level only; a lower bound.

**Earlier wave** (T3): model M1 with Tambopata × 2012–13 on 2008–16 data. Tambopata did not fall more than other zones.

**Sensitivity and products** (T4, T5): narrow and wide La Pampa windows give the same picture. Course table and raster give the same net numbers; first-time mining and old pits split them.

| Step | Status |
|---|---|
| S1 zone map | done; waiting for team review |
| S2 pixel accounting | done |
| S3 stream, Sankey, road bands, corridor share | done |
| S3b gold-left proxy | done |
| S4 comparisons on the new zones | course-table models kept; v2 adds fake-date test for the road |
| S5 2012–14 wave | done (no Tambopata-specific dip) |
| S6 quarterly alerts | done |
| S7 enforcement intensity | done (department spending only) |
| S8 products table | done |

**Code map:** see the walkthrough, section 22. **Plan and decisions:** `docs/PLAN_v2.md`, `docs/overnight/LOG.md`.
