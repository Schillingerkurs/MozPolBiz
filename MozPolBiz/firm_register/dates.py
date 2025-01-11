# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 15:46:26 2022

@author: fs.egb

Identify dates

"""



import handle_html 



def get_backup_date(missing_date):
    missing_date = missing_date.set_index('ID do Registo')
    temp = missing_date.rename(columns ={'Published in':'Publicado em'})
    date = handle_html.define_publication_file(temp)  
    backup = dict(zip(date.index, date['publication_date']))
    backup = {k: str(v)[:10] for k,v in backup.items()}  
    
    backup = {k: v.replace("-","/") for k,v in backup.items()}  
    return backup




def replace_date(df):

    no_date = len(df[df['Date of writing'].isna()])
    print(f" \n{no_date} entries report no date of 'Date of writing' ")
    
    
    date_backup = dict(zip(df.index, df['Place and date of signature']))
    
    
    date_backup = {k: v.split(",")[1] for k,v in date_backup.items() if isinstance(v,str)}
    
    date_backup = {k: v.strip() for k,v in date_backup.items()}
    
    df = df.reset_index()
    
    df['Date of writing'] = df['Date of writing'].fillna(df['ID do Registo'].map(date_backup))
    

    
    no_date = len(df[df['Date of writing'].isna()])
    print(f" \n Now, {no_date} entries report no date of 'Date of writing' \n")
    print( "Publication in date")
    
    missing_date = df[df['Date of writing'].isna()]
    backup = get_backup_date(missing_date)
    df['Date of writing'] = df['Date of writing'].fillna(df['ID do Registo'].map(backup))
    
    no_date = len(df[df['Date of writing'].isna()])
    print(f" \n After Publication in fillna  {no_date} entries have no row \n")    
    
    
    df = df.set_index('ID do Registo')
    

    return df




