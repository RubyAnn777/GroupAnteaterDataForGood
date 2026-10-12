# Mercurio stopped La Pampa for two years. Then mining crossed the road.

> What Operation Mercurio did to illegal gold mining in Madre de Dios, Peru, and what FZS should expect when an operation ends. Team walkthrough: the story first, every analysis behind it, every number from `output/numbers.csv`.

- **1,640 → 163** ha/yr of net new mining in the Tambopata buffer zone, 2016–18 vs 2019–21
- **49% → 72%** share of new mining inside the legal corridor, 2016–18 vs 2022–25
- **5,317 → 11,373** ha/yr of first-time mining in all of Madre de Dios: the region did not mine less
- **21%** of La Pampa's gold-bearing land mined by 2018: the gold was not gone

---

**Part: The story**

## Enforcement worked where it landed, while it lasted

**Mercurio cut mining in La Pampa for about two years. Miners answered across the nearest legal boundary and in old pits, and the region kept growing.**

1. **Before:** La Pampa was Peru's largest illegal mining area: 1,640 ha of net new mining a year (2016–18).
2. **During:** Net new mining fell to 163 ha/yr in 2019–21. Clearing went on through 2019 and collapsed in 2020.
3. **Next door:** First-time mining directly across the highway, in the legal corridor, rose from 69 to 463 ha/yr.
4. **After:** La Pampa came back to 1,829 ha/yr in 2022–25, much of it on old pits. In 2025 miners entered the reserve.
5. **Region:** First-time mining in Madre de Dios doubled, from 5,317 to 11,373 ha/yr.

**Is it causal?** Only conditionally, and only for **net** new mining in 2019–21. In hectares, Tambopata's fall is the largest of 15 zones (p = 0.07, the best this test allows) and sits below two rule-based twins. Relative to its size the fall is ordinary, and per 1-km cell the pre-trends fail. **[causal]**

**Why it matters:** an operation buys a pause, not an end. FZS should plan for what comes after the patrols leave: the legal side of the boundary, old pits, and the river posts.

## Four parts, one figure, one conditional causal sentence

**The 2-page brief tells the story above in the course's four parts.** The brief draft has its own page: [the brief draft](../brief/BRIEF_DRAFT.md).

