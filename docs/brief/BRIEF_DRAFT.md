# When the patrols leave: what Operation Mercurio tells FZS about enforcement against gold mining

Group Giant Anteater · Data for Good · Question 2 · October 2026 · DRAFT

## 1. The question

**FZS pays for enforcement and needs to know what it buys.** FZS supports SERNANP's operations against alluvial gold mining in the Tambopata–Bahuaja-Sonene landscape (FZS, n.d.). Operations are costly and temporary. So the practical question is: **what happens in the targeted area, and around it, when an operation ends?**

Mining could stop (**deterrence**), move next door (**displacement**) or wait and return (**delay**). Inside the target alone, all three look alike at first, so we need comparison areas.

**Our case:** Operation Mercurio, from February 2019 at La Pampa, Peru's largest illegal mining area, in the buffer zone of Tambopata National Reserve (Madre de Dios). **Targeted:** Tambopata buffer zone. **Comparison:** Amarakaeri buffer zone, 14 other Peruvian buffer zones with mining, and one twin abroad picked by fixed rules. **Also tracked:** the reserve itself and the rest of Madre de Dios, 2014–2025. Brazil's Yanomami operation (2023) is a shorter second case.

## 2. Data and provenance

**Outcome:** new mining area per year (ha), MapBiomas Peru Collection 4, class "mining". Buffer zones (course data), check: Tambopata buffer zone 2025 = 20,730 ha, as on the MapBiomas platform. Protected areas (our download), check: Tambopata National Reserve 2025 = 776.9 ha vs 777 ha on the platform. **Context:** World Bank gold price (check: Aug 2026 = $4,411/oz); Madre de Dios declared gold production, Central Reserve Bank of Peru (monthly values sum to annual); MapBiomas Brazil Collection 11 (all indigenous lands 2025 = 39,915 ha). **Zones and timing:** the same MapBiomas maps as rasters, cut to our own zones (check: Tambopata buffer zone 2025 = 20,716 ha vs 20,730), UMD GLAD forest-loss alerts, INGEMMET geology. **Twin search:** Amazon Mining Watch mining scars (Earth Genome), RAISG protected-area maps, MapBiomas Amazonía Collection 6 (check: Amazon mining 2023 = 775,746 ha vs 0.78 Mha published). Every file is in `DOWNLOAD_LOG.csv`; one script, `code/main.py`, produces every number and the figure.

## 3. Findings

![New mining area per year: Tambopata vs Amarakaeri buffer zones and inside Tambopata National Reserve (top); all of Madre de Dios (bottom)](../../output/fig_brief_main.png)

**During the operation, net new mining in the target collapsed** **[description]**. Tambopata fell from 1,640 to 163 ha/yr (2016–18 vs 2019–21), while Amarakaeri rose from 289 to 574: a gap in changes of **−1,762 ha/yr**. Every year of 2019–21 was below every year of 2011–18. But first-time clearing only halved (2,015 → 1,061 ha/yr): it went on through 2019 and collapsed in 2020–21 (GLAD forest-loss alerts).

**No other zone fell like it, and controls don't change that** **[description]**. Giving the "operation" to each of the 14 other zones in turn, Tambopata ranks 1st of 15. Year effects remove shocks shared by all zones (gold price, COVID); adding gold-price sensitivity, zone trends or size scaling keeps the gap at −1,454 to −1,859 ha/yr. A fake 2016 start gives effects 4–9 times smaller.

**Rule-based twins abroad agree, imperfectly** **[description]**. We screened 1,174 Amazon areas on four rules: mining before 2019, no reported operation, distance, terrain. None passed all four; almost every large mining area had an operation. Allowing operations after 2021 leaves three twins (all Brazil). In 2019–21, Tambopata added mining at 38% of the median twin's pace, below all three (p ≈ 0.01–0.02), though it had grown faster than them before 2019. Per 1-km cell, with errors clustered by 10-km block, La Pampa's fall is −1.02 ha per cell-year (p = 0.06).

**Therefore** **[causal]**, *if the comparison areas show what Tambopata would otherwise have done*, Mercurio cut new mining in its target by roughly 1,450–1,860 ha/yr in 2019–21. With one targeted zone, chance (about 1 in 15), local shocks and the extra buffer zone's own enforcement remain possible.

**The effect did not last** **[description]**. In 2022–25 Tambopata averaged 1,829 ha/yr; its gap to the other zones is near zero (−599 to +161).

