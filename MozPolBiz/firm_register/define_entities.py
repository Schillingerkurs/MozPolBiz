# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 13:37:34 2022

@author: fs.egb

define firm_ids
"""

# from collections import Counter
# from prettytable import PrettyTable
# from unidecode import unidecode
from string_grouper import match_strings, group_similar_strings
# from pathlib import Path

# from matplotlib_venn import venn3
import pandas as pd

# import matplotlib
# import plotly.graph_objects as go



import firm_register as f_r

def entity_id(nuels,orge_enty):
    all_ids = nuels.copy()
    all_ids.update(orge_enty)
    id_mapper = {}
    for number,e  in enumerate(set(all_ids.values())):
        id_mapper[e] = number

    all_ids = {k: id_mapper[v] for k, v in all_ids.items()}

    return all_ids

def fill_nuel_id(df):
    """
    Fill in NUEL_ID if orga_entity is identical and NUEl missing

    """
    t = dict(df.groupby('orga_entity')['NUEL_id'].unique())
    t = {k: list(v) for k, v in t.items()}

    t = {k: [x for x in v if isinstance(x,str)] for k, v in t.items()}

    mapper = {k: "".join(v) for k, v in t.items() if len(v) == 1}

    df['NUEL_id']  = df['NUEL_id'].fillna(df['orga_entity'].map(mapper))
    return  df


def get_dict_of_nuels(df):
    """ get dict of nuel per row"""
    nuels = dict(zip(df.index, df['NUEL_id']))
    nuels = {k: v for k, v in nuels.items() if isinstance(v,str)}
    nuels = {k: v for k, v in nuels.items() if v != "expl no nuel or nuit"}
    print(f'{len(nuels)} rows have a nuel_id \n')
    return nuels



def define_entities(df):
    """
    1. Leverage NUEL/NUIT (id), orga type and Comapanynames
    to define unique entities (both companies and institutional owners)

    2. unique NUEL/ NUIT -> unique entity
    3. unique entity name PER orga type ->  unique entity

    4. Instiutional owner has same name as entitiy -> Map unique entity as owners

    """

    nuels =  get_dict_of_nuels(df)

    no_id_yet = set(df.index) - set(nuels)
    df['orga_entity'] = df['norm_name'] +"_" + df['orga_type']

    df = fill_nuel_id(df)

    nuels =  get_dict_of_nuels(df)

    orge_enty = dict(zip(df.index, df['orga_entity']))
    orge_enty = {k: v for k, v in orge_enty.items() if k in  no_id_yet}

    all_ids =  entity_id(nuels,orge_enty)

    df['entity_id'] = df.index.map(all_ids)


    comn = df.groupby('entity_id')['Companyname'].unique()

    comn = {k: list(v) for k,v in comn.items()}

    old_c = df.groupby('entity_id')['Old name(s)'].unique()
    old_c = {k: list(v) for k,v in old_c.items() }
    old_c = {k: [x for x in v if isinstance(x,str)] for k,v in old_c.items() }
    old_c = {k: list(v) for k,v in old_c.items() if v!=[] }


    new_c = df.groupby('entity_id')['New name'].unique()
    new_c = {k: list(v) for k,v in new_c.items() }
    new_c = {k: [x for x in v if isinstance(x,str)] for k,v in new_c.items() }
    new_c = {k: list(v) for k,v in new_c.items() if v!=[] }

    for c in list(comn):
        if c in list(old_c):
            comn[c].extend(old_c[c])
        if c in list(new_c):
            comn[c].extend(new_c[c])

    entity_mapper = {k: list(set(v)) for k,v in comn.items()}


    raw_entity_id = {}
    for k in entity_mapper:
        for x in entity_mapper[k]:
            raw_entity_id[x] = k

    # raw_entity_id = {k: f"bltn_{v}" for k,v in raw_entity_id.items()}
    return df, raw_entity_id



def get_id_for_unknown_institutions(i_p_mapper):


    unknown_entities = {k: [x for x in v  if isinstance(x,str)]
                        for k,v in i_p_mapper.items() }

    unknown_entities = {k: v for k,v in unknown_entities.items() if v }

    unique_inst_owners = set()
    for e in unknown_entities:
        for firm in unknown_entities[e]:
            unique_inst_owners.add(firm)



    inst_mapper = f_r.fuzzy_entity_norm(pd.Series(list(unique_inst_owners)))


    inst_ids = {s: s for s in list(set(inst_mapper.values()))}

    for n, k in enumerate(inst_ids):
        inst_ids[k] = n


    inst_mapper = {k: f"inst_{inst_ids[v]}" for k,v in inst_mapper.items()}
    inst_mapper= finetune_instituion_mapper(inst_mapper)


    i_p_mapper  = {k: [inst_mapper[x] if x in list(inst_mapper) else x
                    for x in v] for k,v in i_p_mapper.items()}


    return i_p_mapper, inst_mapper


def get_corpus_all_enties(entity_mapper):
    t = list(entity_mapper['bulletin_entities'])
    t.extend(entity_mapper['insitutions_enties'])

    corpus = {k:f_r.norm_firm_names(k) for k in t}
    corpus = {k:f_r.lemmatizing_entity_names(v) for k,v in corpus.items()}
    corpus = {k:f_r.remove_orga_string(v) for k,v in corpus.items()}

    return  corpus



def get_all_entitiy_mapper(entity_mapper):

    all_entity_mapper = {}
    for k in entity_mapper:
        all_entity_mapper.update(entity_mapper[k])

    entity_mapper['all_entity_mapper'] = all_entity_mapper

    return entity_mapper



def finetune_instituion_mapper(old_mapper):
    """ remove orga types from strings match with lower fuzzy treshold"""

    instution = pd.DataFrame.from_dict(old_mapper,
                                   orient = 'index')

    instution = instution.reset_index().set_index(0)
    instution.columns = ['string']
    treshold = 0.85
    instution['w_o_orga'] = instution['string'].apply(lambda x: f_r.remove_orga_string(x))
    instution['fuzz'] = group_similar_strings(instution['w_o_orga'],
                                              min_similarity = treshold,
                                               )


    ids = {s: f"inst_{n}" for n, s in enumerate(instution['fuzz'].unique())}

    instution['new_id'] = instution['fuzz'].map(ids)

    new_mapper =  dict(zip( instution['string'],instution['new_id']))

    return new_mapper



def process_institution_entities(df, entity_mapper):
    """
    map Mozambican businesses on the normalize + lemmatized insitutional owners
    add institutional owners w/o to entitiy mapper



    Institutional owners are sepearted by  columns, but so are name/company tape

    entity mapper includes therefor only processed entity types, no raw strings
    for instituions.

    """

    raw_entity_id = entity_mapper['bulletin_entities']

    entity_lemma =  {f_r.norm_firm_names(k) : v for k, v in raw_entity_id.items()
                 if isinstance(k,str)}

    entity_lemma =  {f_r.lemmatizing_entity_names(k) : v for k, v in entity_lemma.items() }


    temp = df[['Institution owner','Previous members institutions']].copy()
    temp = temp.dropna(thresh=1)
    temp['Institution owner'] = temp['Institution owner'].fillna("")
    temp['Previous members institutions'] = temp['Previous members institutions'].fillna("")

    temp['all_institutions'] =   temp['Institution owner'] +  ", " + \
                                temp['Previous members institutions']

    temp['all_institutions'] =  temp['all_institutions'].str.strip(" ")
    temp['all_institutions'] =  temp['all_institutions'].str.strip(",")
    temp['all_institutions'] =  temp['all_institutions'].str.strip(";")
    temp['all_institutions'] =  temp['all_institutions'].str.strip(" ")


    i_p = dict(zip(temp.index, temp['all_institutions']))
    i_p = {k: f_r.norm_firm_names(v) for k, v in i_p.items() if isinstance(v,str)}

    share = len(i_p)/len(df)*100
    # print(f"{share:%.2f}")
    print(round(share,2),"% of the entities have an institutional owner")


    i_p =  {k: f_r.lemmatizing_entity_names(v)  for k, v in i_p.items() }


    i_p = {k: v.split(", ") for k, v in i_p.items()}
    i_p = {k: [x.strip(";") for x in v ]for k, v in i_p.items()}
    i_p = {k: [x.strip() for x in v ]for k, v in i_p.items()}

    i_p = {k: list(set(v)) for k, v in i_p.items()}
    i_p = {k: [str(x) for x in v if x != ''] for k, v in i_p.items()}

    i_p_mapper  = {k: [entity_lemma[x] if x in list(entity_lemma) else x
                       for x in v] for k,v in i_p.items()}


    i_p_mapper, inst_mapper =  get_id_for_unknown_institutions(i_p_mapper)

    i_p_mapper = {k: [str(x) for x in v]for k,v in  i_p_mapper.items()}
    i_p_mapper = {k: ", ".join(v) for k,v in  i_p_mapper.items()}

    entity_mapper['insitutions_enties'] = inst_mapper

    df['inst_owner_norm'] = df.index.map(i_p_mapper)


    entity_mapper = get_all_entitiy_mapper(entity_mapper)
    entity_mapper['corpus'] = get_corpus_all_enties(entity_mapper)

    return df, entity_mapper




