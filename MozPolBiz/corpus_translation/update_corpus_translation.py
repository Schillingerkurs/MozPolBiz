# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 13:43:34 2022

@author: fs.egb
"""

from pathlib import Path
# import re
import pandas as pd
# import json
pd.options.mode.chained_assignment = None  # default='warn'
import pickle

from tqdm import tqdm
import sys
import yaml
# NACE codes
# from stdnum.eu import nace





HERE = Path(__file__).parent.parent.parent.absolute()



# import setup_panel
# import export
# import ids
from deep_translator import DeeplTranslator, GoogleTranslator




def load_translation(HERE):

    files = list(Path(HERE/Path("data","interim", "corpus_translations")).glob('**/*'))
    out = {}
    for fi in files:
        with open(fi , 'rb') as f:
            out[fi.stem] = pickle.load(f)

    return out


def translate_w_deepl(input_list, deepl_translations, config):
    material = [x for x in input_list if x not in deepl_translations.keys()]

    material = [x for x in material if len(x) < 5000]
    out = {}
    for k in  tqdm(material):
        try:
            out[k] = DeeplTranslator(api_key=config.deep_key,
                                  source="pt", target="en",
                                  use_free_api=True).translate(k)
        except ConnectionError:
            print("Connection Error. Probably querry maximum per day ")
            break
        except Exception as e:
            print (f"Unknown error {e}")
            break

    deepl_translations.update({k:v for k, v in out.items() if k != v})

    return deepl_translations





def translate_w_google(input_list, google_dict):

    material = [x for x in input_list if x not in google_dict.keys()]

    material = [x for x in material if len(x) < 5000]
    out = {}
    for k in  tqdm(material):
        try:
            out[k] = GoogleTranslator(source="pt", target="en",
                                     ).translate(k)
        except ConnectionError:
            print("Connection Error. Probably querry maximum per day ")
            break
        except Exception as e:
            print (f"Unknown error {e}")
            break

    google_dict.update({k:v for k, v in out.items() if k != v})

    return google_dict




def update_corpus_translation(df, HERE):

    with open(HERE/Path("data","config.yml"),"r") as file:
            config = yaml.safe_load(file)

    translations = load_translation(HERE)

    google_dict = translations['google_translations']
    deepl_translations = translations['deepl_translations']


    input_list = [x for x in list(df['Social object'].unique()) if isinstance(x,str)]


    google_dict = translate_w_google(input_list, google_dict)
    deepl_translations = translate_w_deepl(input_list, deepl_translations, config)


    corpus_path = HERE/Path("data","interim", "corpus_translations")
    with open(corpus_path/Path("google_translations.pkl"), 'wb') as handle:
        pickle.dump(google_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(corpus_path/Path("deepl_translations.pkl"), 'wb') as handle:
        pickle.dump(deepl_translations, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"saved string translations in {corpus_path}")
    df['corpus_en'] =  df['Social object'].map(google_dict)

    return df
