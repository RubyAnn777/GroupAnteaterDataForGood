# S0 · Potential outcomes, the treatment, and claim labels

*Method card 0 of the causal review (plan: `docs/causal_review_plan.md`). Card only: no estimator is tested here, but every later card builds on these definitions.*

**Decision recorded in this session (Ruby, 2026-10-14):** the treatment is **the start of Operation Mercurio** (February 2019; first treated year 2019). Everything that happened afterwards (COVID-19, Plan Restauración, Mercurio II, the 2023 state of emergency, the 2025 navy withdrawal) is **context**: we show it in the figures and the text, but we do not model it as separate treatments. This is a deliberate simplification, and the brief must say so.

---

## 1. In one sentence

A causal effect is the difference between what happened and what **would have happened** to the same place at the same time without the intervention. Every causal method is a way to estimate the second, unobservable, half.

## 2. Simple version

Imagine two copies of the world in 2019. In world A, the Peruvian state launches Operation Mercurio in La Pampa. In world B, it does not. Everything else is the same: the gold price, the rain, COVID the next year. The effect of Mercurio on new mining in the Tambopata buffer zone is

> new mining in world A − new mining in world B.

We only ever see world A. World B is the **counterfactual**. Two shortcuts are tempting and both are wrong:

- **Before vs after** (Tambopata 2016-18 vs 2019-21). This mixes Mercurio with everything else that changed over time (COVID, the gold price).
- **Treated vs untreated** (Tambopata vs Amarakaeri in 2019-21). This mixes Mercurio with every permanent difference between the two places (size, geology, roads).

Every method in this review is a different recipe for building world B from the data we do have: a comparison zone (DiD), a weighted mix of zones (synthetic control), a twin chosen by rules (matching), or the land just across a border (regression discontinuity). Each recipe works only under its own assumption, and the review checks those assumptions one by one.

## 3. When to use this framework, and when not

**Use it** whenever a sentence contains "because of", "led to", "reduced", "caused" or "worked". The framework forces three questions: what exactly is the treatment, what is the outcome, and what is the counterfactual?

**It does not answer by itself:**
- *Why* something happened (mechanisms). The framework gives effects, not stories.
- Questions where the "treatment" cannot be imagined switched off. Example: "the effect of being in Madre de Dios".
- Prediction. A model can predict mining well without saying anything about what would happen if we changed enforcement (the risk map in S13 is prediction, not causation).

## 4. Assumptions (the vocabulary every later card uses)

| Assumption | In words | Formally |
|---|---|---|
| **SUTVA (a): no interference** | One place's treatment does not change another place's outcome. | Y_i(**d**) = Y_i(d_i) for every treatment vector **d** |
| **SUTVA (b): consistency / one version of treatment** | "Treated" means the same thing everywhere, and the outcome we see under treatment is the potential outcome under treatment. | Y_i = D_i·Y_i(1) + (1 − D_i)·Y_i(0) |
| **No anticipation** | The outcome does not react before the treatment starts. | Y_it(1) = Y_it(0) for t < treatment date |
| **Identification assumption** | What makes the comparison a valid stand-in for world B. It differs per method: parallel trends (DiD), a good pre-period fit (synthetic control), unconfoundedness (matching), continuity at the border (RD). | method-specific, see cards S2-S12 |
| **Overlap / positivity** | Comparison units exist that look like the treated one. | 0 < P(D = 1 \| X) < 1 |

## 5. The maths

### 5.1 Master's level

For unit *i* (a zone) in year *t*, define two **potential outcomes**:
- Y_it(1): new mining if treated
- Y_it(0): new mining if not treated

The individual effect is τ_it = Y_it(1) − Y_it(0). The **fundamental problem of causal inference** (Holland 1986): for any (i, t) we observe only one of the two.

With one treated unit (Tambopata, *i* = T), the estimand is the **effect on the treated** in each post year, or averaged over a window:

  τ_T(2019-21) = (1/3) Σ_{t=2019}^{2021} [ Y_Tt(1) − Y_Tt(0) ]

The first term is observed. Everything hinges on how we fill in Y_Tt(0).

**Why the two shortcuts fail.** Write the naive before/after change for Tambopata:

  Ȳ_T,post − Ȳ_T,pre = τ_T + [ Ȳ_T,post(0) − Ȳ_T,pre(0) ]

The bracket is the change Tambopata would have had anyway (COVID, gold price, depletion). It is **time bias**. The naive treated-vs-control gap in the post period:

  Ȳ_T,post − Ȳ_C,post = τ_T + [ Ȳ_T,post(0) − Ȳ_C,post(0) ]

The bracket is **selection bias**: Tambopata was chosen precisely because it was the biggest mining front.

