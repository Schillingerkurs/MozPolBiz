# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 13:39:07 2022

@author: fs.egb
"""
import re 
from collections import Counter

def define_year(df, y_i):
    """ 
    define publicaiton year of eeach entry based on
    
    1) Date of writing col
    - if missing : than
    2) Place and date of signature
    - if still missing: 
    3) Place and date of signature
    - if still missing:
     Most commen value of the +-5 nearby entry (Only in 2 cases).
     
    """
    
    first_y = min(y_i) -1
    last_y = max(y_i) + 1
    
 

    year_dict = dict(zip(df.index, df['Date of writing']))
    

    
    year_dict = {k:  re.findall(r"(?<!\d)\d{4}(?!\d)", v) for k,v in year_dict.items()  }     
    year_dict = {k:  ",".join(v) for k,v in year_dict.items()} 
    
    year_dict = {k:  int(v) for k,v in year_dict.items() if v.isdigit()}
    year_dict = {k:  int(v) for k,v in year_dict.items() if v > first_y}               
    year_dict = {k:  int(v) for k,v in year_dict.items() if v < last_y}    
  
    u  = [x for x in df.index if x not in year_dict]
    supl_y = dict(zip(df.index, df['Place and date of signature']))
    supl_y = {k: str(v) for k, v in supl_y.items() if k in u}
    supl_y = {k:  re.findall(r"(?<!\d)\d{4}(?!\d)", v) for k,v in supl_y.items()  }     
    supl_y = {k:  ",".join(v) for k,v in supl_y.items()} 
    
    supl_y = {k:  int(v) for k,v in supl_y.items() if v.isdigit()}
    supl_y = {k:  int(v) for k,v in supl_y.items() if v > first_y}               
    supl_y = {k:  int(v) for k,v in supl_y.items() if v < last_y}    
    
    year_dict.update(supl_y)
    u  = [x for x in df.index if x not in year_dict]
    supl_y = dict(zip(df.index, df['Published in']))
    supl_y = {k: str(v) for k, v in supl_y.items() if k in u}
    supl_y = {k:  re.findall(r"(?<!\d)\d{4}(?!\d)", v) for k,v in supl_y.items()  }     
    supl_y = {k:  v[0] for k,v in supl_y.items()}  
    
    supl_y = {k:  int(v) for k,v in supl_y.items() if int(v) < last_y} 

    year_dict.update(supl_y)    

    
    
    missing = [x for x in df.index if x not in year_dict]
    fill_mapper = {}
    for m in missing:
        around = range(m-5, m+5, 1)
        nearby_yars = {k: v  for k,v in year_dict.items() if k in around}
        value = Counter(nearby_yars.values()).most_common(1)[0][0]
        fill_mapper[m] = value
        
    year_dict.update(fill_mapper)     

    
    df['y'] = df.index.map(year_dict)    
    
    return df 
        
        
        