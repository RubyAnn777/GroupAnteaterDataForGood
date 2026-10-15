"""ONE place for the three definitions every module must share (decided 2026-10-15, plan v3; see docs/PLAN_v3.md).

1. OUTCOME  Net mining additions, ha/yr = mining(t) - mining(t-1) = new land + re-mined - stopped,
            counted on the MapBiomas Peru Collection 4 rasters (class 30 = 4.2 Minería), 30-m pixels.
              new land  mining in t, never mining in any earlier year since 1985     (first-time mining)
              re-mined  mining in t, not in t-1, but mining in some year before t-1  (return to old scars)
              stopped   mining in t-1, not in t                                      (pit leaves the mining class:
                        flooded, regrowing, abandoned, or reclassified; split further in raster_zones.py)
            Where an estimator is linear (DiD, two-way fixed effects, event study), net = new + re-mined - stopped
            holds for the estimates too, and we report all four. Where it is not (ratios, logs, weights, Poisson),
            we say so next to the number.
2. ZONES    One registry (ZONES below), built once by raster_zones.py on the MapBiomas grid. Official SERNANP
            buffer zones stay WHOLE (overlaps go to Tambopata first, then Amarakaeri: that is what MapBiomas
            does; Tambopata BZ raster = the publisher's 231,693 ha). Corridor and community land INSIDE a buffer
            zone is a TAG (TENURE) for splitting results, not a carve-out. The MapBiomas statistics workbook
            (data/peru_bufferzone_year.csv) is only a reconciliation check.
3. TREATMENT  The start of Operation Mercurio, February 2019, in the Tambopata buffer zone (La Pampa).
            addition(2019) = map 2019 - map 2018, so 2019 is the first treated year and 2018 the reference year.
            COVID-19 (2020), Plan Restauración (2021), Mercurio II, the state of emergency (Apr 2023) and the navy
            withdrawal (2025) are CONTEXT: shown, not separately estimated. 2022-25 = "later years", never
            "after enforcement ended".
"""
from __future__ import annotations

# --------------------------------------------------------------------------- treatment
TREATED_ZONE = "tambopata_bz"          # the treated unit for every zone design (official buffer zone, whole)
TREATED_SECTOR = "lapampa"             # the targeted sector inside it (pixel designs, figures)
TREATMENT_START = "2019-02"
FIRST_POST = 2019                      # first treated annual addition
REF_YEAR = 2018                        # event-study reference year (omitted)

# Periods (inclusive). Every module uses these names; no module writes its own windows.
PERIODS = {
    "pre": (2016, 2018),               # course card window (before)
    "pre_long": (2014, 2018),          # pooled reference for models and event studies
    "during": (2019, 2021),            # Mercurio and the operations that followed
    "later": (2022, 2025),             # later years (contain the 2023 emergency); also report without 2023
}
LATER_EX = 2023                        # the MapBiomas-only spike year: report "later" with and without it
PLACEBO_START = 2016                   # fake start (course card): compare 2013-15 with 2016-18
PLACEBO_PERIODS = {"pre": (2013, 2015), "during": (2016, 2018)}
YEARS = (2014, 2025)                   # descriptive window (course card: 2014 -> latest)
PANEL_YEARS = (2011, 2025)             # model panels incl. placebo years

def period_label(key: str) -> str:
    a, b = PERIODS[key]
    return f"{a}–{str(b)[2:]}"

# --------------------------------------------------------------------------- outcome
MEASURE = "net"                         # the outcome; parts below
PARTS = ["new", "remined", "stopped"]   # net = new + remined - stopped
COLS = {"net": "net_ha", "new": "new_ha", "remined": "remined_ha", "stopped": "stopped_ha", "stock": "mining_ha"}
SIGN = {"new": +1, "remined": +1, "stopped": -1}
MEASURE_NAME = {
    "net": "Net mining additions",
    "new": "New land (first-time mining)",
    "remined": "Re-mined land",
    "stopped": "Stopped (left the mining class)",
    "stock": "Mining area (stock)",
}
UNIT = "ha/yr"
OUTCOME_LABEL = "Net mining additions, ha/yr (new land + re-mined − stopped)"
OUTCOME_SHORT = "Net additions, ha/yr"
SOURCE = "MapBiomas Peru Collection 4 rasters (class 4.2 Minería), our pixel accounting"

# --------------------------------------------------------------------------- zones
# Exclusive partition of the study region (Madre de Dios + the whole Tambopata and Amarakaeri buffer zones),
# first match wins, in this order. `in_mdd` is a separate flag, so department totals are sums of the same zones.
LP_LON = (-70.15, -69.80)              # La Pampa sector: Tambopata BZ inside these longitudes (no official line)
LP_ALT = {"narrow": (-70.10, -69.85), "wide": (-70.20, -69.75)}
ACROSS_KM = 10.0                        # "across the road": corridor within 10 km north of the Interoceanic Highway

