# S8 · Raster backbone and the 1-km cell panel (attempt A7)

*Method card 8 of the causal review (plan: `docs/methods/causal_review_plan.md`). Code under review: `code/raster_zones.py` (zones, pixel accounting, cells), `code/v2_stats.py` (cell DiD, event studies, road gradient, wild bootstrap), `code/v2_tests.py` (T4 boundary, T7 presumed-illegal share, T9 depth), `code/glad_alerts.py`, `code/raster_gold.py`. Test script: `code/review/s8_cell_panel_checks.py` (read-only, ~10 min because of the bootstraps and Conley errors).*

---

## 1. In one sentence

Cut the map into many small squares, follow each square over the years, and ask whether squares in the targeted area changed differently after the operation from squares elsewhere, with standard errors that allow nearby squares to move together.

## 2. Simple version

Imagine a chessboard laid over the forest. Each square is 1 km × 1 km. Every year we count how many hectares in each square were mined for the first time.

- Some squares sit in La Pampa (the target). Most sit somewhere else.
- We compare each square with **itself** (cell fixed effects: a square that always has a lot of mining is not "treated" just for being busy) and each year with **itself** (year effects: a good gold year lifts every square).
- What is left is: did La Pampa squares drop *more* after 2019 than the other squares did?

Why do this at all, when we already have zone totals? Because one zone gives one number and no standard error. Thousands of squares give thousands of numbers. **But** the squares are not independent: neighbours share a river, a road, a gang, a patrol. The operation hit one contiguous area. So in practice we do not have 572 independent La Pampa observations; we have one treated area cut into 572 pieces. Clustering by 10 × 10 km blocks is the attempt to admit this; it leaves 14 treated blocks.

Two more traps a chessboard has:
- **Empty squares.** If the comparison squares almost never have mining, "relative to the comparison" just means "relative to zero", and the DiD becomes a before/after.
- **Used-up squares.** A square can be mined for the first time only once. A square that is already 60% mined has less land left to mine, so its first-time mining falls even if nobody stops the miners (an *absorbing* outcome; depletion).

## 3. When to use it, and when not

**Use it when:**
- the outcome is mapped on a grid and you want to place a change precisely in space (which side of a road, how far from an edge);
- treatment varies across many separate places, so clusters are many and treated clusters are many;
- comparison cells are similar to treated cells in what drives the outcome (same exposure to the outcome process).

