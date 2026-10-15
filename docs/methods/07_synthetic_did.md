# S7 · Synthetic difference in differences (attempt A6)

*Method card 7 of the causal review (plan: `docs/causal_review_plan.md`). Code under review: `code/peru_sdid.py` (own implementation of Arkhangelsky et al. 2021), compared with `code/peru_models.py` (ladder) and `code/peru_synth.py` (S6). Test script: `code/review/s7_sdid_checks.py` (read-only, about 1 minute).*

---

## 1. In one sentence

Synthetic DiD reweights both the comparison units (so their pre-treatment *trend* matches the treated unit's) and the pre-treatment years (so the baseline years resemble the post period), then takes a difference in differences on the reweighted data.

## 2. Simple version

Plain DiD compares the treated unit's change with the *average* change of all comparison units, and uses *all* pre-years equally as the baseline. Synthetic control (S6) picks a weighted mix of comparison units that copies the treated unit's *level*, and uses no baseline at all.

Synthetic DiD takes a middle path:
- **Unit weights** pick comparison units whose ups and downs before treatment look like the treated unit's ups and downs. A free constant absorbs the difference in level, so a small comparison unit can still be useful if it moves the same way.
- **Time weights** pick the pre-years that look most like the post-years *for the comparison units*. If the comparison units' 2014 resembles their 2019-21, then 2014 becomes the baseline year.
- The estimate is then a DiD: (treated after − treated in the weighted baseline years) − (weighted comparisons after − weighted comparisons in the weighted baseline years).

The method is designed for panels with many units and many pre-periods, where both sets of weights are estimated from a lot of information. With 14 comparison zones, five pre-years and a treated zone that mined 4.7 times more than the largest comparison (Amarakaeri) and 30 times more than the next largest (Allpahuayo Mishana) in 2014-18, the weights have very little to work with. Our tests show what happens then: the time weights put 86% on a single year, and the estimate becomes, in practice, "Tambopata in 2019-21 minus Tambopata in 2014".

## 3. When to use it, and when not

**Use it when:**
- treatment is a block (some units treated from one date on);
- there are enough comparison units that some combination tracks the treated unit's pre-period *movements*;
- there are enough pre-periods for the time weights to be informative;
- the treated unit is not wildly more volatile than the controls (for placebo inference).

**Avoid it, or read it with care, when:**
- the comparison units barely move, so unit weights cannot match the treated unit's dynamics and the "synthetic trend" is flat;
- there are few pre-periods, so time weights can collapse onto one year and the estimate inherits that year's noise;
- there is one treated unit and it is far larger or noisier than the controls: the placebo variance then describes the controls, not the treated unit.

## 4. Assumptions

| Assumption | In words | Formally |
|---|---|---|
| **Latent factor model** | Untreated outcomes = unit effect + time effect + interactive factors + noise | Y_it(0) = α_i + β_t + Γ_i'Υ_t + ε_it (Arkhangelsky et al. 2021, eq. 4.1) |
| **Weights balance the factors** | The weighted comparisons track the treated unit's factor loadings (unit weights), and the weighted pre-years track the post-period factors (time weights) | Σ ω_i Γ_i ≈ Γ_tr up to a constant; Σ λ_t Υ_t ≈ Ῡ_post up to a constant |
| **No interference** | Comparison units are not affected by the treatment | Y_it = Y_it(0) for controls |
| **No anticipation** | No change before treatment because of it | Y_tr,t = Y_tr,t(0), t ≤ T_pre |
| **Block assignment** | One treatment date, treatment absorbing | W_it = 1[i treated, t > T_pre] |
| **Exchangeable noise (placebo variance)** | The treated unit's noise has the same distribution as the controls' | ε_tr ~ ε_co, so the variance of placebo estimates is the variance of τ̂ |

## 5. The maths

### 5.1 Master's level

N_co control units, N_tr treated, T_pre pre-periods, T_post post-periods.

**Unit weights.** With the regularisation level

  ζ = (N_tr · T_post)^{1/4} · σ̂, where σ̂ = standard deviation of the controls' one-period first differences Y_i,t+1 − Y_it in the pre-period,

solve

  (ω̂_0, ω̂) = argmin over ω_0 ∈ ℝ, ω ∈ simplex of Σ_{t ≤ T_pre} (ω_0 + Σ_{i co} ω_i Y_it − Ȳ_tr,t)² + ζ² T_pre ‖ω‖².

The intercept ω_0 lets the weighted controls differ in level from the treated unit. The ridge term spreads weight over several controls.

**Time weights.**

  (λ̂_0, λ̂) = argmin over λ_0 ∈ ℝ, λ ∈ simplex of Σ_{i co} (λ_0 + Σ_{t ≤ T_pre} λ_t Y_it − Ȳ_i,post)²

(with a negligible ridge term, ζ_λ = 10⁻⁶ σ̂, in the authors' software).

**Estimate.** In the block design, the weighted two-way fixed-effects regression of Algorithm 1 reduces to

  τ̂ = [Ȳ_tr,post − Σ_t λ̂_t Y_tr,t] − Σ_{i co} ω̂_i [Ȳ_i,post − Σ_t λ̂_t Y_it].

**How it nests the others** (Arkhangelsky et al. 2021, section 2):
- **DiD:** ω_i = 1/N_co and λ_t = 1/T_pre, with unit and time fixed effects.
- **SC:** ω = synthetic-control weights (no intercept, no penalty), no time weights and no unit fixed effects; τ̂ = Ȳ_tr,post − Σ ω_i Ȳ_i,post.
- **SDID:** both weights estimated, both fixed effects kept.

### 5.2 PhD level

**Why the intercept and the time weights matter.** The intercept makes the unit weights match *deviations* from unit means, so SDID tolerates level differences that break SC (S6). The time weights make the baseline local in time: if the controls' recent past is more like the post-period than their distant past, recent years count more. Both sets of weights are chosen to remove bias from the factor structure Γ_i'Υ_t; the double weighting gives a "doubly robust" flavour (Arkhangelsky et al. 2021, section 4): the estimator is consistent if either set of weights balances the factors well enough.

**Asymptotics.** The paper's results take N_co and T_pre large (with conditions on their rates and on the noise), and the oracle weights well-defined. With N_co = 14 and T_pre = 5 none of that is close.

**The ζ choice.** ζ is calibrated to the size of a typical one-period shock in the controls. If the controls are almost flat, σ̂ is small, and ζ is small relative to the treated unit's scale; the unit weights then try hard to fit the treated unit's pre-period path and can still fail if no combination moves enough.

**Inference with one treated unit.** The paper offers three variance estimators. The bootstrap (Algorithm 2) and jackknife (Algorithm 3) need several treated units; with N_tr = 1 the paper uses the **placebo variance** (Algorithm 4): assign the treatment to controls, recompute τ̂, and use the variance of those placebo estimates. Its validity requires the noise of the treated unit to be exchangeable with that of the controls (homoskedasticity across units). If the treated unit's outcome is far more volatile, the placebo variance understates the uncertainty of τ̂, by as much as the ratio of the noise scales.

**Time-weight collapse.** The time-weight problem has T_pre unknowns and N_co equations. With few pre-years and controls whose cross-sectional pattern in one pre-year happens to resemble the post-period pattern, the solution sits on a vertex of the simplex: (almost) all weight on one year. The estimate then uses a single baseline year for the treated unit. That year is chosen without looking at the treated unit (a design virtue), but the treated unit's value in that year can be anywhere in its own distribution. When the treated unit's year-to-year swings are large, τ̂ inherits them.

## 6. Our example

### 6.1 Panel and code path

| Element | As coded | Where |
|---|---|---|
| Panel | 15 Peruvian buffer zones with non-zero additions 2014-18 (pool B), net additions in ha | `peru_sdid.py:92-98`, `peru_models.py:46-48` |
| Treated | Tambopata buffer zone, from 2019 | `peru_models.py:29` |
| Pre / post | 2014-18; post blocks 2019-21 ("during") and 2022-25 ("after"), each estimated separately | `peru_sdid.py:34-35` |
| Scaled panel | outcome ÷ own 2014-18 signed mean; zones with mean > 10 ha (7) | `peru_sdid.py:93-98` |
| σ̂, ζ | sd of controls' first differences (ddof = 1), ζ = (1 · T_post)^{1/4} σ̂ | `peru_sdid.py:75-76` |
| Unit weights | simplex, intercept, penalty ζ² T_pre | `peru_sdid.py:77` |
| Time weights | simplex, intercept, penalty (10⁻⁶ σ̂)² N_co | `peru_sdid.py:78` |
| Solver | FISTA on the simplex with the intercept profiled out by demeaning | `peru_sdid.py:38-60` |
| τ | closed form above | `peru_sdid.py:79` |
| DiD / SC variants | uniform weights / SC weights without intercept and λ = 0 | `peru_sdid.py:70-73` |
| Check | uniform-weight τ asserted equal to M1 and M4 | `peru_sdid.py:99-104` |
| Inference | each control "treated", Tambopata removed; rank (1 = most negative), p = rank/n, "placebo SE" = sd of placebo τ | `peru_sdid.py:83-87, 110-112` |
| Sensitivity | pre-period 2011-18 | `peru_sdid.py:115-119` |
| Used in text | `sdid_sdid_ha_during_pre2011` (−684) in `brief_content.md:27`; `sdid_sdid_ha_during` (−1,545) in `explainer_content.md:434, 744, 751`, `methods_content.md:183` | |

### 6.2 Registered results (`output/peru_sdid.csv`)

| Estimator, 2019-21 | ha/yr | Rank of 15 | Placebo SE | Scaled | Rank of 7 |
|---|---|---|---|---|---|
| DiD (uniform) | −1,453.6 (`sdid_did_ha_during`) | 1 | 68.3 | −1.45 | 3 |
| SC | −411.3 (`sdid_sc_ha_during`) | 1 | 153.4 | −1.38 | 3 |
| **SDID** | **−1,545.4** (`sdid_sdid_ha_during`) | **1** | **45.0** | −1.31 | 3 |
| SDID, pre 2011-18 | −684.0 (`sdid_sdid_ha_during_pre2011`) | 1 | 24.1 | −1.28 | 3 |
| SDID, 2022-25 | +136.0 (`sdid_sdid_ha_after`) | 13 | 227.3 | −0.26 | 5 |

## 7. Tests run and results

### T1 · The implementation matches Algorithm 1

I wrote an independent SDID (own FISTA with adaptive restart, same objective as the paper) and compared it with `peru_sdid.sdid`.

| Check | Result |
|---|---|
| τ, ha, 2019-21 | ours −1,545.4263 = repo −1,545.4263 = `sdid_sdid_ha_during` |
| τ, scaled | −1.3107 in all three |
| σ̂, ζ (ha) | 67.26, 88.53 |
| ζ formula | (N_tr T_post)^{1/4} σ̂ with N_tr = 1, T_post = 3: matches the paper |
| Unit penalty ζ² T_pre, time penalty (10⁻⁶σ̂)² N_co, both with intercepts | matches the paper and the authors' `synthdid` defaults |
| σ̂ with ddof = 0 (paper's formula) instead of ddof = 1 (R package's `sd`) | τ −1,545.39: immaterial |
| Unit objective at optimum | 1,547,387.9310 for both solvers; max weight difference 1.2 × 10⁻⁹ (λ: 3 × 10⁻⁹) |
| KKT conditions (simplex optimality) | gradient equal on the support (spread 1.5 × 10⁻⁴), larger off the support (by ≥ 4,200): optimum confirmed |
| DiD special case | −1,453.6357 = `model_m1_during` = `sdid_did_ha_during` |

The implementation is correct. One small difference from the authors' R package: `synthdid` uses Frank-Wolfe with a sparsification step that zeroes small unit weights and re-solves; ours solves the convex problem exactly. That can move weights slightly, not the conclusions below. I did not re-run the referee's SLSQP comparison mentioned in the plan; the KKT check above is a direct proof of optimality.

### T2 · Time weights decide the answer

Post 2019-21, pre-window start varied, end 2018:

| Pre-window | τ (ha/yr) | Rank of 15 | Largest λ | Second λ | λ on 2018 | Tambopata's weighted baseline (ha) | τ with uniform λ |
|---|---|---|---|---|---|---|---|
| 2010-18 | −680 | 1 | **2012: 0.93** | 2018: 0.03 | 0.03 | 834 | −1,210 |
| 2011-18 | −684 | 1 | **2012: 0.93** | 2018: 0.03 | 0.03 | 834 | −1,328 |
| 2012-18 | −685 | 1 | **2012: 0.93** | 2018: 0.03 | 0.03 | 834 | −1,316 |
| 2013-18 | −1,545 | 1 | **2014: 0.86** | 2017: 0.14 | 0 | 1,709 | −1,475 |
| 2014-18 (main) | −1,545 | 1 | **2014: 0.86** | 2017: 0.14 | 0 | 1,709 | −1,473 |

- **The estimate takes two values**, about −680 and about −1,545, depending only on whether 2012 is allowed into the window. Audit lead (1) reproduces: λ = 0.86 on 2014, 0.14 on 2017, 0 on 2018; with 2011-18, 0.93 on 2012; τ changes by a factor of 2.3.
- **Why.** Tambopata's 2019-21 mean is 163 ha. Its single-year values before 2019 range from 707 (2016) to 2,455 (2017), and 743 in 2012. The controls' weighted change is close to zero in every case, so τ ≈ 163 − (Tambopata's value in the selected year). With 2012 as baseline: 163 − 834 ≈ −670; with 2014: 163 − 1,709 ≈ −1,546.
- **The time weights are chosen from controls that hardly mine.** The controls' mean addition is 46.5 ha in 2014, 15.7 in 2018 and 53.8 in 2019-21. The weights pick the year in which these small numbers happen to resemble 2019-21, and then apply that choice to a zone mining 1,500 ha a year.
- **Uniform time weights** (plain DiD baseline, SDID unit weights) give −1,210 to −1,475: closer to M1 and much less sensitive to the window.
- In the scaled panel the time weights are spread (2015: 0.33, 2016: 0.32, 2018: 0.35), because scaled controls move as much as Tambopata.

### T3 · Unit weights do not match Tambopata's trend

| Zone | Weight | Mean addition 2014-18 (ha) | Mean 2019-21 | sd 2014-18 | Departments |
|---|---|---|---|---|---|
| Cordillera Azul | 0.45 | −3.7 | 6.7 | 10.4 | Huánuco, Loreto, San Martín, Ucayali |
| de Junín | 0.25 | 11.7 | 3.7 | 42.4 | Junín, Pasco |
| Amarakaeri | 0.16 | 342.2 | 573.8 | 185.2 | Cusco, Madre de Dios |
| Nor Yauyos-Cochas | 0.09 | 3.8 | 13.7 | 4.1 | Junín, Lima |
| de Lachay | 0.04 | 4.6 | −0.1 | 4.5 | Lima |

- Audit lead (2) reproduces: 0.45 on a zone with a **negative** pre-period mean, 0.25 on an Andean reserve, 0.16 on Amarakaeri. Only 5 zones get more than 1% (`sdid_n_weighted`).
- **New finding: the "trend match" is cosmetic.** The weighted comparison moves between 16 and 103 ha in 2014-18; Tambopata between 707 and 2,455. Their correlation is 0.23. After removing the intercept, the pre-period RMSPE is 554 ha against a Tambopata standard deviation of 561 ha: the weighted comparison explains about 2% of Tambopata's pre-2019 variation.
- So the explainer's "unit weights ... chosen so the weighted zones' pre-2019 trend matches Tambopata's ... which is why it works where plain synthetic control failed" (`explainer_content.md:758`) is not supported. It does not fail in the same way as SC (the intercept removes the level problem), but it does not match the trend either.
- Per X12, the one zone with real mining in the comparison (Amarakaeri, 16%) is mostly legal corridor and native-community land and was partly treated.

### T4 · Leave one comparison zone out

| Dropped zone | τ 2019-21 (ha), pre 2014-18 |
|---|---|
| **Amarakaeri** | **−2,198** |
| de Lachay | −1,561 |
| (11 zones) | −1,551 to −1,509 |
| Bahuaja-Sonene | −1,540 |
| **de Junín** | **−1,440** |
| none (main) | −1,545 |

- Range −2,198 to −1,440. Audit lead (3) reproduces (drop Amarakaeri −2,198; drop Bahuaja −1,540).
- Dropping Amarakaeri moves λ to 0.94 on 2017, Tambopata's highest pre-year (2,455 ha), so τ jumps. Again the swing comes through the time weights.
- With pre 2011-18, leave-one-out ranges from −1,098 to −628 (drop Amarakaeri: −749).
- Across the two windows and all leave-one-outs, SDID spans **−628 to −2,198 ha/yr**.

### T5 · The placebo SE is a scale artefact

| Placebo zone | Placebo τ (ha) | Mean \|addition\| 2014-18 (ha) |
|---|---|---|
| de Junín | −67.7 | 31.1 |
| Allpahuayo Mishana | −31.4 | 52.5 |
| (10 zones) | −9.1 to +44.5 | 0.3 to 12.3 |
| Amarakaeri | +134.7 | 342.2 |

- Placebo SE 45.0 ha (`sdid_sdid_ha_during_se`). The correlation between a zone's \|placebo τ\| and its size is 0.89.
- Exchangeability fails by orders of magnitude. The standard deviation of yearly first differences in 2014-18 is **1,172 ha for Tambopata**, 7.2 ha for the median control and 237 ha for the most volatile (Amarakaeri).
- A placebo-variance "95% interval" would be −1,634 to −1,457. It is meaningless: Tambopata's own estimate moves by 860 ha when the pre-window starts one year earlier (T2). Measured against Tambopata's own pre-period volatility, τ is −1.32 first-difference standard deviations.
- Rank 1 of 15 says Tambopata is the largest zone, not that the effect is unusual (X1). Scaled, every estimator ranks **3 of 7** (τ −1.31; placebos −5.55, −2.24, −1.12, +0.80, +1.32, +2.58). Audit lead (4) reproduces.

### T6 · Placebo in time

SDID with fake start years, five pre-years and three post-years, all before 2019:

| Fake start | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 |
|---|---|---|---|---|---|---|
| τ (ha) | +1,036 | +958 | +1,232 | −346 | −43 | +120 |

- The real −1,545 is below every fake (rank 1 of 7). With three pre-years, the fakes for 2009-16 range from −346 to +1,036.
- But the fakes are not centred on zero either: three of six are around +1,000 ha. SDID's baseline-year noise produces swings of ±1,000 ha with no treatment at all. This matches the 2×2 finding that Tambopata outgrew the comparisons for a decade (S2 T3).

### T7 · Other pools

| Pool | Pre 2014-18: τ, rank | Main weights | Pre 2011-18: τ, rank |
|---|---|---|---|
| Pool B, 15 (main) | −1,545, 1 of 15 | Cordillera Azul 0.45; λ 2014: 0.86 | −684, 1 of 15 |
| Amazon-department zones (8) | −1,446, 1 of 8 | Cordillera Azul 0.38; λ 2014: 1.00 | −1,447, 1 of 8 |
| Without Amarakaeri and Bahuaja (13) | **−2,287**, 1 of 13 | Cordillera Azul 1.00; λ 2017: 1.00 | −940, 1 of 13 |
| Without Amarakaeri (14) | −2,198, 1 of 14 | Cordillera Azul 1.00; λ 2017: 0.94 | −749, 1 of 14 |

- Without the two Madre de Dios neighbours, SDID becomes "Tambopata in 2019-21 minus Tambopata in 2017" (its peak year) relative to one near-zero zone: −2,287.
- The Amazon-only pool is the most stable across windows (−1,446 / −1,447), but its rank is out of 8 (best p = 0.125).

### T8 · Later years, with and without 2023

| Later-years block | τ (ha/yr) | Rank of 15 |
|---|---|---|
| 2022-25 | +136.0 | 13 |
| 2022, 2024, 2025 (no 2023) | **−392.8** | **1** |

- The "gone by 2022-25" reading (`explainer_content.md:752`) depends on 2023. Without 2023 (the MapBiomas-only spike, S1), SDID's later-years estimate is negative and ranks first in hectares, which, as everywhere, is a scale statement.

### Tests not possible here

- SDID on first-time mining by buffer zone: raster accounting covers 12 custom Madre de Dios zones, not the 15 Peruvian buffer zones, and the rasters are git-ignored.
- Comparison with the authors' `synthdid` R package: not run in this session; the KKT test (T1) confirms optimality directly.

## 8. Assumption check

| Assumption | Verdict | Evidence |
|---|---|---|
| Unit weights balance the factors | **Not met** | Weighted comparison explains about 2% of Tambopata's pre-2019 variation; correlation 0.23 (T3) |
| Time weights balance the factors | **Fragile** | 86-100% on one year; τ −680 or −1,545 depending on the window (T2) |
| No interference | **Violated** for the 16% Amarakaeri weight | X12; dropping it gives −2,198 (T4) |
| No anticipation | Unclear | 2017-18 operations are in the pre-window; λ avoids 2018 (0) |
| Large N_co, T_pre | **No** | 14 controls, 5 pre-years |
| Exchangeable noise (placebo SE) | **Fails** | First-difference sd 1,172 ha (Tambopata) vs 7.2 ha (median control) (T5) |
| Placebo in time centred on zero | **No** | Fakes up to +1,232 ha (T6) |

## 9. Weaknesses, ranked

1. **The time weights pick one baseline year, and Tambopata's value in that year sets the answer.** −680 vs −1,545 depending on whether 2012 is in the window; −628 to −2,287 across windows, leave-one-outs and pools (T2, T4, T7).
2. **The unit weights match nothing.** The weighted comparisons are flat; SDID is, in practice, Tambopata's own before/after with a data-chosen baseline year (T3).
3. **The placebo SE (45 ha) and the rank 1 of 15 measure scale, not precision.** Tambopata's own noise is 160 times the median control's (T5). Scaled: rank 3 of 7, for every estimator.
4. **Fake start years produce ±1,000 ha** with no treatment (T6).
5. **Later-years result depends on 2023** (T8).
6. **Text overstates the method.** The explainer says the weights match Tambopata's trend and that SDID "works where SC failed"; the brief quotes the 2011-18 version (−684) next to SC as "both rank 1" (`brief_content.md:27`).

## 10. Proposed decisions

| # | Decision | Recommendation |
|---|---|---|
| D-S7-1 | SDID in the [C] range | **No SDID number becomes an end of the [C] range.** Report SDID as a sensitivity: "Synthetic DiD gives −680 to −1,545 ha/yr depending on which pre-years it selects as baseline [D]". |
| D-S7-2 | Brief line 27 ("synthetic DiD from 2011 −684 ... both rank 1") | Replace with D-S7-1 wording plus "scaled to size, rank 3 of 7". Drop "both rank 1". |
| D-S7-3 | Placebo SE | Stop registering and quoting `*_se` as standard errors; if kept, describe as "spread of placebo estimates among much smaller zones". Never show a ± interval. |
| D-S7-4 | Explainer Attempt 6 (`explainer_content.md:742-760`) | Rewrite: the weights do not match Tambopata's trend (2% of variance); time weights put 86% on 2014; the estimate is Tambopata's 2019-21 minus mainly its 2014; window and leave-one-out range −628 to −2,198. Keep the headline's "ordinary for its size". |
| D-S7-5 | Add a uniform-λ row | Optional: report SDID with uniform time weights (−1,210 to −1,475) to show that the swing comes from λ. |
| D-S7-6 | Later years | Report 2022-25 with and without 2023 (+136, rank 13; −393, rank 1 in ha) as decided for all designs. |
| D-S7-7 | What S6/S7 contribute to the brief's [C] range | Neither SC nor SDID can supply a range end. The lower end "411" must go (S6). If S14 keeps a [C] sentence, its range should come from specifications meeting S14's criterion (pooled 2014-18 baseline, no extrapolated slope or trend; see D-S14-3), with SDID mentioned only as sensitivity. |

## 11. Verdict

The SDID code is a correct implementation of Arkhangelsky et al. (2021, Algorithm 1): ζ, intercepts, penalties and τ match the paper, the solver reaches the optimum, and its DiD special case equals model M1 exactly.

The method does not help here. With 14 almost-flat comparison zones and five pre-years, the unit weights cannot track Tambopata (2% of its pre-period variation), and the time weights collapse onto one year. The estimate becomes Tambopata's 2019-21 level minus its level in the chosen baseline year, which is why it is −1,545 with a 2014-18 window and −684 with a 2011-18 window. The rank 1 of 15 and the 45-ha placebo SE describe Tambopata's size; scaled to size it ranks 3 of 7.

Label: **description**.

**The brief may say:** "Synthetic DiD, which reweights comparison zones and baseline years, gives −680 to −1,545 ha/yr in 2019-21 depending on the baseline years it selects; scaled to size it ranks 3 of 7 [D]."

**The brief must not say:** that SDID matches Tambopata's pre-2019 trend; "rank 1, p = 0.07" as evidence of an effect; a standard error or interval; that SDID "confirms" or "narrows" the causal range; and it must not use −684 or −1,545 as an end of the [C] range.

## References

- Arkhangelsky, D., Athey, S., Hirshberg, D., Imbens, G. and Wager, S. (2021). Synthetic difference-in-differences. *American Economic Review* 111(12).
- Abadie, A., Diamond, A. and Hainmueller, J. (2010). Synthetic control methods for comparative case studies. *Journal of the American Statistical Association* 105(490).
- Doudchenko, N. and Imbens, G. (2016). Balancing, regression, difference-in-differences and synthetic control methods: a synthesis. NBER Working Paper 22791.
- Conley, T. and Taber, C. (2011). Inference with "difference in differences" with a small number of policy changes. *Review of Economics and Statistics* 93(1).
- Beck, A. and Teboulle, M. (2009). A fast iterative shrinkage-thresholding algorithm for linear inverse problems. *SIAM Journal on Imaging Sciences* 2(1).
- Duchi, J., Shalev-Shwartz, S., Singer, Y. and Chandra, T. (2008). Efficient projections onto the l1-ball for learning in high dimensions. *Proceedings of ICML*.
