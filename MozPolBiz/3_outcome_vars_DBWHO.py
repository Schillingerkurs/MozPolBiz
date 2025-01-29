# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 18:23:28 2022

@author: fs.egb
"""


from pathlib import Path
# import re
import pandas as pd
# import json
pd.options.mode.chained_assignment = None  # default='warn'
import pickle
from unidecode import unidecode
import networkx as nx
import sys
# import owner
# import manage_pep_data

HERE = Path(__file__).parent.parent.absolute()

print(HERE)

from collections import Counter

import numpy as np
sys.path.insert(0, str(HERE/Path("src", "features")))

#own modules
import network
# import owner
import setup_panel
import export
import ids
import dbwho_specs




def load_data(HERE):
    # load most recent df
    lp =  HERE/Path("data","interim")

    with open(lp/Path("entity_mappings.pkl") , 'rb') as f:
        entity_mapper = pickle.load(f)

    with open(lp/Path("firmregister_full.pkl"), 'rb') as f:
       df = pickle.load(f)

    return df, entity_mapper


def firms_per_entity_type(panel, y_i, df):
    """
    counts  seperatly
    'sociedade por quotas','sociedade individual' and
    'sociedade anonima'

    """
    frames = []
    for y in y_i:
        temp = df[df['y']<= y]
        sub_p = panel[panel['y']== y]
        for orga in ['sociedade por quotas','sociedade individual',
                   'sociedade anonima']:
            all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(temp[temp['orga_type']== orga])
            length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
            sub_p[orga] = sub_p['id'].map(length)

        frames.append(sub_p)

    out_panel = pd.concat(frames)
    out_panel = out_panel.drop(columns = ['id','y'])

    return out_panel




def main_outcomes(panel, y_i,df):
    """
    get number of private entities per period
    calculate network
    get network centralities per period
    """
    frames = []
    graphs = {}
    for y in y_i:
        print(f"panel {y}")
        temp = df[df['y']<= y]
        sub_p = panel[panel['y']== y]
        private = ['sociedade por quotas','sociedade individual',
                   'sociedade anonima']
        private_firms = temp[temp['orga_type'].isin(private)]

        all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(private_firms)

        length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
        sub_p["private_companies"] = sub_p['id'].map(length)
        G = network.create_undirected_network(all_entitiy_reg, firm_dict)
        graphs[y] = G
        centralities = network.collect_centralities(G)
        all_ = sub_p.merge(centralities, left_on = 'id', right_index = True , how = "left")
        frames.append(all_)


    out_panel = pd.concat(frames)

    return out_panel, graphs





# def cntr_vars(df, panel, y_i):
#     frames = []
#     for y in y_i:
#         temp = df[df['y']<= y]
#         sub_p = panel[panel['y']== y]
#         for orga in ['sociedade cooperativa','representacao comercial',"fundacao","associacao"]:
#             all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(temp[temp['orga_type']== orga])
#             length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
#             sub_p[orga] = sub_p['id'].map(length)

#         frames.append(sub_p)

#     panel = pd.concat(frames)
#     panel = panel.drop(columns = ['id','y'])
#     return panel



def dwbho_cntr_vars(df, panel, y_i):
    frames = []
    for y in y_i:
        temp = df[df['y']<= y]
        sub_p = panel[panel['y']== y]
        for orga in ['registration','alteration',"closure"]:
            all_entitiy_reg, firm_dict = setup_panel.get_owner_reg(temp[temp['annoucment']== orga])
            length =  {k: len(v) for k,v in  all_entitiy_reg.items()}
            sub_p[orga] = sub_p['id'].map(length)

        frames.append(sub_p)

    panel = pd.concat(frames)
    panel = panel.drop(columns = ['id','y'])
    return panel


def get_componts(graphs,HERE):
    largest, second = {},{}
    for y in graphs:
        t = [len(x)/len(graphs[y]) for x in nx.connected_components(graphs[y])]
        t.sort()
        largest.update({y:t[-1]})
        second.update({y:t[-2]})

    las_comp = list(set([len(x) for x in nx.connected_components(graphs[max(graphs.keys())])]))
    las_comp.sort()

    largest.update({'last_component':las_comp[-1]})

    second.update({'last_component':las_comp[-2]})


    out =  (pd.DataFrame.from_dict(largest, orient = 'index')
        .assign(second_largest = lambda x: x.index.map(second))
        .rename(columns = {0:"largest"})
        .reset_index()
        .assign(index = lambda x: x['index'].astype(str))
        .set_index('index')
        )

    out.to_stata(HERE/Path("data","processed","dstrb_components.dta"))







def get_blltn_descriptives(df):

    unneeded = ['Agriculture','Communications/Media','Fisheries',
                'Manufacturing', 'Real estate','water/recycling ',
                'Tourism/Entertaiment/restaurants','partiees/unions']

    inst_mapper = dict(zip(df.index, df['inst_owner_norm']))
    inst_mapper =  {k: len(v.split(",")) for k,v in inst_mapper.items() if isinstance(v,str)}



    df['all_owner_ids'] = df['all_owner_ids'].replace( '',np.nan, regex=True)
    private_owner = dict(zip(df.index, df['all_owner_ids']))
    private_owner =  {k: len(v.split(",")) for k,v in private_owner.items() if isinstance(v,str)}




    desc_blltn = (
        pd.get_dummies(df[['Companyname','y','industry_primary','firm_id',
               'orga_type','annoucment']].drop_duplicates('firm_id'),
                        columns=['industry_primary', 'annoucment', 'orga_type'],
                        prefix='', prefix_sep='')

        .assign(no_inst_owner = lambda x: x.index.map(inst_mapper))
        .assign(no_private_owner = lambda x: x.index.map(private_owner))
        .reset_index()


        .assign(temp = lambda x : x[unneeded].sum(axis=1))

        .rename(columns= {'sociedade por quotas':'firm_multi',
                           'sociedade anonima':'firm_anonymous',
                            'sociedade individual':'firm_single',
                            'partido politico': 'pol_party',
                            "y":"year"})

        .assign(Companyname = lambda x : (x['Companyname'].apply(lambda y:
                                         unidecode(y))))
        .assign(unclassified = lambda x : x[['unclassified','temp']].sum(axis=1))

        .drop(columns = unneeded+['firm_id','ID do Registo','sociedade cooperativa',
              'representacao comercial','contrato de consorcio',
              'temp'])

        .fillna(0))

    desc_blltn.to_stata(HERE/Path("data","processed", "bulletin_entries.dta"))




def main():
    y_i = range(1989,2021,5)
    id_level = ['id',"family"]

    description = {}


    keyword_dict = pd.ExcelFile(HERE/Path("data","raw","keywords",
                "all_keywords_mapper.xlsx"))


    for id_ in id_level:

        firms, entity_mapper = load_data(HERE)
        df = ids.manage_ids_in_bulletin(firms, entity_mapper, level = id_)

        df = dbwho_specs.map_industry_keywords(df, keyword_dict)

        name_ids = entity_mapper['individual_mappings'][id_].unique()

        panel = setup_panel.get_panel_identifier(y_i, name_ids)

        f_e = firms_per_entity_type(panel, y_i, df)
        f_all, graphs = main_outcomes(panel, y_i, df)

        f_all = setup_panel.count_dbwho_contolls(df,f_all, y_i)


        if id_ == 'id':
            get_componts(graphs,HERE)
            family_partner = network.count_family_business_partners(graphs, HERE,
                                                                    panel,entity_mapper)

        f_industries = setup_panel.count_dbwho_industries(df, panel, y_i)
        cntrl_panel = dwbho_cntr_vars(df, panel, y_i)

        full_panel = (f_e
                    .merge(f_all, left_on = 'm', right_on = 'm')
                    .merge(f_industries, left_on = 'm', right_on = 'm')
                    .merge(cntrl_panel, left_on = 'm', right_on = 'm')
                    # .assign(family_prtnr1 = lambda x: x['m'].map(family_partner))
                    )

        full_panel = setup_panel.first_firm(full_panel,df)
        full_panel = full_panel.drop(columns = ['m'])
        full_panel = full_panel.dropna(subset = ['first_firm'])

        full_panel = export.dbwho_missing_cols(full_panel, HERE)

        export.export_DBWHO_outcomes(full_panel = full_panel,
                            filename = f"outcome_vars_{id_}",
                            HERE = HERE)

        description[id_] = full_panel.describe().T

        print(f"done with {id_}")



if __name__ == "__main__":
    main()
    print("done with all outcomes")