<!--
Source of docs/brief/BRIEF_DRAFT.md and BRIEF_DRAFT.html. Build: `uv run python docs/overnight/build_report.py`.
Placeholders {{id}} / {{id:fmt}} come from output/numbers.csv. Claim tags: [[D]] description, [[P]] prediction, [[C]] causal.
Target: 2 printed pages for parts 1-4 (references and appendix do not count).
-->

# When the patrols leave: what Operation Mercurio tells FZS about enforcement against gold mining

Group Giant Anteater · Data for Good · Question 2 · October 2026 · DRAFT

## 1. The question

**FZS pays for enforcement and needs to know what it buys.** FZS supports SERNANP's operations against alluvial gold mining in the Tambopata–Bahuaja-Sonene landscape (FZS, n.d.). Operations are costly and temporary. So the practical question is: **what happens in the targeted area, and around it, when an operation ends?**

Mining could stop (**deterrence**), move next door (**displacement**) or wait and return (**delay**). Inside the target alone, all three look alike at first, so we need comparison areas.

**Our case:** Operation Mercurio, from February 2019 at La Pampa, Peru's largest illegal mining area, in the buffer zone of Tambopata National Reserve (Madre de Dios). **Targeted:** Tambopata buffer zone. **Comparison:** 14 other Peruvian buffer zones with mining, two rule-based twins abroad, and 1-km cells outside the corridor; the Amarakaeri buffer zone counts as "less treated" (Mercurio II reached it in late 2019). **Also tracked:** the reserve itself and the rest of Madre de Dios, 2014–2025. Brazil's Yanomami operation (2023) is a shorter second case.

## 2. Data and provenance

**Outcome:** new mining area per year (ha), MapBiomas Peru Collection 4, class "mining". Buffer zones (course data), check: Tambopata buffer zone 2025 = 20,730 ha, as on the MapBiomas platform. Protected areas (our download), check: Tambopata National Reserve 2025 = {{anp_level_tam_nr_2025:,.1f}} ha vs 777 ha on the platform. **Context:** World Bank gold price (check: Aug 2026 = $4,411/oz); Madre de Dios gold output (MINEM; the official series includes an artisanal *estimate* until 2019, so it is not a production series; check: 2019 total = central bank figure); MapBiomas Brazil Collection 11 (all indigenous lands 2025 = 39,915 ha). **Zones and timing:** the same MapBiomas maps as rasters, cut to our own zones (check: Tambopata buffer zone 2025 = {{v2_check_tambopatabufferzone_2025}} ha vs 20,730), UMD GLAD forest-loss alerts, INGEMMET geology. **Twin search:** Amazon Mining Watch mining scars (Earth Genome), RAISG protected-area maps, MapBiomas Amazonía Collection 6 (check: Amazon mining 2023 = 775,746 ha vs 0.78 Mha published). Every file is in `DOWNLOAD_LOG.csv`; one script, `code/main.py`, produces every number and the figure.

## 3. Findings

![Land mined for the first time per year: La Pampa sector vs the legal corridor across the road (top); all of Madre de Dios, inside vs outside the corridor (bottom)](output/fig_brief_main.png)

**During the operation, net new mining in the target collapsed** [[D]]. The Tambopata buffer zone fell from {{mean_add_tambopata_2016_18}} to {{mean_add_tambopata_2019_21}} ha/yr (2016–18 vs 2019–21), while the less-treated Amarakaeri zone rose from {{mean_add_amarakaeri_2016_18}} to {{mean_add_amarakaeri_2019_21}}: a gap of **{{did_main}} ha/yr** ({{did_main_base_2014_18}} with a 2014–18 baseline). Almost half of the net fall is old mining going out of use: land mined for the *first* time fell less, from {{t5_m2_2016_18}} to {{t5_m2_2019_21}} ha/yr, and forest-loss alerts show clearing continued through 2019.

**Large in hectares, ordinary relative to size** [[D]]. With zone and year effects (which absorb the gold price and COVID), Tambopata's 2019–21 gap is {{model_m1_during}} to {{model_m3_during}} ha/yr and ranks 1 of {{model_m1_n}} when each zone in turn gets a fake operation (p = {{model_m1_ri_p:.2f}}, the smallest this test allows). Scaled to each zone's size it ranks {{model_m4_rank:.0f}} of {{model_m4_n:.0f}}. Per 1-km cell against cells outside the corridor, La Pampa's change is {{st_main_lapampasector_during:+.2f}} ha per cell-year (p = {{st_main_lapampasector_during_p:.2f}}; wild bootstrap p = {{st_wcb_lp_p:.2f}}), but its pre-trends fail (p = {{st_event_lp_pretrend_p:.3f}}). Two rule-based twins abroad (no operation 2017–21, lowland, similar size) both grew faster: Tambopata ran at {{top3_median_ratio:.0%}} of their pace.

