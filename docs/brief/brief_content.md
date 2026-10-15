<!--
Source of docs/brief/BRIEF.md / .html / .pdf / .docx. Build: `uv run python docs/walkthrough/build_report.py`.
Placeholders {{id}} / {{id:fmt}} come from output/numbers.csv; the build also writes output/brief_numbers.csv (every
number in order of appearance). Claim tags: [[D]] description, [[P]] prediction, [[C]] causal.
Plan v3 (docs/PLAN_v3.md): ONE measure, net mining additions = new land + re-mined − stopped (ha/yr);
ONE zone registry; treatment = Mercurio from Feb 2019 (first treated year 2019). Target: 2 printed pages for parts 1-4.
-->

# When the patrols leave: what Operation Mercurio tells FZS about enforcement against gold mining

Group Giant Anteater · Data for Good · Question 2 · October 2026 · Ruby Ann Grambauer, Sebastian Schmid, Laurens van der Lely, Omkar Mate, Dhruv Chaudhari

## 1. The question

**FZS pays for enforcement and needs to know what it buys.** It supports SERNANP's operations against alluvial gold mining around Tambopata and Bahuaja-Sonene (FZS, n.d.). Operations are costly and temporary, so: **what happens in the targeted area, and around it, when an operation ends?** Mining could stop (**deterrence**), move (**displacement**) or return (**delay**); inside the target these look alike, so we need comparisons.

**Case:** Operation Mercurio at La Pampa, Peru's largest illegal mining area, in the buffer zone of Tambopata National Reserve (Madre de Dios). **Treatment:** its start in February 2019 (first treated year 2019); COVID-19 (2020), Plan Restauración (2021) and the April 2023 state of emergency are context, so we measure "Mercurio and what followed". **Target:** the Tambopata buffer zone (official boundary) and its La Pampa sector (70.15–69.80 W). **Comparison:** the Amarakaeri buffer zone, only "less treated" (Mercurio II covered all of Madre de Dios in 2019; MINAM, 2021, p. 33), and the 14 other Peruvian buffer zones with mining. **Around it:** the legal corridor across the highway, the reserve, the department. **Periods:** 2016–18, 2019–21, 2022–25 ("later years").

## 2. Data and provenance

**One outcome everywhere: net mining additions** (ha/yr) = land mined for the first time (**new land**) + old mining land mined again (**re-mined**) − mining land that left the mining class (**stopped**), counted pixel by pixel on the 30-m annual maps of **MapBiomas Peru, Collection 4** (class 4.2: all mining, legal and illegal). **Checks, our number vs the publisher's:** mining area (stock) 2025, Tambopata buffer zone {{chk_tbz_2025_ours}} vs {{chk_tbz_2025_pub}} ha; Tambopata reserve {{chk_tnr_2025_ours}} vs {{chk_tnr_2025_pub}} ha; Madre de Dios {{chk_mdd_2025_ours}} vs {{chk_mdd_2025_pub}} ha (0.01%: department boundary versions). **Context:** World Bank gold price, Aug 2026, ${{chk_gold_aug2026_ours}} vs ${{chk_gold_aug2026_pub}}/oz; Madre de Dios gold output 2019 (MINEM files rebuilt vs central bank, BCRP) {{chk_bcrp_2019_ours}} vs {{chk_bcrp_2019_pub}} kg (0.4%; an artisanal *estimate* until 2019); Madre de Dios enforcement spending (MEF, programme PP 0128) 2019, S/ {{chk_pp0128_2019_ours}} vs {{chk_pp0128_2019_pub}}. **Cross-checks only, other products:** Amazon Mining Watch (AMW; no publisher totals: our zone cut agrees with a polygon cut, Tambopata buffer zone mining 2018 {{chk_amw_tbz_2018_ours}} vs {{chk_amw_tbz_2018_pub}} ha); MapBiomas Amazonía Col. 6, mining area of the whole Amazon 2023, {{chk_mb_amazonia_2023_ours:,.0f}} vs 780,000 ha. Files: `DOWNLOAD_LOG.csv`; every number and the figure: `code/main.py`.

