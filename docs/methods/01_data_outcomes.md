# S1 · Measurement: stocks, flows, zones and source checks

*Method card 1 of the causal review (plan: `docs/methods/causal_review_plan.md`). Every later method inherits what this card defines. Test script: `code/review/s1_data_checks.py` (read-only; run from the repo root).*

---

## 1. In one sentence

Before any causal method, we have to know exactly what our outcome counts, because the same satellite maps give three different "amounts of mining" that move in different directions in the same year.

## 2. Simple version

Think of a car park photographed from above once a year. The photo shows how many spaces are occupied: that is the **stock**. If we want to know how many cars *arrived* this year, we can do three things:

1. **Net change:** occupied this year minus occupied last year. If 100 cars arrive and 90 leave, the net change is +10. It looks as if almost nothing happened.
2. **First-time arrivals:** count only spaces that have never been occupied in any earlier photo. This ignores cars parking again in a space that was used before.
3. **Re-arrivals:** spaces occupied now, empty last year, but used at some earlier time.

A car that stays parked in the same space every year is in the stock but never shows up in any of the three counts.

For mining the "spaces" are 30-m pixels, a "car" is a pixel classified as mining, and "leaving" means the pixel stops looking like mining (abandoned, regrown, or turned into a pond).

There is one more twist. First-time arrivals can only happen in spaces that have never been used. As the car park fills up, there are fewer fresh spaces left, so first-time arrivals fall even if demand stays the same. That is **depletion**.

## 3. When this matters

- **Always**, when the outcome is built from a stock (land cover, forest, mined area, population).
- **Most of all** when the treatment can change how land *leaves* the stock, not only how it enters. Enforcement does both: miners are removed (pits stop) and new clearing may slow.
- When products disagree (MapBiomas vs AMW vs GLAD), the disagreement is often about which of these flows each product can see.

## 4. Assumptions behind using a flow as "new mining"

| Assumption | In words | What breaks it |
|---|---|---|
| A1 Valid classification | A mining pixel really is mining, and vice versa | Bare soil, sandbars and settlements confused with mining; water-filled pits classified as water |
| A2 Stable classification over time | The error rate does not change by year or by place | Map artefacts in one year (see the 2023 test), the last year being less filtered |
| A3 Measurement error unrelated to treatment | Errors are not systematically different in treated vs comparison places, before vs after | Enforcement turns active pits into abandoned ponds, which the map reads as "stopped" |
| A4 Comparable at-risk pool | Places have similar shares of unmined land left | In 2018 mining covered 18% of the La Pampa sector (9,681 of ~53,600 ha), 7% of the land across the road, 5.6% of the Tambopata BZ, 2.7% of Amarakaeri BZ and under 0.7% of every other buffer zone |
| A5 Fixed units | Zone boundaries do not change and are assigned the same way in every module | Today's corridor and community polygons applied back to 1985; precedence rules |

## 5. The maths

### 5.1 Master's level

Let M_it be the set of mining pixels in zone *i*, year *t*, and S_it = |M_it| × pixel area its **stock**. Define for each pixel *p*:
- first-mined year F_p = min{ t : p ∈ M_t }
- **new land:** N_it = area of { p ∈ M_it : F_p = t }
- **re-mined:** R_it = area of { p ∈ M_it : p ∉ M_i,t−1, F_p < t }
- **stopped:** X_it = area of { p ∈ M_i,t−1 : p ∉ M_it }

Then, exactly,

  **ΔS_it = S_it − S_i,t−1 = N_it + R_it − X_it.**

Our test confirms this identity holds to the hectare for every zone and year (`T0`: max error 0.0).

**Measurement error in the outcome.** If the observed outcome is Y* = Y + u:
- *Classical* error (u independent of everything, mean zero): estimates stay unbiased but get noisier.
- *Non-classical* error (u correlated with treatment): bias. The direction equals the sign of E[u | treated, post] − E[u | other cells].

With net additions, the stopped term X enters with a minus sign. If enforcement increases X (pits abandoned, flooded, reclassified), then the net addition falls even if no less land is newly mined. In potential-outcome terms the estimate is

  τ_net = τ_N + τ_R − τ_X,

and a large τ_X (> 0) is read as "less mining".

### 5.2 PhD level

**First-time mining is an absorbing-state outcome.** Write the at-risk pool U_i,t−1 = A_i − ∪_{s<t} M_is (land never mined). The natural model is a discrete-time hazard

  h_it = N_it / U_i,t−1.

