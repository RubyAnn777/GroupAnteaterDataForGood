<!--
Source of docs/overnight/EXPLAINER.html (the team walkthrough). Build: `uv run python docs/overnight/build_report.py`.
Placeholders {{id}} or {{id:fmt}} come from output/numbers.csv (default ",.0f"; unknown ids fail the build).
Claim tags: [[D]] description, [[P]] prediction, [[C]] causal. Figures ![caption](output/x.png) are embedded.
Sections split on "## ". The first "> " line is the banner. {{BRIEF_BODY}} embeds the 2-page brief draft.
-->

# Mercurio cut new mining where it struck, for three years. The region kept growing.

> A guided walk through the analysis, in plain words. Each step says what we asked, what we did, where the code is, how to read the figure and why it matters. Section 21 holds the report draft. Every number comes from `output/numbers.csv`. Nobody has checked this yet: treat it as a draft.

## 1. The bottom line

**Operation Mercurio worked locally, and only for a while.**

- **During (2019–21):** net new mining in the targeted zone fell from {{mean_add_tambopata_2016_18}} to {{mean_add_tambopata_2019_21}} ha per year. Every one of those years was lower than any year from 2011 to 2018. [[D]]
- **But clearing didn't stop at once:** land mined for the first time only halved ({{t5_m2_2016_18}} → {{t5_m2_2019_21}} ha/yr), and forest clearing in La Pampa went on through 2019. It collapsed in 2020–21 (step 14). [[D]]
- **It crossed the road:** new mining in the corridor directly across the highway rose from {{v2_new_corridoracrosstheroa_2016_18}} to {{v2_new_corridoracrosstheroa_2019_21}} ha per year (steps 11–12). [[D]]
- **Against other Peruvian zones:** no other zone fell like this, with or without controls for the gold price, trends and size. [[D]]
- **Against Ruby's rule-based twin:** the closest match in the whole Amazon (Amanã, Brazil) grew like Tambopata until 2018. In 2019–21, Tambopata added mining at {{ctl_relaxed_during_ratio:.0%}} of the twin's pace. [[D]]
- **After (2022–25):** Tambopata came back to {{mean_add_tambopata_2022_25}} ha per year, much of it on old pits (step 13). The gold wasn't gone: about {{gold_broad_lapampasector_left_2018_ha:,.0f}} ha of gold-bearing land was still unmined in 2018 (step 15). [[D]]
- **Around it:** Madre de Dios as a whole did not fall: {{mean_add_mdd_total_2016_18}} → {{mean_add_mdd_total_2019_21}} → {{mean_add_mdd_total_2022_25}} ha per year. [[D]]
- **Inside the reserve:** small, but new in 2025 (+{{anp_tam_nr_addition_2025}} ha). [[D]]
- **Brazil:** territories fell after operations, while territories without one grew. But the timing is not clean enough to credit single operations. [[D]]

**Can we say Mercurio *caused* the fall?** Cautiously, yes, for **net** new mining in 2019–21 only. First-time clearing fell less and a year later. Two independent comparisons agree: 14 other Peruvian zones (steps 6–7) and a twin picked by rules abroad (step 8). One targeted zone still leaves room for luck or a local shock. We label it a **conditional causal claim**. [[C]]

**Why it matters:** FZS should expect enforcement to work **while it lasts** and **where it lands**, and miners to answer **across the road** and **in old pits**. It should not expect the region to mine less.

> **One correction from last night still stands.** "Pre-trends fail" came from one odd year: 2016 ({{tam_add_2016}} ha, then {{tam_add_2017}} ha in 2017). Averaged over several years, the fake-date test passes (step 7).

## 2. How to read this page