ZONES = {   # slug: (code, display name, group)
    "tambopata_nr":     (1, "Tambopata National Reserve", "protected"),
    "other_anp":        (2, "Other protected areas", "protected"),
    "lapampa":          (3, "La Pampa sector", "tambopata_bz"),
    "tambopata_bz_rest": (4, "Rest of Tambopata buffer zone", "tambopata_bz"),
    "amarakaeri_bz":    (5, "Amarakaeri buffer zone", "buffer"),
    "bahuaja_bz":       (6, "Bahuaja-Sonene buffer zone", "buffer"),
    "other_bz":         (7, "Other buffer zones", "buffer"),
    "corridor_across":  (8, "Corridor across the road", "outside"),
    "corridor_rest":    (9, "Rest of the mining corridor", "outside"),
    "communities":      (10, "Native communities", "outside"),
    "rest_mdd":         (11, "Rest of Madre de Dios", "outside"),
}
ZONE_CODE = {k: v[0] for k, v in ZONES.items()}
ZONE_NAME = {k: v[1] for k, v in ZONES.items()}
CODE_ZONE = {v[0]: k for k, v in ZONES.items()}

# Reporting units = unions of partition zones. Use ONLY these names in text and figures.
UNITS = {
    "tambopata_bz": ["lapampa", "tambopata_bz_rest"],          # = official SERNANP buffer zone RN09, whole
    "lapampa": ["lapampa"],
    "tambopata_bz_rest": ["tambopata_bz_rest"],
    "amarakaeri_bz": ["amarakaeri_bz"],                          # whole, incl. its Cusco part (Camanti)
    "corridor_across": ["corridor_across"],
    "corridor_rest": ["corridor_rest"],
    "corridor_outside_bz": ["corridor_across", "corridor_rest"],
    "communities": ["communities"],
    "tambopata_nr": ["tambopata_nr"],
    "rest_mdd": ["rest_mdd"],
}
UNIT_NAME = {
    "tambopata_bz": "Tambopata buffer zone", "lapampa": "La Pampa sector",
    "tambopata_bz_rest": "Rest of Tambopata buffer zone", "amarakaeri_bz": "Amarakaeri buffer zone",
    "corridor_across": "Corridor across the road", "corridor_rest": "Rest of the mining corridor",
    "corridor_outside_bz": "Mining corridor outside buffer zones", "communities": "Native communities",
    "tambopata_nr": "Tambopata National Reserve", "rest_mdd": "Rest of Madre de Dios",
    "mdd": "Madre de Dios (department)",
}

# Tenure tag (who may mine where), crossed with every zone. Communities before the corridor (MAAP #208 reports
# community mining separately; some concessions lie inside communities).
TENURE = {0: "none", 1: "corridor", 2: "kotsimba", 3: "community"}

# SERNANP buffer-zone precedence where official polygons overlap (MapBiomas assigns the Tambopata/Bahuaja-Sonene
# overlap, 42,310 ha, to Tambopata; we do the same and give Amarakaeri the Manu overlap). Others: SERNANP code order.
BZ_PRIORITY = ["RN09", "RC03"]
BZ_CODE = {"tambopata_bz": "RN09", "amarakaeri_bz": "RC03", "bahuaja_bz": "PN08"}


def label(measure: str = "net", unit: str | None = None, period: str | None = None, per_year: bool = True) -> str:
    """Standard label: '<measure>, <unit name>, <period>, ha/yr'. Use it in every axis, subtitle and table head."""
    parts = [MEASURE_NAME[measure]]
    if unit:
        parts.append(UNIT_NAME.get(unit, unit))
    if period:
        parts.append(period_label(period) if period in PERIODS else period)
    return ", ".join(parts) + (", ha/yr" if per_year and measure != "stock" else ", ha" if measure == "stock" else "")

# ONE "Amazon" filter for buffer-zone pools (review X7 found three): SERNANP codes of buffer zones whose mapped
# mining lies in lowland/forest Amazon. Excludes coastal and high-Andean zones (Lachay, Huascaran, Junin, Cotahuasi,
# Nor Yauyos, Calipuy, Rio Abiseo).
AMAZON_BZ = {"RN09", "RC03", "PN08", "RN10", "PN09", "BP06", "RN08", "RC02"}
MIN_PRE_HA = 10.0                      # "zone with real mining": mean net additions 2014-18 above this (scaled tests)
