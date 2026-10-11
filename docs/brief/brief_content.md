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

**Our case:** Operation Mercurio, from February 2019 at La Pampa, Peru's largest illegal mining area, in the buffer zone of Tambopata National Reserve (Madre de Dios). **Targeted:** Tambopata buffer zone. **Comparison:** Amarakaeri buffer zone, plus 13 other Peruvian buffer zones with mining. **Also tracked:** the reserve itself and the rest of Madre de Dios, 2014–2025. Brazil's Yanomami operation (2023) is a shorter second case.

## 2. Data and provenance

**Outcome:** new mining area per year (ha), MapBiomas Peru Collection 4, class "mining". Buffer zones (course data), check: Tambopata buffer zone 2025 = 20,730 ha, as on the MapBiomas platform. Protected areas (our download), check: Tambopata National Reserve 2025 = {{anp_level_tam_nr_2025:,.1f}} ha vs 777 ha on the platform. **Context:** World Bank gold price (check: Aug 2026 = $4,411/oz); Madre de Dios declared gold production, Central Reserve Bank of Peru (monthly values sum to annual); MapBiomas Brazil Collection 11 (all indigenous lands 2025 = 39,915 ha). Every file is in `DOWNLOAD_LOG.csv`; one script, `code/main.py`, produces every number and the figure.

## 3. Findings

![New mining area per year: Tambopata vs Amarakaeri buffer zones and inside Tambopata National Reserve (top); all of Madre de Dios (bottom)](output/fig_brief_main.png)

**During the operation, new mining in the target collapsed** [[D]]. Tambopata fell from {{mean_add_tambopata_2016_18}} to {{mean_add_tambopata_2019_21}} ha/yr (2016–18 vs 2019–21), while Amarakaeri rose from {{mean_add_amarakaeri_2016_18}} to {{mean_add_amarakaeri_2019_21}}: a gap in changes of **{{did_main}} ha/yr**. Every year of 2019–21 was below every year of 2011–18.

**No other zone fell like it, and controls don't change that** [[D]]. Giving the "operation" to each of the 14 other zones in turn, Tambopata ranks 1st of 15. Year effects remove shocks shared by all zones (gold price, COVID); adding gold-price sensitivity, zone trends or size scaling keeps the gap at {{model_m1_during}} to {{model_m3_during}} ha/yr. A fake 2016 start gives effects 4–9 times smaller.

**Therefore** [[C]], *if the other zones show what Tambopata would otherwise have done*, Mercurio cut new mining in its target by roughly 1,450–1,860 ha/yr in 2019–21. With one targeted zone, chance (about 1 in 15) and local shocks remain possible.

**The effect did not last** [[D]]. In 2022–25 Tambopata averaged {{mean_add_tambopata_2022_25}} ha/yr; its gap to the other zones is near zero ({{model_m3_after}} to +{{model_m1_after}}).

**The region did not fall** [[D]]. All of Madre de Dios went {{mean_add_mdd_total_2016_18}} → {{mean_add_mdd_total_2019_21}} → {{mean_add_mdd_total_2022_25}} ha/yr. We do not call this displacement: Amazon Mining Watch shows the legal corridor falling, and gold rose {{gold_price_ratio_2025_2018:.1f}}-fold.

**Miners now enter the reserve** [[D]]: +{{anp_tam_nr_addition_2025}} ha inside it in 2025. MAAP reports ~500 ha from late 2025 to Feb 2026, after river posts were withdrawn (Pacsi et al., 2026). **Brazil is inconclusive** [[D]]: Yanomami fell ({{br_ti_yanomami_add_2022}} → {{br_ti_yanomami_add_2024}} ha, 2022–24), but so did Kayapó and Munduruku.

## 4. What FZS can do with this

**(a) What FZS learns** [[P]]. Expect a sharp local fall while patrols are present, a return within about three years after they thin out, and no fall in the region. **Fund enforcement as a permanent presence, not a one-off sweep.** Staff the edges of the core area (the 2025 incursion followed a post withdrawal) and watch the next-nearest unprotected land.

**(b) Why this could mislead.** *Omitted variables:* COVID, the gold price and later waves (2021, 2023) overlap the post-period; year effects remove shared shocks, not zone-specific ones. *Reverse causation:* La Pampa was targeted because it was the worst, so a drop could be a return to normal; but 2019–21 fell below every earlier year. *Selection of units:* one targeted zone makes standard errors meaningless, so we rank against fake targets; Amarakaeri may have received miners, inflating the gap. *Measurement:* the satellite class mixes legal and illegal mining, counts re-mining as new, and **cannot see river dredges or mercury**. MAAP counted 148 → 598 dredges in La Pampa, 2021–23 (Yupanqui et al., 2023), so mining may have moved onto rivers.

**(c) What would let us say more.** Dated patrol and interdiction records per zone from SERNANP or FZS (enforcement intensity instead of a 0/1 flag); more operations as cases (Plan Restauración 2021 covered several zones); river-dredge counts and mercury sampling.

## References

- Conley, T. G., & Taber, C. R. (2011). Inference with "difference in differences" with a small number of policy changes. *Review of Economics and Statistics*, 93(1), 113–125. https://doi.org/10.1162/REST_a_00049
- Finer, M., & Mamani, N. (2020). Illegal gold mining down 78% in Peruvian Amazon, but still threatens key areas. MAAP #130. https://www.maapprogram.org/gold-mining-peru/
- Finer, M., & Mamani, N. (2024). Gold mining in the southern Peruvian Amazon, summary 2021–2024. MAAP #208. https://www.maapprogram.org/maap-208-gold-mining-in-the-southern-peruvian-amazon-summary-2021-2024/
- Frankfurt Zoological Society (n.d.). Bahuaja-Sonene and Tambopata. https://fzs.org/en/programs/peru/bahuaja-sonene-and-tambopata/
- MapBiomas Peru (2025). Collection 4 of annual land cover maps of Peru (buffer-zone and protected-area statistics). https://peru.mapbiomas.org
- MapBiomas Brasil (2025). Collection 11 (mining) and Collection 10.1 (indigenous-territory statistics). https://brasil.mapbiomas.org
- Nunes, F. S. M., et al. (2024). Lessons from the historical dynamics of environmental law enforcement in the Brazilian Amazon. *Scientific Reports*, 14. https://doi.org/10.1038/s41598-024-52180-7
- Pacsi, R., et al. (2026). Rapid expansion of illegal gold mining in Tambopata National Reserve. MAAP #241. https://www.maapprogram.org/mining-peru-tambopata/
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
