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
import json
pd.options.mode.chained_assignment = None  # default='warn'
import pickle
# import re

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


    fdi_markets = pd.ExcelFile(l_p/Path("external","fdi_markets",
                             "FDImarkets_moz.xlsx")).parse('fDiMarkets')

    fdi_markets.columns = fdi_markets.iloc[1]


    return keywrds, adm_information , fdi_markets,



def store_files(df, entity_mapper, HERE):
    df.to_pickle(HERE/Path("data","interim","firmregister_full.pkl"))
    with open(str(HERE/Path("data","interim","entity_mappings.pkl")), 'wb') as handle:
        pickle.dump(entity_mapper, handle, protocol=pickle.HIGHEST_PROTOCOL)




#%%

def main():


#%%

    """
    convert html pages (bulletin entries from Pandorra Box) ->  firm register
        (unique firms with one or more entries in bulletin)

    """
    # use sample_faction to test code snippets 1 = 100 % .

    raw = load_html(sample_faction = 1, HERE = HERE)
    keywrds, adm_information , fdi_markets, \
                = load_other_data(HERE)


    # raw entries for documentation of input data
    raw.to_pickle(HERE/Path("data","interim","raw_bulletin.pkl"))

    flexi_names, felxi_full = flexi.select_flexi(HERE)



    y_i = range (1975, 2023, 1)


    df = (
        raw
        .pipe(firm_register.define_annoucment,keywrds)
        .pipe(firm_register.find_nuits, HERE)
        .pipe(firm_register.norm_all_names)
        .pipe(impute_orga_type.main, bayes_classifier = False)
     #   .pipe(corpus_translation.update_corpus_translation, HERE)
          )

 #%%
    df, entity_mapper = secondary_firm_data.entity_mappings(df,
                        fdi_markets, keywrds , flexi_names)

#%%
    df = (
        df.pipe(firm_register.replace_date)
            .pipe(firm_register.map_anything_on_adm_names, adm_information)
            .pipe(firm_register.translate_capital)
            .pipe(firm_register.define_year, y_i)
            # .pipe(firm_register.identify_FDI_affiliations,entity_mapper)
            # .drop(columns=['Date of writing',
            #              'Place and date of signature','Place of the seat',
            #              'adm_level','Place of signature', 'primary_location',
            #              'adm_location',
            #              'Announcement of', 'Published in', 'orga_entity'])
        )



    store_files(df, entity_mapper, HERE)


#%%


if __name__== "__main__":
    main()





# %%
