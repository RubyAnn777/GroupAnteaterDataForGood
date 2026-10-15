# S9 · Spatial regression discontinuity and the road tests (attempts A8, A9)

*Method card 9 of the causal review (plan: `docs/causal_review_plan.md`, section S9). Code under review: `code/v2_rdd.py` (A8), `code/v2_tests.py:35-60` and `code/placebo_explainer.py:35-41` (A9), `code/raster_zones.py:112-134` (`signed_road_km`). Test script: `code/review/s9_rd_checks.py` (read-only).*

---

## 1. In one sentence

Compare places just on either side of a line where a rule changes; if nothing else jumps at the line, the jump in the outcome is the rule's effect at the line, and if something else does jump but stays fixed over time, the *change* in the jump after a policy date isolates what changed at the line on that date.

## 2. Simple version

A town has a speed camera on one side of a street. Accidents just east of the street are compared with accidents just west of it. Houses 50 m apart are alike in almost every way, so a difference right at the street is plausibly the camera's doing. That is a **regression discontinuity (RD)**.

Now suppose the street is also a bus route, so the east side always had more traffic. A plain RD would mix the camera with the bus route. If the camera arrived in 2019 and the bus route did not change, compare **the jump after 2019 with the jump before**. That is a **difference in discontinuities**.

Two things can still go wrong:
- **Something else changed at the street in 2019** (a new shop opens on one side). Then the change in the jump mixes the camera with the shop.
- **Drivers re-route.** If the camera pushes speeders onto the west side, accidents fall east and rise west. The jump grows from both ends, so it overstates what the camera did on either side. This is a **spillover across the border**.

In our project the "street" is the Interoceanic Highway at La Pampa. South of it is the Tambopata buffer zone (where Mercurio struck, mining illegal). North of it is the legal mining corridor (D.L. 1100). The outcome is the share of land mined for the first time each year.

## 3. When to use it, and when not

**Use it when:**
- treatment is assigned by a known line (a border, a score cut-off) that units cannot precisely choose to sit on;
- there are many observations close to the line on both sides;
- you can argue that every other determinant of the outcome is smooth across the line (or, for a difference in discontinuities, that its jump is stable over time).

**Be careful or avoid it when:**
- the line bundles several changes at once (**compound treatment**): a road is a legal border, an access route and a target line at the same time;
- the treatment can push the outcome across the line (displacement), which breaks "no interference";
- the outcome is absorbing (land can be mined for the first time only once), so one side can run out of land;
- the line is one contiguous object: observations along it are spatially correlated, and the effective number of independent units is the number of segments, not the number of bins;
- there is a single policy date: the over-time comparison has only one "before vs after" contrast, so inference over time rests on a few placebo dates.

## 4. Assumptions

| Assumption | In words | Formally (x = signed distance, c = 0 the border, D = 1[x ≥ 0]) |
|---|---|---|
| **Continuity** (plain RD) | Without the rule, the outcome would be smooth across the line | E[Y(0) ∣ x] and E[Y(1) ∣ x] continuous at x = 0 |
| **Stable other jumps** (diff-in-disc) | Whatever else jumps at the line (road access, geology, legality) jumps by the same amount before and after | lim₊ − lim₋ of E[Y_t(0) ∣ x] equal for t = pre and t = post |
| **No manipulation / sorting** | Units do not move across the line in response to treatment | density of x continuous; for land, polygons fixed |
| **No interference (SUTVA)** | Treatment on one side does not change outcomes on the other | Y_i depends only on D_i |
| **Running variable measured correctly** | x is the true distance in the direction that matters | x = perpendicular distance to the line |
| **Correct functional form near c** | A local line fits each side within the bandwidth | bias of the local linear fit is small, or corrected |
| **Enough independent information** | Clusters (segments) many enough for cluster-robust inference | G large, errors independent across segments |

## 5. The maths

### 5.1 Master's level

**Sharp RD.** With running variable x and cut-off c = 0, treatment D = 1[x ≥ 0]. The RD estimand is

  τ_RD = lim_{x↓0} E[Y ∣ x] − lim_{x↑0} E[Y ∣ x].

Under continuity this equals E[Y(1) − Y(0) ∣ x = 0], the effect for units at the line, and only there.