**Steps 3–19 walk through the analysis.** Steps 10–16 are new (plan v2, after Ruby's review). Each answers one question:

- **3** What is the question, and where?
- **4** What exactly do we measure?
- **5** The basic comparison
- **6** Is the fall special, or just noise?
- **7** Controls: gold price, trends, size
- **8** Ruby's idea: one real twin, picked by rules *(new)*
- **9** Add-on: a synthetic twin
- **10** New measure: one raster, our own zones *(v2)*
- **11** Where did the mining go? *(v2)*
- **12** Crossing the road *(v2)*
- **13** Returns to old pits *(v2)*
- **14** Timing by quarter *(v2)*
- **15** Was the gold gone? *(v2)*
- **16** Enforcement intensity and an earlier wave *(v2)*
- **17** Did it move into the reserve?
- **18** A cross-check with gold production
- **19** Brazil: staggered operations

Then: what we can claim (20), **the report draft (21)**, where everything lives (22), what's on you (23), appendix (24).

**Plain-word glossary**

| Term | Meaning here |
|---|---|
| **Buffer zone** | The ring of land around a protected area. La Pampa lies in Tambopata's buffer zone. |
| **New mining (additions)** | Mining area this year minus last year, in hectares (ha). 1 ha = 100 × 100 m. |
| **Targeted zone** | Tambopata buffer zone, hit by Mercurio from February 2019. |
| **Comparison zone** | A zone that shows what *might* have happened without the operation. |
| **Before / during / after** | 2016–18 / 2019–21 / 2022–25. |
| **Gap change** (difference-in-differences) | (targeted after − before) − (comparison after − before). |
| **Zone and year effects** (fixed effects) | A regression that removes each zone's normal level and each year's shared shock. |
| **Fake date** (placebo in time) | Pretend the operation started in 2016. A good method finds little. |
| **Fake place** (placebo in space) | Pretend each other zone was the target. Tambopata should stand out. |
| **Rule-based twin** (Ruby's idea) | One real area, picked by fixed rules before looking at results. |
| **Synthetic twin** (synthetic control) | A weighted mix of zones built to copy Tambopata before 2019. |
| **MapBiomas** | Yearly land-cover maps from satellites; our main measure (Peru: Collection 4). |
| **AMW** (Amazon Mining Watch) | A second satellite product: gold-mining scars across the whole Amazon, from 2018. |
| **First-time mining** (new land) | Pixels mapped as mining for the first time since 1985. |
| **Return to old pits** | Pixels mined before, not last year, mined again now. |
| **La Pampa sector** | Tambopata buffer zone between longitudes 70.15° and 69.80° W (our boundary; no official one). |
| **Corridor across the road** | Legal mining corridor within 10 km north of the highway, opposite La Pampa. |

**Claim labels.** The brief must label every claim: [[D]] = what happened; [[P]] = what we expect; [[C]] = what caused it.

## 3. The question: what happens in and around a target when enforcement ends?

**What FZS asked:** Christof Schenck's team supports enforcement patrols around Tambopata. They want to know what to expect when an operation ends.

**What we did:** We followed one operation in two countries:
- **Peru:** Operation Mercurio, February 2019, at La Pampa in the Tambopata buffer zone.
- **Brazil:** the Yanomami operation, February 2023.

**The places in Peru:**
- **Targeted:** Tambopata buffer zone.
- **Main comparison:** Amarakaeri buffer zone (nearby, mining, no Mercurio).
- **Also tracked:** Tambopata National Reserve itself, the rest of Madre de Dios, 13 other Peruvian buffer zones with mining, and a rule-based twin abroad (step 8).

![Map of Madre de Dios: protected areas, buffer zones, the legal mining corridor and mining patches by start year](output/fig_map_madre_de_dios.png)

**How to read it:** Coloured dots are mining patches from Amazon Mining Watch, coloured by the year they first appear. Outlined areas are reserves, buffer zones and the legal mining corridor.

**What it shows:** Most mining sits in the legal corridor and around La Pampa. The newest patches (2025–26) hug the northern edge of the reserve. [[D]]

**Why it matters:** The target is small, and mining sits right next to it. Moving a few kilometres is easy for miners.

**Code:** `code/spatial.py`.

## 4. What we measure: new mining per year, not total mining

**The rule:** We count the **new** mining area each year (this year's mining minus last year's). The course requires this, because totals only grow and track the gold price.

**Data:** MapBiomas Peru, Collection 4, the "mining" land class, from satellite maps.

**Limits:**
- Legal and illegal mining look the same.
- River dredges and mercury are invisible.
- Re-mining an old site can count as new.

![New mining per year by buffer zone, Madre de Dios total and rest, and the gold price](output/fig_peru_additions.png)

**How to read it:**
- **Top:** new mining per year in three buffer zones.
- **Middle:** the whole department and the "rest" (department minus all buffer zones).
- **Bottom:** gold price.
- **Red line:** Mercurio. Grey dashed lines: COVID, Plan Restauración and the 2023 state of emergency.

**What it shows:**
- Tambopata drops to almost nothing in 2019–21, then jumps in 2023.
- Every series spikes in 2023.
- The gold price rose {{gold_price_ratio_2025_2018:.1f}}× from 2018 to 2025, but only {{gold_price_pct_change_2022_2023:.0f}}% in 2023 itself. [[D]]

**Why it matters:** Several events overlap. A simple "before vs after" in one zone can't separate them, so we need comparison zones.

**Code:** `code/peru.py` (`build_series`, `fig_additions`).

## 5. The basic comparison: Tambopata fell, Amarakaeri rose

**Question:** Did the targeted zone change differently from a similar zone nearby?

**What we did:** We averaged new mining per year in each period and compared the changes. This is the course's starter comparison.

| ha of new mining per year | Before 2016–18 | During 2019–21 | Change |
|---|---:|---:|---:|
| Tambopata (targeted) | {{mean_add_tambopata_2016_18}} | {{mean_add_tambopata_2019_21}} | {{did_main_tambopata_change}} |
| Amarakaeri (comparison) | {{mean_add_amarakaeri_2016_18}} | {{mean_add_amarakaeri_2019_21}} | +{{did_main_amarakaeri_change}} |
| **Gap change** | | | **{{did_main}}** |

![The brief's figure: Tambopata vs Amarakaeri vs inside the reserve; Madre de Dios total and rest](output/fig_brief_main.png)

**How to read it:**
- **Top:** dots are yearly values. Thick bars are the period averages (before, during, after).
- **Bottom:** the whole department and the rest.

**What it shows:**
- Tambopata collapses during 2019–21 and returns after.
- Amarakaeri and the rest of the department rise. [[D]]

**Two quick tests:**
- **Fake date** (pretend the operation began in 2016): gap change {{did_placebo}} ha/yr. Small next to −1,762. [[D]]
- **Longer "before"** (2014–18): {{did_main_base_2014_18}} ha/yr. Almost the same. [[D]]

**Why it matters:** This is the clearest single number for the brief. It is still only a description: Amarakaeri is one zone, it may have received miners from Tambopata, and it had its own enforcement.

**Code:** `code/peru.py` (`describe_and_compare`). Table: `output/fig_peru_did_table.csv`.

## 6. Is the fall special, or just noise? Year by year, against every zone

**Question:** Is Tambopata's 2019–21 drop bigger than the normal ups and downs of any zone?

**What we did:** an **event study**. For each year, we measure how far Tambopata sits above or below the comparison zones, relative to 2018. Then we repeat it pretending each of 14 other zones was the target (the grey band).

**Model:** new mining = zone effect + year effect + one Tambopata-specific term per year (2018 left out). Estimated with `pyfixest`.

![Event study: Tambopata minus comparison zones, relative to 2018; grey band = same calculation for every other zone](output/fig_peru_event_study.png)

**How to read it:**
- **Red dots:** Tambopata vs the two other Madre de Dios zones with mining.
- **Blue squares:** Tambopata vs all 14 Peruvian zones with mining.
- **Grey band:** the range you get by pretending each other zone was targeted.
- A dot far below the band means "nothing else moved like this".

**What it shows:**
- 2019–22 sit far below the band: Tambopata ranks **1st of {{placebo_space_n_units}}** zones. [[D]]
- 2023 is inside the band again. [[D]]
- 2016 also dips ({{eventstudy_pretrend_poolA_2016}} ha). That is one low year ({{tam_add_2016}} ha) between two high ones, not a trend. [[D]]

**Why it matters:**
- With one targeted zone, normal error bars mean nothing. The fake-place ranking is our honest substitute.
- Ranking 1st of 15 would happen by chance about 1 time in 15 (~7%).

**Code:** `code/peru.py` (`run_event_study`, `placebo_restricted`). Output: `output/peru_event_study.csv`, `output/peru_placebo_in_space.csv`.

## 7. Controls: does the gold price, a trend or zone size explain the fall? No.

**Your question:** "Did the models control for the gold price?" **Yes, in two ways.**

1. **Year effects already remove the gold price.** The price is the same for every zone in a given year. So anything that hits all zones in a year (gold price, COVID, national policy) cancels out. The 2×2 comparison in step 5 cancels it the same way.
2. **But big mining zones may react more to a price rise.** So we added a control for that (M2 below).

**What we did:** We ran four models on all 15 Peruvian buffer zones with mining, 2014–2025. Each was run three ways: with the real date, with a fake 2016 date, and with each other zone as the fake target.

| Model | What it adds | During 2019–21 | After 2022–25 | Fake 2016 | Rank |
|---|---|---:|---:|---:|---:|
| **M1** | Zone + year effects (gold price, COVID as shared shocks) | {{model_m1_during}} | {{model_m1_after}} | {{model_m1_placebo}} | {{model_m1_rank}} of {{model_m1_n}} |
| **M2** | + bigger zones react more to gold price | {{model_m2_during}} | {{model_m2_after}} | {{model_m2_placebo}} | {{model_m2_rank}} of {{model_m2_n}} |
| **M3** | + each zone's own trend | {{model_m3_during}} | {{model_m3_after}} | {{model_m3_placebo}} | {{model_m3_rank}} of {{model_m3_n}} |
| **M4** | Scaled to each zone's size (1 = a normal pre-2019 year) | {{model_m4_during:.2f}} | {{model_m4_after:.2f}} | {{model_m4_placebo:.2f}} | {{model_m4_rank}} of {{model_m4_n}} |

Units: ha per year (M1–M3); M4 is in "normal years". Negative = Tambopata fell more than the others.

![Model ladder: real fall (2019–21) vs fake-date fall (2016–18) for four models](output/fig_peru_models.png)

**How to read it:** For each model, the gold bar is the real effect and the grey bar the fake-date effect. A trustworthy result has a long gold bar and a short grey bar.

**What it shows:**
- **During:** the gap is {{model_m1_during}} to {{model_m3_during}} ha per year (M1–M3). That is about one normal Tambopata year ({{mean_add_tambopata_2014_18}} ha in 2014–18) wiped out, every year. [[D]]
- The fake date is 4–9 times smaller and points both ways. [[D]]
- **After:** the gap shrinks to between {{model_m3_after:,.0f}} and +{{model_m1_after:,.0f}}, so the effect fades. [[D]]
- **Mean reversion?** Tambopata's highest year in 2019–21 ({{tam_add_max_2019_2021}} ha) was below its lowest year in 2011–18 ({{tam_add_min_2011_2018}} ha). Drifting back to normal can't explain a drop that far. [[D]]

**Why it matters:** This is our strongest evidence. It is what lets us make a careful causal statement for 2019–21:

> [[C]] *If the other zones show what Tambopata would have done without Mercurio, the operation cut new mining there by roughly 1,450–1,860 ha per year in 2019–21. The cut did not last into 2022–25.*

**What still threatens it:**
- **One targeted zone.** Rank 1 of 15 can happen by chance (~7%).
- **Spillovers.** Miners pushed into Amarakaeri make the gap look bigger. M1–M4 use 14 zones, mostly far away, so this matters less.
- **Anything else that hit only Tambopata in 2019.** COVID and the gold price hit all zones, but local events would not.
- **Measurement.** River dredges are invisible. A move from land to river would look like a fall.

**Code:** `code/peru_models.py` (new today). Output: `output/peru_models.csv`, `output/fig_peru_models.png`. Cross-checked: the numpy fit equals `pyfixest`.

## 8. Ruby's twin: no clean one exists; the closest one confirms the fall

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

**Why it matters:** A second, independent comparison agrees with steps 5–7. Another country, another data source, picked by rules, not results. The 2019–21 fall is now much harder to dismiss.

**What still threatens it:**
- **Brazil weakened enforcement in 2019–22.** The twin may have grown faster than "normal", which flatters the gap.
- **"No operation found" is not proof of none.** Small patrols are often never published.
- **The two satellite products disagree on 2019.** AMW still sees a lot of new mining in Tambopata in 2019; MapBiomas sees little. Shares, not hectares, are compared here.

**Code:** `code/control_amw.py` (mining per area), `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py` (the rules and figures). Output: `output/control_funnel.csv`, `control_compare.csv`. Operation searches: `docs/overnight/notes/control_interventions.csv`, coded in `data_intermediate/operations_coded.csv`.

## 9. Add-on: a synthetic twin. It fails for levels, works for shares.

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

**Why it matters:** You can't average small numbers into a big one. That is why steps 6–7 compare *changes*, and why step 8 had to look abroad.

**Code:** `code/peru_synth.py`.

## 10. New measure: one raster map, our own zones (plan v2)

**Bottom line:** We now count mining pixel by pixel on one MapBiomas grid, inside boundaries we choose. That reproduces the official numbers and lets us split La Pampa from its surroundings. [[D]]

**Why we rebuilt it (Ruby's review):** whole buffer zones mix La Pampa (shut down) with new fronts. "Rest of Madre de Dios" hid the legal corridor. Different products sat on different grids.

**What we did:**
- **Data:** the MapBiomas Peru Collection 4 maps for every year 1985–2025 (30 m pixels), the same product as the course tables.
- **Zones:** one map, 12 zones, fixed order for overlaps: reserves → native communities → corridor across the road → rest of corridor → La Pampa sector → rest of buffer zone → other buffer zones → rest of Madre de Dios.
- **Check:** the raster gives the Tambopata buffer zone {{v2_check_tambopatabufferzone_2025}} ha in 2025 (table: 20,730) and the reserve {{v2_check_tambopatareserve_2025}} ha (platform: 777).

![Zone map v2 around La Pampa](output/fig_v2_zone_map.png)

**How to read it:** coloured areas are zones; black pixels were mapped as mining at least once since 1985. The thick line is the Interoceanic Highway. Dotted lines mark the La Pampa longitudes.

**What it shows:** La Pampa's mining sits right against the road; the legal corridor starts on the other side. [[D]]

**Each year's change, split into its parts:**

| Tambopata buffer zone, ha/yr | 2016–18 | 2019–21 | 2022–25 |
|---|---:|---:|---:|
| Net addition, course table | {{t5_m0_2016_18}} | {{t5_m0_2019_21}} | {{t5_m0_2022_25}} |
| Net addition, raster (same product) | {{t5_m1_2016_18}} | {{t5_m1_2019_21}} | {{t5_m1_2022_25}} |
| Land mined for the first time | {{t5_m2_2016_18}} | {{t5_m2_2019_21}} | {{t5_m2_2022_25}} |
| Return to old pits | {{t5_m3_2016_18}} | {{t5_m3_2019_21}} | {{t5_m3_2022_25}} |
| Amazon Mining Watch new area (480 m squares) | — | {{t5_m4_2019_21}} | {{t5_m4_2022_25}} |

**Why it matters:** the famous "1,640 → 163" is a *net* number. First-time mining fell by half, not by 90%. The rest of the drop is old mining stopping.

**Boundaries change over time:** the current Tambopata buffer zone was approved in {{t6_bz_approved_tambopata:.0f}}, Bahuaja-Sonene's in {{t6_bz_approved_bahuajasonene:.0f}}, Amarakaeri's in {{t6_bz_approved_amarakaeri:.0f}}; the corridor dates from 2012 (D.L. 1100). MapBiomas applies today's boundaries to every year, and so do we.

**Code:** `code/raster_zones.py`, `code/v2_tests.py` (T5, T6).

## 11. Where did the mining go? Into the legal corridor

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

**Why it matters:** Mercurio moved new mining from illegal land to legal land. For the reserve that is a win. For the region it is not: total new mining kept growing, and corridor mining still uses mercury.

**Can't show:** that the *same* people moved. New arrivals and the gold price fit the same picture.

**Code:** `code/raster_layers.py`.

## 12. Crossing the road: new mining jumped to the north side

**Bottom line:** Right after Mercurio, the tallest bars sit 0–2 km north of the highway, directly across from La Pampa. The north side's share of new mining went from {{t1_road_north_share_2016_18:.0%}} (2016–18) to {{t1_road_north_share_2019_21:.0%}} (2019–21). [[D]]

![New mining by distance band south and north of the highway](output/fig_v2_road_bands.png)

**How to read it:** each bar is a 1-km strip parallel to the highway, inside the La Pampa longitudes. Orange = south (buffer zone side), blue = north (corridor side). Height = land mined for the first time per year.

**Is the jump unusual? Fake start dates:**

![Fake start dates for the move across the road](output/fig_v2_road_placebo.png)

**What it shows:**
- The 2019 move north (+{{t1_road_shift_2019:.2f}} share points) ranks {{t1_road_shift_rank:.0f}} of {{t1_road_shift_n:.0f}} start years. The two above it start in 2020 and 2008. [[D]]
- **The road has been crossed before.** In 2008–10 most new mining was north of the road (the Guacamayo boom; share {{t1_road_north_share_2008:.0%}} in 2008). It moved south to La Pampa by 2015 ({{t1_road_north_share_2015:.0%}}), then back north after Mercurio ({{t1_road_north_share_2021:.0%}} in 2021). [[D]]
- **Boundary choice doesn't matter:** a narrower or wider La Pampa window changes the La Pampa fall from {{t4_lp_narrow_change:.0%}} to {{t4_lp_wide_change:.0%}}.

**Why it matters:** miners follow enforcement and gold across a two-lane road. Any operation south of the highway should expect a response north of it.

**Code:** `code/raster_zones.py` (road bands), `code/v2_tests.py` (T1, T4).

## 13. Returns to old pits: why the net numbers mislead

**Bottom line:** In 2023, most new mining in La Pampa happened on **old pits**, not on new land. The net table can't see this. [[D]]

![New mining split into new land and returns to old pits, by zone and period](output/fig_v2_sankey.png)

**How to read it:** left = where new mining came from (new land, or old pits mined again). Right = the zone it appeared in. Width = hectares per year; same scale in all three panels.

**What it shows:**
- **La Pampa sector, returns to old pits:** {{v2_lapampa_remined_2016_18}} → {{v2_lapampa_remined_2019_21}} → {{v2_lapampa_remined_2022_25}} ha/yr. [[D]]
- **Share of all new mining on old pits:** {{v2_remined_share_2016_18:.0%}} → {{v2_remined_share_2019_21:.0%}} → {{v2_remined_share_2022_25:.0%}}. [[D]]
- MAAP #193 independently reports miners back on degraded land in La Pampa in 2023.

**Caveat:** the old-pit count includes year-to-year map flicker (about 300 ha/yr even before 2019). Trust the 2023 jump, not small changes.

**Why it matters:** an operation can stop clearing while miners quietly return to old pits. FZS should monitor old mining sites, not only forest edges.

## 14. Timing by quarter: clearing in La Pampa went on through 2019

**Bottom line:** Forest clearing on La Pampa's mining land did **not** stop in February 2019. It was higher in 2019 than in 2018 and collapsed only in 2020–21. [[D]]

![Quarterly forest-loss alerts on mining land, by zone](output/fig_v2_glad_quarterly.png)

**What we did:** University of Maryland GLAD forest-loss alerts (Landsat, every pixel dated to the day), counted per quarter on land that MapBiomas maps as mining.

**What it shows:**
- **La Pampa sector, alerts on mining land:** {{glad_mining_lapampasector_2017}} ha (2017), {{glad_mining_lapampasector_2018}} (2018), **{{glad_mining_lapampasector_2019}} (2019)**, {{glad_mining_lapampasector_2020}} (2020), {{glad_mining_lapampasector_2021}} (2021). [[D]]
- **Corridor across the road:** {{glad_mining_corridoracrossther_2018}} ha (2018) → {{glad_mining_corridoracrossther_2019}} (2019) → {{glad_mining_corridoracrossther_2020}} (2020). [[D]]
- Sentinel-2 alerts (every 5 days) confirm clearing in western La Pampa from March to September 2019, so this is not just cloud delay.

**Why it matters:** this corrects our earlier wording. The brief must say clearing fell **from 2020**, not "immediately". It matches Dethier et al. (2023): activity spiked in La Pampa's northwest after the operation.

**Caveats:** clouds bunch alerts in the dry season; compare the same quarter across years. The data version changes in 2021. Alerts need standing forest, so returns to old pits never show.

**Code:** `code/glad_alerts.py`.

## 15. Was the gold gone? No.

**Bottom line:** By 2018, La Pampa had mined only {{gold_broad_lapampasector_depleted_2018:.0%}} of its gold-bearing land. About {{gold_broad_lapampasector_left_2018_ha:,.0f}} ha were left. "Miners left because the gold ran out" is unlikely. [[D]]

**What we did:** no one publishes gold left in the ground. Gold here is alluvial, so we used the national geology map (INGEMMET, 1:100,000): river deposits plus the gold-bearing terraces of the Madre de Dios Formation.

**Does the proxy work?** {{gold_broad_validation:.0%}} of all land ever mined in Madre de Dios lies on these units.

| Gold-bearing land already mined | by 2018 | by 2025 |
|---|---:|---:|
| La Pampa sector | {{gold_broad_lapampasector_depleted_2018:.0%}} | {{gold_broad_lapampasector_depleted_2025:.0%}} |
| Corridor across the road | {{gold_broad_corridoracrossther_depleted_2018:.0%}} | {{gold_broad_corridoracrossther_depleted_2025:.0%}} |
| Rest of mining corridor | {{gold_broad_restofminingcorrid_depleted_2018:.0%}} | {{gold_broad_restofminingcorrid_depleted_2025:.0%}} |
| Kotsimba | {{gold_broad_kotsimbanativecomm_depleted_2018:.0%}} | {{gold_broad_kotsimbanativecomm_depleted_2025:.0%}} |

**Why it matters:** enforcement, not exhaustion, is the better explanation for the move.

**Limits:** the map is coarse and says nothing about gold grade; old pits can be mined again.

**Code:** `code/raster_gold.py`.

## 16. Enforcement intensity and an earlier wave

**Bottom line:** enforcement money peaked in 2019 and faded every year after. Zone-level enforcement data does not exist publicly. [[D]]

![Anti-illegal-mining spending in Madre de Dios vs first-time mined land](output/fig_v2_enforcement_spending.png)

**What it shows:**
- **Peru's anti-illegal-mining programme (PP 0128), spending booked in Madre de Dios:** {{t8_pp0128_mdd_2018:,.0f}} soles (2018) → {{t8_pp0128_mdd_2019:,.0f}} (2019) → {{t8_pp0128_mdd_2021:,.0f}} (2021) → {{t8_pp0128_mdd_2025:,.0f}} (2025). It's a lower bound: national units book spending under Lima. [[D]]
- **Amarakaeri's side was enforced too:** official records show prosecutions in Camanti (next to Amarakaeri) in 2019–20, so it is not a clean control (Ruby's point).

**The earlier wave (2012–13 decrees and interdictions).** Asner and Tupayachi (2017) saw a regional dip, then a doubling. In the course table, Tambopata did **not** fall more than other zones in 2012–13: its gap was +{{t3_wave_m1_2012_13}} ha/yr, rank {{t3_wave_rank:.0f}} of {{t3_wave_n:.0f}}. [[D]] That wave was region-wide, not aimed at Tambopata, so our design can't see it.

**Why it matters:** the "delay" story now has a money trail: spending fell from 2020 while mining rebounded. Still description: enforcement goes where mining is worst.

**Code:** `code/v2_tests.py` (T3, T8). Sources: `docs/overnight/notes/enforcement_intensity.md`.

## 17. Did miners move into the reserve itself? Starting in 2025, yes

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

## 18. A cross-check: declared gold production collapsed while mapped mining grew

**Question:** Does official gold output tell the same story?

**What we did:** We downloaded Madre de Dios gold production from Peru's central bank (source: Ministry of Energy and Mines).

![Declared gold production vs mapped mining area, Madre de Dios](output/fig_peru_production_vs_area.png)

**What it shows:**
- Declared production fell {{pe_prod_fall_2018_2025_pct:.0f}}% from 2018 to 2025 ({{pe_prod_2018_t:.1f}} → {{pe_prod_2025_t:.1f}} tonnes).
- Over the same years, mapped mining area doubled ({{pe_prod_mapbiomas_level_2018_ha}} → {{pe_prod_mapbiomas_level_2025_ha}} ha). [[D]]

**Why it matters:**
- More gold is leaving through informal channels, or the rules on reporting changed. We can't tell which.
- Either way, official production is useless as a measure of mining here.

**Code:** `code/peru_production.py`.

## 19. Brazil: mining fell where operations came and grew where none did. The timing is messy.

**Bottom line:** All three big territories fell after 2022. Territories with no operation found grew sharply, which fits miners moving. But Munduruku fell a year *before* its operation, so timing alone can't credit the operations. [[D]]

**Is the Brazil data too bad?** No. **The design is the problem**, not the data. Almost every big territory got an operation in 2023–25. A new federal government took office in January 2023. Everything changed at once.

**The setup:**
- **2019–22:** federal enforcement weakened (IBAMA fines fell, see below).
- **Operations, staggered:** Yanomami Feb 2023, Munduruku Aug 2023, Kayapó Sep 2024, Sararé Sep 2024. Dates come from pages we opened.

**Ruby's rules for Brazil:** We searched for territories with mining before 2023, no operation in 2022–25, and far from Yanomami. Only small ones pass. Yanomami has no clean twin either, so we use the staggered timing instead.

**What we did:** We measured new mining per territory with Amazon Mining Watch, the same product for every territory and one year longer than MapBiomas (to 2025). Each territory is compared with its **own** operation date. The last panel pools the {{bs_pool_n}} territories with mining and no operation found.

![Brazil: new mining per year in four territories and the no-operation pool, with each territory's own operation date](output/fig_brazil_stagger.png)

**How to read it:** Bars are new mining per year (2025 provisional, hatched). The black line is the territory's own first operation. The dashed line is January 2023, the new federal government. Each panel has its own scale.

**What it shows:**
- **Yanomami** peaked at {{bs_yan_new_ha_2022}} ha in 2022 and fell to {{bs_yan_new_ha_2024}} ha by 2024, after its operation. [[D]]
- **Munduruku** fell already in 2022, before its August 2023 operation. (We only searched for operations from 2021; an earlier one may explain this.) [[D]]
- **Kayapó** fell from 2022 and most in 2024, its operation year. [[D]]
- **Sararé** grew from {{bs_sar_new_ha_2019}} ha (2019) to {{bs_sar_new_ha_2024}} ha (2024), until its own operation. [[D]]
- **No-operation pool:** {{bs_pool_new_ha_2019}} ha (2019) → {{bs_pool_new_ha_2025}} ha (2025, provisional). {{bs_pool_top_share_2023_25:.0%}} of the 2023–25 growth sits in one territory, Aripuanã. [[D]]

**Why it matters:** Brazil echoes Peru in a different way. Mining falls where operations land and grows where they don't. But a national change in 2023 hit every territory at once, so single operations can't be credited.

**Context: the national picture** (unchanged from last night):

![IBAMA fines vs new mining in all indigenous territories](output/fig_brazil_enforcement.png)

**What it shows:** IBAMA fines in the Legal Amazon dropped from {{br_ibama_aml_mean_2015_2018}} to {{br_ibama_aml_mean_2019_2022}} per year in 2019–22. New mining in indigenous lands tripled ({{br_pack_art_add_mean_2016_2018}} → {{br_pack_art_add_mean_2019_2022}} ha per year). [[D]]

**Other sources agree on direction:** MapBiomas per territory (Collection 10.1, to 2024) shows Yanomami falling from {{br_ti_yanomami_add_2022}} ha (2022) to {{br_ti_yanomami_add_2024}} ha (2024). INPE's monthly alerts rose in Yanomami right after the operation: alerts record when a site is *spotted*, and the operation spotted sites. [[D]]

**Code:** `code/brazil_stagger.py` (new), `brazil_deter_all.py` (alerts for every territory), `brazil.py`, `brazil_ibama.py`, `brazil_deter.py`. Operation searches: `docs/overnight/notes/brazil_ti_interventions.csv`.

## 20. What we can claim, and how strongly

| Claim | Label | Evidence for | Evidence against |
|---|---|---|---|
| Tambopata's net new mining fell sharply in 2019–21 | [[D]] | Course table = raster | First-time mining only halved; clearing continued through 2019 |
| New mining moved into the legal corridor, across the road | [[D]] | Raster zones, road bands; MAAP #208 agrees (74%) | Can't show the same people moved; the road was crossed before (2008) |
| Miners returned to old pits in 2023 | [[D]] | Raster accounting; MAAP #193 | Map flicker inflates old-pit counts |
| La Pampa had not run out of gold | [[D]] | Geology: {{gold_broad_lapampasector_depleted_2018:.0%}} mined by 2018 | Coarse map; no gold grade |
| No other Peruvian zone fell like it | [[D]] | Rank 1 of 15 under every model | Only 15 zones |
| Tambopata fell against a rule-based twin abroad | [[D]] | Amanã grew alike until 2018, then kept growing | No clean twin; Brazil's weak enforcement |
| Mercurio caused the 2019–21 fall, roughly 1,450–1,860 ha/yr | [[C]] *conditional* | Two independent comparisons; fake dates small | One targeted zone; spillovers; dredges invisible |
| The effect did not last | [[D]] | 2022–25 gap near zero | 2023 spike everywhere |
| The region mined less | **rejected** | — | First-time mining in Madre de Dios rose {{v2_new_total_2016_18}} → {{v2_new_total_2022_25}} ha/yr |
| Miners now enter the reserve | [[D]] | MapBiomas, MAAP, AMW agree | Small numbers; 2025–26 provisional |
| Brazil: operated territories fell, unoperated grew | [[D]] | AMW, MapBiomas, IBAMA | Munduruku fell before its operation; national change in 2023 |
| Next operation: local fall while present, rebound within ~3 years, no regional fall | [[P]] | Peru pattern, Brazil direction | Two countries, few operations |

**Why it matters:** Grading puts 30% on "analysis and honesty about the claim". One clearly labelled, conditional causal claim with its threats beats a vague one.

## 21. The report draft (the 2-page brief)

**What this is:** the brief as we'd hand it in. Four parts, one figure, every claim labelled. Numbers come from the same `output/numbers.csv`. Print version (two A4 pages for parts 1–4): `docs/brief/BRIEF_DRAFT.html`. Source text: `docs/brief/brief_content.md`.

**What's still open:** team wording of the [[C]] sentence, access dates for references, and the AI appendix (section 23).

{{BRIEF_BODY}}

## 22. Where everything lives

**Run everything:** `uv run python code/main.py`. It takes about a minute and writes every figure, table and number to `output/`.

| Step | Code | Main output |
|---|---|---|
| Checks against publisher numbers | `code/checks.py` | `output/checks.csv` |
| 4–5 Measure + basic comparison | `code/peru.py` | `fig_brief_main.png`, `fig_peru_did_table.csv` |
| 6 Event study + fake places | `code/peru.py` | `fig_peru_event_study.png`, `peru_placebo_in_space.csv` |
| 7 Controls (gold price, trends, size) | `code/peru_models.py` | `fig_peru_models.png`, `peru_models.csv` |
| 8 Ruby's rule-based twin | `code/control_*.py` | `fig_control_*.png`, `control_funnel.csv`, `control_compare.csv` |
| 9 Synthetic twin (add-on) | `code/peru_synth.py` | `fig_peru_synth.png` |
| Robustness (other comparison zones, drop largest) | `code/peru_robust.py` | `peru_robustness.csv` |
| 10 Raster zones, pixel accounting | `code/raster_zones.py` | `fig_v2_zone_map.png`, `data_intermediate/zone_year_v2.csv` |
| 11–13 Corridor, road, old pits | `code/raster_layers.py`, `code/v2_tests.py` | `fig_v2_stream.png`, `fig_v2_road_*.png`, `fig_v2_sankey.png` |
| 14 Quarterly alerts | `code/glad_alerts.py` | `fig_v2_glad_quarterly.png` |
| 15 Gold left | `code/raster_gold.py` | `v2_gold_depletion.csv` |
| 16 Spending, 2012 wave | `code/v2_tests.py` | `fig_v2_enforcement_spending.png` |
| 17 Inside the reserve | `code/peru_anp.py` | `fig_peru_inside_reserves.png` |
| 18 Gold production | `code/peru_production.py` | `fig_peru_production_vs_area.png` |
| 19 Brazil | `code/brazil*.py` | `fig_brazil_stagger.png`, `fig_brazil_*.png` |
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
2. **Agree on the claim wording,** especially the one conditional causal sentence (steps 7–8). It's a team call.
3. **Ruby: check steps 8 and 10.** Step 8 is her twin design (500 m and one-fifth cut-offs). Step 10 is the new zone map: are La Pampa (70.15°–69.80° W) and "across the road" (10 km) drawn right? Should native communities inside the corridor count as legal?
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
| INPE DETER mining alerts (new) | 2019 = {{br_deter_2019_total_wfs_km2:.2f}} km² | {{br_deter_2019_total_dashboard_km2:.2f}} km² | 0.2% off |
| Gold production, BCRP/MINEM (new) | Monthly sums = annual | — | Internal only |
| IBAMA fines (new) | — | No total online | Not checkable |
| World Bank gold price (course data) | Aug 2026 = $4,411/oz | $4,411/oz | Match |
| MapBiomas Amazonía, Collection 6 (new, step 8) | Amazon mining 2023 = 775,746 ha | 0.78 Mha (factsheet p.3) | Match |
| MapBiomas Brazil, Collection 11, mining module (new) | Garimpo 2025 = 445,987 ha | 445,987 ha | Match |
| RAISG protected areas (new, step 8) | 401 areas downloaded | 401 in the service | Match |
| Amazon Mining Watch (step 8, 13) | — | No totals published | Not checkable |

**Decision log** (from `docs/overnight/LOG.md`)

{{DECISIONS_TABLE}}

**Every number** (filterable; from `output/numbers.csv`)

{{NUMBERS_TABLE}}