**Difference in differences** subtracts one from the other:

  DiD = (Ȳ_T,post − Ȳ_T,pre) − (Ȳ_C,post − Ȳ_C,pre) = τ_T + { [Ȳ_T,post(0) − Ȳ_T,pre(0)] − [Ȳ_C,post(0) − Ȳ_C,pre(0)] }

The term in braces is zero under **parallel trends**: without Mercurio, Tambopata would have changed by the same amount as the comparison. That is an assumption about world B, so it can never be proven, only made more or less believable (S2, S3).

### 5.2 PhD level

**Bundled treatment.** With the decision above, the treatment indicator is

  D_it = 1[i = Tambopata BZ] · 1[t ≥ 2019].

The estimand is then the effect of *"Mercurio starting in 2019, together with everything that came with it in this place"*. Formally, if the realised post-2019 enforcement path in Tambopata is e_T = (Mercurio, Restauración, emergency, …) and the counterfactual path is e_T⁰ (no Mercurio, and whatever would have followed), then

  τ_T(t) = Y_Tt(e_T) − Y_Tt(e_T⁰).

Two things follow. First, we cannot separate Mercurio from later waves. Second, *e_T⁰* is not "no enforcement at all": the 2017-18 operations had already started, and some later programmes might have happened anyway. The estimand is "Mercurio as it unfolded vs the world without it", which is the policy-relevant contrast for FZS ("what happens when such an operation starts and ends?").

**Interference and the sign of the bias.** If miners move from Tambopata into the comparison zone C, then C's observed outcome is Y_Ct(d_T = 1) ≠ Y_Ct(0). With a spillover s_Ct > 0 into C,

  DiD = τ_T − s̄_C,post.

With deterrence (τ_T < 0) and displacement (s > 0), the DiD is **more negative than the true effect**: biased away from zero. Exposure-mapping frameworks (Aronow and Samii 2017) generalise this by defining each unit's treatment as its exposure to the treated unit (for example its distance to La Pampa). The cell gradient (S8) and the RD at the road (S9) are partial versions of that idea.

**Consistency with a stock outcome.** MapBiomas measures a stock of mined land. Our outcomes are flows derived from it (net additions, first-time mining). A one-year intervention can change the flow for years, because the remaining unmined land in a place shrinks as it is mined (depletion). So "no anticipation" and "parallel trends" are statements about flows, while depletion is a dynamic in the stock that differs by place. This is why S1 and S8 treat the outcome definition as part of the identification argument.

**Inference with one treated unit.** With N_T = 1, cluster-robust standard errors are not consistent: the treated unit's idiosyncratic shock never averages out (Conley and Taber 2011). The project therefore uses **design-based** inference. Under Fisher's sharp null H₀: τ_it = 0 for all i, t, the "treatment" label can be moved to each comparison unit (placebo in space) or to each fake date (placebo in time), and the real estimate's rank among the fakes gives an exact p-value **if** the units (or dates) are exchangeable. Exchangeability is itself an assumption: a zone 100 times smaller than Tambopata is not exchangeable with it in hectares. This is cross-cutting issue X1 in the plan.

**The claim ladder.** The course requires every sentence to carry one of three labels:

| Label | What it claims | What it needs |
|---|---|---|
| **Description** | What the data show, with no counterfactual: "Tambopata added 1,640 ha/yr in 2016-18 and 163 ha/yr in 2019-21." | Correct data and arithmetic. |
| **Prediction** | What we expect to observe, with no claim about why: "cells near the road and near old pits are most likely to be mined next." | Out-of-sample validation. |
| **Causal** | What would have happened under a different action: "Mercurio lowered new mining by X." | A counterfactual, its assumption stated, and evidence that the assumption is plausible. |

A DiD number is **arithmetically** a description. It becomes a causal claim only when we add "if the comparison shows what Tambopata would have done". That conditional sentence is the bridge.

## 6. Our example

**Unit.** A buffer zone (A1-A6), a 1-km cell (A7), a 250-m bin (A8), a protected area or territory (A10-A14).

**Treated unit.** Tambopata buffer zone, which contains La Pampa (A1-A6), or the La Pampa sector within it (A7-A8).

**Treatment date.** 2019 is the first treated year in every Peru module:
- `peru.py:29` (periods 2016-18 / 2019-21 / 2022-25);
- `peru_models.py:4-5` ("Tambopata = treated from 2019");
- `peru_models.py:94` (`REAL = {"during": (2019, 2021), "after": (2022, 2025)}`);
- `common.py:140-146` (`PERU_EVENTS`).

Why 2019 and not 2018, although the operation started in February 2019: the outcome is `addition(t) = map(t) − map(t−1)` (`common.py:36-47`), so addition(2019) = map 2019 − map 2018 is the first flow that can reflect the operation. Event lines are drawn at Y − 0.5 for that reason (`common.py:149-150`).

**Context events** (shown in figures as dashed lines, `common.py:140-146`; not modelled as treatments):