## 3. Findings

![Net mining additions and their three parts, Tambopata buffer zone 2014–2025 (top); net additions by area, Madre de Dios, period means (bottom)](output/fig_brief_main.png)

**It fell: net mining in the target dropped 90%** [[D]]. In the Tambopata buffer zone net additions fell from {{tambopata_bz_pre_net}} ha/yr (2016–18) to {{tambopata_bz_during_net}} (2019–21), while the less-treated Amarakaeri buffer zone rose from {{amarakaeri_bz_pre_net}} to {{amarakaeri_bz_during_net}}: a difference in differences of **{{did_main_net}} ha/yr** (2016–18 base). With a fake start in 2016 (2013–15 vs 2016–18) it is {{did_placebo_net:+,.0f}}. Every 2019–21 year (≤ {{tambopata_bz_net_max_during}} ha/yr) was below every 2011–18 year (≥ {{tambopata_bz_net_min_2011_18}} ha/yr).

**In 2019, new pits kept opening while old ones went quiet** [[D]]. New land in the Tambopata buffer zone was still {{tambopata_bz_2019_new}} ha in 2019 (2018: {{tambopata_bz_2018_new}}), but {{tambopata_bz_2019_stopped}} ha stopped, so net additions were only {{tambopata_bz_2019_net}} ha. Over 2019–21, stopping explains a quarter to a half of the fall ({{tambopata_bz_stopped_share_of_fall_min:.0%}}–{{tambopata_bz_stopped_share_of_fall_max:.0%}}, depending on whether land mined again within two years counts), {{tambopata_bz_excess_stopped_share_in_2019:.0%}} of the extra stopping came in 2019, and the rest of the fall is fewer new pits, mainly in 2020–21 (COVID). In Amarakaeri stopped land stayed flat ({{amarakaeri_bz_pre_stopped}} → {{amarakaeri_bz_during_stopped}} ha/yr). In the Tambopata buffer zone half of the stopped land became water ({{tambopata_bz_during_stopped_share_to_water:.0%}}) and {{tambopata_bz_during_stopped_share_back_within_2y:.0%}} was mined again within two years (2016–18: {{tambopata_bz_pre_stopped_share_back_within_2y:.0%}}). With other indicators (mining ponds), Dethier et al. (2023) report 70–90% of activity abandoned in the targeted zones and faster mining just outside them.

**Where it went: mining rose next door, and the region never fell** [[D]]. In the corridor strip just across the highway (≤ 10 km north, opposite La Pampa) net additions rose from {{corridor_across_pre_net}} to {{corridor_across_during_net}} ha/yr (2016–18 vs 2019–21). On all legal mining-corridor land (D.L. 1100) the share of the department's net additions rose from {{v2_corridor_share_pre_net:.0%}} to {{v2_corridor_share_during_net:.0%}} (period sums). Madre de Dios went {{mdd_pre_net}} → {{mdd_during_net}} → {{mdd_later_net}} ha/yr (2016–18 → 2019–21 → 2022–25).

**Why and how it came back: money faded, gold soared, old pits reopened** [[D]]. Enforcement spending in Madre de Dios (PP 0128) peaked at S/ {{t8_pp0128_mdd_2019:,.0f}} in 2019 and fell to S/ {{t8_pp0128_mdd_2025:,.0f}} in 2025, while the gold price rose {{gold_price_ratio_2025_2018:.1f}}-fold (2018–25). In 2022–25 the Tambopata buffer zone averaged {{tambopata_bz_later_net}} ha/yr ({{tambopata_bz_later_ex2023_net}} without 2023, a spike only MapBiomas shows); a third to a half of the land added was re-mined ({{tambopata_bz_later_ex2023_remined_share_added:.0%}}–{{tambopata_bz_later_remined_share_added:.0%}}, without/with 2023). Inside Tambopata National Reserve net additions were +{{tambopata_nr_2025_net}} ha in 2025; MAAP reports ~500 ha from late 2025 to Feb 2026, the year the navy left the river posts (Pacsi et al., 2026).

