# Referee 2 report: code audit and replication (round 1)

Project: Group Giant Anteater, Q2 (Operation Mercurio, Peru; Brazil territories). Branch `analysis/v2-raster`, HEAD 4e9c6ce.
Date: 2026-10-13. Mode: code. Scope: replication package for a course brief, so the emphasis is on replication, the package itself, and the econometrics behind the claims the brief makes.
The author code was not modified. Replication scripts live outside the repo in the session scratchpad (`rep/referee2_replicate.R`, `referee2_wcb.R`, `referee2_m3.R`, `referee2_replicate.py`, `referee2_export.py`).

## Summary

The core numbers are computed correctly. An independent R/fixest replication reproduces, to every printed digit, the 2x2 DiD (-1,761.80), all 14 Peru event-study betas (pools A and B, ref 2018), M1/M2 (-1,453.64 / -1,604.82) with placebo rank 1/15, M3 (-1,859.0), the 1-km cell DiD (La Pampa -1.2085, p 0.081; corridor +0.9378, p 0.0057), Brazil TWFE (0.6190, p 0.129), the Gardner two-stage point estimate (0.5447), and both RD diff-in-discs (road 2.1023, p 0.079, h 2.454; reserve 0.1539, p 0.772). SDID solved with a different solver (SLSQP) gives -1,545.60 against the authors' -1,545.43, with the same placebo rank. An independent R wild cluster bootstrap gives a WCR p of 0.063 against the authors' 0.058, a difference that is draw noise.

The problems are in the package and in how three of the tests are read:
1. A fresh clone of the branch crashes. Two input files the code needs are git-ignored.
2. The "rank 1 of 21" fake-start-year test at the road is padded with 13 start years in which no mining existed near the road.
3. The 1-km cell "DiD" is in practice La Pampa's own before/after change. The comparison cells have almost no mining. Its pre-trend failure, read with a relative-magnitudes bound, does not rule out zero.

Verdict: **Minor revision for the code, major revision for the reading of three tests.**

## Audit 1: Code

| # | Where | Finding |
|---|---|---|
| C1 | `peru.py:133`, `peru.py:150` | 2018 is the omitted year. The closed-form beta equals pyfixest (asserted at `peru.py:176`) and R fixest (`i(year, tr, ref=2018)`). Correct. |
| C2 | `peru_models.py:103-106`, `peru.py:180-186`, `peru_sdid.py:82-87`, `peru_context_models.py:66-68` | Placebo-in-space excludes Tambopata from every placebo pool (the 2026-10-12 fix is present in all four modules). Tambopata's own estimate uses the full pool. This matches Abadie et al. (2010). |
| C3 | `peru_models.py:106`, `peru.py:196`, `peru_context_models.py:68` | Ranks use `pd.Series.rank()` (average ties) and then `int()`, which truncates a tie at 1.5 down to 1. This is harmless here (no ties; R min-ties also gives 1/15), but `control_psm.py:205` and `peru_sdid.py:87` use the conservative `(all <= real).sum()`. Use one convention everywhere. p = rank/n = 1/15 = 0.067 is a one-sided rank p. Correct. |
| C4 | `peru.py:197`, numbers.csv `placebo_space_rank_scaled = 10` | The scale-free event-study rank over the full 15-zone pool is 10 of 15. It is registered but never discussed. Only M4 (7 zones above 10 ha/yr, rank 3 of 7) is cited. Either report it next to M4 or drop it with a reason: tiny pre-means blow up the ratios. |
| C5 | `peru_models.py:57-63` (M3) | Unit trends are fitted on 2014-25 with only two post bins, so post-period variation feeds the trend. Saturating Tambopata's post years (trend from pre-years only) gives -2,004 instead of -1,859 (`referee2_m3.R`). The conclusion does not change. Note it. |
| C6 | `v2_stats.py:72-91` | The authors' own WCR is correct: FWL two-way demeaning (balanced panel, so convergence is exact), a restricted fit with the null imposed (`np.delete(X, k)`), Rademacher weights at block level, CRV1 t, and a symmetric two-sided p. The CRV1 factor omits (N-1)/(N-K), which leaves the bootstrap p unchanged. |
| C7 | `v2_stats.py:256-271` | The bootstrap result is read from a tracked cache (`data_intermediate/wcb_cache_v2.csv`). A rerun never re-executes it, and the cache does not depend on its inputs. Recompute in `main.py`, or hash the inputs. |
| C8 | `v2_stats.py:17`, `v2_stats.py:284` | Labels say "2018 = 0" / "vs 2018", but the reference is the pooled 2014-18 period (`v2_stats.py:126`). Fix the strings. |
| C9 | `brazil_v2.py:36-38` vs `brazil_stagger.py:26` | Munduruku is dated May 2021 in one module (`first_op_2021_2025`) and Aug 2023 in the other (hard-coded `OP`). Kayapó has `first_op_2017_2025 = 2017-10` but is coded as untreated until 2025. One territory should have one date in the whole package. |
| C10 | `peru_robust.py:44-100` | The buffer-zone overlap warning (Bahuaja-Sonene x Tambopata 42,310 ha = 18%) is a **false alarm for the pack data**. Pack `total_ha` for Bahuaja-Sonene is 218,936 against a SERNANP polygon of 261,271. The difference, 42,335 ha, equals the overlap, so MapBiomas already assigned the overlap to Tambopata only. The warning text still ends up in numbers.csv descriptions. Replace the polygon test with this `total_ha` test, and say the series are overlap-free. |
| C11 | `rdrobust` call `v2_rdd.py:112` | `vce="hc1"` together with `cluster=` is switched silently to CR1. This is fine, but name it CR1. rdrobust also warns about mass points: all bins sit at the same x within a segment. |

