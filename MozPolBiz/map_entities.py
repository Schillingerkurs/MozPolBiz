# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 17:17:57 2022

@author: fs.egb
"""


from pathlib import Path
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import pickle

from string_grouper import group_similar_strings, match_strings

from unidecode import unidecode
# own modules
import owner
# import test_name_mapper
import firm_register
import secondary_firm_data
import manage_entities
import flexi 



HERE = Path(__file__).parent.parent.parent.absolute()

print(HERE)   

def load_reg_and_mapper(HERE):
    lp = HERE/Path("data","interim")
    bulletin = pd.read_pickle(lp/Path( "firmregister_full.pkl"))
    with open(lp/Path("entity_mappings.pkl"), 'rb') as f:
       ent_mapper = pickle.load(f)
       
    with open(HERE/Path("data","interim",
                        "orbis_entries","orbis_data_MZ.pickle"), 'rb') as f:
        orbis = pickle.load(f)
        
    wb_lp =  HERE/Path("data","external", "worldbank",
                              "Major_Contract_Awards_WB.csv")
    
    wb = pd.read_csv(wb_lp)
    
    wb = wb[wb['Borrower Country']== 'Mozambique']
    return bulletin, ent_mapper, orbis, wb


def load_keywords(HERE):
    keywrds = pd.ExcelFile(HERE/Path("data","raw","keywords","all_keywords_mapper.xlsx")) 



    return keywrds


# TODO: add hand matching mandate. 
# TODO: include business tychoons (listed in keywords)



bulletin, entity_mapper, orbis, wb  =  load_reg_and_mapper(HERE)   
keywrds = load_keywords(HERE)

entity_mapper['individual_mappings']  = manage_entities.map_individual_characteristics(HERE)
    

# ####################


# flexi_names = flexi.select_flexi(HERE)


# flexi_mapper, indiv_mapper = secondary_firm_data.flexicadastre_mapping(keywrds, flexi_names[0], entity_mapper)


# indi_apirs = pd.DataFrame([f for t in [[(k,x) for x in v] for k,v in indiv_mapper.items() ]
#               for f in t], columns = ['raw', 'id'])



# other =   manage_entities.other_name_characteristics(HERE)

# felxi_base = owner.get_name_base(list(indi_apirs['raw']), other)
# felxi_base = owner.get_og_network(bulletin, felxi_base)

# (pd.concat([entity_mapper['individual_mappings'] ,felxi_base])
# .to_csv(HERE/Path("data","processed",'name_mappings.csv'), index=False ))



# ####################
# # base = entity_mapper['individual_mappings'] 
# # check = dict(zip(base['id'], base['raw']))

# # indi_apirs = indi_apirs.assign(check = lambda x : x['id'].map(check))


# entity_mapper['flexi_mapper'] = flexi_mapper

# entity_mapper['corpus'] = manage_entities.get_corpus_all_enties(entity_mapper)

# entity_mapper = manage_entities.get_all_entitiy_mapper(entity_mapper)


# # orbis , WorldBank

# corpi = pd.Series(entity_mapper['corpus'])

# orbi = (
#         orbis
#         .assign(name_clean =  lambda x : x['name_native'].map(\
#             firm_register.dict_norm(orbis['name_native'])))
#         .assign(deduplicated_name = lambda x:\
#                 group_similar_strings(x['name_clean'],
#                       ignore_index=True),
#                 min_similarity = 0.85)
#         .drop_duplicates(subset = ['name_native'])
#         .set_index('name_native')
#           ['deduplicated_name']
#           )

    
    
# fuzzy_mapper = (match_strings(orbi, corpi, min_similarity = 0.85)
#                 .groupby("left_name_native")['right_index'].unique()
#                 .to_dict()
#                 )

# entity_mapper['orbis'] = {k: [entity_mapper['all_entity_mapper'][x] for x in v] 
#                 for k,v in fuzzy_mapper.items()}



# wb_mapper =   firm_register.dict_norm(wb['Supplier'])

# wb = (
#         wb
#         .assign(name_clean =  lambda x : x['Supplier'].map(wb_mapper))
#         .assign(deduplicated_name = lambda x:\
#                 group_similar_strings(x['name_clean'],
#                       ignore_index=True),
#                 min_similarity = 0.85)
#         .drop_duplicates(subset = ['Supplier'])
#         .set_index('Supplier')
#         ['deduplicated_name']
#           )

# fuzzy__wb_mapper = (match_strings(wb, corpi, min_similarity = 0.85)
#                 .groupby("left_Supplier")['right_index'].unique()
#                 .to_dict()
#                 )    
    

# entity_mapper['worldbank'] = {k: [entity_mapper['all_entity_mapper'][x] for x in v] 
#                 for k,v in fuzzy__wb_mapper.items()}

# lp = HERE/Path("data","interim")
# with  open(lp/Path("all_entitiy_mappings.pkl"),'wb') as f:
#     pickle.dump(entity_mapper,f)
 
    
 

