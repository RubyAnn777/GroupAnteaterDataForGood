<!--
Source of docs/overnight/EXPLAINER.html (the team walkthrough). Build: `uv run python docs/overnight/build_report.py`.
Placeholders {{id}} or {{id:fmt}} come from output/numbers.csv (default ",.0f"; unknown ids fail the build).
Claim tags: [[D]] description, [[P]] prediction, [[C]] causal. Figures ![caption](output/x.png) are embedded.
Sections split on "## ". The first "> " line is the banner. {{BRIEF_BODY}} embeds the 2-page brief draft.
Structure follows the team meeting of 12 Oct 2026: background -> descriptives per zone -> qualitative overlays ->
three causal attempts -> Brazil -> recommendations.
-->

# Mercurio stopped La Pampa for about two years. Mining crossed the road, and the region kept growing.

> A guided walk through the analysis, in plain words. Order: background, what happened in each zone, what else was going on, three attempts at a causal answer, Brazil, what FZS can do. Section 21 holds the report draft. Every number comes from `output/numbers.csv`. Draft for the team.

## 1. The bottom line

**Operation Mercurio worked where it landed, for about two years. Then miners came back, and many had simply crossed the road.**

- **During (2019–21):** net new mining in the Tambopata buffer zone fell from {{mean_add_tambopata_2016_18}} to {{mean_add_tambopata_2019_21}} ha per year. [[D]]
- **But not at once:** forest clearing on La Pampa's mining land went on through 2019 and collapsed in 2020–21. [[D]]
- **Across the road:** first-time mining in the legal corridor directly north of the highway rose from {{v2_new_corridoracrosstheroa_2016_18}} to {{v2_new_corridoracrosstheroa_2019_21}} ha per year; the corridor's share of all new mining rose from {{v2_corridor_share_2016_18:.0f}}% to {{v2_corridor_share_2022_25:.0f}}%. [[D]]
- **After (2022–25):** La Pampa came back to {{mean_add_tambopata_2022_25}} ha per year, much of it on old pits. The gold wasn't gone: only {{gold_broad_lapampasector_depleted_2018:.0%}} of its gold-bearing land had been mined by 2018. [[D]]
- **Region:** first-time mining in Madre de Dios rose from {{v2_new_total_2016_18}} to {{v2_new_total_2022_25}} ha per year. Declared gold says little: the official series dropped its artisanal estimate in 2020. [[D]]
- **Brazil:** the same pixel method shows falls from 2022–24, but not after each territory's own operation; the staggered estimate has the wrong sign and is not significant. [[D]]

**Can we say Mercurio *caused* the fall?** Only cautiously, for **net** new mining in 2019–21. In hectares, Tambopata's fall is the largest of 15 zones (randomization p = {{model_m1_ri_p:.2f}}, the best this test allows) and it sits below two rule-based twins. But relative to its size the fall is ordinary, per 1-km cell the pre-trends fail, and first-time mining fell less and a year later. We label it a **conditional causal claim** with these caveats. [[C]]

**Why it matters:** enforcement works **while it lasts** and **where it lands**. Miners answer **across the nearest legal boundary** and **in old pits**. The legal corridor absorbs them: taxes there are near zero and tracing is weak.

## 2. How to read this page

**The page follows our meeting's structure:**

- **3–4 Background:** what is illegal, who enforces, the zones and what each costs a miner
- **5–11 What happened, zone by zone:** where new mining went, crossing the road, old pits, timing, gold left, inside the reserve, declared gold
- **12 What else changed:** COVID, politics, gangs, gold price, enforcement money
- **13–17 Three causal attempts** and every statistical test at a glance
- **18 Brazil** (appendix-level)
- **19 What FZS can do**
- Then: claims (20), **report draft (21)**, files (22), what's on you (23), appendix (24)

**Plain-word glossary**

| Term | Meaning here |
|---|---|
| **La Pampa sector** | Tambopata buffer zone between 70.15° and 69.80° W, south of the highway. The operation's target. Our boundary; no official one exists. |
| **Legal mining corridor** | The area where small-scale mining may be permitted (D.L. 1100, 2012). North of the highway. |
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

**Claim labels.** [[D]] = what happened; [[P]] = what we expect; [[C]] = what caused it.

## 3. Background: what is illegal, who enforces, and what each zone costs a miner

**Bottom line:** in Peru, *where* you mine decides whether it's a crime. La Pampa is illegal by location; the corridor across the road is not. Moving 2 km north turns a crime into an administrative problem.

**What is illegal (D.L. 1105, 2012):**
- **Illegal:** mining in a prohibited zone, or with banned equipment. A crime.
- **Informal:** the same failings, but inside a permitted zone, by someone registered for formalization (REINFO). Not a crime.
- **The corridor (D.L. 1100, 2012):** about 4,983 km² where small-scale mining can be permitted. Outside it, no concessions are granted. La Pampa covers about 1,241 km² (MINAM 2016).
- **Formalization barely happens:** in 2021, 9,592 Madre de Dios miners were registered in REINFO, but only 145 were fully formalized (Plan Restauración 2021). Congress has extended REINFO again and again, now to 31 December 2026.

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

**Taxes are low anyway:**
- **Royalty:** 0% for small producers (Ley 28258).
- **VAT:** raw gold exempt; 1.5% withheld on sale.
- **Fuel:** tax-exempt in the Amazon; 72% of that benefit went to illegal mining (IPE).

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

**FZS's role:** FZS supports SERNANP's law-enforcement operations, ranger control posts and patrols in the Tambopata–Bahuaja-Sonene landscape.

**Why it matters:** the operation raised the cost of mining *in one place*. The legal corridor next door kept the cost low. That alone predicts displacement across the road.

**Sources:** `docs/overnight/notes/qualitative_background.md` (every item with a link and a quote).

## 4. The places: four zones and the road

**Bottom line:** we cut one satellite map into zones that match the law and the meeting's drawing: La Pampa, the corridor across the road, the extra buffer zone, the reserve, plus communities and the rest. [[D]]

![Zone map around La Pampa](output/fig_v2_zone_map.png)

**How to read it:** coloured areas are zones; black pixels were mapped as mining at least once since 1985. The thick line is the Interoceanic Highway. Dotted lines mark La Pampa's longitudes.

**What we did:**
- **Data:** MapBiomas Peru Collection 4 maps for every year 1985–2025 (30 m pixels), the same product as the course tables.
- **Check:** the raster gives the Tambopata buffer zone {{v2_check_tambopatabufferzone_2025}} ha in 2025 (table: 20,730) and the reserve {{v2_check_tambopatareserve_2025}} ha (platform: 777).
- **Boundary choice:** a narrower and a wider La Pampa window give the same result (fall of {{t4_lp_narrow_change:.0%}} and {{t4_lp_wide_change:.0%}}); we keep the middle one.
- **Boundaries change:** the current Tambopata buffer zone dates from {{t6_bz_approved_tambopata:.0f}}, Amarakaeri's from {{t6_bz_approved_amarakaeri:.0f}}; the corridor from 2012. We apply today's boundaries to every year, as MapBiomas does.

**What each zone offers a miner** (study area around La Pampa):

