<!--
Source of docs/walkthrough/EXPLAINER.html (the team walkthrough). Build: `uv run python docs/walkthrough/build_report.py`.
Placeholders {{id}} or {{id:fmt}} come from output/numbers.csv (default ",.0f"; unknown ids fail the build).
Claim tags: [[D]] description, [[P]] prediction, [[C]] causal.

Plan v3 (docs/PLAN_v3.md, code/definitions.py), rewritten 2026-10-15:
  ONE measure: net mining additions (ha/yr) = new land + re-mined − stopped, MapBiomas Peru Collection 4 rasters,
    our pixel accounting. Every number sentence names measure, zone and period. Other products (AMW, GLAD,
    MapBiomas Amazonía/Brazil) are labelled as such and stay out of headline claims.
  ONE zone registry (official buffer zones whole, Kotsimba inside the Tambopata buffer zone as a tenure tag).
  ONE treatment: start of Mercurio, Feb 2019; first treated year 2019; reference 2018; 2022–25 = "later years".
  The brief (docs/brief/brief_content.md) is the reference for wording and for the one conditional [C] sentence.
Story order (2026-10-15) follows the talk, docs/presentation/STORYLINE.md v3.1: question → place → it fell → what fell
  → where it went → across the road → money and gold → how it came back → inside the reserve → is it causal → limits
  → for FZS → team corner. Main time series = Tambopata buffer zone; La Pampa only for the map and across the road.
  Two corridors, never mixed: "corridor across the road" (D.L. 1100 land ≤ 10 km north of the highway at La Pampa's
  longitudes) and "legal mining corridor" (all D.L. 1100 land). One causal range: M1 to 2×2 (2014–18 baseline).

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

# Mining in the target fell, rose across the road, then came back

> What Operation Mercurio's start in February 2019 went with in gold mining in Madre de Dios, Peru, and what FZS should expect around and after an operation. Team walkthrough in the order of the talk: the story first, every analysis behind it. One measure throughout: **net mining additions** (new land + re-mined − stopped, ha/yr, MapBiomas Peru Collection 4). Every number comes from `output/numbers.csv`.

:::stats
{{tambopata_bz_pre_net}} → {{tambopata_bz_during_net}} || ha/yr of net mining additions, Tambopata buffer zone, 2016–18 vs 2019–21: it fell
{{tambopata_bz_stopped_share_of_fall_min:.0%}}–{{tambopata_bz_stopped_share_of_fall_max:.0%}} || of that fall is land stopping (pits leaving the mining class); the rest, fewer new pits
{{corridor_across_pre_net}} → {{corridor_across_during_net}} || ha/yr of net additions in the corridor across the road, 2016–18 vs 2019–21: it rose
{{tambopata_bz_later_net}} || ha/yr of net additions, Tambopata buffer zone, 2022–25 ({{tambopata_bz_later_ex2023_net}} without 2023): it came back
:::

@part The story

## The story in one minute | Mining fell in the target, rose next door, came back

**After Mercurio began in February 2019, net mining additions in the Tambopata buffer zone collapsed for three years. A quarter to a half of that fall was mined land leaving the mining class; the rest was fewer new pits. Next door, net additions rose; the region kept growing; in the later years the target came back, largely on old pits.** [[D]]

:::beats
It fell || Tambopata buffer zone net additions: {{tambopata_bz_pre_net}} → {{tambopata_bz_during_net}} ha/yr (2016–18 vs 2019–21), while the less-treated Amarakaeri buffer zone rose {{amarakaeri_bz_pre_net}} → {{amarakaeri_bz_during_net}} ha/yr. || #it-fell
What fell || In 2019 new pits kept opening ({{tambopata_bz_2019_new}} ha of new land vs {{tambopata_bz_2018_new}} in 2018) while {{tambopata_bz_2019_stopped}} ha stopped. Stopping explains {{tambopata_bz_stopped_share_of_fall_min:.0%}}–{{tambopata_bz_stopped_share_of_fall_max:.0%}} of the 2016–18 to 2019–21 fall. || #what-fell
Where it went || All of Madre de Dios: {{mdd_pre_net}} → {{mdd_during_net}} → {{mdd_later_net}} ha/yr (2016–18 → 2019–21 → 2022–25); the legal mining corridor's share rose from {{v2_corridor_share_pre_net:.0%}} to {{v2_corridor_share_during_net:.0%}}. || #where-it-went
Across the road || Net additions in the corridor across the road rose from {{corridor_across_pre_net}} to {{corridor_across_during_net}} ha/yr (2016–18 vs 2019–21). || #across-the-road
Money and gold || Enforcement money booked in Madre de Dios peaked in 2019 and faded; the gold price rose {{gold_price_ratio_2025_2018:.1f}}-fold from 2018 to 2025. || #money-and-gold
How it came back || The Tambopata buffer zone averaged {{tambopata_bz_later_net}} ha/yr in 2022–25 ({{tambopata_bz_later_ex2023_net}} without 2023); re-mined land was {{tambopata_bz_later_remined_share_added:.0%}} of added land ({{tambopata_bz_later_ex2023_remined_share_added:.0%}} without 2023). || #how-it-came-back
Inside the reserve || Net additions inside Tambopata National Reserve: +{{tambopata_nr_2025_net}} ha in 2025. || #inside-the-reserve
:::