## Audit 2: Cross-language replication

| Quantity | Authors (Python) | Referee (R fixest / rdrobust; Python SLSQP) | Match |
|---|---|---|---|
| 2x2 DiD Tambopata - Amarakaeri | -1,761.8017 | -1,761.8017 | yes |
| Event study pool A, 2019 / 2021 / 2023 | -1,450.744 / -2,190.857 / 775.464 | identical | yes |
| Event study pool B, 2019 / 2025 | -1,357.709 / 61.405 | identical | yes |
| M1, M2 during | -1,453.636, -1,604.817; rank 1/15 | identical; rank 1/15 | yes |
| M3 during | -1,858.98 | -1,859.0 | yes |
| Cell S1 La Pampa / corridor during | -1.20849 (p 0.0813) / 0.93780 (p 0.0057) | identical | yes |
| La Pampa joint pre-trend (2010-13) | p 0.0055 (chi2) | p 0.0076 (F) | package heterogeneity (chi2 vs F); same conclusion |
| WCR p, La Pampa / corridor | 0.058 / 0.000 | 0.063 / 0.000 (WCU: 0.128 / 0.013) | yes (draw noise) |
| Brazil TWFE / Gardner point | 0.6190 / 0.5447 | 0.6190 / 0.5447 | yes |
| RD road / reserve diff-in-disc | 2.1023 (p 0.079) / 0.1539 (p 0.772) | identical | yes |
| SDID ha, during | -1,545.43 (FISTA) | -1,545.60 (SLSQP), rank 1/15 | yes (solver tolerance) |

**Full pipeline rerun** (rsync copy including the git-ignored local files): exit 0 in 107 s. numbers.csv (1,399 ids) and checks.csv are byte-identical to the repo, including the PPML p-values. checks.csv: 26 checks OK, 1 `MISMATCH-documented` (Kayapó Col 10.1 vs Col 11, intended).

## Audit 3: Directory and replication package

**R1 (BLOCKER). A fresh `git clone` of the branch crashes** (`raster_layers.py:74` → `raster_zones.py:85`, then `:87`):
- `data_raw/raisg/vias_nacionales_mdd_box.geojson` (28 MB). It is ignored by `data_raw/raisg/*.geojson` although it is under 50 MB.
- `data_raw/mapbiomas_amazonia/INDIGENOUS_TERRITORIES.zip` (59 MB, ignored).

With those two files added, the clone runs to exit 0, but 7 ids are missing from numbers.csv: `s2_lp_west_*` (3, from `glad_alerts.py:155-157`, needing the ignored Sentinel-2 alert tif) and `sp_lp_*` (4, `spatial.py:378`). `s2_lp_west_*` is cited in `explainer_content.md:302`. Apart from those, the numbers equal the repo's (only PPML p noise, at the 5th to 8th digit).