**Local linear regression.** Fit a separate straight line on each side, using only observations within a bandwidth h, weighted by a kernel K(x/h) that gives more weight to points near the line. The triangular kernel K(u) = (1 − |u|) for |u| ≤ 1 is the standard choice. The RD estimate is the difference between the two intercepts at x = 0.

**Bandwidth.** A wider h uses more data (less variance) but lets curvature bias the intercepts. The MSE-optimal bandwidth (Imbens and Kalyanaraman 2012; Calonico, Cattaneo and Titiunik 2014, "mserd") balances the two.

**Difference in discontinuities** (Grembi, Nannicini and Troiano 2016). Run the RD on the *change* in the outcome:

  τ_DiDisc = τ_RD(Ȳ_post − Ȳ_pre) = [jump in Y_post] − [jump in Y_pre].

Any confounder that jumps at the line but is constant over time cancels. A confounder whose jump changes over time does not.

**Donut RD.** Drop observations within a small distance of the line (here 0.5 km). It guards against problems right at the line (the road verge itself, mis-registration of the border, heaping), at the cost of extrapolating the fit into the hole.

### 5.2 PhD level

**Robust bias-corrected inference** (Calonico, Cattaneo and Titiunik 2014). At the MSE-optimal h, the bias of the local linear estimator is of the same order as its standard error, so conventional confidence intervals under-cover. CCT estimate the leading bias with a local quadratic fit on a pilot bandwidth b, subtract it, and inflate the variance to account for the bias estimate. The reported "robust" CI is centred on the bias-corrected estimate, so the point estimate printed (conventional) can sit off-centre in its own interval. Cluster-robust versions (CR1, CR2, CR3) are available; with few clusters CR1 is anti-conservative, and CR2/CR3 (Bell and McCaffrey 2002; Pustejovsky and Tipton 2018) are safer.

**Geographic RD** (Keele and Titiunik 2015; Dell 2010). With a border in two dimensions, the running variable is the distance to the border, and the estimand is an *average over the border* of point-wise effects. Three issues are specific to it:
1. **Distance metric.** The relevant distance is the shortest (perpendicular) distance to the line. A one-dimensional proxy, such as latitude difference, stretches distances where the line runs at an angle and changes which observations fall inside h.
2. **Boundary heterogeneity.** The effect can differ along the border. Segment fixed effects or segment clusters keep comparisons within stretches of the border; Dell (2010) uses boundary-segment fixed effects.
3. **Compound treatment.** Real borders bundle many changes (Keele and Titiunik 2015 discuss media markets that coincide with other boundaries). The RD then identifies the effect of the whole bundle. A difference in discontinuities removes the time-invariant part of the bundle, but not anything that changes at the border on the policy date.

**Spillovers across the border.** If the treatment on side S changes outcomes on side N (displacement), then with Y_S = Y_S(0) + τ_S and Y_N = Y_N(0) + s_N,

  τ_DiDisc (N − S) = s_N − τ_S.

With τ_S < 0 (deterrence) and s_N > 0 (displacement) both terms push the estimate up. The diff-in-disc measures the **swing** between the two sides; it is not the effect of the policy on either side, and it bounds neither unless one of the two terms is known to be zero.

**Absorbing outcomes.** If Y is "first-time mined", land mined once leaves the risk set. A side that was more depleted before the policy mechanically has less land left to mine afterwards, and the jump in a *share-of-all-land* outcome changes even with constant behaviour. Using the at-risk denominator (land not yet mined) addresses this.

**Mass points and discreteness.** Here the running variable is the mean distance of a 250-m bin, so there are many distinct values; mass points are not a problem. The effective sample is the number of 2-km segments (19 at the road), which is the binding constraint for inference.

**Inference over time.** With one policy date, the time dimension offers a placebo distribution: re-run the identical statistic at fake start years whose windows end before treatment. The rank of the real statistic is a randomization p-value under exchangeability of start years. With 9 clean fakes the smallest attainable p is 0.10.

## 6. Our example

### 6.1 Set-up as coded (A8, `code/v2_rdd.py`)

