#%%
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 09:35:34 2022

@author: fs.egb

Look at html and build the relevant cols.
"""

from pathlib import Path
import random
import pandas as pd
import numpy as np
import json
pd.options.mode.chained_assignment = None  # default='warn'
import pickle
from unidecode import unidecode
# import re
import manage_entities
# from shapely.geometry import MultiPolygon



import orga_classifier.impute_orga_type as impute_orga_type
import firm_register


import handle_html
import secondary_firm_data
import corpus_translation

import flexi


HERE = Path(__file__).parent.parent.absolute()


def get_largest_file_number(HERE):
    p = Path(HERE/Path("data","raw", "pandora_raw_html")).glob('**/*')
    files = [x for x in p if x.is_file()]
    files = [x.stem for x in files]
    files = [x[3:] for x in files]
    files = [int(x) for x in files]
    max_ = max(files) +1
    print(f"largest ID is {max_} \n")
    return max_

def load_html(sample_faction, HERE):
    range_ = range(1, get_largest_file_number(HERE))
    sample = random.sample(range_, int(len(range_)/int(sample_faction)))
    fetch, id_multi_tab = handle_html.get_columns(sample, HERE)

    secondary_fetch = handle_html.check_for_additional_tables(list(id_multi_tab), HERE)
    fetch.update(secondary_fetch)

    df = pd.DataFrame.from_dict(fetch).T
    #  use unique ids (duplicates due to pandorra structure)
    df = df.drop(columns = ['ID do Registo'])
    df.index.names = ['ID do Registo']

    return df


def load_other_data(HERE):
    l_p = HERE/Path("data")
    keywrds = pd.ExcelFile(l_p/Path("raw","keywords",
                "all_keywords_mapper.xlsx"))

    adm_information = {}
    with open(l_p/Path("raw","municipios","municipios_mz.pickle"),"rb") as f:
        adm_information['municipios'] = pickle.load(f)

    with  open (l_p/Path("external","adm",
                             "moz_admbnda_adm3_ine_20190607.json"), "r") as f:
        adm_information['adm3'] = json.loads(f.read())

    return keywrds, adm_information



def store_files(df, entity_mapper, HERE):
    df.to_pickle(HERE/Path("data","interim","firmregister_full.pkl"))
    with open(str(HERE/Path("data","interim","entity_mappings.pkl")), 'wb') as handle:
        pickle.dump(entity_mapper, handle, protocol=pickle.HIGHEST_PROTOCOL)



def export_firms_to_stata(df, HERE):
  df = (df
  .assign(owner_id = lambda x: x['owner_id'].apply(lambda x: "; ".join(x) if isinstance(x, list) else x))
  .rename(columns={"Beneficial owner": "Beneficial_owner"})
  .applymap(lambda x: unidecode(x) if isinstance(x, str) else x)
  .reset_index()
  .drop(columns = ['ID do Registo','imputed_adm'])
  .assign(person_shares = lambda x: "; ".join(x['person_shares']) if isinstance(x['person_shares'], list) else x['person_shares'])
  .assign(institution_shares = lambda x: "; ".join(x['institution_shares']) if isinstance(x['institution_shares'], list) else x['institution_shares'])
  .astype(str)
  )



  df.to_stata(Path(HERE/Path("data","processed","firmregister_full.dta")), version=117)

  print("Stata export done")
  return






#%%

def main():


#%%

    """
    convert html pages (bulletin entries from Pandorra Box) ->  firm register
        (unique firms with one or more entries in bulletin)

    """
    # use sample_faction to test code snippets 1 = 100 % .

    raw = load_html(sample_faction = 1, HERE = HERE)
    keywrds, adm_information = load_other_data(HERE)


    # raw entries for documentation of input data
    raw.to_pickle(HERE/Path("data","interim","raw_bulletin.pkl"))




    y_i = range (1975, 2023, 1)


    df = (
        raw
        .pipe(firm_register.define_annoucment,keywrds)
        .pipe(firm_register.find_nuits, HERE)
        .pipe(firm_register.norm_all_names)
        .pipe(impute_orga_type.main, bayes_classifier = False)
     #   .pipe(corpus_translation.update_corpus_translation, HERE)
          )

    df, entity_mapper = secondary_firm_data.entity_mappings(df,keywrds)

    df = (
        df.pipe(firm_register.replace_date)
            .pipe(firm_register.map_anything_on_adm_names, adm_information)
            .pipe(firm_register.translate_capital)
            .pipe(firm_register.define_year, y_i)
            # .drop(columns=['Date of writing',
            #              'Place and date of signature','Place of the seat',
            #              'adm_level','Place of signature', 'primary_location',
            #              'adm_location',
            #              'Announcement of', 'Published in', 'orga_entity'])
        )


    entity_mapper['individual_mappings'], df  = manage_entities.map_individual_characteristics(HERE,df)


    name_mapper = entity_mapper['individual_mappings'].set_index("raw")['id'].to_dict()

    name_mapper = {k:v for k,v in name_mapper.items() if v !="person__165346"}


    df['full_owner'] = df['full_owner'].fillna("[]")

    df['owner_id'] = df['full_owner'].apply(lambda x:[name_mapper[l] for l in x if l in name_mapper.keys()] )


    df['owner_id'] = df['owner_id'].apply(lambda x: "; ".join(x) if isinstance(x, list) else np.nan)


    df = df.drop(columns=['owner'])

    df['full_owner'] = df['full_owner'].apply(lambda x: "; ".join(x) if isinstance(x, list) else np.nan)


    store_files(df, entity_mapper, HERE)




    from unidecode import unidecode
    # TODO: Check if this is all right and format code to export the entity mappings for transaperencz. Unidecode all columns in the dataframe
    indivdual_df = df.applymap(lambda x: unidecode(x) if isinstance(x, str) else x)
    data_dir = '../data/processed'
    indivdual_df.to_stata(os.path.join(data_dir, 'individual_mappings.dta'))


    export_firms_to_stata(df.drop(columns=['Beneficial owner']), HERE)


    print("done")





#%%


if __name__== "__main__":
    main()






# %%