| Year | Event | Why it matters for reading the results |
|---|---|---|
| 2017-18 | Earlier operations and interdictions (AIDER 2021, cited in MAAP #241) | The pre-period is not enforcement-free. |
| **Feb 2019** | **Operation Mercurio starts in La Pampa** | **The treatment.** |
| Mar 2020 | COVID-19 | Lands in the first "during" window; fewer patrols, miners re-entered (Romo 2020, cited in MAAP #241). |
| 2021 | Plan Restauración; Mercurio II (all of Madre de Dios, incl. Amarakaeri) | The comparison zone is partly treated too. |
| Apr 2023 | State of emergency (DS 046-2023-PCM) | Lies inside the "after" window, so "after" is not "after enforcement ended". |
| 2025 | Navy leaves Malinowski posts | Possible start of a real "after". |

**What this means for every later card:**
1. The 2019-21 estimate is "Mercurio, together with COVID and the first follow-up operations". We cannot split it.
2. The 2022-25 window is **not** "after the operation ended". It contains the 2023 emergency. The brief should call it "later years", not "after enforcement".
3. The comparison is "more enforcement vs less enforcement" (Amarakaeri was partly treated), not "treated vs untreated".

## 7. Variables

| Variable | Definition | Source | Where in code |
|---|---|---|---|
| D_it (treatment) | 1 if Tambopata BZ and year ≥ 2019 | decision; Mercurio start | `peru_models.py:56`, `peru.py:29` |
| Y_it (outcome, zone level) | net annual addition of mining area (ha) | MapBiomas Peru Col 4, class 4.2 Minería, buffer-zone statistics | `peru.py:33-58` |
| Y_it (outcome, pixel level) | first-time mined ha | MapBiomas Peru Col 4 rasters | `raster_zones.py:186-208` |
| t | calendar year; 2019 = first post year | | `common.py:149-150` |
| Context events | 2020, 2021, 2023, 2025 lines | MAAP #241; DS 046-2023-PCM | `common.py:140-146` |

The outcome definitions are examined in S1.

## 8. Assumption check (preview; each is tested in its own session)

| Assumption | Supported by | Threatened by | Tested in |
|---|---|---|---|
| No interference | none | Displacement to Amarakaeri (Camanti), across the road, into the reserve (MAAP #130, #241) | S2, S8, S9 |
| One version of treatment | Single start date for Peru | Treatment is a bundle; Brazil territories have different kinds of operations | S0 (this decision), S12 |
| No anticipation | Mercurio was a surprise operation (to verify) | 2017-18 operations already in the pre-period | S2, S3 |
| Parallel trends | Not supported in hectares (S2 T3, S3 T3) | Tambopata is 5× Amarakaeri and ~100× most zones; scale-dependence | S2-S4 |
| Overlap | none | Tambopata is outside the donor range in hectares; no common support in matching | S6, S11 |

## 9. Weaknesses found

1. **Bundled treatment.** By decision we cannot attribute the 2019-21 fall to Mercurio alone. Acceptable, if stated.
2. **"After" is mislabelled** in some text: 2022-25 includes the 2023 emergency.
3. **Peru dates are consistent** across modules (2019 everywhere). Brazil is not: one module maps July-December operations to the next year (`brazil_v2.py:59-61`) and another does not (`brazil_stagger.py:30-38`). Handled in S12.

## 10. Tests

None run (card only). One check done: every Peru module codes 2019 as the first treated year (grep of `code/`, see section 6).

## 11. Verdict and wording for the brief

- **Treatment wording:** "We treat the start of Operation Mercurio in February 2019 as the treatment. Enforcement continued afterwards (COVID-19 in 2020, Plan Restauración in 2021, a state of emergency from April 2023), so our estimates measure Mercurio together with what followed in those years. We show these events in the figures but do not separate their effects."
- **Causal sentences** must have the form: "*If* [comparison] shows what Tambopata would have done without Mercurio, then Mercurio and the operations that followed lowered [measure] by [range] in 2019-21." Whether any range survives is decided in S14 (proposal: about 1,450-1,660 ha/yr of net additions, read as an upper bound; see `14_synthesis.md` §10-11).
- **Never** write "after the operation ended" for 2022-25.

## References

- Holland, P. (1986). Statistics and causal inference. *JASA* 81(396).
- Rubin, D. (1974). Estimating causal effects of treatments in randomized and nonrandomized studies. *J. Educ. Psych.* 66(5).
- Imbens, G. and Rubin, D. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences*. Cambridge UP. Ch. 1-2.
- Aronow, P. and Samii, C. (2017). Estimating average causal effects under general interference. *Annals of Applied Statistics* 11(4).
- Conley, T. and Taber, C. (2011). Inference with "difference in differences" with a small number of policy changes. *REStat* 93(1).
- Cunningham, S. (2021). *Causal Inference: The Mixtape*, ch. 4 (potential outcomes). Free online.