| Element | As coded | Where |
|---|---|---|
| Borders | (a) the Interoceanic Highway (PE-30C) inside the La Pampa longitudes −70.15 to −69.80; (b) the edge of the Tambopata National Reserve where the land outside is buffer zone | `v2_rdd.py:59-71`, `raster_zones.py:57` |
| Sides at the road | south = zone 7 (La Pampa sector, Tambopata BZ, targeted, illegal mining); north = zone 5 (D.L. 1100 corridor across the road, legal) | `v2_rdd.py:61` |
| Running variable, road | signed km to the road, north positive: **latitude difference to the road at the same longitude × 110.574** | `raster_zones.py:112-134` (line 133) |
| Running variable, reserve | Euclidean distance transform to the reserve edge, inside positive | `v2_rdd.py:67-70` |
| Unit | 250-m distance bin within a 2-km segment along the border (units < 5 ha dropped) | `v2_rdd.py:39, 76-83, 98` |
| Outcome | land mined for the first time, % of the unit's area per year (MapBiomas Peru Col 4, first-mined year) | `v2_rdd.py:102` |
| Windows | PRE 2014-18, POST 2019-21, LATE 2022-25 | `v2_rdd.py:40` |
| Estimand | difference in discontinuities: RD on (mean POST − mean PRE) | `v2_rdd.py:131` |
| Estimator | `rdrobust`, local linear, triangular kernel, MSE-optimal h (mserd), area weights, robust bias-corrected CI, CR1 by segment (`vce="hc1"` + cluster) | `v2_rdd.py:107-116` |
| Sensitivity | fixed h 1/2/3/5 km; 0.5-km donut *at the headline h*; fake start years; fake borders ±2-4 km | `v2_rdd.py:135-155` |

### 6.2 The road test A9 (`code/v2_tests.py:35-60`, `code/placebo_explainer.py:35-41`)

Outcome: the share of first-time mined land that lies north of the road, inside the La Pampa longitudes, summed over 1-km road bands from `road_band_year_v2.csv`. Statistic: mean of the 3 years from the start year minus the mean of the 3 years before (`shift_test`, `v2_tests.py:35-43`). "Clean" start years: ≤ 2013, 2022 and the real 2019 (`v2_tests.py:52`).

Important: the road bands cover **all zones** in the La Pampa longitudes (reserve, communities, rest of the corridor), not just zones 5 and 7, and they run to **±30 km** (`raster_zones.py:64`, `BAND_KM = 30`). The docstrings and the figure caption say 0-15 km (`v2_tests.py:3`, `v2_tests.py:97`, `raster_zones.py:36`), while the `numbers.csv` descriptions say ±30 km.

### 6.3 Data lineage

MapBiomas Peru Col 4 annual rasters → `raster_zones.py` builds `zones_v2_mdd_full.tif` (band 1 zone code, band 2 first-mined year; git-ignored but present in this checkout) → `v2_rdd.build()` writes `rdd_units_v2.csv` and `rdd_unit_year_v2.csv` (committed) → `v2_rdd.analyse()` → `rd_*` rows in `output/numbers.csv` and `output/table_rdd.csv`. My rebuild of the road units from the tif reproduces the committed first-time hectares exactly (18,107.7 ha 1986-2025 in both).

## 7. Tests run and results

All numbers below come from `code/review/s9_rd_checks.py` unless an id from `output/numbers.csv` is given.

### T1 · Reproduce

| Border | Diff-in-disc 2019-21 vs 2014-18 | 95% robust CI | p | h (km) | units in h | clusters in h |
|---|---|---|---|---|---|---|
| Road | **+2.102** (`rd_road_did`) | −0.19 to +3.46 | 0.079 | 2.45 | 376 | 19 |
| Road, 2022-25 vs 2014-18 | +1.192 (`rd_road_did_late`) | −0.84 to +3.06 | 0.263 | 2.20 | 339 | |
| Reserve | **+0.154** (`rd_reserve_did`) | −0.57 to +0.76 | 0.772 | 1.53 | 903 | 158 |
| Reserve, 2022-25 | +0.128 | −1.17 to +1.71 | 0.711 | 1.84 | 1,046 | |

Every audit number reproduces. Note that the conventional point estimate (+2.10) sits near the top of its robust interval, which is centred on the bias-corrected estimate: the bias correction pulls the estimate down.

