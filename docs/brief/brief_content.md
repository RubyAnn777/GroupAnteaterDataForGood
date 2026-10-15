<!--
Source of docs/brief/BRIEF_DRAFT.md / .html / .pdf / .docx. Build: `uv run python docs/overnight/build_report.py`.
Placeholders {{id}} / {{id:fmt}} come from output/numbers.csv; the build also writes output/brief_numbers.csv (every
number in order of appearance). Claim tags: [[D]] description, [[P]] prediction, [[C]] causal.
Plan v3 (docs/PLAN_v3.md): ONE measure, net mining additions = new land + re-mined − stopped (ha/yr);
ONE zone registry; treatment = Mercurio from Feb 2019 (first treated year 2019). Target: 2 printed pages for parts 1-4.
-->

# When the patrols leave: what Operation Mercurio tells FZS about enforcement against gold mining

Group Giant Anteater · Data for Good · Question 2 · October 2026 · Team: [names]

## 1. The question

**FZS pays for enforcement and needs to know what it buys.** It supports SERNANP's operations against alluvial gold mining around Tambopata and Bahuaja-Sonene (FZS, n.d.). Operations are costly and temporary, so: **what happens in the targeted area, and around it, when an operation ends?** Mining could stop (**deterrence**), move (**displacement**) or return (**delay**); inside the target these look alike, so we need comparisons.

**Case:** Operation Mercurio at La Pampa, Peru's largest illegal mining area, in the buffer zone of Tambopata National Reserve (Madre de Dios). **Treatment:** its start in February 2019 (first treated year 2019); COVID-19 (2020), Plan Restauración (2021) and the April 2023 state of emergency are context, so we measure "Mercurio and what followed". **Target:** the Tambopata buffer zone (official boundary) and its La Pampa sector (70.15–69.80 W). **Comparison:** the Amarakaeri buffer zone, only "less treated" (Mercurio II covered all of Madre de Dios; MINAM, 2021, p. 33), and 14 Peruvian buffer zones with mining. **Around it:** the legal corridor across the highway, the reserve, the department. **Periods:** 2016–18, 2019–21, 2022–25 ("later years").

## 2. Data and provenance

**One outcome everywhere: net mining additions** (ha/yr) = land mined for the first time (**new**) + old mining land mined again (**re-mined**) − mining land that left the mining class (**stopped**), counted pixel by pixel on the 30-m annual maps of **MapBiomas Peru, Collection 4** (class 4.2: all mining, legal and illegal). Checks (ours vs publisher): Tambopata buffer zone 2025 {{chk_tbz_2025_ours}} vs {{chk_tbz_2025_pub}} ha; reserve {{chk_tnr_2025_ours}} vs {{chk_tnr_2025_pub}}; Madre de Dios {{chk_mdd_2025_ours}} vs {{chk_mdd_2025_pub}}. **Context:** World Bank gold price (Aug 2026 ${{chk_gold_aug2026_ours}}/oz vs {{chk_gold_aug2026_pub}}); MINEM/BCRP gold (2019 {{chk_bcrp_2019_ours}} vs {{chk_bcrp_2019_pub}} kg; an artisanal *estimate* until 2019); MEF spending, PP 0128 (2019 S/ {{chk_pp0128_2019_ours}} vs {{chk_pp0128_2019_pub}}). **Cross-checks only (other measures):** Amazon Mining Watch (no publisher totals; two clips {{chk_amw_tbz_2018_ours}} vs {{chk_amw_tbz_2018_pub}} ha), MapBiomas Amazonía Col. 6 ({{chk_mb_amazonia_2023_ours:,.0f}} vs 780,000 ha, 2023), MapBiomas Brazil Col. 11 ({{chk_br_ti_2025_ours}} vs {{chk_br_ti_2025_pub}} ha). Files: `DOWNLOAD_LOG.csv`; numbers and figure: `code/main.py`.

## 3. Findings

![Net mining additions and their three parts: La Pampa sector and the corridor across the road (top); Madre de Dios by area (bottom)](output/fig_brief_main.png)

**Net mining collapsed in the target during the operation** [[D]]. The Tambopata buffer zone fell from {{tambopata_bz_pre_net}} to {{tambopata_bz_during_net}} ha/yr (2016–18 vs 2019–21) while the less-treated Amarakaeri rose from {{amarakaeri_bz_pre_net}} to {{amarakaeri_bz_during_net}}: a difference of **{{did_main_net}} ha/yr**. A fake start in 2016 gives {{did_placebo_net:+,.0f}}; every 2019–21 year (≤ {{tambopata_bz_net_max_during}} ha) was below every 2011–18 year (≥ {{tambopata_bz_net_min_2011_18}}).

