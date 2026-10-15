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

# Net new mining in La Pampa fell for two years. Then it grew across the road.

> What Operation Mercurio did to illegal gold mining in Madre de Dios, Peru, and what FZS should expect when an operation ends. Team walkthrough: the story first, every analysis behind it, every number from `output/numbers.csv`.

:::stats
{{mean_add_tambopata_2016_18}} → {{mean_add_tambopata_2019_21}} || ha/yr of net new mining in the Tambopata buffer zone, 2016–18 vs 2019–21
{{v2_corridor_share_2016_18:.0f}}% → {{v2_corridor_share_2022_25:.0f}}% || share of new mining inside the legal corridor, 2016–18 vs 2022–25
{{v2_new_total_2016_18}} → {{v2_new_total_2022_25}} || ha/yr of first-time mining in all of Madre de Dios: the region did not mine less
{{gold_broad_lapampasector_depleted_2018:.0%}} || of La Pampa's gold-bearing land mined by 2018: the gold was not gone
:::

@part The story

## The story in one minute | Mining fell where enforcement landed, while it lasted

**After Mercurio began, net new mining in La Pampa fell for about two years. New mining grew across the nearest legal boundary and on old pits, and the region kept growing.** [[D]]

:::beats
Before || La Pampa was Peru's largest illegal mining area: {{mean_add_tambopata_2016_18}} ha of net new mining a year (2016–18). || #where-it-went
During || Net new mining fell to {{mean_add_tambopata_2019_21}} ha/yr in 2019–21. Clearing went on through 2019 and collapsed in 2020. || #timing
Next door || First-time mining directly across the highway, in the legal corridor, rose from {{v2_new_corridoracrosstheroa_2016_18}} to {{v2_new_corridoracrosstheroa_2019_21}} ha/yr. || #across-the-road
After || La Pampa came back to {{mean_add_tambopata_2022_25}} ha/yr in 2022–25, much of it on old pits. Mining inside the reserve jumped in 2025 (+{{anp_tam_nr_addition_2025}} ha). || #old-pits
Region || First-time mining in Madre de Dios doubled, from {{v2_new_total_2016_18}} to {{v2_new_total_2022_25}} ha/yr. || #where-it-went
:::

**Is it causal?** Only conditionally, and only for **net** new mining in 2019–21. *If* the comparison zones show what Tambopata would otherwise have done, Mercurio and the operations that followed lowered net new mining in the target by roughly {{sdid_sc_ha_during:,.0f|abs}} to {{model_m3_during:,.0f|abs}} ha/yr, depending on how the comparison is weighted. [[C]] It holds in hectares, not relative to size; with one targeted zone the best attainable p is {{model_m1_ri_p:.2f}}; and the fall coincides with COVID: nothing falls in 2019 (La Pampa per 1-km cell {{st_event_lp_2019:+.2f}} ha vs 2014–18, p = {{st_event_lp_2019_p:.2f}}), and first-time mining stayed near its peak that year.

**Why it matters:** we expect an operation to buy a pause, not an end. [[P]] FZS should plan for what comes after the patrols leave: the legal side of the boundary, old pits, and the river posts.

## The brief | Four parts, one figure, one conditional causal sentence

**The 2-page brief tells the story above in the course's four parts.** The brief draft has its own page: {{BRIEF_LINK}}.

