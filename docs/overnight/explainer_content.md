<!--
Source of docs/overnight/EXPLAINER.html (the team walkthrough). Build: `uv run python docs/overnight/build_report.py`.
Placeholders {{id}} or {{id:fmt}} come from output/numbers.csv (default ",.0f"; unknown ids fail the build).
Claim tags: [[D]] description, [[P]] prediction, [[C]] causal.

Page syntax (parsed by build_report.py):
  # Title                      page headline (first line), "> " line right after = lede under it
  @part Name                   starts a part (TOC group + divider)
  ## Eyebrow | Headline        a chapter: eyebrow = topic label, headline = the claim (smart brevity)
  :::stats ... :::             one tile per line: value || label
  :::beats ... :::             one story beat per line: label || text || #chapter-id
  :::fig output/x.png ... :::  a numbered figure; lines "read: ..." and "take: ..." frame it
  :::more Summary ... :::      expandable "go deeper" block (methods, tables, caveats, code)
  :::note ... :::              a callout
Chapter ids are the slug of the eyebrow (e.g. "Where it went" -> #where-it-went).
-->

# Mercurio stopped La Pampa for two years. Then mining crossed the road.

> What Operation Mercurio did to illegal gold mining in Madre de Dios, Peru, and what FZS should expect when an operation ends. Team walkthrough: the story first, every analysis behind it, every number from `output/numbers.csv`.

:::stats
{{mean_add_tambopata_2016_18}} → {{mean_add_tambopata_2019_21}} || ha/yr of net new mining in the Tambopata buffer zone, 2016–18 vs 2019–21
{{v2_corridor_share_2016_18:.0f}}% → {{v2_corridor_share_2022_25:.0f}}% || share of new mining inside the legal corridor, 2016–18 vs 2022–25
{{v2_new_total_2016_18}} → {{v2_new_total_2022_25}} || ha/yr of first-time mining in all of Madre de Dios: the region did not mine less
{{gold_broad_lapampasector_depleted_2018:.0%}} || of La Pampa's gold-bearing land mined by 2018: the gold was not gone
:::

@part The story

## The story in one minute | Enforcement worked where it landed, while it lasted

**Mercurio cut mining in La Pampa for about two years. Miners answered across the nearest legal boundary and in old pits, and the region kept growing.**

:::beats
Before || La Pampa was Peru's largest illegal mining area: {{mean_add_tambopata_2016_18}} ha of net new mining a year (2016–18). || #where-it-went
During || Net new mining fell to {{mean_add_tambopata_2019_21}} ha/yr in 2019–21. Clearing went on through 2019 and collapsed in 2020. || #timing
Next door || First-time mining directly across the highway, in the legal corridor, rose from {{v2_new_corridoracrosstheroa_2016_18}} to {{v2_new_corridoracrosstheroa_2019_21}} ha/yr. || #across-the-road
After || La Pampa came back to {{mean_add_tambopata_2022_25}} ha/yr in 2022–25, much of it on old pits. In 2025 miners entered the reserve. || #old-pits
Region || First-time mining in Madre de Dios doubled, from {{v2_new_total_2016_18}} to {{v2_new_total_2022_25}} ha/yr. || #where-it-went
:::

**Is it causal?** Only conditionally, and only for **net** new mining in 2019–21. In hectares, Tambopata's fall is the largest of 15 zones (p = {{model_m1_ri_p:.2f}}, the best this test allows) and sits below two rule-based twins. Relative to its size the fall is ordinary, and per 1-km cell the pre-trends fail. [[C]]

**Why it matters:** an operation buys a pause, not an end. FZS should plan for what comes after the patrols leave: the legal side of the boundary, old pits, and the river posts.

## The brief | Four parts, one figure, one conditional causal sentence

**The 2-page brief tells the story above in the course's four parts.** The brief draft has its own page: {{BRIEF_LINK}}.

| Brief part | What it says | Evidence on this page |
|---|---|---|
| **1. The question** | FZS pays for enforcement. What happens in the target, and around it, when an operation ends? | [The rules](#the-rules), [The places](#the-places) |
| **2. Data** | MapBiomas Peru Collection 4, one check per dataset | [Appendix](#appendix) |
| **3. Findings** | Fell for two years, crossed the road, came back; the region grew. One conditional causal claim. | [Where it went](#where-it-went) to [Tests](#tests) |
| **4. What FZS can do** | Stay longer, guard the boundary, watch old pits, make the corridor a filter. Satellites miss dredges and mercury. | [For FZS](#for-fzs), [Claims](#claims) |

:::fig output/fig_brief_main.png
read: Top: land mined for the first time each year in La Pampa (orange) and in the legal corridor directly across the highway (blue). Faint bands = period means. Bottom: all of Madre de Dios, inside (blue) and outside (grey) the corridor. Shaded = operation years.
take: La Pampa fell as the corridor across the road rose, and the department as a whole kept growing. This is the brief's one figure.
:::

:::more How to read this page: claim labels and a plain-word glossary
**Claim labels.** [[D]] what happened · [[P]] what we expect next time · [[C]] what caused it. The course grades honesty about claims (30%), so every claim carries one.

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
:::

@part Background

## The rules | Where you mine decides whether it's a crime

**La Pampa is illegal by location. The corridor across the road is not.** Moving 2 km north turns a crime into an administrative problem.

- **Illegal (D.L. 1105, 2012):** mining in a prohibited zone or with banned equipment. A crime.
- **Informal:** the same failings inside a permitted zone, by someone registered for formalization (REINFO). Not a crime.
- **Formalization barely happens:** in 2021, 9,592 Madre de Dios miners were registered, but only 145 were fully formal (Plan Restauración 2021).
- **Taxes are near zero:** 0% royalty for small producers (Ley 28258); raw gold VAT-exempt, 1.5% withheld on sale.

**Why it matters:** the operation raised the cost of mining in one place, while the legal corridor next door stayed cheap. That alone predicts displacement across the road.

:::more The legal detail, who mines, and the enforcement timeline
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
:::

## The places | Four zones and a road

**We cut one satellite map into zones that match the law:** La Pampa, the corridor across the road, the extra buffer zone, the reserve, plus native communities and the rest. [[D]]

:::fig output/fig_v2_zone_map.png
read: Coloured areas are zones; dark pixels were mapped as mining at least once since 1985. The thick line is the Interoceanic Highway; dotted lines mark La Pampa's longitudes.
take: The corridor across the road has the same gold and the same road as La Pampa, without the enforcement risk. The reserve has gold too, but no road.
:::

**Why it matters:** "Tambopata buffer zone" mixes La Pampa (shut down) with new fronts. The zone map separates the stories.

:::more Zone profiles, boundary checks and choices
**What each zone offers a miner** (study area around La Pampa):

| Zone | Status | km to highway | km to river | Gold-bearing land | Mined by 2018 |
|---|---|---:|---:|---:|---:|
| La Pampa sector | illegal | {{zp_lapampasector_km_to_highway:.1f}} | {{zp_lapampasector_km_to_river:.1f}} | {{zp_lapampasector_gold_bearing_share:.0%}} | {{gold_broad_lapampasector_depleted_2018:.0%}} |
| Corridor across the road | legal if titled | {{zp_corridoracrossth_km_to_highway:.1f}} | {{zp_corridoracrossth_km_to_river:.1f}} | {{zp_corridoracrossth_gold_bearing_share:.0%}} | {{gold_broad_corridoracrossther_depleted_2018:.0%}} |
| Rest of mining corridor | legal if titled | {{zp_restofminingcorr_km_to_highway:.1f}} | {{zp_restofminingcorr_km_to_river:.1f}} | {{zp_restofminingcorr_gold_bearing_share:.0%}} | {{gold_broad_restofminingcorrid_depleted_2018:.0%}} |
| Reserves and parks | illegal | {{zp_reservesandparks_km_to_highway:.1f}} | {{zp_reservesandparks_km_to_river:.1f}} | {{zp_reservesandparks_gold_bearing_share:.0%}} | — |

- **Data:** MapBiomas Peru Collection 4 maps for every year 1985–2025 (30 m pixels), the same product as the course tables.
- **Check:** the raster gives the Tambopata buffer zone {{v2_check_tambopatabufferzone_2025}} ha in 2025 (table: 20,730) and the reserve {{v2_check_tambopatareserve_2025}} ha (platform: 777).
- **Boundary choice:** a narrower and a wider La Pampa window give the same result (fall of {{t4_lp_narrow_change:.0%}} and {{t4_lp_wide_change:.0%}}); we keep the middle one.
- **Boundaries change:** the current Tambopata buffer zone dates from {{t6_bz_approved_tambopata:.0f}}, Amarakaeri's from {{t6_bz_approved_amarakaeri:.0f}}; the corridor from 2012. We apply today's boundaries to every year, as MapBiomas does.

**Code:** `code/raster_zones.py`, `code/v2_extra.py` (zone profile).
:::

@part What happened

## Where it went | New mining moved into the legal corridor

**After 2019, land mined for the first time shifted from La Pampa to the legal corridor.** The corridor's share rose from {{v2_corridor_share_2016_18:.0f}}% to {{v2_corridor_share_2022_25:.0f}}%. [[D]]

:::fig output/fig_v2_stream.png
read: Hectares mined for the first time each year in Madre de Dios, stacked by zone; numbers are yearly totals. Shaded = operation years.
take: The orange La Pampa band thins after 2019, while the blue corridor bands widen and the total keeps growing.
:::

- **La Pampa sector:** {{v2_new_lapampasector_2016_18}} → {{v2_new_lapampasector_2019_21}} → {{v2_new_lapampasector_2022_25}} ha/yr (2016–18 → 2019–21 → 2022–25). [[D]]
- **Corridor across the road:** {{v2_new_corridoracrosstheroa_2016_18}} → {{v2_new_corridoracrosstheroa_2019_21}} → {{v2_new_corridoracrosstheroa_2022_25}} ha/yr. [[D]]
- **All Madre de Dios:** {{v2_new_total_2016_18}} → {{v2_new_total_2019_21}} → {{v2_new_total_2022_25}} ha/yr. [[D]]
- **Independent check:** MAAP #208 finds 74% of 2021–24 mining deforestation inside the corridor; we find {{v2_corridor_share_2022_25:.0f}}% for 2022–25.

:::fig output/fig_v2_corridor_share.png
read: Each point is one year's share of Madre de Dios first-time mining that lies inside the legal corridor.
take: The corridor's share stepped up after 2019 and stayed high.
:::

**Not all corridor growth is displaced La Pampa mining.** The rest of the corridor gained far more than La Pampa lost ({{v2_new_restofminingcorridor_2016_18}} → {{v2_new_restofminingcorridor_2022_25}} ha/yr), so new entrants and the gold price drive most of it.

:::fig output/fig_v2_legality.png
read: First-time mining in Madre de Dios split by MAAP's legality grade: Low = active concession, Medium = concession not verified as active, High = outside any concession, Very high = strict protected area.
take: The presumed-illegal share fell, and the grey zone of unverified concessions grew.
:::

- **Presumed illegal (High + Very high):** {{leg_illegal_share_2016_18:.0%}} → {{leg_illegal_share_2019_21:.0%}} → {{leg_illegal_share_2022_25:.0%}} of first-time mining. [[D]]
- **The grey zone grew:** concessions not verified as active took {{leg_medium_share_2016_18:.0%}} → {{leg_medium_share_2019_21:.0%}} → {{leg_medium_share_2022_25:.0%}}. [[D]]

:::fig output/fig_v2_amw_robustness.png
read: The same zones measured with a second satellite product, Amazon Mining Watch (480 m squares, from 2018).
take: A second product agrees on the move north of the road; it counts less infill after 2021.
:::

**Why it matters:** Mercurio moved new mining from illegal land to legal land. For the reserve that is a win. For the region it is not: total new mining kept growing, and corridor mining still uses mercury.

:::more Legality details, the second product, the cell test, and what we can't show
- **Presumed illegal share** (outside the corridor and outside communities, simple rule): {{t7_presumed_illegal_share_2016_18:.0%}} → {{t7_presumed_illegal_share_2019_21:.0%}} → {{t7_presumed_illegal_share_2022_25:.0%}}. [[D]]
- **Inside the legal corridor**, {{leg_corridor_highish_share:.0%}} of all first-time mining since 1986 sits on land without a verified active concession. [[D]]
- **Time-consistent check:** counting a concession only if it was filed by the mining year gives {{leg_tc_illegal_share_2016_18:.0%}} → {{leg_tc_illegal_share_2019_21:.0%}} → {{leg_tc_illegal_share_2022_25:.0%}} presumed illegal and {{leg_tc_medium_share_2016_18:.0%}} → {{leg_tc_medium_share_2022_25:.0%}} grey zone: the same picture.
- **Amazon Mining Watch:** in the La Pampa longitudes, the share of new mining north of the road was {{amw_v2_north_share_2019:.0%}} in 2019 and {{amw_v2_north_share_2021:.0%}} in 2021. [[D]]
- **Why the products disagree after 2021:** AMW flags a 480 m square only once; MapBiomas counts every new 30 m pixel. {{pc_restofminingcorr_in_earlier_patch_2022_25:.0%}} of MapBiomas's first-time mining in the corridor in 2022–25 lies inside AMW squares flagged earlier, so AMW can't count it again. They agree on the move across the road and differ on infill.
- **Statistical test:** per 1-km cell, the corridor across the road gained {{st_main_corridoracross_during:+.2f}} ha per cell-year in 2019–21 relative to clean comparison cells (p = {{st_main_corridoracross_during_p:.2f}}). The comparison excludes the corridor and communities, so it isn't itself a displacement target ([Attempt 1](#attempt-1)).
- **The 2023 spike** appears region-wide and may partly be a map artefact.
- **Can't show:** that the *same* people moved. New arrivals and the gold price fit the same picture.

**Code:** `code/raster_layers.py`, `code/v2_legality.py`, `code/v2_extra.py` (AMW).
:::

## Across the road | Miners crossed the highway, then pushed deeper

**Right after Mercurio, new mining piled up 0–2 km north of the highway, directly across from La Pampa.** The north side's share went from {{t1_road_north_share_2016_18:.0%}} (2016–18) to {{t1_road_north_share_2019_21:.0%}} (2019–21). [[D]]

:::fig output/fig_v2_road_bands.png
read: Each bar is a 1-km strip parallel to the highway, inside La Pampa's longitudes. Orange = south (buffer-zone side), blue = north (corridor side). Height = land mined for the first time per year.
take: The mass of new mining jumped from the south side to the strips just north of the road.
:::

:::fig output/fig_v2_road_placebo.png
read: The change in the north side's share for every possible start year: 3 years after minus 3 years before. The real 2019 start is highlighted.
take: No fake start year shows a bigger jump north than 2019, among windows that don't overlap the event.
:::

:::fig output/fig_v2_depth.png
read: Mean distance north of the highway of each year's first-time mining, with the 0–10, 10–20 and 20–30 km bands.
take: Right after Mercurio new mining hugged the road; then it pushed deeper into the corridor.
:::

- **The jump is unusual:** rank {{t1_road_shift_rank_clean:.0f}} of {{t1_road_shift_n_clean:.0f}} non-overlapping start years (p = {{t1_road_shift_ri_p_clean:.2f}}, the smallest possible). [[D]]
- **Hugging the road:** mean depth fell from {{t9_depth_2016:.0f}} km (2016) to {{t9_depth_2020:.0f}} km (2020), then reached {{t9_depth_2025:.0f}} km by 2025. [[D]]

**Why it matters:** miners follow enforcement and gold across a two-lane road. Any operation south of the highway should expect a response north of it.

:::more The road has been crossed before, plus every test
- **All start years:** the 2019 move north (+{{t1_road_shift_2019:.2f}} share points, within 30 km) ranks {{t1_road_shift_rank:.0f}} of {{t1_road_shift_n:.0f}} start years (p = {{t1_road_shift_ri_p:.2f}}); only 2020, whose window overlaps the event, is higher.
- **History:** in 2008–10 most new mining was north of the road (the Guacamayo boom; share {{t1_road_north_share_2008:.0%}} in 2008). It moved south to La Pampa by 2015 ({{t1_road_north_share_2015:.0%}}), then back north after Mercurio ({{t1_road_north_share_2021:.0%}} in 2021). [[D]]
- **Depth break:** after 2019, {{t9_depth_post2019:+.1f}} km net of trend (p = {{t9_depth_post2019_p:.3f}}, Newey-West). [[D]]
- **Per 1-km cell:** 10–20 km north gained most after 2022, +{{st_grad_b_N10_20_after:.1f}} ha per cell-year (p = {{st_grad_b_N10_20_after_p:.3f}}) relative to cells 10–30 km south. [[D]]
- **Boundary choice doesn't matter:** a narrower or wider La Pampa window changes the La Pampa fall from {{t4_lp_narrow_change:.0%}} to {{t4_lp_wide_change:.0%}}.

**Code:** `code/raster_zones.py` (road bands), `code/v2_tests.py` (T1, T4, T9), `code/v2_stats.py` (road gradient).
:::

## Old pits | Returns to old pits hide inside the net numbers

**In 2023, most new mining in La Pampa happened on old pits, not on new land.** The course's net table can't see this. [[D]]

:::fig output/fig_v2_sankey.png
read: Left: where each period's new mining came from (new land, or old pits mined again). Right: the zone it appeared in. Width = hectares per year, on the same scale in all three panels.
take: Returns to old pits grew in every period, and La Pampa's comeback leaned on them.
:::

- **La Pampa, returns to old pits:** {{v2_lapampa_remined_2016_18}} → {{v2_lapampa_remined_2019_21}} → {{v2_lapampa_remined_2022_25}} ha/yr. [[D]]
- **Share of all new mining on old pits:** {{v2_remined_share_2016_18:.0%}} → {{v2_remined_share_2019_21:.0%}} → {{v2_remined_share_2022_25:.0%}}. [[D]]
- **Independent check:** MAAP #193 reports miners back on degraded land in La Pampa in 2023.

:::fig output/fig_v2_stream_remined.png
read: Hectares of returns to old pits each year, stacked by zone (Ruby's request).
take: The corridor holds most returns too; La Pampa's own returns jump in 2023.
:::

**Why it matters:** an operation can stop clearing while miners quietly return to old pits. FZS should monitor old mining sites, not only forest edges.

:::more Net vs gross, and the map-flicker caveat
**Net vs gross, Tambopata buffer zone (ha/yr):**

| | 2016–18 | 2019–21 | 2022–25 |
|---|---:|---:|---:|
| Net addition (course table) | {{t5_m0_2016_18}} | {{t5_m0_2019_21}} | {{t5_m0_2022_25}} |
| First-time mining | {{t5_m2_2016_18}} | {{t5_m2_2019_21}} | {{t5_m2_2022_25}} |
| Return to old pits | {{t5_m3_2016_18}} | {{t5_m3_2019_21}} | {{t5_m3_2022_25}} |

- **The corridor's share of all returns:** {{rm_corridor_share_2016_18:.0%}} → {{rm_corridor_share_2019_21:.0%}} → {{rm_corridor_share_2022_25:.0%}}. [[D]]
- **La Pampa's share of all returns:** {{rm_lapampa_share_2016_18:.0%}} → {{rm_lapampa_share_2019_21:.0%}} → {{rm_lapampa_share_2022_25:.0%}}. [[D]]
- **Caveat:** the old-pit count includes year-to-year map flicker (about 300 ha/yr even before 2019). Trust the 2023 jump, not small changes.

**Code:** `code/raster_layers.py` (Sankey), `code/v2_extra.py` (returns by zone).
:::

## Timing | Clearing in La Pampa went on through 2019

**Forest clearing on La Pampa's mining land did not stop in February 2019.** It was higher in 2019 than in 2018 and collapsed only in 2020–21. [[D]]

:::fig output/fig_v2_glad_quarterly.png
read: Forest-loss alerts per quarter (University of Maryland GLAD, Landsat, each pixel dated to the day), counted only on land MapBiomas maps as mining.
take: La Pampa's alerts stayed high through 2019 and nearly stopped in 2021–23; across the road they rose from mid-2019.
:::

- **La Pampa, alerts on mining land:** {{glad_mining_lapampasector_2017}} ha (2017), {{glad_mining_lapampasector_2018}} (2018), **{{glad_mining_lapampasector_2019}} (2019)**, {{glad_mining_lapampasector_2020}} (2020), {{glad_mining_lapampasector_2021}} (2021). [[D]]
- **Corridor across the road:** {{glad_mining_corridoracrossther_2018}} ha (2018) → {{glad_mining_corridoracrossther_2019}} (2019) → {{glad_mining_corridoracrossther_2020}} (2020). [[D]]

**Why it matters:** the brief must say clearing fell **from 2020**, not "immediately". This matches Dethier et al. (2023): activity spiked in La Pampa's northwest after the operation.

:::more Sentinel-2 cross-check and caveats
- **Sentinel-2 alerts** (every 5 days) in western La Pampa: {{s2_lp_west_2019_mar_sep_ha}} ha in March–September 2019 ({{s2_lp_west_2019_aug_ha}} ha in August alone), vs {{s2_lp_west_2020_mar_sep_ha}} ha in the same months of 2020. So 2019 clearing was real, not cloud delay.
- **Caveats:** clouds bunch alerts in the dry season, so compare the same quarter across years. The data version changes in 2021. Alerts need standing forest, so returns to old pits never show.

**Code:** `code/glad_alerts.py`.
:::

## Gold left | La Pampa had not run out of gold

**By 2018, La Pampa had mined only {{gold_broad_lapampasector_depleted_2018:.0%}} of its gold-bearing land.** About {{gold_broad_lapampasector_left_2018_ha:,.0f}} ha were left. "Miners left because the gold ran out" is unlikely. [[D]]

| Gold-bearing land already mined | by 2018 | by 2025 |
|---|---:|---:|
| La Pampa sector | {{gold_broad_lapampasector_depleted_2018:.0%}} | {{gold_broad_lapampasector_depleted_2025:.0%}} |
| Corridor across the road | {{gold_broad_corridoracrossther_depleted_2018:.0%}} | {{gold_broad_corridoracrossther_depleted_2025:.0%}} |
| Rest of mining corridor | {{gold_broad_restofminingcorrid_depleted_2018:.0%}} | {{gold_broad_restofminingcorrid_depleted_2025:.0%}} |
| Kotsimba | {{gold_broad_kotsimbanativecomm_depleted_2018:.0%}} | {{gold_broad_kotsimbanativecomm_depleted_2025:.0%}} |

**Why it matters:** enforcement, not exhaustion, is the better explanation for the move.

:::more How we measured gold in the ground
- **The proxy:** no one publishes gold left in the ground. Gold here is alluvial, so we used the national geology map (INGEMMET, 1:100,000): river deposits plus the gold-bearing terraces of the Madre de Dios Formation.
- **Does it work?** {{gold_broad_validation:.0%}} of all land ever mined lies on these units, which cover {{gold_broad_land_share_mdd:.0%}} of Madre de Dios ({{gold_broad_lift:.1f}}× more mining than chance). The strict river-deposit units cover {{gold_strict_land_share_mdd:.0%}} and hold {{gold_strict_validation:.0%}} ({{gold_strict_lift:.1f}}×). La Pampa was {{gold_strict_lapampasector_depleted_2018:.0%}} depleted by 2018 under the strict definition too.
- **Limits:** the map is coarse and says nothing about gold grade; old pits can be mined again.

**Code:** `code/raster_gold.py`.
:::

## Inside the reserve | In 2025, miners entered the reserve

**The course data covers only buffer zones. Inside Tambopata National Reserve, mining reached {{anp_level_tam_nr_2025:,.0f}} ha in 2025, {{anp_tam_nr_addition_2025}} ha of it new that year.** [[D]]

:::fig output/fig_peru_inside_reserves.png
read: Mining area inside each reserve compared with its buffer zone, from the MapBiomas protected-area statistics we downloaded (checked: 777 ha on the platform).
take: Inside the reserves, mining stayed small for years; in 2025 it jumped inside Tambopata.
:::

- **Two other sources agree:** MAAP #241 reports ~500 ha of new mining inside the reserve (late 2025 to Feb 2026); Amazon Mining Watch shows {{sp_amw_tambopata_nr_new_ha_2025}} ha in 2025 (provisional). [[D]]
- **The trigger:** the 2025 incursion came after the navy left its Malinowski River posts (MAAP #241).

**Why it matters:** this is FZS's core area, and the most actionable finding.

:::more The 2017 jump and the code
- The 2017 jump (+{{anp_tam_nr_addition_2017}} ha) looks partly like a map reclassification, not real mining. [[D]]

**Code:** `code/peru_anp.py`.
:::

## Declared gold | The official gold drop is a definition change

**The official Madre de Dios gold series fell {{pe_prod_fall_2018_2025_pct:.0f}}% from 2018 to 2025, but mostly because its definition changed.** Until 2019 it included an *estimate* of artisanal gold; from 2020 it counts only what producers declare. [[D]]

:::fig output/fig_peru_gold_definition.png
read: Madre de Dios gold in the ministry's yearly files, split into what producers declared and the artisanal estimate the ministry added.
take: The "collapse" is the estimate disappearing in 2020; declared output rose.
:::

- **Declared output rose:** {{gold_minem_declared_2018_kg:,.0f}} kg (2018) → {{gold_minem_declared_2025_kg:,.0f}} kg (2025). The estimate was {{gold_minem_estimate_2019_kg:,.0f}} kg in 2019 and is absent from 2020.
- **We withdrew** our earlier "collapse" and its break test: they measured the definition change.

**Why it matters:** official production says almost nothing about mining here. Don't cite "−88%".

:::more The 2015 break, and the "mining in the corridor, declaring nothing" idea
- **The series:** the ministry's files carry "PRODUCTORES ARTESANALES — cifras estimadas" for Madre de Dios until 2019 (about 15.7 t in 2016, 6.0 t in 2019). In 2016, that estimate plus declared output equals the central bank's figure exactly.
- **An earlier break in 2015:** until 2014, artisanal producers' own declarations were in the series ({{gold_minem_declared_2014_kg:,.0f}} kg in 2014); from 2015 producers declared only {{gold_minem_declared_2015_kg:,.0f}} kg and the ministry added an estimate.
- **For the idea:** {{leg_medium_share_2022_25:.0%}} of first-time mining in 2022–25 sat in concessions not verified as active; producers declare about 1 t a year while first-time mining covers over {{v2_new_total_2022_25}} ha a year; only 145 of 9,592 registered miners were fully formal (2021); Bolivia's gold exports jumped from 1.7 t (2012) to 35.7 t (2014); nationally at least 80 of ~180 t exported in 2024 had unknown origin.
- **Against:** gold may be declared in other regions; mapped area includes re-mined pits; gold yield per hectare is unknown.
- **Label:** plausible mechanism, not a finding.

**Code:** `code/peru_gold_minem.py` (checked against the central bank for 2012 and 2019), `code/peru_production.py`. **Source:** `docs/overnight/notes/legality_data.md`.
:::

## Context | Enforcement comes in waves tied to governments and budgets

**Other events line up with the mining curve.** Enforcement money peaked in 2019 and faded; COVID pulled forces away in 2020; a new government arrived in 2021. [[D]]

:::fig output/fig_v2_timeline.png
read: Top: events by type (enforcement, presidents, laws, context). Below: land mined for the first time each year in La Pampa and in all of Madre de Dios. Shaded: 2012–13 and 2019–21.
take: Both enforcement waves started within a year of a new president and faded within about two.
:::

:::fig output/fig_v2_enforcement_spending.png
read: Executed spending of Peru's anti-illegal-mining programme (PP 0128) booked in Madre de Dios, next to first-time mined land. A lower bound: national units book under Lima.
take: Spending peaked in 2019 and fell as mining rebounded.
:::

- **One dip, not two:** La Pampa first-time mining changed by {{tl_dip_2012_13:+.0%}} in 2012–13 vs 2010–11, and by {{tl_dip_2020_21:+.0%}} in 2020–21 vs 2017–18. [[D]]
- **Money:** {{t8_pp0128_mdd_2018:,.0f}} soles (2018), {{t8_pp0128_mdd_2019:,.0f}} (2019), {{t8_pp0128_mdd_2021:,.0f}} (2021), {{t8_pp0128_mdd_2025:,.0f}} (2025). [[D]]
- **Gold price:** up {{gold_price_ratio_2025_2018:.1f}}-fold from 2018 to 2025. It pushes everywhere at once, which the year effects in [Attempt 1](#attempt-1) remove.

**Why it matters:** FZS should plan for the gap after each wave.

:::more Politics, COVID, the 2017 spike and the earlier wave
- **The political-cycle idea:** both enforcement waves started 7–11 months after a new president (Humala 2011 → decrees 2012; Vizcarra 2018 → Mercurio 2019). That's a pattern, not evidence; we found no study of Peruvian election effects (Brazilian studies find more deforestation in election years).
- **Earlier wave in the course table:** Tambopata's gap in 2012–13 was +{{t3_wave_m1_2012_13}} ha/yr, rank {{t3_wave_rank:.0f}} of {{t3_wave_n:.0f}}: no Tambopata-specific dip. [[D]]
- **COVID:** forces left La Pampa in spring 2020; budgets fell sharply in 2020–21 (Mongabay 2023). That fits the 2022–25 rebound.
- **The 2017 spike:** 2017 was the record year for mining deforestation (Caballero Espejo et al. 2018). The gold price was flat (about $1,250/oz, 2016–18), so it doesn't explain it. Gangs ("Guardianes de la Trocha") ran extortion in La Pampa, but no source dates a 2017 takeover; part of the jump may be map reclassification. Mercury controls after Peru ratified the Minamata Convention (2016) made mercury a smuggling business; plausible, undocumented.

**Code:** `code/v2_extra.py` (timeline), `code/v2_tests.py` (spending, 2012 wave). **Sources:** `docs/overnight/notes/qualitative_background.md`, `enforcement_intensity.md`.
:::

@part Is it causal?

## Three attempts | One partly works, one half-works, one fails

**We tried three ways to build "what would have happened without Mercurio". None is clean.** Two point the same way for **net** mining in 2019–21.

| Attempt | Comparison | Pre-trends | Result |
|---|---|---|---|
| **1 Difference-in-differences** | Tambopata vs 14 other Peruvian buffer zones; per 1-km cell vs clean comparison cells | Zone level: averaged fake dates pass. Cell level: fail for La Pampa (p = {{st_event_lp_pretrend_p:.3f}}) | Largest fall in hectares (rank 1 of 15, p = {{model_m1_ri_p:.2f}}); **ordinary for its size** (rank {{model_m4_rank:.0f}} of {{model_m4_n:.0f}}) |
| **2 Synthetic control** | weighted mix of Peruvian zones | can't be met: La Pampa is too big | Fails for levels |
| **3 Rule-based twins** | two existing areas abroad (Amanã, Tapajós) | not parallel: Tambopata grew faster before 2019 | Tambopata below both in 2019–21 (descriptive, 3 years each) |

**Why it matters:** the bar is "anywhere close to causal". We get close for net mining in 2019–21, with every weakness stated.

## Attempt 1 | Largest fall in hectares, ordinary for its size

**In hectares, Tambopata's 2019–21 fall in net mining is the largest of 15 zones and survives controls for the gold price, trends and size.** Relative to its own size it is ordinary, and per 1-km cell the pre-trends fail. [[D]]

:::fig output/fig_peru_event_study.png
read: Top: how far Tambopata sits from the comparison zones each year, relative to 2018 (= 0). The grey band is the range if each other zone had been "treated" instead. Bottom: the raw additions behind it.
take: Tambopata drops below the whole band in 2019–22 and comes back after.
:::

:::fig output/fig_peru_models.png
read: The 2019–21 gap under four models (M1 zone + year effects; M2 + gold price × size; M3 + own trends; M4 scaled to size), next to the same model with a fake 2016 start.
take: In hectares the real gap is large and ranks first under M1–M3; scaled to size (M4) it is only third. M3's fake gap has the same sign as the real one.
:::

:::fig output/fig_v2_stats_zones.png
read: Change per 1-km cell in each zone, 2019–21 and 2022–25, relative to clean comparison cells, with 95% confidence intervals (clustered by 10-km blocks).
take: The corridor across the road clearly rose; La Pampa's fall is borderline.
:::

:::fig output/fig_v2_stats_event.png
read: Year-by-year per-cell estimates for La Pampa and the corridor across the road, with 2014–18 as reference. Leads before 2014 test for pre-trends.
take: The corridor's pre-trends pass; La Pampa's don't, which weakens its cell-level fall.
:::

- **Fake places:** Tambopata ({{model_m1_during}} ha/yr) ranks 1 of {{model_m1_n}} (p = {{model_m1_ri_p:.2f}}, the smallest possible with {{model_m1_n}} zones). [[D]]
- **Scaled to size (M4):** rank {{model_m4_rank:.0f}} of {{model_m4_n:.0f}} (p = {{model_m4_ri_p:.2f}}). Tambopata falls most in hectares because it is the biggest. [[D]]
- **Per cell:** La Pampa {{st_main_lapampasector_during:+.2f}} ha per cell-year (p = {{st_main_lapampasector_during_p:.2f}}; wild bootstrap p = {{st_wcb_lp_p:.2f}}); pre-trends fail (p = {{st_event_lp_pretrend_p:.3f}}). [[D]]

**Why it matters:** honest wording is "consistent with a short-lived effect on net mining", not "proven".

:::more The 2×2, the model ladder and the cell panel in full
**Level 1: the course's 2×2 (Tambopata vs the extra buffer zone, Amarakaeri)**

| ha of net new mining per year | Before 2016–18 | During 2019–21 | Change |
|---|---:|---:|---:|
| Tambopata (targeted) | {{mean_add_tambopata_2016_18}} | {{mean_add_tambopata_2019_21}} | {{did_main_tambopata_change}} |
| Amarakaeri (extra buffer zone) | {{mean_add_amarakaeri_2016_18}} | {{mean_add_amarakaeri_2019_21}} | +{{did_main_amarakaeri_change}} |
| **Gap change** | | | **{{did_main}}** |

- **Amarakaeri was itself treated** (Mercurio II, December 2019), so it is "less treated", not a control.
- **Baseline 2014–18 instead of 2016–18:** gap {{did_main_base_2014_18}} ha/yr.
- **Target + neighbours (the card's check):** the three buffer zones together added {{mean_add_three_bz_sum_2016_18}} → {{mean_add_three_bz_sum_2019_21}} → {{mean_add_three_bz_sum_2022_25}} ha/yr: down during, above the old level after. [[D]]
- **Net is not new:** almost half of the net fall is old mining going out of use; first-time mining fell from {{t5_m2_2016_18}} to {{t5_m2_2019_21}} ha/yr ([Old pits](#old-pits)).

**Level 2: against all 14 other Peruvian buffer zones with mining**

- **Model:** net new mining = zone effect + year effect + Tambopata × period. Year effects remove the gold price, COVID and national policy (shared shocks).
- **Fake places:** each other zone gets the "operation" in turn, with Tambopata removed from its comparison pool. Placebo effects range {{model_m1_placebo_min:,.0f}} to +{{model_m1_placebo_max:,.0f}} ha/yr. Among Amazon-department zones only: rank {{model_m1_rank_amazon:.0f}} of {{model_m1_n_amazon:.0f}}.
- **Dropping the largest comparison zone:** 2019–21 gap {{robust_es_poolB_drop_largest_2019_2021}} ha/yr.

| Model | Adds | During 2019–21 | After 2022–25 | Fake 2016 | Rank |
|---|---|---:|---:|---:|---:|
| **M1** | Zone + year effects | {{model_m1_during}} | {{model_m1_after}} | {{model_m1_placebo}} | {{model_m1_rank}} of {{model_m1_n}} |
| **M2** | + bigger zones react more to gold price | {{model_m2_during}} | {{model_m2_after}} | {{model_m2_placebo}} | {{model_m2_rank}} of {{model_m2_n}} |
| **M3** | + each zone's own trend | {{model_m3_during}} | {{model_m3_after}} | {{model_m3_placebo}} | {{model_m3_rank}} of {{model_m3_n}} |
| **M4** | Scaled to each zone's size | {{model_m4_during:.2f}} | {{model_m4_after:.2f}} | {{model_m4_placebo:.2f}} | {{model_m4_rank}} of {{model_m4_n}} |

- **Fake dates:** M1 and M2 placebos have the opposite sign; M3's placebo ({{model_m3_placebo}}) has the same sign as the real effect, so not every model passes cleanly.

**Level 3: per 1-km cell, with standard errors**

- **Panel:** {{st_n_cells}} cells, 2014–2025 (baseline 2014–18); cell and year fixed effects; errors clustered by 10 × 10 km blocks.
- **Clean comparison:** cells outside every named zone, the legal corridor and native communities ({{st_n_ref_cells_clean:.0f}} cells). The earlier version used the rest of the corridor, where displaced mining went, which exaggerated La Pampa's fall.
- **Few treated clusters:** La Pampa covers {{st_clusters_lp:.0f}} of the {{st_n_clusters:.0f}} clusters, so we add a wild cluster bootstrap.

| Per 1-km cell, ha/yr vs clean comparison | 2019–21 | p (clustered) | 2022–25 | p |
|---|---:|---:|---:|---:|
| La Pampa sector | {{st_main_lapampasector_during:+.2f}} | {{st_main_lapampasector_during_p:.2f}} | {{st_main_lapampasector_after:+.2f}} | {{st_main_lapampasector_after_p:.2f}} |
| Corridor across the road | {{st_main_corridoracross_during:+.2f}} | {{st_main_corridoracross_during_p:.2f}} | {{st_main_corridoracross_after:+.2f}} | {{st_main_corridoracross_after_p:.2f}} |
| Extra buffer zone (Amarakaeri) | {{st_main_amarakaeribzex_during:+.2f}} | {{st_main_amarakaeribzex_during_p:.3f}} | {{st_main_amarakaeribzex_after:+.2f}} | {{st_main_amarakaeribzex_after_p:.2f}} |
| Tambopata reserve | {{st_main_tambopatareser_during:+.2f}} | {{st_main_tambopatareser_during_p:.3f}} | {{st_main_tambopatareser_after:+.2f}} | {{st_main_tambopatareser_after_p:.3f}} |

- **Wild cluster bootstrap (999 draws, only {{st_clusters_lp:.0f}} and {{st_clusters_across:.0f}} treated blocks):** La Pampa 2019–21 p = {{st_wcb_lp_p:.2f}}; corridor across the road p = {{st_wcb_across_p:.2f}}.
- **Old, contaminated comparison:** La Pampa {{st_contam_lapampasector_during:+.2f}} ha per cell-year.
- **Robust to:** gold-bearing land × year effects ({{st_gold_lapampasector_during:+.2f}}, p = {{st_gold_lapampasector_during_p:.2f}}); Poisson ({{st_ppml_lapampasector_during:+.2f}} log points, p = {{st_ppml_lapampasector_during_p:.2f}}).
- **Pre-trends:** with the pooled 2014–18 reference, La Pampa's 2010–13 leads are jointly different from zero (p = {{st_event_lp_pretrend_p:.3f}}); the corridor across the road passes (p = {{st_event_across_pretrend_p:.2f}}).

**Code:** `code/peru.py`, `code/peru_models.py`, `code/v2_stats.py`.
:::

## Attempt 2 | A synthetic twin can't copy La Pampa's size

**A weighted mix of Peruvian zones can't reach La Pampa's size, so this method adds only a weak extra check.** [[D]]

:::fig output/fig_peru_synth.png
read: Left: hectares; right: each zone scaled to its own 2014–18 average. Top: real Tambopata vs its synthetic copy (they should overlap before 2019). Bottom: the gap, with grey lines for each donor zone posing as the target.
take: In hectares the copy never fits; scaled, Tambopata's 2019–21 dip is the deepest, but six zones prove little.
:::

- **In hectares, no fit:** before 2019 Tambopata added {{synth_core_add_pre_mean_tam}} ha a year; the best mix only {{synth_core_add_pre_mean_synth}}. It lay outside every other zone's range in {{synth_core_add_hull_years_outside}} of 9 years. [[D]]
- **Scaled, a good fit:** Tambopata's dip is the deepest of {{synth_core_addsc_n_units_ranked}} zones (rank {{synth_core_addsc_rank}}). [[D]]

**Why it matters:** you can't average small numbers into a big one. That's why Attempt 1 compares *changes*, and why Attempt 3 had to look abroad.

:::more What synthetic control is
A synthetic control builds a fake Tambopata from a weighted mix of other zones (weights ≥ 0, summing to 1), fitted to the years before 2019. After 2019, the gap between Tambopata and the mix is the estimate. It differs from Ruby's idea: a mix of many zones instead of one real twin.

**Code:** `code/peru_synth.py`.
:::

## Attempt 3 | No untouched twin exists; the closest ones grew faster

**No area in the Amazon passes all four of Ruby's rules. Relax one, and two twins appear in Brazil.** In 2019–21 Tambopata added new mining at {{top3_median_ratio:.0%}} of their median pace. [[D]]

**The rules (Ruby):** find one existing area with (R1) at least 500 ha of mining by 2018, (R2) no operation reported in 2017–25, (R3) outside Madre de Dios, and (R4) lowland mining at least a fifth of La Pampa's size. The closest survivor wins.

:::fig output/fig_control_funnel.png
read: Each bar is the number of areas left after one more rule (log scale).
take: Almost every big mining area in the Amazon got an operation, so no strict twin survives.
:::

:::fig output/fig_control_map.png
read: Each dot is an area with at least 500 ha of mining by 2018. Size = mining area; colour = what happened to it under the rules.
take: Peru outside Madre de Dios has no big mining area; the candidates cluster in Brazil's Tapajós gold region.
:::

:::fig output/fig_control_compare.png
read: Left: new mining per year as a share of each area's 2018 mining (same product for both). Right: total mining area, 2018 = 100, each from its own MapBiomas collection (side by side, never subtracted).
take: Tambopata and Amanã grew alike before 2019; in 2019–21 Tambopata went flat while Amanã kept growing.
:::

:::fig output/fig_control_top3.png
read: Tambopata against the two twins that pass the relaxed rules: growth before 2019 and pace in 2019–21.
take: Tambopata ran below both twins in 2019–21, but it also grew faster than them before.
:::

- **Relaxed rule:** no operation in 2017–21 only. {{ctl_n_relaxed}} areas pass; best fit **Amanã National Forest**, then the Tapajós protection area. [[D]]
- **2019–21:** Tambopata {{top3_tam_during:.1f}}% of its 2018 stock per year; Amanã {{top3_amana_twin_during:.1f}}%; Tapajós {{top3_tapajos_twin_during:.1f}}%. [[D]]

**Why it matters:** a second, independent comparison agrees with Attempt 1: another country, another data source, picked by rules, not results.

:::more The funnel, the twin table, and what still threatens it
- {{ctl_n_areas}} protected areas, buffer zones and indigenous territories screened. {{ctl_n_r1}} had real mining before 2019; only {{ctl_n_r2}} of those had no operation found, both small and unlike La Pampa; {{ctl_n_r1_unclear_or_unsearched}} more were unclear. [[D]]
- **Sources:** SERNANP (Peru), RAISG (other countries), FUNAI (Brazil's territories); Amazon Mining Watch for mining; a logged web search per area for operations; OpenTopoData for elevation.

| | Tambopata buffer zone | Amanã National Forest |
|---|---:|---:|
| Mining by 2018 (AMW, ha) | {{ctl_tam_stock_2018}} | {{ctl_relaxed_stock_2018}} |
| Median elevation of the mining (m) | {{ctl_tam_elev_m}} | {{ctl_relaxed_elev_m}} |
| Distance from La Pampa (km) | 0 | {{ctl_relaxed_dist_km}} |
| First operation found | Feb 2019 | Mar 2023 |

- **Before 2019 the two grew alike:** both stood at about half their 2018 size in 2014 ({{ctl_mb_tam_index_2014}} and {{ctl_mb_twin_index_2014}}). By 2021 Tambopata was flat ({{ctl_mb_tam_index_2021}}); Amanã had grown to {{ctl_mb_twin_index_2021}}. [[D]]
- **First twin alone:** Tambopata added {{ctl_relaxed_tam_during:.1f}}% of its 2018 mining per year vs Amanã {{ctl_relaxed_ctl_during:.1f}}% ({{ctl_relaxed_during_ratio:.0%}} of its pace).
- **After 2021 Amanã is spoiled:** its own operation came in March 2023. Use it for 2019–21 only.
- **Munduruku was dropped:** our search log records Operation Mundurukânia there in May 2021, inside the rule's window (search snippets, unverified).

| Twin | Growth gap before 2019 (log points/yr; p) | 2019–21 pace, % of 2018 stock | Gap vs Tambopata |
|---|---:|---:|---:|
| Amanã National Forest | {{top3_amana_pre_growth_diff:+.2f}} ({{top3_amana_pre_growth_p:.2f}}) | {{top3_amana_twin_during:.1f}} | {{top3_amana_during_gap:+.1f}} |
| Tapajós protection area | {{top3_tapajos_pre_growth_diff:+.2f}} ({{top3_tapajos_pre_growth_p:.2f}}) | {{top3_tapajos_twin_during:.1f}} | {{top3_tapajos_during_gap:+.1f}} |

- **No p-values for the gap:** three years per area make a t-test meaningless.
- **Pre-trends are not parallel:** Tambopata grew faster than both before 2019 (significant against Tapajós), and the two sides come from different MapBiomas collections.
- **Threats:** Brazil weakened enforcement in 2019–22, so the twins may have grown faster than "normal". "No operation found" is not proof of none. On Amazon Mining Watch, Tambopata's 2019 value is its highest after 2018; the fall shows from 2020.
- **Ruby's caution holds:** "no intervention" is too strict (no area passes); "comparable enforcement" needs zone-level enforcement data that isn't public.

**Code:** `code/control_amw.py`, `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py`, `control_top3.py`. Searches: `docs/overnight/notes/control_interventions.csv`, coded in `data_intermediate/operations_coded.csv`.
:::

## Tests | The move across the road is clear; the fall in La Pampa is fragile

**Every movement and comparison, tested.** A critical referee found errors in our first round; all are fixed. [[D]]

| Movement or comparison | Test | Estimate | p |
|---|---|---:|---:|
| Tambopata's 2019–21 net fall vs 14 zones | fake places, Tambopata out of the pool | rank 1 of {{model_m1_n}} | {{model_m1_ri_p:.2f}} |
| Same, scaled to each zone's size (M4) | fake places | rank {{model_m4_rank:.0f}} of {{model_m4_n:.0f}} | {{model_m4_ri_p:.2f}} |
| La Pampa sector, per cell, 2019–21 | DiD, cell + year FE, clean comparison, clustered | {{st_main_lapampasector_during:+.2f}} ha | {{st_main_lapampasector_during_p:.2f}} |
| Same | wild cluster bootstrap | — | {{st_wcb_lp_p:.2f}} |
| La Pampa pre-trends (cells) | joint test of 2010–13 leads | — | {{st_event_lp_pretrend_p:.3f}} |
| Corridor across the road, per cell, 2019–21 | DiD, clean comparison | {{st_main_corridoracross_during:+.2f}} ha | {{st_main_corridoracross_during_p:.2f}} |
| Extra buffer zone (Amarakaeri), 2019–21 | same | {{st_main_amarakaeribzex_during:+.2f}} ha | {{st_main_amarakaeribzex_during_p:.3f}} |
| North of highway 10–20 km, 2022–25 | road-gradient DiD | {{st_grad_b_N10_20_after:+.2f}} ha | {{st_grad_b_N10_20_after_p:.3f}} |
| Move north of the road in 2019 | fake start dates, non-overlapping windows | rank {{t1_road_shift_rank_clean:.0f}} of {{t1_road_shift_n_clean:.0f}} | {{t1_road_shift_ri_p_clean:.2f}} |
| New mining hugged the road after 2019 | trend + break, Newey-West | {{t9_depth_post2019:+.1f}} km | {{t9_depth_post2019_p:.3f}} |
| Brazil: falls after own operation | staggered DiD (did2s), clustered by territory | {{brv2_did2s_treat:+.2f}} log (wrong sign) | {{brv2_did2s_treat_p:.2f}} |
| Brazil: same | randomization (2,000 shuffles) | — | {{brv2_ri_p:.2f}} |

**How to read p:** below 0.05 = unlikely to be chance. With 15 zones the smallest possible randomization p is 0.07, so "rank 1 of 15" is as strong as that test gets.

**Why it matters:** the instructor will ask "is this significant?" This table answers each claim, including the ones that fail.

:::more What the referee found, and what we changed
| Problem | Fix | Effect on the result |
|---|---|---|
| Fake-place test kept Tambopata as a control, so every placebo looked positive | Tambopata removed from each placebo's pool; Amazon-only pool added | Still rank 1 in hectares; **rank {{model_m4_rank:.0f}} of {{model_m4_n:.0f}} scaled** |
| Causal number measured net change, called "new mining" | Claim reworded to net mining; first-time change reported | First-time mining fell less ({{t5_m2_2016_18}} → {{t5_m2_2019_21}} ha/yr) |
| Cell comparison included the corridor (displacement target); baseline mislabelled; few treated clusters | Clean comparison cells; 2014–25 panel; pooled 2014–18 reference; wild cluster bootstrap | La Pampa {{st_main_lapampasector_during:+.2f}} (was {{st_contam_lapampasector_during:+.2f}}); pre-trends still fail |
| One twin (Munduruku) had a 2021 operation; t-tests on 3 values | Two twins; no p-values | Tambopata still below both |
| Brazil code skipped Kayapó's 2024 operation | First operation inside 2021–25 used | Estimate {{brv2_did2s_treat:+.2f}}, still not significant |
| Road placebo windows overlapped the event | Non-overlapping start years only | Rank 1 of {{t1_road_shift_n_clean:.0f}} (p = {{t1_road_shift_ri_p_clean:.2f}}) |
| Legality used today's concessions for past years | Concession must be filed by the mining year | Illegal share {{leg_tc_illegal_share_2016_18:.0%}} → {{leg_tc_illegal_share_2022_25:.0%}} (unchanged picture) |
| Risk map tested on the same cells, no benchmark | Spatial hold-out + "mining nearby" benchmark | AUC {{risk_auc_spatial_holdout:.2f}} vs {{risk_auc_benchmark:.2f}}: adds little |
| Untraceable numbers (Sentinel-2, producer gold) | Now computed in code | See [Timing](#timing) and [Declared gold](#declared-gold) |

**Full review:** `docs/overnight/notes/critical_review_v2.md`.
:::

@part Brazil

## Brazil | Same method, weaker result: the direction, not the cause

**The big Brazilian territories fell after 2022–24, but not after their own operations.** The staggered test finds no significant effect. [[D]]

:::fig output/fig_brazil_v2_pixels.png
read: First-time mining and returns to old pits per territory, MapBiomas Brazil Collection 11, measured with the same pixel method as Peru. Dates mark each territory's own first operation.
take: Yanomami fell from 2024, a year after its operation; other territories don't line up with their own dates.
:::

- **Yanomami:** {{brv2_yan_new_2019_22}} ha/yr of first-time mining in 2019–22, {{brv2_yan_new_2023_25}} in 2023–25. [[D]]
- **Staggered DiD:** {{brv2_did2s_treat:+.2f}} log points (p = {{brv2_did2s_treat_p:.2f}}); randomization p = {{brv2_ri_p:.2f}}. Wrong sign, not significant. [[D]]
- **No spill next door:** rings around Yanomami got almost no new mining (0–10 km: {{brv2_r0_10_post:.1f}} ha/yr after 2023). Miners went toward Venezuela and to territories like Sararé (ISA 2026; Greenpeace).

**Why it matters:** Brazil fits "enforcement plus tracing reduces mining", but national rules may matter as much as local operations. That's a lesson for Peru's corridor.

:::more Data, checks, the test, and why the null
- **Data:** MapBiomas Brazil Collection 11 maps, 1985–2025, read only around each territory (24 territories with mining + two rings around Yanomami).
- **Check:** Kayapó mining {{brv2_kayapo_check_2024}} ha (2024) and {{brv2_kayapo_check_2025}} ha (2025) vs 17,632 and 18,573 on the platform. This fixes the old Brazil mismatch (Collection 10.1 vs the platform's Collection 11).
- **Test:** territory + year effects, each territory treated from its own first operation ({{brv2_n_treated:.0f}} of {{brv2_n_units:.0f}} territories); Gardner's two-stage estimator; randomization inference with 2,000 shuffles.
- **Why the null:** after correcting the dates (Munduruku from May 2021; Kayapó from September 2024), territories still don't fall faster after their own operation. Sararé surged as its operation began, and the test has little power.
- **Products disagree on Yanomami's timing:** MapBiomas shows the fall from 2024; Amazon Mining Watch from 2023 ({{bs_yan_new_ha_2022}} → {{bs_yan_new_ha_2023}} ha); MAAP #242 reports about 1,800 ha (2022) and 330 ha (2023).
- **Support:** Amazon Mining Watch shows Yanomami −63% after its operation; IBAMA fines fell 2019–22 while mining tripled, then reversed in 2023.
- **Challenge:** a national change in January 2023 (new government, end of the gold "good faith" rule, electronic gold invoices from August 2023) hit all territories at once, which a territory-level design can't separate.

**Code:** `code/brazil_raster.py`, `code/brazil_v2.py`, plus `brazil_stagger.py` (AMW), `brazil.py`, `brazil_ibama.py`.
:::

@part So what

## For FZS | Stay longer, guard the boundary, watch old pits

**Keep enforcement on longer than two years, patrol the legal side of the boundary, watch old pits, and push tracing inside the legal corridor.** [[P]]

1. **Expect the response across the nearest legal boundary.** New mining jumped into the corridor right across the highway, then went deeper.
2. **Monitor old pits, not only forest edges.** In 2023 most new mining in La Pampa was on old pits. Forest-loss alerts never see this.
3. **Keep river posts staffed.** The 2025 incursion into the reserve followed the navy's withdrawal from the Malinowski posts (MAAP #241).
4. **Make the legal corridor a real filter:** proof of gold origin, gold-buyer registers, real formalization deadlines, mercury checks. Brazil's 2023 reforms are a model.

:::fig output/fig_v2_risk_map.png
read: Predicted chance that a 1-km cell gets first-time mining in 2026–28, from a model trained on 2019–21 and tested out of sample on 2022–25.
take: Risk clusters next to old mining; the model adds little beyond "is there mining nearby?" and misses river-borne incursions.
:::

- **Where to look next:** the model flags {{risk_hi_cells_outside_corridor:.0f}} high-risk cells outside the legal corridor: {{risk_hi_cells_lapampasector:.0f}} in the La Pampa sector and {{risk_hi_cells_nativecommunitie:.0f}} in native communities. [[P]]
- **Honest score:** AUC {{risk_auc_spatial_holdout:.2f}} on held-out 10-km blocks, barely above {{risk_auc_benchmark:.2f}} for "mining nearby" alone. [[P]]

**Why it matters:** enforcement works while it lasts and where it lands. FZS can fund the "while" and watch the "where".

:::more The social cost, and what data would let us say more
- **Damage:** each kg of gold mined in Peru costs US$81,000–364,000 (Conservation Strategy Fund calculator).
- **Mercury:** over a third of carnivorous fish exceed the limit hundreds of km downstream; exposed children score 4.68 IQ points lower.
- **Exploitation:** about 4,500 women are sexually exploited near camps, 78% of them minors.
- **Livelihoods:** about 46,600 people depend directly on mining. Enforcement without income alternatives invites return.
- **The corridor gap:** 0% royalty, 1.5% withholding, and only 145 of 9,592 registered miners fully formal (2021).
- **What would let us say more:** dated patrol and interdiction records per zone (SERNANP, FZS, police); concession and REINFO maps to grade legality pixel by pixel; pond-colour or dredge counts for activity on old pits and rivers.
:::

## Claims | What we can say, and how strongly

| Claim | Label | Evidence for | Evidence against |
|---|---|---|---|
| Net new mining in Tambopata fell sharply in 2019–21 | [[D]] | Course table = raster; rank 1 of 15 | First-time mining only halved; clearing continued through 2019 |
| Mercurio caused the 2019–21 fall in net mining, roughly {{model_m1_during:,.0f}} to {{model_m3_during:,.0f}} ha/yr | [[C]] *conditional* | Rank 1 of 15 in hectares (p = {{model_m1_ri_p:.2f}}); below both twins | Ordinary relative to size; cell pre-trends fail; extra buffer zone also treated |
| New mining moved into the legal corridor, across the road, then deeper | [[D]] | Raster bands; depth break p < 0.01; AMW agrees; MAAP #208 (74%) | Can't show the same people moved; the road was crossed before (2008) |
| Miners returned to old pits in 2023 | [[D]] | Raster accounting; MAAP #193 | Map flicker inflates old-pit counts |
| La Pampa had not run out of gold | [[D]] | Geology: {{gold_broad_lapampasector_depleted_2018:.0%}} mined by 2018 | Coarse map; no gold grade |
| The official gold series fell 88% | **withdrawn** | — | The series dropped its artisanal estimate in 2020; producer-declared gold rose |
| Corridor miners mine informally and don't declare | plausible, **not claimed** | Formalization rates, Bolivia exports, unknown-origin exports | No trace of where Madre de Dios gold is declared |
| The region mined less | **rejected** | — | First-time mining rose {{v2_new_total_2016_18}} → {{v2_new_total_2022_25}} ha/yr |
| Brazil: operations reduced mining | **not claimed** | Falls after 2022–24; AMW −63% Yanomami | Staggered DiD {{brv2_did2s_treat:+.2f}} (wrong sign, p = {{brv2_did2s_treat_p:.2f}}); national reforms in 2023 |
| Next operation: local fall while present, a move across the nearest legal boundary, a return within ~3 years | [[P]] | Peru pattern | One operation, one region; risk model barely beats "mining nearby" |

**Why it matters:** one labelled, conditional causal claim, with its failed tests shown, beats a vague strong one.

@part Team corner

## To do | What's blocked on you

**Only a human can do these:**

1. **Agree on the claim wording,** especially the one conditional causal sentence ([Three attempts](#three-attempts)). It's a team call.
2. **Ruby: check [The places](#the-places) and [Attempt 3](#attempt-3).** The zone map (we kept the middle La Pampa window) and her twin design. Should native communities inside the corridor count as legal?
3. **Confirm Brazil's scope with Raji** (appendix-level, as discussed).
4. **MAAP pages:** the site blocks scripts. Open each link in `docs/overnight/notes/maap_citations.md` and save it with File › Save Page As into `data_raw/maap/`.
5. **Re-open what you cite.** The course only allows sources you opened. Spot-check the operation searches for Amanã, Kayapó and Yanomami.
6. **Team plan:** add members and roles to `templates/TEAM_PLAN.docx`.
7. **AI prompt for brief part 4:** it was run in Claude (`docs/brief/ai_part4_raw.md`). If the course expects your own tool, re-run it.
8. **Merge:** the work sits on branch `analysis/v2-raster`. Opening a pull request into `main` is your call.

:::more Nice to have, and the plan as a diagram
- **Munduruku before 2022:** search for operations in 2019–21. One may explain its early fall.
- **IBAMA embargo file:** no download link found.

{{NEXT_STEPS_DIAGRAM}}
:::

## Files | Where everything lives

**Run everything:** `uv run python code/main.py` (about 2 minutes). It writes every figure, table and number to `output/`.

:::more The code map
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

- **Brief draft:** `docs/brief/brief_content.md` → `BRIEF_DRAFT.html`. **Methods:** {{METHODS_LINK}}.
- **Operation searches:** `docs/overnight/notes/control_interventions.md`, `brazil_data_and_operations.md`.
- **Log and decisions:** `docs/overnight/LOG.md`. **Data log:** `DOWNLOAD_LOG.csv`.
- **Big raw files are git-ignored** (Amazon Mining Watch, RAISG, MapBiomas Amazonía, FUNAI). The run then uses the small files in `data_intermediate/`. Download links are in `DOWNLOAD_LOG.csv`.
:::

## Appendix | Data checks, decisions and every number

**One check per dataset.** Full log in `DOWNLOAD_LOG.csv`.

| Data | Our number | Publisher shows | Status |
|---|---|---|---|
| MapBiomas Peru, Collection 4, buffer zones (course data) | Tambopata buffer zone 2025 = 20,730 ha | 20,730 ha | Match |
| MapBiomas Peru, Collection 4, protected areas (new) | Tambopata reserve 2025 = {{anp_level_tam_nr_2025:,.1f}} ha | 777 ha | Match |
| MapBiomas Brazil, Collection 11, indigenous lands (course data) | 2025 = {{br_pack_art_level_2025}} ha | 39,915 ha (card) | Match |
| MapBiomas Brazil, Collection 10.1, per territory (new) | Kayapó 2024 = {{br_ti_kayapo_stock_2024}} ha | 17,632 ha (Collection 11) | Mismatch: different collection |
| MapBiomas Brazil, Collection 11 rasters (new) | Kayapó 2024 = {{brv2_kayapo_check_2024}} ha | 17,632 ha | Match |
| MapBiomas Peru, Collection 4 rasters (new) | Tambopata buffer zone 2025 = {{v2_check_tambopatabufferzone_2025}} ha | 20,730 ha | Match |
| MEF anti-illegal-mining spending (new) | Madre de Dios 2019 = {{t8_pp0128_mdd_2019:,.0f}} soles | 31,120,611 | Match |
| INPE DETER mining alerts (new) | 2019 = {{br_deter_2019_total_wfs_km2:.2f}} km² | {{br_deter_2019_total_dashboard_km2:.2f}} km² | 0.2% off |
| Gold production, BCRP/MINEM (new) | Monthly sums = annual | — | Internal only |
| IBAMA fines (new) | — | No total online | Not checkable |
| World Bank gold price (course data) | Aug 2026 = $4,411/oz | $4,411/oz | Match |
| MapBiomas Amazonía, Collection 6 (new) | Amazon mining 2023 = 775,746 ha | 0.78 Mha (factsheet p.3) | Match |
| MapBiomas Brazil, Collection 11, mining module (new) | Garimpo 2025 = 445,987 ha | 445,987 ha | Match |
| RAISG protected areas (new) | 401 areas downloaded | 401 in the service | Match |
| Amazon Mining Watch | — | No totals published | Not checkable |

:::more Decision log (from docs/overnight/LOG.md)
{{DECISIONS_TABLE}}
:::

:::more Every number, filterable (from output/numbers.csv)
{{NUMBERS_TABLE}}
:::