**A quarter to a half of that fall is pits going out of use, mostly in 2019** [[D]]. New land fell from {{tambopata_bz_pre_new}} to {{tambopata_bz_during_new}} ha/yr, while stopped land rose from {{tambopata_bz_pre_stopped}} to {{tambopata_bz_during_stopped}}. Stopping explains {{tambopata_bz_stopped_share_of_fall_min:.0%}}–{{tambopata_bz_stopped_share_of_fall_max:.0%}} of the net fall, depending on whether we count land mined again within two years and stopping at the pre-2019 rate; {{tambopata_bz_excess_stopped_share_in_2019:.0%}} of the excess stopping came in 2019, when La Pampa lost {{lapampa_stopping_rate_2019:.0%}} of its mining area from the mining class (2016–18: {{lapampa_stopping_rate_pre:.0%}} a year). In Amarakaeri stopped land barely moved ({{amarakaeri_bz_pre_stopped}} → {{amarakaeri_bz_during_stopped}}), so the stopping was specific to the target. In La Pampa new pits kept opening in 2019 ({{lapampa_2019_new}} ha vs {{lapampa_2018_new}} in 2018) while {{lapampa_2019_stopped}} ha stopped; new land fell only in 2020–21, the COVID years. {{tambopata_bz_during_stopped_share_to_water:.0%}} of stopped land became water; {{tambopata_bz_during_stopped_share_back_within_2y:.0%}} was mined again within two years (before 2019: {{tambopata_bz_pre_stopped_share_back_within_2y:.0%}}). Dethier et al. (2023), using mining ponds, independently report 70–90% abandonment in the targeted zones and faster mining just outside them.

**Mining moved across the road, and the department never fell** [[D]]. In the legal corridor across the highway net additions rose from {{corridor_across_pre_net}} to {{corridor_across_during_net}} ha/yr; the corridor's share of the department's net additions rose from {{v2_corridor_share_pre_net:.0%}} to {{v2_corridor_share_during_net:.0%}}. Madre de Dios went {{mdd_pre_net}} → {{mdd_during_net}} → {{mdd_later_net}} ha/yr. Rises elsewhere add up to {{mdd_rise_elsewhere_vs_tambopata_fall:.1f}} times the target's fall: not all of it can be miners who moved.

**Therefore** [[C]], *if the other Peruvian buffer zones show what the Tambopata buffer zone would otherwise have done*, Mercurio and the operations that followed lowered its net mining additions by about {{model_m1_during_net:,.0f|abs}} to {{did_base2014_net:,.0f|abs}} ha/yr in 2019–21 (all 14 zones, or Amarakaeri alone, 2014–18 baseline). A quarter to a half of it is land stopping (in this model {{model_m1_during_stopped:,.0f}} of {{model_m1_during_net:,.0f|abs}}), not less new clearing; the fall is large in hectares but ordinary relative to the zone's size ({{model_m4_rank:.0f}}th–{{placebo_space_rank_scaled:.0f}}th of 7 by scaling; in hectares it also ranks first in 2014–16, before Mercurio). Read it as an upper bound (4b).

**It came back, on old pits; then mining entered the reserve** [[D]]. In 2022–25 the target averaged {{tambopata_bz_later_net}} ha/yr ({{tambopata_bz_later_ex2023_net}} without 2023, a spike only MapBiomas shows), {{tambopata_bz_later_remined}} of it re-mined. Inside the reserve net additions were +{{tambopata_nr_2025_net}} ha in 2025; MAAP reports ~500 ha from late 2025 to Feb 2026, after the navy left the river posts (Pacsi et al., 2026).

## 4. What FZS can do with this

**(a) What FZS learns** [[P]]. From this one case: a sharp local fall while patrols are present, a quarter to a half of it pits being abandoned; new pits nearby and across the nearest legal boundary; a return within about three years, largely on old pits; no fall in the region. So: **fund presence, not one-off sweeps; watch a ring of a few kilometres around each operation with near-real-time forest-loss alerts** (new pits opened in 2019 while patrolled pits stopped); **hold the reserve's first kilometre and the river posts** ({{rd_reserve_inside_share_1km:.0%}} of first-time mining inside the reserve is within 1 km of its edge); and trace gold origin in the corridor (0% royalty for small producers, Ley 28258, Art. 5; 145 of 9,592 miners in formalization fully formalized, MINAM, 2021, pp. 55–56).