A DiD in levels of N_it assumes that, without treatment, N would move in parallel. But N_it = h_it × U_i,t−1, and U declines faster where mining is denser. So even with a constant hazard, the dense unit's N falls mechanically. Parallel trends in N then fails by construction, and the direction of the bias is toward finding a fall in the dense, treated place. Remedies:
- model the hazard (N / U) instead of N;
- add the lagged cumulative mined share as a control;
- compare units with similar depletion.

**Stock-flow error propagation.** Classification noise ("flicker") of a pixel that is mining in one year only adds to N in that year and to X the next. It also permanently removes the pixel from U. With annual maps, flicker inflates both R and X and leaves ΔS roughly unaffected on average. It does bias N upward in noisy years.

**The modifiable areal unit problem (MAUP).** Results depend on how pixels are grouped. The same pixels give different trends when grouped as "Tambopata buffer zone" (statistics workbook) or as "La Pampa sector + rest of buffer zone" (our raster zones), because the zone rules differ (test T6).

## 6. Our example: the data lineage

### 6.1 Sources

| Data | Publisher, version | File | Used for |
|---|---|---|---|
| Buffer-zone statistics | MapBiomas Peru, Collection 4 (ZONA-AMORTIGUAMIENTO workbook) | `data/peru_bufferzone_year.csv` (built by `how_the_panels_were_built/04_panels.py:98-103`) | A1-A6 (zone designs) |
| Department statistics | MapBiomas Peru, Collection 4 (LIMITES-POLITICOS) | `data/peru_department_year.csv` | displacement totals |
| Protected-area statistics | MapBiomas Peru, Collection 4 (AREAS-PROTEGIDAS) | `data_raw/mapbiomas_peru/...AREAS-PROTEGIDAS.xlsx` | inside the reserve |
| Annual land-cover rasters | MapBiomas Peru, Collection 4 (git-ignored, ~3 GB) | → `data_intermediate/zone_year_v2.csv`, `cell_year_v2.csv.gz`, `zones_v2_mdd_full.tif` | A7-A9 (pixel designs) |
| Mining patches | Amazon Mining Watch, model 48px_v4.10b (git-ignored) | → `data_intermediate/amw_*` | A10, A11, A13 |
| Forest-loss alerts | GLAD-L | → `data_intermediate/glad_zone_quarter_v2.csv` | timing check |
| Gold production | BCRP (source MINEM); MINEM yearly files | `data_raw/bcrp/`, `data_raw/minem_produccion/` | context |

### 6.2 The three outcome variables

| Variable | Definition as coded | Built where | Used by |
|---|---|---|---|
| **Net addition** | stock(t) − stock(t−1), summed over all department rows of a buffer zone first | `peru.py:33-58`, `peru_models.py:46-48` | 2×2, event study, ladder, SC, SDID |
| **First-time mining** | pixel is class 30 in t and in no earlier year since 1985 | `raster_zones.py:186-208` | cell panel, RD, brief figure, map animation |
| **AMW new area** | union of new 480-m patches minus all earlier patches; 2018 = baseline stock | `spatial.py:72-82` | twins, matching, Brazil stagger |

### 6.3 Zones (raster)

Twelve exclusive zones, first match wins (`raster_zones.py:162-165`): 1 Tambopata reserve, 2 other reserves and parks, 3 Kotsimba, 4 other native communities, 5 corridor across the road (D.L. 1100, ≤ 10 km north of the road, La Pampa longitudes), 6 rest of the corridor, 7 La Pampa sector (Tambopata BZ × lon −70.15 to −69.80), 8 rest of Tambopata BZ, 9 Amarakaeri BZ, 10 Bahuaja-Sonene BZ, 11 other BZs, 12 rest of Madre de Dios.

Because communities and the corridor come first, **the raster "La Pampa sector + rest of Tambopata BZ" is not the same land as the statistics workbook's "Tambopata buffer zone"**: Kotsimba and the 21 km² of corridor inside the BZ are assigned elsewhere.

## 7. Tests run and results

### T0 · The accounting identity

net = new + re-mined − stopped holds exactly in every zone and year (max error 0.0 ha).

### T1 · Gross vs net: what the "fall" in La Pampa is made of

Mean ha/yr, raster zones (`zone_year_v2.csv`):

| La Pampa sector | Net | New land | Re-mined | Stopped |
|---|---|---|---|---|
| 2016-18 | 1,193 | 1,395 | 252 | 454 |
| 2019-21 | **79** | **722** | 379 | **1,022** |
| 2022-25 | 1,547 | 987 | 893 | 332 |

From 2016-18 to 2019-21 the net addition fell by 1,114 ha/yr. That splits into:
- −673 from less new land (60% of the fall);
- −568 from more land stopping (51%);
- +127 from more re-mining (−11%).

**About half of the "fall" in net additions is pits leaving the mining class, not less new mining.**

