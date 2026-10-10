import sys,re,unicodedata,pandas as pd
src,out=sys.argv[1],sys.argv[2]
cols=["SIT_CANCELADO","TIPO_AUTO","DAT_HORA_AUTO_INFRACAO","UF","DES_INFRACAO","DES_AUTO_INFRACAO","DES_LOCAL_INFRACAO","UNIDADE_CONSERVACAO","TIPO_INFRACAO","DS_BIOMAS_ATINGIDOS","OPERACAO"]
def norm(s): return s.fillna("").map(lambda x: unicodedata.normalize("NFKD",x).encode("ascii","ignore").decode().lower())
MIN=re.compile(r"garimp|lavra|minerio|mineracao|extracao mineral|extrair.*(ouro|minerio|mineral)|\bouro\b|cassiterita|dragagem|recursos minerais|bens minerais|permissao de lavra|ccaa|mercurio")
IND=re.compile(r"terra indigena|terras indigenas|\bti\b|indigena|yanomami|munduruku|kayapo|raposa serra")
AML={"AC","AP","AM","MA","MT","PA","RO","RR","TO"}
rows=[]; st=[]
for y in range(2014,2026):
    d=pd.read_csv(f"{src}/auto_infracao_{y}.csv",sep=";",dtype=str,usecols=cols,encoding_errors="replace")
    d["yr"]=pd.to_numeric(d["DAT_HORA_AUTO_INFRACAO"].str[:4],errors="coerce")
    d=d[(d.SIT_CANCELADO=="N")&(d.yr==y)]
    txt=norm(d.DES_INFRACAO)+" | "+norm(d.DES_AUTO_INFRACAO)
    loc=txt+" | "+norm(d.DES_LOCAL_INFRACAO)+" | "+norm(d.OPERACAO)
    d["mining"]=txt.str.contains(MIN); d["ind"]=loc.str.contains(IND)
    d["aml"]=d.UF.isin(AML); d["amz"]=d.DS_BIOMAS_ATINGIDOS.fillna("").str.contains("Amazonia")
    r=dict(year=y,n_all_brazil=len(d),n_legal_amazon_states=int(d.aml.sum()),n_amazon_biome=int(d.amz.sum()))
    r["n_mining_brazil"]=int(d.mining.sum()); r["n_mining_legal_amazon"]=int((d.mining&d.aml).sum())
    for u in ["RR","PA","AM"]:
        r[f"n_all_{u}"]=int((d.UF==u).sum()); r[f"n_mining_{u}"]=int((d.mining&(d.UF==u)).sum())
    r["n_indigenous_text_legal_amazon"]=int((d.ind&d.aml).sum())
    r["n_mining_and_indigenous_text_brazil"]=int((d.mining&d.ind).sum())
    r["n_mining_and_indigenous_text_legal_amazon"]=int((d.mining&d.ind&d.aml).sum())
    rows.append(r)
    g=d.groupby("UF").size().rename(y); st.append(g)
    print(y,r,flush=True)
pd.DataFrame(rows).to_csv(out+"/ibama_annual.csv",index=False)
pd.concat(st,axis=1).fillna(0).astype(int).rename_axis("UF").to_csv(out+"/ibama_by_state_year.csv")
