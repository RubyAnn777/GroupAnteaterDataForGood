<!--
Source of docs/brief/BRIEF_DRAFT.md and BRIEF_DRAFT.html. Build: `uv run python docs/overnight/build_report.py`.
Placeholders {{id}} / {{id:fmt}} come from output/numbers.csv. Claim tags: [[D]] description, [[P]] prediction, [[C]] causal.
Target: 2 printed pages for parts 1-4 (references and appendix do not count).
-->

# When the patrols leave: what Operation Mercurio tells FZS about enforcement against gold mining

Group Giant Anteater · Data for Good · Question 2 · October 2026 · DRAFT

## 1. The question

**FZS pays for enforcement and needs to know what it buys.** FZS supports SERNANP's operations against alluvial gold mining in the Tambopata–Bahuaja-Sonene landscape (FZS, n.d.). Operations are costly and temporary, so the practical question is: **what happens in the targeted area, and around it, when an operation ends?** Mining could stop (**deterrence**), move next door (**displacement**) or wait and return (**delay**). Inside the target alone these look alike, so we need comparison areas.

**Our case:** Operation Mercurio, from February 2019 at La Pampa, Peru's largest illegal mining area, in the buffer zone of Tambopata National Reserve (Madre de Dios). **Targeted:** Tambopata buffer zone, 2014–2025. **Comparison:** 14 other Peruvian buffer zones with mining, two rule-based twins abroad, 1-km cells outside the corridor. Amarakaeri is only "less treated": Mercurio II covered all of Madre de Dios in 2019 (MINAM, 2021, p. 33). **Also tracked:** the reserve, the rest of Madre de Dios, and Brazil's Yanomami operation (2023).

## 2. Data and provenance

**Outcome:** new mining area per year (ha), MapBiomas Peru Collection 4, class "mining". Buffer zones (course data), check: Tambopata buffer zone 2025 = 20,730 ha, as on the platform; protected areas (our download): Tambopata reserve 2025 = {{anp_level_tam_nr_2025:,.1f}} ha vs 777; the same maps as rasters cut to our zones: {{v2_check_tambopatabufferzone_2025}} vs 20,730 ha. **Context:** World Bank gold price (Aug 2026 = $4,411/oz); MINEM Madre de Dios gold (an artisanal *estimate* until 2019, so not a production series; 2019 = central bank figure); MapBiomas Brazil Col. 11 (indigenous lands 2025 = 39,915 ha); GLAD forest-loss alerts; INGEMMET geology. **Twins:** Amazon Mining Watch (Earth Genome), RAISG, MapBiomas Amazonía Col. 6 (Amazon mining 2023 = 775,746 ha vs 0.78 Mha published). All files in `DOWNLOAD_LOG.csv`; `code/main.py` produces every number and the figure.

## 3. Findings

![Land mined for the first time per year: La Pampa sector vs the legal corridor across the road (top); all of Madre de Dios, inside vs outside the corridor (bottom)](output/fig_brief_main.png)

**During the operation, net new mining in the target collapsed** [[D]]. The Tambopata buffer zone fell from {{mean_add_tambopata_2016_18}} to {{mean_add_tambopata_2019_21}} ha/yr (2016–18 vs 2019–21) while the less-treated Amarakaeri rose from {{mean_add_amarakaeri_2016_18}} to {{mean_add_amarakaeri_2019_21}}: a gap of **{{did_main}} ha/yr**. MAAP saw mining deforestation in La Pampa fall 90% (Finer & Mamani, 2020). Almost half the net fall is old mining going out of use: *first-time* mining fell less, {{t5_m2_2016_18}} → {{t5_m2_2019_21}} ha/yr (La Pampa sector, in the figure: {{v2_new_lapampasector_2016_18}} → {{v2_new_lapampasector_2019_21}}). **Timing:** it stayed near its peak in 2019 and fell only in 2020–21, the COVID years (Dethier et al., 2023, date the halt to 2019).

