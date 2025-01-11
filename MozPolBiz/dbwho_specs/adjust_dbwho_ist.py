# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 14:07:12 2022

@author: fs.egb
"""

def adjust_dbwho_ist(bltn):
    

    
    bltn.loc[bltn['industry_primary']=='mining', 'industry_primary'] = 'Heavy industry & mining'
    bltn.loc[bltn['industry_primary']=='HeavyIndustry', 'industry_primary'] = 'Heavy industry & mining'
    
    # select the most important industries
    other_industries =['Tourism/Entertaiment/restaurants','Communications/Media',
              'Manufacturing','Agriculture','Real estate','water/recycling ',
              'Fisheries','partiees/unions']
    
    for c in other_industries:
        bltn.loc[bltn['industry_primary']== c, 'industry_primary'] = 'other'
        
    bltn['industry_primary'] = bltn['industry_primary'].fillna('unclassified')
    
    return bltn