**(b) Why this could mislead, and which way.** *Omitted variables:* COVID-19, the gold price (×{{gold_price_ratio_2025_2018:.1f}} 2018–25) and later waves overlap the post-period and need not hit all zones alike (probably overstates). *Reverse causation:* La Pampa was targeted at its peak; part of the fall is a return to normal (overstates). *Selection of units:* one targeted zone, far larger than any comparison: standard errors are not informative (Conley & Taber, 2011) and raw placebo ranks measure size; Amarakaeri received miners (overstates) but had its own operation (understates). *Measurement error:* net additions mix three processes; a quarter to a half of the fall is pits leaving the mining class, and part of "stopped" is temporary or classification flicker, so **net additions can fall while activity does not** (overstates); hectares proxy for miners; the class mixes legal and illegal mining; **satellites cannot see river dredges or mercury** (MAAP counted 148 → 598 dredges in La Pampa, 2021–23; Yupanqui et al., 2023), so a shift to rivers adds no hectares (overstates). **Read the fall as an upper bound, the return as a lower bound.**

**(c) What would let us say more.** Dated patrol and interdiction records from SERNANP or FZS (intensity, not a 0/1 flag: were the stopped pits the raided ones?); an image-checked sample of stopped pits; concession and REINFO maps for legality pixel by pixel; dredge counts and mercury sampling; more operations as cases.

## References

Access dates are when the source was opened for this project (see `DOWNLOAD_LOG.csv`).

- Asner, G. P., & Tupayachi, R. (2017). Accelerated losses of protected forests from gold mining in the Peruvian Amazon. *Environmental Research Letters*, 12, 094004. https://doi.org/10.1088/1748-9326/aa7dab (accessed 2026-10-12)
- Conley, T. G., & Taber, C. R. (2011). Inference with "difference in differences" with a small number of policy changes. *Review of Economics and Statistics*, 93(1), 113–125. https://doi.org/10.1162/REST_a_00049 (accessed 2026-10-10)
- Dethier, E. N., Silman, M. R., Fernandez, L. E., Caballero Espejo, J., Alqahtani, S., Pauca, P., & Lutz, D. A. (2023). Operation Mercury: Impacts of national-level armed forces intervention and anticorruption strategy on artisanal gold mining and water quality in the Peruvian Amazon. *Conservation Letters*, 16(5), e12978. https://doi.org/10.1111/conl.12978 (abstract; accessed 2026-10-15)
- Earth Genome (2026). Amazon Mining Watch, mining detections, model 48px_v4.10b (updated 3 Oct 2026). https://source.coop/earthgenome/amazon-mining-watch (accessed 2026-10-10)
- Finer, M., & Mamani, N. (2020, 1 Dec). Illegal gold mining down 78% in Peruvian Amazon, but still threatens key areas. MAAP #130, figures "La Pampa" and "Before and after". https://www.maapprogram.org/gold-mining-peru/ (accessed 2026-10-10)
- Frankfurt Zoological Society (n.d.). Bahuaja-Sonene and Tambopata. https://fzs.org/en/programs/peru/bahuaja-sonene-and-tambopata/ (accessed 2026-10-09)
- MapBiomas Amazonía (2024). Colección 6.0 de mapas anuales de cobertura y uso del suelo en la Amazonía, 1985–2023; factsheet p. 3. https://amazonia.mapbiomas.org (accessed 2026-10-12)
- MapBiomas Brasil (2025). Collection 11 (mining) and Collection 10.1 (indigenous-territory statistics). https://brasil.mapbiomas.org (accessed 2026-10-10)
- MapBiomas Peru (2025). Collection 4 of annual land cover maps of Peru: annual maps and buffer-zone, protected-area and department statistics. https://peru.mapbiomas.org (accessed 2026-10-10)
- MEF (2026). Consulta Amigable, programa presupuestal 0128, Madre de Dios. https://apps5.mineco.gob.pe/transparencia/Navegador/ (accessed 2026-10-12)
- MINAM (2021). Plan Restauración: Plan integral frente a la minería ilegal (Anexo, D.S. N° 017-2021-MINAM), pp. 33, 55–56. https://faolex.fao.org/docs/pdf/per206467anx.pdf (accessed 2026-10-13)
- MINEM (2026). Estadísticas mineras: producción minera; and BCRP (2026), Madre de Dios gold production series. https://www.gob.pe/institucion/minem/informes-publicaciones/5472883-produccion-minera ; https://estadisticas.bcrp.gob.pe (accessed 2026-10-12)
- Pacsi, R., Novoa, S., La Torre, S., Balbuena, H., Finer, M., Santana, A., & Castillo, H. (2026, 10 May). Rapid expansion of illegal gold mining in Tambopata National Reserve. MAAP #241, Image 1. https://www.maapprogram.org/mining-peru-tambopata/ (accessed 2026-10-10)
- Peru (2004). Ley N° 28258, Ley de Regalía Minera, Art. 5 and Art. 10. https://www.leyes.congreso.gob.pe (accessed 2026-10-13)
- University of Maryland GLAD (2026). GLAD-L Landsat forest-loss alerts, 2017–2026. https://storage.googleapis.com/earthenginepartners-hansen/ (accessed 2026-10-12)
- World Bank (2026). Commodity price data (Pink Sheet), monthly, gold. https://www.worldbank.org/en/research/commodity-markets (accessed 2026-09-23)
- Yupanqui, O., Quispe, M., Novoa, S., Castañeda, C., Escalante, E., Finer, M., & Mamani, N. (2023, 28 Sep). El retorno de minería ilegal en La Pampa. MAAP #193, dredge counts. https://www.maapprogram.org/es/retorno-mineria-la-pampa-peru/ (accessed 2026-10-10)

