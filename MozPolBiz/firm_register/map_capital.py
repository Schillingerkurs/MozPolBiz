# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 16:31:34 2022

@author: fs.egb

currency mapper

Die Macht am Block. Ein neuer Mapper!
"""

import numpy as np
from text_to_num import alpha2digit


def find_numeric_word_tranlations(df):
    mpr = {}
    curncy_strings = []

    for r in  list(df['Capital']):
        if isinstance(r, str):
            temp = r.split('-')
            if len(temp) == 1:
                curncy_strings.append(temp)
            if len(temp)>= 2:
                mpr[temp[1].strip()] = temp[0].strip()
            if len(temp)> 2:
                print(f" strange string in currency mapper:\n {temp}")
            
    curncy_strings = [i for j in curncy_strings for i in j]
    curncy_strings = list(set(curncy_strings))  
    curncy_strings = [mpr[x] if x in list(mpr) else x for x in curncy_strings] 
    
    only_word = [x for x in curncy_strings if not any(map(str.isdigit, x)) ]
    
    swappie = {v:k for k,v in mpr.items() if  any(map(str.isdigit, k))}
    
    mpr_clean = {k:v for k,v in mpr.items() if  any(map(str.isdigit, v))}
    mpr_clean.update(swappie)
     
    return mpr_clean, only_word

def translate_string_words(only_word , mpr, df ):
    translation = {}
    for w in only_word:
        number = alpha2digit(w ,"pt")
        number = number.replace( "meticais", "MT")
        number = number.lstrip("(")
        number = number.rstrip(",")
        number = number.strip(".")
        number = number.replace( "de ", " ")
        translation[w]= number
    
    translation = {k:v for k,v in translation.items() if v !=''}
    gt = {k: v.replace( "MT","") for k,v in translation.items()}
    gt = {k: v.strip() for k,v in gt.items()}
    gt = {k: v for k,v in gt.items() if v.isdecimal()}
    
    finished_translation = {k: v for k,v in translation.items() if k in list(gt)}
    not_done_yet = {k: v for k,v in translation.items() if k not in list(gt)}
    
    mpr.update(finished_translation)
    
    mapper = {x: x for x in list(df['Capital'])}
    mapper =  {k: v for k, v in mapper.items() if isinstance(v,str)}
    mapper = {k: (v.split('-')[1] if "-" in v else v) for k,v in mapper.items()}
    mapper =  {k: v.strip() for k, v in mapper.items()}
    mapper =  {k: (mpr[v] if v in list(mpr) else v )for k, v in mapper.items()}

    return mapper, not_done_yet
    

def translate_capital(df):
    missing_captial = round(len(df[df['Capital'].isna()])/ len(df), 4)
    print(f'{missing_captial*100} % of the rows report no Capital')
      
    # basic currency  map 
    df['Capital'] = df['Capital'].str.replace('norte-americanos', 'norte americanos')
    df['Capital'] = df['Capital'].str.replace(' MZN', ' MT')
    df['Capital'] = df['Capital'].str.replace('  meticais', ' MT')    
    df['Capital'] = df['Capital'].fillna('')
    df.loc[df['Capital'].str.contains("da nova família"),'Capital_details'] = "da nova família"
    df['Capital'] = df['Capital'].str.replace("da nova família", "")
    df['Capital'] = df['Capital'].replace('', np.nan)    
    
    mpr, only_word = find_numeric_word_tranlations(df)
       
    mapper, not_done_yet= translate_string_words(only_word, mpr, df)
    
    print(f'{len(not_done_yet)} number strings require addtional cleaning \n')
    
    df['Capital'] = df['Capital'].map(mapper)
    
    
    return df


