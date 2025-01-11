# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 09:14:53 2022

@author: fs.egb
"""

import pandas as pd

from nltk.stem import WordNetLemmatizer, SnowballStemmer
from unidecode import unidecode
from collections import Counter



def get_corpus(df):
    df['corpus'] = df['Companyname'] +" "  + df['Social object'].\
        apply(lambda x : unidecode(str(x).lower()))
    return df
  
def map_industry_keywords(bltn, keyword_dict ):
    bltn = get_corpus(bltn)
    industries = pd.read_excel(keyword_dict, sheet_name ='industries' ).set_index('category')
    industries = industries[~industries.index.isna()]
    
    out = {}
    for c in list(industries.index):
        r = industries[industries.index == c]
        r = r.dropna(axis='columns').T 
        r['group'] = c
        out.update(dict(zip(r[c],r['group'])))
              
    t = dict(zip(bltn.index , bltn['corpus']))  
    t = {k: v for k, v in t.items() if type(v) != float}
    t = {k: v.split(" ") for k, v in t.items()}
    
    
    findings =  {k: [out[x] for x in v if x in list(out)] for k,v in t.items()}
    
    print(100* round(len(findings) / len(bltn), 3),\
          "% of the entries map on at least one  industry")
    findings = {k:v for k,v in findings.items() if v != []}
    
    
    count = {k: {t: round(u/len(v), 2)  for t, u in dict(Counter(v)).items() }for k,v in findings.items()}
    
    primary_industry = {k: max(v, key = v.get) for k, v in count.items()}
    
    bltn['industry_primary'] = bltn.index.map(primary_industry)
    
    bltn['industry_primary'] = bltn['industry_primary'].fillna('unclassified')
    return bltn