Year by year, 2019 is the clearest case: net +234, but new land 1,494 (almost the 2018 level of 1,782), because 1,453 ha stopped.

| Corridor across the road | Net | New | Re-mined | Stopped |
|---|---|---|---|---|
| 2016-18 | 61 | 69 | 66 | 74 |
| 2019-21 | 395 | 463 | 193 | 261 |
| 2022-25 | 603 | 538 | 242 | 178 |

Here the rise is visible in every measure, so the "across the road" increase does not depend on which outcome we use.

### T2 · The 2023 spike

Ratio of 2023 to the mean of 2022 and 2024:

| Measure | Ratio |
|---|---|
| MapBiomas first-time mining, all zones | 1.55 |
| MapBiomas re-mined, all zones | **2.94** (La Pampa **5.79**) |
| MapBiomas net additions, all zones | 2.14 |
| GLAD alerts on mining pixels | 0.97 |
| GLAD all alerts | 0.76 |
| AMW new area | 1.04 |

The spike appears in **every** zone in MapBiomas only (first-time spike 1.28-1.89 by zone; re-mined 1.9-5.8). Neither GLAD nor AMW shows it.

**Verdict.** This is likely, at least in part, a MapBiomas 2023 classification effect. But GLAD and AMW cannot see re-working of old pits, so the re-mining part cannot be refuted with them. MAAP #193 does report many more dredges in La Pampa in 2021-23. **Proposed rule:** report every 2022-25 number with and without 2023.

### T3 · MINEM vs BCRP gold, every year

(The BCRP series is in grams.)

| Years | MINEM rebuild vs BCRP |
|---|---|
| 2005-14 | exact |
| 2015 | +47.6% (declared 556 + estimate 12,175 vs BCRP 8,622 kg) |
| 2016 | **+8.3%** (17,569 vs 16,223 kg) |
| 2017 | exact |
| 2018 / 2019 | +0.9% / +0.4% |
| 2020 | +47.4% (2,152 vs 1,460 kg) |
| 2021-25 | +10% to +16% |

For 2021 and 2025 I checked the raw MINEM workbooks:
- The parser reads them correctly: one sheet, gold rows in Madre de Dios, the ACUM column. The sum equals the rebuild.
- So the gap is a difference between the **sources** (MINEM's yearly file vs the central bank's departmental series, probably later revisions), not a parsing bug.

Consequences:
- The check at `peru_gold_minem.py:119-120` tests only 2012 and 2019, two years that agree.
- The docstring (`:10`), `DOWNLOAD_LOG.csv` and `explainer_content.md:352` say 2016 matches "exactly". **That is false.**
- The qualitative point still stands: the official series drops in 2020 because the artisanal estimate leaves the files (BCRP itself goes 7,073 → 1,460 kg).
- The kg levels quoted as "declared output" (944 → 1,362 kg) are MINEM-file numbers that run 10-16% above BCRP after 2020.

### T4 · What "rest of Madre de Dios" contains

First-time mining outside all buffer zones, shares of ha/yr:

| Zone | 2016-18 | 2019-21 | 2022-25 |
|---|---|---|---|
| Rest of the mining corridor | 65% | 71% | 75% |
| Native communities (incl. Kotsimba) | 27% | 20% | 17% |
| Corridor across the road | 2% | 8% | 5% |
| Tambopata reserve | 5% | 1% | 1% |
| Rest of the department | 0% | 1% | 1% |

So "rest of Madre de Dios" is mostly the corridor, but **one sixth to one quarter is native-community land**, and it includes the reserve. The label "incl. legal corridor" (`peru.py:316, 356`) undersells this. **Proposed label:** "Rest of Madre de Dios (mostly the legal mining corridor; also native communities and protected-area interiors)".

### T5 · Bahuaja-Sonene

The Bahuaja-Sonene buffer zone is 218,791 ha in Puno and 145 ha in Madre de Dios. Its mining (532 ha in 2025) is all in Puno. It enters event-study pool A ("zones touching Madre de Dios", `peru.py:160-162`) only through that 145-ha sliver. This is to be decided in S3.

### T6 · Statistics workbook vs raster zones

Tambopata BZ net additions, ha:

| Year | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Workbook (pack) | 1,590 | 1,463 | **707** | 2,455 | 1,757 | 417 | 181 | −111 | 580 | 3,565 | 1,276 | 1,896 |
| Raster: La Pampa + rest of BZ | 1,490 | 987 | **356** | 2,034 | 1,550 | 284 | 186 | −89 | 483 | 3,273 | 1,172 | 1,857 |