Plain-language side means within h (`rd_road_mean_*`): south 1.77 → 1.15, north 0.13 → 2.60 % of land a year. In these raw side means, about 20% of the change in the gap is the south falling (−0.62) and 80% is the north rising (+2.47). (The raw-mean change, +3.09, is larger than the local linear estimate, +2.10, because the fitted lines are extrapolated to the road.)

### T2 · Is the gap constant without treatment?

**T2a · Yearly gap at the road** (north − south, levels, fixed h = 2.45 km):

| 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| +0.03 | +1.85 | +1.09 | **−3.53** | −0.21 | −0.71 | +0.38 | −0.08 | −0.21 | −1.25 | −1.36 | +0.31 | +1.30 | **+3.18** | +2.11 | +0.36 | +0.27 | −0.24 |

The pre-2019 gap swings from +1.85 to −3.53 with no Mercurio (sd 1.24 over 2005-18). The headline change (+2.10) is about 1.7 pre-period standard deviations. The two years right before Mercurio (2017-18, −1.3) are the lowest since 2011, which inflates the diff-in-disc when they are in the baseline.

**T2b · Choice of PRE window** (POST 2019-21, bandwidth re-chosen each time):

| PRE | Road | p | Reserve | p |
|---|---|---|---|---|
| 2014-18 (main) | **+2.10** | 0.079 | +0.15 | 0.77 |
| 2009-13 | +1.89 | 0.21 | **+1.05** | **0.001** |
| 2016-18 | +2.54 | 0.036 | −0.46 | 0.44 |
| 2011-18 | +2.63 | 0.066 | +0.47 | 0.18 |
| 2009-18 | +2.17 | 0.085 | +0.59 | 0.046 |
| 2017-18 | +2.88 | 0.068 | −0.92 | 0.27 |
| 2014-16 | +1.62 | 0.37 | +0.84 | 0.060 |

The road sign never changes (+1.6 to +2.9), but p runs from 0.036 to 0.37. The reserve result is **not** robustly null: with a 2009-13 baseline it is +1.05 (p = 0.001), and its sign flips across windows. Its null depends on the 2017 invasion sitting in the main PRE window (T8).

### T3 · Timing: when did the gap open?

| POST (vs PRE 2014-18) | mserd h: estimate (p) | fixed h 2.45: estimate (p) |
|---|---|---|
| 2019 only | +0.77 (0.58) | +0.82 (0.22) |
| 2020 only | +1.71 (0.14) | +1.81 (0.22) |
| 2021 only | +3.67 (0.093) | +3.69 (0.19) |
| 2020-21 | +2.74 (0.078) | +2.75 (0.089) |
| 2019-21 (main) | +2.10 (0.079) | +2.10 (0.075) |
| 2022 only | +2.53 (**0.043**) | +2.61 (0.028) |
| 2023 only | +0.83 (0.61) | +0.87 (0.43) |
| 2022-25 | +1.19 (0.26) | +1.13 (0.19) |
| 2022, 2024, 2025 (no 2023) | +1.31 (0.19) | |

**In 2019, the first treated year, the gap barely moved (+0.8, p 0.22-0.58).** It widened in 2020 and peaked in 2021-22, then closed by 2023-25. This matches X3 (the fall starts with COVID) and the S8 cell event study (2019 = +0.13). The statement "new mining jumped across this legal line within a year" (`explainer_content.md:670`, also :809, :883, :899) and the figure headline "After Mercurio, mining jumped across the road" (`v2_rdd.py:234`) overstate the timing. The swing is a 2020-22 phenomenon.

### T4 · Fake start years (same statistic, headline h)

**Road** (first year with mining within h = 2008): fakes 2008-16 are +0.99, −0.20, −1.26, **−2.08** (2011), −0.07, +0.02, +0.33, +0.08, −0.11.
- Real +2.102 ranks **1 of 10** two-sided (`rd_road_fake_rank`, p = 0.10, the floor). It beats the 2011 fake (|−2.077|, `rd_road_fake_max_abs`) by 1.2%.
- One-sided (moves north) it also ranks 1 of 10.

**Reserve** (`rd_reserve_fake_first_year` = 1998): the pool starts in 1998 because one unit within h had a speck of mining then. Fakes 1998-2006 are all within ±0.11, effectively zeros, which pads the pool.

| Reserve pool | rank of |real| | p |
|---|---|---|
| from 1998 (as coded) | 10 of 20 | 0.50 |
| from 2007 | 10 of 11 | 0.91 |
| from 2008 | 9 of 10 | 0.90 |

