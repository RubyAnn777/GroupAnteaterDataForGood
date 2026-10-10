"""IBAMA notices of infraction (autos de infracao), annual table 2014-2025.

Rebuilds the table from the raw zip when it exists (data_raw/ibama/auto_infracao_csv.zip, 117 MB, git-ignored,
link in DOWNLOAD_LOG), and writes the committed intermediate data_intermediate/ibama_autos_annual.csv.
If the zip is missing, reads the intermediate and prints a warning.

Filters: SIT_CANCELADO == "N" (not cancelled); year of DAT_HORA_AUTO_INFRACAO == year of the file.
Legal Amazon = autos whose UF is AC AP AM MA MT PA RO RR TO. All types of autos (fines, warnings) are counted.
Mining flag = NOISY regex on the accent-stripped lower-case text of DES_INFRACAO + DES_AUTO_INFRACAO
(see MIN below). It will include some non-mining autos and miss autos with generic text. Description only.
"""
from __future__ import annotations
import re, unicodedata, zipfile
import pandas as pd
from common import ROOT

ZIP = ROOT / "data_raw" / "ibama" / "auto_infracao_csv.zip"
INTERMEDIATE = ROOT / "data_intermediate" / "ibama_autos_annual.csv"
NOTES_REF = ROOT / "docs" / "overnight" / "notes" / "ibama_annual.csv"
YEARS = range(2014, 2026)
COLS = ["SIT_CANCELADO", "DAT_HORA_AUTO_INFRACAO", "UF", "DES_INFRACAO", "DES_AUTO_INFRACAO",
        "DES_LOCAL_INFRACAO", "DS_BIOMAS_ATINGIDOS", "OPERACAO"]
MIN = re.compile(r"garimp|lavra|minerio|mineracao|extracao mineral|extrair.*(ouro|minerio|mineral)|\bouro\b|"
                 r"cassiterita|dragagem|recursos minerais|bens minerais|permissao de lavra|ccaa|mercurio")
IND = re.compile(r"terra indigena|terras indigenas|\bti\b|indigena|yanomami|munduruku|kayapo|raposa serra")
AML = {"AC", "AP", "AM", "MA", "MT", "PA", "RO", "RR", "TO"}

def _norm(s: pd.Series) -> pd.Series:
    return s.fillna("").map(lambda x: unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower())

def rebuild(zip_path=ZIP) -> pd.DataFrame:
    rows = []
    with zipfile.ZipFile(zip_path) as zf:
        for y in YEARS:
            with zf.open(f"auto_infracao_{y}.csv") as fh:
                d = pd.read_csv(fh, sep=";", dtype=str, usecols=COLS, encoding_errors="replace")
            d["yr"] = pd.to_numeric(d["DAT_HORA_AUTO_INFRACAO"].str[:4], errors="coerce")
            d = d[(d.SIT_CANCELADO == "N") & (d.yr == y)]
            txt = _norm(d.DES_INFRACAO) + " | " + _norm(d.DES_AUTO_INFRACAO)
            loc = txt + " | " + _norm(d.DES_LOCAL_INFRACAO) + " | " + _norm(d.OPERACAO)
            d = d.assign(mining=txt.str.contains(MIN), ind=loc.str.contains(IND),
                         aml=d.UF.isin(AML), amz=d.DS_BIOMAS_ATINGIDOS.fillna("").str.contains("Amazonia"))
            r = dict(year=y, n_all_brazil=len(d), n_legal_amazon_states=int(d.aml.sum()),
                     n_amazon_biome=int(d.amz.sum()), n_mining_brazil=int(d.mining.sum()),
                     n_mining_legal_amazon=int((d.mining & d.aml).sum()))
            for u in ["RR", "PA", "AM"]:
                r[f"n_all_{u}"] = int((d.UF == u).sum()); r[f"n_mining_{u}"] = int((d.mining & (d.UF == u)).sum())
            r["n_indigenous_text_legal_amazon"] = int((d.ind & d.aml).sum())
            r["n_mining_and_indigenous_text_brazil"] = int((d.mining & d.ind).sum())
            r["n_mining_and_indigenous_text_legal_amazon"] = int((d.mining & d.ind & d.aml).sum())
            rows.append(r)
    return pd.DataFrame(rows)

def load() -> tuple[pd.DataFrame, str]:
    """Returns (table, how) with how in {'rebuilt', 'intermediate'}."""
    if ZIP.exists():
        t = rebuild()
        INTERMEDIATE.parent.mkdir(exist_ok=True)
        t.to_csv(INTERMEDIATE, index=False)
        if NOTES_REF.exists():
            ref = pd.read_csv(NOTES_REF)
            pd.testing.assert_frame_equal(t.reset_index(drop=True), ref.reset_index(drop=True), check_dtype=False)
            print("OK   IBAMA rebuilt table equals docs/overnight/notes/ibama_annual.csv")
        return t, "rebuilt"
    print(f"WARNING: {ZIP.relative_to(ROOT)} not found; using committed intermediate "
          f"{INTERMEDIATE.relative_to(ROOT)} (not rebuilt from raw).")
    return pd.read_csv(INTERMEDIATE), "intermediate"