**Is it causal?** Only conditionally. *If* the other Peruvian buffer zones show what the Tambopata buffer zone would otherwise have done, Mercurio and the operations that followed lowered its net mining additions by about {{model_m1_during_net:,.0f|abs}} to {{did_base2014_net:,.0f|abs}} ha/yr in 2019–21 (Tambopata vs 14 other Peruvian buffer zones, or vs Amarakaeri alone on a 2014–18 baseline). [[C]] In hectares the fall stands out; for its size it does not ({{model_m4_rank:.0f}}rd–{{placebo_space_rank_scaled:.0f}}th of 7 depending on the scaling). Read it as an upper bound ([The claim](#the-claim)).

**Why it matters:** we expect an operation to buy a pause, not an end. [[P]] Part of the pause is idle pits that can restart, and new pits opened nearby in the first year. FZS should plan for the ring around the operation and for the years after it.

## The brief | Four parts, one figure, one conditional causal sentence

**The 2-page brief tells the story above in the course's four parts.** The brief has its own page: {{BRIEF_LINK}}. Where this page and the brief differ, the brief wins.

| Brief part | What it says | Evidence on this page |
|---|---|---|
| **1. The question** | FZS pays for enforcement. What happens in the target, and around it, when an operation ends? | [The question](#the-question), [The places](#the-places) |
| **2. Data** | Net mining additions from MapBiomas Peru Collection 4 rasters; one check per dataset | [The places](#the-places), [Appendix](#appendix) |
| **3. Findings** | Net additions collapsed in the target, a quarter to a half of it land stopping; net additions rose across the road; the department never fell; the target came back on old pits. One conditional causal claim. | [It fell](#it-fell) to [The claim](#the-claim) |
| **4. What FZS can do** | Stay after the sweep, watch a ring around each operation, guard the reserve's edge and river. Satellites miss dredges and mercury. | [For FZS](#for-fzs), [Limits](#limits) |

:::fig output/fig_brief_main.png
read: Top: net mining additions (black line) and their three parts (bars: new land brown, re-mined amber, stopped teal below zero), Tambopata buffer zone, 2014–2025. Bottom: net additions in Madre de Dios by area, period means.
take: The Tambopata buffer zone fell from {{fig_brief_tbz_net_pre}} to {{fig_brief_tbz_net_during}} ha/yr (2016–18 vs 2019–21) and came back to {{fig_brief_tbz_net_later}} (2022–25); the legal mining corridor outside buffer zones rose from {{fig_brief_cor_net_pre}} to {{fig_brief_cor_net_during}} and {{fig_brief_cor_net_later}} ha/yr. This is the brief's one figure.
:::

:::more How to read this page: claim labels and a plain-word glossary
**Claim labels.** [[D]] what happened · [[P]] what we expect next time · [[C]] what caused it. The course grades honesty about claims (30%), so every claim carries one.

**Each chapter has two layers.** The visible layer is the claim, the figure and the key numbers. "Go deeper" holds methods, tables, tests, caveats and code.

| Term | Meaning here |
|---|---|
| **Net mining additions** | Mining area this year minus last year, per zone, ha/yr. **The one outcome on this page.** It equals new land + re-mined − stopped. |
| **New land** | Pixels mapped as mining for the first time since 1985 (first-time mining). |
| **Re-mined** | Pixels mapped as mining now, not last year, but in some earlier year (old pits worked again). |
| **Stopped** | Pixels mapped as mining last year and not this year: flooded, regrowing, bare, or reclassified. Some come back within two years. |
| **Tambopata buffer zone** | The official SERNANP buffer zone of Tambopata National Reserve, whole (incl. the Kotsimba native community, a tenure tag). The treated unit and the zone of every main time series. |
| **La Pampa sector** | The part of the Tambopata buffer zone between 70.15° and 69.80° W. Our boundary; no official one exists. Used for the map and the road. |
| **Legal mining corridor** | All land where small-scale mining can be permitted under Legislative Decree (D.L.) 1100 of 2012, about 4,983 km². |
| **Corridor across the road** | The part of the legal mining corridor within 10 km north of the Interoceanic Highway, at La Pampa's longitudes, outside every buffer zone. |
| **Amarakaeri buffer zone** | The neighbouring buffer zone, whole. "Less treated": Mercurio II covered all of Madre de Dios. |
| **Later years** | 2022–25. Reported with and without 2023, a spike year only MapBiomas shows. Never "after enforcement ended". |
| **Fixed effects** | A regression that removes each zone's normal level and each year's shock *common to all zones*. Shocks that hit zones unequally (gold price, COVID) are not removed. |
| **Fake date / fake place** | Pretend the operation happened earlier or elsewhere. A real effect should stand out. |
| **Raw vs scaled rank** | Raw: rank of the hectare change among zones (measures size too). Scaled: the change divided by each zone's normal pre-2019 additions. |
| **Rule-based twin** | An existing area picked by fixed rules to show what might have happened without the operation (Ruby's design). |
| **Other products** | **AMW** = Amazon Mining Watch (Earth Genome's machine-learning map of gold-mining scars, 480-m squares, no "stopped" state); **GLAD-L** = the University of Maryland's Landsat forest-loss alerts. Labelled wherever used; never net additions. |
:::

@part Question and place

## The question | FZS pays for operations. What happens when one ends?

**FZS supports SERNANP's operations against alluvial gold mining around Tambopata and Bahuaja-Sonene. Operations are costly and temporary. So: what happens in the targeted area, and around it, when one ends?** Mining could stop (**deterrence**), move (**displacement**) or return (**delay**). Inside the target the three look alike, so we need comparisons.

**Where you mine decides whether it's a crime.** La Pampa is illegal by location; the corridor across the road is not. Moving 2 km north turns a crime into an administrative problem.

- **Illegal (D.L. 1105, 2012):** mining in a prohibited zone or with banned equipment. A crime.
- **Informal:** the same failings inside the legal mining corridor (D.L. 1100, 2012), by someone in REINFO, the registry of miners in formalization. Not a crime.
- **Formalization barely happens:** 9,592 Madre de Dios miners were in formalization, but only 145 were fully formalized (MINAM, 2021, pp. 55–56; two separate counts).
- **Taxes are near zero:** 0% royalty for small producers (Ley 28258, Art. 5); raw gold VAT-exempt, 1.5% withheld on sale.

**Why it matters:** an operation raises the cost of mining in one place, while the legal mining corridor next door stays cheap. That alone predicts more mining across the road. [[P]]

:::more The legal detail, who mines, and FZS's role
**The legal mining corridor (D.L. 1100, 2012):** about 4,983 km² where small-scale mining can be permitted. Outside it, no concessions are granted. La Pampa covers about 1,241 km² (MINAM 2016). Congress has extended REINFO again and again, now to 31 December 2026.

**How MAAP grades illegality (MAAP #235):** Very high = inside a protected area; High = outside any concession; Medium = inside a concession not verified as active; Low = inside an active concession.

**Who mines:** about 46,605 artisanal miners in Madre de Dios, of whom 31,390 informal and 9,323 illegal (ACCA & USAID 2022). About 35% of the department's population is directly linked to mining.

**What each zone costs a miner:**

| Zone | Status | Main cost |
|---|---|---|
| La Pampa sector (buffer zone) | illegal | enforcement risk: seizure, eviction, prison |
| Corridor across the road | legal if titled | taxes, permits, competition for space |
| Amarakaeri buffer zone | illegal | enforcement risk (Mercurio II covered it) |
| Tambopata reserve | illegal, highest risk | enforcement; reached by river, far from the highway |
| Native communities | depends on concession | community consent; mixed legality |

**Fuel:** tax-exempt in the Amazon; 72% of that benefit went to illegal mining (IPE).

**Who enforces, and when:** the dated timeline is in [Money and gold](#money-and-gold).

**FZS's role:** FZS supports SERNANP's law-enforcement operations, ranger control posts and patrols in the Tambopata–Bahuaja-Sonene landscape. So FZS is part of the enforcement we study.

**Sources:** `docs/walkthrough/notes/qualitative_background.md` (every item with a link and a quote).
:::

## The places | La Pampa sits one road away from legal mining land

**One mining belt, split by the Interoceanic Highway: La Pampa on the buffer-zone side, the corridor across the road on the legal side, the reserve just south.** We cut one satellite map into one set of zones, used by every analysis: the official buffer zones kept whole, the La Pampa sector inside the Tambopata buffer zone, the corridor across the road, the rest of the legal mining corridor, native communities, the reserve and the rest of Madre de Dios. [[D]]

:::fig output/fig_v2_zone_map.png
read: Coloured areas are registry zones around La Pampa; black pixels were mapped as mining at least once since 1985. The thick line is the Interoceanic Highway; dotted lines mark La Pampa's longitudes (70.15–69.80 W). The pink outline is Kotsimba, a native community inside the buffer zone (a tenure tag, not a separate zone).
take: La Pampa and the corridor across the road share one mining belt; only the road and the law separate them.
:::

**Why it matters:** the same land is counted the same way in every chart, table and model. The v2 pages used two different "Tambopata buffer zones" (statistics workbook vs raster); v3 uses one.

:::more Zone profiles, checks and boundary choices
**What each zone offers a miner** (1-km cells of the study window, majority zone):

| Zone | Status | km to highway | km to river | Gold-bearing land | Gold-bearing land mined by 2018 |
|---|---|---:|---:|---:|---:|
| La Pampa sector | illegal | {{zp_lapampa_km_to_highway:.1f}} | {{zp_lapampa_km_to_river:.1f}} | {{zp_lapampa_gold_bearing_share:.0%}} | {{gold_broad_lapampa_depleted_2018:.0%}} |
| Corridor across the road | legal if titled | {{zp_corridor_across_km_to_highway:.1f}} | {{zp_corridor_across_km_to_river:.1f}} | {{zp_corridor_across_gold_bearing_share:.0%}} | {{gold_broad_corridor_across_depleted_2018:.0%}} |
| Rest of the legal mining corridor | legal if titled | {{zp_corridor_rest_km_to_highway:.1f}} | {{zp_corridor_rest_km_to_river:.1f}} | {{zp_corridor_rest_gold_bearing_share:.0%}} | {{gold_broad_corridor_rest_depleted_2018:.0%}} |
| Amarakaeri buffer zone | illegal | {{zp_amarakaeri_bz_km_to_highway:.1f}} | {{zp_amarakaeri_bz_km_to_river:.1f}} | {{zp_amarakaeri_bz_gold_bearing_share:.0%}} | {{gold_broad_amarakaeri_bz_depleted_2018:.0%}} |
| Reserves and parks | illegal | {{zp_protected_km_to_highway:.1f}} | {{zp_protected_km_to_river:.1f}} | {{zp_protected_gold_bearing_share:.0%}} | — |

- **Data:** MapBiomas Peru Collection 4 annual maps, 1985–2025, 30-m pixels (class 4.2 Minería: all mining, legal and illegal).
- **Checks (ours vs publisher, mining stock 2025):** Tambopata buffer zone {{chk_tbz_2025_ours}} vs {{chk_tbz_2025_pub}} ha; Tambopata reserve {{chk_tnr_2025_ours:,.1f}} vs {{chk_tnr_2025_pub}} ha; Madre de Dios {{chk_mdd_2025_ours}} vs {{chk_mdd_2025_pub}} ha.
- **Order of precedence:** where official buffer zones overlap, the land goes to Tambopata first, then Amarakaeri, as MapBiomas does. Corridor and community land *inside* a buffer zone stays in that zone, with a tenure tag.
- **Boundary choice:** a narrower or wider La Pampa window gives the same picture: net additions in the La Pampa sector change by {{t4_lapampa_narrow_change_net:.0%}} (narrow) or {{t4_lapampa_wide_change_net:.0%}} (wide), 2016–18 to 2019–21, vs {{t4_lapampa_main_change_net:.0%}} for the main window.
- **Boundaries change:** the current Tambopata buffer zone dates from {{t6_bz_approved_tambopata:.0f}}, Amarakaeri's from {{t6_bz_approved_amarakaeri:.0f}}; the legal mining corridor from 2012. We apply today's boundaries to every year, as MapBiomas does.
- **The statistics workbook** (the course tables) is now only a reconciliation check: the card's 1,640 → 163 ha/yr for the Tambopata buffer zone reproduces in `code/checks.py`.

**Code:** `code/definitions.py` (zones, treatment, periods), `code/raster_zones.py`, `code/zonedata.py`, `code/v2_extra.py` (zone profile).
:::

@part What happened

## It fell | Target's net mining fell {{tambopata_bz_pre_net}} → {{tambopata_bz_during_net}} ha/yr

**Net mining additions in the Tambopata buffer zone fell from {{tambopata_bz_pre_net}} ha/yr (2016–18) to {{tambopata_bz_during_net}} ha/yr (2019–21). Over the same years the less-treated Amarakaeri buffer zone rose from {{amarakaeri_bz_pre_net}} to {{amarakaeri_bz_during_net}} ha/yr.** [[D]]

| Net mining additions, ha/yr | 2016–18 | 2019–21 | 2022–25 | 2022–25 without 2023 |
|---|---:|---:|---:|---:|
| Tambopata buffer zone (target) | {{tambopata_bz_pre_net}} | {{tambopata_bz_during_net}} | {{tambopata_bz_later_net}} | {{tambopata_bz_later_ex2023_net}} |
| Amarakaeri buffer zone (less treated) | {{amarakaeri_bz_pre_net}} | {{amarakaeri_bz_during_net}} | {{amarakaeri_bz_later_net}} | {{amarakaeri_bz_later_ex2023_net}} |

- **The course's 2×2 (2016–18 baseline):** the target's change minus Amarakaeri's change is **{{did_main_net}} ha/yr**, 2016–18 vs 2019–21. A fake start in 2016 gives {{did_placebo_net:+,.0f}} ha/yr. [[D]]
- **Every year, not just the average:** each 2019–21 year (at most {{tambopata_bz_net_max_during}} ha) was below every 2011–18 year (at least {{tambopata_bz_net_min_2011_18}} ha), Tambopata buffer zone. [[D]]
- **Short-lived:** by 2022–25 the target was back at {{tambopata_bz_later_net}} ha/yr ({{tambopata_bz_later_ex2023_net}} without 2023). [[D]]

**Why it matters:** the fall was real and large, and it lasted three years. What it was made of decides what FZS should expect next time.

## What fell | In 2019, new pits kept opening while old ones went quiet

**Net additions = new land + re-mined − stopped. In the Tambopata buffer zone, 2016–18 to 2019–21, new land fell and stopped land nearly doubled; in the less-treated Amarakaeri buffer zone stopped land barely moved.** [[D]]

| Net mining additions and parts, ha/yr | Tambopata BZ 2016–18 | Tambopata BZ 2019–21 | Amarakaeri BZ 2016–18 | Amarakaeri BZ 2019–21 |
|---|---:|---:|---:|---:|
| New land | {{tambopata_bz_pre_new}} | {{tambopata_bz_during_new}} | {{amarakaeri_bz_pre_new}} | {{amarakaeri_bz_during_new}} |
| + Re-mined | {{tambopata_bz_pre_remined}} | {{tambopata_bz_during_remined}} | {{amarakaeri_bz_pre_remined}} | {{amarakaeri_bz_during_remined}} |
| − Stopped | {{tambopata_bz_pre_stopped}} | {{tambopata_bz_during_stopped}} | {{amarakaeri_bz_pre_stopped}} | {{amarakaeri_bz_during_stopped}} |
| **= Net additions** | **{{tambopata_bz_pre_net}}** | **{{tambopata_bz_during_net}}** | **{{amarakaeri_bz_pre_net}}** | **{{amarakaeri_bz_during_net}}** |

:::fig output/fig_peru_additions.png
read: Top: net mining additions (black line) and their parts per year in the Tambopata buffer zone, 2014–2025: new land (brown) and re-mined land (amber) above zero, stopped land (teal) below zero. Middle and bottom: net additions in neighbouring zones and in all of Madre de Dios, for context.
take: In 2019 the stopped bar is the deepest of the series while new land is still high; new land shrinks only in 2020–21.
:::

- **2019, Tambopata buffer zone:** new land {{tambopata_bz_2019_new}} ha (2018: {{tambopata_bz_2018_new}}), stopped {{tambopata_bz_2019_stopped}} ha (2018: {{tambopata_bz_2018_stopped}}), net additions {{tambopata_bz_2019_net}} ha (2018: {{tambopata_bz_2018_net}}). New land fell only in 2020 ({{tambopata_bz_2020_new}} ha) and 2021 ({{tambopata_bz_2021_new}} ha), the COVID years. [[D]]
- **Share of the fall that is stopping:** {{tambopata_bz_stopped_share_of_fall_min:.0%}}–{{tambopata_bz_stopped_share_of_fall_max:.0%}} of the fall in net additions, Tambopata buffer zone, 2016–18 to 2019–21, depending on how we count it (four ways, below). Of the Tambopata buffer zone's excess stopping in 2019–21 (above its 2016–18 rate), {{tambopata_bz_excess_stopped_share_in_2019:.0%}} came in 2019. [[D]]
- **Specific to the target:** Amarakaeri's stopped land went {{amarakaeri_bz_pre_stopped}} → {{amarakaeri_bz_during_stopped}} ha/yr over the same years. [[D]]
- **What the stopped land became, Tambopata buffer zone, 2019–21:** {{tambopata_bz_during_stopped_share_to_water:.0%}} water, {{tambopata_bz_during_stopped_share_to_forest:.0%}} forest, {{tambopata_bz_during_stopped_share_to_bare:.0%}} bare ground (sand banks); {{tambopata_bz_during_stopped_share_back_within_2y:.0%}} was mapped as mining again within two years (2016–18: {{tambopata_bz_pre_stopped_share_back_within_2y:.0%}}). [[D]]
- **An independent study agrees:** Dethier et al. (2023, *Conservation Letters*; abstract), using mining ponds, report 70–90% abandonment in the targeted zones and faster mining just outside them.

**Why it matters:** net additions can fall while the people and machines stay nearby. Stopped pits are flooded or idle pits that can restart, and in 2019 new pits kept opening. So the next operation needs a ring of near-real-time forest-loss alerts around it, not only patrols on the target. [[P]]

:::more How we count the stopped share, its caveats, and the depletion check
**Four ways to count the stopped share of the fall** (Tambopata buffer zone, 2016–18 to 2019–21):

| Variant | Stopped share of the fall |
|---|---:|
| Raw change in stopped land | {{tambopata_bz_stopped_share_of_fall_raw:.0%}} |
| Without land mapped as mining again within two years | {{tambopata_bz_stopped_share_of_fall_excl_back2y:.0%}} |
| Only stopping above the zone's 2016–18 stopping rate | {{tambopata_bz_stopped_share_of_fall_excess_rate:.0%}} |
| Relative to Amarakaeri (difference in differences) | {{tambopata_bz_stopped_share_of_fall_did:.0%}} |

- **The parts add up:** in the 2×2 against Amarakaeri (2016–18 baseline), the net gap ({{did_main_net}} ha/yr) splits into new land {{did_main_new}}, re-mined {{did_main_remined:+,.0f}} and stopped {{did_main_stopped:+,.0f}} ha/yr (stopped counts with a minus sign).
- **Stopped is not "abandoned":** a pixel leaves the mining class when it floods, regrows, turns to bare sand, or flickers in the classification. Part comes back within two years. We did not check images (plan v3, V3-5).
- **Do not compare later years' destinations:** the water share of stopped land collapses in 2023–25 in every zone, an end-of-series effect of the map. Shares for 2022–25 are not comparable with earlier periods.
- **Depletion, at cell level:** the most-mined third of La Pampa's 1-km cells was {{st_lp_tq_high_share18:.0%}} mined by 2018. The La Pampa sector's hazard of new land on not-yet-mined land fell from {{st_hazard_lapampa_pre_long:.2f}}% a year (2014–18) to {{st_hazard_lapampa_during:.2f}}% a year (2019–21), but per cell on an at-risk basis the change is {{st_hazard_ols_lapampa_during:+.2f}} points (p = {{st_hazard_ols_lapampa_during_p:.2f}}). Part of the fall in new land is pits running out of room.

:::fig output/fig_v2_parts_by_zone.png
read: Net mining additions (black line) and their parts per year, 2010–2025, in four zones of Madre de Dios, each on its own scale: new land (brown) and re-mined land (amber) above zero, stopped land (teal) below zero. Shaded: 2019–21.
take: In the La Pampa sector the teal bar is deepest in 2019, while new land is still high. In the corridor across the road and the rest of the legal mining corridor, net additions rise in the same years.
:::

**Code:** `code/raster_zones.py` (parts and destinations), `code/definitions.py` (OUTCOME), `code/v2_stats.py` (hazard).
:::

:::more Timing inside 2019: La Pampa, forest-loss alerts and Sentinel-2
**The La Pampa sector, within the Tambopata buffer zone:** net additions fell from {{lapampa_2018_net}} ha (2018) to {{lapampa_2019_net}} ha (2019), but new land fell only from {{lapampa_2018_new}} to {{lapampa_2019_new}} ha; {{lapampa_2019_stopped}} ha stopped. The share of the previous year's mining area that stopped rose from {{lapampa_stopping_rate_pre:.0%}} a year (2016–18) to {{lapampa_stopping_rate_2019:.0%}} (2019). La Pampa's own stopped land, 2019–21: {{lapampa_during_stopped_share_to_water:.0%}} became water, {{lapampa_during_stopped_share_back_within_2y:.0%}} was mined again within two years. [[D]]

:::fig output/fig_v2_glad_quarterly.png
read: Another measure: GLAD-L forest-loss alerts (University of Maryland, Landsat) per quarter, counted only on land MapBiomas maps as mining by the next year, four zones, 2017–2026. Alert area is a timing signal, not net additions.
take: La Pampa's alerts stayed high through 2019 and nearly stopped in 2021–22; in the corridor across the road they rose from mid-2019.
:::

- **GLAD-L alerts on mining land, La Pampa sector:** {{glad_mining_lapampasector_2017}} ha (2017), {{glad_mining_lapampasector_2018}} (2018), **{{glad_mining_lapampasector_2019}} (2019)**, {{glad_mining_lapampasector_2020}} (2020), {{glad_mining_lapampasector_2021}} (2021). Another measure. [[D]]
- **Corridor across the road (GLAD-L):** {{glad_mining_corridoracrossther_2018}} ha (2018) → {{glad_mining_corridoracrossther_2019}} (2019) → {{glad_mining_corridoracrossther_2020}} (2020). [[D]]
- **Per 1-km cell, La Pampa sector, 2019 vs 2014–18:** net additions {{st_event_lapampa_2019_net:+.2f}} ha per cell (p = {{st_event_lapampa_2019_net_p:.2f}}), new land {{st_event_lapampa_2019_new:+.2f}}, stopped {{st_event_lapampa_2019_stopped:+.2f}}. [[D]]
- **Sentinel-2 alerts** (every 5 days) in western La Pampa: {{s2_lp_west_2019_mar_sep_ha}} ha in March–September 2019 ({{s2_lp_west_2019_aug_ha}} ha in August alone), vs {{s2_lp_west_2020_mar_sep_ha}} ha in the same months of 2020. So 2019 clearing was real, not cloud delay.
- **Caveats:** clouds bunch alerts in the dry season, so compare the same quarter across years. The GLAD data version changes in 2021. Alerts need standing forest, so re-mined pits never show.

**Code:** `code/glad_alerts.py`.
:::

## Where it went | The region kept growing, mostly on legal-corridor land

**Madre de Dios never fell: net additions went {{mdd_pre_net}} → {{mdd_during_net}} → {{mdd_later_net}} ha/yr (2016–18 → 2019–21 → 2022–25; {{mdd_later_ex2023_net}} without 2023). The share of those net additions on legal-mining-corridor land rose from {{v2_corridor_share_pre_net:.0%}} (2016–18) to {{v2_corridor_share_during_net:.0%}} (2019–21) and {{v2_corridor_share_later_net:.0%}} (2022–25; {{v2_corridor_share_later_ex2023_net:.0%}} without 2023).** [[D]]

**Corridor share** = the department's net additions on land of the legal mining corridor (D.L. 1100 tenure, in any zone, native communities excluded), divided by all of the department's net additions, each summed over the period.

:::fig output/fig_v2_stream.png
read: Net mining additions in Madre de Dios each year, ha, stacked by registry zone; numbers are yearly totals. Shaded: 2019–21. Lines mark Mercurio (solid) and the context events (dashed).
take: The orange La Pampa band nearly vanishes in 2019–21 while the light-blue rest of the legal mining corridor grows; the total keeps growing.
:::

Net mining additions, ha/yr, 2016–18 → 2019–21 → 2022–25 (without 2023 in brackets): [[D]]

- **Tambopata buffer zone (target):** {{tambopata_bz_pre_net}} → {{tambopata_bz_during_net}} → {{tambopata_bz_later_net}} ({{tambopata_bz_later_ex2023_net}}).
- **Corridor across the road:** {{corridor_across_pre_net}} → {{corridor_across_during_net}} → {{corridor_across_later_net}} ({{corridor_across_later_ex2023_net}}).
- **Rest of the legal mining corridor:** {{corridor_rest_pre_net}} → {{corridor_rest_during_net}} → {{corridor_rest_later_net}} ({{corridor_rest_later_ex2023_net}}).
- **Native communities:** {{communities_pre_net}} → {{communities_during_net}} → {{communities_later_net}} ({{communities_later_ex2023_net}}).
- **All of Madre de Dios:** {{mdd_pre_net}} → {{mdd_during_net}} → {{mdd_later_net}} ({{mdd_later_ex2023_net}}).

**Not all of it can be miners who moved.** Take every other zone inside Madre de Dios whose net additions rose from 2016–18 to 2019–21: together their rises are {{mdd_rise_elsewhere_vs_tambopata_fall:.1f}} times the Tambopata buffer zone's fall. New entrants and the gold price fit too (not tested). [[D]]

**Why it matters:** after 2019, net additions rose mostly on legal land. [[D]] For the reserve that is good news. For the region it is not: the department's net additions kept growing, and corridor mining still uses mercury.

:::more Legality, the second product, and what we can't show
:::fig output/fig_v2_corridor_share.png
read: Each point is one year's share of Madre de Dios mining additions on legal-mining-corridor land (dark: net additions; light: new land), 2005–2025. Bars: period shares.
take: The net share jumped in 2019 and stayed high; the new-land share rose more gradually. Both stayed above their 2016–18 level.
:::

:::fig output/fig_v2_legality.png
read: New land (first-time mining, not net) in Madre de Dios split by MAAP's legality grade: Low = active concession, Medium = concession not verified as active, High = outside any concession, Very high = strict protected area.
take: The presumed-illegal share of new land fell after 2019, and the grey zone of unverified concessions grew.
:::

- **Presumed illegal (High + Very high), share of new land:** {{leg_illegal_share_pre:.0%}} → {{leg_illegal_share_during:.0%}} → {{leg_illegal_share_later:.0%}} (2016–18 → 2019–21 → 2022–25). Another measure (new land only): legality is graded per pixel when it is first mined. [[D]]
- **The grey zone grew:** concessions not verified as active took {{leg_medium_share_pre:.0%}} → {{leg_medium_share_during:.0%}} → {{leg_medium_share_later:.0%}} of new land. [[D]]
- **Presumed-illegal share of net additions** (tenure "none": outside the legal mining corridor and outside communities): {{t7_presumed_illegal_share_pre_net:.0%}} → {{t7_presumed_illegal_share_during_net:.0%}} → {{t7_presumed_illegal_share_later_net:.0%}}. Of new land: {{t7_presumed_illegal_share_pre_new:.0%}} → {{t7_presumed_illegal_share_during_new:.0%}} → {{t7_presumed_illegal_share_later_new:.0%}}. [[D]]
- **Inside the legal mining corridor**, {{leg_corridor_highish_share:.0%}} of all new land since 1986 sits on land without a verified active concession. [[D]]
- **Time-consistent check:** counting a concession only if it was filed by the mining year gives {{leg_tc_illegal_share_pre:.0%}} → {{leg_tc_illegal_share_during:.0%}} → {{leg_tc_illegal_share_later:.0%}} presumed illegal and {{leg_tc_medium_share_pre:.0%}} → {{leg_tc_medium_share_later:.0%}} grey zone: the same picture.

:::fig output/fig_v2_amw_robustness.png
read: Another product, Amazon Mining Watch (AMW): new gold-mining area per year in the La Pampa sector and in the corridor across the road (left), and the share north of the highway at La Pampa's longitudes (right), 2019–2025 (2025 provisional). AMW has no "stopped" state, so it cannot give net additions.
take: A second product also puts most new area north of the road from 2019 on. Its hectares are not comparable with ours.
:::

- **AMW, north-of-road share of new area** at La Pampa's longitudes: {{amw_reg_north_share_2019:.0%}} (2019) and {{amw_reg_north_share_2021:.0%}} (2021). [[D]]
- **Why the products differ:** AMW flags a 480-m square only once; MapBiomas counts every 30-m pixel. {{pc_restofminingcorr_in_earlier_patch_later:.0%}} of MapBiomas new land in the rest of the legal mining corridor in 2022–25 lies inside AMW squares flagged earlier, so AMW cannot count it again.
- **MAAP #208** finds 74% of 2021–24 mining deforestation in Madre de Dios inside the legal mining corridor. Another measure (deforestation); it agrees on the direction.
- **The 2023 spike** appears region-wide in MapBiomas only (GLAD-L alerts and AMW stay flat); every later-years number is also given without 2023.
- **Can't show:** that the *same* people moved.

**Code:** `code/raster_layers.py`, `code/v2_legality.py`, `code/v2_extra.py` (AMW), `code/v2_products_check.py`.
:::

## Across the road | Across the road, net mining rose {{corridor_across_pre_net}} → {{corridor_across_during_net}} ha/yr

**In the corridor across the road (legal-mining-corridor land within 10 km north of the highway at La Pampa's longitudes) net additions rose from {{corridor_across_pre_net}} ha/yr (2016–18) to {{corridor_across_during_net}} ha/yr (2019–21) and {{corridor_across_later_net}} ha/yr in 2022–25 ({{corridor_across_later_ex2023_net}} without 2023).** Over the same years the La Pampa sector, just south of the road, fell from {{lapampa_pre_net}} to {{lapampa_during_net}} ha/yr. [[D]]

**The wider view, 1-km bands within 30 km of the highway at La Pampa's longitudes:** net additions south of the road fell from {{v2_road_south_pre_net}} to {{v2_road_south_during_net}} ha/yr, while north of it they rose from {{v2_road_north_pre_net}} to {{v2_road_north_during_net}} (2016–18 vs 2019–21). The north side's share of these bands' net additions went from {{t1_road_north_share_pre_net:.0%}} to {{t1_road_north_share_during_net:.0%}}. [[D]]

:::fig output/fig_v2_road_bands.png
read: Net mining additions per year in 1-km bands parallel to the highway, La Pampa's longitudes only. Orange = south (La Pampa side), blue = north (legal-corridor side); shaded = more than 10 km north. Three periods.
take: In 2019–21 the mass of net additions jumped from the south side to the bands just north of the road; in 2022–25 both sides grew, the north mostly 10–20 km in.
:::

- **The jump north stands out among clean start years:** net additions, rank {{t1_road_shift_rank_clean_net:.0f}} of {{t1_road_shift_n_clean_net:.0f}} (p = {{t1_road_shift_ri_p_clean_net:.2f}}, the smallest possible with {{t1_road_shift_n_clean_net:.0f}} start years); new land, rank {{t1_road_shift_rank_clean_new:.0f}} of {{t1_road_shift_n_clean_new:.0f}}. [[D]]
- **Hugging the road (new land, north of the highway):** mean distance north fell from {{t9_depth_2016:.0f}} km (2016) to {{t9_depth_2020:.0f}} km (2020), then reached {{t9_depth_2025:.0f}} km by 2025. [[D]]

**Why it matters:** a two-lane road is no barrier. After an operation south of the highway, expect more mining north of it in the following years. [[P]]

:::more The road has been crossed before, plus every test
:::fig output/fig_v2_road_placebo.png
read: Change in the share of new land (first-time mining) north of the highway, 3 years from each start year minus the 3 years before. Blue = the real 2019 start; pale bars = windows that overlap the event.
take: Among start years whose windows do not touch the event, none moves new land north as much as 2019. There are only 8 such years.
:::

:::fig output/fig_v2_depth.png
read: New land (first-time mining) north of the highway at La Pampa's longitudes: hectares per year by distance band (left) and mean distance north of the highway (right), 2008–2025. New land only: a mean distance cannot be taken of net additions.
take: Right after Mercurio new land hugged the road; from 2021 it spread deeper into the legal mining corridor.
:::

- **All start years 2008–2022:** the 2019 shift ranks {{t1_road_shift_rank_net:.0f}} of 15 for net additions (p = {{t1_road_shift_ri_p_net:.2f}}) and {{t1_road_shift_rank_new:.0f}} of 15 for new land (p = {{t1_road_shift_ri_p_new:.2f}}); for new land the 2020 window, which overlaps the event, is larger.
- **History (new land):** in 2008 {{t1_road_north_share_2008_new:.0%}} of new land was north of the road (the Guacamayo boom). The share fell to {{t1_road_north_share_2015_new:.0%}} by 2015, as La Pampa grew, then rose again after Mercurio ({{t1_road_north_share_2021_new:.0%}} in 2021). [[D]]
- **Depth break (new land):** {{t9_depth_post2019:+.1f}} km after 2019, net of trend (p = {{t9_depth_post2019_p:.3f}}, Newey-West). [[D]]
- **Per 1-km cell (net additions, vs cells 10–30 km south):** 0–5 km north {{st_grad_b_N0_5_during_net:+.2f}} ha per cell-year in 2019–21 (p = {{st_grad_b_N0_5_during_net_p:.3f}}); 10–20 km north {{st_grad_b_N10_20_later_net:+.2f}} in 2022–25 (p = {{st_grad_b_N10_20_later_net_p:.3f}}). Description: the reference cells hold little mining.
- **Per 1-km cell, corridor across the road:** {{st_main_corridor_across_during_net:+.2f}} ha of net additions per cell-year in 2019–21 vs 2014–18. The comparison cells hold almost no mining, so this is close to the zone's own before/after, and its pre-trend test fails on net ([Six methods](#six-methods), Attempt 1).
- **Boundary choice doesn't matter:** see [The places](#the-places).
- **Not "within a year":** the spatial RD at the road shows the swing mainly in 2020–22, and it is weak on net ([Six methods](#six-methods), Attempt 4).

**Code:** `code/raster_zones.py` (road bands), `code/v2_tests.py` (T1, T4, T9), `code/v2_stats.py` (road gradient).
:::

## Money and gold | Money faded after 2019, while gold rose {{gold_price_ratio_2025_2018:.1f}}-fold

**Two things line up with the return: enforcement money booked in Madre de Dios peaked in 2019 and faded, and the gold price rose {{gold_price_ratio_2025_2018:.1f}}-fold from 2018 to 2025.** We can show both next to the mining curve; we cannot test either as a cause. [[D]]

:::fig output/fig_v2_enforcement_spending.png
read: Executed spending of PP 0128, Peru's budget programme against illegal mining, booked in Madre de Dios, million soles (top), next to net mining additions in all of Madre de Dios (bottom), 2015–2025. Spending is a lower bound: national units book under Lima.
take: Spending peaked in 2019 and faded; the department's net additions kept growing. Two measures side by side, never one as the cause of the other.
:::

- **Money (PP 0128, booked in Madre de Dios):** {{t8_pp0128_mdd_2018:,.0f}} soles (2018), {{t8_pp0128_mdd_2019:,.0f}} (2019), {{t8_pp0128_mdd_2021:,.0f}} (2021), {{t8_pp0128_mdd_2025:,.0f}} (2025). [[D]]
- **Gold price:** up {{gold_price_ratio_2025_2018:.1f}}-fold from 2018 to 2025 (annual means, nominal US$). Year effects remove it only if it hits every zone equally, which it need not. [[D]]
- **The gold was still there:** by 2018 only {{gold_broad_lapampa_depleted_2018:.0%}} of the La Pampa sector's gold-bearing land had been mined (about {{gold_broad_lapampa_left_2018_ha:,.0f}} ha left), though its most-mined third of 1-km cells was {{st_lp_tq_high_share18:.0%}} mined. Miners could come back. [[D]]
- **Other waves overlap:** COVID pulled forces away in 2020; Plan Restauración followed in 2021, a state of emergency in April 2023. Our estimates measure "Mercurio and what followed", never Mercurio alone.

**Why it matters:** the operation's money was spent in its first years, and the gold kept getting more valuable. Plan for the years after the sweep, when both pull the other way. [[P]]

:::more The enforcement timeline, politics, COVID, 2017, and Asner & Tupayachi
:::fig output/fig_v2_timeline.png
read: Top: events by type (enforcement, presidents, laws, context). Below: net mining additions per year in the La Pampa sector and in all of Madre de Dios, 2008–2025. Shaded: 2019–21.
take: La Pampa's net additions fell in 2019–21 and in no earlier window; in 2012–13 they rose.
:::

| When | What |
|---|---|
| 2009–2010 | First interdictions; dredges banned (DU 012-2010) |
| Feb–Apr 2012 | D.L. 1100 (legal mining corridor, interdiction) and D.L. 1105 (formalization), under President Humala |
| 2013–2016 | Interdictions fade: 49 (2013) → 1 (Jan–May 2016) in Madre de Dios |
| 2017–2018 | Series of operations and interdictions in the region (AIDER 2021, cited in MAAP #241): the pre-period is not enforcement-free |
| Nov 2018 | La Pampa plan approved (later "Mercurio"), under President Vizcarra |
| 19 Feb 2019 | **Operation Mercurio** (the treatment): 1,272 police, 300 soldiers, 70 prosecutors; monthly rotation of garrisons and commanders against corruption (Dethier et al. 2023) |
| 2019 | "Mercurio II" covers all of Madre de Dios (MINAM, 2021, p. 33) |
| Spring 2020 | Forces pulled away for COVID; deep budget cuts |
| 2021 | Plan Restauración |
| 2021–2022 | President Castillo; ministerial churn; enforcement relaxes |
| Apr 2023 → | State of emergency in six districts |
| 2025 | Navy withdrawn from Malinowski river posts (MAAP #241) |

- **One fall, not two:** La Pampa sector net additions changed by {{tl_lp_change_2012_13_vs_2010_11_net:+.0%}} in 2012–13 vs 2010–11 (new land {{tl_lp_change_2012_13_vs_2010_11_new:+.0%}}). [[D]]
- **The political-cycle idea:** both enforcement waves started 7–11 months after a new president (Humala 2011 → decrees 2012; Vizcarra 2018 → Mercurio 2019). A pattern, not evidence.
- **The 2012–13 check (zone level):** the Tambopata buffer zone's 2012–13 coefficient on net additions was {{t3_asner_2012_13_net:+,.0f}} ha/yr vs 2008–11, rank {{t3_asner_rank:.0f}} of {{t3_asner_n:.0f}} zones: no Tambopata-specific fall. [[D]]
- **COVID:** forces left La Pampa in spring 2020; budgets fell sharply in 2020–21 (Mongabay 2023).
- **The 2017 spike:** 2017 was the record year for mining deforestation (Caballero Espejo et al. 2018). The gold price was flat (about $1,250/oz, 2016–18). Gangs ran extortion in La Pampa, but no source dates a 2017 takeover.
- **Asner & Tupayachi (2017)** report a brief dip after the 2012 interdictions, then a near doubling, also inside the reserve. Our data show no 2012–13 dip in La Pampa. The first cycle is theirs, not ours.

**Code:** `code/v2_extra.py` (timeline), `code/v2_tests.py` (spending, 2012–13 check). **Sources:** `docs/walkthrough/notes/qualitative_background.md`, `enforcement_intensity.md`.
:::

:::more Gold left in the ground: how we measured it
| Gold-bearing land already mined (broad definition) | by 2018 | by 2025 |
|---|---:|---:|
| La Pampa sector | {{gold_broad_lapampa_depleted_2018:.0%}} | {{gold_broad_lapampa_depleted_2025:.0%}} |
| Corridor across the road | {{gold_broad_corridor_across_depleted_2018:.0%}} | {{gold_broad_corridor_across_depleted_2025:.0%}} |
| Rest of the legal mining corridor | {{gold_broad_corridor_rest_depleted_2018:.0%}} | {{gold_broad_corridor_rest_depleted_2025:.0%}} |
| Kotsimba land inside the Tambopata buffer zone | {{gold_broad_tambopata_bz_kotsimba_depleted_2018:.0%}} | {{gold_broad_tambopata_bz_kotsimba_depleted_2025:.0%}} |

- **The proxy:** no one publishes gold left in the ground. Gold here is alluvial, so we used the national geology map (INGEMMET, 1:100,000): river deposits plus the gold-bearing terraces of the Madre de Dios Formation.
- **Does it work?** {{gold_broad_validation:.0%}} of all land ever mined lies on these units, which cover {{gold_broad_land_share_mdd:.0%}} of Madre de Dios ({{gold_broad_lift:.1f}}× more mining than chance). The strict river-deposit units cover {{gold_strict_land_share_mdd:.0%}} and hold {{gold_strict_validation:.0%}} ({{gold_strict_lift:.1f}}×). La Pampa was {{gold_strict_lapampa_depleted_2018:.0%}} depleted by 2018 under the strict definition too.
- **Limits:** the map is coarse and says nothing about gold grade; old pits can be mined again.

**Code:** `code/raster_gold.py`, `code/v2_stats.py` (depletion terciles).
:::

:::more Informed speculation: what the gold is worth, and what enforcement costs
**New land mined in Madre de Dios yields about {{eco_gold_t_lo_later:.0f}}–{{eco_gold_t_hi_later:.0f}} t of gold a year (2022–25), worth US$ {{eco_value_musd_lo_later:,.0f}}–{{eco_value_musd_hi_later:,.0f}} M a year. Producers declared {{eco_declared_t_2022_25:.1f}} t.** Every number here is our arithmetic on cited parameters, not a measurement, and it is built on new land, not net additions. [[P]]

:::fig output/fig_v2_economics.png
read: Six yearly amounts for Madre de Dios, 2022–25, US$ on a log scale (each tick = 10×). Bars span the low–high range our cited parameters allow; a dot means one value.
take: The gold mined and its social cost are hundreds of times the enforcement money booked in the region; the tax at stake is small next to both.
:::

- **Enforcement money is tiny next to the gold:** US$ {{eco_spend_musd:,.1f}} M a year booked in Madre de Dios (a lower bound), about {{eco_spend_share_of_value:.1%}} of the gold's value. [[P]]
- **Tax is a weak reason to stay illegal:** small producers pay **0% royalty**; income tax is only {{eco_tax_share_value_lo:.0%}}–{{eco_tax_share_value_hi:.0%}} of the gold's value. Location is the strong reason: La Pampa can never be formalized. [[P]]
- **Social cost dwarfs both:** two separate Conservation Strategy Fund (CSF) estimates, US$ {{eco_social_busd_calc_lo:,.1f}}–{{eco_social_busd_calc_hi:,.1f}} bn a year (calculator) or US$ {{eco_social_busd_pdf_lo:,.0f}}–{{eco_social_busd_pdf_hi:,.0f}} bn a year (2023 report), mostly mercury's health damage. [[P]]
- **The lever is the sale, not the tax rate:** make laundered gold hard to sell and the discount on illegal gold grows. At 2025 prices one hectare holds about US$ {{eco_gold_usd_per_ha_2025_lo:,.0f}}–{{eco_gold_usd_per_ha_2025_hi:,.0f}} of gold, which is why old pits are worth re-mining. [[P]]
- **The gold:** {{eco_ha_low_later:,.0f}} ha of new land a year (2022–25) × {{eco_param_yield_kg_ha_lo:.1f}}–{{eco_param_yield_kg_ha_hi:.1f}} kg per ha (CSF, 2023). Low and high differ only in the yield. Re-mined land ({{eco_ha_high_later:,.0f}} ha a year newly mined or re-mined, 2022–25) gets no gold: CSF has no yield for old pits, so both ends understate if old pits still pay.
- **Cross-check:** MINEM's 2016–18 gold (declared + estimate) implies {{eco_implied_kg_ha_new_pre:.1f}} kg per hectare of new land we mapped ({{eco_implied_kg_ha_pre:.1f}} per hectare newly mined or re-mined): above the CSF yield, so the range is likely low.
- **Declared:** {{eco_declared_share_lo:.0%}}–{{eco_declared_share_hi:.0%}} of that gold shows up as declared Madre de Dios production. The rest leaves under someone else's paperwork or none.
- **Taxes not paid:** income tax (29.5% of an 11–37% margin): US$ {{eco_tax_musd_lo:,.0f}}–{{eco_tax_musd_hi:,.0f}} M a year. **Mercury:** {{eco_hg_t_lo:,.0f}}–{{eco_hg_t_hi:,.0f}} t a year.

| Parameter | Low | High | Source |
|---|---:|---:|---|
| Gold per hectare (kg) | {{eco_param_yield_kg_ha_lo:.1f}} | {{eco_param_yield_kg_ha_hi:.1f}} | CSF (2023), Cuadro 3, 2.5-m pits at Huepetuhe, Puquiri, Malinowski |
| Profit margin | {{eco_param_margin_lo:.0%}} | {{eco_param_margin_hi:.0%}} | Torres (2015, CooperAcción) via MINAM (2016) |
| Income tax | {{eco_param_income_tax_lo:.1%}} | {{eco_param_income_tax_hi:.1%}} | D.L. 1269 (general rate) |
| Mercury per kg of gold (kg) | {{eco_param_hg_per_au_lo:.1f}} | {{eco_param_hg_per_au_hi:.1f}} | CSF (2023), p.43 |
| Social cost per kg of gold, calculator (US$) | {{eco_param_social_calc_usd_kg_lo:,.0f}} | {{eco_param_social_calc_usd_kg_hi:,.0f}} | CSF calculator web page |
| Social cost per kg of gold, report (US$) | {{eco_param_social_pdf_usd_kg_lo:,.0f}} | {{eco_param_social_pdf_usd_kg_hi:,.0f}} | CSF (2023), p.7 |
| Soles per US$, 2022 / 2023 / 2024 / 2025 | {{eco_param_pen_per_usd_2022:.2f}} / {{eco_param_pen_per_usd_2023:.2f}} | {{eco_param_pen_per_usd_2024:.2f}} / {{eco_param_pen_per_usd_2025:.2f}} | BCRP annual averages, each year converted at its own rate |

- **Yield is the weak link:** CSF found no grade for La Pampa's suction-pump method. Kg per hectare scales with pit depth: 5-m pits would double it.
- **Two social-cost estimates, never merged:** CSF's calculator and its 2023 report value mercury's health damage very differently. Quote both, and say which.
- **Cost per hectare kept out of the target:** PP 0128 spending in Madre de Dios, 2019–21, was about S/ {{eco_soles_per_ha_kept:,.0f}} per hectare of net additions kept out of the Tambopata buffer zone, using the zone-level gap (likely an upper bound on the hectares, so a lower bound on the cost). One hectare held US$ {{eco_gold_usd_per_ha_1921_lo:,.0f}}–{{eco_gold_usd_per_ha_1921_hi:,.0f}} of gold at 2019–21 prices. The region did not mine less.
- **Three ways to sell the same gold.** *Legal:* a concession in the legal mining corridor, an environmental permit, taxes; only 145 of 9,592 miners in formalization in Madre de Dios were fully formalized (MINAM, 2021); nationally 2.4% (2024). *Informal (REINFO):* registered "in formalization", protected from prosecution (D.L. 1351) as long as they work outside banned zones; nearly all Madre de Dios registrations sit inside the legal mining corridor (our overlay of MINEM's register). *Illegal:* outside the corridor, like La Pampa; it can never be formalized; its gold sells at a discount (S/ 80 instead of S/ 180 per gram during the 2020 lockdown) or travels on corridor paperwork.
- **Crime:** extortion of S/ 1,000 per raft per week in La Pampa (Mongabay, 2026); illegal mining is now Peru's largest illegal economy, ahead of drugs (IPE, 2025). Illegal gold exports of about US$ 7.4 bn (2024) and over US$ 11.5 bn (2025) nationally (IPE, press reports; the method also catches stock changes and re-exports).
- **Don't cite:** the "25% of GDP" figure (Canal N) and the "44% of exports" snippet (it's Peru's share of South American illegal exports).

**Code:** `code/v2_economics.py`. **Sources with quotes and pages:** `docs/walkthrough/notes/economics_sources.md`. The CSF report is in `data_raw/literature/` and `DOWNLOAD_LOG.csv`.
:::

:::more Declared gold: the official "−88%" is a definition change
**The official Madre de Dios gold series fell {{pe_prod_fall_2018_2025_pct:.0f}}% from 2018 to 2025, but that is a definition change, not a production fall.** Until 2019 it included the ministry's *estimate* of artisanal gold; from 2020 it holds only what producers declare. Don't cite "−88%". [[D]]

:::fig output/fig_peru_gold_definition.png
read: Madre de Dios gold in the official series, tonnes per year: what producers declared (dark) plus the ministry's artisanal estimate (light), 2010–2025; dots = central bank series, 2020–25.
take: The "collapse" in 2020 is the estimate leaving the files. Declared output was about 1 t a year before and after.
:::

- **Declared output stayed small:** {{gold_minem_declared_2018_kg:,.0f}} kg in 2018 (MINEM file); {{gold_bcrp_declared_2020_kg:,.0f}} kg in 2020 and {{gold_bcrp_declared_2025_kg:,.0f}} kg in 2025 (central bank). The estimate was {{gold_minem_estimate_2019_kg:,.0f}} kg in 2019 and is absent from 2020. We withdrew our earlier "collapse" and its break test.
- **The series:** the ministry's files carry "PRODUCTORES ARTESANALES — cifras estimadas" for Madre de Dios until {{gold_minem_last_estimate_year:.0f}} ({{gold_minem_estimate_2016_kg:,.0f}} kg in 2016, {{gold_minem_estimate_2019_kg:,.0f}} kg in 2019).
- **Source check:** MINEM declared + estimate equals the central bank's series within 2% in {{gold_minem_bcrp_n_match:.0f}} of 25 years (2001–2025); not in 2015–16 nor from 2020, when the MINEM files run above the central bank. For declared output after 2020 we cite the central bank.
- **An earlier break in 2015:** until 2014, artisanal producers' own declarations were in the series ({{gold_minem_declared_2014_kg:,.0f}} kg in 2014); from 2015 producers declared only {{gold_minem_declared_2015_kg:,.0f}} kg and the ministry added an estimate.
- **"Mining in the corridor, declaring nothing" (plausible mechanism, not a finding).** For: {{leg_medium_share_later:.0%}} of new land in 2022–25 sat in concessions not verified as active; producers declare about 1 t a year while new land covers over {{mdd_later_new}} ha a year (2022–25); Bolivia's gold exports jumped from 1.7 t (2012) to 35.7 t (2014); nationally at least 80 of ~180 t exported in 2024 had unknown origin. Against: gold may be declared in other regions; mapped area includes re-mined pits; gold yield per hectare is unknown.

**Code:** `code/peru_gold_minem.py`, `code/peru_production.py`. **Source:** `docs/walkthrough/notes/legality_data.md`.
:::

## How it came back | It came back, a third to a half on old pits

**In 2022–25 the Tambopata buffer zone averaged {{tambopata_bz_later_net}} ha/yr of net additions ({{tambopata_bz_later_ex2023_net}} without 2023). Re-mined land made up {{tambopata_bz_later_remined_share_added:.0%}} of the land added (new + re-mined) in 2022–25, and {{tambopata_bz_later_ex2023_remined_share_added:.0%}} without 2023.** [[D]]

| Tambopata buffer zone, ha/yr | 2016–18 | 2019–21 | 2022–25 | 2022–25 without 2023 |
|---|---:|---:|---:|---:|
| New land | {{tambopata_bz_pre_new}} | {{tambopata_bz_during_new}} | {{tambopata_bz_later_new}} | {{tambopata_bz_later_ex2023_new}} |
| + Re-mined | {{tambopata_bz_pre_remined}} | {{tambopata_bz_during_remined}} | {{tambopata_bz_later_remined}} | {{tambopata_bz_later_ex2023_remined}} |
| − Stopped | {{tambopata_bz_pre_stopped}} | {{tambopata_bz_during_stopped}} | {{tambopata_bz_later_stopped}} | {{tambopata_bz_later_ex2023_stopped}} |
| **= Net additions** | **{{tambopata_bz_pre_net}}** | **{{tambopata_bz_during_net}}** | **{{tambopata_bz_later_net}}** | **{{tambopata_bz_later_ex2023_net}}** |

- **2023 alone:** {{tambopata_bz_2023_remined}} ha of re-mined land in the Tambopata buffer zone, a MapBiomas-only spike year; hence every later-years number with and without 2023. [[D]]
- **Another source agrees on the direction:** MAAP #193 reports miners back on degraded land in La Pampa in 2023, and 148 → 598 dredges (2021 → 2023).

**Why it matters:** an operation can stop clearing while miners quietly return to old pits. FZS should monitor old mining sites, not only forest edges. [[P]]

:::more Re-mining across the region, and map flicker
:::fig output/fig_v2_sankey.png
read: Gross inflow (not net): land newly mined or re-mined per year, by origin (left) and zone (right), Madre de Dios, three periods; stopped land and net additions are named above each period. Width = ha/yr, same scale in all panels.
take: Re-mined land grew in every period, and La Pampa's later-years inflow leans on it.
:::

:::fig output/fig_v2_stream_remined.png
read: Re-mined land (one part of net additions) per year in Madre de Dios, stacked by zone (top, ha) and as shares (bottom), 2010–2025.
take: The legal mining corridor holds most re-mined land; La Pampa's own re-mining jumps in 2023.
:::

- **Re-mined share of the gross inflow, Madre de Dios:** {{v2_remined_share_pre:.0%}} → {{v2_remined_share_during:.0%}} → {{v2_remined_share_later:.0%}} (2016–18 → 2019–21 → 2022–25). [[D]]
- **Where re-mining happens:** legal-mining-corridor land holds {{rm_corridor_share_pre:.0%}} → {{rm_corridor_share_during:.0%}} → {{rm_corridor_share_later:.0%}} of Madre de Dios re-mined land; the La Pampa sector {{rm_lapampa_share_pre:.0%}} → {{rm_lapampa_share_during:.0%}} → {{rm_lapampa_share_later:.0%}}. [[D]]
- **La Pampa sector in 2023:** re-mined land ({{lapampa_2023_remined}} ha) was nearly twice new land ({{lapampa_2023_new}} ha). [[D]]
- **Flicker:** "re-mined" and "stopped" both include pixels that switch class back and forth. The La Pampa sector already showed {{lapampa_pre_remined}} ha/yr of re-mined land in 2016–18. Trust large changes, not small ones.

**Code:** `code/raster_layers.py` (Sankey, streams), `code/raster_zones.py` (parts).
:::

## Inside the reserve | In 2025, mining inside the reserve jumped {{tambopata_nr_2025_net}} ha

**The course tables cover only buffer zones. Inside Tambopata National Reserve net additions were +{{tambopata_nr_2025_net}} ha in 2025, after {{tambopata_nr_during_net:+,.0f}} ha/yr in 2019–21; the mining stock reached {{tambopata_nr_stock_2025:,.0f}} ha in 2025.** [[D]]

:::fig output/fig_peru_inside_reserves.png
read: Net mining additions (line) and their parts (bars) per year, 2011–2025: Tambopata National Reserve (top) and its buffer zone (bottom), different y-scales. Raster stock 2025 inside the reserve agrees with the publisher's protected-area statistics (777 ha).
take: Inside the reserve net additions were near zero except 2017 and 2025.
:::

- **Where inside:** {{rd_reserve_inside_share_1km:.0%}} of new land inside the reserve (2000–25, stretches next to the buffer zone) lies within 1 km of its edge. [[D]]
- **Other sources agree on the direction:** MAAP #241 reports ~500 ha of new mining deforestation inside the reserve (late 2025 to Feb 2026); AMW shows {{sp_amw_tambopata_nr_new_ha_2025:,.0f}} ha of new area there in 2025 (another product, provisional). [[D]]
- **Timing, not cause:** the navy withdrew from its Malinowski River posts in 2025, the same year (MAAP #241). We cannot test whether one led to the other.
- **It happened before:** by October 2016, 521 ha inside the reserve had been lost to mining (Asner & Tupayachi, 2017). Different maps, so we don't subtract.

**Why it matters:** this is FZS's core area, and the most actionable finding.

:::more The 2017 jump and the code
- **2017:** +{{tambopata_nr_2017_net}} ha of net additions inside the reserve, almost all new land ({{tambopata_nr_2017_new}} ha). 2017 was the record year for mining deforestation in the region (Caballero Espejo et al. 2018). We cannot tell from our data how much of the jump is real mining. [[D]]

**Code:** `code/peru_anp.py`, `code/raster_zones.py`.
:::

@part Is it causal?

## Six methods | Six methods: all point down, two hold up, none clean

**We tried six ways to build "what would have happened without Mercurio". All six find the target slower or falling; two, difference-in-differences and synthetic DiD, give a large, stable number in hectares. None passes its own identifying check cleanly.** In hectares, the Tambopata buffer zone's 2019–21 fall in net additions stands out against 14 other Peruvian buffer zones, but it ranked first in hectares before Mercurio too; relative to its size it is ordinary; against areas abroad it can't be told from chance. All six are description; the one conditional causal sentence rests on Attempt 1 ([The claim](#the-claim)).

| Attempt | Compares the Tambopata buffer zone with | Result | Problem | Verdict |
|---|---|---|---|---|
| **1 Difference-in-differences** | 14 other Peruvian buffer zones (M1); Amarakaeri alone (2×2) | Net additions, 2019–21: M1 {{model_m1_during_net}} ha/yr; 2×2 {{did_base2014_net}} (2014–18 baseline) | Raw rank 1 also in 2014–16; scaled {{model_m4_rank:.0f}}rd–{{placebo_space_rank_scaled:.0f}}th of 7 | **Holds up in hectares: the basis of the [C] sentence** |
| **2 Synthetic control** | a weighted mix of Peruvian zones | {{synth_ext_add_gap_during}} ha/yr = all weight on Amarakaeri | No pre-2019 fit in hectares ({{synth_core_add_hull_years_outside:.0f}} of 5 years outside every donor) | Misfit, description only |
| **3 Rule-based twins** | Amanã, Tapajós, Munduruku (Brazil) | AMW measure: Tambopata at {{top3_ratio:.0%}} of the twins' pace ({{top3_ratio_excl_unverified:.0%}} without Munduruku) | Not parallel before 2019; another product | Weak check |
| **4 Spatial RD** | land either side of the road and the reserve edge | Net additions: road {{rd_road_did_net:+.1f}} pts (p = {{rd_road_did_net_p:.2f}}); reserve edge {{rd_reserve_did_net:+.1f}} (p = {{rd_reserve_did_net_p:.2f}}) | Road p {{rd_road_sens_p_min:.2f}}–{{rd_road_sens_p_max:.2f}} across bandwidths; displacement breaks the design | Uninformative on net |
| **5 Matching** | areas picked by algorithm across the Amazon | AMW measure: Tambopata at {{psm_ratio_min:.0%}}–{{psm_ratio_max:.0%}} of its matches' pace | Placebo p {{psm_p_min:.2f}}–{{psm_p_max:.2f}}; no common support | Can't decide |
| **6 Synthetic DiD** | weighted zones, trend-matched | {{sdid_sdid_ha_during_net}} ha/yr | Weights explain {{sdid_pre_fit_r2:.0%}} of the pre-2019 variation; {{sdid_sdid_ha_during_pre2011_net}} when fitted from 2011 | **Holds up in hectares (sensitivity)** |

**Why it matters:** only the zone-level comparisons give a large, stable number, and only in hectares. That supports one conditional sentence, read as an upper bound, not more.

:::more Attempt 1, difference-in-differences: the 2×2, the model ladder and the cell panel
**In hectares, the Tambopata buffer zone's 2019–21 fall in net additions is the largest against 14 other Peruvian buffer zones under every model. Relative to its own size it is ordinary, and the cell panel is close to a before/after.** [[D]]

:::fig output/fig_peru_event_study.png
read: Top: the Tambopata buffer zone's net additions relative to 14 other Peruvian buffer zones, each year vs 2018 (= 0), with its three parts (one treated zone: no confidence intervals). Bottom: net additions in the Tambopata and Amarakaeri buffer zones that make up most of the coefficients.
take: The net coefficient drops in 2019–21, spikes in 2023 and is back near zero in 2025. The new-land line stays low from 2020; the stopped line moves most in 2019. Before 2019 the line is not flat (2016).
:::

:::fig output/fig_peru_models.png
read: The 2019–21 coefficient on net additions under four models (M1 zone + year effects; M2 + gold price × size; M3 + own trends; M4 scaled to size), each next to the same model with a fake 2016 start. Labels give the raw and the scaled rank.
take: In hectares every model shows a fall (M1 {{model_m1_during_net}}, M2 {{model_m2_during_net}}, M3 {{model_m3_during_net}} ha/yr), raw rank 1; relative to size the ranks are ordinary. M3's and M4's fakes have the same sign as the real effect.
:::

**Level 1: the course's 2×2 (Tambopata buffer zone vs the less-treated Amarakaeri buffer zone, 2016–18 baseline), net additions and parts**

| Change 2016–18 → 2019–21, ha/yr | Net | New land | Re-mined | Stopped |
|---|---:|---:|---:|---:|
| Tambopata buffer zone | {{did_main_chg_tambopata_net:+,.0f}} | {{did_main_chg_tambopata_new:+,.0f}} | {{did_main_chg_tambopata_remined:+,.0f}} | {{did_main_chg_tambopata_stopped:+,.0f}} |
| Amarakaeri buffer zone | {{did_main_chg_amarakaeri_net:+,.0f}} | {{did_main_chg_amarakaeri_new:+,.0f}} | {{did_main_chg_amarakaeri_remined:+,.0f}} | {{did_main_chg_amarakaeri_stopped:+,.0f}} |
| **Difference** | **{{did_main_net:+,.0f}}** | {{did_main_new:+,.0f}} | {{did_main_remined:+,.0f}} | {{did_main_stopped:+,.0f}} |

- **Amarakaeri was itself treated** (Mercurio II covered all of Madre de Dios), so it is "less treated", not a control. It may also have received miners.
- **Baseline 2014–18 instead of 2016–18:** {{did_base2014_net:+,.0f}} ha/yr. This is the 2×2 in the causal range: five base years, so the 2017 peak weighs less.
- **Later years (persistence):** {{did_persistence_net:+,.0f}} ha/yr, 2016–18 vs 2022–25.
- **Other comparisons (same 2×2, 2016–18 baseline):** vs Bahuaja-Sonene {{robust_did_main_bahuaja_net:+,.0f}}; vs other Amazon buffer zones {{robust_did_main_amazon_pool_net:+,.0f}}; vs all other Peruvian buffer zones {{robust_did_main_all_peru_poolB_net:+,.0f}} ha/yr. Against the legal mining corridor, a displacement target, it is {{robust_did_main_corridor_outside_bz_net:+,.0f}}: inflated by design.

**Level 2: Tambopata vs 14 other Peruvian buffer zones with mining (net additions)**

- **Model:** net additions = zone effect + year effect + Tambopata × period, 2014–25, reference 2014–18. Year effects remove shocks common to every zone; the gold price and COVID need not be common, which is why M2 and the context models exist.
- **Fake places:** each other zone gets the "operation" in turn, with Tambopata removed from its comparison pool. Raw rank {{model_m1_rank:.0f}} of {{model_m1_n:.0f}} in hectares, which the zone also holds in 2014–16; scaled rank {{model_m1_rank_scaled:.0f}} of {{model_m1_n_scaled:.0f}} (M1), {{model_m4_rank:.0f}} of {{model_m4_n:.0f}} (M4); among the Amazon zones scaled to size (M4), rank {{model_m4_rank_amazon:.0f}} of {{model_m4_n_amazon:.0f}}.
- **The parts (M1):** new land {{model_m1_during_new:+,.0f}}, re-mined {{model_m1_during_remined:+,.0f}}, stopped {{model_m1_during_stopped:+,.0f}} ha/yr (stopped enters with a minus sign).
- **Dropping the largest comparison zone (Amarakaeri), event study:** {{robust_es_poolB_drop_largest_during_net:+,.0f}} ha/yr (2019–21 vs 2018).

| Model | Adds | 2019–21 | 2022–25 | Fake 2016 | Raw rank | Scaled rank |
|---|---|---:|---:|---:|---:|---:|
| **M1** | Zone + year effects | {{model_m1_during_net}} | {{model_m1_later_net:+,.0f}} | {{model_m1_placebo_net:+,.0f}} | {{model_m1_rank:.0f}} of {{model_m1_n:.0f}} | {{model_m1_rank_scaled:.0f}} of {{model_m1_n_scaled:.0f}} |
| **M2** | + bigger zones react more to the gold price | {{model_m2_during_net}} | {{model_m2_later_net:+,.0f}} | {{model_m2_placebo_net:+,.0f}} | {{model_m2_rank:.0f}} of {{model_m2_n:.0f}} | {{model_m2_rank_scaled:.0f}} of {{model_m2_n_scaled:.0f}} |
| **M3** | + each zone's own trend | {{model_m3_during_net}} | {{model_m3_later_net:+,.0f}} | {{model_m3_placebo_net:+,.0f}} | {{model_m3_rank:.0f}} of {{model_m3_n:.0f}} | {{model_m3_rank_scaled:.0f}} of {{model_m3_n_scaled:.0f}} |
| **M4** | Scaled to each zone's size | {{model_m4_during_net:.2f}} | {{model_m4_later_net:.2f}} | {{model_m4_placebo_net:.2f}} | — | {{model_m4_rank:.0f}} of {{model_m4_n:.0f}} |

- **M3 with trends fitted on pre-years only:** {{model_m3pre_during_net}} ha/yr in 2019–21; it extrapolates a slope, so the causal range does not use it.
- **Fake dates:** M1 and M2 placebos have the opposite sign; M3's and M4's have the same sign as the real effect, so not every model passes cleanly.

**Level 3: per 1-km cell (net additions)**

:::fig output/fig_v2_stats_zones.png
read: Change in net additions per 1-km cell, 2019–21 (filled) and 2022–25 (open) vs 2014–18, relative to comparison cells with little mining, 95% intervals (errors clustered by 10-km blocks).
take: La Pampa's cells fell and the corridor across the road rose in 2019–21. Because the comparison cells hold almost no mining, each point is close to the zone's own before/after: the p-values overstate.
:::

:::fig output/fig_v2_stats_event.png
read: Year-by-year net additions per cell vs the pooled 2014–18 mean (= 0), La Pampa sector and corridor across the road, 95% intervals. The panel titles test only the 2011–13 leads.
take: La Pampa's cells are below 2014–18 from 2019 and the corridor's above. With the 2010 lead added, the pre-trend test fails for La Pampa (p = {{st_event_lapampa_pretrend2010_net_p:.3f}}) and for the corridor across the road (p = {{st_event_corridor_across_pretrend2010_net_p:.3f}}): neither panel title's verdict holds on both windows.
:::

- **Panel:** {{st_n_cells:,.0f}} cells, 2014–2025 (reference 2014–18); cell and year fixed effects; errors clustered by 10 × 10 km blocks ({{st_n_clusters:.0f}} clusters).
- **Comparison cells:** other protected areas, other buffer zones and the rest of Madre de Dios with no corridor or community tenure ({{st_n_ref_cells_clean:,.0f}} cells). They hold almost no mining ({{st_n_ref_cells_depleted18:.0f}} had any by 2018), so each coefficient is close to the zone's own before/after.

| Per 1-km cell, net additions, ha/yr vs 2014–18 | 2019–21 | 2022–25 |
|---|---:|---:|
| La Pampa sector | {{st_main_lapampa_during_net:+.2f}} | {{st_main_lapampa_later_net:+.2f}} |
| Corridor across the road | {{st_main_corridor_across_during_net:+.2f}} | {{st_main_corridor_across_later_net:+.2f}} |
| Rest of Tambopata buffer zone | {{st_main_tambopata_bz_rest_during_net:+.2f}} | {{st_main_tambopata_bz_rest_later_net:+.2f}} |
| Amarakaeri buffer zone | {{st_main_amarakaeri_bz_during_net:+.2f}} | {{st_main_amarakaeri_bz_later_net:+.2f}} |
| Tambopata reserve | {{st_main_tambopata_nr_during_net:+.2f}} | {{st_main_tambopata_nr_later_net:+.2f}} |

- **La Pampa's parts, 2019–21:** new land {{st_main_lapampa_during_new:+.2f}}, re-mined {{st_main_lapampa_during_remined:+.2f}}, stopped {{st_main_lapampa_during_stopped:+.2f}} ha per cell-year.
- **p-values** (clustered; wild cluster bootstrap with {{st_clusters_lapampa:.0f}} La Pampa blocks): La Pampa p = {{st_main_lapampa_during_net_p:.3f}} (bootstrap {{st_wcb_lapampa_during_net_p:.3f}}); corridor across the road p = {{st_main_corridor_across_during_net_p:.3f}} (bootstrap {{st_wcb_corridor_across_during_net_p:.3f}}). They test a before/after, not an effect; keep them out of headlines.
- **Variants:** gold-bearing bins × year {{st_gold_lapampa_during_net:+.2f}}; 2018-depletion bins × year {{st_depbin_lapampa_during_net:+.2f}}; on an at-risk (hazard) basis {{st_hazard_ols_lapampa_during:+.2f}} points (p = {{st_hazard_ols_lapampa_during_p:.2f}}): the cell-level fall in new land disappears once depletion is allowed for.
- **Pre-trends, both lead windows:** La Pampa 2011–13 p = {{st_event_lapampa_pretrend_net_p:.2f}}, 2010–13 p = {{st_event_lapampa_pretrend2010_net_p:.3f}}; corridor across the road 2011–13 p = {{st_event_corridor_across_pretrend_net_p:.2f}}, 2010–13 p = {{st_event_corridor_across_pretrend2010_net_p:.3f}}. La Pampa passes only with 2011+ leads; the corridor fails on net either way.

**Code:** `code/peru.py`, `code/peru_models.py`, `code/peru_robust.py`, `code/v2_stats.py`.
:::

:::more Attempt 2, synthetic control: no mix of zones reaches the target's size
**No weighted mix of Peruvian buffer zones reaches the Tambopata buffer zone's size, so synthetic control adds only a misfit.** [[D]]

:::fig output/fig_peru_synth.png
read: Synthetic control on net additions, fit 2014–18. Left: hectares; right: each zone scaled to its own 2014–18 mean. Top: the Tambopata buffer zone vs its synthetic copy; bottom: the gap, with grey lines for each donor posing as the target.
take: In hectares the copy never comes close before 2019, so the gap is a misfit. Scaled, the fit is loose and four donors prove little.
:::

- **In hectares, no fit:** in 2014–18 the Tambopata buffer zone averaged {{synth_core_add_pre_mean_tam}} ha/yr of net additions; the best mix of core donors {{synth_core_add_pre_mean_synth}} ha/yr. It lay outside every donor's range in {{synth_core_add_hull_years_outside:.0f}} of 5 fit years. [[D]]
- **The {{synth_ext_add_gap_during}} is Amarakaeri:** with Amarakaeri allowed as a donor, the solver puts all weight on it ({{synth_ext_add_w1:.0%}}), and the 2019–21 gap ({{synth_ext_add_gap_during}} ha/yr) is just Tambopata minus Amarakaeri. [[D]]
- **Scaled:** the 2019–21 gap ranks {{synth_core_addsc_rank_gap:.0f}} of {{synth_core_addsc_n_units_ranked:.0f}}. [[D]]
- **What it is:** a fake Tambopata built from a weighted mix of other zones (weights ≥ 0, summing to 1), fitted to the years before 2019. You can't average small numbers into a big one; that's why Attempt 1 compares *changes*, and why Attempt 3 had to look abroad.

**Code:** `code/peru_synth.py`.
:::

:::more Attempt 3, rule-based twins: no untouched twin exists; three relaxed twins grew faster
**No area in the Amazon passes all four of Ruby's rules. Allow verified operations after 2021, and three Brazilian twins pass.** On another product, Amazon Mining Watch (AMW), the Tambopata buffer zone added new area in 2019–21 at {{top3_ratio:.0%}} of the twins' mean pace, or {{top3_ratio_excl_unverified:.0%}} without Munduruku. [[D]]

**The rules (Ruby):** find one existing area with (R1) at least 500 ha of mining by 2018, (R2) no verified operation in 2017–25, (R3) outside Madre de Dios, and (R4) lowland mining at least a fifth of La Pampa's size. One dating rule (R*) for every operation: the first *verified* one.

:::fig output/fig_control_funnel.png
read: Areas left after each rule (log scale), from all protected areas, buffer zones and indigenous territories with polygons.
take: Almost every big mining area in the Amazon got an operation, so no strict twin survives; allowing operations after 2021 lets three pass.
:::

:::fig output/fig_control_map.png
read: Each dot is an area with at least 500 ha of mining by 2018 (AMW); size = hectares, colour = operation status.
take: Peru outside Madre de Dios has no big mining area; the candidates cluster in Brazil's Tapajós gold region, at least 1,300 km away.
:::

:::fig output/fig_control_compare.png
read: Left: AMW new area per year as a share of each area's own 2018 AMW area, 2019–2025 (comparable to new land, not to net additions). Right: mining stock, 2018 = 100, each area from its own MapBiomas collection, side by side, never subtracted.
take: In 2019–21 the Tambopata buffer zone ran at about a third of Amanã's pace; before 2019 both stocks grew alike from 2013.
:::

:::fig output/fig_control_top3.png
read: The Tambopata buffer zone against the three twins: mining stock index (left, two collections) and AMW new area as % of own 2018 area (right).
take: All three twins added new area faster than Tambopata in 2019–21; Munduruku was booming, which drives the {{top3_ratio:.0%}} headline.
:::

- **Relaxed rule:** verified operations after 2021 allowed. {{ctl_n_relaxed:.0f}} areas pass: **Amanã National Forest**, the Tapajós protection area and Munduruku (whose 2021 report is unverified; {{ctl_n_relaxed_excl_unverified:.0f}} pass if an unverified report disqualifies). [[D]]
- **2019–21, AMW new area as % of own 2018 AMW area per year:** Tambopata {{top3_tam_during:.1f}}%; Amanã {{top3_amana_twin_during:.1f}}%; Tapajós {{top3_tapajos_twin_during:.1f}}%; Munduruku {{top3_munduruku_twin_during:.0f}}%. Against Amanã alone: {{ctl_relaxed_during_ratio:.0%}}. [[D]]
- **The funnel:** {{ctl_n_areas:,.0f}} protected areas, buffer zones and indigenous territories screened. {{ctl_n_r1:.0f}} had real mining before 2019; {{ctl_n_r2:.0f}} of those had no verified operation, and it fails the size rule; {{ctl_n_r1_unclear_or_unsearched:.0f}} more were unclear or not searched. [[D]]
- **Sources:** SERNANP (Peru), RAISG (other countries), FUNAI (Brazil's territories); AMW for mining; a logged web search per area for operations; OpenTopoData for elevation.

| | Tambopata buffer zone | Amanã National Forest |
|---|---:|---:|
| Mining by 2018 (AMW, ha) | {{ctl_tam_stock_2018}} | {{ctl_relaxed_stock_2018}} |
| Median elevation of the mining (m) | {{ctl_tam_elev_m}} | {{ctl_relaxed_elev_m}} |
| Distance from La Pampa (km) | 0 | {{ctl_relaxed_dist_km}} |
| First operation found | Feb 2019 | Mar 2023 |

- **Stock index (2018 = 100):** 2014 Tambopata {{ctl_mb_tam_index_2014:.0f}}, Amanã {{ctl_mb_twin_index_2014:.0f}}; 2021 Tambopata {{ctl_mb_tam_index_2021:.0f}}, Amanã {{ctl_mb_twin_index_2021:.0f}}. [[D]]
- **After 2021 the twins are spoiled:** they had their own operations from 2023. Use them for 2019–21 only.

| Twin | Mean growth gap before 2019 (log points/yr; p) | Trend in that gap (p) | 2019–21 pace, % of 2018 stock | Gap vs Tambopata (pp) |
|---|---:|---:|---:|---:|
| Amanã National Forest | {{top3_amana_pre_growth_diff:+.2f}} ({{top3_amana_pre_growth_p:.2f}}) | {{top3_amana_pre_trend_p:.3f}} | {{top3_amana_twin_during:.1f}} | {{top3_amana_during_gap:+.1f}} |
| Tapajós protection area | {{top3_tapajos_pre_growth_diff:+.2f}} ({{top3_tapajos_pre_growth_p:.2f}}) | {{top3_tapajos_pre_trend_p:.3f}} | {{top3_tapajos_twin_during:.1f}} | {{top3_tapajos_during_gap:+.1f}} |
| Munduruku territory | {{top3_munduruku_pre_growth_diff:+.2f}} ({{top3_munduruku_pre_growth_p:.2f}}) | {{top3_munduruku_pre_trend_p:.3f}} | {{top3_munduruku_twin_during:.0f}} | {{top3_munduruku_during_gap:+.0f}} |

- **Reading the pre-2019 tests:** the growth gap is Tambopata's stock growth minus the twin's, 2010–18. Its mean says Tambopata grew faster on average; the trend test says the gap was shrinking year by year. Either way the paths were not parallel.
- **No p-values for the 2019–21 gap:** three years per area make a t-test unreliable.
- **Threats:** Brazil's enforcement in 2019–22 may have let the twins grow faster than "normal". "No operation found" is not proof of none. Two products (Peru Collection 4, Amazonía Collection 6) for the stock index.
- **Ruby's caution holds:** "no intervention" is too strict (no area passes); "comparable enforcement" needs zone-level enforcement data that isn't public.

**Code:** `code/control_amw.py`, `control_elevation.py`, `control_mb_amazonia.py`, `control_select.py`, `control_top3.py`. Searches: `docs/walkthrough/notes/control_interventions.csv`, coded in `data_intermediate/operations_coded.csv`.
:::

:::more Attempt 4, spatial RD: at the road the gap opened, weakly on net; at the reserve edge we can't tell
**A spatial regression discontinuity compares land just either side of a legal border, before and after Mercurio.** On net additions, the gap at the road rose by {{rd_road_did_net:+.1f}} points of land per year (p = {{rd_road_did_net_p:.2f}}); at the reserve edge it changed by {{rd_reserve_did_net:+.1f}} (p = {{rd_reserve_did_net_p:.2f}}). Neither is informative on its own. [[D]]

:::fig output/fig_v2_rdd.png
read: Net additions (% of land per year) by distance from each border (left; dashed = 2014–18, solid = 2019–21, lines = local fits on each side), and the gap at the border each year with 95% intervals (right). Top: the road (La Pampa south, legal mining corridor north). Bottom: the reserve edge (buffer zone outside, reserve inside).
take: At the road, the south side mined more before Mercurio and the north side after, but the yearly gaps have wide intervals and peak in 2021. At the reserve edge nothing stands out.
:::

- **The road, net additions within {{rd_road_did_h:.1f}} km:** south (La Pampa) {{rd_road_mean_pre_l_net:.1f}}% of land a year in 2014–18, north {{rd_road_mean_pre_r_net:.2f}}%; in 2019–21 south {{rd_road_mean_post_l_net:.1f}}%, north {{rd_road_mean_post_r_net:.1f}}%. [[D]]
- **The change in the gap:** {{rd_road_did_net:+.1f}} points (95% interval {{rd_road_did_net_lo:+.1f}} to {{rd_road_did_net_hi:+.1f}}; p = {{rd_road_did_net_p:.2f}}). For new land alone it is {{rd_road_did_new:+.1f}} (p = {{rd_road_did_new_p_fixedh:.2f}} at the fixed bandwidth). 2019 alone: {{rd_road_did2019_net:+.1f}} (p = {{rd_road_did2019_net_p:.2f}}). [[D]]
- **The reserve edge:** {{rd_reserve_did_net:+.1f}} points (95% interval {{rd_reserve_did_net_lo:+.1f}} to {{rd_reserve_did_net_hi:+.1f}}). We cannot tell whether buffer-zone enforcement shielded the reserve. [[D]]
- **The idea:** land 200 m north of the road and 200 m south of it has the same soil, rivers and gold, but a different legal status. At the road, the line also changes access; at the reserve, the Malinowski River runs along the edge. Those don't change over time, so we take the **change in the gap**, after 2019 minus before: a *difference in discontinuities* (Grembi, Nannicini & Troiano, 2016).
- **Set-up:** 250-m distance bins inside 2-km segments along each border (road: {{rd_road_did_n:.0f}} units within the bandwidth; reserve: {{rd_reserve_did_n:.0f}}); net additions as % of each unit's land per year; `rdrobust` (Calonico, Cattaneo & Titiunik), local linear, triangular kernel, MSE-optimal bandwidth (road {{rd_road_did_h:.1f}} km, reserve {{rd_reserve_did_h:.1f}} km), robust bias-corrected intervals, errors clustered by segment.

| Check (net additions) | Road | Reserve edge |
|---|---:|---:|
| Gap 2014–18 (north − south / inside − outside) | {{rd_road_level_pre_net:+.2f}} (p = {{rd_road_level_pre_net_p:.2f}}) | {{rd_reserve_level_pre_net:+.2f}} (p = {{rd_reserve_level_pre_net_p:.2f}}) |
| Gap 2019–21 | {{rd_road_level_post_net:+.2f}} (p = {{rd_road_level_post_net_p:.2f}}) | {{rd_reserve_level_post_net:+.2f}} (p = {{rd_reserve_level_post_net_p:.2f}}) |
| **Change in the gap, 2019–21 vs 2014–18** | **{{rd_road_did_net:+.2f}}** (p = {{rd_road_did_net_p:.2f}}) | **{{rd_reserve_did_net:+.2f}}** (p = {{rd_reserve_did_net_p:.2f}}) |
| Change, 2022–25 vs 2014–18 | {{rd_road_didlater_net:+.2f}} (p = {{rd_road_didlater_net_p:.2f}}) | {{rd_reserve_didlater_net:+.2f}} (p = {{rd_reserve_didlater_net_p:.2f}}) |
| Fixed bandwidth 1 / 2 / 3 / 5 km | {{rd_road_sens_h1_net:+.1f}} / {{rd_road_sens_h2_net:+.1f}} / {{rd_road_sens_h3_net:+.1f}} / {{rd_road_sens_h5_net:+.1f}} | {{rd_reserve_sens_h1_net:+.1f}} / {{rd_reserve_sens_h2_net:+.1f}} / {{rd_reserve_sens_h3_net:+.1f}} / {{rd_reserve_sens_h5_net:+.1f}} |
| p across bandwidths and a 500-m donut | {{rd_road_sens_p_min:.2f}}–{{rd_road_sens_p_max:.2f}} | {{rd_reserve_sens_p_min:.2f}}–{{rd_reserve_sens_p_max:.2f}} |
| Fake start years (rank of the real change) | {{rd_road_fake_rank:.0f}} of {{rd_road_fake_n:.0f}} (p = {{rd_road_fake_p:.2f}}) | {{rd_reserve_fake_rank:.0f}} of {{rd_reserve_fake_n:.0f}} (p = {{rd_reserve_fake_p:.2f}}) |
| Fake borders ±2–4 km, significant | {{rd_road_pb_n_sig:.0f}} of 6 | {{rd_reserve_pb_n_sig:.0f}} of 6 |

- **Perpendicular distance to the road** instead of the north-south offset: {{rd_roadperp_did_net:+.1f}} (p = {{rd_roadperp_did_net_p:.2f}}).
- **The big limit: displacement breaks the RD.** An RD assumes one side doesn't affect the other. Here net additions fell south and rose north, so the gap opens from both sides at once. The road estimate is the **swing**, an upper bound on what happened on either side alone.

**Code:** `code/v2_rdd.py` (table `output/table_rdd.csv`).
:::

:::more Attempt 5, matching: every method finds Tambopata slower; none beats chance
**We let matching methods pick the Tambopata buffer zone's comparison areas instead of hand-set rules.** On AMW new area (another product), all {{psm_n_methods:.0f}} methods with a result find Tambopata at {{psm_ratio_min:.0%}}–{{psm_ratio_max:.0%}} of its matches' pace in 2019–21. But areas with no operation often look just as "slow" against their own matches. [[D]]

:::fig output/fig_psm.png
read: Left: AMW new area per year in 2019–21 as % of each area's own 2018 AMW area. Orange line = Tambopata buffer zone; violet dots = the areas each method picks (first row: Ruby's rule-based twin). Right: Tambopata's gap (orange) against the gaps when each pool area plays "treated" (grey bars).
take: Every method finds Tambopata slower than its matches, but the gap sits inside the placebo range (p {{psm_p_min:.2f}}–{{psm_p_max:.2f}}). Propensity-score matching finds no area within the caliper.
:::

- **Same measure as the twins:** Tambopata added {{psm_tam_pace_during:.1f}}% of its 2018 AMW area per year in 2019–21; its matches {{psm_maha1_ctl_during:.0f}}–{{psm_cem_ctl_during:.0f}}%. [[D]]
- **Placebo fails for all:** p = {{psm_p_min:.2f}} to {{psm_p_max:.2f}}; {{psm_n_methods_p10:.0f}} of {{psm_n_methods:.0f}} reach p ≤ 0.10. [[D]]
- **No common support:** Tambopata's propensity score ({{psm_ps_tam:.2f}}) is above every area in the pool (max {{psm_ps_pool_max:.2f}}); both propensity-score methods find no match within the caliper.
- **Pool:** {{psm_n_units:.0f}} Amazon areas with AMW data; {{psm_n_pool:.0f}} with no operation in 2017–21, at least 100 ha of mining by 2018, and outside Madre de Dios. **Propensity score:** a ridge-penalised logit of "operation reported 2017–21" on pre-2019 traits (log mining stock in 2018, median elevation of the mining, log area, country and area type), fitted on the {{psm_ps_n:.0f}} areas with a known status ({{psm_ps_n_treated:.0f}} with an operation; pseudo-R² {{psm_ps_pseudo_r2:.2f}}).

| Method | Matches | Their pace, % per yr | Gap (pp) | Pace ratio | Placebo rank | p |
|---|---:|---:|---:|---:|---:|---:|
| Rule-based twin (Amanã) | {{psm_twin_n_ctl:.0f}} | {{psm_twin_ctl_during:.1f}} | {{psm_twin_gap_during:+.1f}} | {{psm_twin_ratio_during:.2f}} | — | — |
| Propensity score, nearest 1 or 5 | 0 | — | — | — | no match within the caliper | — |
| Mahalanobis, nearest 1 | {{psm_maha1_n_ctl:.0f}} | {{psm_maha1_ctl_during:.1f}} | {{psm_maha1_gap_during:+.1f}} | {{psm_maha1_ratio_during:.2f}} | {{psm_maha1_rank:.0f}} of {{psm_maha1_n_placebo:.0f}} | {{psm_maha1_p:.2f}} |
| Mahalanobis, nearest 3 | {{psm_maha3_n_ctl:.0f}} | {{psm_maha3_ctl_during:.1f}} | {{psm_maha3_gap_during:+.1f}} | {{psm_maha3_ratio_during:.2f}} | {{psm_maha3_rank:.0f}} of {{psm_maha3_n_placebo:.0f}} | {{psm_maha3_p:.2f}} |
| Coarsened exact matching | {{psm_cem_n_ctl:.0f}} | {{psm_cem_ctl_during:.1f}} | {{psm_cem_gap_during:+.1f}} | {{psm_cem_ratio_during:.2f}} | {{psm_cem_rank:.0f}} of {{psm_cem_n_placebo:.0f}} | {{psm_cem_p:.2f}} |
| Entropy balancing (closest) | {{psm_ebal_n_ctl:.0f}} | {{psm_ebal_ctl_during:.1f}} | {{psm_ebal_gap_during:+.1f}} | {{psm_ebal_ratio_during:.2f}} | {{psm_ebal_rank:.0f}} of {{psm_ebal_n_placebo:.0f}} | {{psm_ebal_p:.2f}} |
| Inverse-probability weighting | {{psm_ipw_n_ctl:.0f}} | {{psm_ipw_ctl_during:.1f}} | {{psm_ipw_gap_during:+.1f}} | {{psm_ipw_ratio_during:.2f}} | {{psm_ipw_rank:.0f}} of {{psm_ipw_n_placebo:.0f}} | {{psm_ipw_p:.2f}} |

- **What each does:** *propensity score* matches on the predicted chance of getting an operation; *Mahalanobis* on distance in the traits themselves; *coarsened exact matching* on identical bins (stock, lowland); *entropy balancing* reweights the pool so its average traits equal Tambopata's; *IPW* weights every pool area by its odds of being treated.
- **With one treated area, matching collapses to a distance rule.** Entropy balancing can't reach exact balance (largest remaining gap {{psm_ebal_max_imbalance:.2f}} SD); coarsened exact matching with an area bin finds {{psm_cem3_n_matches:.0f}} areas, the same verdict as the strict rules.

**Code:** `code/control_psm.py` (results `output/psm_results.csv`, balance `output/table_psm_balance.csv`).
:::

:::more Attempt 6, synthetic DiD: same answer as M1, same caveats
**Synthetic difference-in-differences weights the other zones and the pre-years, then compares changes.** On net additions: {{sdid_sdid_ha_during_net}} ha/yr in 2019–21, raw rank {{sdid_sdid_ha_during_rank:.0f}} of {{sdid_sdid_ha_during_n:.0f}}; scaled to size, rank {{sdid_sdid_scaled_during_rank:.0f}} of {{sdid_sdid_scaled_during_n:.0f}}. [[D]]

:::fig output/fig_sdid.png
read: Left: net additions in the Tambopata buffer zone vs the synthetic-DiD comparison (shifted to Tambopata's level), 2014–25; grey bars are the time weights on each pre-2019 year. Right: the 2019–21 estimate with each other zone "treated".
take: The comparison is nearly flat, so the estimate is mostly Tambopata's own before/after; the time weight sits almost entirely on 2014.
:::

- **Three estimators, one function:** plain DiD {{sdid_did_ha_during_net}}, synthetic control {{sdid_sc_ha_during_net}}, synthetic DiD {{sdid_sdid_ha_during_net}} ha/yr (2019–21). [[D]]
- **Later years:** {{sdid_sdid_ha_later_net:+,.0f}} ha/yr in 2022–25; {{sdid_sdid_ha_later_ex2023_net:+,.0f}} without 2023. [[D]]
- **Sensitive to the window:** fitting on 2011–18 instead of 2014–18 gives {{sdid_sdid_ha_during_pre2011_net}} ha/yr.
- **Weights:** unit weights non-negative, summing to 1, chosen to make the comparison parallel to Tambopata in 2014–18; they explain only {{sdid_pre_fit_r2:.0%}} of its pre-2019 variation. Time weights: {{sdid_lambda_max:.0%}} on 2014, {{sdid_lambda_2018:.0%}} on 2018. The largest single zone weight is {{sdid_top_weight:.0%}}; {{sdid_n_weighted:.0f}} zones get more than 1%. With equal weights the estimator equals M1 exactly (asserted in the code).
- **Reference:** Arkhangelsky, Athey, Hirshberg, Imbens & Wager (2021), *American Economic Review* 111(12).

**Code:** `code/peru_sdid.py` (own implementation; results `output/peru_sdid.csv`).
:::

:::more Which attempt answers which question, and what we didn't try
| Question | Best attempt | Why |
|---|---|---|
| Did the target fall more than elsewhere? | 1 and 6 | Many comparison zones, placebo ranks |
| Did it fall more than a look-alike? | 3 and 5 | Real areas abroad, picked by rules or algorithms |
| Did miners cross the legal line? | 4 | Same land either side of one border |
| Did the reserve border hold? | 4 | The reserve edge as a border |

**Not tried, and why:**
- **Callaway–Sant'Anna or Sun–Abraham:** built for many units treated at different dates. Peru has one; Brazil's staggered version is done (did2s, see [Limits](#limits)).
- **Synthetic control with prediction intervals (conformal inference):** needs a good pre-fit, which Attempt 2 can't get in hectares.
- **Bayesian structural time series (CausalImpact):** same donor problem as Attempt 2, with stronger assumptions.
- **Instrumental variables** (e.g. gold price × gold geology): the gold price drives mining directly, so the exclusion restriction fails.
- **Spatial DiD with spillover rings (Butts, 2023):** partly done as the road gradient in the cell panel.
:::

## The claim | In hectares the fall stands out; for its size, not

**The one causal sentence, conditional:** *if* the other Peruvian buffer zones show what the Tambopata buffer zone would otherwise have done, Mercurio and the operations that followed lowered its net mining additions by about **{{model_m1_during_net:,.0f|abs}} to {{did_base2014_net:,.0f|abs}} ha/yr in 2019–21** (low end: Tambopata vs 14 other Peruvian buffer zones, M1; high end: the 2×2 vs Amarakaeri on a 2014–18 baseline). [[C]]

- **What it is made of:** {{tambopata_bz_stopped_share_of_fall_min:.0%}}–{{tambopata_bz_stopped_share_of_fall_max:.0%}} of the target's own 2016–18 to 2019–21 fall is land stopping; the rest is less new clearing. In the M1 model, stopped land is {{model_m1_during_stopped:,.0f}} of the {{model_m1_during_net:,.0f|abs}} ha/yr. That is a different comparison (against 14 zones, 2014–18 reference), not a contradiction of the range. [[D]]
- **In hectares it stands out:** rank {{model_m1_rank:.0f}} of {{model_m1_n:.0f}}, Tambopata vs 14 other Peruvian buffer zones. But it ranked first in hectares in 2014, 2015 and 2016 too, before Mercurio. [[D]]
- **For its size it doesn't:** scaled to each zone's normal additions, it ranks {{model_m4_rank:.0f}}rd–{{placebo_space_rank_scaled:.0f}}th of 7 depending on the scaling. [[D]]
- **COVID overlaps:** new land fell only from 2020. We cannot separate the operation from COVID ([Limits](#limits)).

:::fig output/fig_placebo_explainer.png
read: Each row runs one analysis many times. Grey dots: the fakes (another zone gets the "operation", or the operation "starts" in another year). Orange: the real result. Rows 1–2: net additions, Tambopata vs 14 other Peruvian buffer zones, 2019–21 gap, in hectares and scaled to each zone's size. Row 3: the jump in the north-of-road share of new land at La Pampa's longitudes.
take: In hectares the Tambopata buffer zone is far outside every fake, because it is far bigger. Scaled to size, two fake zones fall as much. At the road, the 2019 jump beats every clean fake start year, but there are only a few.
:::

**Other estimates, and why they are not the range:**
- **2×2 vs Amarakaeri, 2016–18 baseline:** {{did_main_net}} ha/yr. Three base years include the 2017 peak, the year La Pampa was picked for; the 2014–18 baseline weighs it less.
- **M2 (bigger zones react more to the gold price):** {{model_m2_during_net}} ha/yr; inside the range.
- **Synthetic DiD:** {{sdid_sdid_ha_during_net}} ha/yr; inside the range, but its weights barely track Tambopata (sensitivity only).
- **M3 (each zone's own trend):** {{model_m3_during_net}} ha/yr; it extrapolates a slope, and its fake 2016 start has the same sign.
- **Synthetic control:** {{synth_ext_add_gap_during}} ha/yr; all weight on Amarakaeri and no pre-2019 fit: a misfit.

**Why it matters:** read the range as an upper bound for 2019–21 only. It tells FZS an operation can go with a large, short pause in the target, not that the region mined less.

:::more Placebos: what a fake test shows, and every one we ran
**A placebo runs the same analysis where nothing happened. If the fakes look as big as the real result, the real result can't be told from noise.** We use placebos instead of standard errors, because one treated zone makes standard errors uninformative (Conley & Taber, 2011).

- **Fake place:** give "Mercurio" to another zone. **Fake date:** pretend it started in 2016. **Fake border:** move the border 2–4 km into one side.
- **How:** run the identical analysis on every fake, line them up, and rank the real one. Rank 1 of {{plc_m1_n:.0f}} means p = 1/{{plc_m1_n:.0f}} = {{model_m1_ri_p:.2f}}, the floor.
- **The size problem:** in hectares the Tambopata buffer zone ranks first even before Mercurio: rank {{placebo_space_rank_raw_preyear_2014:.0f}} in 2014, {{placebo_space_rank_raw_preyear_2015:.0f}} in 2015, {{placebo_space_rank_raw_preyear_2016:.0f}} in 2016; only in the 2017 boom year does it rank last ({{placebo_space_rank_raw_preyear_2017:.0f}}). So the raw rank measures size as much as effect.
- **A pass shows the real result is unusual,** not that Mercurio caused it. **A fail is decisive:** scaled to size, the M4 model ranks {{plc_m4_rank:.0f}} of {{plc_m4_n:.0f}} (p = {{model_m4_ri_p:.2f}}): ordinary. **The floor:** with {{plc_m1_n:.0f}} zones, p can't go below {{model_m1_ri_p:.2f}}; with {{plc_road_n:.0f}} clean start years at the road, not below 1/{{plc_road_n:.0f}}.

| Analysis | Placebo | Real result | Placebo result |
|---|---|---|---|
| 2×2 vs Amarakaeri (net, 2016–18 baseline) | fake date 2016 (2013–15 vs 2016–18) | {{did_main_net}} ha/yr | {{did_placebo_net:+,.0f}} (opposite sign: pass) |
| Model ladder M1 (net, ha) | fake places (14 zones) | {{model_m1_during_net}} ha/yr | range {{model_m1_placebo_min_net:,.0f}} to +{{model_m1_placebo_max_net:,.0f}}; raw rank {{model_m1_rank:.0f}} of {{model_m1_n:.0f}}; scaled {{model_m1_rank_scaled:.0f}} of {{model_m1_n_scaled:.0f}} |
| Model ladder M1 | fake date (2016, on 2011–18) | {{model_m1_during_net}} ha/yr | {{model_m1_placebo_net:+,.0f}} (opposite sign: pass) |
| Model ladder M3 (own trends) | fake date | {{model_m3_during_net}} ha/yr | {{model_m3_placebo_net:+,.0f}} (same sign: weak fail) |
| Model ladder M4 (scaled) | fake places (6 zones) | {{model_m4_during_net:.2f}} normal years | rank {{model_m4_rank:.0f}} of {{model_m4_n:.0f}} (fail) |
| Event study (pooled 2014–18 reference) | fake places, scaled | {{es_poolB_pooledref_during_net}} ha/yr | scaled rank {{placebo_space_rank_scaled:.0f}} of {{placebo_space_n_scaled:.0f}} |
| Every 2019–21 year vs every 2011–18 year | placebo in time | largest 2019–21 year {{tambopata_bz_net_max_during}} ha | smallest 2011–18 year {{tambopata_bz_net_min_2011_18}} ha |
| Context models K0–K3 | fake places | {{ctx_k3_during_net}} ha/yr (K3) | raw rank {{ctx_k3_rank:.0f}} of {{ctx_n:.0f}}; scaled {{ctx_k3_rank_scaled:.0f}} of {{ctx_n_scaled:.0f}} |
| Road: north-of-road share, net additions | clean fake start years | rank {{t1_road_shift_rank_clean_net:.0f}} | of {{t1_road_shift_n_clean_net:.0f}} (p = {{t1_road_shift_ri_p_clean_net:.2f}}) |
| Spatial RD at the road (net) | fake start years {{rd_road_fake_first_year:.0f}} on | {{rd_road_did_net:+.1f}} pts | rank {{rd_road_fake_rank:.0f}} of {{rd_road_fake_n:.0f}} (p = {{rd_road_fake_p:.2f}}) |
| Spatial RD at the road (net) | fake borders ±2–4 km | {{rd_road_did_net:+.1f}} pts | largest {{rd_road_pb_max_abs:.1f}}; {{rd_road_pb_n_sig:.0f}} of 6 significant |
| Spatial RD at the reserve edge (net) | fake start years | {{rd_reserve_did_net:+.1f}} pts | rank {{rd_reserve_fake_rank:.0f}} of {{rd_reserve_fake_n:.0f}} (p = {{rd_reserve_fake_p:.2f}}) |
| Cell panel, La Pampa (net) | pre-trend leads | {{st_main_lapampa_during_net:+.2f}} ha/cell | 2011–13 leads p = {{st_event_lapampa_pretrend_net_p:.2f}} (pass); 2010–13 p = {{st_event_lapampa_pretrend2010_net_p:.3f}} (fail) |
| Synthetic DiD (net) | fake places | {{sdid_sdid_ha_during_net}} ha/yr | raw rank {{sdid_sdid_ha_during_rank:.0f}} of {{sdid_sdid_ha_during_n:.0f}}; scaled {{sdid_sdid_scaled_during_rank:.0f}} of {{sdid_sdid_scaled_during_n:.0f}} |
| Matching (AMW measure) | each pool area as "treated" | Tambopata slower | p {{psm_p_min:.2f}}–{{psm_p_max:.2f}} |

**Two kinds of placebo answer two questions.** Fake places ask "is the Tambopata buffer zone special?" (yes, in size). Fake dates ask "is 2019 special?" (yes: every 2019–21 year is below every 2011–18 year). A result that passes both can still be explained by something else that hit the target in 2019–21, such as COVID, which is why the claim stays conditional.

**How to read p:** below 0.05 = unlikely to be chance. With {{model_m1_n:.0f}} zones the smallest possible placebo p is {{model_m1_ri_p:.2f}}, and in hectares that rank measures size.

**Code:** `code/placebo_explainer.py` (figure), `code/peru.py`, `code/peru_models.py`, `code/v2_tests.py`, `code/v2_rdd.py`.
:::

:::more Do COVID and money explain it? We cannot separate them
**We added each zone's COVID exposure and Madre de Dios's enforcement money (PP 0128) as controls. The two controls push the 2019–21 gap in opposite directions, so a stable gap proves nothing.** [[D]]

:::fig output/fig_peru_context_models.png
read: Left: the Tambopata buffer zone's 2019–21 coefficient on net additions, Tambopata vs 14 other Peruvian buffer zones, 2015–25, as controls are added: K0 = gold price × size; K1 + COVID 2020–21 × size; K2 + Madre de Dios × enforcement money; K3 both. Right: each year's gap against the money booked that year.
take: The COVID term moves the gap by {{ctx_shift_covid_during_net:+,.0f}} ha/yr and the money term by {{ctx_shift_money_during_net:+,.0f}} ha/yr: they offset, so K3 ≈ K0 proves nothing. Money is partly the treatment itself.
:::

- **Coefficients, net additions, 2019–21:** K0 {{ctx_k0_during_net}}, K1 {{ctx_k1_during_net}}, K2 {{ctx_k2_during_net}}, K3 {{ctx_k3_during_net}} ha/yr; raw rank {{ctx_k3_rank:.0f}} of {{ctx_n:.0f}}, scaled rank {{ctx_k3_rank_scaled:.0f}} of {{ctx_n_scaled:.0f}}. [[D]]
- **No dose-response:** the yearly gap and spending correlate at r = {{ctx_dose_corr:.2f}} (2015–25). [[D]]
- **Why controlling for money is tricky:** spending rose with Mercurio. Controlling for it removes part of the effect we measure. The spending coefficient is {{ctx_k2_spend_coef:+.0f}} ha/yr per log-point, consistent with money following mining; we cannot tell the direction.
- **Politics:** presidents and laws hit every zone at once; with one region they cannot be tested separately.

**Code:** `code/peru_context_models.py`.
:::

:::more Every claim: what we can say, how strongly, and the test behind it
| Claim | Label | Key test | Evidence against |
|---|---|---|---|
| Net additions in the Tambopata buffer zone collapsed in 2019–21 ({{tambopata_bz_pre_net}} → {{tambopata_bz_during_net}} ha/yr) while Amarakaeri rose ({{amarakaeri_bz_pre_net}} → {{amarakaeri_bz_during_net}} ha/yr) | [[D]] | Raster = course table (reproduction check); every 2019–21 year below every 2011–18 year | Ranked first in hectares before 2019 too |
| A quarter to a half of that fall ({{tambopata_bz_stopped_share_of_fall_min:.0%}}–{{tambopata_bz_stopped_share_of_fall_max:.0%}}) is land stopping; the rest is fewer new pits | [[D]] | Parts accounting, four variants; Amarakaeri's stopped land flat | Stopped includes flicker; no image check |
| New pits kept opening in the Tambopata buffer zone in 2019; new land fell from 2020 | [[D]] | Raster parts; GLAD-L and Sentinel-2 alerts in La Pampa (other measures) | Annual maps blur the start |
| *If* the other Peruvian buffer zones show what the Tambopata buffer zone would otherwise have done, Mercurio and the operations that followed lowered its net mining additions by about {{model_m1_during_net:,.0f|abs}} to {{did_base2014_net:,.0f|abs}} ha/yr in 2019–21; ordinary relative to size; an upper bound | [[C]] *conditional* | M1, Tambopata vs 14 other Peruvian buffer zones; 2×2 vs Amarakaeri (2014–18 baseline) | Not parallel before 2019; COVID; size; Amarakaeri also treated; matching can't beat chance |
| Net additions rose on legal-mining-corridor land and across the road; the department never fell | [[D]] | Corridor share {{v2_corridor_share_pre_net:.0%}} → {{v2_corridor_share_during_net:.0%}} (2016–18 → 2019–21); Madre de Dios {{mdd_pre_net}} → {{mdd_during_net}} → {{mdd_later_net}} ha/yr; MAAP #208 (other measure) | Rises in the other Madre de Dios zones are {{mdd_rise_elsewhere_vs_tambopata_fall:.1f}}× the target's fall: not all displaced miners; road RD weak on net |
| The target came back in 2022–25, a third to a half on old pits ({{tambopata_bz_later_ex2023_remined_share_added:.0%}}–{{tambopata_bz_later_remined_share_added:.0%}} of added land, without / with 2023) | [[D]] | Raster parts; MAAP #193 | 2023 spike MapBiomas only; flicker |
| La Pampa had not run out of gold | [[D]] | Geology: {{gold_broad_lapampa_depleted_2018:.0%}} mined by 2018 | Its most-mined cells were {{st_lp_tq_high_share18:.0%}} mined |
| Net additions inside the reserve jumped in 2025 (+{{tambopata_nr_2025_net}} ha) | [[D]] | Raster; MAAP #241 and AMW agree on the direction | 521 ha were already inside by 2016 (Asner & Tupayachi) |
| Buffer-zone enforcement shielded the reserve | **not claimed** | Reserve-edge RD {{rd_reserve_did_net:+.1f}} (p = {{rd_reserve_did_net_p:.2f}}) | Uninformative |
| The fall-and-return cycle happened twice (2012 and 2019) | **not claimed** | Asner & Tupayachi (2017) report the 2012 dip | Our data: La Pampa net additions {{tl_lp_change_2012_13_vs_2010_11_net:+.0%}} in 2012–13 |
| The official gold series fell 88% | **withdrawn** | — | Definition change in 2020 |
| Corridor miners mine informally and don't declare | plausible, **not claimed** | Formalization rates, Bolivia exports, unknown-origin exports | No trace of where Madre de Dios gold is declared |
| The region mined less | **rejected** | — | Madre de Dios net additions rose {{mdd_pre_net}} → {{mdd_later_net}} ha/yr (2016–18 → 2022–25) |
| Brazil: operations reduced mining | **not claimed** | Boom, then fall after 2022 | Operations at the peak; Munduruku fell first; national reforms in 2023 |
| Next operation: local fall while it lasts, partly idle pits; new pits in a ring around it; a return within ~3 years | [[P]] | Peru pattern; Dethier et al. (2023) | One operation, one region; risk model barely beats "mining nearby" |
:::

@part So what

## Limits | Most biases make the fall look bigger

**Most of our limitations make the 2019–21 fall look bigger than it was, and most make the rise elsewhere and the return look smaller.** Read the fall as an upper bound, the return as a lower bound. [[D]]

**How to read the arrows:** ▲ = makes the 2019–21 fall in the Tambopata buffer zone look **bigger** than the truth. ▼ = makes it look **smaller**. ? = either way.

| Limitation | What happens | Fall in the target | Displacement | How we checked |
|---|---|:---:|:---:|---|
| **Net additions mix three processes** | A quarter to a half of the fall is land stopping, and part of "stopped" is temporary or flicker: net additions can fall while activity does not. | ▲ | — | Parts shown everywhere; {{tambopata_bz_during_stopped_share_back_within_2y:.0%}} of the Tambopata buffer zone's 2019–21 stopped land mined again within two years ([What fell](#what-fell)) |
| **Hectares, not people** | We count mapped land, a proxy for miners. Activity on old pits and rivers adds few new hectares. | ▲ | ▼ | Parts accounting; MAAP #193 dredge counts. No data on people. |
| **Satellites miss river dredges and mercury** | Mining on the river doesn't show as land. Dredges in La Pampa rose from 148 to 598 (2021 → 2023, MAAP #193). | ▲ | ▼ | Named in part 4 of the brief; can't be fixed with these data. |
| **Spillovers into comparison zones** | If miners moved into Amarakaeri or the legal mining corridor, they raised the comparison. | ▲ (gap too wide) | — | 14-zone pool; the legal mining corridor never a comparison ([Six methods](#six-methods)). |
| **Comparison zones were also treated** | Mercurio II covered all of Madre de Dios; 2017–18 operations sit in the pre-period. | ▼ (gap too narrow) | — | Amarakaeri called "less treated" ([Six methods](#six-methods)). |
| **Picked at its peak** | La Pampa was targeted *because* mining was at a record (2017). Records tend to fall back on their own. | ▲ | — | Fake-date tests; each 2019–21 year (at most {{tambopata_bz_net_max_during}} ha) is below every 2011–18 year (at least {{tambopata_bz_net_min_2011_18}} ha). |
| **Size** | A bigger zone falls more in hectares just by being bigger; it ranked first in hectares in 2014–16 too. | ▲ in hectares | — | Scaled ranks: ordinary for its size ({{model_m4_rank:.0f}}rd–{{placebo_space_rank_scaled:.0f}}th of 7 depending on the scaling) ([The claim](#the-claim)). |
| **COVID (2020–21)** | New land fell only from 2020. If big mining zones reacted differently, part of the gap is COVID. | ▲ probably | ? | Context model K1; inseparable with these data ([The claim](#the-claim)). |
| **Gold price** | Up {{gold_price_ratio_2025_2018:.1f}}-fold 2018–25; year effects remove it only if it hits every zone equally. | ? (small) | ▼ for 2022–25 | M2 lets big zones react more: {{model_m2_during_net}} vs {{model_m1_during_net}} ha/yr (M1). |
| **Enforcement money moved with the operation** | Spending peaked in 2019; controlling for it absorbs part of the effect itself. | ? | — | K2/K3; the COVID and money terms offset, so the stable gap proves nothing ([The claim](#the-claim)). |
| **Pre-2019 paths not parallel** | Tambopata outgrew the comparison in hectares before 2019; the cell pre-trend fails with the 2010 lead. | ? (depends on the scale) | — | Both lead windows reported ([Six methods](#six-methods)). |
| **Annual maps, a February start** | The 2019 map includes clearing from January–February 2019 and late 2018. | ▼ (first year blurred) | ▼ | Quarterly GLAD-L alerts ([What fell](#what-fell)). |
| **Legal or illegal?** | MapBiomas can't see legality; the legal mining corridor holds legal concessions and informal miners. | — | ? | MAAP #235 legality layer, time-consistent ([Where it went](#where-it-went)). |
| **"No operation found" is not "no operation"** | A twin or match may have had an unreported operation. | ▼ | — | Logged searches; unverified-report sensitivity ([Six methods](#six-methods)). |
| **Twins in Brazil's weaker-enforcement years (2019–22)** | The twins may have grown faster than "normal". | ▲ (vs the twins) | — | Used only as a second check, never alone. |
| **Displacement inside the RD** | Net additions falling south and rising north open the road gap from both sides. | — | ▲ at the road (swing, not net) | Labelled as an upper bound ([Six methods](#six-methods)). |
| **One treated zone, one case** | No informative standard errors; the pattern is seen once. Brazil could not add a second case (below). | ? (uncertainty, not a direction) | ? | Placebos instead ([The claim](#the-claim)). |

**Why it matters:** FZS should read our fall as "at most this big, for three years, much of it pits going idle" and the rise elsewhere as "at least this much". We expect enforcement in one spot to buy a short pause, not a regional fall. [[P]]

:::more Hectares as a proxy for people
**We measure land, not miners.** Every hectare in this report is mapped mining land: MapBiomas pixels, AMW squares, GLAD-L alerts. None of them counts people, camps or machines.

- **Why we can't do better:** no public, dated count of miners exists per zone. Censuses don't reach camps; REINFO lists registrants, not where they work; police reports count arrests, not people present.
- **When the proxy works:** while miners clear new forest, hectares track effort fairly well.
- **When it fails:** on old pits and rivers. One crew can work the same pit for years, adding no new hectares; a dredge adds none. A pit that floods leaves the mining class whether or not its crew has gone.
- **The direction:** hectares understate activity after a crackdown, when miners return to old ground. So the return in 2022–25 is likely a lower bound, and the fall in 2019–21 likely an upper bound for the fall in people.
- **What would fix it:** dredge counts from high-resolution imagery (as MAAP does), night-time lights over camps, mercury sales, or field counts by SERNANP and FZS rangers.
:::

:::more Brazil, the mirror case: mining boomed and fell; operations arrived at the peak (backup only)
**In Brazil, mining in the Yanomami, Munduruku and Kayapó territories had boomed for years and fell after 2022. Federal operations arrived at the peak, and Munduruku was already falling before its operation, so our data cannot separate the operations from the end of the boom.** [[D]]

:::fig output/fig_brazil_v2_pixels.png
read: Net mining additions per year (dot) = new land + re-mined (bars up) − stopped (down), MapBiomas Brazil Collection 11, four territories, 2010–2025. Black line: each territory's first verified operation (rule R*); dashed grey: other operations.
take: Each territory boomed before its operation; Munduruku fell before August 2023; Sararé surged as its operation began.
:::

- **Net additions, ha/yr, 2019–22 → 2023–25 (MapBiomas Brazil Collection 11):** Yanomami {{brv2_yan_net_boom}} → {{brv2_yan_net_later}}; Munduruku {{brv2_mun_net_boom}} → {{brv2_mun_net_later}}; Kayapó {{brv2_kay_net_boom}} → {{brv2_kay_net_later}}; Sararé {{brv2_sar_net_boom}} → {{brv2_sar_net_later}}. Yanomami's 2023 was still at its peak; its fall shows in 2024–25. [[D]]
- **AMW (another product):** Yanomami new area {{bs_yan_new_ha_2022:,.0f}} ha (2022) → {{bs_yan_new_ha_2024:,.0f}} ha (2024). Never spliced with MapBiomas.
- **No rise next door:** rings 0–10 km around Yanomami show {{brv2_r0_10_net_later:.1f}} ha/yr of net additions in 2023–25. Press reports (ISA 2026, Greenpeace) describe miners moving toward Venezuela and to territories like Sararé.
- **Data and check:** MapBiomas Brazil Collection 11 rasters, 1985–2025, same pixel accounting as Peru. Kayapó mining stock {{brv2_kayapo_check_2024:,.0f}} ha (2024) and {{brv2_kayapo_check_2025:,.0f}} ha (2025) vs 17,632 and 18,573 on the platform.
- **Staggered design:** territory + year effects on net additions, each territory treated from its first verified operation in 2021–25 ({{brv2_n_treated:.0f}} of {{brv2_n_units:.0f}} territories with Collection 11 mining in 2014–18). Only {{brv2_never_n:.0f}} territories count as never treated, and {{brv2_never_n_unsearched:.0f}} of them was never searched for operations.
- **Why it can't decide:** the treated territories boomed before their operations (event-study leads: {{brv2_net_es_m6:+,.0f}} ha/yr at six years before, {{brv2_net_es_m2:+,.0f}} at two years before), so parallel trends fail. Across dating rules and samples the estimate changes sign. We report no Brazil p-value as a test of the operations.
- **National change in 2023:** a new government, the end of the gold "good faith" rule, electronic gold invoices from August 2023. A territory-level design can't separate them.
- **IBAMA fines** (Legal Amazon, all infractions): {{br_ibama_aml_mean_2015_2018:,.0f}}/yr (2015–18), {{br_ibama_aml_mean_2019_2022:,.0f}}/yr (2019–22), {{br_ibama_aml_2023:,.0f}} (2023). Counts, not enforcement intensity in the territories.

**Code:** `code/brazil_raster.py`, `code/brazil_v2.py`, plus `brazil_stagger.py` (AMW), `brazil.py`, `brazil_ibama.py`. Card: `docs/methods/12_brazil.md`.
:::

## For FZS | Stay after the sweep, watch the ring, guard the edge

**What happened, from this one case:** in 2019–21 net additions in the Tambopata buffer zone fell, a quarter to a half of the fall land leaving the mining class; new pits kept opening in 2019; net additions rose across the road and in the region; the target came back on old pits; in 2025 net additions inside the reserve jumped. [[D]]

**What we expect next time** [[P]]:

1. **Stay after the sweep.** Net additions in the target stayed low only in 2019–21, while the operation's money was at its peak. Fund presence over the following years, not one-off operations.
2. **Watch the ring around the operation.** In 2019 new pits kept opening in the target while old ones went quiet, and net additions rose across the road. Near-real-time forest-loss alerts (GLAD-L or MAAP-type) on a ring of a few kilometres around each operation catch the next pit before it is dug out. Dethier et al. (2023) also report faster mining just outside the targeted zones.
3. **Guard the reserve's edge and the river.** {{rd_reserve_inside_share_1km:.0%}} of new land inside the reserve lies within 1 km of its edge [[D]], and the 2025 jump came in by the Malinowski River. Staffed river posts are the direct shield.

:::fig output/fig_v2_risk_map.png
read: Predicted chance that a 1-km cell gets more than 1 ha of new land (first-time mining) in 2026–28, from a model trained on 2019–21 and tested out of sample on 2022–25 in held-out blocks. A prediction, not a causal map.
take: Risk clusters next to existing mining; the model adds little beyond "is there mining nearby?". Reserves score low by construction (almost no mining in training), and river access is not in the model, so the 2025 rise inside the reserve is not foreseen.
:::

- **Where to look next:** the model flags {{risk_hi_cells_outside_corridor:.0f}} high-risk cells outside the legal mining corridor, {{risk_hi_cells_lapampa:.0f}} of them in the La Pampa sector and {{risk_hi_cells_communities:.0f}} in native communities. [[P]]
- **Honest score:** AUC {{risk_auc_spatial_holdout:.2f}} on held-out 10-km blocks, barely above {{risk_auc_benchmark:.2f}} for "mining nearby" alone. [[P]]

**Why it matters:** we expect the months around and after an operation to be the most exposed, and FZS can fund those months. [[P]]

:::more Three more lessons, the social cost, and what data would let us say more
- **Don't count on the buffer zone as a shield, yet.** The reserve-edge RD is uninformative ({{rd_reserve_did_net:+.1f}} points, p = {{rd_reserve_did_net_p:.2f}}); we cannot tell whether buffer-zone enforcement protected the reserve. [[D]]
- **Watch idle and old pits, not only forest edges.** In 2019–21, {{tambopata_bz_during_stopped_share_back_within_2y:.0%}} of the Tambopata buffer zone's stopped land was mined again within two years, and in 2022–25 re-mined land was {{tambopata_bz_later_remined_share_added:.0%}} of added land ({{tambopata_bz_later_ex2023_remined_share_added:.0%}} without 2023). Forest-loss alerts never see this. [[D]]
- **Make the legal mining corridor a real filter:** proof of gold origin, gold-buyer registers, real formalization deadlines, mercury checks. Brazil's 2023 reforms are a model. [[P]]
- **Damage:** CSF gives two separate estimates per kg of gold mined in Peru: US$ {{eco_param_social_calc_usd_kg_lo:,.0f}}–{{eco_param_social_calc_usd_kg_hi:,.0f}} (calculator) and US$ {{eco_param_social_pdf_usd_kg_lo:,.0f}}–{{eco_param_social_pdf_usd_kg_hi:,.0f}} (2023 report, p. 7). Quote both, never one merged range.
- **Mercury:** over a third of carnivorous fish exceed the limit hundreds of km downstream; exposed children score 4.68 IQ points lower.
- **Exploitation:** about 4,500 women are sexually exploited near camps, 78% of them minors.
- **Livelihoods:** about 46,600 people depend directly on mining. Enforcement without income alternatives invites return.
- **What would let us say more:** dated patrol and interdiction records per zone (SERNANP, FZS, police): were the stopped pits the raided ones? An image-checked sample of stopped pits; concession and REINFO maps to grade legality pixel by pixel; dredge counts and mercury sampling; more operations as cases.
:::

:::more What next: informed speculation, pressure on the reserve rises from 2027
**Several forces point to more pressure on Tambopata, not less.** These are expectations from sources and our one case, not findings. [[P]]

1. **REINFO ends on 31 December 2026, on paper.** A new small-mining law (Ley MAPE, bill due 15 October 2026) would give about 30,000 registrants a two-year regime from 2027. Every deadline since 2012 has been extended. Expect another, under a new name.
2. **A new government.** The president elected in June 2026 campaigned on cracking down on illegal mining; Reuters judged that neither runoff candidate would dismantle REINFO quickly. Expect announcements and operations before budgets.
3. **Record gold prices** (about US$ 4,400/oz in August 2026) make old pits pay again; the 2023 return in La Pampa coincided with rising prices.
4. **More operations, less money each.** Interdictions rose from 62 a month (2024) to over 130 (2026), while the national PP 0128 budget fell from S/ 121 M (2019) to S/ 70 M (2025). In Madre de Dios, booked spending fell from {{t8_pp0128_mdd_2019:,.0f}} soles (2019) to {{t8_pp0128_mdd_2025:,.0f}} soles (2025).
5. **The river is open.** The navy left the Malinowski posts in 2025 (MAAP #241). Organised crime now operates there: a safety issue for rangers, not only for the forest.

| If… | Then expect… [[P]] | Based on |
|---|---|---|
| A new operation hits La Pampa | A local fall in net additions while it lasts, a large part of it pits going idle | [What fell](#what-fell), [The claim](#the-claim) |
| … and the ring around it is not watched | New pits nearby in the first year | [What fell](#what-fell) |
| … and the corridor across the road stays open | More mining across the road in the following years | [Across the road](#across-the-road) |
| … and enforcement then lapses | A return on old pits within about three years, then pressure on the reserve edge | [How it came back](#how-it-came-back), [Inside the reserve](#inside-the-reserve) |
| REINFO is extended again | La Pampa gold keeps travelling on corridor paperwork | [Money and gold](#money-and-gold) |
| Gold sales are traced (origin proof, buyer checks) | A bigger discount on illegal gold, the one lever that could act region-wide | Brazil 2023 ([Limits](#limits)) |

- **Watch:** GLAD-L alerts in a ring around each operation and in the first kilometre inside the reserve; REINFO and Ley MAPE votes in December 2026; state-of-emergency renewals (the last we found: DS 093-2026-PCM, June 2026); river-post staffing; dredge counts.
- **How sure:** we see the pattern (fall, rise next door, return) once, after 2019; Asner & Tupayachi (2017) report a similar cycle after 2012 that our data don't show. The politics are press-based; the original IPE reports and the full law texts were not opened.

**Sources:** `docs/walkthrough/notes/economics_sources.md` (section "Political and context items"), `qualitative_background.md`, `maap_citations.md`.
:::

@part Team corner

## Status | Final version, ready to hand in

**Everything for Lesson 5 is built from one run of the code** and sits in `deliverables/` (brief PDF and Word, slides, map videos) and `replication/` (the replication zip and a zip with all our material). The work is on branch `analysis/v3-definitions`.

- **Team:** Ruby Ann Grambauer, Sebastian Schmid, Laurens van der Lely, Omkar Mate, Dhruv Chaudhari.
- **Rebuild from scratch:** `uv sync` then `uv run python code/main.py`; checks: `uv run pytest tests -q`.

:::more What would let us say more
- **An image-checked sample of stopped pits** (out of scope in v3): would settle how much of "stopped" is abandonment.
- **Brazil:** most never-treated territories were never searched for operations.
- **Dated patrol and interdiction records** from SERNANP or FZS: would turn the 0/1 treatment into intensity.
:::

## Files | Where everything lives

**Run everything:** `uv run python code/main.py`. It writes every figure, table and number to `output/`.

:::more The code map
| Chapter | Code | Main output |
|---|---|---|
| Definitions: outcome, zones, treatment, periods | `code/definitions.py` | used by every module |
| Checks against publisher numbers | `code/checks.py` | `output/checks.csv` |
| The places, parts, stopped destinations | `code/raster_zones.py`, `code/zonedata.py` | `fig_v2_zone_map.png`, `fig_peru_additions.png`, `fig_v2_parts_by_zone.png` |
| What fell: timing inside 2019 | `code/glad_alerts.py` | `fig_v2_glad_quarterly.png` |
| Where it went, across the road, how it came back | `code/raster_layers.py`, `code/v2_tests.py`, `code/v2_legality.py` | `fig_v2_stream.png`, `fig_v2_road_*.png`, `fig_v2_sankey.png` |
| Money and gold: spending, timeline, gold left, declared gold, economics | `code/v2_tests.py`, `code/v2_extra.py`, `code/raster_gold.py`, `code/peru_gold_minem.py`, `code/peru_production.py`, `code/v2_economics.py` | `fig_v2_enforcement_spending.png`, `fig_v2_timeline.png`, `fig_peru_gold_definition.png`, `fig_v2_economics.png` |
| Inside the reserve | `code/peru_anp.py` | `fig_peru_inside_reserves.png` |
| Six methods, Attempt 1: 2×2, event study, model ladder, cell panel | `code/peru.py`, `code/peru_robust.py`, `code/peru_models.py`, `code/v2_stats.py` | `fig_peru_event_study.png`, `fig_peru_models.png`, `fig_v2_stats_*.png` |
| Attempt 2: synthetic control | `code/peru_synth.py` | `fig_peru_synth.png` |
| Attempt 3: rule-based twins | `code/control_*.py` | `fig_control_*.png` |
| Attempt 4: spatial RD | `code/v2_rdd.py` | `fig_v2_rdd.png`, `table_rdd.csv` |
| Attempt 5: matching | `code/control_psm.py` | `fig_psm.png`, `psm_results.csv` |
| Attempt 6: synthetic DiD | `code/peru_sdid.py` | `fig_sdid.png`, `peru_sdid.csv` |
| The claim: placebos, context models | `code/placebo_explainer.py`, `code/peru_context_models.py` | `fig_placebo_explainer.png`, `fig_peru_context_models.png` |
| Limits: Brazil | `code/brazil_raster.py`, `brazil_v2.py`, `brazil*.py` | `fig_brazil_v2_pixels.png` |
| For FZS: risk map | `code/v2_extra.py` | `fig_v2_risk_map.png` |
| The brief's figure | `code/brief_figure.py` | `fig_brief_main.png` |
| Every number | all of the above | `output/numbers.csv` |

- **Brief:** `docs/brief/brief_content.md` → `BRIEF.html`. **Methods:** {{METHODS_LINK}}.
- **Review cards:** `docs/methods/` (00–14). **Plan:** `docs/PLAN_v3.md`.
- **Operation searches:** `docs/walkthrough/notes/control_interventions.md`, `brazil_data_and_operations.md`.
- **Log and decisions:** `docs/walkthrough/LOG.md`. **Data log:** `DOWNLOAD_LOG.csv`.
- **Big raw files are git-ignored** (rasters, Amazon Mining Watch, RAISG, MapBiomas Amazonía, FUNAI). The run then uses the small files in `data_intermediate/`. Download links are in `DOWNLOAD_LOG.csv`.
:::

## Appendix | Data checks, decisions and every number

**One check per dataset (ours vs the publisher).** Full log in `DOWNLOAD_LOG.csv`.

| Data | What we checked | Ours | Publisher |
|---|---|---:|---:|
| MapBiomas Peru Collection 4 rasters, our zone registry | Tambopata buffer zone, mining 2025 (ha) | {{chk_tbz_2025_ours}} | {{chk_tbz_2025_pub}} |
| Same, vs protected-area statistics | Tambopata reserve, mining 2025 (ha) | {{chk_tnr_2025_ours:,.1f}} | {{chk_tnr_2025_pub}} |
| Same, vs department statistics | Madre de Dios, mining 2025 (ha) | {{chk_mdd_2025_ours}} | {{chk_mdd_2025_pub}} |
| World Bank Pink Sheet | Gold, August 2026 ($/oz) | {{chk_gold_aug2026_ours}} | {{chk_gold_aug2026_pub}} |
| MINEM yearly files vs central bank (BCRP) | Madre de Dios gold 2019 (kg) | {{chk_bcrp_2019_ours}} | {{chk_bcrp_2019_pub}} |
| MEF Consulta Amigable, PP 0128 | Madre de Dios 2019 (soles) | {{chk_pp0128_2019_ours}} | {{chk_pp0128_2019_pub}} |
| MapBiomas Amazonía Collection 6 | Amazon mining 2023 (ha) | {{chk_mb_amazonia_2023_ours}} | {{chk_mb_amazonia_2023_pub}} |
| MapBiomas Brazil Collection 11 | Artisanal mining, indigenous lands, 2025 (ha) | {{chk_br_ti_2025_ours}} | {{chk_br_ti_2025_pub}} |
| MapBiomas Brazil Collection 11 rasters | Kayapó mining 2025 (ha) | {{chk_kayapo_2025_ours}} | {{chk_kayapo_2025_pub}} |
| INPE DETER mining alerts | Total 2019 (km²) | {{br_deter_2019_total_wfs_km2:.2f}} | {{br_deter_2019_total_dashboard_km2:.2f}} |
| Amazon Mining Watch | Tambopata buffer zone by 2018, polygon clip vs registry (internal; no publisher totals) | {{chk_amw_tbz_2018_ours}} | {{chk_amw_tbz_2018_pub}} |
| IBAMA fines | — | — | no total online |

:::more What changed in plan v3, and why
| Before (v2 pages) | Now (v3) | Why |
|---|---|---|
| Mixed measures: workbook net for zones, first-time mining for maps and the brief figure | Net additions everywhere, parts where shown; other products labelled | Team decision 2026-10-15 (PLAN_v3 V3-1, V3-4) |
| Two "Tambopata buffer zones" (workbook vs raster, raster without Kotsimba) | One registry; official zones whole; Kotsimba a tenure tag | V3-2 |
| Treatment dates varied by module | Start of Mercurio, Feb 2019; reference 2018; later events context | V3-3 |
| "Nothing fell in 2019" | "New clearing did not fall in 2019; land going out of use did" | Raster parts: {{tambopata_bz_2019_stopped}} ha of Tambopata buffer zone land stopped in 2019 |
| Causal range 411–1,859 ha/yr | {{model_m1_during_net:,.0f|abs}}–{{did_base2014_net:,.0f|abs}} ha/yr, partly stopping, an upper bound | Review D-S14-3; v3 parts |
| "Rank 1 of 15" as evidence | Raw rank 1 also in 2014–16 (size); scaled ranks {{model_m4_rank:.0f}}rd–{{placebo_space_rank_scaled:.0f}}th of 7 | Review X1 |
| "Year effects absorb the gold price and COVID"; "keeps 97%" | Year effects remove only common shocks; the K-model controls offset | Review cards 04, 05 |
| Twins at 40% of pace | {{top3_ratio:.0%}}–{{top3_ratio_excl_unverified:.0%}} (with / without Munduruku), AMW measure, backup only | One dating rule (R*) |
| Brazil "wrong sign" | Boom, then fall; operations at the peak; cannot separate | Review D-S14-8 |
| La Pampa cell pre-trend "fails" / road "within a year" | Passes with 2011+ leads, fails with 2010; road swing mainly 2020–22 and weak on net | Review cards 08, 09 |
| Chapters in analysis order | Chapters in the talk's order (STORYLINE v3.1); side analyses in "Go deeper" | Team request 2026-10-15 |

**Plan and decisions:** `docs/PLAN_v3.md`, `docs/walkthrough/LOG.md` (D29 on), `docs/methods/14_synthesis.md`.
:::

:::more Decision log (from docs/walkthrough/LOG.md)
{{DECISIONS_TABLE}}
:::

:::more Every number, filterable (from output/numbers.csv)
{{NUMBERS_TABLE}}
:::
