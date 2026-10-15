# Presentation storyline v3.1 (10 min + 5 min Q&A, FZS / Christof Schenck)

2026-10-15, second pass. The team asked to go back to the story of the 2026-10-13 deck (it flowed better and was
simpler; reference copy: `archive/old_deck_2026-10-13.pdf`) while keeping plan v3 (`docs/PLAN_v3.md`): one measure
(net mining additions = new land + re-mined − stopped), one zone set, one treatment. Every number from
`output/numbers.csv`. Labels: [D] description, [P] prediction, [C] causal (one conditional slide only).

## Rules

1. Titles: punchy, the takeaway, ≤ 10 words, plain words (smart brevity). No method names in main-slide titles.
2. One measure: net mining additions (ha/yr). Parts only where the slide is about parts (fixed colours: new land
   brown, re-mined amber, stopped teal below zero, net black). Subtitle = measure · unit · zone · period.
3. **Zones in the main flow:** the Tambopata buffer zone for every time series (fell, 2019 zoom, came back, cause);
   La Pampa only on the map and on "across the road". Never switch zone between two neighbouring chart slides.
4. Lean charts: years 2014–2025 (2016–2022 for the 2019 zoom), on-chart labels only for Mercurio and the 2023
   emergency (other events in the notes), one callout per chart, no in-chart number labels except that callout.
5. No causal wording outside the claim slide: no "patrols", "because", "after the navy left" in titles.
6. 2022–25 = "later years", always with "without 2023" where a number depends on 2023.

## Slide plan (21 main + backup)

| # | Title (takeaway) | Visual | Label | Key ids |
|---|---|---|---|---|
| 1 | Cover: "A pause, not an end: mining after Operation Mercurio" (old cover layout; La Pampa 2019 aerial, CC BY-SA; FZS logo on every slide) | photo + 3 stat tiles (Feb 2019 · 30 m · 6 tests) | — | — |
| 2 | Anteaters eat 35,000 ants a day, and never destroy a nest (old slide 2) | photo + 2 facts | — | — |
| 3 | FZS pays for operations. What happens when one ends? (three findings: fell 1,640 → 163 · moved 60 → 395 · came back 1,829) | dark, 3 icons (current v3 slide 2) | D | `tambopata_bz_*_net`, `corridor_across_*_net` |
| 4–7 | La Pampa sits one road away from legal mining land (4 click-through map steps) | map stills | D | — |
| 8 | 2010–2025 in one minute (timeline animation: new / re-mined / stopped pixels) | video | D | — |
| 9 | Net mining fell 90%, then came back | Tambopata BZ net additions 2014–25, period bars | D | `tambopata_bz_{pre,during,later}_net` |
| 10 | In 2019, new pits kept opening while old ones went quiet | user's chart 1 style: parts, Tambopata BZ, 2016–22; callout 2019 | D | `tambopata_bz_2018_new`, `tambopata_bz_2019_{new,stopped,net}`, `tambopata_bz_stopped_share_of_fall_{min,max}` |
| 11 | The region kept growing, mostly in the legal corridor | Madre de Dios net additions by area, period means | D | `mdd_*_net`, `v2_corridor_share_*_net` |
| 12 | Across the road, mining rose six-fold | corridor across the road vs La Pampa, net, 2014–25 | D | `corridor_across_*_net`, `lapampa_*_net` |
| 12b | 2019–21: mining fell south of the highway, rose north (1-km road bands, three periods) | road bands | D | `sl_band_{south,north}_*_net` |
| 13 | Money faded after 2019, while gold rose 2.7-fold | old slide 15 (spending · gold · Tambopata BZ net) | D | `sl_pp0128_*`, `gold_price_ratio_2025_2018` |
| 14 | It came back, partly on old pits (33–46%) | user's chart 2 style: parts, Tambopata BZ, 2014–25, lean | D | `tambopata_bz_later_{net,new,remined}`, `*_later_ex2023_*` |
| 15 | In 2025, mining inside the reserve jumped 241 ha | old slide 17 | D | `tambopata_nr_2025_net` |
| 16 | Six methods: two hold up, none is clean | old slide 18 grid (green = agrees in hectares) | C · conditional | `model_m1_during_net`, `sdid_sdid_ha_during_net`, … |
| 17 | What we can say about cause | old slide 19 (dark): conditional sentence, 1,453–1,663 ha/yr; tiles: "Hectares only" · "A quarter to a half is pits stopping" · "COVID overlaps" | C · conditional | `model_m1_during_net`, `did_base2014_net`, stopped-share ids |
| 18 | In hectares the fall stands out. For its size, it doesn't | old slide 20 (raw vs scaled placebo dots) | C · conditional | `placebo_space_rank_*`, `model_m4_rank` |
| 19 | Most biases make the fall look bigger | old slide 21 | D | — |
| 20 | Plan for the months after the operation ends | old slide 22 + ring monitoring: Stay after the sweep · Watch the ring around it · Guard the reserve's edge and river | P | `rd_reserve_inside_share_1km`, `corridor_across_*_net` |
| 21 | Thank you / Questions | photo | — | — |
| B | Backup: six methods in detail · estimates (one causal range only) · placebo explainer · stopped split · timing · cell panel & RD · legality · declared gold · money · risk map · twins (AMW, 16–41%) · Brazil (card-12 wording) · map video · definitions | | | |

## Recommendations (slide 20, [P], from this one case)

1. **Stay after the sweep.** Net additions stayed low only in 2019–21.
2. **Watch the ring around the operation.** In 2019 new pits kept opening while old ones went quiet, and mining rose
   across the road: near-real-time forest-loss alerts on a ring of a few km around each operation.
3. **Guard the reserve's edge and the river.** 91% of first-time mining inside the reserve lies within 1 km of its edge.
