# Presentation storyline (10 min + 5 min Q&A, FZS / Christof Schenck)

Draft 2026-10-13. Every number on a slide comes from `output/numbers.csv` (ids in brackets) or from
`code/slides_figures.py`. Labels: [D] description, [P] prediction, [C] causal (conditional only).

## What changed from the team's draft, and why

| Team draft | Change | Why |
|---|---|---|
| Research question at step 3, after a long map context | Question + one-line answer on slide 2, before the map | Front-load the "so what" for an executive; the map then *shows* the answer |
| Context map (2a) and displacement (4a) as separate blocks | The animated map **is** the first descriptive result; 4a keeps two charts | 10 minutes ≈ 11 slides; no story told twice |
| Mining layer "differentiated by legality" | Legality shown by **zone** (legal corridor vs buffer zone/reserve), not by pixel | MapBiomas can't tell legal from illegal (rule 5); the law makes legality a matter of location (D.L. 1100/1105) |
| Mercurio layer "where it took place" | La Pampa sector highlighted (our boundary) + "Mercurio II: all of Madre de Dios, 2019" as text | No official polygon of the operation exists |
| 4b.iii "interviews + yellowness" | Pond yellowness from **Dethier et al. (2023)** as a cited quote; interviews: **no source in the repo**, so dropped unless the team gives one | AI is not a source; cite only what we opened |
| 4c "correlation analysis budget vs mining" | Not a slide. Already computed: r = −0.31 (`ctx_dose_corr`, 11 years), and money follows mining (bad control). One spoken sentence, details in backup | n = 11 and reverse causation; a scatter would invite a causal reading |
| 4d "miners returned to old pits" | "**Mining** returned to old pits" | Hectares, not people; we can't show the same people |
| 5a "Mercurio **caused** the fall, −1,454 to −1,859" | "*If* the comparison zones show what Tambopata would otherwise have done, Mercurio and the operations that followed lowered **net** new mining by ≈ 411–1,859 ha/yr in 2019–21. In hectares only; coincides with COVID." | The one allowed claim (agent.md, D26). The range starts at the synthetic control (−411), not M1 |
| 5c "Brazil control shows parallel trends & supports our claim" | **Reversed.** The twins (Amanã, Tapajós) **fail** the pre-trend test (p < 0.001; Tambopata grew faster before 2019). Brazil's own staggered DiD has the wrong sign (+0.26, p = 0.44). Brazil goes to one honest line + backup | Saying "parallel trends hold" would be false and costs the 30% honesty block |
| Recommendations: 5 points incl. "mercury blast radius → expand buffer zones" | 3 recommendations. Mercury becomes the "what satellites can't see" ask (fund river/mercury monitoring), labelled as from the literature | We have no mercury data; a recommendation must rest on our findings or on cited sources |
| Missing | **New slide: inside the reserve** (+241 ha in 2025, after the navy left the river posts) | FZS's core area and the most actionable finding |

## Slide plan (≈ 10 min)

| # | Time | Slide (headline = the takeaway) | Visual | Label |
|---|---|---|---|---|
| 1 | 0:30 | Title + two giant-anteater facts | Photo placeholder | — |
| 2 | 0:40 | **FZS pays for operations. What happens when one ends?** Answer up front: fell where enforcement landed, while it lasted; moved across the road; came back | 3 icons: fell · moved · returned | — |
| 3 | 1:00 | **La Pampa: Peru's largest illegal mining area, one road from legal land** (map build: zones → highway → rivers → legal corridor → La Pampa target) | Map, 5 layers (animation part A) | D |
| 4 | 1:15 | **2010–2025 in one minute** | Animated map + moving timeline (part B) | D |
| 5 | 0:45 | **Net new mining in Tambopata fell 90% in 2019–21, then came back** (1,640 → 163 → 1,829 ha/yr) | `slide_01_tambopata_net.png` | D |
| 6 | 0:45 | **The region didn't fall: new mining grew in the legal corridor** (MdD 5,317 → 6,571 → 11,373 ha/yr first-time) | `slide_02_zones.png` | D |
| 7 | 0:50 | **New mining jumped across the highway** (north share 23% → 65%; crossed before in 2008) + Dethier yellowness quote | `slide_03_road_share.png` | D |
| 8 | 0:50 | **Why it came back: money faded, gold kept rising, gold was left** (PP 0128 peak 2019; gold ×2.7; 21% mined by 2018) | `slide_04_context.png` | D |
| 9 | 0:40 | **In 2023 most new mining in La Pampa was on old pits** | `slide_05_old_pits.png` | D |
| 10 | 0:40 | **2025: mining inside the reserve jumped, after the navy left the river** | `slide_06_reserve.png` | D |
| 11 | 1:00 | **Did Mercurio cause the fall? Only conditionally, and only in hectares** | `slide_07_causal.png` + six-attempt strip | C (conditional) |
| 12 | 0:30 | **What satellites can't see, and which way our biases push** | text: dredges 148 → 598 (MAAP #193), mercury | D |
| 13 | 0:45 | **For FZS: plan for the months after the operation** — 3 recommendations | icons + risk-map thumbnail | P |
| — | | Backup: six attempts table · Brazil (twins fail pre-trends; Yanomami) · budget correlation · legality grades · risk map | | |

## Recommendations (slide 13, [P])

1. **Stay after the sweep.** The local fall lasted about two years; the reserve incursion followed a withdrawal. Fund presence, not one-off operations.
2. **Hold the reserve's first kilometre and the river.** 91% of first-time mining inside the reserve lies within 1 km of its edge (`rd_reserve_inside_share_1km`); staff the Malinowski posts.
3. **Watch the legal side and old pits.** Expect a response across the nearest legal boundary within a year; monitor old pits, not only forest edges; push for gold traceability in the corridor (Brazil 2023 as a model).

## Open for the team

- ~~Interviews (4b.iii)~~ Decided 2026-10-13: no citable source, dropped.
- ~~Brazil~~ Decided 2026-10-13: backup slides only.
- Photos: anteater (title), La Pampa aerial (slide 3), rangers (slide 13): licence-free sources needed.