The two agree in shape but differ by up to 476 ha in 2015 and by half in 2016. That is the land assigned to Kotsimba and the corridor in the raster, plus product differences.
- The 2016 dip that drives several placebo results (S3, S4) is **twice as deep in the workbook**.
- Zone-level and pixel-level results therefore cannot be compared one-to-one.

### Tests not possible here (need the git-ignored rasters)

- **Grid identity:** assert the same CRS, transform and shape for all 41 yearly rasters.
- **Flicker:** count pixels mined in exactly one year; redefine first-time mining as "mined in t and t+1".

Both should be run on a machine that has `data_raw/mapbiomas_peru_raster/`.

### Source checks: what is a real publisher check

| Kind | Checks |
|---|---|
| **Publisher screen read by us** | Tambopata NR 777 ha (screenshot); Kayapó Col 11 17,632 / 18,573; PP 0128 S/ 31,120,611; DETER 2019 |
| **Publisher numbers from the course log** | gold price; MdD 112,622; Tambopata BZ 20,730; Brazil 609,637; garimpo 445,987; TIs 39,915 |
| **Reproductions, not publisher checks** | "Card:" lines (1,640 / 163 / 289 / 574 / −1,762); ANP 834 ha; raster vs table |
| **Plausibility only** | Tambopata reserve area 2,778 vs FZS 2,746 km² |

The brief needs **one publisher check per dataset**. The table-based ones are fine. The "Card:" lines should not be described as publisher checks.

## 8. Assumption check

| Assumption | Verdict | Evidence |
|---|---|---|
| A1 Valid classification | Partly | Publisher totals reproduce (raster vs table within 0.1%), but legality and dredges are invisible by design |
| A2 Stable over time | **Doubtful for 2023** | T2: MapBiomas-only spike |
| A3 Error unrelated to treatment | **Violated for net additions** | T1: "stopped" doubles in La Pampa exactly in 2019-21 |
| A4 Comparable at-risk pool | **Violated** | Mined share in 2018: La Pampa 18%, Tambopata BZ 5.6%, Amarakaeri 2.7%, all other BZs < 0.7% (pack `total_ha`, raster zone areas) |
| A5 Fixed units | Partly | Zone rules differ between workbook, raster and AMW modules (T6; AMW precedence differs, S13) |

## 9. Weaknesses, ranked

1. **Net additions mix less mining with more abandonment.** About half of La Pampa's 2019-21 fall in net additions is pits stopping. Every zone-level design (A1-A6) inherits this.
2. **Depletion biases first-time mining toward a fall in dense places.** This affects A7-A9.
3. **2023 is probably a MapBiomas artefact** in part. It sits in every "later years" mean.
4. **The MINEM text and check claims an exact 2016 match that does not exist.** Kg levels after 2020 are from MINEM files that run 10-16% above BCRP.
5. **"Rest of Madre de Dios" is mislabelled** (communities and the reserve inside it).
6. **Workbook and raster zones are different land.** Do not mix their numbers in one sentence.
7. Bahuaja-Sonene is a Puno zone in a "Madre de Dios" pool.

## 10. Proposed decisions (to confirm with Ruby)

| # | Decision | Recommendation |
|---|---|---|
| D-S1-1 | Which measure carries the causal sentence? | Keep **net additions** for the zone designs (course rule), but always show the split (new / re-mined / stopped) next to it, and state that half the net fall is abandonment. Use first-time mining for the pixel designs. Never mix the two in one comparison. |
| D-S1-2 | 2023 | Report every 2022-25 number with and without 2023. |
| D-S1-3 | MINEM | Change the check to compare every year and list the mismatches. Fix the "2016 exactly" sentence (docstring, log, walkthrough). Keep the definition-change point; cite BCRP kg rather than MINEM kg for declared output after 2020. |
| D-S1-4 | Labels | Rename "rest of Madre de Dios" as above, in `peru.py` and the walkthrough. |
| D-S1-5 | Depletion | Add an at-risk (hazard) version of first-time mining in S8 and S9. |

## 11. Verdict

The outcome measures are correctly computed: the identity holds and publisher totals reproduce. But they are **not interchangeable**, and the most-used one (net additions) partly measures abandonment.

Any claim about "less mining" must name its measure. Where the measure is net additions, the claim needs the sentence: "about half of this fall is land leaving the mining class, not less new clearing".

## References

- Bound, J., Brown, C. and Mathiowetz, N. (2001). Measurement error in survey data. *Handbook of Econometrics* 5, ch. 59.
- Openshaw, S. (1984). *The Modifiable Areal Unit Problem*. Geo Books.
- Olofsson, P. et al. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment* 148.
- MAAP #193 (2023), maapprogram.org: dredges in La Pampa 2021-23 (see `docs/walkthrough/notes/maap_citations.md`).