| Brief part | What it says | Evidence on this page |
|---|---|---|
| **1. The question** | FZS pays for enforcement. What happens in the target, and around it, when an operation ends? | [The rules](#the-rules), [The places](#the-places) |
| **2. Data** | MapBiomas Peru Collection 4, one check per dataset | [Appendix](#appendix) |
| **3. Findings** | Fell for two years, crossed the road, came back; the region grew. One conditional causal claim. | [Where it went](#where-it-went) to [Tests](#tests) |
| **4. What FZS can do** | Stay longer, guard the boundary, watch old pits, make the corridor a filter. Satellites miss dredges and mercury. | [For FZS](#for-fzs), [Claims](#claims) |

![La Pampa fell as the corridor across the road rose, and the department as a whole kept growing. This is the brief's one figure.](../../output/fig_brief_main.png)

*How to read it:* Top: land mined for the first time each year in La Pampa (orange) and in the legal corridor directly across the highway (blue). Faint bands = period means. Bottom: all of Madre de Dios, inside (blue) and outside (grey) the corridor. Shaded = operation years.

*Takeaway:* La Pampa fell as the corridor across the road rose, and the department as a whole kept growing. This is the brief's one figure.

<details><summary>Go deeper: How to read this page: claim labels and a plain-word glossary</summary>

**Claim labels.** **[description]** what happened · **[prediction]** what we expect next time · **[causal]** what caused it. The course grades honesty about claims (30%), so every claim carries one.

**Each chapter has two layers.** The visible layer is the claim, the figure and the key numbers. "Go deeper" holds methods, tables, tests, caveats and code.

| Term | Meaning here |
|---|---|
| **La Pampa sector** | Tambopata buffer zone between 70.15° and 69.80° W, south of the highway. The operation's target. Our boundary; no official one exists. |
| **Legal mining corridor** | Where small-scale mining may be permitted (D.L. 1100, 2012). North of the highway. |
| **Corridor across the road** | The corridor within 10 km north of the highway, opposite La Pampa. |
| **Extra buffer zone** | Amarakaeri buffer zone, west of the corridor; Mercurio was extended there from late 2019. |
| **First-time mining** | Pixels mapped as mining for the first time since 1985 (MapBiomas, 30 m). |
| **Return to old pits** | Pixels mined before, not last year, mined again now. |
| **Net new mining (addition)** | Mining area this year minus last year. The course measure. |
| **Fixed effects** | A regression that removes each place's normal level and each year's shared shock (gold price, COVID). |
| **Clustered errors** | Uncertainty that allows nearby places to move together. |
| **Fake date / fake place** | Pretend the operation happened earlier or elsewhere. A real effect should stand out. |
| **p-value** | Chance of a result this large if nothing happened. Below 0.05 = unlikely to be chance. |
| **Rule-based twin** | An existing area picked by fixed rules to show what might have happened without the operation (Ruby's design). |

</details>

---

**Part: Background**

## Where you mine decides whether it's a crime

**La Pampa is illegal by location. The corridor across the road is not.** Moving 2 km north turns a crime into an administrative problem.

- **Illegal (D.L. 1105, 2012):** mining in a prohibited zone or with banned equipment. A crime.
- **Informal:** the same failings inside a permitted zone, by someone registered for formalization (REINFO). Not a crime.
- **Formalization barely happens:** in 2021, 9,592 Madre de Dios miners were registered, but only 145 were fully formal (Plan Restauración 2021).
- **Taxes are near zero:** 0% royalty for small producers (Ley 28258); raw gold VAT-exempt, 1.5% withheld on sale.

**Why it matters:** the operation raised the cost of mining in one place, while the legal corridor next door stayed cheap. That alone predicts displacement across the road.

<details><summary>Go deeper: The legal detail, who mines, and the enforcement timeline</summary>

**The corridor (D.L. 1100, 2012):** about 4,983 km² where small-scale mining can be permitted. Outside it, no concessions are granted. La Pampa covers about 1,241 km² (MINAM 2016). Congress has extended REINFO again and again, now to 31 December 2026.

**How MAAP grades illegality (MAAP #235):** Very high = inside a protected area; High = outside any concession; Medium = inside a concession not verified as active; Low = inside an active concession.

**Who mines:** about 46,605 artisanal miners in Madre de Dios, of whom 31,390 informal and 9,323 illegal (ACCA & USAID 2022). About 35% of the department's population is directly linked to mining.

**What each zone costs a miner:**

| Zone | Status | Main cost |
|---|---|---|
| La Pampa (buffer zone) | illegal | enforcement risk: seizure, eviction, prison |
| Corridor across the road | legal if titled | taxes, permits, competition for space |
| Extra buffer zone (Amarakaeri) | illegal | enforcement risk (Mercurio extended there) |
| Tambopata reserve | illegal, highest risk | enforcement; only one river, far from the highway |
| Native communities | depends on concession | community consent; mixed legality |

**Fuel:** tax-exempt in the Amazon; 72% of that benefit went to illegal mining (IPE).

**Who enforces, and when:**

| When | What |
|---|---|
| 2009–2010 | First interdictions; dredges banned (DU 012-2010) |
| Feb–Apr 2012 | D.L. 1100 (corridor, interdiction) and D.L. 1105 (formalization), under President Humala |
| 2013–2016 | Interdictions fade: 49 (2013) → 1 (Jan–May 2016) in Madre de Dios |
| Nov 2018 | La Pampa plan approved (later "Mercurio"), under President Vizcarra |
| 19 Feb 2019 | **Operation Mercurio:** 1,272 police, 300 soldiers, 70 prosecutors; monthly rotation of garrisons and commanders against corruption (Dethier et al. 2023) |
| 2019 | "Mercurio II" extends operations to all of Madre de Dios and border provinces of Cusco and Puno; Dec 2019 interdiction in the Amarakaeri buffer zone |
| Spring 2020 | Forces pulled away for COVID; deep budget cuts |
| Jul 2021 | Plan Restauración replaces Mercurio; adds Camanti and Ayapata |
| 2021–2022 | President Castillo; ministerial churn; enforcement relaxes |
| Apr 2023 → | State of emergency in six districts |
| 2025 | Navy withdrawn from Malinowski river posts; mining enters the reserve |

**FZS's role:** FZS supports SERNANP's law-enforcement operations, ranger control posts and patrols in the Tambopata–Bahuaja-Sonene landscape. So FZS is part of the enforcement we study.

**Sources:** `docs/overnight/notes/qualitative_background.md` (every item with a link and a quote).

</details>

## Four zones and a road

**We cut one satellite map into zones that match the law:** La Pampa, the corridor across the road, the extra buffer zone, the reserve, plus native communities and the rest. **[description]**

![The corridor across the road has the same gold and the same road as La Pampa, without the enforcement risk. The reserve has gold too, but no road.](../../output/fig_v2_zone_map.png)

*How to read it:* Coloured areas are zones; dark pixels were mapped as mining at least once since 1985. The thick line is the Interoceanic Highway; dotted lines mark La Pampa's longitudes.

*Takeaway:* The corridor across the road has the same gold and the same road as La Pampa, without the enforcement risk. The reserve has gold too, but no road.

**Why it matters:** "Tambopata buffer zone" mixes La Pampa (shut down) with new fronts. The zone map separates the stories.

<details><summary>Go deeper: Zone profiles, boundary checks and choices</summary>

**What each zone offers a miner** (study area around La Pampa):

| Zone | Status | km to highway | km to river | Gold-bearing land | Mined by 2018 |
|---|---|---:|---:|---:|---:|
| La Pampa sector | illegal | 7.4 | 1.5 | 99% | 21% |
| Corridor across the road | legal if titled | 5.0 | 2.2 | 100% | 8% |
| Rest of mining corridor | legal if titled | 24.9 | 2.0 | 85% | 9% |
| Reserves and parks | illegal | 36.1 | 3.8 | 81% | — |

- **Data:** MapBiomas Peru Collection 4 maps for every year 1985–2025 (30 m pixels), the same product as the course tables.
- **Check:** the raster gives the Tambopata buffer zone 20,716 ha in 2025 (table: 20,730) and the reserve 776 ha (platform: 777).
- **Boundary choice:** a narrower and a wider La Pampa window give the same result (fall of −52% and −48%); we keep the middle one.
- **Boundaries change:** the current Tambopata buffer zone dates from 2005, Amarakaeri's from 2016; the corridor from 2012. We apply today's boundaries to every year, as MapBiomas does.

**Code:** `code/raster_zones.py`, `code/v2_extra.py` (zone profile).

</details>

---

**Part: What happened**

## New mining moved into the legal corridor

**After 2019, land mined for the first time shifted from La Pampa to the legal corridor.** The corridor's share rose from 49% to 72%. **[description]**

![The orange La Pampa band thins after 2019, while the blue corridor bands widen and the total keeps growing.](../../output/fig_v2_stream.png)

*How to read it:* Hectares mined for the first time each year in Madre de Dios, stacked by zone; numbers are yearly totals. Shaded = operation years.

*Takeaway:* The orange La Pampa band thins after 2019, while the blue corridor bands widen and the total keeps growing.

- **La Pampa sector:** 1,395 → 722 → 987 ha/yr (2016–18 → 2019–21 → 2022–25). **[description]**
- **Corridor across the road:** 69 → 463 → 538 ha/yr. **[description]**
- **All Madre de Dios:** 5,317 → 6,571 → 11,373 ha/yr. **[description]**
- **Independent check:** MAAP #208 finds 74% of 2021–24 mining deforestation inside the corridor; we find 72% for 2022–25.

![The corridor's share stepped up after 2019 and stayed high.](../../output/fig_v2_corridor_share.png)

*How to read it:* Each point is one year's share of Madre de Dios first-time mining that lies inside the legal corridor.

*Takeaway:* The corridor's share stepped up after 2019 and stayed high.

**Not all corridor growth is displaced La Pampa mining.** The rest of the corridor gained far more than La Pampa lost (2,450 → 7,638 ha/yr), so new entrants and the gold price drive most of it.

![The presumed-illegal share fell, and the grey zone of unverified concessions grew.](../../output/fig_v2_legality.png)

*How to read it:* First-time mining in Madre de Dios split by MAAP's legality grade: Low = active concession, Medium = concession not verified as active, High = outside any concession, Very high = strict protected area.

*Takeaway:* The presumed-illegal share fell, and the grey zone of unverified concessions grew.

- **Presumed illegal (High + Very high):** 41% → 25% → 21% of first-time mining. **[description]**
- **The grey zone grew:** concessions not verified as active took 18% → 30% → 37%. **[description]**

![A second product agrees on the move north of the road; it counts less infill after 2021.](../../output/fig_v2_amw_robustness.png)

*How to read it:* The same zones measured with a second satellite product, Amazon Mining Watch (480 m squares, from 2018).

*Takeaway:* A second product agrees on the move north of the road; it counts less infill after 2021.

**Why it matters:** Mercurio moved new mining from illegal land to legal land. For the reserve that is a win. For the region it is not: total new mining kept growing, and corridor mining still uses mercury.

<details><summary>Go deeper: Legality details, the second product, the cell test, and what we can't show</summary>

- **Presumed illegal share** (outside the corridor and outside communities, simple rule): 31% → 15% → 13%. **[description]**
- **Inside the legal corridor**, 36% of all first-time mining since 1986 sits on land without a verified active concession. **[description]**
- **Time-consistent check:** counting a concession only if it was filed by the mining year gives 42% → 26% → 22% presumed illegal and 18% → 37% grey zone: the same picture.
- **Amazon Mining Watch:** in the La Pampa longitudes, the share of new mining north of the road was 68% in 2019 and 87% in 2021. **[description]**
- **Why the products disagree after 2021:** AMW flags a 480 m square only once; MapBiomas counts every new 30 m pixel. 68% of MapBiomas's first-time mining in the corridor in 2022–25 lies inside AMW squares flagged earlier, so AMW can't count it again. They agree on the move across the road and differ on infill.
- **Statistical test:** per 1-km cell, the corridor across the road gained +0.94 ha per cell-year in 2019–21 relative to clean comparison cells (p = 0.01). The comparison excludes the corridor and communities, so it isn't itself a displacement target ([Attempt 1](#attempt-1)).
- **The 2023 spike** appears region-wide and may partly be a map artefact.
- **Can't show:** that the *same* people moved. New arrivals and the gold price fit the same picture.

**Code:** `code/raster_layers.py`, `code/v2_legality.py`, `code/v2_extra.py` (AMW).

</details>

## Miners crossed the highway, then pushed deeper

**Right after Mercurio, new mining piled up 0–2 km north of the highway, directly across from La Pampa.** The north side's share went from 23% (2016–18) to 65% (2019–21). **[description]**

![The mass of new mining jumped from the south side to the strips just north of the road.](../../output/fig_v2_road_bands.png)

*How to read it:* Each bar is a 1-km strip parallel to the highway, inside La Pampa's longitudes. Orange = south (buffer-zone side), blue = north (corridor side). Height = land mined for the first time per year.

*Takeaway:* The mass of new mining jumped from the south side to the strips just north of the road.

![No fake start year shows a bigger jump north than 2019, among windows that don't overlap the event.](../../output/fig_v2_road_placebo.png)

*How to read it:* The change in the north side's share for every possible start year: 3 years after minus 3 years before. The real 2019 start is highlighted.

*Takeaway:* No fake start year shows a bigger jump north than 2019, among windows that don't overlap the event.

![Right after Mercurio new mining hugged the road; then it pushed deeper into the corridor.](../../output/fig_v2_depth.png)

*How to read it:* Mean distance north of the highway of each year's first-time mining, with the 0–10, 10–20 and 20–30 km bands.

*Takeaway:* Right after Mercurio new mining hugged the road; then it pushed deeper into the corridor.

- **The jump is unusual:** rank 1 of 8 non-overlapping start years (p = 0.12, the smallest possible). **[description]**
- **Hugging the road:** mean depth fell from 20 km (2016) to 13 km (2020), then reached 19 km by 2025. **[description]**

**Why it matters:** miners follow enforcement and gold across a two-lane road. Any operation south of the highway should expect a response north of it.

<details><summary>Go deeper: The road has been crossed before, plus every test</summary>

- **All start years:** the 2019 move north (+0.41 share points, within 30 km) ranks 2 of 15 start years (p = 0.13); only 2020, whose window overlaps the event, is higher.
- **History:** in 2008–10 most new mining was north of the road (the Guacamayo boom; share 93% in 2008). It moved south to La Pampa by 2015 (19%), then back north after Mercurio (82% in 2021). **[description]**
- **Depth break:** after 2019, −8.8 km net of trend (p = 0.000, Newey-West). **[description]**
- **Per 1-km cell:** 10–20 km north gained most after 2022, +2.9 ha per cell-year (p = 0.000) relative to cells 10–30 km south. **[description]**
- **Boundary choice doesn't matter:** a narrower or wider La Pampa window changes the La Pampa fall from −52% to −48%.

**Code:** `code/raster_zones.py` (road bands), `code/v2_tests.py` (T1, T4, T9), `code/v2_stats.py` (road gradient).

</details>

## Returns to old pits hide inside the net numbers

**In 2023, most new mining in La Pampa happened on old pits, not on new land.** The course's net table can't see this. **[description]**

![Returns to old pits grew in every period, and La Pampa's comeback leaned on them.](../../output/fig_v2_sankey.png)

*How to read it:* Left: where each period's new mining came from (new land, or old pits mined again). Right: the zone it appeared in. Width = hectares per year, on the same scale in all three panels.

*Takeaway:* Returns to old pits grew in every period, and La Pampa's comeback leaned on them.

- **La Pampa, returns to old pits:** 252 → 379 → 893 ha/yr. **[description]**
- **Share of all new mining on old pits:** 25% → 32% → 32%. **[description]**
- **Independent check:** MAAP #193 reports miners back on degraded land in La Pampa in 2023.

![The corridor holds most returns too; La Pampa's own returns jump in 2023.](../../output/fig_v2_stream_remined.png)

*How to read it:* Hectares of returns to old pits each year, stacked by zone (Ruby's request).

*Takeaway:* The corridor holds most returns too; La Pampa's own returns jump in 2023.

**Why it matters:** an operation can stop clearing while miners quietly return to old pits. FZS should monitor old mining sites, not only forest edges.

<details><summary>Go deeper: Net vs gross, and the map-flicker caveat</summary>

**Net vs gross, Tambopata buffer zone (ha/yr):**

| | 2016–18 | 2019–21 | 2022–25 |
|---|---:|---:|---:|
| Net addition (course table) | 1,640 | 163 | 1,829 |
| First-time mining | 2,015 | 1,061 | 1,344 |
| Return to old pits | 344 | 514 | 1,139 |

- **The corridor's share of all returns:** 59% → 62% → 61%. **[description]**
- **La Pampa's share of all returns:** 13% → 12% → 15%. **[description]**
- **Caveat:** the old-pit count includes year-to-year map flicker (about 300 ha/yr even before 2019). Trust the 2023 jump, not small changes.

**Code:** `code/raster_layers.py` (Sankey), `code/v2_extra.py` (returns by zone).

</details>

## Clearing in La Pampa went on through 2019

**Forest clearing on La Pampa's mining land did not stop in February 2019.** It was higher in 2019 than in 2018 and collapsed only in 2020–21. **[description]**

![La Pampa's alerts stayed high through 2019 and nearly stopped in 2021–23; across the road they rose from mid-2019.](../../output/fig_v2_glad_quarterly.png)

*How to read it:* Forest-loss alerts per quarter (University of Maryland GLAD, Landsat, each pixel dated to the day), counted only on land MapBiomas maps as mining.

*Takeaway:* La Pampa's alerts stayed high through 2019 and nearly stopped in 2021–23; across the road they rose from mid-2019.

- **La Pampa, alerts on mining land:** 936 ha (2017), 987 (2018), **1,385 (2019)**, 275 (2020), 35 (2021). **[description]**
- **Corridor across the road:** 56 ha (2018) → 189 (2019) → 209 (2020). **[description]**

**Why it matters:** the brief must say clearing fell **from 2020**, not "immediately". This matches Dethier et al. (2023): activity spiked in La Pampa's northwest after the operation.

<details><summary>Go deeper: Sentinel-2 cross-check and caveats</summary>

- **Sentinel-2 alerts** (every 5 days) in western La Pampa: 532 ha in March–September 2019 (168 ha in August alone), vs 362 ha in the same months of 2020. So 2019 clearing was real, not cloud delay.
- **Caveats:** clouds bunch alerts in the dry season, so compare the same quarter across years. The data version changes in 2021. Alerts need standing forest, so returns to old pits never show.

**Code:** `code/glad_alerts.py`.

</details>

## La Pampa had not run out of gold

**By 2018, La Pampa had mined only 21% of its gold-bearing land.** About 41,574 ha were left. "Miners left because the gold ran out" is unlikely. **[description]**

| Gold-bearing land already mined | by 2018 | by 2025 |
|---|---:|---:|
| La Pampa sector | 21% | 33% |
| Corridor across the road | 8% | 18% |
| Rest of mining corridor | 9% | 19% |
| Kotsimba | 20% | 31% |

**Why it matters:** enforcement, not exhaustion, is the better explanation for the move.

<details><summary>Go deeper: How we measured gold in the ground</summary>

- **The proxy:** no one publishes gold left in the ground. Gold here is alluvial, so we used the national geology map (INGEMMET, 1:100,000): river deposits plus the gold-bearing terraces of the Madre de Dios Formation.
- **Does it work?** 90% of all land ever mined lies on these units, which cover 47% of Madre de Dios (1.9× more mining than chance). The strict river-deposit units cover 16% and hold 64% (4.1×). La Pampa was 21% depleted by 2018 under the strict definition too.
- **Limits:** the map is coarse and says nothing about gold grade; old pits can be mined again.

**Code:** `code/raster_gold.py`.

</details>

## In 2025, miners entered the reserve

**The course data covers only buffer zones. Inside Tambopata National Reserve, mining reached 777 ha in 2025, 241 ha of it new that year.** **[description]**

![Inside the reserves, mining stayed small for years; in 2025 it jumped inside Tambopata.](../../output/fig_peru_inside_reserves.png)

*How to read it:* Mining area inside each reserve compared with its buffer zone, from the MapBiomas protected-area statistics we downloaded (checked: 777 ha on the platform).

*Takeaway:* Inside the reserves, mining stayed small for years; in 2025 it jumped inside Tambopata.

- **Two other sources agree:** MAAP #241 reports ~500 ha of new mining inside the reserve (late 2025 to Feb 2026); Amazon Mining Watch shows 640 ha in 2025 (provisional). **[description]**
- **The trigger:** the 2025 incursion came after the navy left its Malinowski River posts (MAAP #241).

**Why it matters:** this is FZS's core area, and the most actionable finding.

<details><summary>Go deeper: The 2017 jump and the code</summary>

- The 2017 jump (+534 ha) looks partly like a map reclassification, not real mining. **[description]**

**Code:** `code/peru_anp.py`.

</details>

## The official gold drop is a definition change

**The official Madre de Dios gold series fell 88% from 2018 to 2025, but mostly because its definition changed.** Until 2019 it included an *estimate* of artisanal gold; from 2020 it counts only what producers declare. **[description]**

![The "collapse" is the estimate disappearing in 2020; declared output rose.](../../output/fig_peru_gold_definition.png)

*How to read it:* Madre de Dios gold in the ministry's yearly files, split into what producers declared and the artisanal estimate the ministry added.

*Takeaway:* The "collapse" is the estimate disappearing in 2020; declared output rose.

- **Declared output rose:** 944 kg (2018) → 1,362 kg (2025). The estimate was 6,002 kg in 2019 and is absent from 2020.
- **We withdrew** our earlier "collapse" and its break test: they measured the definition change.

**Why it matters:** official production says almost nothing about mining here. Don't cite "−88%".

<details><summary>Go deeper: The 2015 break, and the "mining in the corridor, declaring nothing" idea</summary>

- **The series:** the ministry's files carry "PRODUCTORES ARTESANALES — cifras estimadas" for Madre de Dios until 2019 (about 15.7 t in 2016, 6.0 t in 2019). In 2016, that estimate plus declared output equals the central bank's figure exactly.
- **An earlier break in 2015:** until 2014, artisanal producers' own declarations were in the series (8,032 kg in 2014); from 2015 producers declared only 556 kg and the ministry added an estimate.
- **For the idea:** 37% of first-time mining in 2022–25 sat in concessions not verified as active; producers declare about 1 t a year while first-time mining covers over 11,373 ha a year; only 145 of 9,592 registered miners were fully formal (2021); Bolivia's gold exports jumped from 1.7 t (2012) to 35.7 t (2014); nationally at least 80 of ~180 t exported in 2024 had unknown origin.
- **Against:** gold may be declared in other regions; mapped area includes re-mined pits; gold yield per hectare is unknown.
- **Label:** plausible mechanism, not a finding.

**Code:** `code/peru_gold_minem.py` (checked against the central bank for 2012 and 2019), `code/peru_production.py`. **Source:** `docs/overnight/notes/legality_data.md`.

</details>

## Enforcement comes in waves tied to governments and budgets

**Other events line up with the mining curve.** Enforcement money peaked in 2019 and faded; COVID pulled forces away in 2020; a new government arrived in 2021. **[description]**

![Both enforcement waves started within a year of a new president and faded within about two.](../../output/fig_v2_timeline.png)

*How to read it:* Top: events by type (enforcement, presidents, laws, context). Below: land mined for the first time each year in La Pampa and in all of Madre de Dios. Shaded: 2012–13 and 2019–21.

*Takeaway:* Both enforcement waves started within a year of a new president and faded within about two.

![Spending peaked in 2019 and fell as mining rebounded.](../../output/fig_v2_enforcement_spending.png)

*How to read it:* Executed spending of Peru's anti-illegal-mining programme (PP 0128) booked in Madre de Dios, next to first-time mined land. A lower bound: national units book under Lima.

*Takeaway:* Spending peaked in 2019 and fell as mining rebounded.

- **One dip, not two:** La Pampa first-time mining changed by +36% in 2012–13 vs 2010–11, and by −81% in 2020–21 vs 2017–18. **[description]**
- **Money:** 651,901 soles (2018), 31,120,611 (2019), 9,665,775 (2021), 5,008,539 (2025). **[description]**
- **Gold price:** up 2.7-fold from 2018 to 2025. It pushes everywhere at once, which the year effects in [Attempt 1](#attempt-1) remove.

**Why it matters:** FZS should plan for the gap after each wave.

<details><summary>Go deeper: Politics, COVID, the 2017 spike and the earlier wave</summary>

- **The political-cycle idea:** both enforcement waves started 7–11 months after a new president (Humala 2011 → decrees 2012; Vizcarra 2018 → Mercurio 2019). That's a pattern, not evidence; we found no study of Peruvian election effects (Brazilian studies find more deforestation in election years).
- **Earlier wave in the course table:** Tambopata's gap in 2012–13 was +628 ha/yr, rank 14 of 14: no Tambopata-specific dip. **[description]**
- **COVID:** forces left La Pampa in spring 2020; budgets fell sharply in 2020–21 (Mongabay 2023). That fits the 2022–25 rebound.
- **The 2017 spike:** 2017 was the record year for mining deforestation (Caballero Espejo et al. 2018). The gold price was flat (about $1,250/oz, 2016–18), so it doesn't explain it. Gangs ("Guardianes de la Trocha") ran extortion in La Pampa, but no source dates a 2017 takeover; part of the jump may be map reclassification. Mercury controls after Peru ratified the Minamata Convention (2016) made mercury a smuggling business; plausible, undocumented.

**Code:** `code/v2_extra.py` (timeline), `code/v2_tests.py` (spending, 2012 wave). **Sources:** `docs/overnight/notes/qualitative_background.md`, `enforcement_intensity.md`.

</details>

---

**Part: Is it causal?**

## One partly works, one half-works, one fails

**We tried three ways to build "what would have happened without Mercurio". None is clean.** Two point the same way for **net** mining in 2019–21.

| Attempt | Comparison | Pre-trends | Result |
|---|---|---|---|
| **1 Difference-in-differences** | Tambopata vs 14 other Peruvian buffer zones; per 1-km cell vs clean comparison cells | Zone level: averaged fake dates pass. Cell level: fail for La Pampa (p = 0.005) | Largest fall in hectares (rank 1 of 15, p = 0.07); **ordinary for its size** (rank 3 of 7) |
| **2 Synthetic control** | weighted mix of Peruvian zones | can't be met: La Pampa is too big | Fails for levels |
| **3 Rule-based twins** | two existing areas abroad (Amanã, Tapajós) | not parallel: Tambopata grew faster before 2019 | Tambopata below both in 2019–21 (descriptive, 3 years each) |

**Why it matters:** the bar is "anywhere close to causal". We get close for net mining in 2019–21, with every weakness stated.

## Largest fall in hectares, ordinary for its size

**In hectares, Tambopata's 2019–21 fall in net mining is the largest of 15 zones and survives controls for the gold price, trends and size.** Relative to its own size it is ordinary, and per 1-km cell the pre-trends fail. **[description]**

![Tambopata drops below the whole band in 2019–22 and comes back after.](../../output/fig_peru_event_study.png)

*How to read it:* Top: how far Tambopata sits from the comparison zones each year, relative to 2018 (= 0). The grey band is the range if each other zone had been "treated" instead. Bottom: the raw additions behind it.

*Takeaway:* Tambopata drops below the whole band in 2019–22 and comes back after.

![In hectares the real gap is large and ranks first under M1–M3; scaled to size (M4) it is only third. M3's fake gap has the same sign as the real one.](../../output/fig_peru_models.png)

*How to read it:* The 2019–21 gap under four models (M1 zone + year effects; M2 + gold price × size; M3 + own trends; M4 scaled to size), next to the same model with a fake 2016 start.

*Takeaway:* In hectares the real gap is large and ranks first under M1–M3; scaled to size (M4) it is only third. M3's fake gap has the same sign as the real one.

![The corridor across the road clearly rose; La Pampa's fall is borderline.](../../output/fig_v2_stats_zones.png)

*How to read it:* Change per 1-km cell in each zone, 2019–21 and 2022–25, relative to clean comparison cells, with 95% confidence intervals (clustered by 10-km blocks).

*Takeaway:* The corridor across the road clearly rose; La Pampa's fall is borderline.

![The corridor's pre-trends pass; La Pampa's don't, which weakens its cell-level fall.](../../output/fig_v2_stats_event.png)

*How to read it:* Year-by-year per-cell estimates for La Pampa and the corridor across the road, with 2014–18 as reference. Leads before 2014 test for pre-trends.

*Takeaway:* The corridor's pre-trends pass; La Pampa's don't, which weakens its cell-level fall.

- **Fake places:** Tambopata (−1,454 ha/yr) ranks 1 of 15 (p = 0.07, the smallest possible with 15 zones). **[description]**
- **Scaled to size (M4):** rank 3 of 7 (p = 0.43). Tambopata falls most in hectares because it is the biggest. **[description]**
- **Per cell:** La Pampa −1.21 ha per cell-year (p = 0.08; wild bootstrap p = 0.06); pre-trends fail (p = 0.005). **[description]**

**Why it matters:** honest wording is "consistent with a short-lived effect on net mining", not "proven".

<details><summary>Go deeper: The 2×2, the model ladder and the cell panel in full</summary>

**Level 1: the course's 2×2 (Tambopata vs the extra buffer zone, Amarakaeri)**

| ha of net new mining per year | Before 2016–18 | During 2019–21 | Change |
|---|---:|---:|---:|
| Tambopata (targeted) | 1,640 | 163 | −1,477 |
| Amarakaeri (extra buffer zone) | 289 | 574 | +285 |
| **Gap change** | | | **−1,762** |

- **Amarakaeri was itself treated** (Mercurio II, December 2019), so it is "less treated", not a control.
- **Baseline 2014–18 instead of 2016–18:** gap −1,663 ha/yr.
- **Target + neighbours (the card's check):** the three buffer zones together added 1,941 → 778 → 3,127 ha/yr: down during, above the old level after. **[description]**
- **Net is not new:** almost half of the net fall is old mining going out of use; first-time mining fell from 2,015 to 1,061 ha/yr ([Old pits](#old-pits)).

**Level 2: against all 14 other Peruvian buffer zones with mining**

- **Model:** net new mining = zone effect + year effect + Tambopata × period. Year effects remove the gold price, COVID and national policy (shared shocks).
- **Fake places:** each other zone gets the "operation" in turn, with Tambopata removed from its comparison pool. Placebo effects range −66 to +226 ha/yr. Among Amazon-department zones only: rank 1 of 8.
- **Dropping the largest comparison zone:** 2019–21 gap −1,595 ha/yr.

| Model | Adds | During 2019–21 | After 2022–25 | Fake 2016 | Rank |
|---|---|---:|---:|---:|---:|
| **M1** | Zone + year effects | −1,454 | 161 | 255 | 1 of 15 |
| **M2** | + bigger zones react more to gold price | −1,605 | −175 | 187 | 1 of 15 |
| **M3** | + each zone's own trend | −1,859 | −599 | −337 | 1 of 15 |
| **M4** | Scaled to each zone's size | −1.45 | −0.20 | −0.33 | 3 of 7 |

- **Fake dates:** M1 and M2 placebos have the opposite sign; M3's placebo (−337) has the same sign as the real effect, so not every model passes cleanly.

**Level 3: per 1-km cell, with standard errors**

- **Panel:** 14,241 cells, 2014–2025 (baseline 2014–18); cell and year fixed effects; errors clustered by 10 × 10 km blocks.
- **Clean comparison:** cells outside every named zone, the legal corridor and native communities (4856 cells). The earlier version used the rest of the corridor, where displaced mining went, which exaggerated La Pampa's fall.
- **Few treated clusters:** La Pampa covers 14 of the 161 clusters, so we add a wild cluster bootstrap.

| Per 1-km cell, ha/yr vs clean comparison | 2019–21 | p (clustered) | 2022–25 | p |
|---|---:|---:|---:|---:|
| La Pampa sector | −1.21 | 0.08 | −0.76 | 0.40 |
| Corridor across the road | +0.94 | 0.01 | +1.13 | 0.02 |
| Extra buffer zone (Amarakaeri) | −0.06 | 0.181 | +0.30 | 0.21 |
| Tambopata reserve | −0.07 | 0.057 | −0.03 | 0.655 |

- **Wild cluster bootstrap (999 draws, only 14 and 10 treated blocks):** La Pampa 2019–21 p = 0.06; corridor across the road p = 0.00.
- **Old, contaminated comparison:** La Pampa −1.39 ha per cell-year.
- **Robust to:** gold-bearing land × year effects (−1.20, p = 0.08); Poisson (−1.96 log points, p = 0.00).
- **Pre-trends:** with the pooled 2014–18 reference, La Pampa's 2010–13 leads are jointly different from zero (p = 0.005); the corridor across the road passes (p = 0.24).

**Code:** `code/peru.py`, `code/peru_models.py`, `code/v2_stats.py`.

</details>

## A synthetic twin can't copy La Pampa's size

**A weighted mix of Peruvian zones can't reach La Pampa's size, so this method adds only a weak extra check.** **[description]**

![In hectares the copy never fits; scaled, Tambopata's 2019–21 dip is the deepest, but six zones prove little.](../../output/fig_peru_synth.png)

*How to read it:* Left: hectares; right: each zone scaled to its own 2014–18 average. Top: real Tambopata vs its synthetic copy (they should overlap before 2019). Bottom: the gap, with grey lines for each donor zone posing as the target.

*Takeaway:* In hectares the copy never fits; scaled, Tambopata's 2019–21 dip is the deepest, but six zones prove little.

- **In hectares, no fit:** before 2019 Tambopata added 1,375 ha a year; the best mix only 32. It lay outside every other zone's range in 9 of 9 years. **[description]**
- **Scaled, a good fit:** Tambopata's dip is the deepest of 6 zones (rank 1). **[description]**

**Why it matters:** you can't average small numbers into a big one. That's why Attempt 1 compares *changes*, and why Attempt 3 had to look abroad.

<details><summary>Go deeper: What synthetic control is</summary>

A synthetic control builds a fake Tambopata from a weighted mix of other zones (weights ≥ 0, summing to 1), fitted to the years before 2019. After 2019, the gap between Tambopata and the mix is the estimate. It differs from Ruby's idea: a mix of many zones instead of one real twin.

**Code:** `code/peru_synth.py`.

</details>

## No untouched twin exists; the closest ones grew faster

**No area in the Amazon passes all four of Ruby's rules. Relax one, and two twins appear in Brazil.** In 2019–21 Tambopata added new mining at 40% of their median pace. **[description]**

**The rules (Ruby):** find one existing area with (R1) at least 500 ha of mining by 2018, (R2) no operation reported in 2017–25, (R3) outside Madre de Dios, and (R4) lowland mining at least a fifth of La Pampa's size. The closest survivor wins.

![Almost every big mining area in the Amazon got an operation, so no strict twin survives.](../../output/fig_control_funnel.png)

*How to read it:* Each bar is the number of areas left after one more rule (log scale).

*Takeaway:* Almost every big mining area in the Amazon got an operation, so no strict twin survives.

![Peru outside Madre de Dios has no big mining area; the candidates cluster in Brazil's Tapajós gold region.](../../output/fig_control_map.png)

*How to read it:* Each dot is an area with at least 500 ha of mining by 2018. Size = mining area; colour = what happened to it under the rules.

*Takeaway:* Peru outside Madre de Dios has no big mining area; the candidates cluster in Brazil's Tapajós gold region.

![Tambopata and Amanã grew alike before 2019; in 2019–21 Tambopata went flat while Amanã kept growing.](../../output/fig_control_compare.png)

*How to read it:* Left: new mining per year as a share of each area's 2018 mining (same product for both). Right: total mining area, 2018 = 100, each from its own MapBiomas collection (side by side, never subtracted).

*Takeaway:* Tambopata and Amanã grew alike before 2019; in 2019–21 Tambopata went flat while Amanã kept growing.

![Tambopata ran below both twins in 2019–21, but it also grew faster than them before.](../../output/fig_control_top3.png)

*How to read it:* Tambopata against the two twins that pass the relaxed rules: growth before 2019 and pace in 2019–21.

*Takeaway:* Tambopata ran below both twins in 2019–21, but it also grew faster than them before.

- **Relaxed rule:** no operation in 2017–21 only. 2 areas pass; best fit **Amanã National Forest**, then the Tapajós protection area. **[description]**
- **2019–21:** Tambopata 7.9% of its 2018 stock per year; Amanã 20.9%; Tapajós 18.4%. **[description]**

**Why it matters:** a second, independent comparison agrees with Attempt 1: another country, another data source, picked by rules, not results.

<details><summary>Go deeper: The funnel, the twin table, and what still threatens it</summary>

- 1,174 protected areas, buffer zones and indigenous territories screened. 31 had real mining before 2019; only 2 of those had no operation found, both small and unlike La Pampa; 7 more were unclear. **[description]**
- **Sources:** SERNANP (Peru), RAISG (other countries), FUNAI (Brazil's territories); Amazon Mining Watch for mining; a logged web search per area for operations; OpenTopoData for elevation.

| | Tambopata buffer zone | Amanã National Forest |
|---|---:|---:|
| Mining by 2018 (AMW, ha) | 21,362 | 23,916 |
| Median elevation of the mining (m) | 263 | 86 |
| Distance from La Pampa (km) | 0 | 1,511 |
| First operation found | Feb 2019 | Mar 2023 |

- **Before 2019 the two grew alike:** both stood at about half their 2018 size in 2014 (51 and 48). By 2021 Tambopata was flat (104); Amanã had grown to 165. **[description]**
- **First twin alone:** Tambopata added 7.9% of its 2018 mining per year vs Amanã 20.9% (38% of its pace).
- **After 2021 Amanã is spoiled:** its own operation came in March 2023. Use it for 2019–21 only.
- **Munduruku was dropped:** our search log records Operation Mundurukânia there in May 2021, inside the rule's window (search snippets, unverified).

| Twin | Growth gap before 2019 (log points/yr; p) | 2019–21 pace, % of 2018 stock | Gap vs Tambopata |
|---|---:|---:|---:|
| Amanã National Forest | +0.20 (0.08) | 20.9 | −13.0 |
| Tapajós protection area | +0.24 (0.02) | 18.4 | −10.5 |

- **No p-values for the gap:** three years per area make a t-test meaningless.
- **Pre-trends are not parallel:** Tambopata grew faster than both before 2019 (significant against Tapajós), and the two sides come from different MapBiomas collections.
- **Threats:** Brazil weakened enforcement in 2019–22, so the twins may have grown faster than "normal". "No operation found" is not proof of none. On Amazon Mining Watch, Tambopata's 2019 value is its highest after 2018; the fall shows from 2020.
- **Ruby's caution holds:** "no intervention" is too strict (no area passes); "comparable enforcement" needs zone-level enforcement data that isn't public.

**Code:** `code/control_amw.py`, `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py`, `control_top3.py`. Searches: `docs/overnight/notes/control_interventions.csv`, coded in `data_intermediate/operations_coded.csv`.

</details>

## The move across the road is clear; the fall in La Pampa is fragile

**Every movement and comparison, tested.** A critical referee found errors in our first round; all are fixed. **[description]**

| Movement or comparison | Test | Estimate | p |
|---|---|---:|---:|
| Tambopata's 2019–21 net fall vs 14 zones | fake places, Tambopata out of the pool | rank 1 of 15 | 0.07 |
| Same, scaled to each zone's size (M4) | fake places | rank 3 of 7 | 0.43 |
| La Pampa sector, per cell, 2019–21 | DiD, cell + year FE, clean comparison, clustered | −1.21 ha | 0.08 |
| Same | wild cluster bootstrap | — | 0.06 |
| La Pampa pre-trends (cells) | joint test of 2010–13 leads | — | 0.005 |
| Corridor across the road, per cell, 2019–21 | DiD, clean comparison | +0.94 ha | 0.01 |
| Extra buffer zone (Amarakaeri), 2019–21 | same | −0.06 ha | 0.181 |
| North of highway 10–20 km, 2022–25 | road-gradient DiD | +2.87 ha | 0.000 |
| Move north of the road in 2019 | fake start dates, non-overlapping windows | rank 1 of 8 | 0.12 |
| New mining hugged the road after 2019 | trend + break, Newey-West | −8.8 km | 0.000 |
| Brazil: falls after own operation | staggered DiD (did2s), clustered by territory | +0.54 log (wrong sign) | 0.17 |
| Brazil: same | randomization (2,000 shuffles) | — | 0.92 |

**How to read p:** below 0.05 = unlikely to be chance. With 15 zones the smallest possible randomization p is 0.07, so "rank 1 of 15" is as strong as that test gets.

**Why it matters:** the instructor will ask "is this significant?" This table answers each claim, including the ones that fail.

<details><summary>Go deeper: What the referee found, and what we changed</summary>

| Problem | Fix | Effect on the result |
|---|---|---|
| Fake-place test kept Tambopata as a control, so every placebo looked positive | Tambopata removed from each placebo's pool; Amazon-only pool added | Still rank 1 in hectares; **rank 3 of 7 scaled** |
| Causal number measured net change, called "new mining" | Claim reworded to net mining; first-time change reported | First-time mining fell less (2,015 → 1,061 ha/yr) |
| Cell comparison included the corridor (displacement target); baseline mislabelled; few treated clusters | Clean comparison cells; 2014–25 panel; pooled 2014–18 reference; wild cluster bootstrap | La Pampa −1.21 (was −1.39); pre-trends still fail |
| One twin (Munduruku) had a 2021 operation; t-tests on 3 values | Two twins; no p-values | Tambopata still below both |
| Brazil code skipped Kayapó's 2024 operation | First operation inside 2021–25 used | Estimate +0.54, still not significant |
| Road placebo windows overlapped the event | Non-overlapping start years only | Rank 1 of 8 (p = 0.12) |
| Legality used today's concessions for past years | Concession must be filed by the mining year | Illegal share 42% → 22% (unchanged picture) |
| Risk map tested on the same cells, no benchmark | Spatial hold-out + "mining nearby" benchmark | AUC 0.92 vs 0.91: adds little |
| Untraceable numbers (Sentinel-2, producer gold) | Now computed in code | See [Timing](#timing) and [Declared gold](#declared-gold) |

**Full review:** `docs/overnight/notes/critical_review_v2.md`.

</details>

---

**Part: Brazil**

## Same method, weaker result: the direction, not the cause

**The big Brazilian territories fell after 2022–24, but not after their own operations.** The staggered test finds no significant effect. **[description]**

![Yanomami fell from 2024, a year after its operation; other territories don't line up with their own dates.](../../output/fig_brazil_v2_pixels.png)

*How to read it:* First-time mining and returns to old pits per territory, MapBiomas Brazil Collection 11, measured with the same pixel method as Peru. Dates mark each territory's own first operation.

*Takeaway:* Yanomami fell from 2024, a year after its operation; other territories don't line up with their own dates.

- **Yanomami:** 518 ha/yr of first-time mining in 2019–22, 458 in 2023–25. **[description]**
- **Staggered DiD:** +0.54 log points (p = 0.17); randomization p = 0.92. Wrong sign, not significant. **[description]**
- **No spill next door:** rings around Yanomami got almost no new mining (0–10 km: 0.4 ha/yr after 2023). Miners went toward Venezuela and to territories like Sararé (ISA 2026; Greenpeace).

**Why it matters:** Brazil fits "enforcement plus tracing reduces mining", but national rules may matter as much as local operations. That's a lesson for Peru's corridor.

<details><summary>Go deeper: Data, checks, the test, and why the null</summary>

- **Data:** MapBiomas Brazil Collection 11 maps, 1985–2025, read only around each territory (24 territories with mining + two rings around Yanomami).
- **Check:** Kayapó mining 17,628 ha (2024) and 18,569 ha (2025) vs 17,632 and 18,573 on the platform. This fixes the old Brazil mismatch (Collection 10.1 vs the platform's Collection 11).
- **Test:** territory + year effects, each territory treated from its own first operation (11 of 24 territories); Gardner's two-stage estimator; randomization inference with 2,000 shuffles.
- **Why the null:** after correcting the dates (Munduruku from May 2021; Kayapó from September 2024), territories still don't fall faster after their own operation. Sararé surged as its operation began, and the test has little power.
- **Products disagree on Yanomami's timing:** MapBiomas shows the fall from 2024; Amazon Mining Watch from 2023 (8,570 → 3,961 ha); MAAP #242 reports about 1,800 ha (2022) and 330 ha (2023).
- **Support:** Amazon Mining Watch shows Yanomami −63% after its operation; IBAMA fines fell 2019–22 while mining tripled, then reversed in 2023.
- **Challenge:** a national change in January 2023 (new government, end of the gold "good faith" rule, electronic gold invoices from August 2023) hit all territories at once, which a territory-level design can't separate.

**Code:** `code/brazil_raster.py`, `code/brazil_v2.py`, plus `brazil_stagger.py` (AMW), `brazil.py`, `brazil_ibama.py`.

</details>

---

**Part: So what**

## Stay longer, guard the boundary, watch old pits

**Keep enforcement on longer than two years, patrol the legal side of the boundary, watch old pits, and push tracing inside the legal corridor.** **[prediction]**

1. **Expect the response across the nearest legal boundary.** New mining jumped into the corridor right across the highway, then went deeper.
2. **Monitor old pits, not only forest edges.** In 2023 most new mining in La Pampa was on old pits. Forest-loss alerts never see this.
3. **Keep river posts staffed.** The 2025 incursion into the reserve followed the navy's withdrawal from the Malinowski posts (MAAP #241).
4. **Make the legal corridor a real filter:** proof of gold origin, gold-buyer registers, real formalization deadlines, mercury checks. Brazil's 2023 reforms are a model.

![Risk clusters next to old mining; the model adds little beyond "is there mining nearby?" and misses river-borne incursions.](../../output/fig_v2_risk_map.png)

*How to read it:* Predicted chance that a 1-km cell gets first-time mining in 2026–28, from a model trained on 2019–21 and tested out of sample on 2022–25.

*Takeaway:* Risk clusters next to old mining; the model adds little beyond "is there mining nearby?" and misses river-borne incursions.

- **Where to look next:** the model flags 672 high-risk cells outside the legal corridor: 261 in the La Pampa sector and 411 in native communities. **[prediction]**
- **Honest score:** AUC 0.92 on held-out 10-km blocks, barely above 0.91 for "mining nearby" alone. **[prediction]**

**Why it matters:** enforcement works while it lasts and where it lands. FZS can fund the "while" and watch the "where".

<details><summary>Go deeper: The social cost, and what data would let us say more</summary>

- **Damage:** each kg of gold mined in Peru costs US$81,000–364,000 (Conservation Strategy Fund calculator).
- **Mercury:** over a third of carnivorous fish exceed the limit hundreds of km downstream; exposed children score 4.68 IQ points lower.
- **Exploitation:** about 4,500 women are sexually exploited near camps, 78% of them minors.
- **Livelihoods:** about 46,600 people depend directly on mining. Enforcement without income alternatives invites return.
- **The corridor gap:** 0% royalty, 1.5% withholding, and only 145 of 9,592 registered miners fully formal (2021).
- **What would let us say more:** dated patrol and interdiction records per zone (SERNANP, FZS, police); concession and REINFO maps to grade legality pixel by pixel; pond-colour or dredge counts for activity on old pits and rivers.

</details>

## What we can say, and how strongly

| Claim | Label | Evidence for | Evidence against |
|---|---|---|---|
| Net new mining in Tambopata fell sharply in 2019–21 | **[description]** | Course table = raster; rank 1 of 15 | First-time mining only halved; clearing continued through 2019 |
| Mercurio caused the 2019–21 fall in net mining, roughly −1,454 to −1,859 ha/yr | **[causal]** *conditional* | Rank 1 of 15 in hectares (p = 0.07); below both twins | Ordinary relative to size; cell pre-trends fail; extra buffer zone also treated |
| New mining moved into the legal corridor, across the road, then deeper | **[description]** | Raster bands; depth break p < 0.01; AMW agrees; MAAP #208 (74%) | Can't show the same people moved; the road was crossed before (2008) |
| Miners returned to old pits in 2023 | **[description]** | Raster accounting; MAAP #193 | Map flicker inflates old-pit counts |
| La Pampa had not run out of gold | **[description]** | Geology: 21% mined by 2018 | Coarse map; no gold grade |
| The official gold series fell 88% | **withdrawn** | — | The series dropped its artisanal estimate in 2020; producer-declared gold rose |
| Corridor miners mine informally and don't declare | plausible, **not claimed** | Formalization rates, Bolivia exports, unknown-origin exports | No trace of where Madre de Dios gold is declared |
| The region mined less | **rejected** | — | First-time mining rose 5,317 → 11,373 ha/yr |
| Brazil: operations reduced mining | **not claimed** | Falls after 2022–24; AMW −63% Yanomami | Staggered DiD +0.54 (wrong sign, p = 0.17); national reforms in 2023 |
| Next operation: local fall while present, a move across the nearest legal boundary, a return within ~3 years | **[prediction]** | Peru pattern | One operation, one region; risk model barely beats "mining nearby" |

**Why it matters:** one labelled, conditional causal claim, with its failed tests shown, beats a vague strong one.

---

**Part: Team corner**

## What's blocked on you

**Only a human can do these:**

1. **Agree on the claim wording,** especially the one conditional causal sentence ([Three attempts](#three-attempts)). It's a team call.
2. **Ruby: check [The places](#the-places) and [Attempt 3](#attempt-3).** The zone map (we kept the middle La Pampa window) and her twin design. Should native communities inside the corridor count as legal?
3. **Confirm Brazil's scope with Raji** (appendix-level, as discussed).
4. **MAAP pages:** the site blocks scripts. Open each link in `docs/overnight/notes/maap_citations.md` and save it with File › Save Page As into `data_raw/maap/`.
5. **Re-open what you cite.** The course only allows sources you opened. Spot-check the operation searches for Amanã, Kayapó and Yanomami.
6. **Team plan:** add members and roles to `templates/TEAM_PLAN.docx`.
7. **AI prompt for brief part 4:** it was run in Claude (`docs/brief/ai_part4_raw.md`). If the course expects your own tool, re-run it.
8. **Merge:** the work sits on branch `analysis/v2-raster`. Opening a pull request into `main` is your call.

<details><summary>Go deeper: Nice to have, and the plan as a diagram</summary>

- **Munduruku before 2022:** search for operations in 2019–21. One may explain its early fall.
- **IBAMA embargo file:** no download link found.

| Step | Lane | Owner (role) | Missing data |
|---|---|---|---|
| 1. Share the walkthrough page with the team (it is private until shared) | Now (before Lesson 4) | Sebastian | none |
| 2. Ruby checks step 8: her four rules and the cut-offs | Now (before Lesson 4) | Ruby | none |
| 3. Agree the claim wording, esp. the one conditional causal sentence | Now (before Lesson 4) | whole team | none |
| 4. Re-open every cited source; save MAAP pages with "Save as" | Now (before Lesson 4) | each citer | raw MAAP HTML |
| 5. Fill in TEAM_PLAN.docx (members, roles) | Before Lesson 5 | team lead | none |
| 6. Edit the brief (section 15) to final; keep or re-run the AI prompt | Before Lesson 5 | writer + editor | none |
| 7. Build the replication zip; make slides from the walkthrough figures | Before Lesson 5 | data lead | none |
| 8. Ask FZS/SERNANP for dated patrol / interdiction records per zone | Optional / extension | team lead | enforcement intensity |
| 9. Brazil: search Munduruku operations 2019-21; Col 11 territory file | Optional / extension | Brazil analyst | news, MapBiomas |

</details>

## Where everything lives

**Run everything:** `uv run python code/main.py` (about 2 minutes). It writes every figure, table and number to `output/`.

<details><summary>Go deeper: The code map</summary>

| Chapter | Code | Main output |
|---|---|---|
| Checks against publisher numbers | `code/checks.py` | `output/checks.csv` |
| Attempt 1: measure, 2×2, event study, fake places | `code/peru.py` | `fig_peru_event_study.png`, `peru_placebo_in_space.csv` |
| Attempt 1: model ladder | `code/peru_models.py` | `fig_peru_models.png`, `peru_models.csv` |
| Attempt 1: cell panel | `code/v2_stats.py` | `fig_v2_stats_*.png`, `v2_stats_coefficients.csv` |
| Attempt 2: synthetic twin | `code/peru_synth.py` | `fig_peru_synth.png` |
| Attempt 3: rule-based twins | `code/control_*.py` | `fig_control_*.png`, `control_funnel.csv`, `control_top3_tests.csv` |
| Robustness (other comparison zones, drop largest) | `code/peru_robust.py` | `peru_robustness.csv` |
| The places: zones, pixel accounting | `code/raster_zones.py` | `fig_v2_zone_map.png`, `data_intermediate/zone_year_v2.csv` |
| Where it went, across the road, old pits | `code/raster_layers.py`, `code/v2_tests.py`, `code/v2_legality.py` | `fig_v2_stream.png`, `fig_v2_road_*.png`, `fig_v2_sankey.png` |
| Timing | `code/glad_alerts.py` | `fig_v2_glad_quarterly.png` |
| Gold left | `code/raster_gold.py` | `v2_gold_depletion.csv` |
| Inside the reserve | `code/peru_anp.py` | `fig_peru_inside_reserves.png` |
| Declared gold | `code/peru_gold_minem.py`, `code/peru_production.py` | `fig_peru_gold_definition.png` |
| Context: spending, timeline | `code/v2_tests.py`, `code/v2_extra.py` | `fig_v2_enforcement_spending.png`, `fig_v2_timeline.png` |
| Brazil | `code/brazil_raster.py`, `brazil_v2.py`, `brazil*.py` | `fig_brazil_v2_pixels.png` |
| For FZS: risk map | `code/v2_extra.py` | `fig_v2_risk_map.png` |
| The brief's figure | `code/brief_figure.py` | `fig_brief_main.png` |
| Every number | all of the above | `output/numbers.csv` |

- **Brief draft:** `docs/brief/brief_content.md` → `BRIEF_DRAFT.html`. **Methods:** [METHODS.html](METHODS.html).
- **Operation searches:** `docs/overnight/notes/control_interventions.md`, `brazil_data_and_operations.md`.
- **Log and decisions:** `docs/overnight/LOG.md`. **Data log:** `DOWNLOAD_LOG.csv`.
- **Big raw files are git-ignored** (Amazon Mining Watch, RAISG, MapBiomas Amazonía, FUNAI). The run then uses the small files in `data_intermediate/`. Download links are in `DOWNLOAD_LOG.csv`.

</details>

## Data checks, decisions and every number

**One check per dataset.** Full log in `DOWNLOAD_LOG.csv`.

| Data | Our number | Publisher shows | Status |
|---|---|---|---|
| MapBiomas Peru, Collection 4, buffer zones (course data) | Tambopata buffer zone 2025 = 20,730 ha | 20,730 ha | Match |
| MapBiomas Peru, Collection 4, protected areas (new) | Tambopata reserve 2025 = 776.9 ha | 777 ha | Match |
| MapBiomas Brazil, Collection 11, indigenous lands (course data) | 2025 = 39,915 ha | 39,915 ha (card) | Match |
| MapBiomas Brazil, Collection 10.1, per territory (new) | Kayapó 2024 = 18,176 ha | 17,632 ha (Collection 11) | Mismatch: different collection |
| MapBiomas Brazil, Collection 11 rasters (new) | Kayapó 2024 = 17,628 ha | 17,632 ha | Match |
| MapBiomas Peru, Collection 4 rasters (new) | Tambopata buffer zone 2025 = 20,716 ha | 20,730 ha | Match |
| MEF anti-illegal-mining spending (new) | Madre de Dios 2019 = 31,120,611 soles | 31,120,611 | Match |
| INPE DETER mining alerts (new) | 2019 = 105.64 km² | 105.40 km² | 0.2% off |
| Gold production, BCRP/MINEM (new) | Monthly sums = annual | — | Internal only |
| IBAMA fines (new) | — | No total online | Not checkable |
| World Bank gold price (course data) | Aug 2026 = $4,411/oz | $4,411/oz | Match |
| MapBiomas Amazonía, Collection 6 (new) | Amazon mining 2023 = 775,746 ha | 0.78 Mha (factsheet p.3) | Match |
| MapBiomas Brazil, Collection 11, mining module (new) | Garimpo 2025 = 445,987 ha | 445,987 ha | Match |
| RAISG protected areas (new) | 401 areas downloaded | 401 in the service | Match |
| Amazon Mining Watch | — | No totals published | Not checkable |

<details><summary>Go deeper: Decision log (from docs/overnight/LOG.md)</summary>

See `docs/overnight/LOG.md`.

</details>

<details><summary>Go deeper: Every number, filterable (from output/numbers.csv)</summary>

See [`output/numbers.csv`](../../output/numbers.csv).

</details>

---
*Built 2026-10-12 21:28 from git commit aabc940 (working tree may contain uncommitted changes). Numbers from output/numbers.csv (1053 rows).*