**Large in hectares, ordinary relative to size, smaller with other weights** [[D]]. With zone and year effects, the 2019–21 gap is {{model_m1_during}} to {{model_m3_during}} ha/yr and ranks 1 of {{model_m1_n}} when each zone in turn gets a fake operation (p = {{model_m1_ri_p:.2f}}, this test's floor); scaled to size it ranks {{model_m4_rank:.0f}} of {{model_m4_n:.0f}}. Synthetic control cannot fit Tambopata's past, and synthetic DiD swings with the baseline years it picks. Twins abroad and {{psm_n_methods:.0f}} matching estimators all find Tambopata slower ({{top3_median_ratio:.0%}} of the twins' pace) but none beats chance (placebo p {{psm_p_min:.2f}}–{{psm_p_max:.2f}}), and Tambopata outgrew both twins before 2019. Per 1-km cell La Pampa changes {{st_main_lapampasector_during:+.2f}} ha per cell-year (p = {{st_main_lapampasector_during_p:.2f}}), but comparison cells hold almost no mining and pre-trends fail (p = {{st_event_lp_pretrend_p:.3f}}): little more than a before/after.

**Therefore** [[C]], *if the other Peruvian buffer zones show what the Tambopata buffer zone would otherwise have done*, Mercurio and the operations that followed lowered its **net** mining additions by about {{model_m1_during:,.0f|abs}} to {{did_main_base_2014_18:,.0f|abs}} ha/yr in 2019–21 (all 14 zones, or Amarakaeri alone, against a 2014–18 baseline). About half of that is mined land going out of use rather than less new clearing; new clearing fell only from 2020, the COVID years; and relative to its size the fall is not unusual (rank {{model_m4_rank:.0f}} of {{model_m4_n:.0f}}). Read it as likely an upper bound (part 4b).

**It did not last, and new mining grew across the road** [[D]]. In 2022–25 Tambopata averaged {{mean_add_tambopata_2022_25}} ha/yr ({{mean_add_tambopata_2022_25_ex2023}} without 2023, a spike everywhere), much of it on old pits; the three Madre de Dios buffer zones went {{mean_add_three_bz_sum_2016_18}} → {{mean_add_three_bz_sum_2019_21}} → {{mean_add_three_bz_sum_2022_25}} ha/yr. Across the highway, in the legal corridor, first-time mining rose from {{v2_new_corridoracrosstheroa_2016_18}} to {{v2_new_corridoracrosstheroa_2019_21}} ha/yr. A spatial regression discontinuity at the road (just north vs just south, before vs after) puts the step +{{rd_road_did:.1f}} points of land a year further north (p = {{rd_road_did_p:.2f}}; {{rd_road_sens_p_min:.2f}}–{{rd_road_sens_p_max:.2f}} across bandwidths), counting the fall south and the gain north together; Dethier et al. (2023) also see mining accelerate in permitted concessions north of the highway. The corridor's share of the department's new mining rose from {{v2_corridor_share_2016_18:.0f}}% to {{v2_corridor_share_2022_25:.0f}}% (MAAP: 74% of 2021–Mar 2024 mining deforestation; Finer & Mamani, 2024) while the total grew ({{v2_new_total_2016_18}} → {{v2_new_total_2022_25}} ha/yr): the corridor's rise exceeds La Pampa's fall, so it is not all miners moving. La Pampa had not run out of gold ({{gold_broad_lapampasector_depleted_2018:.0%}} of its gold-bearing land mined by 2018).

**Mining inside the reserve jumped** [[D]]: +{{anp_tam_nr_addition_2025}} ha in 2025; MAAP reports ~500 ha from late 2025 to Feb 2026, after the navy left the river posts and as gold soared (Pacsi et al., 2026). **Brazil, same method, no evidence** [[D]]: a staggered DiD across {{brv2_n_units}} territories gives the wrong sign ({{brv2_did2s_treat:+.2f}} log points, p = {{brv2_did2s_treat_p:.2f}}); gold rules changed in 2023 and power is low.

## 4. What FZS can do with this

**(a) What FZS learns** [[P]]. From this one case, expect a sharp local fall while patrols are present, new mining growing across the nearest legal boundary, a return within about three years (much of it to old pits), and no fall in the region. Asner & Tupayachi (2017) describe a similar regional pattern after the 2012 interdictions (a brief dip, then a near doubling, also inside the reserve), although our maps show no 2012–13 dip in La Pampa. **Fund enforcement as a permanent presence, not a one-off sweep.** Patrol the legal side of the boundary, watch old pits, and staff river posts (the 2025 incursion followed a withdrawal). **Make the corridor a filter:** with a 0% royalty for small producers (Ley 28258, Art. 5) and 9,592 miners registered in formalization but only 145 fully formalized (MINAM, 2021, pp. 55–56), gold-origin tracing there would close an easy outlet.

**(b) Why this could mislead, and which way.** *Omitted variables:* COVID, the gold price and later waves (2021, 2023) overlap the post-period; year effects remove shared shocks. A COVID-exposure control shrinks the gap to {{ctx_k1_during:,.0f|abs}} of {{ctx_k0_during:,.0f|abs}} ha/yr; adding enforcement money keeps {{ctx_k3_vs_k0_share:.0%}}, but money is partly the treatment (a bad control). *Reverse causation:* La Pampa was targeted at its peak, so part of the drop may be a return to normal (overstates); yet every 2019–21 year (≤ {{tam_add_max_2019_2021}} ha) fell below every 2011–18 year (≥ {{tam_add_min_2011_2018}}). *Selection of units:* with one targeted zone standard errors are unreliable (Conley & Taber, 2011), so we rank against fake targets; Amarakaeri received miners (overstates) but had its own operation (understates); the best twin sat in Brazil's weak-enforcement years (overstates). *Measurement:* hectares proxy for miners; the class mixes legal and illegal mining, counts re-mining as new, and **cannot see river dredges or mercury**: MAAP counted 148 → 598 dredges in La Pampa, 2021–23 (Yupanqui et al., 2023). Activity moved to old pits and rivers, which add few hectares. Most biases overstate the fall: **read it as likely an upper bound, and the return as a lower bound**.

**(c) What would let us say more.** Dated patrol and interdiction records per zone from SERNANP or FZS (enforcement intensity instead of a 0/1 flag); concession and REINFO maps to grade legality pixel by pixel; more operations as cases (Plan Restauración 2021 covered several zones); river-dredge counts and mercury sampling.

## References

- Asner, G. P., & Tupayachi, R. (2017). Accelerated losses of protected forests from gold mining in the Peruvian Amazon. *Environmental Research Letters*, 12, 094004. https://doi.org/10.1088/1748-9326/aa7dab
- Conley, T. G., & Taber, C. R. (2011). Inference with "difference in differences" with a small number of policy changes. *Review of Economics and Statistics*, 93(1), 113–125. https://doi.org/10.1162/REST_a_00049
- Finer, M., & Mamani, N. (2020, 1 Dec). Illegal gold mining down 78% in Peruvian Amazon, but still threatens key areas. MAAP #130. https://www.maapprogram.org/gold-mining-peru/
- Finer, M., & Mamani, N. (2024, 8 May). Gold mining in the southern Peruvian Amazon, summary 2021–2024. MAAP #208. https://www.maapprogram.org/maap-208-gold-mining-in-the-southern-peruvian-amazon-summary-2021-2024/
- Dethier, E. N., Silman, M. R., Fernandez, L. E., Caballero Espejo, J., Alqahtani, S., Pauca, P., & Lutz, D. A. (2023). Operation Mercury: Impacts of national-level armed forces intervention and anticorruption strategy on artisanal gold mining and water quality in the Peruvian Amazon. *Conservation Letters*, 16(5), e12978. https://doi.org/10.1111/conl.12978
- Earth Genome (2026). Amazon Mining Watch, mining detections, model 48px_v4.10b (updated 3 Oct 2026). https://source.coop/earthgenome/amazon-mining-watch
- Frankfurt Zoological Society (n.d.). Bahuaja-Sonene and Tambopata. https://fzs.org/en/programs/peru/bahuaja-sonene-and-tambopata/
- MapBiomas Peru (2025). Collection 4 of annual land cover maps of Peru (buffer-zone and protected-area statistics). https://peru.mapbiomas.org
- INGEMMET (2026). GEOCATMIN, Mapa geológico integrado 1:100,000 (map service, layer 6). https://geocatmin.ingemmet.gob.pe
- Ley N° 28258 (2004), Ley de Regalía Minera, Art. 5 and Art. 10 (0% for small producers and artisanal miners). Congreso de la República del Perú.
- MapBiomas Amazonía (2024). Colección 6.0 de mapas anuales de cobertura y uso del suelo en la Amazonía, 1985–2023. https://amazonia.mapbiomas.org
- MapBiomas Brasil (2025). Collection 11 (mining) and Collection 10.1 (indigenous-territory statistics). https://brasil.mapbiomas.org
- MINAM (2021). Plan Restauración: Plan integral frente a la minería ilegal (Anexo, D.S. N° 017-2021-MINAM). Ministerio del Ambiente, Lima. pp. 33, 55–56. https://faolex.fao.org/docs/pdf/per206467anx.pdf
- Pacsi, R., Novoa, S., La Torre, S., Balbuena, H., Finer, M., Santana, A., & Castillo, H. (2026, 10 May). Rapid expansion of illegal gold mining in Tambopata National Reserve. MAAP #241. https://www.maapprogram.org/mining-peru-tambopata/
- RAISG (2026). Áreas Naturales Protegidas Nacionales (map service). https://geo.socioambiental.org/raisg/rest/services/raisg/rg_srv_mapas_anps/MapServer/2
- University of Maryland GLAD (2026). GLAD-L Landsat forest-loss alerts, 2017–2026 (public bucket). https://storage.googleapis.com/earthenginepartners-hansen/
- World Bank (2026). Commodity price data (Pink Sheet).
- Yupanqui, O., Quispe, M., Novoa, S., Castañeda, C., Escalante, E., Finer, M., & Mamani, N. (2023, 28 Sep). El retorno de minería ilegal en La Pampa. MAAP #193. https://www.maapprogram.org/es/retorno-mineria-la-pampa-peru/

*Every team member must re-open what they cite and fill in the access dates. AI is not a source.*

## Appendix A. Data log

See `DOWNLOAD_LOG.csv`: one row per raw file with URL, access date, collection, sha256 and check number.

## Appendix B. AI output for part 4

- **Raw answer:** `docs/brief/ai_part4_raw.md` (prompt as required by the course; tool and date noted there).
- **Our edited version:** part 4(b) above.

**What we changed and why:**
- The raw answer calls any causal claim "not supported". We kept one causal claim, made it conditional, and backed it with the fake-date and fake-place tests the AI itself suggested.
- We added the mean-reversion check: 2019–21 fell below every year of 2011–18.
- The prompt as sent called Amarakaeri a zone with no targeted operation; we later found Mercurio II covered it (part 1), so our edited version treats it as "less treated" and gives the bias both ways.
- We dropped suggestions we could not carry out: road and geology covariates, and radar.