On a comparable pool the reserve change is among the smallest. The largest fakes are 2015 (+1.10) and 2016 (+1.47), whose POST windows contain the 2017 invasion.

### T5 · The running variable: latitude offset vs true distance

`signed_road_km` computes `(pixel latitude − road latitude at that longitude) × 110.574` (`raster_zones.py:133`). This is the north-south offset, not the perpendicular distance, and the docstring's "Equal-area metres via ESRI:102033" (`raster_zones.py:114`) is not what the code does. Where the road runs at an angle, the offset overstates the distance.

I recomputed the perpendicular distance in UTM 19S (EPSG:32719) to the road densified at 10 m, kept the sign and zone rule, and rebuilt the units.

| Measure | Value |
|---|---|
| Offset / perpendicular distance, pixels within 10 km | median 1.08, p90 1.24, max 7.7 (at a bend) |
| Same, within 1 km of the road | median 1.07, p90 1.40 |

| Spec | Latitude offset (rebuild) | Perpendicular distance |
|---|---|---|
| Diff-in-disc 2019-21 | +2.08 (p 0.071, h 2.35) | **+2.51 (p 0.108, h 2.68)** |
| 2022-25 | +1.22 (p 0.24) | +1.31 (p 0.30) |
| 2019 only | +0.77 (p 0.57) | +0.96 (p 0.55) |
| 2020-21 | +2.72 (p 0.070) | +3.46 (p 0.105) |
| Donut 0.5 km, own h | +3.40 (p 0.18) | +3.46 (p 0.33) |
| Fake start years 2008-16, two-sided | rank 1 of 10 | **rank 2 of 10** (fake 2011 = −3.18) |

My rebuild with the coded offset gives 1,506 units (committed file: 1,513) and +2.08 instead of +2.10; first-time hectares match exactly, so the small gap is in unit formation, not in the pixels. With the correct distance the point estimate grows, but the p-value rises above 0.10 and **2019 is no longer the largest start year**: 2011 is larger in absolute size.

### T6 · Depletion and geology across the road

| Within the bandwidth | South (La Pampa) | North (corridor) |
|---|---|---|
| Land first-mined by 2013, within 2.45 km | 7.5% | 9.0% |
| Land first-mined by 2018, within 2.45 km | **16.4%** | **9.7%** |
| Land first-mined by 2018, within 1 km | 14.3% | 9.0% |
| Gold-bearing land mined by 2018 (1-km cells within 6 km) | 15.6% | 9.8% |

Around 2013 the two sides were similarly depleted (7.5% vs 9.0%). By 2018 the south had mined 1.7 times more of its land. An absorbing outcome then mechanically lowers the south's rate after 2018.

- With an **at-risk denominator** (new first-time ha / land not yet mined, including land mined in 1985): +1.98 (p = 0.39); 2022-25: +3.00 (p = 0.30). The point estimate barely moves, so depletion does not explain the swing, but significance disappears.
- **Geology cannot be tested.** All 477 1-km cells in zones 5 and 7 within 6 km of the road have `gold_share` = 1.0 (`cell_gold_v2.csv`). The gold proxy (INGEMMET placer geology) cannot show a discontinuity, because there is no variation.

### T7 · Inference and bandwidth

| Variant | Estimate | p | clusters |
|---|---|---|---|
| CR1, 2-km segments (main) | +2.10 | 0.079 | 19 |
| CR2, 2-km | +2.10 | 0.079 | 19 |
| CR3, 2-km | +2.11 | 0.091 | 19 |
| CR1, 4-km segments | +2.15 | 0.19 | 10 |
| CR1, 6-km segments | +2.16 | 0.16 | 7 |
| CR3, 4-km | +2.17 | 0.23 | 10 |
| No area weights | +1.92 | 0.088 | 19 |

| Bandwidth (fixed) | 1.0 | 1.5 | 2.0 | 2.45 | 3.0 | 4.0 | 5.0 |
|---|---|---|---|---|---|---|---|
| Estimate | +1.09 | +1.68 | +1.98 | +2.10 | +2.25 | +2.77 | +3.29 |
| p | 0.98 | 0.61 | 0.23 | 0.076 | 0.052 | 0.093 | 0.11 |

