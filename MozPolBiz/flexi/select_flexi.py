# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 08:23:52 2022

@author: fs.egb
"""



from pathlib import Path
import pandas as pd
from unidecode import unidecode
from string_grouper  import group_similar_strings


# local modules

import flexi
# import  flexi







def merge_national_statistics(HERE, cntry_lower_2: str) -> None:
    """
    Map flexi, parties and commodity of a single country on
    featureId.
    Plot venn diagramm of id overlap

    :param country: country code
    :type country: str
    """
    sql_path = HERE/Path("data","external","flexicadastre","datastore_oct_2022",
                         "datastore.sqlite3")

    flexi_ = flexi.load_flexi(sql_path, cntry_lower_2)
    print(flexi_['Type'].value_counts(dropna = False))
    # flexi_ = flexi_[['Type','CalculatedAreaValue', 'Region', 'OBJECTID',
    #                'Concession', 'Con_Type',
    #                'FeatureId','Grant_Date', 'DteExpires', 'Location']]
    parties = flexi.get_party_names(sql_path, cntry_lower_2)
    parties = pd.DataFrame.from_dict(parties)

    commodities = flexi.get_commodities_per_feature(sql_path, cntry_lower_2)

    parties['entity'] = parties['Parties'].fillna(parties['Company'])



    df = (pd.DataFrame(parties['entity'])
        .assign(commodities = lambda x: x.index.map(commodities))
        .merge(flexi_, left_index = True, right_on = 'FeatureId' )
        )

    return df




def select_flexi(HERE):



    flexi_full = merge_national_statistics(HERE, cntry_lower_2 = 'mz')




    names = set([unidecode(x) for x in flexi_full['entity'] if isinstance(x, str)])



    flexi_name_mapper = (pd.DataFrame(names, columns = ['parties'])
             .assign(deduplicated = lambda x : group_similar_strings(x['parties'],
                                                                    # ignore_index = True
                                                                     ))
             )

    return flexi_name_mapper, flexi_full





