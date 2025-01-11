# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 10:31:26 2022

@author: fs.egb

find NUEL or NUIT as a first identifier
"""


from unidecode import unidecode
# import matplotlib
import plotly.graph_objects as go

import re
import pandas as pd
from pathlib import Path

import plotly.io as pio


def drop_empty_vales(dict):
    return {k:",".join(v) for k,v in dict.items() if v != []}


def check_for_hidden_ids(df):
    exclude = ['NUEL\xa0ou Nº Registo antigo','New name','NUIT',
               'person_shares','institution_shares']
    cols = [x for x in df.keys() if x not in exclude]
    temp = df[cols].copy()
    for e in cols:
        temp[e] = temp[e].apply(lambda x : str(x))

    one = temp[cols].T.agg(",".join).to_dict()
    one = {k: unidecode(v.lower()) for k,v in one.items()}


    passport = {k:  re.findall("passaporte", v) for k,v in one.items()}
    passport = drop_empty_vales(passport)

    nuel = {k: re.findall("nuel ", v) for k,v in one.items()}
    nuel =  drop_empty_vales(nuel)
    # Regex to find all digits with the legth  9
    nuel_digit = {k:  re.findall("\d{9}", v) for  k, v in one.items() if k in list(nuel)}
    nuel_digit = drop_empty_vales(nuel_digit)

    no_nuel = {k:  re.findall('consta o nuel e o nuit', v) for k,v in one.items()}
    no_nuel = drop_empty_vales(no_nuel)

    infos = {k: "expl no nuel or nuit" for k in list(no_nuel)}
    len(infos)
    infos.update(nuel_digit)

    return infos


def find_nuits(df,HERE):
    all_nuel = check_for_hidden_ids(df)
    id_nuel = dict(zip(df.index, df['NUEL\xa0ou Nº Registo antigo'] ))
    id_nuel = {k: v.strip() for k,v in id_nuel.items() if str(v).isdigit()}
    nueL_in_new_names =  dict(zip(df.index, df['New name'] ))
    nueL_in_new_names = {k: v for k,v in nueL_in_new_names.items() if str(v).isdigit()}
    id_nuel.update(nueL_in_new_names)
    all_nuel.update(id_nuel)
    df['NUEL_id'] = df.index.map(all_nuel)
    dfp = pd.DataFrame(columns= ["organization", "share_w_o_nuit"])
    for t in df['orga_type'].unique():
        temp = df[df['orga_type'] == t]

        share = temp['NUEL_id'].isna().sum()
        share = round(share/len(temp),2)

        df_length = len(dfp)
        dfp.loc[df_length] = t, share

    latex_mining =  dfp.style.format(precision=3).to_latex()
    table_path = Path(HERE) / Path("reports", "tables", "bulletin_parser","orgas_w_o_nuel.tex")

    print(f"saved plot in {table_path}")

    if not table_path.parent.exists():
        table_path.parent.mkdir(parents=True, exist_ok=True)

    with open(table_path, 'w') as f:
        f.write(latex_mining)



    df["ID status"] = "known"
    df.loc[df['NUEL_id'].isna(), "ID status"]  = "unknown"
    df.loc[df['NUEL_id']=='expl no nuel or nuit', "ID status"]  = "expl_not"


    # fig.write_html(str(plot_path/Path("orgas_w_o_nuel.html")))

    return df