| Donut | at headline h 2.45 | at its own mserd h |
|---|---|---|
| 0.25 km | +2.97 (p 0.009) | +3.00 (p 0.11) |
| 0.5 km (as coded) | +3.29 (p **0.041**, `rd_road_sens_donut_p`) | +3.33 (p 0.20) |
| 0.75 km | +2.74 (p 0.38) | +3.07 (p 0.51) |

Findings:
- The estimate **grows with the bandwidth** (1.1 at 1 km, 3.3 at 5 km). The discontinuity is weakest right at the road, and it builds with distance. That is the signature of a regional shift (south falling, corridor rising over several km), not of a sharp effect at the line.
- The only p < 0.05 in the sensitivity set is the donut at a bandwidth chosen for the full sample. With the donut's own optimal bandwidth it is p = 0.20.
- The brief (`brief_content.md:31`) and `explainer_content.md:432` say "{{rd_road_sens_p_min}}–{{rd_road_sens_p_max}} across bandwidths" = 0.04-0.98; the 0.04 is the donut. Across bandwidths alone the range is 0.052-0.98. (`explainer_content.md:696` and `methods_content.md:247` correctly say "bandwidths and the donut".)
- Coarser clusters double the p-value. The shock is one contiguous operation; 2-km segments along the same road are not independent.

### T8 · The reserve edge

| Fact | Value |
|---|---|
| First-time ha inside the reserve (reserve units), 2000-25 | 1,244 ha |
| of which in **2017** | **521 ha (42%)**; next largest 2025: 237 ha. (RD units clipped to the reserve; raster zone 1 gives 525 ha for 2017, card 13 A3. The 521 ha in Asner and Tupayachi 2017 is a different quantity, cumulative loss to October 2016, and matches only by coincidence.) |
| Share within 1 km of the edge | 90.7% (`rd_reserve_inside_share_1km`); 91.9% without 2017 |
| Reserve-majority 1-km cells: share of 2000-25 first-time mining in cells within 1 km of a river | 99.1% (those cells are 21% of reserve cells) |
| Outside side (buffer zone) first-time ha per year, 2014-18 → 2019-21 | 1,251 → 589 |

Consequences:
1. The 2017 invasion sits in the PRE window. It raises the PRE gap (inside − outside), so the change is pulled towards zero.
2. The **outside side is the treated La Pampa / Tambopata buffer zone**, whose mining halved. A constant inside rate would show up as a *rising* gap. The diff-in-disc mixes Mercurio on the outside with whatever happened inside, so a null does not mean "no change inside".
3. The edge coincides with the Malinowski river, and nearly all inside mining is near a river. "Mining spills about 1 km inside" (`v2_rdd.py:258`) is better described as "mining inside the reserve follows the river along the edge".

### T9 · The A9 road fake-date test (north share)

| Band width | North share 2016-18 → 2019-21 | 2019 shift | Rank, clean set as coded (≤ 2013, 2022, 2019) | Rank, strict (≤ 2013, 2019) | Two-sided, clean |
|---|---|---|---|---|---|
| ±30 km (as coded) | 0.23 → 0.65 | +0.41 | **1 of 8** (`t1_road_shift_rank_clean`) | 1 of 7 | 3 of 8 |
| ±15 km (as documented) | 0.08 → 0.51 | +0.43 | **2 of 8** | 2 of 7 | 5 of 8 |
| ±5 km | 0.11 → 0.56 | +0.45 | 1 of 8 | 1 of 7 | 4 of 8 |
| ±2 km | 0.07 → 0.69 | +0.62 | 1 of 8 | 1 of 7 | 2 of 8 |

- At ±15 km the 2008 shift (+0.59, the Guacamayo boom) beats 2019. The rank depends on the band width.
- Start year 2022 is in the "clean" set (`v2_tests.py:52`), but its PRE window is 2019-21, the treated years. It is not a placebo.
- The negative shifts of 2010-12 (−0.42 to −0.70) are as large as 2019's positive one. The share swings back and forth by 40-70 points every few years. A one-sided rank hides that.
- The share is a ratio of two flows. It rises when the south falls even if the north does not move, so on its own it cannot separate deterrence from displacement.

### Tests not possible here