Fix:
- Commit the road file, or a clipped IOH line, and a clipped MdD native-community layer.
- Make `rz.layers()` fall back to them.
- Have `glad_alerts`/`spatial` write their numbers to a committed intermediate.
- Add a CI-style test: a clean clone runs, then numbers are diffed.

Other findings:
- R2: no absolute paths (`common.py:15` ROOT-relative). Seeds are fixed (`brazil_v2.py:58`, `v2_stats.py:72`, `v2_extra.py:246`, `placebo_explainer.py:57`).
- R3: the replication README is not written yet (only `templates/REPLICATION_README.txt`). It must list the git-ignored inputs (IBAMA zip 117 MB, AMW 108 MB, rasters ~3 GB, GLAD, MapBiomas Amazonía xlsx) and the fact that `data_intermediate/` is what makes the run possible without them.
- R4: the course zip expects `data_raw/ code/ output/`. `data_intermediate/` is extra and must be in the zip.
- R5: `code/` holds 40 modules, against the brief's "ONE script". `main.py` satisfies the entry-point requirement, but say so in the README.
- R6: dependencies are pinned through `uv.lock`, and `rdrobust` and `wildboottest` are declared.

Replication readiness: **6/10** now, 9/10 after R1 and R3.

## Audit 4: Output automation

Every brief number is a `{{id}}` placeholder from `output/numbers.csv`, which is fully automated. Good. Exceptions: the bootstrap cache (C7), and the economics parameters that are hard-coded and partly unverified (E2, E3).

## Audit 5: Econometrics

**Q1, Peru ladder.** Fixed effects are zone + year (`peru_models.py:65-66`, no intercept, all zone dummies, first year dropped). These are correct and equal pyfixest (asserted) and R. The ladder's reference is the pooled 2014-18 period. The event study's reference is 2018. The p of 0.07 = 1/15 is right. The raw-hectare rank mechanically favours the largest zone, which the M4 rank of 3/7 (p 0.43) already shows. Keep both together, as the brief does.

**Q2, cell panel (the main new concern).**
- Comparison cells average 0.00-0.03 ha/cell-yr of first-time mining in every year 2010-25, against 0.3-3.2 in La Pampa (`referee2_replicate.py`). The "DiD" of -1.21 is therefore La Pampa's own change: 2014-18 mean 2.47 → 2019-21 mean 1.27. The year effects are estimated from cells with no exposure to gold prices or COVID, so parallel trends is not a meaningful assumption here.
- The year profile matters. 2019 = +0.13 (no fall in the operation year); 2020 = -1.90 and 2021 = -1.86. The fall coincides with COVID, not with Feb 2019.
- The pre-trend failure comes from 2010 (-2.14) and 2012 (-1.01): La Pampa was ramping up into its 2014-18 peak. Under a Rambachan-Roth relative-magnitudes bound with M̄ = 1, the largest pre-period deviation (2.14) exceeds the estimate (1.21), so the identified set includes 0. A La Pampa-specific linear pre-trend, imputed, gives -2.04, so the sign of the bias is not identified.
- The WCR p of 0.06 with 14 treated clusters of 161 is plausible. MacKinnon & Webb (2017) find WCR conservative with few treated clusters. WCU gives 0.13.
- Implication: in the brief, report -1.21 as a description of La Pampa's own change, not as a cell-level DiD that supports the conditional causal sentence.

**Q3, Brazil.**
- The estimator is TWFE (`brazil_v2.py:48`) plus Gardner two-stage `pf.did2s` (`brazil_v2.py:50`). That design is robust to forbidden comparisons. The two are close (0.62 vs 0.54), so contamination is small.
- The brief's +0.54 log points, p = 0.17, is the did2s cluster-robust two-sided test. agent.md's "RI p = 0.92" is a different test: one-sided P(shuffled TWFE ≤ real) (`brazil_v2.py:58-70`). For a positive estimate, 0.92 is consistent, so the two do not contradict each other. But the RI uses the TWFE statistic, not did2s.
- Of the 13 "never-treated" territories, 10 have no operation search at all (not in `operations_coded.csv`) and 1 is "unclear". 4 of the 11 treated units are treated only in 2025.
- Say "no evidence, low power"; that is already the brief's framing.