**Be careful or avoid it when:**
- one contiguous area is treated: the number of *independent* treated units is the number of treated clusters (here 14), and conventional cluster-robust errors over-reject with few treated clusters (MacKinnon and Webb 2017);
- most comparison cells can never have the outcome (forest reserves far from any mine): they add precision on paper but no information about the counterfactual;
- the outcome is absorbing (first-time events) and the treated cells are already partly used up;
- the zone boundaries were drawn by looking at the outcome (La Pampa's window was chosen from the map of first-mined years, `raster_zones.py:21-22`);
- displacement is likely: then nearby cells are not untreated, and "across the road" is itself a treated outcome.

## 4. Assumptions

| Assumption | In words | Formally |
|---|---|---|
| **Parallel trends (cells)** | Without Mercurio, La Pampa cells' first-time mining would have changed like the comparison cells' | E[Y_ct(0) − Y_cs(0) \| c ∈ LP] = E[Y_ct(0) − Y_cs(0) \| c ∈ ref] for pre s, post t |
| **Comparable exposure** | Comparison cells could have had mining at all (common support in the outcome process) | P(Y_ct > 0 \| ref) not ≈ 0 |
| **No spillover** | Mercurio did not change the comparison cells | Y_ct = Y_ct(0) for c ∈ ref |
| **No depletion / at-risk equal** | The pool of land still minable does not differ in a way that changes first-time mining by itself | hazard h_ct = Y_ct / U_c,t−1 has parallel trends, or U is not binding |
| **Correct dependence model** | Errors are independent across the chosen clusters (10-km blocks), or the spatial kernel captures the correlation | E[ε_ct ε_c't'] = 0 if block(c) ≠ block(c') |
| **Enough treated clusters** | The CRV1 / wild bootstrap reference distribution is valid | G_treated large; CRV1 over-rejects badly when few clusters are treated (MacKinnon and Webb 2017, 2018) |
| **Zones fixed and not chosen on the outcome** | La Pampa and "across" boundaries are exogenous to Y | boundaries independent of ε |

## 5. The maths

### 5.1 Master's level

The main specification (`v2_stats.py:95-113`) is a two-way fixed-effects regression with one dummy per focal zone and period:

  y_ct = α_c + γ_t + Σ_z Σ_p β_zp · 1[c ∈ z] · 1[t ∈ p] + ε_ct,

with y = first-time mined hectares in cell c and year t, periods p ∈ {2019-21, 2022-25}, reference period 2014-18, and the omitted group = "clean" reference cells.

**Exact algebra.** Every non-reference group has its own dummy for every post period and the panel is balanced, so the model is saturated in group × period. Then

  β̂_zp = (Ȳ_z,p − Ȳ_z,pre) − (Ȳ_ref,p − Ȳ_ref,pre),

a difference in differences of simple means. If Ȳ_ref barely moves, β̂ is the zone's own before/after change.

**Clustered errors.** CRV1 by block g:

  V̂ = (X̃'X̃)⁻¹ (Σ_g X̃_g' ê_g ê_g' X̃_g) (X̃'X̃)⁻¹ · G/(G−1) · (N−1)/(N−K),

where X̃ are the regressors after removing cell and year effects (Frisch-Waugh-Lovell). Its reliability depends on the number of clusters that contain treated cells, not on the total G.

**Wild cluster restricted bootstrap (WCR).** Impose H₀: β = 0, fit the restricted model, and resample by flipping the sign of whole clusters' restricted residuals (Rademacher weights). Compute the CRV1 t-statistic in each draw; the p-value is the share of |t*| ≥ |t̂| (Cameron, Gelbach and Miller 2008). With few treated clusters WCR tends to be conservative rather than liberal (MacKinnon and Webb 2017), which is the safer direction.

**PPML.** Poisson pseudo-maximum likelihood (Santos Silva and Tenreyro 2006) models E[y | x] = exp(α_c + γ_t + β'x). It is consistent for non-negative outcomes with many zeros, and β is a proportional change. Two facts matter here:
1. Cells whose outcome is zero in every year contribute nothing (their cell effect goes to −∞), so PPML uses only ever-positive cells.
2. With saturated group × period dummies, the first-order conditions match fitted and observed **totals** per group and period, so β̂_zp ≈ log(total_z,p / total_z,pre) − log(total_ref,p / total_ref,pre). The reference here is the set of ever-positive reference cells only.

**Depletion / hazard.** First-time mining is absorbing: a pixel leaves the risk set once mined. Let U_c,t−1 be the unmined area of cell c at the end of t−1. The hazard h_ct = y_ct / U_c,t−1 is the share of the remaining land mined for the first time. A fall in y with constant h is depletion; a fall in h is a change in the rate at which the remaining land is taken.

### 5.2 PhD level

**Few treated clusters.** Conley and Taber (2011) and MacKinnon and Webb (2017, 2018) show that when the treated observations sit in a handful of clusters, CRV1 t-tests over-reject because the treated clusters' scores dominate the meat matrix and their residuals are shrunk by the fit. WCR fixes much of this when treated clusters are not too few, but with very few it can under-reject and the p-value distribution becomes discrete. Randomisation-style inference over placebo locations (Conley and Taber 2011; a spatial permutation here) is the natural complement.

**Spatial correlation.** Conley (1999) spatial HAC uses a kernel K(d_cc') to weight cross-products of scores of cells within a cutoff distance:

  Meat = Σ_c Σ_c' K(d_cc') s_c s_c'',  with s_c = Σ_t x̃_ct ê_ct

(scores summed over years within a cell allow arbitrary serial correlation). Blocks are a crude version with a box kernel and arbitrary borders. When the shock (an operation) is larger than the block, both understate the variance; results that hold only at small cutoffs are fragile. Recent work on design-based inference for spatial treatments (e.g. randomisation over feasible treated locations) makes the same point.

**Spatial spillovers.** Butts (2023) shows that with spillovers decaying with distance, a DiD with "near-treated" controls is biased, and proposes rings: estimate effects for treated cells and for distance rings around them against far-away controls. The road gradient here (`v2_stats.py:144-157`) is a ring design in one dimension (north-south distance to the highway), but its reference ring is inside the treated area (see T8).

**Multiple testing.** With dozens of coefficients, some will clear 0.05 by chance. Holm (1979) controls the family-wise error rate step-down; Romano and Wolf (2005) do the same using the joint bootstrap distribution, so they are less conservative when tests are correlated.

**Absorbing outcomes.** With first-time events, TWFE on counts conflates rate changes with shrinking risk sets. Discrete-time hazard models (or OLS on y / U_{t−1} with U as weight) separate them. Conditioning on the lagged cumulative share is a bad control after treatment (it is itself an outcome); pre-treatment depletion × year effects are the cleaner version, but require comparison cells at similar depletion levels (overlap).

## 6. Our example

### 6.1 From pixels to cells

| Element | As coded | Where |
|---|---|---|
| Raster | MapBiomas Peru Collection 4, 30 m, 1985-2025; mining = class 30 | `raster_zones.py:54-56` |
| First-time mining (outcome) | pixel is mining in t and was never mining in any earlier year since 1985 | `raster_zones.py:195` |
| Zones | 12 exclusive zones, first match wins (reserve, other ANP, Kotsimba, other communities, across the road, rest of corridor, La Pampa, rest of Tambopata BZ, ...) | `raster_zones.py:158-166` |
| La Pampa | Tambopata BZ inside lon −70.15…−69.80, chosen from the map of first-mined years | `raster_zones.py:21-22, 58` |
| Across the road | D.L. 1100 corridor, inside the La Pampa longitudes, 0-10 km north of the highway | `raster_zones.py:160` |
| Cells | 33 × 33 pixels (~1 km), inside the study window lon 70.65-69.30 W, lat 13.30-12.40 S, inside Madre de Dios | `raster_zones.py:62-63, 213-223` |
| Cell zone | majority zone of the cell's pixels | `raster_zones.py:248-249` |
| Panel | every cell, 2010-2025, never-mined cells filled with zeros | `v2_stats.py:42-58` |
| Blocks | 10 × 10 cells (row // 10, col // 10) | `v2_stats.py:50-52` |
| Gold share | share of the cell on "broad" gold-bearing geology (INGEMMET alluvium + Madre de Dios Formation upper member); binned low / mid / high | `raster_gold.py:26-27, 80`; `v2_stats.py:57` |
| Road distance | mean signed north-south offset to the Interoceanic Highway (km) | `raster_zones.py:112-134, 243-244` |

### 6.2 The specifications

| Spec | Formula | Sample | Where |
|---|---|---|---|
| S1 main | new_land_ha ~ Σ_z Σ_p zone_z × period_p \| cell + year; CRV1 by block | 2014-25; clean reference = cells outside all six focal zones, the rest of the corridor (6) and other communities (4) | `v2_stats.py:95-113` |
| S1 variants | + gold_bin × year; outcome re-mined; PPML; contaminated reference | same | `v2_stats.py:235-238` |
| WCR | 999 Rademacher draws, 10-km blocks, after FWL | S1 main sample | `v2_stats.py:73-92, 257-283` |
| S2 event study | year dummies 2010-13 and 2019-25 × zone; pooled 2014-18 = 0; joint test on 2010-13 | one focal zone + clean reference | `v2_stats.py:122-141` |
| S3 road gradient | 6 distance bands × 2 periods; omitted band "S 10-30" | cells inside lon −70.20…−69.75 | `v2_stats.py:144-157` |

Panel size: 14,241 cells × 16 years (`st_n_cells`); the S1 regression sample has 8,744 cells (572 La Pampa, 395 across the road, 353 Kotsimba, 1,383 reserve, 1,090 rest of Tambopata BZ, 95 Amarakaeri BZ, 4,856 reference: `st_n_ref_cells_clean`).

## 7. Tests run and results

All from `code/review/s8_cell_panel_checks.py` unless an `output/numbers.csv` id is given.

### T0 · Trace

Rebuilding first-time mined hectares per cell-year from the pixels' first-mined year in `zones_v2_mdd_full.tif` reproduces `cell_year_v2.csv.gz` to 0.0005 ha (rounding). The block layout in `v2_stats.py:50` (152 cells per row, recomputed from the window) equals the cell grid in `raster_zones.py:218` (152). **The backbone is consistent.** Cell purity is high: 98.1% of the 2014-25 first-time mining in La Pampa cells lies in La Pampa pixels (1.1% in the reserve, 0.4% across the road); 97.5% for the across-the-road cells.

### T1 · Reproduce S1

Every coefficient and p-value matches `output/numbers.csv` to four decimals:

| Zone | 2019-21 | p | 2022-25 | p |
|---|---|---|---|---|
| La Pampa sector | −1.208 | 0.081 | −0.755 | 0.402 |
| Corridor across the road | +0.938 | 0.006 | +1.125 | 0.020 |
| Kotsimba | −0.682 | 0.083 | −0.802 | 0.042 |
| Tambopata reserve | −0.066 | 0.057 | −0.028 | 0.655 |
| Rest of Tambopata BZ | −0.003 | 0.857 | +0.036 | 0.266 |
| Amarakaeri BZ | −0.057 | 0.181 | +0.303 | 0.211 |

Ids `st_main_*`. WCR p: La Pampa 0.058 (`st_wcb_lp_p`), across 0.000 (`st_wcb_across_p`; with 999 draws this means **p < 0.001**, and should be printed that way). Contaminated reference: La Pampa −1.385 (p 0.046, `st_contam_lapampasector_during`).

**Small error:** `st_n_clusters` = 161 is counted on the full 2010-25 panel (`v2_stats.py:247`). The regression sample has **136** blocks; the text "La Pampa covers 14 of the 161 clusters" (`explainer_content.md:560`) should say 136.

### T2 · The reference cells: the DiD is a before/after

| Group | Cells | 2014-18 | 2019-21 | 2022-25 | Own change 2019-21 | DiD |
|---|---|---|---|---|---|---|
| La Pampa | 572 | 2.470 | 1.268 | 1.729 | −1.202 | **−1.208** |
| Across the road | 395 | 0.194 | 1.138 | 1.333 | +0.945 | +0.938 |
| Kotsimba | 353 | 1.384 | 0.709 | 0.596 | −0.675 | −0.682 |
| Reference | 4,856 | 0.003 | 0.009 | 0.017 | +0.007 | n/a |

(ha of first-time mining per cell-year)

- The reference cells are "Rest of Madre de Dios" (2,606), "Other reserves and parks" (2,173), other buffer zones (60) and the Bahuaja-Sonene BZ (17).
- **99.56%** of reference cell-years are zero; only **68 of 4,856** reference cells have any first-time mining in 2014-25.
- The regression coefficient equals own change minus reference change exactly (saturated, balanced panel). The reference moves by +0.007 ha per cell-year, so La Pampa's DiD (−1.208) is its own before/after (−1.202).

**So the "clean" comparison solved the contamination problem by choosing cells where mining almost never happens.** It does not tell us what La Pampa would have done; it tells us that the rest of the forest stayed unmined. The p-value then measures only how noisy La Pampa's own change is across blocks. Audit lead 2 reproduced.

### T3 · PPML: the coefficient is the reference's growth

PPML drops every cell whose outcome is zero in all years. It uses **896 of 8,744 cells, and only 68 reference cells**. Those 68 cells together went from 12.5 to 45.6 ha/yr (log change +1.29).

| Zone | Own log change 2019-21 vs 2014-18 | − reference | = | PPML (`st_ppml_*_during`) |
|---|---|---|---|---|
| La Pampa | −0.67 | +1.29 | −1.96 | −1.96 |
| Across the road | +1.77 | +1.29 | +0.48 | +0.48 |
| Amarakaeri BZ | −0.65 | +1.29 | −1.94 | −1.94 |
| Rest of Tambopata BZ | +0.05 | +1.29 | −1.24 | −1.24 |
| Kotsimba | −0.67 | +1.29 | −1.96 | −1.96 |
| Tambopata reserve | −1.15 | +1.29 | −2.44 | −2.44 |

The decomposition is exact to two decimals. **Every focal zone gets a large negative PPML coefficient because 68 sparse reference cells grew by a factor of 3.6.** La Pampa's own proportional fall is −0.67 log points (−49%). With the contaminated reference, PPML gives −1.17 for La Pampa and +1.27 across the road, so the sign of the "across" result depends on which 68-cell or corridor reference is used. Audit lead 3 reproduced. The robustness claim at `explainer_content.md:571` ("Poisson −1.96 log points, p < 0.01") should be removed or restated as "La Pampa's own first-time mining fell by about half (−0.67 log points)".

### T4 · Is "across the road" special? Placebo strips and sliding windows

**T4a · Strips of corridor cells** (mean first-time ha per cell-year):

| Strip | Cells | 2014-18 | 2019-21 | 2022-25 | Change 2019-21 |
|---|---|---|---|---|---|
| Across the road (zone 5) | 395 | 0.19 | 1.14 | 1.33 | **+0.94** |
| Corridor 0-10 km north, **east** of La Pampa (lon > −69.80) | 222 | 0.54 | 1.43 | 2.09 | **+0.89** |
| Corridor 0-10 km north, west of La Pampa | 333 | 0.08 | 0.15 | 0.30 | +0.08 |
| Corridor > 10 km north, all longitudes | 3,667 | 0.58 | 0.96 | 1.87 | +0.38 |
| Corridor > 10 km north, La Pampa longitudes | 950 | 0.43 | 1.07 | 2.75 | +0.64 |

**T4b · Spatial permutation.** I slid a 0.35° window (the width of La Pampa) along the road in 0.05° steps and ran the S1 regression for corridor cells 0-10 km north of the road in each window, against the same clean reference (21 windows with ≥ 30 cells).

| Window (lon) | 2019-21 | p |
|---|---|---|
| −70.65…−70.30 (west) | +0.10 | 0.19 |
| −70.50…−70.15 (west, touching LP) | +0.07 | 0.08 |
| −70.15…−69.80 (**real**) | **+0.93** | 0.006 |
| −70.10…−69.75 | +1.03 | 0.011 |
| −69.80…−69.45 (east, no overlap) | +0.89 | < 0.001 |
| −69.75…−69.40 (east, no overlap) | +1.21 | < 0.001 |
| −69.70…−69.35 (east, no overlap) | +1.15 | < 0.001 |
| −69.65…−69.30 (east, no overlap) | +1.02 | < 0.001 |

The real window ranks **7 of 21** (all windows) and **4 of 9** against the windows that do not overlap it. The non-overlapping windows to the **east** (towards Laberinto and Puerto Maldonado) rose as much or more, with smaller p-values; the windows to the west did not rise. Audit lead 4 reproduced.

**What this means.** "Across the road from La Pampa" is not where the corridor's 2019-21 growth was unusual; the whole eastern corridor strip along the road grew. What is distinctive is the *relative* jump: across the road started from a much lower base (0.19 vs 0.54 east), so in proportional terms it rose ~6-fold against ~2.6-fold to the east. The displacement reading ("miners crossed the road") is consistent with this, but so is a corridor-wide boom along the highway that would have happened anyway. Description only.

**T4c · Fake La Pampas.** The same sliding window over Tambopata buffer-zone cells (zones 7-8) gives La Pampa-sized falls for every window that overlaps La Pampa (−0.86 to −1.51; the window −70.25…−69.90 is larger than the real one) and **zero for every non-overlapping window**, because the rest of the buffer zone has no mining (2014-18 mean 0.00-0.03 ha per cell-year). There is no mined area in the buffer zone outside La Pampa to permute over. A spatial randomization test for La Pampa is therefore not possible with this design.

### T5 · Event studies

| Year | 2010 | 2011 | 2012 | 2013 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| La Pampa | −2.14 | +0.05 | −1.01 | +0.04 | **+0.13** | −1.90 | −1.86 | −1.59 | −0.54 | −0.89 | −0.01 |
| p | 0.001 | 0.97 | 0.11 | 0.94 | 0.87 | 0.007 | 0.009 | 0.038 | 0.51 | 0.39 | 0.99 |
| Across the road | +1.36 | +0.63 | +0.11 | +0.51 | +0.59 | +0.79 | +1.43 | +1.67 | +1.56 | +0.74 | +0.53 |
| p | 0.19 | 0.08 | 0.31 | 0.06 | 0.004 | 0.021 | 0.005 | 0.001 | 0.046 | 0.07 | 0.05 |

(ha per cell-year vs the pooled 2014-18 mean; ids `st_event_lp_*`, `st_event_across_*`)

- La Pampa joint pre-trend test: **p = 0.0055** (`st_event_lp_pretrend_p`), driven by 2010 (−2.14) and 2012 (−1.01): La Pampa was still ramping up before 2014.
- **2019 is +0.13 (p 0.87).** La Pampa's fall starts in 2020, with COVID, and has faded by 2023-25 (X3). Across the road rises from 2019 (+0.59, p 0.004) and its pre-trend test passes (p = 0.235, `st_event_across_pretrend_p`).
- Audit lead 5 reproduced.

### T6 · Depletion: the session's key new test (D-S1-5)

First-time mining is absorbing. La Pampa cells were on average **20.7% mined by 2018** (7.7% in 2013, 24.7% in 2021), and **113 of 572 cells were more than half mined in 2018**. Across the road: 8.3% in 2018.

**(a) Hazard outcome** = first-time ha / unmined ha at t−1 (%), same S1 specification:

| Version | La Pampa 2019-21 | p | Across 2019-21 | p |
|---|---|---|---|---|
| Hectares (S1 main, for reference) | −1.21 ha | 0.081 | +0.94 ha | 0.006 |
| Hazard, cell-level, unweighted | −0.38 pts | 0.71 | +2.11 pts | 0.014 |
| Hazard, weighted by unmined area | +0.50 pts | 0.44 | +1.21 pts | 0.010 |
| Hazard, cells never fully mined (balanced) | −0.84 pts | 0.23 | | |
| Hectares + 2018-depletion bin × year FE | −0.20 ha | 0.53 | +1.22 ha | 0.002 |
| Hectares + lagged cumulative mined share (bad control) | +0.08 ha | 0.81 | | |

**(b) Zone-level hazard** (sum of first-time ha / sum of unmined ha at t−1):

| Zone | 2014-18 | 2019-21 | 2022-25 | 2019-21 / 2014-18 |
|---|---|---|---|---|
| La Pampa | 2.98% | 1.73% | 2.49% | **0.58** |
| Across the road | 0.22% | 1.32% | 1.64% | 5.98 |
| Kotsimba | 1.57% | 0.85% | 0.74% | 0.54 |
| Reference | 0.003% | 0.010% | 0.018% | 3.6 |

La Pampa's yearly hazard: 2014 3.40%, 2015 2.49, 2016 1.19, 2017 3.93, 2018 3.94, **2019 3.45**, 2020 0.80, 2021 0.87, 2022 1.26, 2023 2.77, 2024 2.31, 2025 3.69. The 2019 hazard is at its pre-period level; the fall is 2020-22, and by 2025 it is back to 2017-18 levels.

**(c) Inside La Pampa, by how used-up each cell was in 2018** (terciles of cells with some mining by 2018):

| Cells (2018 mined share) | Cells | ha 2014-18 | ha 2019-21 | Change | Hazard 2014-18 | Hazard 2019-21 | Change |
|---|---|---|---|---|---|---|---|
| none mined by 2018 | 304 | 0.00 | 0.21 | up from 0 | 0.00% | 0.24% | up from 0 |
| low (mean 8%) | 90 | 1.14 | 2.58 | +125% | 1.27% | 3.35% | +163% |
| mid (mean 40%) | 89 | 5.02 | 3.78 | −25% | 6.42% | 8.50% | +32% |
| high (mean 85%) | 89 | 9.69 | 1.03 | **−89%** | 24.55% | 10.22% | −58% |

**What this means.**
1. At the level of the whole zone, depletion explains little: the unmined pool shrank only a few points, and La Pampa's hazard still fell by 42% (hectares −49%). So "La Pampa slowed down in 2019-21" survives depletion as a **zone-level description**.
2. At the level of the cell, it does not. Once each cell is compared with itself on the scale of its remaining land, or with comparison cells equally used up, La Pampa's 2019-21 coefficient is small and not distinguishable from zero (−0.38 to +0.50 pts; −0.20 ha with depletion bins).
3. The fall is concentrated in La Pampa's **mostly-mined core** (85% mined by 2018: −89% in hectares). Less-mined La Pampa cells **rose** in 2019-21 (+125%), and cells with no mining by 2018 started to be mined. Mining moved *within* La Pampa from the used-up core to its edges.
4. Two readings fit. (i) Depletion: the core was exhausted and miners moved outward, as they would have anyway. (ii) Enforcement: Mercurio's camps and checkpoints targeted the core (the main mining camps), so the core stopped and miners moved to the margins. The cell data cannot separate them, because every cell that was heavily mined in 2018 is a La Pampa, Kotsimba or across-the-road cell: only **24 reference cells** are in any depletion bin above zero (14 at 0-5%, 5 at 5-20%, 5 above 20%), so the bin × year control rests on very few comparison cells.

### T7 · Clustering and spatial correlation

| Dependence model | Clusters (La Pampa in) | La Pampa 2019-21 p | Across 2019-21 p |
|---|---|---|---|
| CRV1, 10-km blocks (main) | 136 (14) | 0.081 | 0.006 |
| CRV1, 20-km blocks | 42 (6) | 0.088 | 0.012 |
| CRV1, 30-km blocks | 23 (6) | 0.051 | 0.002 |
| CRV1, 50-km blocks | 10 (1) | 0.000 (degenerate: one treated cluster) | 0.040 |
| WCR, 10-km blocks | 136 | 0.058 | < 0.001 |
| WCR, 20-km blocks | 42 | 0.002 | 0.006 |
| WCR, 30-km blocks | 23 | 0.021 | 0.219 |
| Conley, Bartlett, 10 km | n/a | 0.067 | 0.011 |
| Conley, Bartlett, 25 km | n/a | 0.016 | 0.002 |
| Conley, Bartlett, 50 km | n/a | < 0.001 | < 0.001 |

Audit lead 7 reproduced (0.081 / 0.088 / 0.051 / degenerate at 50 km).

- The p-values move between 0.002 and 0.088 for La Pampa, and between < 0.001 and 0.22 for across the road, depending only on how dependence is modelled. **No dependence model is clearly right**, and the answer is not monotone in the cluster size.
- Conley errors **shrink** as the cutoff grows. That means cross-products of nearby cells' scores are on balance negative: La Pampa cells falling next to corridor cells rising (displacement shows up as negative spatial correlation). In that case larger windows are not "more conservative".
- The uniform-kernel Conley variance is not positive semi-definite in two dimensions here (it returned negative variances at 25 and 50 km); only Bartlett is reported.
- With 6 treated clusters at 20-30 km, WCR is in the region where MacKinnon and Webb (2017) find it unreliable.
- **Verdict:** sampling-based p-values for La Pampa are not informative beyond "borderline". The shock is one contiguous operation; the honest unit of inference is the zone, where we have one treated unit (S2-S4).

### T8 · Road gradient

Bands (cells): S 10-30 (1,017), S 5-10 (253), S 0-5 (253), N 0-5 (255), N 5-10 (255), N 10-20 (509), N 20-30 (510).

- **The reference band "S 10-30" is not a clean reference:** of its 1,017 cells, 176 are La Pampa, 147 Kotsimba, 318 the Tambopata reserve, 351 other reserves and 25 rest of the Tambopata BZ. La Pampa and Kotsimba are the zones that fell most.
- **Out-of-range cells:** `pd.cut` returns NaN outside ±30 km (`v2_stats.py:146-148`), so **1,760 of the 4,812** gradient cells (|road| > 30 km) get no band dummy and silently join the omitted reference. They are rest of Madre de Dios (888), other reserves (501), rest of the mining corridor (309) and other communities (62): the reference category silently includes 309 corridor cells far north, a displacement target.
- Fixing both barely matters for the headline: N 10-20 km 2022-25 = +2.87 (published, `st_grad_b_N10_20_after`) → +3.07 with |road| ≤ 30 only → +2.96 when La Pampa and Kotsimba cells are also removed from the reference band. N 0-5 2019-21: +0.78 → +0.93 → +0.81.
- Audit lead 8 reproduced (reference band contains La Pampa and Kotsimba; out-of-range cells in the omitted category). The gradient is a one-dimensional ring design (Butts 2023), but rings are measured from the road, not from the treated area, so it describes *where* mining grew, not spillover from the treated zone.

### T9 · Gold control, GLAD mask, documentation

**Gold × year.** 82.4% of all cells and 80.9% of reference cells are "high gold" (`v2_stats.py:57`; the broad definition includes the Madre de Dios Formation upper member, `raster_gold.py:27`). The control splits the sample into one big bin and two small ones, so it can hardly change anything: La Pampa −1.198 (`st_gold_lapampasector_during`) vs −1.208. Audit lead 7 (gold) reproduced. It should not be cited as controlling for gold endowment.

**GLAD look-ahead** (`glad_alerts.py:71`, `mined = first[zr, zc] > 0`; the plan cites ~67). An alert is "mining-related" if the pixel is mapped as mining in **any** year 1985-2025, including years after the alert. Composition of that mask:

| Zone | first mined ≤ 2016 | 2017-18 | 2019-21 | 2022-25 |
|---|---|---|---|---|
| La Pampa | 44% | 21% | 12% | 23% |
| Across the road | 44% | 3% | 21% | 33% |
| Rest of corridor | 42% | 6% | 15% | 38% |

A third of the across-the-road mask was first mined in 2022-25. So a 2017-18 alert there counts as "mining-related" if the land was mined years later, while a 2024 alert has only one or two years to be confirmed. The lead window is unequal across years, which inflates early alerts in late-mined zones and deflates the latest quarters. A time-consistent mask (alert counted if the pixel is first mined in the alert year or the next) needs the GLAD tiles, which are not in this checkout. Audit lead 9 confirmed in the code; size of the bias not testable here.

**Documentation drift** (X10):
- `v2_stats.py:12-14` says the reference cells are "mostly the rest of the mining corridor and communities", but the main (clean) spec drops exactly those (`v2_stats.py:39, 100-101`). They are reserves and unmined forest (T2).
- `v2_stats.py:19` describes an "S4" test of the Amarakaeri BZ "2020-21 vs pre" with a "Mercurio extension in 2020"; no such test exists (Amarakaeri is one of the S1 focal zones with the standard periods), and the 2020 extension is not sourced in the code.
- `raster_zones.py:113-114` says distances are "equal-area metres via ESRI:102033"; the code uses a latitude offset × 110.574 km (S1 lead 6).
- `st_wcb_across_p` = 0.0 is printed as "p = 0.00" (`explainer_content.md:569`); with 999 draws it is p < 0.001.
- `st_n_clusters` (161) is not the regression's cluster count (136) (T1).

### T10 · Multiple testing

The S1 main family has 12 coefficients (6 zones × 2 periods). Holm-adjusted p-values:

| Coefficient | p | Holm p |
|---|---|---|
| Across the road 2019-21 | 0.006 | **0.069** |
| Across the road 2022-25 | 0.020 | 0.217 |
| Kotsimba 2022-25 | 0.042 | 0.420 |
| Reserve 2019-21 | 0.057 | 0.513 |
| La Pampa 2019-21 | 0.081 | 0.651 |
| Kotsimba 2019-21 | 0.083 | 0.651 |
| (other six) | 0.18-0.86 | 1.000 |

`v2_stats.py` registers **86 p-values** in `output/numbers.csv` (5 S1 specs × 12, 2 WCR, 2 pre-trend tests, 10 event-study years, 12 gradient terms); 43 are below 0.05. After Holm within the main family, nothing is below 0.05; across the road 2019-21 is the only coefficient below 0.10. A Romano-Wolf step-down using the joint wild bootstrap would be less conservative (the tests are correlated) and is the right next step if any cell p-value stays in the brief. Audit lead 10 reproduced.

### Tests not possible here

- **Time-consistent GLAD mask** (needs `data_raw/glad_alerts/` tiles, git-ignored).
- **Re-cutting cells or zones** (e.g. 500-m or 2-km cells, moving the La Pampa window at pixel level, varying `ACROSS_KM`): needs the 41 MapBiomas rasters. The cell-level sliding windows in T4 are the closest available substitute.
- **Flicker-robust first-time mining** (mined in t and t+1): needs the yearly rasters (the full tif keeps only the first year).

## 8. Assumption check

| Assumption | Verdict | Evidence |
|---|---|---|
| Parallel trends (cells) | **Fails for La Pampa**, passes for across the road | Pre-trend p 0.0055 vs 0.235 (T5) |
| Comparable exposure | **Fails** | 99.56% zeros, 68 of 4,856 reference cells ever mine (T2); PPML identified by those 68 (T3) |
| No spillover | Satisfied for the clean reference by construction (it holds almost no mining), at the cost of comparability | T2 |
| No depletion | **Fails at cell level** | La Pampa core 85% mined by 2018, fell 89%; less-mined cells rose; hazard specs ≈ 0 (T6) |
| Correct dependence model | **Unknown**; p moves 0.002-0.09 with the model | T7 |
| Enough treated clusters | Borderline at 10 km (14), fails at 20-50 km (6, 6, 1) | T7 |
| Zones not chosen on the outcome | **Fails** for La Pampa (window drawn from the outcome map); "across" not distinctive among strips | `raster_zones.py:21-22`; T4 |

## 9. Weaknesses, ranked

1. **The comparison is empty.** The clean reference cells almost never have mining, so the cell DiD equals La Pampa's own before/after (−1.202 of −1.208) and the PPML equals a ratio driven by 68 sparse cells. The cell panel adds standard errors, not a counterfactual.
2. **Depletion.** In hazard terms, or against equally used-up cells, La Pampa's cell-level fall disappears; the fall is the collapse of an 85%-mined core while the less-mined edges rose (T6).
3. **Inference depends on the dependence model.** p from 0.002 to 0.09 for La Pampa; Conley shows negative spatial correlation (displacement), so bigger clusters are not safer.
4. **Pre-trends fail and the fall starts in 2020** (2019 = +0.13), so the timing points at COVID as much as at Mercurio (X3).
5. **"Across the road" is not unusual among corridor strips.** The eastern corridor along the road rose as much (T4); only the jump relative to its low base is distinctive.
6. **PPML "robustness" is wrong as stated** (`explainer_content.md:571`): every focal zone gets ≈ −2 log points from the reference alone.
7. **Multiple testing:** 86 p-values, none below 0.05 after Holm in the main family.
8. Smaller: gradient reference band contains La Pampa and Kotsimba and the out-of-range cells; gold control nearly empty; GLAD mask looks ahead; cluster count and docstrings out of date.

## 10. Proposed decisions

| # | Decision | Recommendation |
|---|---|---|
| D-S8-1 | What the cell panel is for | Keep it as **description of where mining moved** (La Pampa core vs edges, across the road, the depth gradient), not as a test of Mercurio's effect. Stop presenting its p-values as the "standard errors" the zone designs lack. |
| D-S8-2 | Wording of the La Pampa cell result | "Per 1-km cell, first-time mining in La Pampa fell from 2.47 to 1.27 ha a year in 2019-21. Outside La Pampa and the corridor almost no cell is mined, so this is a before/after, not a comparison." Drop "relative to clean comparison cells" as if it were a control. |
| D-S8-3 | Depletion (closes D-S1-5) | Add the zone-level hazard (La Pampa ×0.58, across ×6.0) and the within-La Pampa tercile table to the walkthrough. State that the fall is concentrated in the mostly-mined core and that at cell level it does not survive a depletion adjustment. Add an at-risk version to `v2_stats.py` (outcome new_land / unmined area at t−1, and 2018-depletion bins × year) and register it. |
| D-S8-4 | PPML | Remove "robust to Poisson" at `explainer_content.md:571`, or replace it with La Pampa's own log change (−0.67) and say the PPML coefficient is driven by 68 reference cells. |
| D-S8-5 | Inference | Report the p-value range across dependence models (0.002-0.09 La Pampa; < 0.001-0.22 across) instead of one p. Print WCR 0 as "< 0.001". Fix `st_n_clusters` to the regression sample (136). |
| D-S8-6 | Across the road | Report the sliding-window result: the eastern corridor along the road rose as much; across the road's rise is distinctive only relative to its low base (×6 vs ×2.6). Keep the displacement reading as one of two explanations. |
| D-S8-7 | Gradient | Restrict to |road| ≤ 30 km and drop La Pampa / Kotsimba cells from the reference band (headline changes from +2.87 to +2.96). Low priority. |
| D-S8-8 | GLAD | Replace `first > 0` with a fixed lead window (first-mined year in [alert year, alert year + 1]) when the tiles are available; until then add a sentence on the unequal look-ahead. |
| D-S8-9 | Multiple testing | If any cell p-value stays in the brief, report the Holm (or Romano-Wolf) adjusted value; across the road 2019-21 is Holm p = 0.07. |
| D-S8-10 | Docstrings | Fix `v2_stats.py:12-19` (reference description, remove S4) and `raster_zones.py:113-114`. |

## 11. Verdict

The raster backbone is sound: the cell outcome rebuilds exactly from the pixels, cells are 97-98% pure, and the regressions reproduce `output/numbers.csv` to four decimals.

As a **causal design** the cell panel adds little. Its comparison cells are unmined forest, so the La Pampa coefficient is a before/after. Its pre-trends fail. Its p-values swing with the dependence model. Once depletion is accounted for, the La Pampa cell-level fall disappears: it is the collapse of an already 85%-mined core, while La Pampa's less-mined edges grew.

As **description** it is valuable: it shows *where* mining went in 2019-21 (out of La Pampa's core, into its edges, across the road and along the whole eastern corridor, then deeper north after 2022).

Label: **description**.

**The brief may say:** "Per 1-km cell, first-time mining in La Pampa halved in 2019-21 (2.47 → 1.27 ha per cell-year), almost entirely in its already mostly-mined core, while it rose six-fold in the corridor across the road (0.19 → 1.14) [D]."

**The brief must not say:** "statistically significant" for any cell result; "relative to clean comparison cells" as if those cells were a counterfactual; "robust to Poisson"; "robust to gold endowment"; or that the cell panel confirms the causal claim.

## References

- Butts, K. (2023). Difference-in-differences with spatial spillovers. arXiv working paper 2105.03737.
- Cameron, A. C., Gelbach, J. B. and Miller, D. L. (2008). Bootstrap-based improvements for inference with clustered errors. *Review of Economics and Statistics* 90(3).
- Cameron, A. C. and Miller, D. L. (2015). A practitioner's guide to cluster-robust inference. *Journal of Human Resources* 50(2).
- Conley, T. G. (1999). GMM estimation with cross sectional dependence. *Journal of Econometrics* 92(1).
- Conley, T. G. and Taber, C. R. (2011). Inference with "difference in differences" with a small number of policy changes. *Review of Economics and Statistics* 93(1).
- Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics* 6(2).
- MacKinnon, J. G. and Webb, M. D. (2017). Wild bootstrap inference for wildly different cluster sizes. *Journal of Applied Econometrics* 32(2).
- MacKinnon, J. G. and Webb, M. D. (2018). The wild bootstrap for few (treated) clusters. *Econometrics Journal* 21(2).
- Romano, J. P. and Wolf, M. (2005). Stepwise multiple testing as formalized data snooping. *Econometrica* 73(4).
- Santos Silva, J. M. C. and Tenreyro, S. (2006). The log of gravity. *Review of Economics and Statistics* 88(4).