- **Covariate continuity at the road** (soil, elevation, river access, distance to towns): no such layers are in the repo at pixel level, and the gold proxy has no variation.
- **Pre-1985 depletion**: MapBiomas starts in 1985.
- **A legal-status placebo**: a road stretch where both sides are legal corridor (or both buffer zone) would show whether the road itself creates time-varying gaps. Possible with the zone raster, but it needs a new zone definition. Recommended as a follow-up.

## 8. Assumption check

| Assumption | Verdict | Evidence |
|---|---|---|
| Stable other jumps (road) | **Not supported** | Yearly gap swings −3.5 to +1.9 before 2019 (T2a); PRE window moves p 0.04-0.37 (T2b) |
| Stable other jumps (reserve) | **Not supported** | 2009-13 baseline gives +1.05, p 0.001 (T2b); 2017 invasion in PRE (T8) |
| No interference | **Violated by design** | The raw swing is about 20% south falling, 80% north rising (T1); displacement across the road is the story itself |
| Single treatment at the line | **Violated (compound)** | The road separates illegal from legal mining, targeted from untargeted, and is the access route; COVID (2020) changed patrols and incomes differently on each side |
| Running variable correct | **Violated (minor)** | Latitude offset, not perpendicular distance; median 8% overstatement, up to 40% near the road; changes the estimate to +2.51 (p 0.11) and the fake rank to 2 of 10 (T5) |
| Continuity of geology | **Untestable** | gold_share = 1 for all cells within 6 km (T6) |
| Comparable depletion | **Not met** | 16.4% vs 9.7% of land mined by 2018 (T6) |
| Enough independent clusters | **Weak** | 19 segments; 10 or 7 coarser clusters give p 0.16-0.23 (T7) |
| No manipulation | Holds | Fixed polygons; land cannot sort |
| Timing (effect from 2019) | **Not supported** | 2019 alone +0.8, p 0.22-0.58; swing appears 2020-22 (T3) |

## 9. Weaknesses, ranked

1. **Compound treatment at the road.** The road is at once the legal-mining boundary, the targeting boundary, and the access route, and COVID hit in the second treated year. The diff-in-disc removes only what is constant over time. A change in the relative attractiveness of legal vs illegal land, from any cause, opens the same gap.
2. **The gap is not stable without treatment.** The 2011 swing (−3.5) is larger than any post-2019 year, and the fake-year win over 2011 is 1.2% (offset) or a loss (true distance).
3. **Timing.** Nothing moves in 2019. The swing appears in 2020-22, alongside COVID and Plan Restauración / Mercurio II (context under the S0 decision, but the RD cannot separate them).
4. **The estimate builds with distance from the line** (1.1 at h = 1 km, 3.3 at h = 5 km). This is a regional north-south shift seen through an RD lens, not a local discontinuity.
5. **Inference is fragile.** p 0.079 with 19 segment clusters; 0.16-0.23 with coarser clusters; 0.11 with the correct distance; the only p < 0.05 runs (donut at the full-sample h, PRE 2016-18, 2022 alone) are selected variants.
6. **The reserve null is not informative.** The outside is treated, the 2017 invasion sits in PRE, the pool of fakes is padded, and other baselines give a significant positive change.
7. **Documentation drift.** Docstring of `signed_road_km` (ESRI:102033), A9 band width (0-15 vs ±30 km), "across bandwidths" range including the donut, "within a year".

## 10. Proposed decisions

