# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 09:53:25 2022

@author: fs.egb
"""
from pathlib import Path
# import random
import pandas as pd
# import json
pd.options.mode.chained_assignment = None  # default='warn'
import pickle
import sys


# import ids



HERE = Path(__file__).parent.parent.absolute()





sys.path.insert(0, str(HERE/Path("src", "features")))

import manage_pep_data
import export
import setup_panel




def load_pep_data(HERE):
    # load all files in pep_directory
    d = HERE/Path("data","external","pep_data")
    pep_mandates = {}
    pep_mandates['CIP3']  = pd.ExcelFile(d/Path("CIP_Borges",
                            "cip3.xlsm")).parse("Sheet1")
    temp = pd.ExcelFile(d/Path("hand_coded_mandates","PEP_database.xlsx"))
    for i in temp.sheet_names:
        pep_mandates[i] = temp.parse(i)

    pep_mandates["lexis"] = pd.read_stata(d/Path("LexisNexis_World_Compliance",\
                                             "mozambique_pep_list.dta"))

    temp = pd.read_csv(d/Path("WhoGov_within_V2.0.csv"), \
                      on_bad_lines = "skip", index_col = 0,
                     low_memory = False, encoding = "iso-8859-1")

    temp = temp[temp['country_isocode'] == "MOZ"]
    pep_mandates["Who_Gov"]  = temp
    return pep_mandates


def load_blltn_and_entities(HERE):
    # load most recent df
    lp = HERE/Path("data","interim")

    with open(lp/Path("entity_mappings.pkl") , 'rb') as f:
        entity_mapper = pickle.load(f)

    with open(lp/Path("firmregister_full.pkl"), 'rb') as f:
       firms = pickle.load(f)

    return firms, entity_mapper




firms, entity_mapper = load_blltn_and_entities(HERE)


name_base =  entity_mapper['individual_mappings']

name_mapper = dict(zip(name_base['raw'],name_base['id']))
# og_mapper = dict(zip(name_base['id'], name_base['og']))


pep_mandates = load_pep_data(HERE)

all_owners = [x for x in name_base['id'].unique() if isinstance(x,str) if x != '']


y_i = range(1962,2023,1)


panel = manage_pep_data.setup_pep_panel(y_i, all_owners, pep_mandates, name_mapper)



pers_char = name_base[['family','gender', 'id', 'lawyer']].drop_duplicates('id')


party_mapper = manage_pep_data.get_party_founders(panel, firms, y_i, entity_mapper)

oppo_mapper = {k: v for k,v in party_mapper.items() if "frelimo" not in v.lower()}

print("starting the panel")
panel_full = (
        panel
        .merge(pers_char, left_on ="id", right_on = "id", how = 'left')
        # .assign(og  = lambda x : x['id'].map(og_mapper))
        .fillna(0)
        .assign(gender  = lambda x : x['gender'].astype(float))
        .assign(lawyer  = lambda x : x['lawyer'].astype(str))
        # .assign(og  = lambda x : x['og'].astype(str))
        .sort_values(by=['y'])
        .assign(opposition_founder  = lambda x : x['m'].map(oppo_mapper))
        .drop(columns = ['m'])  )



# with open(Path.cwd().parent/Path("pipeline","indie_varaibles.pkl"), 'wb') as handle:
#     pickle.dump(panel_full, handle, protocol=pickle.HIGHEST_PROTOCOL)



description = panel_full.describe().T

panel_full = panel_full[panel_full['y']<2020]


panel_full = panel_full.fillna(0)
panel_full['gender'] = panel_full['gender'].apply(lambda x: int(x*100))

panel_full['lawyer'] = panel_full['lawyer'].str.replace("nan", "0")


panel_full = setup_panel.pep_affil_bnz(panel_full,firms, entity_mapper)
panel_full = panel_full.fillna(0)

panel_full = panel_full.drop(columns = [ 'MP','opposition_founder', 'family_old_peps', 'old_pep_business'] )
# panel_full = panel_full.set_index('id')



controll_vars = panel_full[['id', 'family', 'gender', 'lawyer']].drop_duplicates()


treatments = panel_full[['id', 'y', 'Minister', 'Governor', 'Vice-Minister', 'Minister_who_gov', 'cc', 'pb']]


export.export_DBWHO_treatments(treatments, filename = "treatments_vars",
                                HERE= HERE)

export.export_DBWHO_treatments(controll_vars, filename = "controll_vars",
                                HERE= HERE)



export.export_to_panel_folder(export = panel_full,
                    filename = "treatment_individual_vars_1962",
                    HERE = HERE)


