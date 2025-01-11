# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 16:56:27 2022

@author: fs.egb
"""
import requests
import pandas as pd


from pathlib import Path
# import re
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
import pickle
# import itertools
import geopandas as gpd



HERE = Path(__file__).parent.parent.parent.absolute()





def get_coutnry_experts(cntry :str) -> "expert_list":
    url = f"https://wbgindicators.azure-api.net/DoingBusiness/api/GetLocalPartners/{cntry}?lang=en"

    headers = {'Ocp-Apim-Subscription-Key': '7c202aad75524b5a9c9f0a9fa42cbbbc'}

    r = requests.get(url,  headers = headers )

    check = r.json()
    content = (
            pd.DataFrame(r.json()) 
            .dropna(how='all')
            )

    return content



def try_geocdeing(df):
    return  (
        df
        .assign(geometry = lambda x: gpd.tools.geocode(x['streetAddress'])['geometry'])
             )



df = get_coutnry_experts(cntry= "moz")


df.to_parquet(HERE/Path("data","interim", 'dbr_experts_moz.parquet.gzip'),
              compression='gzip') 