**Mining crossed the road into the legal corridor; the region did not fall** **[description]**. Directly across the highway from La Pampa, first-time mining rose from 69 to 463 ha/yr; the corridor's share of Madre de Dios' new mining rose from 49% to 72% (MAAP #208: 74%), while the total kept growing (3,610 → 12,049 ha/yr). La Pampa had not run out: 21% of its gold-bearing land was mined by 2018. In 2023 most of its new mining was on old pits.

**Miners now enter the reserve** **[description]**: +241 ha inside it in 2025. MAAP reports ~500 ha from late 2025 to Feb 2026, after river posts were withdrawn (Pacsi et al., 2026). **Brazil, same method, no clear effect** **[description]**: big territories fell after 2022–24, but a staggered DiD across 24 territories finds no significant effect of each territory's own operation (p = 0.38); Munduruku fell before its operation, and national gold rules changed in 2023. **Declared gold collapsed** **[description]**: Madre de Dios' declared output broke −1.16 log points below trend after 2019 (p < 0.01) while mapped mining grew.

## 4. What FZS can do with this

**(a) What FZS learns** **[prediction]**. Expect a sharp local fall while patrols are present, a move across the nearest legal boundary, a return to old pits within about three years, and no fall in the region. **Fund enforcement as a permanent presence, not a one-off sweep.** Patrol the legal side of the boundary, watch old pits, and staff river posts (the 2025 incursion followed a withdrawal). **Make the corridor a filter:** with a 0% royalty and only 145 of 9,592 registered miners fully formal (2021), gold-origin tracing there would remove the cheapest escape.

**(b) Why this could mislead.** *Omitted variables:* COVID, the gold price and later waves (2021, 2023) overlap the post-period; year effects remove shared shocks, not zone-specific ones. *Reverse causation:* La Pampa was targeted because it was the worst, so a drop could be a return to normal; but 2019–21 fell below every earlier year. *Selection of units:* one targeted zone makes standard errors meaningless, so we rank against fake targets; no untouched twin exists, and the best one sat in Brazil's weak-enforcement years; Amarakaeri may have received miners, inflating the gap. *Measurement:* the satellite class mixes legal and illegal mining, counts re-mining as new, and **cannot see river dredges or mercury**. MAAP counted 148 → 598 dredges in La Pampa, 2021–23 (Yupanqui et al., 2023), so mining may have moved onto rivers.

**(c) What would let us say more.** Dated patrol and interdiction records per zone from SERNANP or FZS (enforcement intensity instead of a 0/1 flag); concession and REINFO maps to grade legality pixel by pixel; more operations as cases (Plan Restauración 2021 covered several zones); river-dredge counts and mercury sampling.

## References

- Conley, T. G., & Taber, C. R. (2011). Inference with "difference in differences" with a small number of policy changes. *Review of Economics and Statistics*, 93(1), 113–125. https://doi.org/10.1162/REST_a_00049
- Finer, M., & Mamani, N. (2020). Illegal gold mining down 78% in Peruvian Amazon, but still threatens key areas. MAAP #130. https://www.maapprogram.org/gold-mining-peru/
- Finer, M., & Mamani, N. (2024). Gold mining in the southern Peruvian Amazon, summary 2021–2024. MAAP #208. https://www.maapprogram.org/maap-208-gold-mining-in-the-southern-peruvian-amazon-summary-2021-2024/
- Dethier, E. N., Silman, M. R., Fernandez, L. E., Caballero Espejo, J., Alqahtani, S., Pauca, P., & Lutz, D. A. (2023). Operation Mercury: Impacts of national-level armed forces intervention and anticorruption strategy on artisanal gold mining and water quality in the Peruvian Amazon. *Conservation Letters*, 16, e12978. https://doi.org/10.1111/conl.12978
- Earth Genome (2026). Amazon Mining Watch, mining detections, model 48px_v4.10b (updated 3 Oct 2026). https://source.coop/earthgenome/amazon-mining-watch
- Frankfurt Zoological Society (n.d.). Bahuaja-Sonene and Tambopata. https://fzs.org/en/programs/peru/bahuaja-sonene-and-tambopata/
- MapBiomas Peru (2025). Collection 4 of annual land cover maps of Peru (buffer-zone and protected-area statistics). https://peru.mapbiomas.org
- INGEMMET (2026). GEOCATMIN, Mapa geológico integrado 1:100,000 (map service, layer 6). https://geocatmin.ingemmet.gob.pe
- MapBiomas Amazonía (2024). Colección 6.0 de mapas anuales de cobertura y uso del suelo en la Amazonía, 1985–2023. https://amazonia.mapbiomas.org
- MapBiomas Brasil (2025). Collection 11 (mining) and Collection 10.1 (indigenous-territory statistics). https://brasil.mapbiomas.org
- MINAM (2021). Plan Restauración (Anexo, D.S. N° 017-2021-MINAM). Ministerio del Ambiente, Lima.
- Nunes, F. S. M., et al. (2024). Lessons from the historical dynamics of environmental law enforcement in the Brazilian Amazon. *Scientific Reports*, 14. https://doi.org/10.1038/s41598-024-52180-7
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


---
*Built 2026-10-12 16:40 from git commit 4dc9bf2 (working tree may contain uncommitted changes). Numbers from output/numbers.csv (952 rows).*