| Zone | Status | km to highway | km to river | Gold-bearing land | Mined by 2018 |
|---|---|---:|---:|---:|---:|
| La Pampa sector | illegal | {{zp_lapampasector_km_to_highway:.1f}} | {{zp_lapampasector_km_to_river:.1f}} | {{zp_lapampasector_gold_bearing_share:.0%}} | {{gold_broad_lapampasector_depleted_2018:.0%}} |
| Corridor across the road | legal if titled | {{zp_corridoracrossth_km_to_highway:.1f}} | {{zp_corridoracrossth_km_to_river:.1f}} | {{zp_corridoracrossth_gold_bearing_share:.0%}} | {{gold_broad_corridoracrossther_depleted_2018:.0%}} |
| Rest of mining corridor | legal if titled | {{zp_restofminingcorr_km_to_highway:.1f}} | {{zp_restofminingcorr_km_to_river:.1f}} | {{zp_restofminingcorr_gold_bearing_share:.0%}} | {{gold_broad_restofminingcorrid_depleted_2018:.0%}} |
| Reserves and parks | illegal | {{zp_reservesandparks_km_to_highway:.1f}} | {{zp_reservesandparks_km_to_river:.1f}} | {{zp_reservesandparks_gold_bearing_share:.0%}} | — |

**Why it matters:** the corridor across the road has the same gold and the same road access as La Pampa, without the enforcement risk. The reserve has gold too, but no road. That ranking matches where the mining went.

**Code:** `code/raster_zones.py`, `code/v2_extra.py` (zone profile).

## 5. Where did the new mining go? Into the legal corridor

**Bottom line:** After 2019, land mined for the first time shifted from La Pampa to the legal corridor. The corridor's share rose from {{v2_corridor_share_2016_18:.0f}}% to {{v2_corridor_share_2022_25:.0f}}%. [[D]]

![Land mined for the first time each year, by zone](output/fig_v2_stream.png)

**How to read it:**
- **Top:** hectares mined for the first time each year, stacked by zone; the label is the total.
- **Bottom:** the same as shares of each year's total.

**What it shows:**
- **La Pampa sector:** {{v2_new_lapampasector_2016_18}} → {{v2_new_lapampasector_2019_21}} → {{v2_new_lapampasector_2022_25}} ha/yr. [[D]]
- **Corridor across the road:** {{v2_new_corridoracrosstheroa_2016_18}} → {{v2_new_corridoracrosstheroa_2019_21}} → {{v2_new_corridoracrosstheroa_2022_25}} ha/yr. [[D]]
- **All Madre de Dios:** {{v2_new_total_2016_18}} → {{v2_new_total_2019_21}} → {{v2_new_total_2022_25}} ha/yr. [[D]]
- **Presumed illegal share** (outside the corridor and outside communities): {{t7_presumed_illegal_share_2016_18:.0%}} → {{t7_presumed_illegal_share_2019_21:.0%}} → {{t7_presumed_illegal_share_2022_25:.0%}}. [[D]]
- MAAP #208 independently finds 74% of 2021–24 mining deforestation inside the corridor. We find {{v2_corridor_share_2022_25:.0f}}% for 2022–25.

![Share of newly mined land inside the legal corridor](output/fig_v2_corridor_share.png)

