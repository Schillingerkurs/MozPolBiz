# -*- coding: utf-8 -*-
"""
Created on Fri May 20 10:56:46 2022

@author: fs.egb
"""



import sys

from pathlib import Path
import secondary_firm_data


#HERE = Path(__file__).parent.parent.parent.absolute()

# # adding Folder_2 to the system path
#sys.path.insert(0, str(HERE/Path("features")))


import firm_register




def entity_mappings(df, fdi_markets, keywrds , flexi):
    entity_mapper = {}
    df, entity_mapper['bulletin_entities'] = firm_register.define_entities(df)
    df, entity_mapper  = firm_register.process_institution_entities(df, entity_mapper)

    # entity_mapper = firm_register.map_top40_fdi(df, fdi_markets, entity_mapper, keywrds, flexi)


    # df['firm_id'] = df['Companyname'].map(entity_mapper['bulletin_entities'])



    return df, entity_mapper