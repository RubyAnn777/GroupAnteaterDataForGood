# S5 · Context controls and bad controls: K0-K3 (attempt A4)

*Method card 5 of the causal review (plan: `docs/causal_review_plan.md`). Code under review: `code/peru_context_models.py`, the spending series `code/v2_tests.py:175-186` (`mef_series`), and the ladder it builds on, `code/peru_models.py` (card S4). Test script: `code/review/s5_context_checks.py` (read-only, about 3 s).*

---

## 1. In one sentence

Adding a control variable to a DiD only helps if the variable is a cause of the outcome that the treatment did not itself change; a control that the treatment moved (a "bad control") removes part of the effect or adds bias, in a direction you cannot sign without a model.

## 2. Simple version

You want to know whether a new medicine lowers blood pressure. Two candidate controls:

- **Age, measured before the trial.** Older patients have higher blood pressure whatever they take. Controlling for age is fine: the medicine cannot change anyone's age.
- **Number of doctor visits during the trial.** Patients on the medicine were called in more often *because* they were on the medicine. If you "hold visits constant", you compare treated and untreated patients who had the same number of visits, which are no longer comparable groups. You may remove part of the medicine's effect (if visits are how it works) or create a spurious one.

In our case:
- **COVID exposure** looks like age: COVID was not caused by Mercurio. But the way it is measured here lets it soak up Tambopata's own post-2019 fall (§7, U2).
- **Enforcement money** is doctor visits: PP 0128 spending in Madre de Dios jumped 48-fold in 2019 *because of* Mercurio.

## 3. When to use controls, and when not

**Good controls:** determined before treatment, or by forces the treatment cannot touch (world gold price, rainfall), and that affect the outcome differently across units.

**Bad controls:**
- **Mediators:** variables on the causal path (treatment → control → outcome). Controlling for them estimates only the "direct" effect, which is rarely the question.
- **Colliders / outcomes of the treatment:** variables that the treatment and some unobserved factor both move. Conditioning opens a spurious path.
- **Post-treatment versions of good controls:** e.g. a zone's 2020 mining area used to predict its 2021 additions.

**Interacted exposure controls** (exposure_i × common shock_t) are common in panel DiD. They are only as good as two things: the exposure measure must be pre-treatment, and the interaction must not be collinear with the treated unit's own post-period path.

## 4. Assumptions

| Assumption | In words | Formally |
|---|---|---|
| **Pre-treatment covariates** | Controls are not affected by Mercurio | X_it(1) = X_it(0) for all t |
| **Conditional parallel trends** | Given the controls, Tambopata would have moved like the comparison zones | E[Y_Tt(0) − Y_Ts(0) ∣ X] = E[Y_Ct(0) − Y_Cs(0) ∣ X] |
| **Correct functional form** | COVID hit each zone in proportion to its pre-2019 size; money moved the three Madre de Dios zones by the same amount per log-point | Y_it(0) = α_i + γ_t + θ·pre_i·ln g_t + κ·pre_i·1[2020-21] + λ·MdD_i·ln S_t + ε_it |
| **Identification from comparison zones** | κ and λ are learnt from zones and years that tell us about the untreated path | Tambopata's post-period outcomes do not enter κ, λ |
| **No spillover** | The comparison zones' outcomes are not changed by Mercurio | as in S2-S4 |

## 5. The maths

### 5.1 Master's level

**Bad control bias.** Suppose the true model is y = β·D + γ·X + u, and X itself responds to D: X = π·D + v. Regressing y on D alone gives the **total** effect β + γ·π. Regressing y on D and X gives β, the part of the effect that does not run through X. If the question is "what did Mercurio do", the total effect is the target, and controlling for X is wrong. Worse, if X is also driven by an unobserved factor that affects y (v correlated with u), the coefficient on D is biased in an unknown direction (Angrist and Pischke 2009, section 3.2.3).

