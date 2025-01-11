# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 10:52:18 2022

@author: fs.egb
"""

from pathlib import Path
# import re
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
import pickle
# import itertools
import geopandas as gpd


# HERE = Path(__file__).parent.parent.parent.absolute()


# def load_data(HERE):    
     
  
#     with open(HERE/Path("data","external","flexicadastre",
#                         "national_flexi_full.pkl") , 'rb') as f:
#         felxi = pickle.load(f) 
    
#     flexi_selections = ['code','commodities', 'commoditiescd',
#            'start_date', 'expiry_date']
    
#     adm2 = gpd.read_file(HERE/Path("data","external","adm", 
#            "moz_admbnda_adm2_ine_20190607.json"))[['ADM2_PT','geometry']]


#     return adm2, felxi, flexi_selections
        
    


def map_mines_on_adm(gdf, felxi, flexi_selections):
    
    

    geographic_crs = str(gdf.crs)
    
    projected_crs = 3857
    
    flexi_selections.append("geometry")
    

    
    print(f"Includes the variables {flexi_selections} from flexi")
    
    mapi = (gpd.GeoDataFrame(
                felxi[flexi_selections],
                      geometry =  'geometry')
            .assign(geometry = lambda x: x['geometry'].centroid)
            .to_crs(geographic_crs))
    
    
    #.sjoin_nearest  helps to deal with islands (of teritory)
    mines_w_adm2 = (mapi.to_crs(projected_crs).sjoin_nearest(
        gdf.to_crs(projected_crs), distance_col="distances")
        .to_crs(geographic_crs)
        )

    return mines_w_adm2





