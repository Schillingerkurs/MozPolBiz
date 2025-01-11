# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 11:56:13 2022

@author: fs.egb
"""

def identify_FDI_affiliations(df,entity_mapper):
    
    fdi_mapper = entity_mapper['fdi_projects']
    

    
    # drop flexicadastre affiliations
    fdi_mapper = {k: v for k,v in fdi_mapper.items() if isinstance(v,list)}
    
    fdi_mapper =  {k: [str(x) for x in v] for k,v in fdi_mapper.items()}
    
    
    affiliations = [x for s in fdi_mapper.values() for x in s]
    
    temp = {}
    for a in affiliations:
        temp[a] = [k for k,v in fdi_mapper.items() if a in v]


    # inst_fdi = {k: v for k,v in temp.items() if "inst_" in k}
    direct_fdi = {k: v for k,v in temp.items() if k.isdecimal()}
                  
    direct_fdi = {int(k): ", ".join(v) for k,v in direct_fdi.items()}

    df['fdi_firm'] = df['firm_id'].map(direct_fdi)
    
    all_ins = dict(zip(df.index, df['inst_owner_norm']))
    all_ins = {k:v.split(", ") for k,v in all_ins.items() if isinstance(v, str)}
    fdi_ins =  {k: [x for x in v if x in list(temp)] for k,v in all_ins.items()}
    fdi_ins = {k: v for k,v in fdi_ins.items() if v!=[]}
    fdi_ins = {k: 1 for k,v in fdi_ins.items()}
    df['fdi_shareholder'] = df.index.map(fdi_ins)
    
    return df