**Dose-response.** If treatment comes in amounts S_t (money), a dose-response slope asks whether more money goes with a larger effect. It is only informative if the dose varies for reasons unrelated to the outcome. When the dose is set in response to the outcome (money follows mining, or money is cut when mining has fallen), the slope mixes both directions.

### 5.2 PhD level

**Within-bin identification (FWL again).** With binned treatment dummies (one dummy for 2019-21), any regressor that varies inside 2019-21 for Tambopata is identified partly from Tambopata's post-treatment path. Here pre_i·1[2020-21] equals Tambopata's pre mean (1,594) in 2020-21 and 0 in 2019. Inside the treated bin, it separates 2019 from 2020-21 for the treated unit, i.e. it fits Tambopata's own 2019 → 2021 decline. Saturating the treated unit's post years removes this channel; the coefficient is then identified from comparison zones (and Tambopata's pre-years, where the regressor is 0).

**Offsetting biases.** When two questionable controls move the coefficient in opposite directions, the fact that the combined estimate is close to the baseline is not evidence of robustness. It is the sum of two shifts whose sizes depend on the identification of each control (Oster 2019 discusses why coefficient stability alone is uninformative without accounting for the explained variance).

**Mediation with one treated unit.** With one treated region and one regional spending series, money and treatment are almost collinear in time. Any partial effect of "money" is identified from the other Madre de Dios zones (Amarakaeri, Bahuaja-Sonene). If those zones' outcomes are themselves affected by Mercurio through displacement, the money coefficient picks up the spillover.

## 6. Our example

### 6.1 Variables and code path

| Element | As coded | Where |
|---|---|---|
| Sample | 15 buffer zones (same pool as M1-M3), 2015-25 | `peru_context_models.py:37`, `:61` |
| Outcome | net annual addition, ha (MapBiomas Peru Col 4) | `peru_models.py:46-48` via `:57` |
| Treatment | Tambopata × 2019-21, Tambopata × 2022-25 (binned) | `peru_context_models.py:38`, `:44` |
| K0 | zone + year FE + pre_i × ln(gold) (= M2 on 2015-25) | `:45`, `:51` |
| K1 | K0 + pre_i × 1[2020-21] ("COVID exposure") | `:46-47` |
| K2 | K0 + 1[Madre de Dios zone] × ln(PP 0128 devengado booked in Madre de Dios) | `:48-49`, MDD set `:32` |
| K3 | K1 + K2 | `:33-36` |
| pre_i | zone's 2014-18 mean addition | `:43` |
| Spending | MEF Consulta Amigable, PP 0128, "MADRE DE DIOS" row, devengado column; check 2019 = 31,120,611 soles | `v2_tests.py:175-186`, `:193` |
| Inference | placebo in space, Tambopata removed from each placebo pool | `:66-67` |
| Dose | Tambopata minus the 14-zone mean, net of its 2015-18 mean, correlated with ln(spending), 2015-25 | `:84-92` |

### 6.2 The spending series (million soles, devengado, `t8_pp0128_mdd_*`)

| 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| 2.32 | 0.24 | 1.01 | 0.65 | **31.12** | 20.25 | 9.67 | 7.75 | 7.03 | 6.34 | 5.01 |

Mean 1.05 M in 2015-18, 20.34 M in 2019-21, 6.53 M in 2022-25.

## 7. Tests run and results

### U1 · Reproduce

My re-implementation matches `output/numbers.csv`.

| Model | 2019-21 | 2022-25 | Rank | Extra coefficient | ids |
|---|---|---|---|---|---|
| K0 | −1,607.8 | −172.0 | 1 of 15 | | `ctx_k0_*` |
| K1 | −1,321.6 | −340.1 | 1 of 15 | COVID −0.348 | `ctx_k1_*`, `ctx_k1_covid_coef` |
| K2 | −1,852.6 | −324.2 | 1 of 15 | spending +93.3 | `ctx_k2_*`, `ctx_k2_spend_coef` |
| K3 | −1,566.6 | −492.0 | 1 of 15 | −0.348, +93.2 | `ctx_k3_*` |

K3 / K0 = 0.974 (`ctx_k3_vs_k0_share`). Dose correlation −0.315 (`ctx_dose_corr`). Every design matrix is full rank (asserted in the test).

### U2 · Where the COVID term comes from (lead (a): confirmed)

| Estimated on | COVID coefficient |
|---|---|
| All 15 zones, binned (published) | −0.348 |
| All 15 zones, Tambopata's post years saturated | −0.143 |
| The 14 comparison zones only | −0.145 |
| The 13 comparison zones without Amarakaeri | **+0.710** |

- The regressor equals 1,594 for Tambopata in 2020-21, 342 for Amarakaeri and at most 52 for every other zone. So it is almost a Tambopata-specific 2020-21 dummy.
- Inside the binned 2019-21 treatment dummy, Tambopata went 417 → 181 → −111 ha. The COVID term fits the 2020-21 part of this fall. Binned, it attributes −555 ha/yr of Tambopata's 2020-21 fall to "COVID"; saturated, −229 ha/yr.
- Even the clean estimate (−0.145) comes from Amarakaeri alone. Without Amarakaeri the sign flips (+0.71). **X12:** Amarakaeri is corridor and community land. Its 2020-21 behaviour is a poor stand-in for how a mostly illegal buffer zone reacts to COVID.

### U3 · Binned vs saturated (lead (a): confirmed)

| Model | Binned (published) | Saturated | Rank, saturated |
|---|---|---|---|
| K0 | −1,607.8 | −2,568.1 | 1 of 15 |
| K1 | −1,321.6 | −2,425.3 | 1 of 15 |
| K2 | −1,852.6 | −2,621.3 | 1 of 15 |
| K3 | −1,566.6 | −2,213.6 | 1 of 15 |

- K1 vs K0: **−17.8% binned, −5.6% saturated.** The "COVID shrinks the gap" result is mostly the within-bin artefact.
- K0 saturated is −2,568 for the same reason M2 saturated is −2,508 (S4 T4): the gold slope is then Amarakaeri's, scaled to Tambopata's size.
- K3 / K0 saturated: 0.862.

### U4 · "Keeps 97%" is two shifts that cancel (lead (b): confirmed)

| Shift vs K0 (binned) | ha/yr |
|---|---|
| K1 − K0 (COVID control) | **+286.2** (gap smaller) |
| K2 − K0 (money control) | **−244.8** (gap larger) |
| Sum of the two | +41.4 |
| K3 − K0 | +41.2 |

The 97% is not stability. It is a +286 artefact (U2) and a −245 bad-control shift (U5) that happen to almost cancel.

### U5 · Where the spending coefficient comes from (lead (b): confirmed)

| Spending interacted with | Spending coefficient | 2019-21 gap |
|---|---|---|
| Tambopata, Amarakaeri, Bahuaja (as coded) | +93.3 | −1,852.6 |
| Amarakaeri + Bahuaja only | +62.2 | −1,554.9 |
| Amarakaeri only | +123.3 | −1,530.6 |
| Bahuaja only | −6.6 | −1,609.2 |
| Tambopata only | +496.7 | −3,333.5 |
| As coded, Tambopata saturated | +61.8 | −2,621.3 |
| As coded, Amarakaeri dropped | +55.8 | −1,582.7 |

Annual additions, ha:

| | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Amarakaeri | 301 | 362 | 452 | 54 | 291 | 772 | 658 | 1,086 | 2,099 | 740 | 938 |
| Bahuaja-Sonene | 14 | 8 | 5 | 25 | 10 | 48 | 66 | 83 | 45 | 43 | 157 |

- The positive coefficient comes from Amarakaeri: its additions rose in the high-spending years 2020-21 compared with the low-spending pre-years. Bahuaja alone gives −6.6.
- Because Tambopata is in the MDD set, the term also enters Tambopata's within-bin path (with spending on Tambopata alone the coefficient is +497 and the gap −3,334).
- **X12:** the most plausible reading of "Amarakaeri grew when money was high" is displacement from La Pampa into the corridor and community land. K2 then treats that spillover as the "effect of money" and subtracts it from Tambopata's counterfactual, pushing the gap away from zero. This is the mirror image of the walkthrough's reading ("money following mining", `explainer_content.md:415`).

### U6 · Spending is post-treatment (lead (c): confirmed)

- 0.65 M soles in 2018 → 31.12 M in 2019: a **48-fold** jump in the treatment year.
- corr(ln spending, 1[year ≥ 2019]) = 0.87; a single post-2019 dummy explains 76% of the variance of ln spending in 2015-25.
- The spending *is* Mercurio's budget (the docstring says so, `peru_context_models.py:14-17`). It is a mediator and an outcome of the treatment. By the standard in §5.1 it is a bad control, whichever way the coefficient comes out.

### U7 · The dose correlation is pre vs post, not dose (lead (c): confirmed)

Tambopata's yearly gap (its addition minus the 14-zone mean, net of 2015-18), ha: 2015 −131, 2016 −892, 2017 +849, 2018 +174, 2019 −1,184, 2020 −1,452, 2021 −1,739, 2022 −1,095, 2023 +1,834, 2024 −351, 2025 +236.

| Correlation of the gap with ln(spending) | r |
|---|---|
| 2015-25 (published) | −0.315 |
| Gap with a plain post-2019 dummy instead of spending | −0.251 |
| Within 2015-18 only (4 years) | +0.54 |
| Within 2019-25 only (7 years) | −0.53 |
| Within 2019-21 only (3 years) | **+0.99** |
| After removing pre/post means (partial) | −0.20 |

- Most of the −0.315 is the pre/post contrast that any post-2019 indicator would give.
- **Within the operation years, the relation runs the other way:** 2019 had the most money (31 M) and the smallest gap (−1,184); 2021 the least (9.7 M) and the largest gap (−1,739). So the walkthrough's "years with more money had a weakly bigger fall" (`explainer_content.md:383`) and the figure subtitle "more money, slightly bigger fall" (`peru_context_models.py:131-132`) do not hold year by year in 2019-21. With 3 to 11 points, none of these correlations means much; the honest statement is that the data cannot show a dose-response.

### Tests not possible here

None. The MEF pages are committed under `data_raw/enforcement_peru/mef_pp0128/` (the parser also reads 2026 = 20.62 M soles, which the models do not use).

## 8. Assumption check

| Assumption | Verdict | Evidence |
|---|---|---|
| Pre-treatment covariates | **Violated for K2/K3** | Spending ×48 in 2019 (U6) |
| COVID exposure is pre-treatment | Holds for the measure (2014-18 mean × 2020-21) | but see identification |
| Identification from comparison zones | **Violated for binned K1** | −0.348 binned vs −0.145 from controls (U2) |
| Correct functional form | **Not supported** | COVID slope flips sign without Amarakaeri (+0.71); spending slope driven by Amarakaeri (U2, U5) |
| No spillover | **Likely violated** | Amarakaeri = corridor + communities (X12), rising in 2020-21; both K1 and K2 coefficients come from it |
| Dose-response | **Not identified** | within 2019-21 r = +0.99, opposite sign to the headline (U7) |

## 9. Weaknesses, ranked

1. **K2/K3 control for the treatment's own budget.** A bad control by construction; its coefficient is driven by Amarakaeri's likely spillover.
2. **K1's shrinkage is mostly an artefact** of binned dummies (−18% binned vs −6% saturated).
3. **"Keeps 97%" sounds like robustness but is cancellation** of +286 and −245 ha/yr shifts.
4. **Both new coefficients are identified from Amarakaeri** (X12), the comparison zone most likely to be contaminated by displacement.
5. **The dose statement is reversed inside the operation years** and has too few points to support either direction.
6. The text says money "barely moves" the gap (`explainer_content.md:383`), but K2 moves it by −245 ha/yr (15%).
7. The baseline K0 inherits every problem of M2 (S4 T4).

## 10. Proposed decisions

| # | Decision | Recommendation |
|---|---|---|
| D-S5-1 | K2, K3 (money) | **Drop from the brief.** Keep in the walkthrough only as a worked example of a bad control: "spending rose 48-fold in 2019 because of Mercurio, so it cannot be held constant". Do not report "keeps 97%". |
| D-S5-2 | K1 (COVID) | Replace with the saturated version (or drop). If kept: "allowing big zones to react differently to 2020-21 shrinks the gap by about 6% (−2,568 → −2,425 ha/yr, saturated); the COVID slope comes from one comparison zone". Do not quote "shrinks to 1,322 of 1,608". |
| D-S5-3 | Brief part 4(b), COVID sentence | Replace the K1/K3 numbers with the timing evidence (S1 T1, S8 T5): the net fall starts in 2019 in the workbook but first-time mining stays near its peak in 2019 (X3), so COVID and Mercurio cannot be separated with this panel. Label description. |
| D-S5-4 | Dose | Delete "years with more money had a weakly bigger fall" and the figure subtitle. Say: "With one region and 11 years, the data cannot show whether more money meant a larger fall; in 2019-21 the fall deepened as money declined." |
| D-S5-5 | "Year effects absorb COVID / presidents" (`explainer_content.md:379`, `:389`; `peru_context_models.py:6-7`) | Same fix as D-S4-1: year effects remove the average comparison zone's hectare change (about 22 ha), not shocks that scale with size. |
| D-S5-6 | If a pre-treatment money control is wanted | There is none in this design: a fixed pre-2019 spending level is absorbed by the zone effects. Use money only as context (a timeline figure), not as a control. |

## 11. Verdict

The context models are coded correctly and reproduce. Their interpretation does not hold.
- The COVID control shrinks the gap mainly because, with one 2019-21 dummy, it fits Tambopata's own 2019 → 2021 decline; estimated properly it moves the gap by about 6%, from a slope identified by Amarakaeri alone.
- The money control is a textbook bad control: spending is Mercurio's budget, it rose 48-fold in the treatment year, and its positive coefficient comes from Amarakaeri, the corridor zone most likely to have received displaced miners.
- "Keeps 97%" is the sum of two biased shifts that cancel.

Label: **description**, and not evidence for or against a causal reading.

Wording the brief may use: "COVID began a year after Mercurio, and enforcement money rose 48-fold in 2019 because of it. With one targeted zone we cannot separate Mercurio from COVID or from its own budget [D]."

Wording the brief must not use: "a COVID-exposure control shrinks the gap to 1,322 of 1,608 ha/yr"; "adding enforcement money keeps 97%"; "more money, bigger fall"; "year effects remove COVID".

## References

- Angrist, J. and Pischke, J.-S. (2009). *Mostly Harmless Econometrics*. Princeton University Press, section 3.2.3 ("Bad control").
- Cinelli, C., Forney, A. and Pearl, J. (2024). A crash course in good and bad controls. *Sociological Methods & Research* 53(3).
- Conley, T. and Taber, C. (2011). Inference with "difference in differences" with a small number of policy changes. *Review of Economics and Statistics* 93(1).
- Montgomery, J., Nyhan, B. and Torres, M. (2018). How conditioning on posttreatment variables can ruin your experiment and what to do about it. *American Journal of Political Science* 62(3).
- Oster, E. (2019). Unobservable selection and coefficient stability: theory and evidence. *Journal of Business & Economic Statistics* 37(2).
- Rosenbaum, P. (1984). The consequences of adjustment for a concomitant variable that has been affected by the treatment. *Journal of the Royal Statistical Society A* 147(5).
