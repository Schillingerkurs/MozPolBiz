# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 08:53:33 2022

@author: fs.egb
"""
import re
import pickle
from tqdm import tqdm
from pathlib import Path
import pandas as pd
from unidecode import unidecode



def set_column_names(df):
    col_strings = dict(zip(df['native'], df['translation']))
    col_strings = {k: str(v).strip() for k, v in col_strings.items()}
    
    return col_strings



  
def rename_cols(df, keywrds): 
    col_strings = set_column_names(keywrds.parse('col_names')) 
    df = df.rename(columns = col_strings)
    return df
 


def define_annoucment(df, keywrds):
    """
    Define core annoucments ( registraion,anoucement, closure)
    and annoucment details (type of organization)
    ----------
    df : pd.DataFrame
        bulletin raw entries
    keywrds : ExcelSheet
        Keyword mapper to translate annoucments
    Returns
    -------
    df : pd.DatFrame
        bulletin with defined annoucment details.

    """
    
    df = rename_cols(df, keywrds)
    
    anouc_mapper = set_column_names(keywrds.parse('announcement'))
    anouc_mapper = {k: v.strip() for k,v in anouc_mapper.items()}
    # orga_dict = set_column_names(keywrds.parse('organization_type'))
    
                           
    df['Announcement of'] = df['Announcement of'].astype(str)
    df['Announcement of'] = df['Announcement of'].apply(lambda x: unidecode(str(x).lower()))
    
    annoucment_dict = dict(zip(df.index, df['Announcement of']))
    annoucment_dict = {k: unidecode(str(v).lower()) for k,v in annoucment_dict.items()}


    
    ann_prim = {k: v.split(" de ")[0] for k, v in annoucment_dict.items()}
    ann_prim = {k: v.replace("de","").strip() for k, v in ann_prim.items()}    
    ann_prim = {k: anouc_mapper[v] for k,v in ann_prim.items() if v in list(anouc_mapper)}


   
    
    organizations = ['partido politico','sociedade individual',
                    'sociedade por quotas','sociedade anonima', 
                    'sociedade cooperativa','associacao', 'fundacao',
                    'representacao comercial','contrato de consorcio']
    

    orga_type = {}
    for a in list(annoucment_dict):
        orga_type[a] = []
        for o in organizations:
              if o in annoucment_dict[a]:
                  orga_type[a].append(o)
      
    orga_type = {k: ", ".join(v) for k, v in orga_type.items()}
    
    
    df['annoucment'] = df.index.map(ann_prim)
    df['orga_type'] = df.index.map(orga_type)
    
    return df    











        