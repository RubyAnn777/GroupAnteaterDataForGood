# Presentation storyline v3 (10 min + 5 min Q&A, FZS / Christof Schenck)

Rewritten 2026-10-15 for plan v3 (`docs/PLAN_v3.md`). Supersedes the 2026-10-13 draft (in git history).
Every number comes from `output/numbers.csv` (ids in brackets). Labels: [D] description, [P] prediction,
[C] causal (one conditional sentence only).

## Rules for every slide

1. **One measure: net mining additions** (ha/yr) = new land + re-mined − stopped, MapBiomas Peru Collection 4 rasters.
   Where we show the parts, the colours are fixed: new land brown, re-mined amber, stopped teal (below zero), net black.
2. **Every chart says what it measures:** measure, unit, zone, period in the subtitle or axis. No bare "mining".
3. **Same zones everywhere:** Tambopata buffer zone (official, whole, incl. Kotsimba), La Pampa sector (its
   70.15–69.80 W part), corridor across the road (D.L. 1100, ≤ 10 km north of the highway), Amarakaeri buffer zone
   (whole, "less treated"), Madre de Dios (department).
4. **Same periods everywhere:** 2016–18 (before), 2019–21 ("Mercurio and what followed"), 2022–25 ("later years",
   never "after the operation ended"; with and without 2023).
5. Hectares are a proxy for mining activity, not for miners.

## The story in one line

Mining fell where the patrols were, while they were there, but **half the fall was pits going out of use, not
fewer new pits**; new mining opened across the road and in the corridor, and the target came back on old pits.

## Slide plan (≈ 10 min, 14 main slides)

| # | Time | Headline (= the takeaway) | Visual | Label | Key ids |
|---|---|---|---|---|---|
| 1 | 0:30 | Title + two giant-anteater facts | photo | — | — |
| 2 | 0:40 | **FZS pays for operations. What happens when one ends?** Answer up front: it fell locally (half of it pits stopping), moved across the road, came back on old pits | 3 icons | — | — |
| 3 | 0:40 | **One measure on every slide: net mining additions = new land + re-mined − stopped** | definition diagram (pixel states → three flows) + zone map | D | — |
| 4 | 0:50 | **La Pampa sits one road away from legal mining land** (map build: zones → highway → corridor → La Pampa) | animation part A (map layers) | D | — |
| 5 | 1:00 | **2010–2025 in one minute: new pits, old pits re-mined, pits stopping** | animation part B: pixels by flow (new brown, re-mined amber, stopped teal) + net counter per year | D | `lapampa_*_{net,new,remined,stopped}` |
| 6 | 0:40 | **Net additions in the Tambopata buffer zone fell 90% in 2019–21** (1,639 → 162 ha/yr) while Amarakaeri rose (289 → 573) | slide_01: net, two zones | D | `tambopata_bz_{pre,during}_net`, `amarakaeri_bz_*_net`, `did_main_net` |
| 7 | 0:50 | **A quarter to a half of the fall was pits going out of use; the rest, fewer new pits** (new land 2,015 → 1,061; stopped 720 → 1,412; Amarakaeri's stopped flat) | slide_02: parts, small multiples Tambopata BZ vs Amarakaeri | D | `tambopata_bz_fall_share_*`, `*_stopped`, `did_main_{new,remined,stopped}` |
| 8 | 0:40 | **New pits kept opening in 2019; pits stopped where the patrols were** (La Pampa 2019: new 1,532 vs 1,834 in 2018; stopped 1,494) → why a monitoring ring matters | slide_03: La Pampa yearly parts 2016–2022 | D | `lapampa_2018_new`, `lapampa_2019_{new,stopped,net}` |
| 9 | 0:50 | **Mining moved across the road and into the corridor; the department never fell** (across the road 60 → 395; Madre de Dios 3,607 → 4,636 → 12,039) | slide_04: across-the-road parts + department by area | D | `corridor_across_*_net`, `mdd_*_net`, `v2_corridor_share_*_net`, `mdd_rise_elsewhere_vs_tambopata_fall` |
| 10 | 0:40 | **It came back on old pits** (later years 1,828 ha/yr, 1,250 without 2023; re-mined 1,139) | slide_05: later-years parts | D | `tambopata_bz_later_*`, `tambopata_bz_later_ex2023_net` |
| 11 | 0:30 | **2025: mining inside the reserve jumped, after the navy left the river posts** (+241 ha) | slide_06 reserve | D | `tambopata_nr_2025_net` |
| 12 | 1:00 | **Did Mercurio cause the fall? Only conditionally, and half of it is pits stopping** | slide_07: estimates with parts (2×2, M1, SDID) + ranks raw vs scaled | C (conditional) | `model_m1_during_*`, `did_base2014_*`, `model_m1_rank_scaled`, `model_m4_rank` |
| 13 | 0:30 | **What satellites cannot see, and which way our biases push** | text: dredges 148 → 598 (MAAP #193), mercury; flicker share | D | `tambopata_bz_during_stopped_share_back_within_2y` |
| 14 | 0:50 | **For FZS: stay after the sweep and watch the ring around it** — 3 recommendations | icons | P | — |
| — | | Backup: six attempts table · stopped split (water / forest / back within 2 yrs) · cell panel & RD on net · twins (AMW, other measure: 16–41% of twins' pace) · Brazil (net, card-12 wording) · money and gold (context) · definitions and data table | | | |

## Recommendations (slide 14, [P], from this one case)

1. **Stay after the sweep.** Net additions stayed low only in 2019–21; the reserve incursion of 2025 followed a
   withdrawal. Fund presence, not one-off operations.
2. **Watch the ring around the enforcement zone, in near real time.** In 2019 new pits kept opening in La Pampa
   while patrolled pits stopped, and new mining rose across the road and in the corridor. A forest-loss alert
   system (GLAD/MAAP-type) on a ring of a few km around each operation catches the next pit before it is dug out.
3. **Hold the reserve's first kilometre and the river.** 91% of first-time mining inside the reserve lies within
   1 km of its edge (`rd_reserve_inside_share_1km`); staff the Malinowski posts; push gold traceability in the
   corridor.

## What changed from the 2026-10-13 storyline, and why

| Before | Now | Why |
|---|---|---|
| Mixed measures: net for the zone, first-time for the map and the brief figure | Net everywhere, parts where shown | Team decision 2026-10-15 (PLAN_v3 V3-1, V3-4) |
| "Nothing fell in 2019" | "New clearing did not fall in 2019; land going out of use did" | Net additions fall in 2019 because 1,494 ha stopped |
| Causal range 411–1,859 ha/yr | 1,452–1,662 ha/yr, half of it stopping, upper bound | Review D-S14-3; v3 parts |
| "Rank 1 of 15" as evidence | Raw rank 1 also in 2014–16 (size); scaled 3–6 of 7 | Review X1 |
| Twins 40% of pace | 16–41% (with / without Munduruku), AMW measure, backup only | One dating rule (R*) admits Munduruku |
| Brazil "wrong sign" | Card 12 wording: boom, then fall; operations at the peak; cannot separate | Review D-S14-8 |