**Q4, spatial RD.**
- Unit: 250-m bins x 2-km segments, area-weighted, local linear, triangular kernel, MSE-optimal h = 2.45 km, CR1 by segment, outcome in % of the unit's land per year. So "+2.1 points" means +2.1 percentage points of land per year. Correct.
- Donut 0.5 km: 3.29, p 0.04. Note that the donut estimate is larger, and fixed-h estimates range from 1.08 (h = 1) to 3.29 (h = 5).
- **Fake-start-year rank (`v2_rdd.py:139-144`) is not informative as built:**
  1. 13 of the 21 "clean" start years (1995-2007) are exactly 0, because no mining existed near the road before 2008.
  2. The real statistic in the ranking is fake[2019] = 2.54 (3-yr windows 2016-18 vs 2019-21), not the headline 2.10.
  3. 2011 gives |-2.47|, nearly as large as the real statistic. The headline 2.10 would rank 2nd.
  4. Start year 2022 uses 2019-21 (treated years) as its pre-window, contradicting the comment "windows not touching 2016-21".

  Restricted to start years with mining (2008-13, 2022), the real result ranks 1 of 8 (p = 0.125), not 1/21 (0.048). This figure is cited in the walkthrough (`explainer_content.md:482, 688, 782`). Recompute it on 2008+ and rank the same statistic that is reported.

**Q5, SDID and matching.**
- SDID follows ADH+ Algorithm 1: ζ = (N_tr·T_post)^¼·σ̂(ΔY), unit penalty ζ²T0, time penalty (1e-6σ̂)²N0, and the intercept handled by demeaning along the correct axis (`peru_sdid.py:48-49`). It is verified against SLSQP.
- Matching: common support fails (`psm_ps_n_above_tam = 0`). The caliper is computed but never used (`control_psm.py:172`). Entropy balancing drops the Brazil dummy. The outcome is a post-only level (pace as a share of 2018 stock), with no pre-period differencing, because AMW starts in 2018. All of this is honestly labelled. The placebo p range is 0.19-0.57. Fine as description.

**Q6, context models.** `ctx_k3_vs_k0_share` = K3/K0 on 2015-25 (`peru_context_models.py:84`). The bad-control problem is acknowledged in the docstring (`:14-17`), the figure note (`:134`) and the spend-coefficient description. But brief part 4(b) (`brief_content.md:41`) uses "keep 97% of the gap" as reassurance without that caveat. Also, Tambopata's post years are all absorbed by its own dummies, so `mdd_x_lnspend` is identified from Amarakaeri, Bahuaja-Sonene and Tambopata 2015-18. It mostly measures spillover into the two neighbours, not money "absorbing" the treatment. Add one clause to the brief.

**Q7, economics (`v2_economics.py:33-40` vs `economics_sources.md`).**
- Yield 1.7-1.9 kg/ha (CSF-PE Cuadro 3), Hg:Au 2.4-2.8 (p.47), margins 11/23.9/36.8% of sales (Torres via MINAM16), 29.5% income tax, 0% royalty: all used as the sources state.
- E1: the "high" gold applies 1.9 kg/ha to returns to old pits as well (`:63`). Old pits are partly worked out, so this overstates. The source also warns that grades for the suction-pump method are unknown.
- E2: social cost low = US$81,000/kg comes from the CSF calculator, marked "team note", not re-opened (`economics_sources.md:50`). High = US$1.8 M is CSF-PE p.7. The range mixes two models.
- E3: the exchange rate 3.3-3.9 has no source row ("verify", `:39`).
- E4: the implied 3.7 kg/ha cross-check (`:69`) is 2x the CSF yield. Mention it next to the 19-32 t figure.

**Q9, data rules.**
- Additions from levels after aggregation: `peru.py:39,57`, `peru_models.py:48`, `common.additions` asserts unit-year uniqueness.
- No cross-source subtraction found. Rest-of-MdD is Col 4 minus Col 4.
- The twin pre-trend compares a Peru Col 4 index with an Amazonía Col 6 index side by side (`control_select.py:211-226`). That is not subtraction, but it is a levels (stock) index, against rule 1. The reason is documented.
- `checks.py:38` sums MdD over all biomes to match the publisher. That is fine for a check only.

## Prioritized recommendations

BLOCKER: R1. SHOULD: Q4 fake-year rank; Q2 reading of the cell DiD; Q6 brief caveat; C9 one treatment date per territory; R3 README; C7 bootstrap cache; E1-E3. NICE: C3, C4, C5, C8, C10, C11, E4.
