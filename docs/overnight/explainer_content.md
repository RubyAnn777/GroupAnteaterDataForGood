<!--
Source of docs/overnight/EXPLAINER.html (the team walkthrough). Build: `uv run python docs/overnight/build_report.py`.
Placeholders {{id}} or {{id:fmt}} come from output/numbers.csv (default ",.0f"; unknown ids fail the build).
Claim tags: [[D]] description, [[P]] prediction, [[C]] causal. Figures ![caption](output/x.png) are embedded.
Sections split on "## ". The first "> " line is the banner. {{BRIEF_BODY}} embeds the 2-page brief draft.
-->

# Mercurio cut new mining where it struck, for three years. The region kept growing.

> A guided walk through the analysis, in plain words. Each step says what we asked, what we did, where the code is, how to read the figure and why it matters. Section 15 holds the report draft. Every number comes from `output/numbers.csv`. Nobody has checked this yet: treat it as a draft.

## 1. The bottom line

**Operation Mercurio worked locally, and only for a while.**

- **During (2019–21):** new mining in the targeted zone fell from {{mean_add_tambopata_2016_18}} to {{mean_add_tambopata_2019_21}} ha per year. Every one of those years was lower than any year from 2011 to 2018. [[D]]
- **Against other Peruvian zones:** no other zone fell like this, with or without controls for the gold price, trends and size. [[D]]
- **Against Ruby's rule-based twin:** the closest match in the whole Amazon (Amanã, Brazil) grew like Tambopata until 2018. In 2019–21, Tambopata added mining at {{ctl_relaxed_during_ratio:.0%}} of the twin's pace. [[D]]
- **After (2022–25):** Tambopata came back to {{mean_add_tambopata_2022_25}} ha per year. The extra fall is gone. [[D]]
- **Around it:** Madre de Dios as a whole did not fall: {{mean_add_mdd_total_2016_18}} → {{mean_add_mdd_total_2019_21}} → {{mean_add_mdd_total_2022_25}} ha per year. [[D]]
- **Inside the reserve:** small, but new in 2025 (+{{anp_tam_nr_addition_2025}} ha). [[D]]
- **Brazil:** territories fell after operations, while territories without one grew. But the timing is not clean enough to credit single operations. [[D]]

**Can we say Mercurio *caused* the fall?** Cautiously, yes, for 2019–21 only. Two independent comparisons agree: 14 other Peruvian zones (steps 6–7) and a twin picked by rules abroad (step 8). One targeted zone still leaves room for luck or a local shock. We label it a **conditional causal claim**. [[C]]

**Why it matters:** FZS should expect enforcement to work **while it lasts** and **where it lands**. It should not expect the region to mine less.

> **One correction from last night still stands.** "Pre-trends fail" came from one odd year: 2016 ({{tam_add_2016}} ha, then {{tam_add_2017}} ha in 2017). Averaged over several years, the fake-date test passes (step 7).

## 2. How to read this page

**Steps 3–13 walk through the analysis.** Each answers one question:

- **3** What is the question, and where?
- **4** What exactly do we measure?
- **5** The basic comparison
- **6** Is the fall special, or just noise?
- **7** Controls: gold price, trends, size
- **8** Ruby's idea: one real twin, picked by rules *(new)*
- **9** Add-on: a synthetic twin
- **10** Where did the mining go?
- **11** Did it move into the reserve?
- **12** A cross-check with gold production
- **13** Brazil: staggered operations *(rebuilt)*

Then: what we can claim (14), **the report draft (15)**, where everything lives (16), what's on you (17), appendix (18).

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

## 10. Where did the mining go? Not clear, but the region did not fall

**Question:** If miners left La Pampa, did total mining fall, or did they move?

**What we did:** We added up the zones and compared them with the whole department.

![Displacement: three buffer zones stacked vs the Madre de Dios total and the rest](output/fig_peru_displacement.png)

**How to read it:**
- **Top:** stacked bars for the three buffer zones; the black line is their sum.
- **Bottom:** the whole department (grey) and everything outside the buffer zones (purple).

**What it shows:**
- The three buffer zones together fell by {{displacement_three_bz_sum_chg_2019_21_vs_2016_18}} ha per year during 2019–21. [[D]]
- The rest of the department rose from {{mean_add_rest_mdd_2016_18}} to {{mean_add_rest_mdd_2019_21}} ha per year, then to {{mean_add_rest_mdd_2022_25}}. [[D]]
- This *fits* displacement. It fits the gold price, COVID and legal-corridor growth just as well. [[D]]

**A second satellite product disagrees:**

![Amazon Mining Watch: new mining area by zone and year](output/fig_spatial_zones.png)

