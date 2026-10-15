"""Brazil (backup slides only): the same pixel method as Peru (MapBiomas Brazil Collection 11 rasters, brazil_raster.py).

Plan v3 + review card 12 (docs/methods/12_brazil.md). This module is the ONE place for Brazil's definitions:
  BRAZIL      every Brazil window, group and unit definition (imported by brazil.py, brazil_stagger.py, brazil_deter.py,
              spatial.py and the control_* modules); no other Brazil script writes its own dates or windows.
  R*          the ONE treatment-dating rule (D-S12-1), read from data_intermediate/operations_coded.csv:
              treatment starts in the month of the unit's first VERIFIED operation against mining (column verified_ops:
              a source we opened) inside the systematic search window (2021-25 for dating Brazil territories here;
              2017-25 for choosing twins in control_select / control_psm). Unverified snippets (column unverified_ops)
              and operations outside the window are CONTEXT (dashed lines), never treatment and never, on their own,
              a reason to exclude a twin (sensitivity: count them, the twin becomes "unclear"). Annual mapping: an
              operation in Jan-Jun treats that year, Jul-Dec the next year. Removals of non-mining invaders
              (mining_op = "no": Apyterewa, Trincheira Bacaja) are dropped from treated AND comparison groups.
  Units       one Munduruku: the complex Munduruku (29801) + Sai-Cinza (40901), dated with Munduruku. Main sample:
              territories with MapBiomas Col 11 mining before 2019 (pre-treatment selection, D-S12-2); the 24-unit
              candidate list (chosen by AMW, a different product) is a sensitivity only.

  B1 Check: Kayapo mining 2024 / 2025 vs the MapBiomas platform (Collection 11): 17,632 / 18,573 ha.
  B2 Net additions and their parts per territory (net = new land + re-mined - stopped), Collection 11 only.
  B3 Staggered DiD, territory-year panel 2014-2025, territory + year fixed effects, errors clustered by territory.
     HEADLINE outcome: NET additions in hectares (levels), with the three parts (TWFE and did2s are linear in y, so
     net = new + re-mined - stopped holds for the estimates too). Sensitivity: log(1 + first-time ha) (not decomposable).
     Event-study leads are always reported next to the estimate (D-S12-3): parallel trends fail.
  B4 Relabeling check (D-S12-4): shuffle dates over the mining units; NOT a test of the operations (operations
     were targeted at booms, so no shuffle is "as if random").
  B5 Yanomami rings 0-10 / 10-25 km outside the border, boom vs later years.
Reading (card 12): mining in the treated territories boomed for years and fell after 2022; operations arrived at the
peak; our data cannot separate the operations from the end of the boom. DESCRIPTION.
Collection 11 numbers here are never combined with Collection 10.1 (brazil.py) or AMW (brazil_stagger.py).
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyfixest as pf

from common import ROOT, OUT, style_axes, finish_figure, headline, C, INK, INK2, MUTED, AXIS
import checks

INTER = ROOT / "data_intermediate"
OPS_FILE = INTER / "operations_coded.csv"
RASTER_CSV = INTER / "brazil_raster_unit_year.csv"      # = brazil_raster.OUT_CSV (not imported: avoids a cycle)
SRC = ("MapBiomas Brazil Collection 11 rasters (class 30 mining) x FUNAI territories, our pixel accounting; "
       "operations: data_intermediate/operations_coded.csv (rule R*)")
COL11 = "MapBiomas Brazil Collection 11"

# --------------------------------------------------------------------------- ONE place for Brazil's definitions
BRAZIL = dict(
    panel=(2014, 2025),               # staggered DiD panel (Col 11 rasters, 2014-2025)
    pre_sample=(2014, 2018),          # main sample: territories with Col 11 mining in these years (pre-treatment)
    boom=(2019, 2022),                # weaker federal enforcement years (premise needs an external source, card T9)
    later=(2023, 2025),               # Yanomami emergency/operation onwards (Col 11 to 2025)
    pre_col101=(2020, 2022),          # Collection 10.1 2x2 (brazil.py, superseded): pre
    post_col101=(2023, 2024),         # Collection 10.1 ends in 2024
    placebo_col101=((2017, 2019), (2020, 2022)),   # fake start 2020 (Col 10.1)
    dating_window=(2021, 2025),       # R* window for dating Brazil territories (A14)
    twin_window=(2017, 2025),         # R* window for choosing twins (control_select, control_psm)
    twin_free=(2017, 2021),           # relaxed rule R2b: no verified operation in Mercurio's own years
    deter_months=(("2022-02", "2023-01"), ("2023-02", "2024-01")),   # 12 months before / after Feb 2023
    emergency="2023-01",              # Yanomami public-health emergency (20 Jan 2023), context
    gov_change="2019-01",             # federal government change, context
    groups={"Yanomami": ["BR-TI-50901"], "Munduruku": ["BR-TI-29801", "BR-TI-40901"],
            "Kayapó": ["BR-TI-23001"], "Sararé": ["BR-TI-42101"]},
    group_date={"Munduruku": "BR-TI-29801"},        # the complex is dated by Munduruku's own operations
    geocode_col101={"Yanomami": 50901, "Munduruku": 29801, "Kayapó": 23001},   # Col 10.1 workbook (no Sai-Cinza row)
    funai_names={"Yanomami": ["Yanomami"], "Munduruku": ["Munduruku", "Sai-Cinza"], "Kayapó": ["Kayapó"]},
)
UNIT_OF = {u: g for g, us in BRAZIL["groups"].items() for u in us}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def ops_table() -> pd.DataFrame:
    return pd.read_csv(OPS_FILE, dtype=str).fillna("").set_index("unit_id")


def _dates(s: str) -> list[str]:
    return sorted(x.strip()[:7] for x in s.split(";") if len(x.strip()) >= 7 and x.strip()[:4].isdigit())


def first_verified(window=None, unit_ids=None) -> pd.Series:
    """R*: unit_id -> 'YYYY-MM' of the first VERIFIED operation against mining inside `window` (years, inclusive;
    default BRAZIL['dating_window']). Groups take the date of their dating unit (Munduruku complex). Units whose only
    operations removed non-mining invaders are not listed (they are dropped elsewhere via non_mining_units())."""
    a, b = window or BRAZIL["dating_window"]
    ops = ops_table()
    out = {}
    for uid, r in ops.iterrows():
        if r.get("mining_op", "yes") == "no":
            continue
        ds = [d for d in _dates(r["verified_ops"]) if a <= int(d[:4]) <= b]
        if ds:
            out[uid] = ds[0]
    for g, dater in BRAZIL["group_date"].items():           # complex members share the dating unit's date
        for uid in BRAZIL["groups"][g]:
            if dater in out:
                out[uid] = out[dater]
            else:
                out.pop(uid, None)
    s = pd.Series(out, dtype=str)
    return s if unit_ids is None else s.reindex(unit_ids).dropna()


def unverified(window=None) -> pd.Series:
    """unit_id -> first UNVERIFIED report inside the window (context; sensitivity for twin selection)."""
    a, b = window or BRAZIL["twin_window"]
    ops = ops_table()
    out = {uid: [d for d in _dates(r["unverified_ops"]) if a <= int(d[:4]) <= b] for uid, r in ops.iterrows()}
    return pd.Series({k: v[0] for k, v in out.items() if v}, dtype=str)


def non_mining_units() -> list[str]:
    ops = ops_table()
    return ops.index[ops.get("mining_op", pd.Series("yes", index=ops.index)).eq("no")].tolist()


def verdict(window=None, count_unverified=False) -> pd.Series:
    """Operation status per coded unit under R* for twin selection: 'yes' (verified operation in the window),
    'none' (searched over the WHOLE window, nothing found), 'unclear' (undated report, or searched only part of the
    window, or - if count_unverified - an unverified report in BRAZIL['twin_free'] before any verified one), 'treated' (Tambopata)."""
    a, b = window or BRAZIL["twin_window"]
    ops = ops_table()
    fv = first_verified((a, b))
    uv = unverified(BRAZIL["twin_free"])          # sensitivity: only unverified reports in Mercurio's years count
    out = {}
    for uid, r in ops.iterrows():
        if r["verdict_2017_2025"] == "treated":
            out[uid] = "treated"
        elif count_unverified and uid in uv.index and (uid not in fv.index or uv[uid] < fv[uid]):
            out[uid] = "unclear"                             # sensitivity: an earlier unverified report counts
        elif uid in fv.index:
            out[uid] = "yes"
        elif r["verdict_2017_2025"] == "none" and r["searched"] == "2017-2025":
            out[uid] = "none"
        elif r["verdict_2017_2025"] == "yes" and not _dates(r["verified_ops"]):
            out[uid] = "unclear"                             # only unverified reports
        elif r["verdict_2017_2025"] == "yes":
            out[uid] = "none_in_window"                      # verified operations, all outside this window
        else:
            out[uid] = "unclear"
    return pd.Series(out)


def month_label(ym: str) -> str:
    return f"{MONTHS[int(ym[5:7]) - 1]} {ym[:4]}"


def first_treat_year(ym: str) -> int:
    """R* annual mapping: an operation in Jan-Jun treats that year; Jul-Dec treats the next year."""
    return int(ym[:4]) + (1 if int(ym[5:7]) >= 7 else 0)


def br_events(groups=None, window=None):
    """Event markers (common.add_event_markers format) from operations_coded.csv under R*: solid = the group's coded
    treatment (first verified operation in the dating window), dashed = other verified or unverified operations."""
    groups = groups or list(BRAZIL["groups"])
    fv = first_verified(window)
    ops = ops_table()
    ev = []
    for g in groups:
        uid = BRAZIL["group_date"].get(g, BRAZIL["groups"][g][0])
        coded = fv.get(uid)
        if coded:
            ev.append(dict(year=first_treat_year(coded), label=f"{g} {month_label(coded)}", short=g, color=INK,
                           style="solid", group=g, ym=coded, kind="coded"))
        for d in _dates(ops.loc[uid, "verified_ops"]):
            if d != coded:
                ev.append(dict(year=first_treat_year(d), label=f"{g} {month_label(d)}", short=g, color=MUTED,
                               style="dashed", group=g, ym=d, kind="other verified"))
        for d in _dates(ops.loc[uid, "unverified_ops"]):
            ev.append(dict(year=first_treat_year(d), label=f"{g} {month_label(d)} (unverified)", short=g,
                           color=MUTED, style="dashed", group=g, ym=d, kind="unverified"))
    return ev


# --------------------------------------------------------------------------- panel
def load(all_units: bool = False) -> pd.DataFrame:
    """Territory-year panel (Col 11): Munduruku complex merged, non-mining removals dropped, net = new + re-mined -
    stopped. all_units=False keeps the main sample (Col 11 mining in BRAZIL['pre_sample'] years)."""
    d = pd.read_csv(RASTER_CSV)
    d = d[~d.unit_id.isin(non_mining_units())].copy()
    rings = d[d.unit_id.str.startswith("Yanomami_ring")].copy()
    d = d[~d.unit_id.str.startswith("Yanomami_ring")].copy()
    grp = {u: g for g, us in BRAZIL["groups"].items() for u in us if len(us) > 1}
    key = d.unit_id.map(lambda u: BRAZIL["groups"][grp[u]][0] if u in grp else u)
    d["unit"] = np.where(d.unit_id.isin(grp), d.unit_id.map(grp), d.unit)
    d["unit_id"] = key
    d = d.groupby(["unit_id", "unit", "year"], as_index=False)[["mining_ha", "new_land_ha", "remined_ha",
                                                                  "stopped_ha"]].sum(min_count=1)
    d = pd.concat([d, rings], ignore_index=True)
    d["net_ha"] = d.new_land_ha + d.remined_ha - d.stopped_ha
    # identity: net = stock(t) - stock(t-1) for consecutive years (accounting starts 2002)
    s = d.sort_values(["unit_id", "year"])
    diff = s.groupby("unit_id").mining_ha.diff()
    ok = s.year.gt(2002) & s.net_ha.notna()
    assert (diff[ok] - s.net_ha[ok]).abs().max() < 1e-3, "Col 11 identity net = new + remined - stopped fails"
    fv = first_verified()
    d["first_treat"] = d.unit_id.map(lambda u: first_treat_year(fv[u]) if u in fv.index else 0)
    a, b = BRAZIL["pre_sample"]
    pre = d[d.year.between(a, b)].groupby("unit_id").mining_ha.max()
    d["mining_unit"] = d.unit_id.map(pre.gt(0)).fillna(False)
    if not all_units:
        d = d[d.mining_unit | d.unit_id.str.startswith("Yanomami_ring")]
    return d


def panel(d):
    a, b = BRAZIL["panel"]
    p = d[d.year.between(a, b) & ~d.unit_id.str.startswith("Yanomami_ring")].copy()
    p["ln_new"] = np.log1p(p.new_land_ha.fillna(0))
    p["treat"] = ((p.first_treat > 0) & (p.year >= p.first_treat)).astype(int)
    return p


def did(p, y):
    twfe = pf.feols(f"{y} ~ treat | unit_id + year", data=p, vcov={"CRV1": "unit_id"})
    try:
        g = pf.did2s(p, yname=y, first_stage="~ 0 | unit_id + year", second_stage="~ treat", treatment="treat",
                     cluster="unit_id")
        gg = (g.coef()["treat"], g.se()["treat"], g.pvalue()["treat"])
    except Exception as e:                                    # pragma: no cover
        warnings.warn(f"did2s failed: {e}"); gg = (np.nan, np.nan, np.nan)
    return (twfe.coef()["treat"], twfe.pvalue()["treat"]), gg


def event_study(p, y="net_ha", lo=-6, hi=2):
    """TWFE event study with leads (reference e = -1; e binned at lo and hi); never-treated units have all dummies 0."""
    q = p.copy()
    e = np.where(q.first_treat > 0, q.year - q.first_treat, np.nan)
    e = np.clip(e, lo, hi)
    ks = [k for k in range(lo, hi + 1) if k != -1]
    names = []
    for k in ks:
        nm = f"e_{'m' if k < 0 else 'p'}{abs(k)}"
        q[nm] = (e == k).astype(int); names.append(nm)
    f = pf.feols(f"{y} ~ {' + '.join(names)} | unit_id + year", data=q, vcov={"CRV1": "unit_id"})
    return pd.DataFrame({"e": ks, "coef": f.coef()[names].values, "p": f.pvalue()[names].values})


def ri(p, y="net_ha", reps=2000, seed=0):
    """Relabeling check: shuffle treated dates over units; share of shuffles with a TWFE effect <= the real one."""
    rng = np.random.default_rng(seed)
    real = pf.feols(f"{y} ~ treat | unit_id + year", data=p).coef()["treat"]
    units = p.unit_id.unique(); fts = p.groupby("unit_id").first_treat.first()
    dates = fts[fts > 0].values
    sims = []
    for _ in range(reps):
        fake = pd.Series(0, index=units)
        fake[rng.choice(units, size=len(dates), replace=False)] = rng.permutation(dates)
        q = p.assign(treat=((p.unit_id.map(fake) > 0) & (p.year >= p.unit_id.map(fake))).astype(int))
        sims.append(pf.feols(f"{y} ~ treat | unit_id + year", data=q).coef()["treat"])
    return real, float((np.array(sims) <= real).mean())


def _add(reg, id, v, unit, desc, measure, zone, period, src=SRC):
    reg.add(id, v, unit, desc, "description", src, measure=measure, zone=zone, period=period)


def _per(k):
    a, b = BRAZIL[k]
    return f"{a}-{b}"


def run(reg):
    print("\n== Brazil v2 (Collection 11 rasters, net additions, rule R*) ==")
    if not RASTER_CSV.exists():
        warnings.warn("brazil_v2: brazil_raster_unit_year.csv missing; skipping"); return
    d_all = load(all_units=True)
    d = d_all[d_all.mining_unit | d_all.unit_id.str.startswith("Yanomami_ring")]
    k = d_all[d_all.unit == "Kayapó"].set_index("year").mining_ha
    checks.check("MapBiomas Brazil Col 11 raster: Kayapo mining 2024, ha (platform 17,632)", k[2024], 17632, tol=400)
    checks.check("MapBiomas Brazil Col 11 raster: Kayapo mining 2025, ha (platform 18,573)", k[2025], 18573, tol=400)
    checks.save()
    for y in (2024, 2025):
        _add(reg, f"brv2_kayapo_check_{y}", k[y], "ha", f"Kayapo mining area {y}, {COL11} raster x FUNAI polygon "
             f"(platform: {17632 if y == 2024 else 18573})", "stock_col11", "br_kayapo", str(y))

    p, p_all = panel(d), panel(d_all)
    per = _per("panel")
    rows = []
    for samp, pp in (("", p), ("_all24", p_all)):
        for m, ycol in (("net", "net_ha"), ("new", "new_land_ha"), ("remined", "remined_ha"), ("stopped", "stopped_ha")):
            (tc, tp), (gc, gs, gp) = did(pp, ycol)
            rows.append(dict(sample=samp or "mining_units", measure=m, twfe=tc, twfe_p=tp, did2s=gc, did2s_p=gp))
            what = ("main sample: territories with Col 11 mining 2014-18" if not samp else
                    "sensitivity: all 24 candidate territories (chosen with AMW)")
            _add(reg, f"brv2_{m}_twfe{samp}", tc, "ha/yr", f"Staggered DiD (TWFE), {m} additions per territory-year, "
                 f"{COL11}, territory + year FE, rule R*; {what}. Treated territories boomed before their operations: leads "
                 "not flat (brv2_net_es_*), parallel trends fail (card 12)",
                 f"{m}_col11", "br_territories", per)
            reg.add(f"brv2_{m}_twfe{samp}_p", tp, "p-value", f"TWFE p, two-sided, clustered by territory ({what})",
                    "description", SRC)
            _add(reg, f"brv2_{m}_did2s{samp}", gc, "ha/yr", f"Two-stage DiD (Gardner), {m} additions, {COL11}, rule R*; "
                 f"{what}", f"{m}_col11", "br_territories", per)
            reg.add(f"brv2_{m}_did2s{samp}_p", gp, "p-value", f"did2s p, two-sided, clustered by territory ({what})",
                    "description", SRC)
        for est in ("twfe", "did2s"):
            r = {x["measure"]: x[est] for x in rows if x["sample"] == (samp or "mining_units")}
            assert abs(r["net"] - (r["new"] + r["remined"] - r["stopped"])) < 1e-6 * (1 + abs(r["net"])), (est, r)
        # sensitivity: log(1 + first-time ha) (the v2 headline; not decomposable)
        (tc, tp), (gc, gs, gp) = did(pp, "ln_new")
        reg.add(f"brv2_lnnew_twfe{samp}", tc, "log points", f"Sensitivity: TWFE on log(1 + first-time mining ha), {COL11}, "
                "rule R*; a log is not decomposable into net parts", "description", SRC)
        reg.add(f"brv2_lnnew_did2s{samp}", gc, "log points", "Sensitivity: did2s on log(1 + first-time mining ha), rule R*",
                "description", SRC)
        reg.add(f"brv2_lnnew_did2s{samp}_p", gp, "p-value", "did2s p (log sensitivity), two-sided", "description", SRC)
    pd.DataFrame(rows).round(4).to_csv(OUT / "brazil_v2_did.csv", index=False)
    es = event_study(p)
    es.round(4).to_csv(OUT / "brazil_v2_event_study.csv", index=False)
    for _, r in es.iterrows():
        tag = f"{'m' if r.e < 0 else 'p'}{abs(int(r.e))}"
        _add(reg, f"brv2_net_es_{tag}", r.coef, "ha/yr", f"Event study (TWFE), net additions, event time {int(r.e)} "
             "relative to e = -1 (binned at -6 and +2); leads show the pre-operation boom", "net_col11",
             "br_territories", per)
        reg.add(f"brv2_net_es_{tag}_p", r.p, "p-value", f"Event-study p, e = {int(r.e)}", "description", SRC)
    real, pri = ri(p)
    reg.add("brv2_ri_p", pri, "p-value", "Relabeling check (NOT a test of the operations): share of 2,000 shuffles of "
            "operation dates over the mining-unit territories with a TWFE net effect <= the real one, one-sided",
            "description", SRC)
    ft = p.groupby("unit_id").first_treat.first()
    reg.add("brv2_n_units", p.unit_id.nunique(), "count", "Territories in the main Brazil panel (Col 11 mining 2014-18; "
            "Munduruku + Sai-Cinza one unit; non-mining removals dropped)", "description", SRC)
    reg.add("brv2_n_units_all", p_all.unit_id.nunique(), "count", "Territories in the sensitivity panel (all AMW-chosen "
            "candidates, same merges and drops)", "description", SRC)
    reg.add("brv2_n_treated", int((ft > 0).sum()), "count", "Main panel: territories with a first verified operation "
            "2021-2025 (rule R*)", "description", SRC)
    v = verdict(BRAZIL["dating_window"]).reindex(ft.index[ft == 0])
    reg.add("brv2_never_n", int((ft == 0).sum()), "count", "Main panel: 'never-treated' territories (no verified "
            "operation 2021-25)", "description", SRC)
    reg.add("brv2_never_n_unsearched", int(v.isna().sum()), "count", "... of which never searched: 'no operation found' is "
            "NOT 'no operation'", "description", SRC)
    reg.add("brv2_n_treated_2025", int((ft == 2025).sum()), "count", "Treated territories whose first treated year is "
            "2025 (one post year only)", "description", SRC)
    # sensitivity: Kayapo treated from its Oct 2017 raid (outside the dating window)
    pk = p.assign(first_treat=np.where(p.unit_id == "BR-TI-23001", 2018, p.first_treat))
    pk["treat"] = ((pk.first_treat > 0) & (pk.year >= pk.first_treat)).astype(int)
    tk = pf.feols("net_ha ~ treat | unit_id + year", data=pk, vcov={"CRV1": "unit_id"})
    _add(reg, "brv2_net_twfe_kay2017", tk.coef()["treat"], "ha/yr", "Sensitivity: TWFE net additions with Kayapo "
         "treated from 2018 (its Oct 2017 raid) instead of 2023 (R*: Jun 2023)", "net_col11", "br_territories", per)
    reg.add("brv2_net_twfe_kay2017_p", tk.pvalue()["treat"], "p-value", "Sensitivity TWFE p, two-sided", "description", SRC)
    print(pd.DataFrame(rows).round(2).to_string(index=False)); print(es.round(2).to_string(index=False))

    # descriptive: four territories, boom vs later years, net and parts
    show = ["Yanomami", "Munduruku", "Kayapó", "Sararé"]
    wide = {m: d.pivot_table(index="year", columns="unit", values=c) for m, c in
            (("net", "net_ha"), ("new", "new_land_ha"), ("remined", "remined_ha"), ("stopped", "stopped_ha"))}
    for nm in show:
        key = {"Yanomami": "yan", "Munduruku": "mun", "Kayapó": "kay", "Sararé": "sar"}[nm]
        for pk_ in ("boom", "later"):
            a, b = BRAZIL[pk_]
            for m in ("net", "new", "remined", "stopped"):
                _add(reg, f"brv2_{key}_{m}_{pk_}", wide[m].loc[a:b, nm].mean(), "ha/yr",
                     f"{nm}: {m} additions per year {a}-{b}, {COL11}", f"{m}_col11", f"br_{key}", f"{a}-{b}")
    ring = d[d.unit_id.str.startswith("Yanomami_ring")].pivot_table(index="year", columns="unit", values="net_ha")
    for u in ring.columns:
        key = "r0_10" if "0-10" in u else "r10_25"
        for pk_ in ("boom", "later"):
            a, b = BRAZIL[pk_]
            _add(reg, f"brv2_{key}_net_{pk_}", ring.loc[a:b, u].mean(), "ha/yr", f"{u}: net additions per year {a}-{b}",
                 "net_col11", f"br_yanomami_{key}", f"{a}-{b}")
    d.round(2).to_csv(OUT / "brazil_v2_unit_year.csv", index=False)
    figure(wide, show, es)
    return d


def figure(wide, show, es):
    a0 = 2010
    fv = first_verified()
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.4), sharex=True, gridspec_kw={"hspace": 0.55, "wspace": 0.25})
    axes = axes.ravel()
    headline(fig, "Brazil: mining boomed for years and fell after 2022; operations arrived at the peak",
             f"Net mining additions per year, ha (dot) = new land + re-mined (up) − stopped (down), {COL11}, {a0}–2025.\n"
             "Our data cannot separate the operations from the end of the boom.")
    evs = br_events(show)
    for ax, nm in zip(axes, show):
        yrs = wide["net"].loc[a0:].index
        new, rem, stp, net = (wide[m].loc[a0:, nm] for m in ("new", "remined", "stopped", "net"))
        ax.bar(yrs, new, color=C["lapampa"], width=0.72)
        ax.bar(yrs, rem, bottom=new, color=C["lapampa_tint"], width=0.72)
        ax.bar(yrs, -stp, color=C["other"], width=0.72)
        ax.plot(yrs, net, "o", color=INK, ms=3.6, zorder=4)
        ax.axhline(0, color=AXIS, lw=0.8)
        top = float((new + rem).max()) * 1.3
        ax.set_ylim(-float(stp.max()) * 1.15, top)
        for e in [e for e in evs if e["group"] == nm and e["year"] >= a0]:
            coded = e["kind"] == "coded"
            ax.axvline(e["year"] - 0.5, color=INK if coded else AXIS, lw=1.1 if coded else 0.9,
                       ls="-" if coded else (0, (3, 2)))
            if coded or e["kind"] == "unverified":
                ax.annotate(month_label(e["ym"]) + ("" if coded else "\n(unverified)"), xy=(e["year"] - 0.5, 1),
                            xycoords=("data", "axes fraction"), xytext=(-4, -3), textcoords="offset points",
                            ha="right", va="top", fontsize=7.2, color=INK2 if coded else MUTED, linespacing=1.1)
        ax.set_title(nm + (" (+ Sai-Cinza)" if nm == "Munduruku" else ""), pad=6); style_axes(ax)
        ax.set_xticks(range(a0, 2026, 3)); ax.set_xticklabels([f"'{str(y)[2:]}" for y in range(a0, 2026, 3)])
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    axes[1].legend(handles=[Patch(color=C["lapampa"], label="New land"), Patch(color=C["lapampa_tint"], label="Re-mined"),
                            Patch(color=C["other"], label="Stopped (shown below 0)"),
                            Line2D([], [], marker="o", ls="", color=INK, ms=4, label="Net")],
                   loc="upper left", fontsize=7.5, frameon=False, handlelength=1.0, handleheight=0.9)
    axes[0].set_ylabel("ha per year"); axes[2].set_ylabel("ha per year")
    lead = es.set_index("e").coef
    finish_figure(fig, f"{SRC}. Black line = the territory’s first verified operation 2021–25 (rule R*), drawn before its "
                       "first treated year (Jan–Jun: that year; Jul–Dec: the next). Dashed grey = other operations, not "
                       f"coded as treatment. Event-study leads (net, ha/yr): e = −3 {lead.get(-3, np.nan):+,.0f}, "
                       f"e = −2 {lead.get(-2, np.nan):+,.0f}, e ≤ −6 {lead.get(-6, np.nan):+,.0f}: not flat (the treated territories "
                       "boomed before their operations; card 12 finds parallel trends fail). Y-axes differ. Description.",
                  OUT / "fig_brazil_v2_pixels.png")
