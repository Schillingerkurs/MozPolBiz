# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 19:35:02 2022

@author: fs.egb
"""

def clean_cip3(dict_):
    df = dict_['CIP3']
    df = df.fillna('')
    df['name'] = df['Given_Name'] +' '+ df['Additonal_Name'] +' '+ df['Family Name']
    dct = dict(zip(df.index, df['name']))
    dct = {k: v.split(" ") for k,v in dct.items()}
    dct = {k:  " ".join([x.strip() for x in v if x != '']) for k,v in dct.items()}
    df['name'] = df.index.map(dct)
    
    dict_.pop('CIP3')
    dict_.update({'CIP3':df})
    return  dict_