**Legality levels (MAAP #235, the same grades Amazon Mining Watch uses):** we crossed every pixel of first-time mining with the published legality layer (Low = active concession; Medium = concession not verified as active; High = outside any concession; Very high = strict protected area).

![Legality of new mining in Madre de Dios over time](output/fig_v2_legality.png)

- **Presumed illegal (High + Very high):** {{leg_illegal_share_2016_18:.0%}} → {{leg_illegal_share_2019_21:.0%}} → {{leg_illegal_share_2022_25:.0%}} of first-time mining. [[D]]
- **The grey zone grew:** concessions not verified as active took {{leg_medium_share_2016_18:.0%}} → {{leg_medium_share_2019_21:.0%}} → {{leg_medium_share_2022_25:.0%}}. [[D]]
- **Inside the legal corridor**, {{leg_corridor_highish_share:.0%}} of all first-time mining since 1986 sits on land without a verified active concession. [[D]]
- **Time-consistent check:** counting a concession only if it was filed by the mining year gives {{leg_tc_illegal_share_2016_18:.0%}} → {{leg_tc_illegal_share_2019_21:.0%}} → {{leg_tc_illegal_share_2022_25:.0%}} presumed illegal and {{leg_tc_medium_share_2016_18:.0%}} → {{leg_tc_medium_share_2022_25:.0%}} grey zone: the same picture.

**Not all corridor growth is displaced La Pampa mining:** the rest of the corridor gained far more new mining than La Pampa lost ({{v2_new_restofminingcorridor_2016_18}} → {{v2_new_restofminingcorridor_2022_25}} ha/yr), so new entrants and the gold price drive most of it. The 2023 spike appears region-wide and may partly be a map artefact.

**Why it matters:** Mercurio moved new mining from illegal land to legal land. For the reserve that is a win. For the region it is not: total new mining kept growing, and corridor mining still uses mercury.

**Can't show:** that the *same* people moved. New arrivals and the gold price fit the same picture.

**Second satellite product agrees (Amazon Mining Watch, same zones):** in the La Pampa longitudes, the share of new mining north of the road was {{amw_v2_north_share_2019:.0%}} in 2019 and {{amw_v2_north_share_2021:.0%}} in 2021. [[D]]

![Robustness: Amazon Mining Watch on the same zones](output/fig_v2_amw_robustness.png)

**Why AMW and MapBiomas disagree after 2021 in the corridor:** AMW flags a 480 m square only once; MapBiomas counts every new 30 m pixel. {{pc_restofminingcorr_in_earlier_patch_2022_25:.0%}} of MapBiomas's first-time mining in the corridor in 2022–25 lies inside AMW squares flagged earlier, so AMW can't count it again. The products agree on the move across the road; they differ on infill. Details: `review.md`, response section.

**Statistical test:** per 1-km cell, the corridor across the road gained {{st_main_corridoracross_during:+.2f}} ha per cell-year in 2019–21 relative to clean comparison cells (p = {{st_main_corridoracross_during_p:.2f}}). The comparison now excludes the corridor and communities, so it isn't itself a displacement target (section 14).

**Code:** `code/raster_layers.py`, `code/v2_extra.py` (AMW).

## 6. Crossing the road, then going deeper

**Bottom line:** Right after Mercurio, the tallest bars sit 0–2 km north of the highway, directly across from La Pampa. The north side's share of new mining went from {{t1_road_north_share_2016_18:.0%}} (2016–18) to {{t1_road_north_share_2019_21:.0%}} (2019–21). [[D]]

![New mining by distance band south and north of the highway](output/fig_v2_road_bands.png)

**How to read it:** each bar is a 1-km strip parallel to the highway, inside the La Pampa longitudes. Orange = south (buffer zone side), blue = north (corridor side). Height = land mined for the first time per year.

**Is the jump unusual? Fake start dates:**

![Fake start dates for the move across the road](output/fig_v2_road_placebo.png)

**What it shows:**
- The 2019 move north (+{{t1_road_shift_2019:.2f}} share points, within 30 km) ranks {{t1_road_shift_rank:.0f}} of {{t1_road_shift_n:.0f}} start years (p = {{t1_road_shift_ri_p:.2f}}); only 2020, whose window overlaps the event, is higher. Counting only non-overlapping windows: rank {{t1_road_shift_rank_clean:.0f}} of {{t1_road_shift_n_clean:.0f}} (p = {{t1_road_shift_ri_p_clean:.2f}}, the smallest possible). [[D]]
- **The road has been crossed before.** In 2008–10 most new mining was north of the road (the Guacamayo boom; share {{t1_road_north_share_2008:.0%}} in 2008). It moved south to La Pampa by 2015 ({{t1_road_north_share_2015:.0%}}), then back north after Mercurio ({{t1_road_north_share_2021:.0%}} in 2021). [[D]]
- **Boundary choice doesn't matter:** a narrower or wider La Pampa window changes the La Pampa fall from {{t4_lp_narrow_change:.0%}} to {{t4_lp_wide_change:.0%}}.

**How deep do they go?** We split the north side into 0–10, 10–20 and 20–30 km bands (meeting idea).

![Depth of new mining north of the highway](output/fig_v2_depth.png)

- **Right after Mercurio, new mining hugged the road:** mean depth fell from {{t9_depth_2016:.0f}} km (2016) to {{t9_depth_2020:.0f}} km (2020); break after 2019 {{t9_depth_post2019:+.1f}} km net of trend (p = {{t9_depth_post2019_p:.3f}}). [[D]]
- **Then it pushed deeper:** {{t9_depth_2025:.0f}} km by 2025. [[D]]
- **Per 1-km cell, 10–30 km north gained most after 2022:** +{{st_grad_b_N10_20_after:.1f}} ha per cell-year (p = {{st_grad_b_N10_20_after_p:.3f}}) relative to cells 10–30 km south. [[D]]

**Why it matters:** miners follow enforcement and gold across a two-lane road. Any operation south of the highway should expect a response north of it.

**Code:** `code/raster_zones.py` (road bands), `code/v2_tests.py` (T1, T4).

## 7. Returns to old pits: why net numbers mislead

**Bottom line:** In 2023, most new mining in La Pampa happened on **old pits**, not on new land. The net table can't see this. [[D]]

![New mining split into new land and returns to old pits, by zone and period](output/fig_v2_sankey.png)

**How to read it:** left = where new mining came from (new land, or old pits mined again). Right = the zone it appeared in. Width = hectares per year; same scale in all three panels.

**What it shows:**
- **La Pampa sector, returns to old pits:** {{v2_lapampa_remined_2016_18}} → {{v2_lapampa_remined_2019_21}} → {{v2_lapampa_remined_2022_25}} ha/yr. [[D]]
- **Share of all new mining on old pits:** {{v2_remined_share_2016_18:.0%}} → {{v2_remined_share_2019_21:.0%}} → {{v2_remined_share_2022_25:.0%}}. [[D]]
- MAAP #193 independently reports miners back on degraded land in La Pampa in 2023.

**The same map for returns to old pits** (Ruby's request):

![Returns to old pits each year, by zone](output/fig_v2_stream_remined.png)

- **The corridor holds most returns too:** {{rm_corridor_share_2016_18:.0%}} → {{rm_corridor_share_2019_21:.0%}} → {{rm_corridor_share_2022_25:.0%}} of all returns to old pits. [[D]]
- **La Pampa's share:** {{rm_lapampa_share_2016_18:.0%}} → {{rm_lapampa_share_2019_21:.0%}} → {{rm_lapampa_share_2022_25:.0%}}. [[D]]

**Net vs gross, Tambopata buffer zone (ha/yr):**

| | 2016–18 | 2019–21 | 2022–25 |
|---|---:|---:|---:|
| Net addition (course table) | {{t5_m0_2016_18}} | {{t5_m0_2019_21}} | {{t5_m0_2022_25}} |
| First-time mining | {{t5_m2_2016_18}} | {{t5_m2_2019_21}} | {{t5_m2_2022_25}} |
| Return to old pits | {{t5_m3_2016_18}} | {{t5_m3_2019_21}} | {{t5_m3_2022_25}} |

**Caveat:** the old-pit count includes year-to-year map flicker (about 300 ha/yr even before 2019). Trust the 2023 jump, not small changes.

**Why it matters:** an operation can stop clearing while miners quietly return to old pits. FZS should monitor old mining sites, not only forest edges.

## 8. Timing by quarter: clearing in La Pampa went on through 2019

**Bottom line:** Forest clearing on La Pampa's mining land did **not** stop in February 2019. It was higher in 2019 than in 2018 and collapsed only in 2020–21. [[D]]

![Quarterly forest-loss alerts on mining land, by zone](output/fig_v2_glad_quarterly.png)

**What we did:** University of Maryland GLAD forest-loss alerts (Landsat, every pixel dated to the day), counted per quarter on land that MapBiomas maps as mining.

**What it shows:**
- **La Pampa sector, alerts on mining land:** {{glad_mining_lapampasector_2017}} ha (2017), {{glad_mining_lapampasector_2018}} (2018), **{{glad_mining_lapampasector_2019}} (2019)**, {{glad_mining_lapampasector_2020}} (2020), {{glad_mining_lapampasector_2021}} (2021). [[D]]
- **Corridor across the road:** {{glad_mining_corridoracrossther_2018}} ha (2018) → {{glad_mining_corridoracrossther_2019}} (2019) → {{glad_mining_corridoracrossther_2020}} (2020). [[D]]
- **Sentinel-2 alerts** (every 5 days) in western La Pampa: {{s2_lp_west_2019_mar_sep_ha}} ha in March–September 2019 ({{s2_lp_west_2019_aug_ha}} ha in August alone), vs {{s2_lp_west_2020_mar_sep_ha}} ha in the same months of 2020. So 2019 clearing was real, not just cloud delay.

**Why it matters:** this corrects our earlier wording. The brief must say clearing fell **from 2020**, not "immediately". It matches Dethier et al. (2023): activity spiked in La Pampa's northwest after the operation.

**Caveats:** clouds bunch alerts in the dry season; compare the same quarter across years. The data version changes in 2021. Alerts need standing forest, so returns to old pits never show.

**Code:** `code/glad_alerts.py`.

## 9. Was the gold gone? No.

**Bottom line:** By 2018, La Pampa had mined only {{gold_broad_lapampasector_depleted_2018:.0%}} of its gold-bearing land. About {{gold_broad_lapampasector_left_2018_ha:,.0f}} ha were left. "Miners left because the gold ran out" is unlikely. [[D]]

**What we did:** no one publishes gold left in the ground. Gold here is alluvial, so we used the national geology map (INGEMMET, 1:100,000): river deposits plus the gold-bearing terraces of the Madre de Dios Formation.

**Does the proxy work?** {{gold_broad_validation:.0%}} of all land ever mined lies on these units, which cover {{gold_broad_land_share_mdd:.0%}} of Madre de Dios ({{gold_broad_lift:.1f}}× more mining than chance). The strict river-deposit units cover {{gold_strict_land_share_mdd:.0%}} and hold {{gold_strict_validation:.0%}} ({{gold_strict_lift:.1f}}×). La Pampa was {{gold_strict_lapampasector_depleted_2018:.0%}} depleted by 2018 under the strict definition too.

| Gold-bearing land already mined | by 2018 | by 2025 |
|---|---:|---:|
| La Pampa sector | {{gold_broad_lapampasector_depleted_2018:.0%}} | {{gold_broad_lapampasector_depleted_2025:.0%}} |
| Corridor across the road | {{gold_broad_corridoracrossther_depleted_2018:.0%}} | {{gold_broad_corridoracrossther_depleted_2025:.0%}} |
| Rest of mining corridor | {{gold_broad_restofminingcorrid_depleted_2018:.0%}} | {{gold_broad_restofminingcorrid_depleted_2025:.0%}} |
| Kotsimba | {{gold_broad_kotsimbanativecomm_depleted_2018:.0%}} | {{gold_broad_kotsimbanativecomm_depleted_2025:.0%}} |

**Why it matters:** enforcement, not exhaustion, is the better explanation for the move.

**Limits:** the map is coarse and says nothing about gold grade; old pits can be mined again.

**Code:** `code/raster_gold.py`.

## 10. Inside the reserve: miners arrived in 2025

**Question:** The course data only covers buffer zones. What happened *inside* Tambopata National Reserve?

**What we did:** We downloaded the MapBiomas protected-area file (new data) and checked it against the MapBiomas website (777 ha, a match).

![Inside the reserves vs their buffer zones](output/fig_peru_inside_reserves.png)

**How to read it:** Mining area inside each reserve vs its buffer zone.

**What it shows:**
- Mining inside the reserve reached {{anp_level_tam_nr_2025:,.0f}} ha in 2025, of which {{anp_tam_nr_addition_2025}} ha was new that year. [[D]]
- The 2017 jump (+{{anp_tam_nr_addition_2017}} ha) looks partly like a map reclassification, not real mining. [[D]]
- Two other sources agree on the direction. MAAP #241 reports ~500 ha of new mining inside the reserve (late 2025 to Feb 2026), and Amazon Mining Watch shows {{sp_amw_tambopata_nr_new_ha_2025}} ha in 2025 (provisional). [[D]]

**Why it matters:** This is FZS's core area. The 2025 incursion came after navy posts on the Malinowski River were withdrawn (MAAP #241). It's the most actionable finding.

**Code:** `code/peru_anp.py`.

## 11. Declared gold: the official drop is a change in the series, not in output

**Bottom line:** the official Madre de Dios gold series fell {{pe_prod_fall_2018_2025_pct:.0f}}% from 2018 to 2025, but that is mostly a definition change. Until 2019 it included an *estimate* of artisanal gold; from 2020 it counts only what producers declare. [[D]]

**What we found (correction):**
- **The series changed:** the Ministry of Energy and Mines' yearly files carry "PRODUCTORES ARTESANALES — cifras estimadas" for Madre de Dios until 2019 (about 15.7 t in 2016, 6.0 t in 2019). In 2016, that estimate plus declared output equals the central bank's figure exactly. From 2020 the estimate is gone.
- **Declared output by producers rose,** from {{gold_minem_declared_2018_kg:,.0f}} kg (2018) to {{gold_minem_declared_2025_kg:,.0f}} kg (2025). The estimate was {{gold_minem_estimate_2019_kg:,.0f}} kg in 2019 and is absent from 2020.
- **An earlier break in 2015:** until 2014, artisanal producers' own declarations were in the series ({{gold_minem_declared_2014_kg:,.0f}} kg in 2014); from 2015 producers declared only {{gold_minem_declared_2015_kg:,.0f}} kg and the ministry added an estimate.
- **So our earlier "collapse" and its break test measured the definition change.** We withdraw them.

![The official gold series changed definition twice](output/fig_peru_gold_definition.png)

**Does the "mining in the corridor, declaring nothing" idea still fit?** Yes, in a weaker form:
- **For:** new mining moved into the grey zone: {{leg_medium_share_2022_25:.0%}} of first-time mining in 2022–25 sat in concessions not verified as active (section 5); producers declare about 1 t a year while first-time mining covers over {{v2_new_total_2022_25}} ha a year; only 145 of 9,592 registered miners were fully formal (2021); the state presumes Madre de Dios gold is smuggled to Bolivia, whose gold exports jumped from 1.7 t (2012) to 35.7 t (2014); nationally at least 80 of ~180 t exported in 2024 had unknown origin.
- **Against:** gold may be declared in other regions; mapped area includes re-mined pits; gold yield per hectare is unknown.
- **Label:** plausible mechanism, not a finding.

**Why it matters:** official production says almost nothing about mining here, and its 2020 break is a trap. Don't cite "−88%".

**Code:** `code/peru_gold_minem.py` (checked against the central bank for 2012 and 2019), `code/peru_production.py`. **Source of the correction:** `docs/overnight/notes/legality_data.md`, section on MINEM production.

## 12. What else changed: COVID, politics, gangs, gold price, money

**Bottom line:** other events line up with the mining curve. Enforcement money peaked in 2019 and faded; COVID pulled forces away in 2020; a new government arrived in 2021. The 2012–13 wave, under a new government too, left no mark on La Pampa. [[D]]

![Timeline: enforcement, politics, laws and context vs first-time mining](output/fig_v2_timeline.png)

**How to read it:** top = events (orange enforcement, purple presidents, blue laws, grey context). Bottom = first-time mining in La Pampa (bars) and all Madre de Dios divided by 5 (line).

**What it shows:**
- **One dip, not two:** La Pampa first-time mining changed by {{tl_dip_2012_13:+.0%}} in 2012–13 vs 2010–11, and by {{tl_dip_2020_21:+.0%}} in 2020–21 vs 2017–18. [[D]]
- **The political-cycle idea:** both enforcement waves started 7–11 months after a new president (Humala 2011 → decrees 2012; Vizcarra 2018 → Mercurio 2019), and both faded within about two years. That's a pattern, not evidence; we found no study of Peruvian election effects (Brazilian studies find more deforestation in election years).
- **Earlier wave in the course table:** Tambopata's gap in 2012–13 was +{{t3_wave_m1_2012_13}} ha/yr, rank {{t3_wave_rank:.0f}} of {{t3_wave_n:.0f}}: no Tambopata-specific dip. [[D]]

![Anti-illegal-mining spending in Madre de Dios vs first-time mined land](output/fig_v2_enforcement_spending.png)

- **Money:** PP 0128 spending booked in Madre de Dios was {{t8_pp0128_mdd_2018:,.0f}} soles (2018), {{t8_pp0128_mdd_2019:,.0f}} (2019), {{t8_pp0128_mdd_2021:,.0f}} (2021), {{t8_pp0128_mdd_2025:,.0f}} (2025). A lower bound: national units book under Lima. [[D]]
- **COVID:** forces left La Pampa in spring 2020 for the pandemic; budgets fell sharply in 2020–21 (Mongabay 2023). That fits the 2022–25 rebound.
- **The 2017 spike:** 2017 was the record year for mining deforestation (Caballero Espejo et al. 2018). The gold price was flat (about $1,250/oz, 2016–18), so it doesn't explain it. Gangs ("Guardianes de la Trocha") ran extortion in La Pampa, but no source dates a 2017 takeover; part of the jump may be map reclassification. Mercury controls after Peru ratified the Minamata Convention (2016) made mercury a smuggling business; plausible, undocumented.
- **Gold price:** rose {{gold_price_ratio_2025_2018:.1f}}-fold from 2018 to 2025; it pushes everywhere at once, which the year effects in section 14 remove.

**Why it matters:** enforcement in Madre de Dios comes in waves tied to governments and budgets. FZS should plan for the gap after each wave.

**Code:** `code/v2_extra.py` (timeline), `code/v2_tests.py` (spending, 2012 wave). **Sources:** `docs/overnight/notes/qualitative_background.md`, `enforcement_intensity.md`.

## 13. Three attempts at a causal answer: one partly works, one half-works, one fails

**Bottom line:** we tried three ways to build "what would have happened without Mercurio". None is clean. Two point the same way for **net** mining in 2019–21; their tests are weaker than we first reported (a referee found errors, now fixed: section 17).

| Attempt | Comparison | Pre-trends | Result |
|---|---|---|---|
| **1 Difference-in-differences** | Tambopata vs 14 other Peruvian buffer zones; per 1-km cell vs clean comparison cells | Zone level: averaged fake dates pass. Cell level: fail for La Pampa (p = {{st_event_lp_pretrend_p:.3f}}) | Large fall in hectares (rank 1 of 15, p = {{model_m1_ri_p:.2f}}); **not unusual relative to La Pampa's size** (rank {{model_m4_rank:.0f}} of {{model_m4_n:.0f}}) |
| **2 Synthetic control** | weighted mix of Peruvian zones | can't be met: La Pampa is too big | Fails for levels |
| **3 Rule-based twins** | two existing areas abroad (Amanã, Tapajós) | not parallel: Tambopata grew faster before 2019 | Tambopata below both in 2019–21 (descriptive, 3 years each) |

**Why it matters:** the supervisor's bar is "anywhere close to causal". We get close for net mining in 2019–21, with every weakness stated. That's the honest score.

## 14. Attempt 1: difference-in-differences, at three levels

**Bottom line:** in hectares, Tambopata's 2019–21 fall in **net** mining is the largest of 15 zones and survives controls for the gold price, trends and size. But relative to its own size it is ordinary, and per 1-km cell the pre-trends fail. [[D]]

**Level 1: the course's 2×2 (Tambopata vs the extra buffer zone, Amarakaeri)**

| ha of net new mining per year | Before 2016–18 | During 2019–21 | Change |
|---|---:|---:|---:|
| Tambopata (targeted) | {{mean_add_tambopata_2016_18}} | {{mean_add_tambopata_2019_21}} | {{did_main_tambopata_change}} |
| Amarakaeri (extra buffer zone) | {{mean_add_amarakaeri_2016_18}} | {{mean_add_amarakaeri_2019_21}} | +{{did_main_amarakaeri_change}} |
| **Gap change** | | | **{{did_main}}** |

- **Amarakaeri was itself treated** (Mercurio II, interdiction in December 2019), so it is "less treated", not a control.
- **Baseline 2014–18 instead of 2016–18:** gap {{did_main_base_2014_18}} ha/yr.
- **The card's own check, target + neighbours:** the three buffer zones together added {{mean_add_three_bz_sum_2016_18}} → {{mean_add_three_bz_sum_2019_21}} → {{mean_add_three_bz_sum_2022_25}} ha/yr: the combined total fell during and rose above its old level after. [[D]]
- **Net is not new:** of Tambopata's net fall, almost half is old mining going out of use; first-time mining fell from {{t5_m2_2016_18}} to {{t5_m2_2019_21}} ha/yr (section 7).

**Level 2: against all 14 other Peruvian buffer zones with mining**

- **Model:** net new mining = zone effect + year effect + Tambopata × period. Year effects remove the gold price, COVID and national policy (shared shocks).
- **Fake places (fixed after the review):** each other zone gets the "operation" in turn, *with Tambopata removed from its comparison pool*. Placebo effects now range {{model_m1_placebo_min:,.0f}} to +{{model_m1_placebo_max:,.0f}} ha/yr; Tambopata ({{model_m1_during}}) ranks 1 of {{model_m1_n}} (randomization p = {{model_m1_ri_p:.2f}}, the smallest possible with {{model_m1_n}} zones). Among Amazon-department zones only: rank {{model_m1_rank_amazon:.0f}} of {{model_m1_n_amazon:.0f}}.
- **Scaled to each zone's size (M4), the fall is ordinary:** rank {{model_m4_rank:.0f}} of {{model_m4_n:.0f}} (p = {{model_m4_ri_p:.2f}}). Tambopata falls most in hectares because it is the biggest.
- **Dropping the largest comparison zone:** 2019–21 gap {{robust_es_poolB_drop_largest_2019_2021}} ha/yr.

![Event study: Tambopata minus comparison zones, relative to 2018](output/fig_peru_event_study.png)

| Model | Adds | During 2019–21 | After 2022–25 | Fake 2016 | Rank |
|---|---|---:|---:|---:|---:|
| **M1** | Zone + year effects | {{model_m1_during}} | {{model_m1_after}} | {{model_m1_placebo}} | {{model_m1_rank}} of {{model_m1_n}} |
| **M2** | + bigger zones react more to gold price | {{model_m2_during}} | {{model_m2_after}} | {{model_m2_placebo}} | {{model_m2_rank}} of {{model_m2_n}} |
| **M3** | + each zone's own trend | {{model_m3_during}} | {{model_m3_after}} | {{model_m3_placebo}} | {{model_m3_rank}} of {{model_m3_n}} |
| **M4** | Scaled to each zone's size | {{model_m4_during:.2f}} | {{model_m4_after:.2f}} | {{model_m4_placebo:.2f}} | {{model_m4_rank}} of {{model_m4_n}} |

![Model ladder: real fall vs fake-date fall](output/fig_peru_models.png)

- **Fake dates:** M1 and M2 placebos have the opposite sign; M3's placebo ({{model_m3_placebo}}) has the same sign as the real effect, so not every model passes cleanly.

**Level 3: per 1-km cell, with standard errors**

- **Panel:** {{st_n_cells}} cells, 2014–2025 (baseline 2014–18); cell and year fixed effects; errors clustered by 10 × 10 km blocks.
- **Clean comparison (after the review):** cells outside every named zone, the legal corridor and native communities ({{st_n_ref_cells_clean:.0f}} cells). The earlier version used the rest of the corridor, where displaced mining went, which exaggerated La Pampa's fall.
- **Few treated clusters:** La Pampa covers {{st_clusters_lp:.0f}} of the {{st_n_clusters:.0f}} clusters, so we add a wild cluster bootstrap.

![Per-cell change by zone, with 95% confidence intervals](output/fig_v2_stats_zones.png)

| Per 1-km cell, ha/yr vs clean comparison | 2019–21 | p (clustered) | 2022–25 | p |
|---|---:|---:|---:|---:|
| La Pampa sector | {{st_main_lapampasector_during:+.2f}} | {{st_main_lapampasector_during_p:.2f}} | {{st_main_lapampasector_after:+.2f}} | {{st_main_lapampasector_after_p:.2f}} |
| Corridor across the road | {{st_main_corridoracross_during:+.2f}} | {{st_main_corridoracross_during_p:.2f}} | {{st_main_corridoracross_after:+.2f}} | {{st_main_corridoracross_after_p:.2f}} |
| Extra buffer zone (Amarakaeri) | {{st_main_amarakaeribzex_during:+.2f}} | {{st_main_amarakaeribzex_during_p:.3f}} | {{st_main_amarakaeribzex_after:+.2f}} | {{st_main_amarakaeribzex_after_p:.2f}} |
| Tambopata reserve | {{st_main_tambopatareser_during:+.2f}} | {{st_main_tambopatareser_during_p:.3f}} | {{st_main_tambopatareser_after:+.2f}} | {{st_main_tambopatareser_after_p:.3f}} |

- **Wild cluster bootstrap (999 draws, only {{st_clusters_lp:.0f}} and {{st_clusters_across:.0f}} treated blocks):** La Pampa 2019–21 p = {{st_wcb_lp_p:.2f}}; corridor across the road p = {{st_wcb_across_p:.2f}}.
- **Old, contaminated comparison:** La Pampa {{st_contam_lapampasector_during:+.2f}} ha per cell-year.
- **Robust to:** gold-bearing land × year effects ({{st_gold_lapampasector_during:+.2f}}, p = {{st_gold_lapampasector_during_p:.2f}}); Poisson ({{st_ppml_lapampasector_during:+.2f}} log points, p = {{st_ppml_lapampasector_during_p:.2f}}).

![Year-by-year per-cell event study (2014-18 = reference)](output/fig_v2_stats_event.png)

- **Pre-trends:** with the pooled 2014–18 reference, La Pampa's 2010–13 leads are jointly different from zero (p = {{st_event_lp_pretrend_p:.3f}}); the corridor across the road passes (p = {{st_event_across_pretrend_p:.2f}}).

**Why it matters:** the zone-level fall stands out in hectares; per cell and per unit of size it doesn't clearly. Honest wording: "consistent with a short-lived effect on net mining", not "proven".

**Code:** `code/peru.py`, `code/peru_models.py`, `code/v2_stats.py`.

## 15. Attempt 2: a synthetic twin. It fails for levels.

**Bottom line:** A weighted mix of Peruvian zones cannot copy La Pampa's size, so this method only adds a weak extra check. [[D]]

**What it is:** Synthetic control builds a fake Tambopata from a weighted mix of other zones, fitted to the years before 2019. It differs from Ruby's idea: a mix of many zones instead of one real twin.

![Synthetic control attempt (not used for claims)](output/fig_peru_synth.png)

**How to read it:**
- **Left (A):** hectares. **Right (B):** each zone scaled to its own 2014–18 average.
- **Top:** gold line = real Tambopata; blue dashed = the synthetic copy. Before 2019 (shaded) they should overlap.
- **Bottom:** the gap between them. Grey lines = the same gap when each donor zone pretends to be the target.

**What it shows:**
- **In hectares, no fit.** Before 2019, Tambopata added {{synth_core_add_pre_mean_tam}} ha per year; the best mix only {{synth_core_add_pre_mean_synth}}. Tambopata lay outside every other zone's range in {{synth_core_add_hull_years_outside}} of 9 years. [[D]]
- **Scaled (B), a good fit.** Tambopata's 2019–21 dip is the deepest of {{synth_core_addsc_n_units_ranked}} zones (rank {{synth_core_addsc_rank}}). But 6 zones are too few to prove anything. [[D]]

**Why it matters:** You can't average small numbers into a big one. That is why attempt 1 (section 14) compares *changes*, and why attempt 3 (section 16) had to look abroad.

**Code:** `code/peru_synth.py`.

## 16. Attempt 3: rule-based twins (Ruby's design), now the three best

**Bottom line:** No area in the Amazon passes all four rules. Relax one rule, and the best twin is **Amanã National Forest** in Brazil. It grew just like Tambopata until 2018. In 2019–21, Tambopata added new mining at {{ctl_relaxed_during_ratio:.0%}} of the twin's pace. [[D]]

**The idea (Ruby):** Don't build a fake Tambopata. Find one existing area that passes four rules:

1. **R1 Mining before 2019:** at least 500 ha of mining seen by satellite by 2018.
2. **R2 No intervention:** no operation against mining reported in 2017–25.
3. **R3 Far enough away:** outside Madre de Dios, so La Pampa's miners can't simply walk over.
4. **R4 Geographic twin:** lowland mining like La Pampa (below 500 m), and at least a fifth of its size. The closest survivor wins.

**What we did:**

- **Map:** {{ctl_n_areas}} protected areas, buffer zones and indigenous territories. Peru from the park service (SERNANP), the other eight countries from the Amazon network RAISG, Brazil's territories from FUNAI.
- **Mining (R1):** Amazon Mining Watch patches inside each area. One satellite product covers all nine countries.
- **Operations (R2):** a documented web search per candidate area, every query logged, including those with no hits.
- **Geography (R4):** elevation of each area's mining, from a public elevation service (OpenTopoData).

![Ruby's rules, step by step: how many areas survive each rule](output/fig_control_funnel.png)

**How to read it:** Each bar is the number of areas left after one more rule. The scale is logarithmic.

**What it shows:**
- {{ctl_n_r1}} areas had real mining before 2019. [[D]]
- Only {{ctl_n_r2}} of them had no operation found, and both are small and unlike La Pampa. [[D]]
- {{ctl_n_r1_unclear_or_unsearched}} more could not be classified: the search was unclear. [[D]]

**Why it matters:** Almost every big mining area in the Amazon got an operation. An untouched twin of La Pampa does not exist. That is a finding about enforcement, not a failure of the method.

![Map of all candidate areas with at least 500 ha of mining by 2018, coloured by what happened to them](output/fig_control_map.png)

**How to read it:** Each dot is an area with at least 500 ha of mining by 2018. Dot size = mining area. Colour = its fate under the rules. Green shapes are protected areas.

**What it shows:**
- Peru outside Madre de Dios has **no** big mining area. The nearest rule-passing candidates are in Brazil. [[D]]
- The big candidates cluster in Brazil's Tapajós gold region. Nearly all had an operation, most in 2023. [[D]]

**Relax one rule, and a twin appears.** Ruby asked for "no intervention in the same period". So we require no operation only in **2017–21**: Mercurio's years and the two before. {{ctl_n_relaxed}} areas pass. Best fit: **Amanã National Forest**.

| | Tambopata buffer zone | Amanã National Forest |
|---|---:|---:|
| Mining by 2018 (AMW, ha) | {{ctl_tam_stock_2018}} | {{ctl_relaxed_stock_2018}} |
| Median elevation of the mining (m) | {{ctl_tam_elev_m}} | {{ctl_relaxed_elev_m}} |
| Distance from La Pampa (km) | 0 | {{ctl_relaxed_dist_km}} |
| First operation found | Feb 2019 | Mar 2023 |

![Tambopata vs its rule-based twin: new mining per year (left) and total mining area before and after 2019 (right)](output/fig_control_compare.png)

**How to read it:**
- **Left:** new mining per year as a share of each area's 2018 mining. Same satellite product for both, so the shares compare fairly.
- **Right:** total mining area, 2018 = 100. Each area comes from its own MapBiomas collection; they sit side by side and are never subtracted.

**What it shows:**
- **Before 2019, the two grew alike:** both stood at about half their 2018 size in 2014 ({{ctl_mb_tam_index_2014}} and {{ctl_mb_twin_index_2014}}). [[D]]
- **2019–21:** Tambopata added {{ctl_relaxed_tam_during:.1f}}% of its 2018 mining per year; Amanã {{ctl_relaxed_ctl_during:.1f}}%. [[D]]
- **By 2021:** Tambopata's mining area was flat ({{ctl_mb_tam_index_2021}}); Amanã's had grown to {{ctl_mb_twin_index_2021}}. [[D]]
- **After 2021, the twin is spoiled:** Amanã got its own operation in March 2023 and fell. Use it for 2019–21 only.

**The best twins (final version, after the review):** the two areas that pass the relaxed rules: Amanã National Forest and the Tapajós protection area. **Munduruku was dropped:** our own search log records Operation Mundurukânia there in May 2021, inside the rule's 2017–21 window (from search snippets, unverified).

![Rule-based twins: growth before 2019 and pace after](output/fig_control_top3.png)

| Twin | Growth gap before 2019 (log points/yr; p) | 2019–21 pace, % of 2018 stock | Gap vs Tambopata |
|---|---:|---:|---:|
| Amanã National Forest | {{top3_amana_pre_growth_diff:+.2f}} ({{top3_amana_pre_growth_p:.2f}}) | {{top3_amana_twin_during:.1f}} | {{top3_amana_during_gap:+.1f}} |
| Tapajós protection area | {{top3_tapajos_pre_growth_diff:+.2f}} ({{top3_tapajos_pre_growth_p:.2f}}) | {{top3_tapajos_twin_during:.1f}} | {{top3_tapajos_during_gap:+.1f}} |

- **Tambopata 2019–21:** {{top3_tam_during:.1f}}% of its 2018 stock per year, below **both** twins, at {{top3_median_ratio:.0%}} of their median pace. [[D]]
- **No p-values here:** with three years per area, a t-test means little; we report the gap only.
- **Pre-trends are not parallel:** Tambopata grew faster than both before 2019 (significant against Tapajós), and the two sides come from different MapBiomas collections.
- **Another caveat:** on Amazon Mining Watch itself, Tambopata's 2019 value is its highest after 2018; the fall shows from 2020.
- **Ruby's caution holds:** "no intervention" is too strict a rule (no area passes); "comparable enforcement" needs zone-level enforcement data that doesn't exist publicly.

**Why it matters:** A second, independent comparison agrees with attempt 1 (section 14). Another country, another data source, picked by rules, not results. The 2019–21 fall is now much harder to dismiss.

**What still threatens it:**
- **Brazil weakened enforcement in 2019–22.** The twin may have grown faster than "normal", which flatters the gap.
- **"No operation found" is not proof of none.** Small patrols are often never published.
- **The two satellite products disagree on 2019.** AMW still sees a lot of new mining in Tambopata in 2019; MapBiomas sees little. Shares, not hectares, are compared here.

**Code:** `code/control_amw.py` (mining per area), `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py` (the rules and figures). Output: `output/control_funnel.csv`, `control_compare.csv`. Operation searches: `docs/overnight/notes/control_interventions.csv`, coded in `data_intermediate/operations_coded.csv`.

## 17. Every movement and comparison, tested, and what a referee found

**Bottom line:** the move across the road and the depth change are statistically clear; the fall in La Pampa is large in hectares but fragile in every finer test. A critical referee found five errors in our first round; all are fixed below. [[D]]

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

**How to read p:** below 0.05 = unlikely to be chance. With 15 zones the smallest possible randomization p is 0.07, so "rank 1 of 15" is as strong as that test can get.

**What the referee found, and what we changed:**

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
| Untraceable numbers (Sentinel-2, producer gold) | Now computed in code | See sections 8 and 11 |

**Full review:** `docs/overnight/notes/critical_review_v2.md`.

**Why it matters:** the professor will ask "is this significant?" This table answers each claim, including the ones that fail.

## 18. Brazil: the same pixel method supports the direction, not the cause

**Bottom line:** same method, weaker result. The big territories fell after 2022–24, but not after their *own* operations, and the staggered test finds **no significant effect**. Brazil supports the direction, not the cause. [[D]]

**What we did (same as Peru):**
- **Data:** MapBiomas Brazil Collection 11 maps, 1985–2025, read only around each territory (24 territories with mining + two rings around Yanomami).
- **Check:** Kayapó mining {{brv2_kayapo_check_2024}} ha (2024) and {{brv2_kayapo_check_2025}} ha (2025) vs 17,632 and 18,573 on the MapBiomas platform. **This fixes our old Brazil mismatch** (we were comparing Collection 10.1 with the platform's Collection 11).
- **Accounting:** first-time mining, returns to old pits, stopped.
- **Test:** staggered DiD, territory + year effects, each territory treated from its own first operation ({{brv2_n_treated:.0f}} of {{brv2_n_units:.0f}} territories); Gardner's two-stage estimator, robust to staggered timing; randomization inference with 2,000 shuffles.

![Brazil, same pixel method as Peru: first-time mining and returns to old pits](output/fig_brazil_v2_pixels.png)

**What it shows:**
- **Yanomami:** {{brv2_yan_new_2019_22}} ha/yr of first-time mining in 2019–22, {{brv2_yan_new_2023_25}} in 2023–25. The fall shows from 2024, a year after the operation. [[D]]
- **Staggered DiD:** {{brv2_did2s_treat:+.2f}} log points (p = {{brv2_did2s_treat_p:.2f}}); randomization p = {{brv2_ri_p:.2f}}. Wrong sign, not significant. [[D]]
- **Why the null, and the wrong sign:** after correcting the dates (Munduruku from its May 2021 operation; Kayapó from September 2024), territories still don't fall faster after their own operation. Sararé surged as its operation began, and the test has little power (few territories, few years after).
- **Products disagree on Yanomami's timing:** MapBiomas shows the fall only from 2024; Amazon Mining Watch from 2023 ({{bs_yan_new_ha_2022}} → {{bs_yan_new_ha_2023}} ha); MAAP #242 reports new garimpo impact of about 1,800 ha (2022) and 330 ha (2023). Timing-based tests are sensitive to this.
- **No spill next door:** the rings around Yanomami got almost no new mining (0–10 km: {{brv2_r0_10_post:.1f}} ha/yr after 2023). Miners went toward the Venezuelan border and to other territories like Sararé (ISA 2026; Greenpeace).

**Support and challenge from the earlier Brazil steps:**
- **Support:** Amazon Mining Watch shows Yanomami −63% after its operation; IBAMA fines fell 2019–22 while mining tripled (national weakening, then reversal in 2023).
- **Challenge:** MapBiomas and AMW disagree on timing (2023 vs 2024). A national change in January 2023 (new government, end of the gold "good faith" rule, electronic gold invoices from August 2023) hit all territories at once, which a territory-level design can't separate.

**Why it matters:** Brazil fits "enforcement plus tracing reduces mining", but the cause could be national rules as much as local operations. That's a lesson for Peru's corridor (section 19).

**Code:** `code/brazil_raster.py`, `code/brazil_v2.py`, plus `brazil_stagger.py` (AMW), `brazil.py`, `brazil_ibama.py`.

## 19. What FZS can do with this

**Bottom line:** keep enforcement on longer than two years, guard the legal boundary next to the target, watch old pits, and push tracing and taxes inside the legal corridor. [[P]]

**1. Expect the response across the nearest legal boundary.** After Mercurio, new mining jumped into the corridor right across the highway, then went deeper. Any operation should plan patrols on the *legal* side of its boundary too.

**2. Monitor old pits, not only forest edges.** In 2023 most new mining in La Pampa was on old pits. Forest-loss alerts never see this; MapBiomas returns or pond colour (Dethier et al. 2023) do.

**3. Where to enforce next (prediction):** a model trained on 2019–21 predicts 2022–25 in held-out 10-km blocks with AUC {{risk_auc_spatial_holdout:.2f}}, barely above the {{risk_auc_benchmark:.2f}} of "is there mining nearby?" alone. It says: new mining starts next to old mining. It misses the reserve incursion, which comes by river. For 2026–28 it flags {{risk_hi_cells_outside_corridor:.0f}} high-risk 1-km cells outside the legal corridor: {{risk_hi_cells_lapampasector:.0f}} in the La Pampa sector and {{risk_hi_cells_nativecommunitie:.0f}} in native communities. [[P]]

![Predicted risk of first-time mining 2026-28](output/fig_v2_risk_map.png)

**4. Make the legal corridor a real filter.** Miners who cross into the corridor and dodge tracking pay almost nothing and ignore mercury rules.
- **The gap:** 0% royalty, 1.5% withholding, and only 145 of 9,592 registered miners fully formal (2021).
- **The fix:** proof of gold origin, gold-buyer registers, real formalization deadlines, mercury checks inside the corridor.
- **A model:** Brazil's 2023 reforms (end of the "good faith" rule, electronic gold invoices).

**5. Count the social and health cost.**
- **Damage:** each kg of gold mined in Peru costs US$81,000–364,000 (Conservation Strategy Fund calculator).
- **Mercury:** over a third of carnivorous fish exceed the limit hundreds of km downstream; exposed children score 4.68 IQ points lower.
- **Exploitation:** about 4,500 women are sexually exploited near camps, 78% of them minors.
- **Livelihoods:** about 46,600 people depend directly on mining. Enforcement without income alternatives invites return.

**6. Keep river posts staffed.** The 2025 incursion into the reserve followed the navy's withdrawal from the Malinowski river posts (MAAP #241).

**What would let us say more:** dated patrol and interdiction records per zone (SERNANP, FZS, police); concession and REINFO maps to grade legality pixel by pixel; pond-colour or dredge counts for activity on old pits and rivers.

## 20. What we can claim, and how strongly

| Claim | Label | Evidence for | Evidence against |
|---|---|---|---|
| Net new mining in Tambopata fell sharply in 2019–21 | [[D]] | Course table = raster; rank 1 of 15 | First-time mining only halved; clearing continued through 2019 |
| Mercurio caused the 2019–21 fall in net mining, roughly {{model_m1_during:,.0f}} to {{model_m3_during:,.0f}} ha/yr | [[C]] *conditional* | Rank 1 of 15 in hectares (p = {{model_m1_ri_p:.2f}}); below both twins | Ordinary relative to size; cell pre-trends fail; extra buffer zone also treated |
| New mining moved into the legal corridor, across the road, then deeper | [[D]] | Raster bands; depth break p < 0.01; AMW agrees; MAAP #208 (74%) | Can't show the same people moved; the road was crossed before (2008) |
| Miners returned to old pits in 2023 | [[D]] | Raster accounting; MAAP #193 | Map flicker inflates old-pit counts |
| La Pampa had not run out of gold | [[D]] | Geology: {{gold_broad_lapampasector_depleted_2018:.0%}} mined by 2018 | Coarse map; no gold grade |
| The official gold series fell 88% | **withdrawn** | — | The series dropped its artisanal estimate in 2020; producer-declared gold rose |
| Corridor miners mine informally and don't declare | plausible mechanism, **not claimed** | Formalization rates, Bolivia exports, unknown-origin exports | No trace of where Madre de Dios gold is declared |
| The region mined less | **rejected** | — | First-time mining rose {{v2_new_total_2016_18}} → {{v2_new_total_2022_25}} ha/yr |
| Brazil: operations reduced mining | **not claimed** | Falls after 2022–24; AMW −63% Yanomami | Staggered DiD {{brv2_did2s_treat:+.2f}} (wrong sign, p = {{brv2_did2s_treat_p:.2f}}); low power; national reforms in 2023 |
| Next operation: local fall while present, a move across the nearest legal boundary, a return within ~3 years | [[P]] | Peru pattern | One operation, one region; risk model barely beats "mining nearby" |

**Why it matters:** grading puts 30% on honesty about the claim. One labelled conditional causal claim, with failed tests shown, beats a vague strong one.

## 21. The report draft (the 2-page brief)

**What this is:** the brief as we'd hand it in. Four parts, one figure, every claim labelled. Numbers come from the same `output/numbers.csv`. Print version (two A4 pages for parts 1–4): `docs/brief/BRIEF_DRAFT.html`. Source text: `docs/brief/brief_content.md`.

**What's still open:** team wording of the [[C]] sentence, access dates for references, and the AI appendix (section 23).

{{BRIEF_BODY}}

## 22. Where everything lives

**Run everything:** `uv run python code/main.py`. It takes about a minute and writes every figure, table and number to `output/`.

| Step | Code | Main output |
|---|---|---|
| Checks against publisher numbers | `code/checks.py` | `output/checks.csv` |
| 14 Measure + basic comparison | `code/peru.py` | `fig_brief_main.png`, `fig_peru_did_table.csv` |
| 14 Event study + fake places | `code/peru.py` | `fig_peru_event_study.png`, `peru_placebo_in_space.csv` |
| 14 Controls (gold price, trends, size) | `code/peru_models.py` | `fig_peru_models.png`, `peru_models.csv` |
| 16 Ruby's rule-based twin | `code/control_*.py` | `fig_control_*.png`, `control_funnel.csv`, `control_compare.csv` |
| 15 Synthetic twin | `code/peru_synth.py` | `fig_peru_synth.png` |
| Robustness (other comparison zones, drop largest) | `code/peru_robust.py` | `peru_robustness.csv` |
| 4 Zones, pixel accounting, 1-km cells | `code/raster_zones.py` | `fig_v2_zone_map.png`, `data_intermediate/zone_year_v2.csv` |
| 5–7 Corridor, road, depth, old pits | `code/raster_layers.py`, `code/v2_tests.py` | `fig_v2_stream.png`, `fig_v2_road_*.png`, `fig_v2_sankey.png` |
| 8 Quarterly alerts | `code/glad_alerts.py` | `fig_v2_glad_quarterly.png` |
| 9 Gold left | `code/raster_gold.py` | `v2_gold_depletion.csv` |
| 12 Spending, 2012 wave, timeline | `code/v2_tests.py` | `fig_v2_enforcement_spending.png` |
| 10 Inside the reserve | `code/peru_anp.py` | `fig_peru_inside_reserves.png` |
| 11 Declared gold | `code/peru_production.py` | `fig_peru_production_vs_area.png` |
| 18 Brazil (pixels, staggered DiD) | `code/brazil_raster.py`, `brazil_v2.py`, `brazil*.py` | `fig_brazil_v2_pixels.png`, `fig_brazil_*.png` |
| 14 Cell-panel statistics | `code/v2_stats.py` | `fig_v2_stats_*.png`, `v2_stats_coefficients.csv` |
| 16 Top-3 twins + tests | `code/control_top3.py` | `fig_control_top3.png`, `control_top3_tests.csv` |
| 19 Risk map, zone profile, AMW check | `code/v2_extra.py` | `fig_v2_risk_map.png`, `v2_zone_profile.csv` |
| The brief's figure | `code/brief_figure.py` | `fig_brief_main.png` |
| Every number | all of the above | `output/numbers.csv` |

**Other files:**
- **Brief draft:** `docs/brief/BRIEF_DRAFT.md` and `.html`.
- **Operation searches:** `docs/overnight/notes/control_interventions.md` and `brazil_data_and_operations.md`.
- **Log and decisions:** `docs/overnight/LOG.md`. **Data log:** `DOWNLOAD_LOG.csv`.

**Big raw files are git-ignored** (Amazon Mining Watch, RAISG, MapBiomas Amazonía, FUNAI). The run then uses the small files in `data_intermediate/`. Download links are in `DOWNLOAD_LOG.csv`.

## 23. What's blocked on you

**Must do (only a human can):**

1. **Share this page** with the team. It's private until you click Share.
2. **Agree on the claim wording,** especially the one conditional causal sentence (sections 13–16). It's a team call.
3. **Ruby: check sections 4 and 16.** Section 4 is the zone map (we kept the middle La Pampa window). Section 16 is her three-twin design. Should native communities inside the corridor count as legal?
4. **Confirm Brazil's scope with Raji** (appendix-level, as discussed).
4. **MAAP pages:** the site blocks scripts. Open each link in `docs/overnight/notes/maap_citations.md` in your browser and save it with File › Save Page As into `data_raw/maap/`.
5. **Re-open what you cite.** The course only allows sources you opened. The operation searches list every page; spot-check the ones used for Amanã, Kayapó and Yanomami.
6. **Team plan:** add members and roles to `templates/TEAM_PLAN.docx`.
7. **AI prompt for brief part 4:** I ran it (`docs/brief/ai_part4_raw.md`). If the course expects your own tool, re-run it.
8. **Merge:** the work sits on branch `analysis/overnight-2026-10-10`. Opening a pull request into `main` is your call.

**Nice to have:**

- **Munduruku before 2022:** search for operations in 2019–21. One may explain its early fall.
- **Brazil check:** the per-territory file is Collection 10.1; the website shows Collection 11. State the mismatch.
- **IBAMA embargo file:** no download link found.

{{NEXT_STEPS_DIAGRAM}}

## 24. Appendix: data, decisions and every number

**Data and checks** (one check per dataset; full log in `DOWNLOAD_LOG.csv`)

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
| MapBiomas Amazonía, Collection 6 (new, section 16) | Amazon mining 2023 = 775,746 ha | 0.78 Mha (factsheet p.3) | Match |
| MapBiomas Brazil, Collection 11, mining module (new) | Garimpo 2025 = 445,987 ha | 445,987 ha | Match |
| RAISG protected areas (new, section 16) | 401 areas downloaded | 401 in the service | Match |
| Amazon Mining Watch (sections 5, 16, 18) | — | No totals published | Not checkable |

**Decision log** (from `docs/overnight/LOG.md`)

{{DECISIONS_TABLE}}

**Every number** (filterable; from `output/numbers.csv`)

{{NUMBERS_TABLE}}