**What we can say about cause** [[C]]. *If the other Peruvian buffer zones show what the Tambopata buffer zone would otherwise have done*, Mercurio and the operations that followed lowered its net mining additions by about {{model_m1_during_net:,.0f|abs}} to {{did_base2014_net:,.0f|abs}} ha/yr in 2019–21 (against all 14 other zones, or Amarakaeri alone, with a 2014–18 base). A quarter to a half of that is pits going quiet; the rest is fewer new pits. Six methods point down; two hold up in hectares; none passes all its own checks: the fall is the largest of 15 zones in hectares (as in 2014–16, before Mercurio: it is the biggest zone), but only {{model_m4_rank:.0f}}rd to {{placebo_space_rank_scaled:.0f}}th of 7 relative to each zone's size. Read it as an upper bound (4b).

## 4. What FZS can do with this

**(a) What FZS learns** [[P]]. From this one case: a sharp local fall while the operation runs, a quarter to a half of it pits going quiet; mining rising next door and across the nearest legal boundary; a return within about three years, largely on old pits; no fall in the region. So: **fund presence, not one-off sweeps; watch a ring of a few kilometres around each operation with near-real-time forest-loss alerts** (new pits kept opening in 2019); **guard the reserve's first kilometre and the river posts** ({{rd_reserve_inside_share_1km:.0%}} of first-time mining inside the reserve along its buffer-zone border, 2000–25, lies within 1 km of the edge); and trace gold origin in the corridor (0% royalty for small producers, Ley 28258, Art. 5; nationally 9,592 miners in the formalization register but 145 fully formalized, MINAM, 2021, pp. 55–56).

**(b) Why this could mislead, and which way.** *Omitted variables:* COVID-19, the gold price (×{{gold_price_ratio_2025_2018:.1f}}, 2018–25) and later operations overlap 2019–21 and need not hit all zones alike (probably overstates the fall). *Reverse causation:* La Pampa was targeted at its peak; part of the fall is a return to normal (overstates). *Selection of units:* one targeted zone, far larger than any comparison, so standard errors are not informative (Conley & Taber, 2011) and ranks in hectares mostly measure size; Amarakaeri received miners (overstates) but had its own operation (understates). *Measurement error:* net additions mix three processes; part of "stopped" is temporary or map noise, so **net additions can fall while activity does not** (overstates); hectares proxy for miners; the class mixes legal and illegal mining; **satellites cannot see river dredges or mercury** (MAAP counted 148 → 598 dredges in La Pampa, 2021–23; Yupanqui et al., 2023), so a shift to rivers adds no hectares (overstates). **Read the fall as an upper bound and the return as a lower bound.**

**(c) What would let us say more.** Dated patrol and interdiction records from SERNANP or FZS (were the stopped pits the raided ones?); an image-checked sample of stopped pits; concession and formalization-register (REINFO) maps to grade legality pixel by pixel; dredge counts and mercury sampling; more operations as cases.

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

**Tool:** Claude Code CLI 2.1.300 (Anthropic), non-interactive, no tools, run outside our project folder (no access to our files), 2026-10-15. The prompt quotes −1,761 ha/yr, our value before a later 0.07% pixel-area correction; the brief uses the corrected −1,762. **Raw answer:** reproduced in full below (Appendix B1). **Edited version:** part 4(b) above.

**What we kept, changed and dropped:**
- *Kept:* mean reversion (targeted at the peak), displacement into the comparison, one treated unit (placebo inference), net additions mixing new, re-mined and exits (the AI's "net additions could fall while mining activity stays the same"), dredges invisible to the maps.
- *Added from our own tests:* the size of each part (stopping explains a quarter to a half of the fall), the flicker share, the direction of each bias, and the fake-start check.
- *Dropped, could not do with our data or time:* hydrology and cloud-cover controls, per-zone accuracy assessment, a dose built from operation logs, distance-to-base designs (no patrol records available to us).
- *Corrected:* the AI dates follow-up operations under "Plan Restauración extensions" in 2019; Plan Restauración is from 2021 (MINAM, 2021).

### Appendix B1. Raw AI answer (unedited)

{{TEXT:ai_part4_raw}}