| # | Decision | Recommendation |
|---|---|---|
| D-S9-1 | Claim label of A8 (road) | **Description**, never causal and never "effect of Mercurio". Word it as "the north-south gap in new mining at the road swung by about 2 points of land a year in 2019-21, mostly from the north rising". |
| D-S9-2 | Timing wording | Replace "within a year" everywhere (`explainer_content.md:670, 809, 883, 899`) with "in 2020-22, starting the year after Mercurio"; change the figure headline (`v2_rdd.py:234`) to something like "From 2020, new mining moved across the road; at the reserve edge the step did not measurably change". Show 2019 alone (+0.8, p 0.22) in the RD table. |
| D-S9-3 | Running variable | Fix `signed_road_km` to perpendicular distance (UTM 19S) and its docstring; report +2.51 (p 0.11) and fake rank 2 of 10. If not fixed, correct the docstring and disclose the offset. |
| D-S9-4 | p-value range | State "p 0.05-0.98 across fixed bandwidths; 0.04 with a 0.5-km donut at the main bandwidth (0.20 at its own)" in the brief and explainer:432; recompute `rd_road_sens_p_min` over bandwidths only. |
| D-S9-5 | Inference | Report CR3 (0.091) and 4-km clusters (0.19) next to CR1. Present the fake-year rank as "1 of 10 (offset) / 2 of 10 (true distance); the 2011 swing is as large". |
| D-S9-6 | Reserve | Drop "nothing changed at the reserve edge" as a finding. Say: "the RD at the reserve edge is uninformative: its outside is the treated zone, the 2017 invasion sits in the baseline, and other baselines give a positive change". Keep the descriptive fact (91% within 1 km, along the river). Start its fake pool at 2007 (rank 10 of 11). |
| D-S9-7 | A9 road fake-date test | Use the documented ±15 km (or report ±2/5/15/30 together); drop 2022 from the clean set; report two-sided ranks. At ±15 km it is rank 2 of 7 (strict), so it should be called "large but not unusual relative to the 2008 swing". Fix `v2_tests.py:3, 97` and `raster_zones.py:36`. |
| D-S9-8 | Depletion | Report the at-risk version (+1.98, p 0.39) as a robustness row. |
| D-S9-9 | Follow-up | A placebo border where the road separates two zones of the same legal status, to test whether the road alone creates gaps over time. |

## 11. Verdict

The RD code is correct as written and every audit number reproduces. As a design it **cannot support a causal claim** about Mercurio, for three independent reasons: the border bundles legality, targeting and access (compound treatment); the gap was not stable before 2019 (2011 swing as large as 2019-21); and displacement across the line is part of what is measured (no interference fails by design). It also has weak inference: one road, 19 segments, p 0.08 at best on the main specification, rising above 0.10 with the correct running variable or coarser clusters.

What it **does** support, as **description**: within about 2.5 km of the highway at La Pampa, the south (targeted, illegal) mined 1.8% of its land a year for the first time in 2014-18 and the north (legal corridor) 0.1%; in 2019-21 the south 1.1% and the north 2.6%. The swing is mostly the north rising. It appeared in 2020, peaked in 2021-22 and had closed by 2023-25.

Label: **description**.

**Wording the brief may use:** "Within 2.5 km of the highway, new mining in the legal corridor north of the road rose from 0.1% to 2.6% of the land a year between 2014-18 and 2019-21, while the targeted La Pampa side fell from 1.8% to 1.1%. The swing appeared in 2020 and faded by 2023 [D]. We cannot tell how much of it is miners moving, and the road is also where legality and access change."

**Wording the brief must not use:** "Mercurio caused mining to jump across the road"; "within a year"; "p = 0.04-0.98 across bandwidths" (unless "and the donut" is added); "at the reserve edge nothing changed" or "the reserve held"; "rank 1 of 10" without noting the 2011 fake and the running-variable issue.

## References

- Bell, R. and McCaffrey, D. (2002). Bias reduction in standard errors for linear regression with multi-stage samples. *Survey Methodology* 28(2).
- Calonico, S., Cattaneo, M. and Titiunik, R. (2014). Robust nonparametric confidence intervals for regression-discontinuity designs. *Econometrica* 82(6).
- Cattaneo, M., Idrobo, N. and Titiunik, R. (2020). *A Practical Introduction to Regression Discontinuity Designs: Foundations*. Cambridge Elements.
- Dell, M. (2010). The persistent effects of Peru's mining *mita*. *Econometrica* 78(6).
- Grembi, V., Nannicini, T. and Troiano, U. (2016). Do fiscal rules matter? *American Economic Journal: Applied Economics* 8(3).
- Imbens, G. and Kalyanaraman, K. (2012). Optimal bandwidth choice for the regression discontinuity estimator. *Review of Economic Studies* 79(3).
- Keele, L. and Titiunik, R. (2015). Geographic boundaries as regression discontinuities. *Political Analysis* 23(1).
- Pustejovsky, J. and Tipton, E. (2018). Small-sample methods for cluster-robust variance estimation and hypothesis testing in fixed effects models. *Journal of Business & Economic Statistics* 36(4).
