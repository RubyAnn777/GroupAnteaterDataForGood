"""Fill templates/TEAM_PLAN.docx (left unchanged) -> docs/team_plan/TEAM_PLAN_GroupAnteater_Q2.docx.
Run: uv run --with python-docx python docs/team_plan/make_team_plan.py   (plan v2, 2026-10-12)"""
from pathlib import Path
import docx

ROOT = Path(__file__).resolve().parents[2]
ANS = {
    2: ("Group and members: ", "Group Giant Anteater. Ruby Ann Grambauer, Sebastian Schmid, [add members]."),
    3: ("Question: ", "Question 2, Peru (Operation Mercurio, from February 2019). Brazil (Yanomami operation, February 2023) as a short second case."),
    4: ("1. Our question. ", "When Operation Mercurio hit La Pampa (Tambopata buffer zone), did illegal gold mining stop there, for how long, "
        "and did it cross the Interoceanic Highway into the legal mining corridor?"),
    5: ("2. Unit and years. ", "One row is one zone in one year, Madre de Dios, 2010-2025: La Pampa sector, rest of the Tambopata buffer zone, "
        "the legal corridor across the road, rest of the corridor, native communities, other buffer zones, Tambopata reserve. "
        "Outcome: land mapped as mining for the first time, and returns to old pits (ha)."),
    6: ("3. Comparison. ", "We compare the Tambopata buffer zone (and its La Pampa sector) to 14 other Peruvian buffer zones with mining before "
        "2019, before (2016-18), during (2019-21) and after (2022-25) Mercurio; plus a rule-based twin abroad (Amana National Forest, Brazil). "
        "For displacement we compare the south and north sides of the highway. We chose these groups because they mined before 2019 and "
        "share national shocks (gold price, COVID); nearby zones may have received miners, so we also use distant ones."),
    7: ("4. Sources. ", "From the data pack: peru_bufferzone_year, peru_department_year, prices. Added: MapBiomas Peru Collection 4 rasters "
        "and protected-area statistics (peru.mapbiomas.org); SERNANP boundaries; INGEMMET mining corridor and geology (GEOCATMIN); "
        "RAISG roads; UMD GLAD forest-loss alerts; Amazon Mining Watch; MAAP reports #130, #193, #208, #241."),
    8: ("5. Initial statistics. ", "Our raster count shows 20,716 ha of mining in the Tambopata buffer zone in 2025; the publisher's table shows "
        "20,730 ha. Tambopata National Reserve: 776 ha vs 777 ha on the MapBiomas platform."),
    9: ("6. Main concern. ", "There is one targeted zone, and other events overlap (COVID 2020, Plan Restauracion 2021, the 2023 emergency, the gold "
        "price). Satellites miss river dredges and mercury; net numbers hide miners returning to old pits; clearing in La Pampa continued "
        "through 2019. Nearby zones may have received miners or had their own enforcement."),
    10: ("7. Who does what (to confirm). ", "Data and data log: Sebastian. Analysis: Sebastian, reviewed by Ruby. Figure: [add]. "
         "Brief and slides: Ruby, [add]. Replication files: Sebastian."),
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