AI is not a source: no fact above is cited to an AI tool.

## Appendix A. Data log and definitions

`DOWNLOAD_LOG.csv` has one row per raw file (or per set of identical-format files): source, URL, collection, theme, years, access date, downloader and check number. Files above 50 MB and files with personal data are not in the zip; the log links them. Definitions used everywhere (`code/definitions.py`): net additions = new + re-mined − stopped; zones = official SERNANP buffer zones kept whole (overlaps go to Tambopata, as MapBiomas does), the La Pampa sector, the D.L. 1100 corridor outside buffer zones (across the road: ≤ 10 km north of the highway at La Pampa's longitudes), native communities, rest of Madre de Dios; periods 2016–18, 2019–21, 2022–25. `output/brief_numbers.csv` lists every number in this brief, in order of appearance, with its measure, zone and period.

## Appendix B. AI output for part 4

**Prompt (the course's required prompt, our comparison filled in):** "Here is my comparison: Units: the buffer zone of the Tambopata National Reserve in Madre de Dios, Peru, where the government enforcement operation "Operación Mercurio" against illegal gold mining started in February 2019, versus the buffer zone of the Amarakaeri Communal Reserve, a nearby zone with mining that was less treated (a follow-up operation in 2019 also covered it), plus 13 other Peruvian buffer zones with mining as additional comparisons. Years: 2014–2025. Outcome: net mining additions per year in hectares, i.e. the annual change in area classified as mining in MapBiomas Peru Collection 4 satellite land-cover maps, which equals land mined for the first time plus old mining land mined again minus mining land that left the mining class. Comparison: the change in mean annual net additions from 2016–18 (before) to 2019–21 (during the operation and its follow-ups) in Tambopata minus the same change in Amarakaeri (difference-in-differences: −1,761 ha/yr), and the same with zone and year fixed effects across all 15 zones. List the reasons this comparison could mislead, distinguishing omitted variables, reverse causation, selection of units, and measurement error in the outcome. For each, say what data or design would fix it."

**Tool:** Claude Code CLI 2.1.300 (Anthropic), non-interactive, no tools, run outside our project folder (no access to our files), 2026-10-15. **Raw answer:** reproduced in full below (Appendix B1). **Edited version:** part 4(b) above.

**What we kept, changed and dropped:**
- *Kept:* mean reversion (targeted at the peak), displacement into the comparison, one treated unit (placebo inference), net additions mixing new, re-mined and exits (the AI's "net additions could fall while mining activity stays the same"), dredges invisible to the maps.
- *Added from our own tests:* the size of each part (half the fall is stopping), the flicker share, the direction of each bias, and the fake-start check.
- *Dropped, could not do with our data or time:* hydrology and cloud-cover controls, per-zone accuracy assessment, a dose built from operation logs, distance-to-base designs (no patrol records available to us).
- *Corrected:* the AI dates follow-up operations under "Plan Restauración extensions" in 2019; Plan Restauración is from 2021 (MINAM, 2021).

### Appendix B1. Raw AI answer (unedited)

{{TEXT:ai_part4_raw}}