| Brief part | What it says | Evidence on this page |
|---|---|---|
| **1. The question** | FZS pays for enforcement. What happens in the target, and around it, when an operation ends? | [The rules](#the-rules), [The places](#the-places) |
| **2. Data** | MapBiomas Peru Collection 4, one check per dataset | [Appendix](#appendix) |
| **3. Findings** | Net new mining fell for two years, grew across the road, came back; the region grew. One conditional causal claim. | [Where it went](#where-it-went) to [Claims](#claims) |
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

:::more The legal detail and who mines
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

**Who enforces, and when:** the dated timeline is in [Context](#context).

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

## Where it went | The legal corridor's share of new mining rose

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

**Not all corridor growth can be La Pampa's mining moving.** The rest of the corridor gained far more than La Pampa lost ({{v2_new_restofminingcorridor_2016_18}} → {{v2_new_restofminingcorridor_2022_25}} ha/yr), so most of it cannot be La Pampa's mining moving; new entrants and the gold price fit better (not tested). [[D]]

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

**Why it matters:** after 2019, new mining shifted from illegal to legal land. [[D]] For the reserve that is good news. For the region it is not: total new mining kept growing, and corridor mining still uses mercury.

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

## Across the road | New mining jumped across the highway, then spread deeper

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
take: Right after Mercurio new mining hugged the road; then it spread deeper into the corridor.
:::

- **The jump is unusual:** rank {{t1_road_shift_rank_clean:.0f}} of {{t1_road_shift_n_clean:.0f}} non-overlapping start years (p = {{t1_road_shift_ri_p_clean:.2f}}, the smallest possible with {{t1_road_shift_n_clean:.0f}} start years). [[D]]
- **Hugging the road:** mean depth fell from {{t9_depth_2016:.0f}} km (2016) to {{t9_depth_2020:.0f}} km (2020), then reached {{t9_depth_2025:.0f}} km by 2025. [[D]]

**Why it matters:** a two-lane road is no barrier. After any operation south of the highway, expect a response north of it. [[P]]

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
- **Caveat:** the old-pit count includes year-to-year map flicker: La Pampa already showed {{v2_lapampa_remined_2016_18}} ha/yr of "returns" in 2016–18. Trust the 2023 jump, not small changes.

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

**Why it matters:** exhaustion does not explain the move. [[D]]

:::more How we measured gold in the ground
- **The proxy:** no one publishes gold left in the ground. Gold here is alluvial, so we used the national geology map (INGEMMET, 1:100,000): river deposits plus the gold-bearing terraces of the Madre de Dios Formation.
- **Does it work?** {{gold_broad_validation:.0%}} of all land ever mined lies on these units, which cover {{gold_broad_land_share_mdd:.0%}} of Madre de Dios ({{gold_broad_lift:.1f}}× more mining than chance). The strict river-deposit units cover {{gold_strict_land_share_mdd:.0%}} and hold {{gold_strict_validation:.0%}} ({{gold_strict_lift:.1f}}×). La Pampa was {{gold_strict_lapampasector_depleted_2018:.0%}} depleted by 2018 under the strict definition too.
- **Limits:** the map is coarse and says nothing about gold grade; old pits can be mined again.

**Code:** `code/raster_gold.py`.
:::

## Inside the reserve | In 2025, mining inside the reserve jumped

**The course data covers only buffer zones. Inside Tambopata National Reserve, mining reached {{anp_level_tam_nr_2025:,.0f}} ha in 2025, {{anp_tam_nr_addition_2025}} ha of it new that year.** [[D]]

:::fig output/fig_peru_inside_reserves.png
read: Mining area inside each reserve compared with its buffer zone, from the MapBiomas protected-area statistics we downloaded (checked: 777 ha on the platform).
take: Inside the reserves, mining stayed small for years; in 2025 it jumped inside Tambopata.
:::

- **Two other sources agree:** MAAP #241 reports ~500 ha of new mining inside the reserve (late 2025 to Feb 2026); Amazon Mining Watch shows {{sp_amw_tambopata_nr_new_ha_2025}} ha in 2025 (provisional). [[D]]
- **The trigger:** the 2025 incursion came after the navy left its Malinowski River posts (MAAP #241).
- **It happened before:** by October 2016, 521 ha inside the reserve had been lost to mining, with losses up 37% after the 2012–13 interdictions (Asner & Tupayachi, 2017). Different maps, so we don't subtract.
- **Where inside:** {{rd_reserve_inside_share_1km:.0%}} of first-time mining inside the reserve lies within 1 km of its edge ([Attempt 4](#attempt-4)). [[D]]

**Why it matters:** this is FZS's core area, and the most actionable finding.

:::more The 2017 jump and the code
- The 2017 jump (+{{anp_tam_nr_addition_2017}} ha) looks partly like a map reclassification, not real mining. [[D]]

**Code:** `code/peru_anp.py`.
:::

## Declared gold | The official gold drop is a definition change

**The official Madre de Dios gold series fell {{pe_prod_fall_2018_2025_pct:.0f}}% from 2018 to 2025, but that is entirely a definition change: declared output rose.** Until 2019 it included an *estimate* of artisanal gold; from 2020 it counts only what producers declare. [[D]]

:::fig output/fig_peru_gold_definition.png
read: Madre de Dios gold in the ministry's yearly files, split into what producers declared and the artisanal estimate the ministry added.
take: The "collapse" is the estimate disappearing in 2020; declared output rose.
:::

- **Declared output rose:** {{gold_minem_declared_2018_kg:,.0f}} kg (2018) → {{gold_minem_declared_2025_kg:,.0f}} kg (2025). The estimate was {{gold_minem_estimate_2019_kg:,.0f}} kg in 2019 and is absent from 2020.
- **We withdrew** our earlier "collapse" and its break test: they measured the definition change.

**Why it matters:** official production says almost nothing about mining here. Don't cite "−88%".

:::more The 2015 break, and the "mining in the corridor, declaring nothing" idea
- **The series:** the ministry's files carry "PRODUCTORES ARTESANALES — cifras estimadas" for Madre de Dios until 2019 ({{gold_minem_estimate_2016_kg:,.0f}} kg in 2016, {{gold_minem_estimate_2019_kg:,.0f}} kg in 2019). In 2016, that estimate plus declared output equals the central bank's figure exactly.
- **An earlier break in 2015:** until 2014, artisanal producers' own declarations were in the series ({{gold_minem_declared_2014_kg:,.0f}} kg in 2014); from 2015 producers declared only {{gold_minem_declared_2015_kg:,.0f}} kg and the ministry added an estimate.
- **For the idea:** {{leg_medium_share_2022_25:.0%}} of first-time mining in 2022–25 sat in concessions not verified as active; producers declare about 1 t a year while first-time mining covers over {{v2_new_total_2022_25}} ha a year; only 145 of 9,592 registered miners were fully formal (2021); Bolivia's gold exports jumped from 1.7 t (2012) to 35.7 t (2014); nationally at least 80 of ~180 t exported in 2024 had unknown origin.
- **Against:** gold may be declared in other regions; mapped area includes re-mined pits; gold yield per hectare is unknown.
- **Label:** plausible mechanism, not a finding.

**Code:** `code/peru_gold_minem.py` (checked against the central bank for 2012 and 2019), `code/peru_production.py`. **Source:** `docs/overnight/notes/legality_data.md`.
:::

## Context | Enforcement comes in waves tied to governments and budgets

**Other events line up with the mining curve.** Enforcement money peaked in 2019 and faded; COVID pulled forces away in 2020; a new government arrived in 2021. [[D]]

:::fig output/fig_v2_timeline.png
read: Top: events by type (enforcement, presidents, laws, context). Below: land mined for the first time each year in La Pampa and in all of Madre de Dios. Shaded = operation years (2012–13 and 2019–21).
take: Both enforcement waves started within a year of a new president and faded within about two.
:::

:::fig output/fig_v2_enforcement_spending.png
read: Executed spending of Peru's anti-illegal-mining programme (PP 0128) booked in Madre de Dios, next to first-time mined land. A lower bound: national units book under Lima.
take: Spending peaked in 2019 and fell as mining rebounded.
:::

- **One dip, not two:** La Pampa first-time mining changed by {{tl_dip_2012_13:+.0%}} in 2012–13 vs 2010–11, and by {{tl_dip_2020_21:+.0%}} in 2020–21 vs 2017–18. [[D]]
- **Money:** {{t8_pp0128_mdd_2018:,.0f}} soles (2018), {{t8_pp0128_mdd_2019:,.0f}} (2019), {{t8_pp0128_mdd_2021:,.0f}} (2021), {{t8_pp0128_mdd_2025:,.0f}} (2025). [[D]]
- **Gold price:** up {{gold_price_ratio_2025_2018:.1f}}-fold from 2018 to 2025. It pushes everywhere at once, which the year effects in [Attempt 1](#attempt-1) remove.

**Do these events explain the fall? Mostly not.** The models already remove anything that hit every zone in the same year: the gold price, COVID as a national shock, a new president. What's left is *different exposure*, so we add it as controls. [[D]]

:::fig output/fig_peru_context_models.png
read: Left: Tambopata's 2019–21 gap (ha/yr, against 14 other buffer zones) as we add controls: K0 = gold price × size; K1 + COVID 2020–21 × size; K2 + Madre de Dios × enforcement money; K3 both. Right: each year's gap against the money spent that year.
take: COVID exposure shrinks the gap, money barely moves it, and Tambopata stays first; years with more money had a weakly bigger fall.
:::

- **COVID:** controlling for how hard each zone was exposed shrinks the gap to {{ctx_k1_during:,.0f|abs}} of {{ctx_k0_during:,.0f|abs}} ha/yr. Still rank {{ctx_k1_rank:.0f}} of {{ctx_n:.0f}}. [[D]]
- **Money:** adding Madre de Dios × spending gives {{ctx_k2_during}} ha/yr; both together {{ctx_k3_during}} ({{ctx_k3_vs_k0_share:.0%}} of the baseline). But money is partly the treatment itself (a bad control), so "keeps {{ctx_k3_vs_k0_share:.0%}}" is not reassurance. [[D]]
- **Dose:** the yearly gap and spending correlate at r = {{ctx_dose_corr:.2f}} (2015–25): a weak link. [[D]]
- **Politics:** presidents and laws hit every zone at once, so year effects absorb them. They can't be tested separately with one region.

**Why it matters:** COVID exposure explains part of the gap, not all of it. Money and the operation arrived together, so we can't say which did the work.

:::more The enforcement timeline, politics, COVID, the 2017 spike and the earlier wave
**The enforcement timeline (dated):**

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
| 2025 | Navy withdrawn from Malinowski river posts; mining inside the reserve jumps |

- **The political-cycle idea:** both enforcement waves started 7–11 months after a new president (Humala 2011 → decrees 2012; Vizcarra 2018 → Mercurio 2019). That's a pattern, not evidence; we found no study of Peruvian election effects (Brazilian studies find more deforestation in election years).
- **Earlier wave in the course table:** Tambopata's gap in 2012–13 was +{{t3_wave_m1_2012_13}} ha/yr, rank {{t3_wave_rank:.0f}} of {{t3_wave_n:.0f}}: no Tambopata-specific dip. [[D]]
- **COVID:** forces left La Pampa in spring 2020; budgets fell sharply in 2020–21 (Mongabay 2023). That fits the 2022–25 rebound.
- **The 2017 spike:** 2017 was the record year for mining deforestation (Caballero Espejo et al. 2018). The gold price was flat (about $1,250/oz, 2016–18), so it doesn't explain it. Gangs ("Guardianes de la Trocha") ran extortion in La Pampa, but no source dates a 2017 takeover; part of the jump may be map reclassification. Mercury controls after Peru ratified the Minamata Convention (2016) made mercury a smuggling business; plausible, undocumented.

- **Why controlling for money is tricky:** spending rose *because of* Mercurio. Controlling for it removes part of the effect we measure. A smaller gap would mean "money and the operation move together", not "the operation didn't matter". The gap didn't shrink, and the spending coefficient is positive ({{ctx_k2_spend_coef:+.0f}} ha/yr per log-point), consistent with money following mining; we cannot tell the direction.
- **Asner & Tupayachi (2017)** report a brief dip after the 2012 interdictions ("said to have eradicated 90% of miners" in the buffer zone), then a near doubling, also inside the reserve (losses up 37% after 2012). Our MapBiomas data show no 2012–13 dip in La Pampa ({{tl_dip_2012_13:+.0%}} vs 2010–11), and in the course table Tambopata ranks {{t3_wave_rank:.0f}} of {{t3_wave_n:.0f}} for 2012–13. The first cycle is theirs, not ours.

**Code:** `code/v2_extra.py` (timeline), `code/v2_tests.py` (spending, 2012 wave), `code/peru_context_models.py` (controls). **Sources:** `docs/overnight/notes/qualitative_background.md`, `enforcement_intensity.md`.
:::

@part Is it causal?

## Six attempts | Six methods, mixed verdicts: the hectare fall is unusual, the scaled fall ordinary, and matching can't beat chance

**We tried six ways to build "what would have happened without Mercurio". None is clean, and they don't all agree.** In hectares, Tambopata's 2019–21 net fall stands out against other Peruvian zones; relative to its size it doesn't; against matched areas abroad it can't be told from chance. At the road, the swing north is borderline.

| Attempt | Compares | Result | Disagrees on | Verdict |
|---|---|---|---|---|
| **1 Difference-in-differences** | Tambopata vs 14 Peruvian buffer zones; 1-km cells | {{model_m1_during}} to {{model_m3_during}} ha/yr (M1–M3; {{model_m3pre_during}} with pre-year trends); rank 1 of 15 in hectares | Scaled to size rank {{model_m4_rank:.0f}} of {{model_m4_n:.0f}}; cell pre-trends fail and the comparison cells hold almost no mining, so the cell panel is close to a before/after | **Partly works** |
| **2 Synthetic control** | weighted mix of Peruvian zones | {{sdid_sc_ha_during}} ha/yr, rank 1 | La Pampa is too big to copy: no pre-2019 fit in hectares | Weak check |
| **3 Rule-based twins** | Amanã and Tapajós (Brazil) | Tambopata at {{top3_median_ratio:.0%}} of their pace | Tambopata grew faster than both before 2019; no p-value possible | Weak check |
| **4 Spatial RD** | land just either side of the road and the reserve edge | Road step {{rd_road_did:+.1f}} pts (p = {{rd_road_did_p:.2f}}) | Road p across bandwidths {{rd_road_sens_p_min:.2f}}–{{rd_road_sens_p_max:.2f}}; fake-start rank {{rd_road_fake_rank:.0f}} of {{rd_road_fake_n:.0f}} from {{rd_road_fake_first_year:.0f}} (p = {{rd_road_fake_p:.2f}}); reserve edge null ({{rd_reserve_did:+.1f}}, p = {{rd_reserve_did_p:.2f}}) | Borderline, for the swing only |
| **5 Matching (PSM and six others)** | areas picked by algorithm across the Amazon | All 7 find Tambopata slower | Placebo p {{psm_p_min:.2f}}–{{psm_p_max:.2f}}; no common support | Can't decide |
| **6 Synthetic DiD** | weighted zones, trend-matched | {{sdid_sdid_ha_during}} ha/yr, rank 1 | From 2011 only {{sdid_sdid_ha_during_pre2011}} ha/yr; scaled rank {{sdid_sdid_scaled_during_rank:.0f}} of {{sdid_sdid_scaled_during_n:.0f}} | Same as Attempt 1 |

**Why it matters:** only the zone-level designs clear their placebo floor, and only in hectares. That supports one conditional sentence, not more.

:::more Which attempt answers which question, and what we didn't try
| Question | Best attempt | Why |
|---|---|---|
| Did La Pampa fall more than elsewhere? | 1 and 6 | Many comparison zones, placebo ranks |
| Did it fall more than a look-alike? | 3 and 5 | Real areas abroad, picked by rules or algorithms |
| Did miners cross the legal line? | 4 | Same land either side of one border |
| Did the reserve border hold? | 4 | The reserve edge as a border |

**Not tried, and why:**
- **Callaway–Sant'Anna or Sun–Abraham:** built for many units treated at different dates. Peru has one; Brazil's staggered version is done (did2s, [Brazil](#brazil)).
- **Synthetic control with prediction intervals (conformal inference):** needs a good pre-fit, which Attempt 2 can't get in hectares.
- **Bayesian structural time series (CausalImpact):** predicts Tambopata from other series; same donor problem as Attempt 2, with stronger assumptions.
- **Instrumental variables** (e.g. gold price × gold geology): the gold price drives mining directly, so the exclusion restriction fails.
- **Spatial DiD with spillover rings (Butts, 2023):** partly done as the road gradient in the cell panel.
:::

## Placebos | A fake test shows whether the real result stands out

**A placebo runs the same analysis where nothing happened. If the fakes look as big as the real result, the real result can't be told from noise.** We use placebos instead of standard errors, because one treated zone makes standard errors untrustworthy (Conley & Taber, 2011).

:::fig output/fig_placebo_explainer.png
read: Each row runs one analysis many times. Grey dots: the fakes (another zone gets the "operation", or the operation "starts" in another year). Orange: the real result. The real result's rank among all of them is the p-value.
take: In hectares, Tambopata's fall is far outside every fake. Scaled to size, two fake zones fall as much. At the road, the 2019 jump north beats every fake start year, but there are only a few.
:::

- **What:** we pretend. **Fake place:** give "Mercurio" to another zone. **Fake date:** pretend it started in 2016. **Fake border:** move the border 2–4 km into one side.
- **How:** run the identical analysis on every fake, line them up, and rank the real one. Rank 1 of {{plc_m1_n:.0f}} means p = 1/{{plc_m1_n:.0f}} = {{model_m1_ri_p:.2f}}.
- **The logic:** if Mercurio did nothing, Tambopata is just one more zone, and it has a 1-in-{{plc_m1_n:.0f}} chance of ranking first by luck.
- **Why we do it:** it shows how big "nothing happened" can look in *this* data, with its noise, its booms and its map flicker.

**What it proves, and what it doesn't:**
- **A pass shows the real result is unusual,** not that Mercurio caused it. Anything else that hit only Tambopata in 2019 would pass too.
- **A fail is decisive.** If a fake is as big as the real one, we can't tell the real result from noise. Scaled to size (rank {{plc_m4_rank:.0f}} of {{plc_m4_n:.0f}}, p = {{model_m4_ri_p:.2f}}), that's what happens.
- **The floor:** with {{plc_m1_n:.0f}} zones, p can't go below {{model_m1_ri_p:.2f}}. With {{plc_road_n:.0f}} clean start years at the road, it can't go below {{t1_road_shift_ri_p_clean:.2f}}. "Rank 1" is as strong as these tests get.

**Why it matters:** placebos are our honesty check. They're why we call the hectare fall "unusual" and the scaled fall "ordinary".

:::more Every placebo we run, and its result
| Analysis | Placebo | Real result | Placebo result |
|---|---|---|---|
| Model ladder M1 (hectares) | fake places (14 zones) | {{model_m1_during}} ha/yr | range {{model_m1_placebo_min:,.0f}} to +{{model_m1_placebo_max:,.0f}}; rank 1 of {{model_m1_n}} |
| Model ladder M1 | fake date (2016, on 2011–18) | {{model_m1_during}} ha/yr | +{{model_m1_placebo}} (opposite sign: pass) |
| Model ladder M3 (own trends) | fake date | {{model_m3_during}} ha/yr | {{model_m3_placebo}} (same sign: weak fail) |
| Model ladder M4 (scaled) | fake places (6 zones) | {{model_m4_during:.2f}} normal years | rank {{model_m4_rank:.0f}} of {{model_m4_n:.0f}} (fail) |
| Context models K0–K3 | fake places | {{ctx_k3_during}} ha/yr (K3) | rank {{ctx_k3_rank:.0f}} of {{ctx_n:.0f}} |
| Road: share north of the highway | fake start years | +{{t1_road_shift_2019:.2f}} share points | rank {{t1_road_shift_rank_clean:.0f}} of {{t1_road_shift_n_clean:.0f}} |
| Spatial RD at the road | fake start years {{rd_road_fake_first_year:.0f}} on | {{rd_road_did:+.1f}} pts | rank {{rd_road_fake_rank:.0f}} of {{rd_road_fake_n:.0f}} (p = {{rd_road_fake_p:.2f}}) |
| Spatial RD at the road | fake borders ±2–4 km | {{rd_road_did:+.1f}} pts | largest {{rd_road_pb_max_abs:.1f}}; {{rd_road_pb_n_sig:.0f}} of 6 significant |
| Spatial RD at the reserve edge | fake start years | {{rd_reserve_did:+.1f}} pts | rank {{rd_reserve_fake_rank:.0f}} of {{rd_reserve_fake_n:.0f}} (p = {{rd_reserve_fake_p:.2f}}) |
| Cell panel | pre-trend leads 2010–13 | {{st_main_lapampasector_during:+.2f}} ha/cell | joint p = {{st_event_lp_pretrend_p:.3f}} (fail for La Pampa) |
| Synthetic control | each donor as the target | see [Attempt 2](#attempt-2) | rank {{synth_core_addsc_rank}} of {{synth_core_addsc_n_units_ranked}} |
| Brazil staggered DiD (TWFE) | 2,000 shuffled operation dates | {{brv2_twfe_treat:+.2f}} log points | one-sided p = {{brv2_ri_p:.2f}} (fail) |

**Two kinds of placebo answer two questions.** Fake places ask "is Tambopata special?". Fake dates ask "is 2019 special?". A result that passes both is hard to explain by luck alone. It can still be explained by something else that happened in Tambopata in 2019, which is why the claim stays conditional.

**Code:** `code/placebo_explainer.py` (figure), `code/peru_models.py`, `code/v2_tests.py`, `code/v2_rdd.py`.
:::

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

- **M3 with trends fitted on pre-years only:** {{model_m3pre_during}} ha/yr in 2019–21 ({{model_m3pre_after}} in 2022–25), the largest variant; the brief's range stops at M3.
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
take: Tambopata and Amanã both stood at about half their 2018 size in 2014; in 2019–21 Tambopata went flat while Amanã kept growing.
:::

:::fig output/fig_control_top3.png
read: Tambopata against the two twins that pass the relaxed rules: growth before 2019 and pace in 2019–21.
take: Tambopata ran below both twins in 2019–21, but it also grew faster than them before.
:::

- **Relaxed rule:** no operation in 2017–21 only. {{ctl_n_relaxed}} areas pass; best fit **Amanã National Forest**, then the Tapajós protection area. [[D]]
- **2019–21:** Tambopata {{top3_tam_during:.1f}}% of its 2018 stock per year; Amanã {{top3_amana_twin_during:.1f}}%; Tapajós {{top3_tapajos_twin_during:.1f}}%. [[D]]

**Why it matters:** a second comparison, picked by rules, not results, points the same way as Attempt 1. But Tambopata grew faster than both twins before 2019 (pre-trend tests p = {{top3_amana_pre_trend_p:.2f}} Amanã, {{top3_tapajos_pre_trend_p:.2f}} Tapajós), so it is a weak check.

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

- **No p-values for the gap:** three years per area make a t-test unreliable.
- **Pre-trends are not parallel:** Tambopata grew faster than both before 2019 (trend tests p = {{top3_amana_pre_trend_p:.2f}} and {{top3_tapajos_pre_trend_p:.2f}}), and the two sides come from different MapBiomas collections.
- **Threats:** Brazil weakened enforcement in 2019–22, so the twins may have grown faster than "normal". "No operation found" is not proof of none. On Amazon Mining Watch, Tambopata's 2019 value is its highest after 2018; the fall shows from 2020.
- **Ruby's caution holds:** "no intervention" is too strict (no area passes); "comparable enforcement" needs zone-level enforcement data that isn't public.

**Code:** `code/control_amw.py`, `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py`, `control_top3.py`. Searches: `docs/overnight/notes/control_interventions.csv`, coded in `data_intermediate/operations_coded.csv`.
:::

## Attempt 4 | At the road, the gap flipped; at the reserve edge, nothing changed

**A spatial regression discontinuity compares land just either side of a legal border, before and after Mercurio.** At the road the north side overtook the south. At the reserve edge the step didn't move. [[D]]

:::fig output/fig_v2_rdd.png
read: Left: land mined for the first time (% of land per year) by distance from each border; dashed = 2014–18, solid = 2019–21; lines are local fits on each side. Right: the step at the border in each year, with 95% intervals.
take: Before Mercurio the south side of the road (La Pampa) mined more; after, the north side (the corridor) did. At the reserve edge mining runs about 1 km inside, before and after alike.
:::

- **The road:** within {{rd_road_did_h:.1f}} km of the highway, the south mined {{rd_road_mean_pre_l:.1f}}% of its land a year in 2014–18 and the north {{rd_road_mean_pre_r:.1f}}%. In 2019–21: south {{rd_road_mean_post_l:.1f}}%, north {{rd_road_mean_post_r:.1f}}%. [[D]]
- **The step changed by {{rd_road_did:+.1f}} points** (95% interval {{rd_road_did_lo:+.1f}} to {{rd_road_did_hi:+.1f}}; p = {{rd_road_did_p:.2f}}). Dropping the 500 m next to the road: {{rd_road_sens_donut:+.1f}} (p = {{rd_road_sens_donut_p:.2f}}). [[D]]
- **The reserve edge:** the step changed by {{rd_reserve_did:+.1f}} points (p = {{rd_reserve_did_p:.2f}}). {{rd_reserve_inside_share_1km:.0%}} of all first-time mining inside the reserve since 2000 lies within 1 km of the edge. [[D]]

**Why it matters:** a border only works if it's enforced on both sides. New mining jumped across this legal line within a year. The reserve edge leaks about a kilometre along the river, and deeper inside the reserve has held.

:::more How the RD works, why it's a "difference in discontinuities", and its limits
**The idea.** Land 200 m north of the road and 200 m south of it has the same soil, rivers and gold, but a different legal status. Compare the two right at the line, and geography cancels out.

**Why not a plain RD?** At the road, the line also changes access: the road itself attracts mining. At the reserve, the Malinowski River runs along the edge. Those don't change over time. So we take the **change in the step**: the step after 2019 minus the step before. That's a *difference in discontinuities* (Grembi, Nannicini & Troiano, 2016).

**Set-up.**
- **Units:** 250-m distance bins inside 2-km segments along each border (road: {{rd_road_did_n:.0f}} units within the bandwidth; reserve: {{rd_reserve_did_n:.0f}}).
- **Road:** La Pampa's longitudes; south = La Pampa sector, north = the legal corridor across the road. No new polygons: the signed distance comes from the existing road line.
- **Reserve:** Tambopata National Reserve vs its buffer zone, only where the land outside is buffer zone.
- **Estimator:** `rdrobust` (Calonico, Cattaneo & Titiunik): local linear, triangular kernel, bandwidth chosen to minimise error (road {{rd_road_did_h:.1f}} km, reserve {{rd_reserve_did_h:.1f}} km), robust bias-corrected intervals, errors clustered by segment.

| Check | Road | Reserve edge |
|---|---:|---:|
| Step 2014–18 (north − south / inside − outside) | {{rd_road_level_pre:+.2f}} (p = {{rd_road_level_pre_p:.2f}}) | {{rd_reserve_level_pre:+.2f}} (p = {{rd_reserve_level_pre_p:.2f}}) |
| Step 2019–21 | {{rd_road_level_post:+.2f}} (p = {{rd_road_level_post_p:.2f}}) | {{rd_reserve_level_post:+.2f}} (p = {{rd_reserve_level_post_p:.2f}}) |
| **Change in the step, 2019–21 vs 2014–18** | **{{rd_road_did:+.2f}}** (p = {{rd_road_did_p:.2f}}) | **{{rd_reserve_did:+.2f}}** (p = {{rd_reserve_did_p:.2f}}) |
| Change, 2022–25 vs 2014–18 | {{rd_road_did_late:+.2f}} (p = {{rd_road_did_late_p:.2f}}) | {{rd_reserve_did_late:+.2f}} (p = {{rd_reserve_did_late_p:.2f}}) |
| Fixed bandwidth 1 / 2 / 3 / 5 km | {{rd_road_sens_h1:+.1f}} / {{rd_road_sens_h2:+.1f}} / {{rd_road_sens_h3:+.1f}} / {{rd_road_sens_h5:+.1f}} | {{rd_reserve_sens_h1:+.1f}} / {{rd_reserve_sens_h2:+.1f}} / {{rd_reserve_sens_h3:+.1f}} / {{rd_reserve_sens_h5:+.1f}} |
| Donut (drop 0–500 m) | {{rd_road_sens_donut:+.2f}} (p = {{rd_road_sens_donut_p:.2f}}) | {{rd_reserve_sens_donut:+.2f}} (p = {{rd_reserve_sens_donut_p:.2f}}) |
| Fake start years (rank of 2019) | {{rd_road_fake_rank:.0f}} of {{rd_road_fake_n:.0f}} (p = {{rd_road_fake_p:.2f}}) | {{rd_reserve_fake_rank:.0f}} of {{rd_reserve_fake_n:.0f}} (p = {{rd_reserve_fake_p:.2f}}) |
| Fake borders ±2–4 km, significant | {{rd_road_pb_n_sig:.0f}} of 6 | {{rd_reserve_pb_n_sig:.0f}} of 6 |

**The big limit: displacement breaks the RD.** An RD assumes one side doesn't affect the other. Here new mining fell south and rose north (plausibly some of the same miners moving), so the step opens from both sides at once. The road estimate is the **swing** (deterrence south + displacement north), not Mercurio's net effect. It is a description of the border, and an upper bound on what happened on either side alone.

**Other limits.** Wide intervals: only ~19 road segments, and mining comes in clumps. The main estimate (p = {{rd_road_did_p:.2f}}) is borderline; across bandwidths and the donut p runs {{rd_road_sens_p_min:.2f}}–{{rd_road_sens_p_max:.2f}}, and with fake start years from {{rd_road_fake_first_year:.0f}} the floor is {{rd_road_fake_p:.2f}}. The reserve result is a null: "no change" can't be told apart from "small change".

**Code:** `code/v2_rdd.py` (cached intermediates `data_intermediate/rdd_units_v2.csv`, `rdd_unit_year_v2.csv`; table `output/table_rdd.csv`).
:::

## Attempt 5 | Every matching method finds Tambopata slower; none beats chance

**We let seven matching methods pick Tambopata's comparison areas instead of hand-set rules.** All seven find Tambopata mining at {{psm_ratio_min:.0%}}–{{psm_ratio_max:.0%}} of its matches' pace in 2019–21. But areas with no operation often look just as "slow" against their own matches. [[D]]

:::fig output/fig_psm.png
read: Left: new mining per year in 2019–21 as % of each area's 2018 mining. Orange line = Tambopata; violet dots = the areas each method picks (first row: Ruby's rule-based twin). Right: Tambopata's gap (orange) against the gaps when each pool area plays "treated" (grey bars).
take: Every method finds Tambopata slower than its matches, but the gap sits inside the placebo range, so matching can't rule out chance.
:::

- **Same outcome as the twin:** Tambopata added {{psm_tam_pace_during:.1f}}% of its 2018 mining per year in 2019–21; its matches {{psm_ps_nn1_ctl_during:.0f}}–{{psm_ipw_ctl_during:.0f}}%. [[D]]
- **Placebo fails for all seven:** p = {{psm_p_min:.2f}} to {{psm_p_max:.2f}}; {{psm_n_methods_p10:.0f}} of {{psm_n_methods:.0f}} reach p ≤ 0.10. [[D]]
- **No common support:** Tambopata's propensity score ({{psm_ps_tam:.2f}}) is higher than every area in the pool (max {{psm_ps_pool_max:.2f}}). No area is "as likely to get an operation" as La Pampa was.

**Why it matters:** matching confirms the direction of Ruby's twin with a formal method. It also shows why one treated area can't carry a causal claim alone.

:::more Seven estimators, the propensity model, and why matching struggles here
**Pool:** {{psm_n_units:.0f}} Amazon areas with Amazon Mining Watch data; {{psm_n_pool:.0f}} with no operation in 2017–21, at least 100 ha of mining by 2018, and outside Madre de Dios.

**Propensity score:** a logit of "operation reported 2017–21" on pre-2019 traits (log mining stock in 2018, median elevation of the mining, log area, country and area type), fitted on the {{psm_ps_n:.0f}} areas with a known status ({{psm_ps_n_treated:.0f}} with an operation; pseudo-R² {{psm_ps_pseudo_r2:.2f}}).

| Method | Matches | Their pace, % per yr | Gap (pp) | Pace ratio | Placebo rank | p |
|---|---:|---:|---:|---:|---:|---:|
| Rule-based twin (Amanã) | 1 | {{psm_twin_ctl_during:.1f}} | {{psm_twin_gap_during:+.1f}} | {{psm_twin_ratio_during:.2f}} | — | — |
| Propensity score, nearest 1 | {{psm_ps_nn1_n_ctl:.0f}} | {{psm_ps_nn1_ctl_during:.1f}} | {{psm_ps_nn1_gap_during:+.1f}} | {{psm_ps_nn1_ratio_during:.2f}} | {{psm_ps_nn1_rank:.0f}} of {{psm_ps_nn1_n_placebo:.0f}} | {{psm_ps_nn1_p:.2f}} |
| Propensity score, nearest 5 | {{psm_ps_nn5_n_ctl:.0f}} | {{psm_ps_nn5_ctl_during:.1f}} | {{psm_ps_nn5_gap_during:+.1f}} | {{psm_ps_nn5_ratio_during:.2f}} | {{psm_ps_nn5_rank:.0f}} of {{psm_ps_nn5_n_placebo:.0f}} | {{psm_ps_nn5_p:.2f}} |
| Mahalanobis, nearest 1 | {{psm_maha1_n_ctl:.0f}} | {{psm_maha1_ctl_during:.1f}} | {{psm_maha1_gap_during:+.1f}} | {{psm_maha1_ratio_during:.2f}} | {{psm_maha1_rank:.0f}} of {{psm_maha1_n_placebo:.0f}} | {{psm_maha1_p:.2f}} |
| Mahalanobis, nearest 3 | {{psm_maha3_n_ctl:.0f}} | {{psm_maha3_ctl_during:.1f}} | {{psm_maha3_gap_during:+.1f}} | {{psm_maha3_ratio_during:.2f}} | {{psm_maha3_rank:.0f}} of {{psm_maha3_n_placebo:.0f}} | {{psm_maha3_p:.2f}} |
| Coarsened exact matching | {{psm_cem_n_ctl:.0f}} | {{psm_cem_ctl_during:.1f}} | {{psm_cem_gap_during:+.1f}} | {{psm_cem_ratio_during:.2f}} | {{psm_cem_rank:.0f}} of {{psm_cem_n_placebo:.0f}} | {{psm_cem_p:.2f}} |
| Entropy balancing (closest) | {{psm_ebal_n_ctl:.0f}} | {{psm_ebal_ctl_during:.1f}} | {{psm_ebal_gap_during:+.1f}} | {{psm_ebal_ratio_during:.2f}} | {{psm_ebal_rank:.0f}} of {{psm_ebal_n_placebo:.0f}} | {{psm_ebal_p:.2f}} |
| Inverse-probability weighting | {{psm_ipw_n_ctl:.0f}} | {{psm_ipw_ctl_during:.1f}} | {{psm_ipw_gap_during:+.1f}} | {{psm_ipw_ratio_during:.2f}} | {{psm_ipw_rank:.0f}} of {{psm_ipw_n_placebo:.0f}} | {{psm_ipw_p:.2f}} |

- **What each does:** *propensity score* matches on the predicted chance of getting an operation; *Mahalanobis* on distance in the traits themselves; *coarsened exact matching* on identical bins (stock, lowland); *entropy balancing* reweights the pool so its average traits equal Tambopata's; *IPW* weights every pool area by its odds of being treated.
- **With one treated area, PSM collapses to a distance rule.** Its strength (balancing many treated units on average) needs many treated units. Here it can only pick neighbours, like Ruby's rules do.
- **Weak balance:** after matching, traits still differ by up to about 1.3 standard deviations (`output/table_psm_balance.csv`). Entropy balancing can't reach exact balance (left gap {{psm_ebal_max_imbalance:.2f}} SD).
- **Stricter bins leave nothing:** coarsened exact matching with an area bin finds {{psm_cem3_n_matches:.0f}} areas, the same verdict as the strict rules.
- **Robust to the pool:** counting unclear or unsearched areas as "no operation" ({{psm_n_pool_unknown_none:.0f}} areas) keeps every gap negative.
- **2022–25 is noise:** one Brazilian territory (Sararé) surged, which drives the entropy-balancing and IPW gaps.

**Code:** `code/control_psm.py` (results `output/psm_results.csv`, balance `output/table_psm_balance.csv`).
:::

## Attempt 6 | Synthetic DiD agrees: biggest fall in hectares, ordinary for its size

**Synthetic difference-in-differences combines the twin idea with the model ladder:** weight the other zones so their trend before 2019 matches Tambopata's, then compare changes. Result: {{sdid_sdid_ha_during}} ha/yr in 2019–21, rank 1 of {{sdid_sdid_ha_during_n:.0f}}; scaled to size, rank {{sdid_sdid_scaled_during_rank:.0f}} of {{sdid_sdid_scaled_during_n:.0f}}. [[D]]

:::fig output/fig_sdid.png
read: Left: yearly additions in Tambopata vs a weighted mix of other buffer zones, shifted to Tambopata's level; grey bars are the weights on each pre-2019 year. Right: the same estimate with each other zone as "treated".
take: In hectares, Tambopata's 2019–21 fall is the biggest of 15 zones; scaled to its size it ranks 3 of 7. By 2022–25 the gap is gone.
:::

- **Three estimators, one function:** plain DiD {{sdid_did_ha_during}}, synthetic control {{sdid_sc_ha_during}}, synthetic DiD {{sdid_sdid_ha_during}} ha/yr (all rank 1 of {{sdid_sdid_ha_during_n:.0f}}, p = {{sdid_sdid_ha_during_p:.2f}}). [[D]]
- **Gone by 2022–25:** {{sdid_sdid_ha_after:+,.0f}} ha/yr, rank {{sdid_sdid_ha_after_rank:.0f}} of {{sdid_sdid_ha_after_n:.0f}}. [[D]]
- **Sensitive to the start year:** fitting on 2011–18 instead of 2014–18 shrinks it to {{sdid_sdid_ha_during_pre2011}} ha/yr, still rank 1.

**Why it matters:** the method built for "few treated units" gives the same two-sided answer as Attempt 1. That makes the answer robust, but not stronger.

:::more How synthetic DiD works
- **Unit weights:** non-negative, summing to 1, chosen so the weighted zones' pre-2019 *trend* matches Tambopata's. A free intercept absorbs the level gap, which is why it works where plain synthetic control failed ([Attempt 2](#attempt-2)).
- **Time weights:** pick the pre-years that best predict the post years ({{sdid_lambda_2018:.0%}} on 2018).
- **Weights found:** the largest single zone weight is {{sdid_top_weight:.0%}}; {{sdid_n_weighted:.0f}} zones get more than 1%.
- **Check:** with equal weights the estimator equals M1 exactly (asserted in the code).
- **Inference:** placebo in space, each other zone as "treated" with Tambopata removed.
- **Reference:** Arkhangelsky, Athey, Hirshberg, Imbens & Wager (2021), *American Economic Review* 111(12).

**Code:** `code/peru_sdid.py` (own implementation; results `output/peru_sdid.csv`).
:::

@part Brazil

## Brazil | Same method, weaker result: the direction, not the cause

**The big Brazilian territories fell after 2022–24, but not after their own operations.** The staggered test finds no significant effect. [[D]]

:::fig output/fig_brazil_v2_pixels.png
read: First-time mining and returns to old pits per territory, MapBiomas Brazil Collection 11, measured with the same pixel method as Peru. Dates mark each territory's own first operation.
take: Yanomami fell from 2024, a year after its operation; other territories don't line up with their own dates.
:::

- **Yanomami:** {{brv2_yan_new_2019_22}} ha/yr of first-time mining in 2019–22, {{brv2_yan_new_2023_25}} in 2023–25. [[D]]
- **Staggered DiD:** {{brv2_did2s_treat:+.2f}} log points (two-stage, two-sided p = {{brv2_did2s_treat_p:.2f}}); plain two-way fixed effects {{brv2_twfe_treat:+.2f}} (p = {{brv2_twfe_treat_p:.2f}}), randomization p = {{brv2_ri_p:.2f}} (one-sided, on the two-way estimate). Wrong sign, not significant. [[D]]
- **No spill next door:** rings around Yanomami got almost no new mining (0–10 km: {{brv2_r0_10_post:.1f}} ha/yr after 2023). ISA (2026) and Greenpeace report miners moving toward Venezuela and to territories like Sararé.

**Why it matters:** Brazil is consistent with "enforcement plus gold tracing goes with less mining", but our test can't confirm it, and national rules may matter as much as local operations. [[D]]

:::more Data, checks, the test, and why the null
- **Data:** MapBiomas Brazil Collection 11 maps, 1985–2025, read only around each territory (24 territories with mining + two rings around Yanomami).
- **Check:** Kayapó mining {{brv2_kayapo_check_2024}} ha (2024) and {{brv2_kayapo_check_2025}} ha (2025) vs 17,632 and 18,573 on the platform. This fixes the old Brazil mismatch (Collection 10.1 vs the platform's Collection 11).
- **Test:** territory + year effects, each territory treated from its own first *verified* operation in 2021–25 ({{brv2_n_treated:.0f}} of {{brv2_n_units:.0f}} territories); Gardner's two-stage estimator (two-sided p); randomization inference with 2,000 shuffles (one-sided, on the two-way fixed-effects estimate).
- **The comparison pool is thin:** {{brv2_never_n:.0f}} territories count as never treated, but {{brv2_never_n_unsearched:.0f}} of them were never searched for operations, so "no operation found" is not "no operation".
- **Why the null:** after correcting the dates (Munduruku from August 2023, its first verified operation; Kayapó from September 2024), territories still don't fall faster after their own operation. Sararé surged as its operation began, and the test has little power.
- **Products disagree on Yanomami's timing:** MapBiomas shows the fall from 2024; Amazon Mining Watch from 2023 ({{bs_yan_new_ha_2022}} → {{bs_yan_new_ha_2023}} ha); MAAP #242 reports about 1,800 ha (2022) and 330 ha (2023).
- **Support:** Amazon Mining Watch shows Yanomami −63% after its operation; IBAMA fines fell 2019–22 while mining tripled, then reversed in 2023.
- **Challenge:** a national change in January 2023 (new government, end of the gold "good faith" rule, electronic gold invoices from August 2023) hit all territories at once, which a territory-level design can't separate.

**Code:** `code/brazil_raster.py`, `code/brazil_v2.py`, plus `brazil_stagger.py` (AMW), `brazil.py`, `brazil_ibama.py`.
:::

@part So what

## For FZS | To protect the reserve, hold its edge and its river after the operation ends

**The reserve was breached after enforcement lapsed, not while it was on.** After Mercurio, mining returned by 2022, and mining inside the reserve jumped in 2025 (+{{anp_tam_nr_addition_2025}} ha), after the navy left the river posts (MAAP #241). [[D]] Asner & Tupayachi (2017) report a brief dip after the 2012 interdictions, then a near doubling, also inside the reserve; our MapBiomas data show no 2012–13 dip in La Pampa.

**Where we expect FZS's effort to protect the protected area most** [[P]]:

1. **Stay after the sweep.** Mercurio's fall faded within about three years, and the reserve incursion followed a withdrawal. Fund a permanent presence, not another one-off operation.
2. **Hold the first kilometre and the river.** {{rd_reserve_inside_share_1km:.0%}} of all first-time mining inside the reserve since 2000 lies within 1 km of its edge [[D]]. Staffed river posts on the Malinowski are a direct shield, given where the 2025 incursion came in. [[P]]
3. **Don't count on the buffer zone as a shield, yet.** In 2019–21 the step at the reserve edge did not measurably change ({{rd_reserve_did:+.1f}}, p = {{rd_reserve_did_p:.2f}}); we cannot tell whether buffer-zone enforcement shielded the reserve. [[D]]
4. **Expect a response across the nearest legal boundary.** First-time mining across the road rose within a year ([Attempt 4](#attempt-4)). [[D]]
5. **Monitor old pits, not only forest edges.** In 2023 most new mining in La Pampa was on old pits. Forest-loss alerts never see this.
6. **Make the legal corridor a real filter:** proof of gold origin, gold-buyer registers, real formalization deadlines, mercury checks. Brazil's 2023 reforms are a model.

:::fig output/fig_v2_risk_map.png
read: Predicted chance that a 1-km cell gets first-time mining in 2026–28, from a model trained on 2019–21 and tested out of sample on 2022–25.
take: Risk clusters next to old mining; the model adds little beyond "is there mining nearby?" and misses river-borne incursions.
:::

- **Where to look next:** the model flags {{risk_hi_cells_outside_corridor:.0f}} high-risk cells outside the legal corridor: {{risk_hi_cells_lapampasector:.0f}} in the La Pampa sector and {{risk_hi_cells_nativecommunitie:.0f}} in native communities. [[P]]
- **Honest score:** AUC {{risk_auc_spatial_holdout:.2f}} on held-out 10-km blocks, barely above {{risk_auc_benchmark:.2f}} for "mining nearby" alone. [[P]]

**Why it matters:** mining fell where enforcement landed, while it lasted. For the reserve, we expect the years after an operation to be the most exposed, and FZS can fund those years. [[P]]

:::more The social cost, and what data would let us say more
- **Damage:** Conservation Strategy Fund gives two separate estimates per kg of gold mined in Peru: US$ {{eco_param_social_calc_usd_kg_lo:,.0f}}–{{eco_param_social_calc_usd_kg_hi:,.0f}} (calculator) and US$ {{eco_param_social_pdf_usd_kg_lo:,.0f}}–{{eco_param_social_pdf_usd_kg_hi:,.0f}} (2023 report, p. 7). Quote both, never one merged range.
- **Mercury:** over a third of carnivorous fish exceed the limit hundreds of km downstream; exposed children score 4.68 IQ points lower.
- **Exploitation:** about 4,500 women are sexually exploited near camps, 78% of them minors.
- **Livelihoods:** about 46,600 people depend directly on mining. Enforcement without income alternatives invites return.
- **The corridor gap:** 0% royalty, 1.5% withholding, and only 145 of 9,592 registered miners fully formal (2021).
- **What would let us say more:** dated patrol and interdiction records per zone (SERNANP, FZS, police); concession and REINFO maps to grade legality pixel by pixel; pond-colour or dredge counts for activity on old pits and rivers.
:::

## Money | Illegal gold pays well, costs society far more, and outweighs enforcement money hundreds of times

**Informed speculation: mapped mining in Madre de Dios yields about {{eco_gold_t_lo_2022_25:.0f}}–{{eco_gold_t_hi_2022_25:.0f}} t of gold a year (2022–25), worth US$ {{eco_value_musd_lo_2022_25:,.0f}}–{{eco_value_musd_hi_2022_25:,.0f}} M. Producers declared {{eco_declared_t_2022_25:.1f}} t.** Every number here is our arithmetic on cited parameters, not a measurement. [[P]]

:::fig output/fig_v2_economics.png
read: Five yearly amounts for Madre de Dios, 2022–25, on a log scale (each tick = 10×). Bars span the low–high range our cited parameters allow; a dot means one value.
take: The gold mined and its social cost are hundreds of times the enforcement money booked in the region; the tax at stake is small next to both.
:::

- **Enforcement money is tiny next to the gold:** US$ {{eco_spend_musd:,.1f}} M a year booked in Madre de Dios (a lower bound), about {{eco_spend_share_of_value:.1%}} of the gold's value. [[P]]
- **Tax is a weak reason to stay illegal:** small producers pay **0% royalty**; income tax is only {{eco_tax_share_value_lo:.0%}}–{{eco_tax_share_value_hi:.0%}} of the gold's value. Location is the strong reason: La Pampa can never be formalized. [[P]]
- **Social cost dwarfs both:** two separate CSF estimates, US$ {{eco_social_busd_calc_lo:,.1f}}–{{eco_social_busd_calc_hi:,.1f}} bn a year (calculator) or US$ {{eco_social_busd_pdf_lo:,.0f}}–{{eco_social_busd_pdf_hi:,.0f}} bn (2023 report), mostly mercury's health damage. [[P]]

**Why it matters:** the lever is the *sale*, not the tax rate: make laundered gold hard to sell and the discount on illegal gold grows. At 2025 prices one hectare holds about US$ {{eco_gold_usd_per_ha_2025_lo:,.0f}}–{{eco_gold_usd_per_ha_2025_hi:,.0f}} of gold, which is why old pits are worth re-mining.

:::more The arithmetic, every parameter, and three ways to sell the same gold
- **The gold:** {{eco_ha_low_2022_25:,.0f}}–{{eco_ha_high_2022_25:,.0f}} ha worked a year × {{eco_param_yield_kg_ha_lo:.1f}}–{{eco_param_yield_kg_ha_hi:.1f}} kg per ha (CSF, 2023). Cross-check: MINEM's own 2016–18 estimate implies {{eco_implied_kg_ha_2016_18:.1f}} kg per ha we mapped.
- **Declared:** {{eco_declared_share_lo:.0%}}–{{eco_declared_share_hi:.0%}} of that gold shows up as declared Madre de Dios production. The rest leaves under someone else's paperwork or none.
- **Taxes not paid:** income tax (29.5% of an 11–37% margin): US$ {{eco_tax_musd_lo:,.0f}}–{{eco_tax_musd_hi:,.0f}} M a year.
- **Mercury:** {{eco_hg_t_lo:,.0f}}–{{eco_hg_t_hi:,.0f}} t a year.

| Parameter | Low | High | Source |
|---|---:|---:|---|
| Gold per hectare (kg) | {{eco_param_yield_kg_ha_lo:.1f}} | {{eco_param_yield_kg_ha_hi:.1f}} | CSF (2023), Cuadro 3, 2.5-m pits at Huepetuhe, Puquiri, Malinowski |
| Profit margin | {{eco_param_margin_lo:.0%}} | {{eco_param_margin_hi:.0%}} | Torres (2015, CooperAcción) via MINAM (2016) |
| Income tax | {{eco_param_income_tax_lo:.1%}} | {{eco_param_income_tax_hi:.1%}} | D.L. 1269 (general rate) |
| Mercury per kg of gold (kg) | {{eco_param_hg_per_au_lo:.1f}} | {{eco_param_hg_per_au_hi:.1f}} | CSF (2023), p.43 |
| Social cost per kg of gold, calculator (US$) | {{eco_param_social_calc_usd_kg_lo:,.0f}} | {{eco_param_social_calc_usd_kg_hi:,.0f}} | CSF calculator web page |
| Social cost per kg of gold, report (US$) | {{eco_param_social_pdf_usd_kg_lo:,.0f}} | {{eco_param_social_pdf_usd_kg_hi:,.0f}} | CSF (2023), p.7 |
| Soles per US$, 2022 / 2023 / 2024 / 2025 | {{eco_param_pen_per_usd_2022:.2f}} / {{eco_param_pen_per_usd_2023:.2f}} | {{eco_param_pen_per_usd_2024:.2f}} / {{eco_param_pen_per_usd_2025:.2f}} | BCRP annual averages, each year converted at its own rate |

- **Low vs high:** low = first-time mining only × low yield; high = first-time mining + returns to old pits × high yield. River dredges add gold but no mapped hectares, so even "high" may be low.
- **Yield is the weak link:** CSF found no grade for La Pampa's suction-pump method. Kg per hectare scales with pit depth: 5-m pits would double it.
- **Two social-cost estimates, never merged:** CSF's calculator and its 2023 report value mercury's health damage very differently. Quote both, and say which.
- **Cost per hectare kept out of the target:** PP 0128 spending in Madre de Dios, 2019–21, was about S/ {{eco_soles_per_ha_kept:,.0f}} per hectare of net mining kept out of the Tambopata buffer zone (using the zone-level gap, likely an upper bound). One hectare held US$ {{eco_gold_usd_per_ha_1921_lo:,.0f}}–{{eco_gold_usd_per_ha_1921_hi:,.0f}} of gold at 2019–21 prices. Those hectares moved; the region didn't mine less.

**Legal, informal, illegal: three ways to sell the same gold.**
- **Legal (formal):** a concession in the corridor, an environmental permit, taxes. Only 145 of 9,592 registered miners in Madre de Dios were fully formal (MINAM, 2021); nationally 2.4% (2024).
- **Informal (REINFO):** registered "in formalization", protected from prosecution (D.L. 1351) as long as they work outside banned zones. Nearly all Madre de Dios registrations sit inside the corridor (our overlay of MINEM's register).
- **Illegal:** outside the corridor, like La Pampa: it can never be formalized. Its gold sells at a discount (S/ 80 instead of S/ 180 per gram during the 2020 lockdown) or travels on corridor paperwork.
- **Crime:** extortion of S/ 1,000 per raft per week in La Pampa (Mongabay, 2026); illegal mining is now Peru's largest illegal economy, ahead of drugs (IPE, 2025).
- **National context (IPE, press reports):** illegal gold exports of about US$ 7.4 bn (2024) and over US$ 11.5 bn (2025), and 54% of Peru's export volume in early 2026. IPE's method (exports minus declared production) also catches stock changes and re-exports.
- **Don't cite:** the "25% of GDP" figure (Canal N) and the "44% of exports" snippet (it's Peru's share of South American illegal exports).

**Code:** `code/v2_economics.py`. **Sources with quotes and pages:** `docs/overnight/notes/economics_sources.md`. The CSF report is in `data_raw/literature/` and `DOWNLOAD_LOG.csv`.
:::

## What next | Informed speculation: pressure on the reserve rises from 2027

**Several forces point to more pressure on Tambopata, not less.** These are expectations from sources and our pattern, not findings. [[P]]

- **The window is the end of the next operation.** After a sweep we expect a local fall for about two years, new mining across the nearest legal boundary within a year, then a return to old pits and pressure on the reserve edge. [[P]]
- **Record gold prices** (about US$ 4,500/oz in 2026) make old pits pay again. [[P]]
- **The river is open:** the navy left the Malinowski posts in 2025, and mining inside the reserve jumped within months (MAAP #241). [[D]]

**Why it matters:** FZS can plan its support for the months after the next operation now.

:::more Five forces, the if–then table, what to watch, and how sure we are
1. **REINFO ends on 31 December 2026, on paper.** A new small-mining law (Ley MAPE, bill due 15 October 2026) would give about 30,000 registrants a two-year regime from 2027. Every deadline since 2012 has been extended. Expect another, under a new name.
2. **A new government.** The president elected in June 2026 campaigned on cracking down on illegal mining; Reuters judged that neither runoff candidate would dismantle REINFO quickly. Expect announcements and operations before budgets.
3. **Record gold prices.** Old pits pay again; the 2023 return in La Pampa coincided with rising prices.
4. **More operations, less money each.** Interdictions rose from 62 a month (2024) to over 130 (2026), while the national PP 0128 budget fell from S/ 121 M (2019) to S/ 70 M (2025). In Madre de Dios, booked spending fell from {{t8_pp0128_mdd_2019:,.0f}} to {{t8_pp0128_mdd_2025:,.0f}} soles.
5. **The river is open.** Organised crime now operates there: a safety issue for rangers, not only for the forest.

| If… | Then expect… [[P]] | Based on |
|---|---|---|
| A new operation hits La Pampa | A local fall in net new mining for about two years | [Attempt 1](#attempt-1) |
| … and the corridor across the road stays open | New mining across the road within a year | [Attempt 4](#attempt-4) |
| … and enforcement then lapses | A return to old pits within about three years, then pressure on the reserve edge | [Old pits](#old-pits), [Inside the reserve](#inside-the-reserve) |
| REINFO is extended again | La Pampa gold keeps travelling on corridor paperwork | [Money](#money) |
| Gold sales are traced (origin proof, buyer checks) | A bigger discount on illegal gold, the one lever that could act region-wide | Brazil 2023 ([Brazil](#brazil)) |

- **Watch:** GLAD alerts in the first kilometre inside the reserve; REINFO and Ley MAPE votes in December 2026; state-of-emergency renewals (the last we found: DS 093-2026-PCM, June 2026); river-post staffing; dredge counts.
- **How sure:** we see the pattern (fall, move, return) once, after 2019; Asner & Tupayachi (2017) report a similar cycle after 2012 that our data don't show. The politics are press-based; the original IPE reports and the full law texts were not opened.

**Sources:** `docs/overnight/notes/economics_sources.md` (section "Political and context items"), `qualitative_background.md`, `maap_citations.md`.
:::

## Limits | Every limitation, and which way it pushes the result

**Most of our limitations make Mercurio's local fall look bigger than it was, and most make displacement look smaller.** Most biases overstate the fall, so read it as likely an upper bound, and the displacement as likely a lower bound. [[D]]

**How to read the arrows:** ▲ = makes the 2019–21 fall in Tambopata look **bigger** than the truth (overstates Mercurio). ▼ = makes it look **smaller** (understates). ? = could go either way.

| Limitation | What happens | Fall in Tambopata | Displacement | How we checked |
|---|---|:---:|:---:|---|
| **Hectares, not people (2019–21)** | We count cleared land, a proxy for miners. Activity that moved to old pits and rivers adds few new hectares. | ▲ | ▼ | Old-pit accounting; MAAP #193 dredge counts. No data on people. |
| **Hectares, not people (2022–25)** | The same proxy makes the return look smaller than it was. | — (return understated) | ▼ | Old-pit accounting. |
| **Satellites miss river dredges and mercury** | Mining on the river doesn't show as land. Dredges in La Pampa rose from 148 to 598 (2021 → 2023, MAAP #193). | ▲ | ▼ | Named in part 4 of the brief; can't be fixed with these data. |
| **Spillovers into comparison zones** | If miners moved into comparison zones, they raised them. | ▲ (gap too wide) | — | Clean comparison cells exclude the corridor ([Attempt 1](#attempt-1)). |
| **Comparison zones were also treated** | Amarakaeri had its own operation (Dec 2019); Plan Restauración hit several zones. | ▼ (gap too narrow) | — | Compared against all 14 zones, not only Amarakaeri ([Attempt 1](#attempt-1)). |
| **Picked at its peak** | La Pampa was targeted *because* mining was at a record (2017). Records tend to fall back on their own. | ▲ | — | Fake-date tests; each 2019–21 year (at most {{tam_add_max_2019_2021}} ha) is below every 2011–18 year (at least {{tam_add_min_2011_2018}}). |
| **Size** | A bigger zone falls more in hectares just by being bigger. | ▲ in hectares | — | Scaled models: ordinary for its size ([Placebos](#placebos)). |
| **COVID (2020–21)** | Patrols left; if big mining zones reacted differently, part of the gap is COVID. | ▲ slightly | ? | Controlling for COVID exposure shrinks the gap to {{ctx_k1_during:,.0f|abs}} of {{ctx_k0_during:,.0f|abs}} ha/yr ([Context](#context)). |
| **Gold price** | Prices rose {{gold_price_ratio_2025_2018:.1f}}-fold 2018–25. Year effects remove the shared push. | ? (small) | ▼ for 2022–25 | M2 lets big zones react more: gap {{model_m2_during}} vs {{model_m1_during}} ha/yr. |
| **Enforcement money moved with the operation** | Spending peaked in 2019; controlling for it absorbs part of the effect itself. | ? | — | K2/K3 keep {{ctx_k3_vs_k0_share:.0%}} of the gap, but money is partly the treatment itself (a bad control). |
| **Map flicker and reclassification** | A pixel can switch class year to year; additions include re-mined scars. | ? (adds noise, not a direction) | ? | First-time mining as the main measure; identity check per pixel. |
| **Annual maps, a February start** | The 2019 map includes clearing from January–February 2019 and late 2018. | ▼ (first year blurred) | ▼ | Quarterly GLAD alerts ([Timing](#timing)). |
| **Legal or illegal?** | MapBiomas can't see legality; the corridor holds legal concessions and informal miners. | — | ? (illegal displacement could be over- or understated) | MAAP #235 legality layer, time-consistent ([Where it went](#where-it-went)). |
| **"No operation found" is not "no operation"** | A twin or match may have had an unreported operation. | ▼ | — | Logged searches; unclear areas tested as a variant ([Attempt 5](#attempt-5)). |
| **Twins in Brazil under weak enforcement (2019–22)** | The twins may have grown faster than "normal". | ▲ (vs the twins) | — | Used only as a second check, never alone. |
| **Displacement inside the RD** | Miners moving south → north open the road gap from both sides. | — | ▲ at the road (swing, not net) | Labelled as an upper bound ([Attempt 4](#attempt-4)). |
| **One treated zone** | No reliable standard errors. | ? (uncertainty, not a direction) | ? | Placebos instead ([Placebos](#placebos)). |

**Why it matters:** FZS should read our fall as "likely at most this big, for two years" and our displacement as "likely at least this much". We expect enforcement in one spot to buy a short pause, not a regional fall. [[P]]

:::more Hectares as a proxy for people
**We measure land, not miners.** Every hectare in this report is mapped mining land: MapBiomas pixels, Amazon Mining Watch squares, GLAD alerts. None of them counts people, camps or machines.

- **Why we can't do better:** no public, dated count of miners exists per zone. Censuses don't reach camps; REINFO lists registrants, not where they work; police reports count arrests, not people present.
- **When the proxy works:** while miners clear new forest, hectares track effort fairly well.
- **When it fails:** on old pits and rivers. One crew can work the same pit for years, adding no new hectares; a dredge adds none. After 2019 more of the activity moved to exactly these places ([Old pits](#old-pits)).
- **The direction:** hectares understate activity after a crackdown, when miners return to old ground. So the "return" in 2022–25 is likely a lower bound, and the "fall" in 2019–21 likely an upper bound for the fall in people.
- **What would fix it:** dredge counts from high-resolution imagery (as MAAP does), night-time lights over camps, mercury sales, or field counts by SERNANP and FZS rangers.
:::

## Claims | What we can say, how strongly, and the test behind it

| Claim | Label | Key test | Evidence against |
|---|---|---|---|
| Net new mining in Tambopata fell sharply in 2019–21 | [[D]] | Course table = raster; {{mean_add_tambopata_2016_18}} → {{mean_add_tambopata_2019_21}} ha/yr | First-time mining only halved ({{t5_m2_2016_18}} → {{t5_m2_2019_21}}); clearing continued through 2019 |
| *If* the comparison zones show what Tambopata would otherwise have done, Mercurio and the operations that followed lowered net new mining in the target by roughly {{sdid_sc_ha_during:,.0f|abs}} to {{model_m3_during:,.0f|abs}} ha/yr in 2019–21 | [[C]] *conditional* | Fake places, zone level: rank 1 of {{model_m1_n}} in hectares (p = {{model_m1_ri_p:.2f}}, the floor) | Ordinary relative to size; matching can't beat chance; coincides with COVID (nothing falls in 2019); Amarakaeri also treated |
| New mining grew in the legal corridor, across the road, then deeper | [[D]] | Corridor cells {{st_main_corridoracross_during:+.2f}} ha/cell-yr (p = {{st_main_corridoracross_during_p:.2f}}, pre-trends pass); depth break p = {{t9_depth_post2019_p:.3f}}; MAAP #208 (74%) | Can't show the same people moved; road RD borderline; the road was crossed before (2008) |
| New mining returned to old pits in 2023 | [[D]] | Raster accounting; MAAP #193 | Map flicker inflates old-pit counts |
| La Pampa had not run out of gold | [[D]] | Geology: {{gold_broad_lapampasector_depleted_2018:.0%}} mined by 2018 | Coarse map; no gold grade |
| Mining inside the reserve jumped in 2025 | [[D]] | +{{anp_tam_nr_addition_2025}} ha (MapBiomas); MAAP #241 agrees | 521 ha were already inside by 2016 (Asner & Tupayachi) |
| Buffer-zone enforcement shielded the reserve | **not claimed** | Reserve-edge step {{rd_reserve_did:+.1f}} (p = {{rd_reserve_did_p:.2f}}) | A null can't tell "no change" from "small change" |
| The fall-and-return cycle happened twice (2012 and 2019) | **not claimed** | Asner & Tupayachi (2017) report the 2012 dip | Our data show no 2012–13 dip in La Pampa ({{tl_dip_2012_13:+.0%}}) |
| The official gold series fell 88% | **withdrawn** | — | The series dropped its artisanal estimate in 2020; producer-declared gold rose |
| Corridor miners mine informally and don't declare | plausible, **not claimed** | Formalization rates, Bolivia exports, unknown-origin exports | No trace of where Madre de Dios gold is declared |
| The region mined less | **rejected** | — | First-time mining rose {{v2_new_total_2016_18}} → {{v2_new_total_2022_25}} ha/yr |
| Brazil: operations reduced mining | **not claimed** | Staggered DiD {{brv2_did2s_treat:+.2f}} (wrong sign, two-sided p = {{brv2_did2s_treat_p:.2f}}) | National reforms in 2023; low power |
| Next operation: local fall while present, new mining across the nearest legal boundary, a return within ~3 years | [[P]] | Peru pattern | One operation, one region; risk model barely beats "mining nearby" |

**How to read p:** below 0.05 = unlikely to be chance. With {{model_m1_n}} zones the smallest possible randomization p is {{model_m1_ri_p:.2f}}, so "rank 1" is as strong as that test gets. Every other test is in its chapter.

**Why it matters:** one labelled, conditional causal claim, with its failed tests shown, beats a vague strong one.

:::more What the referee found, and what we changed
| Problem | Fix | Effect on the result |
|---|---|---|
| Fake-place test kept Tambopata as a control, so every placebo looked positive | Tambopata removed from each placebo's pool; Amazon-only pool added | Still rank 1 in hectares; **rank {{model_m4_rank:.0f}} of {{model_m4_n:.0f}} scaled** |
| Causal number measured net change, called "new mining" | Claim reworded to net mining; first-time change reported | First-time mining fell less ({{t5_m2_2016_18}} → {{t5_m2_2019_21}} ha/yr) |
| Cell comparison included the corridor (displacement target); baseline mislabelled; few treated clusters | Clean comparison cells; 2014–25 panel; pooled 2014–18 reference; wild cluster bootstrap | La Pampa {{st_main_lapampasector_during:+.2f}} (was {{st_contam_lapampasector_during:+.2f}}); pre-trends still fail |
| One twin (Munduruku) had a 2021 operation; t-tests on 3 values | Two twins; no p-values | Tambopata still below both |
| Brazil code skipped Kayapó's 2024 operation; Munduruku dated by an unverified 2021 snippet | First *verified* operation inside 2021–25 (Munduruku Aug 2023) | Estimate {{brv2_did2s_treat:+.2f}}, still not significant |
| Road placebo windows overlapped the event | Non-overlapping start years only | Rank 1 of {{t1_road_shift_n_clean:.0f}} (p = {{t1_road_shift_ri_p_clean:.2f}}) |
| Legality used today's concessions for past years | Concession must be filed by the mining year | Illegal share {{leg_tc_illegal_share_2016_18:.0%}} → {{leg_tc_illegal_share_2022_25:.0%}} (unchanged picture) |
| Risk map tested on the same cells, no benchmark | Spatial hold-out + "mining nearby" benchmark | AUC {{risk_auc_spatial_holdout:.2f}} vs {{risk_auc_benchmark:.2f}}: adds little |
| Untraceable numbers (Sentinel-2, producer gold) | Now computed in code | See [Timing](#timing) and [Declared gold](#declared-gold) |

**Full review:** `docs/overnight/notes/critical_review_v2.md`.
:::

@part Team corner

## To do | What's blocked on you

**Only a human can do these:**

1. **Agree on the claim wording,** especially the one conditional causal sentence ([Six attempts](#six-attempts)). It's a team call.
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
| Placebos: the explainer figure | `code/placebo_explainer.py` | `fig_placebo_explainer.png` |
| Attempt 4: spatial RD at the road and the reserve edge | `code/v2_rdd.py` | `fig_v2_rdd.png`, `table_rdd.csv` |
| Attempt 5: matching (PSM, Mahalanobis, CEM, entropy balancing, IPW) | `code/control_psm.py` | `fig_psm.png`, `psm_results.csv`, `table_psm_balance.csv` |
| Attempt 6: synthetic DiD | `code/peru_sdid.py` | `fig_sdid.png`, `peru_sdid.csv` |
| Context: COVID and money as controls | `code/peru_context_models.py` | `fig_peru_context_models.png`, `peru_context_models.csv` |
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
