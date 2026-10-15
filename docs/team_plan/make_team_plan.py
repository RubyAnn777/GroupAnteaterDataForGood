"""Fill templates/TEAM_PLAN.docx (left unchanged) -> docs/team_plan/TEAM_PLAN_GroupAnteater_Q2.docx.
Run: uv run --with python-docx python docs/team_plan/make_team_plan.py   (plan v2, 2026-10-12)"""
from pathlib import Path
import docx

ROOT = Path(__file__).resolve().parents[2]
ANS = {
    2: ("Group and members: ", "Group Giant Anteater. Ruby Ann Grambauer, Sebastian Schmid, Member 3, Member 4, Member 5 (replace placeholders)."),
    3: ("Question: ", "Question 2, Peru (Operation Mercurio, from 19 Feb 2019). Brazil (Yanomami, Feb 2023) as an appendix case."),
    4: ("1. Our question. ", "Did Operation Mercurio reduce new mining in La Pampa during (2019-21) and after (2022-25) the operation, "
        "and did mining move across the Interoceanic Highway into the legal mining corridor?"),
    5: ("2. Unit and years. ", "Main panel: 1-km cell x year, Madre de Dios study window (14,241 cells), 2010-2025. Zone-level panel: "
        "15 Peruvian buffer zones x year, 2011-2025. Outcome: land mapped as mining for the first time (ha), MapBiomas Peru "
        "Collection 4 rasters; secondary: returns to old pits; net addition (course measure)."),
    6: ("3. Comparison. ", "Treatment: La Pampa sector = Tambopata buffer zone (SERNANP) between 70.15 and 69.80 W; post = 2019-21, "
        "after = 2022-25. Border robustness: narrow (70.10-69.85 W), wide (70.20-69.75 W), whole buffer zone. Comparison groups: "
        "(i) 14 Peruvian buffer zones with mining before 2019; (ii) cells outside the named zones; (iii) two rule-based twins "
        "abroad (mining before 2019, no operation 2017-21, lowland, similar size); (iv) Amarakaeri buffer zone as 'less treated' "
        "(Mercurio II from Dec 2019). Models: y_zt = a_z + g_t + b D_zt + e (zone and year fixed effects); event study with "
        "year leads/lags, 2014-18 pooled reference; cell DiD y_ct = a_c + g_t + sum b_zp + gold-bearing x year effects, comparison cells outside the corridor, errors "
        "clustered by 10-km block plus wild cluster bootstrap; randomization inference over fake places and fake start dates (one treated zone). Displacement: corridor "
        "within 10 km north of the highway; 1-km road bands -30..+30 km; mean depth (trend break, Newey-West)."),
    7: ("4. Sources. ", "Pack: peru_bufferzone_year, peru_department_year, prices. Added: MapBiomas Peru Col 4 rasters; SERNANP "
        "boundaries; INGEMMET corridor, geology and cadastre; RAISG roads; MapBiomas Amazonia communities; UMD GLAD alerts; Amazon "
        "Mining Watch (incl. MAAP #235 legality layer); MINEM gold production; MEF PP 0128 spending; MapBiomas Brazil Col 11 rasters."),
    8: ("5. Initial statistics. ", "Our raster count: Tambopata buffer zone 2025 = 20,716 ha; publisher table 20,730 ha. Reserve: 776 vs "
        "777 ha (platform). Brazil Col 11 raster: Kayapo 2024 = 17,628 vs 17,632 ha (platform)."),
    9: ("6. Main concern. ", "One treated zone and overlapping events (COVID 2020, Plan Restauracion 2021, emergency 2023); the "
        "comparison cells include the corridor that received miners; pre-trends at cell level fail for La Pampa; satellites miss "
        "dredges and mercury; the official gold series changed definition in 2015 and 2020."),
    10: ("7. Who does what. ", "Team A, description (Ruby, Member 3): zones, displacement layers, old pits, timing, legality, "
         "qualitative background. Team B, causal attempts (Sebastian, Member 4): DiD and event studies, cell panel, twins, "
         "synthetic control, Brazil. Team C, brief, slides and replication (Member 5, with Ruby): figure, references, data log, "
         "replication zip. All: review of each other's section before Lesson 5."),
}


def main():
    d = docx.Document(ROOT / "templates" / "TEAM_PLAN.docx")
    for i, (label, text) in ANS.items():
        p = d.paragraphs[i]
        for r in list(p.runs):
            r._element.getparent().remove(r._element)
        p.add_run(label).bold = True
        p.add_run(text)
    out = ROOT / "docs" / "team_plan" / "TEAM_PLAN_GroupAnteater_Q2.docx"
    d.save(out)
    print("saved", out.relative_to(ROOT), sum(len(t.split()) for _, t in ANS.values()), "words")

if __name__ == "__main__":
    main()