**What it shows:** Amazon Mining Watch shows new mining in the legal corridor *falling*, from {{spz_corridor_ha_2019_21}} ha (2019–21) to {{spz_corridor_ha_2022_24}} ha (2022–24). The regional rise rests on MapBiomas alone. [[D]]

![New mining area by distance ring around La Pampa (Amazon Mining Watch)](output/fig_spatial_rings.png)

**What it shows:** Within 50 km of La Pampa, new mining splits across distance rings about the same way before and after. There's no visible "push outward". [[D]]

**Why it matters:**
- We can't prove displacement, but we can rule out one thing: **the region did not get less mining.**
- An operation that saves one zone may not save the landscape.

**Code:** `code/peru.py` (`fig_displacement`), `code/spatial_zones.py`, `code/spatial.py`.

## 11. Did miners move into the reserve itself? Starting in 2025, yes

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

## 12. A cross-check: declared gold production collapsed while mapped mining grew

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

## 13. Brazil: mining fell where operations came and grew where none did. The timing is messy.

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

## 14. What we can claim, and how strongly

| Claim | Label | Evidence for | Evidence against |
|---|---|---|---|
| Tambopata's new mining fell sharply in 2019–21 | [[D]] | Both satellite products | AMW sees the fall start later |
| No other Peruvian zone fell like it | [[D]] | Rank 1 of 15 under every model | Only 15 zones |
| Tambopata fell against a rule-based twin abroad | [[D]] | Amanã grew alike until 2018, then kept growing | No clean twin; Brazil's weak enforcement |
| Mercurio caused the 2019–21 fall, roughly 1,450–1,860 ha/yr | [[C]] *conditional* | Two independent comparisons; fake dates small | One targeted zone; spillovers; dredges invisible |
| The effect did not last | [[D]] | 2022–25 gap near zero | 2023 spike everywhere |
| Mining moved to the rest of Madre de Dios | **not claimed** | MapBiomas rise | AMW shows a fall; gold price, COVID, legal corridor |
| Miners now enter the reserve | [[D]] | MapBiomas, MAAP, AMW agree | Small numbers; 2025–26 provisional |
| Brazil: operated territories fell, unoperated grew | [[D]] | AMW, MapBiomas, IBAMA | Munduruku fell before its operation; national change in 2023 |
| Next operation: local fall while present, rebound within ~3 years, no regional fall | [[P]] | Peru pattern, Brazil direction | Two countries, few operations |

**Why it matters:** Grading puts 30% on "analysis and honesty about the claim". One clearly labelled, conditional causal claim with its threats beats a vague one.

## 15. The report draft (the 2-page brief)

**What this is:** the brief as we'd hand it in. Four parts, one figure, every claim labelled. Numbers come from the same `output/numbers.csv`. Print version (two A4 pages for parts 1–4): `docs/brief/BRIEF_DRAFT.html`. Source text: `docs/brief/brief_content.md`.

**What's still open:** team wording of the [[C]] sentence, access dates for references, and the AI appendix (section 17).

{{BRIEF_BODY}}

## 16. Where everything lives

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
| 10 Displacement + maps | `code/peru.py`, `code/spatial*.py` | `fig_peru_displacement.png`, `fig_spatial_*.png` |
| 11 Inside the reserve | `code/peru_anp.py` | `fig_peru_inside_reserves.png` |
| 12 Gold production | `code/peru_production.py` | `fig_peru_production_vs_area.png` |
| 13 Brazil | `code/brazil*.py` | `fig_brazil_stagger.png`, `fig_brazil_*.png` |
| The brief's figure | `code/brief_figure.py` | `fig_brief_main.png` |
| Every number | all of the above | `output/numbers.csv` |

**Other files:**
- **Brief draft:** `docs/brief/BRIEF_DRAFT.md` and `.html`.
- **Operation searches:** `docs/overnight/notes/control_interventions.md` and `brazil_data_and_operations.md`.
- **Log and decisions:** `docs/overnight/LOG.md`. **Data log:** `DOWNLOAD_LOG.csv`.

**Big raw files are git-ignored** (Amazon Mining Watch, RAISG, MapBiomas Amazonía, FUNAI). The run then uses the small files in `data_intermediate/`. Download links are in `DOWNLOAD_LOG.csv`.

## 17. What's blocked on you

**Must do (only a human can):**

1. **Share this page** with the team. It's private until you click Share.
2. **Agree on the claim wording,** especially the one conditional causal sentence (steps 7–8). It's a team call.
3. **Show Ruby step 8.** It's her design; she should check the four rules and the 500 m and one-fifth cut-offs.
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

## 18. Appendix: data, decisions and every number

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