**Therefore** [[C]], *if the comparison zones show what Tambopata would otherwise have done*, Mercurio cut **net** new mining in its target by roughly {{model_m1_during:,.0f}} to {{model_m3_during:,.0f}} ha/yr in 2019–21. This is fragile: with one targeted zone the best attainable p is {{model_m1_ri_p:.2f}}, the fall is not unusual for La Pampa's size, and local shocks remain possible.

**It did not last, and mining crossed the road** [[D]]. In 2022–25 Tambopata averaged {{mean_add_tambopata_2022_25}} ha/yr, much of it on old pits. The three Madre de Dios buffer zones together went {{mean_add_three_bz_sum_2016_18}} → {{mean_add_three_bz_sum_2019_21}} → {{mean_add_three_bz_sum_2022_25}} ha/yr. Directly across the highway, in the legal corridor, first-time mining rose from {{v2_new_corridoracrosstheroa_2016_18}} to {{v2_new_corridoracrosstheroa_2019_21}} ha/yr. Right at the road, a spatial regression discontinuity (land just north vs just south, before vs after) shows the step flipping north: +{{rd_road_did:.1f}} points of land mined a year (p = {{rd_road_did_p:.2f}}; {{rd_road_sens_donut_p:.2f}} without the 500 m beside the road), a swing that counts both the fall south and the gain north. The corridor's share of the department's new mining rose from {{v2_corridor_share_2016_18:.0f}}% to {{v2_corridor_share_2022_25:.0f}}% (MAAP #208: 74%), while the total kept growing ({{v2_new_total_2016_18}} → {{v2_new_total_2022_25}} ha/yr). Most corridor growth is not displaced La Pampa mining; it outgrew La Pampa's fall. La Pampa had not run out of gold ({{gold_broad_lapampasector_depleted_2018:.0%}} of its gold-bearing land mined by 2018).

**Miners now enter the reserve** [[D]]: +{{anp_tam_nr_addition_2025}} ha inside it in 2025. MAAP reports ~500 ha from late 2025 to Feb 2026, after river posts were withdrawn (Pacsi et al., 2026). **Brazil, same method, no evidence** [[D]]: big territories fell after 2022–24, but a staggered DiD across 24 territories gives the wrong sign ({{brv2_did2s_treat:+.2f}} log points, p = {{brv2_did2s_treat_p:.2f}}); national gold rules changed in 2023 and the test has little power.

## 4. What FZS can do with this

**(a) What FZS learns** [[P]]. Expect a sharp local fall while patrols are present, a move across the nearest legal boundary, a return to old pits within about three years, and no fall in the region, as after the 2012–13 interdictions (Asner & Tupayachi, 2017). **Fund enforcement as a permanent presence, not a one-off sweep.** Patrol the legal side of the boundary, watch old pits, and staff river posts (the 2025 incursion followed a withdrawal). **Make the corridor a filter:** with a 0% royalty for small producers (Ley 28258) and only 145 of 9,592 registered miners fully formal (MINAM, 2021), gold-origin tracing there would remove the cheapest escape.

**(b) Why this could mislead, and which way.** *Omitted variables:* COVID, the gold price and later waves (2021, 2023) overlap the post-period; year effects remove shared shocks, and controls for COVID exposure and enforcement money keep {{ctx_k3_vs_k0_share:.0%}} of the gap. *Reverse causation:* La Pampa was targeted at its peak, so part of the drop could be a return to normal (overstates the fall); but 2019–21 fell below every earlier year. *Selection of units:* one targeted zone makes standard errors meaningless (Conley & Taber, 2011), so we rank against fake targets; Amarakaeri received miners (overstates) but had its own operation (understates); the best twin sat in Brazil's weak-enforcement years (overstates). *Measurement:* hectares are a proxy for miners; the satellite class mixes legal and illegal mining, counts re-mining as new, and **cannot see river dredges or mercury**. MAAP counted 148 → 598 dredges in La Pampa, 2021–23 (Yupanqui et al., 2023). Activity moved to old pits and rivers, which add few hectares, so **our fall is an upper bound and the return a lower bound**.

**(c) What would let us say more.** Dated patrol and interdiction records per zone from SERNANP or FZS (enforcement intensity instead of a 0/1 flag); concession and REINFO maps to grade legality pixel by pixel; more operations as cases (Plan Restauración 2021 covered several zones); river-dredge counts and mercury sampling.

## References

- Asner, G. P., & Tupayachi, R. (2017). Accelerated losses of protected forests from gold mining in the Peruvian Amazon. *Environmental Research Letters*, 12, 094004. https://doi.org/10.1088/1748-9326/aa7dab
- Conley, T. G., & Taber, C. R. (2011). Inference with "difference in differences" with a small number of policy changes. *Review of Economics and Statistics*, 93(1), 113–125. https://doi.org/10.1162/REST_a_00049
- Finer, M., & Mamani, N. (2020). Illegal gold mining down 78% in Peruvian Amazon, but still threatens key areas. MAAP #130. https://www.maapprogram.org/gold-mining-peru/
- Finer, M., & Mamani, N. (2024). Gold mining in the southern Peruvian Amazon, summary 2021–2024. MAAP #208. https://www.maapprogram.org/maap-208-gold-mining-in-the-southern-peruvian-amazon-summary-2021-2024/
- Dethier, E. N., Silman, M. R., Fernandez, L. E., Caballero Espejo, J., Alqahtani, S., Pauca, P., & Lutz, D. A. (2023). Operation Mercury: Impacts of national-level armed forces intervention and anticorruption strategy on artisanal gold mining and water quality in the Peruvian Amazon. *Conservation Letters*, 16, e12978. https://doi.org/10.1111/conl.12978
- Earth Genome (2026). Amazon Mining Watch, mining detections, model 48px_v4.10b (updated 3 Oct 2026). https://source.coop/earthgenome/amazon-mining-watch
- Frankfurt Zoological Society (n.d.). Bahuaja-Sonene and Tambopata. https://fzs.org/en/programs/peru/bahuaja-sonene-and-tambopata/
- MapBiomas Peru (2025). Collection 4 of annual land cover maps of Peru (buffer-zone and protected-area statistics). https://peru.mapbiomas.org
- INGEMMET (2026). GEOCATMIN, Mapa geológico integrado 1:100,000 (map service, layer 6). https://geocatmin.ingemmet.gob.pe
- Ley N° 28258 (2004), Ley de Regalía Minera, Art. 4.4 (0% for small producers and artisanal miners). Congreso de la República del Perú.
- MapBiomas Amazonía (2024). Colección 6.0 de mapas anuales de cobertura y uso del suelo en la Amazonía, 1985–2023. https://amazonia.mapbiomas.org
- MapBiomas Brasil (2025). Collection 11 (mining) and Collection 10.1 (indigenous-territory statistics). https://brasil.mapbiomas.org
- MINAM (2021). Plan Restauración (Anexo, D.S. N° 017-2021-MINAM). Ministerio del Ambiente, Lima.
- Pacsi, R., et al. (2026). Rapid expansion of illegal gold mining in Tambopata National Reserve. MAAP #241. https://www.maapprogram.org/mining-peru-tambopata/
- RAISG (2026). Áreas Naturales Protegidas Nacionales (map service). https://geo.socioambiental.org/raisg/rest/services/raisg/rg_srv_mapas_anps/MapServer/2
- University of Maryland GLAD (2026). GLAD-L Landsat forest-loss alerts, 2017–2026 (public bucket). https://storage.googleapis.com/earthenginepartners-hansen/
- World Bank (2026). Commodity price data (Pink Sheet).
- Yupanqui, O., et al. (2023). El retorno de minería ilegal en La Pampa. MAAP #193. https://www.maapprogram.org/es/retorno-mineria-la-pampa-peru/

*Every team member must re-open what they cite and fill in the access dates. AI is not a source.*

## Appendix A. Data log

See `DOWNLOAD_LOG.csv`: one row per raw file with URL, access date, collection, sha256 and check number.

## Appendix B. AI output for part 4

- **Raw answer:** `docs/brief/ai_part4_raw.md` (prompt as required by the course; tool and date noted there).
- **Our edited version:** part 4(b) above.

**What we changed and why:**
- The raw answer calls any causal claim "not supported". We kept one causal claim, made it conditional, and backed it with the fake-date and fake-place tests the AI itself suggested.
- We added the mean-reversion check: 2019–21 fell below every year of 2011–18.
- We dropped suggestions we could not carry out: road and geology covariates, and radar.
