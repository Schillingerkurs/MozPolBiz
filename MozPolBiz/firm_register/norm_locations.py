# -*- coding: utf-8 -*-
"""
Created on Tue May 17 13:05:03 2022

@author: fs.egb
"""


from unidecode import unidecode

def norm_locations(municipal_name):
    """ remove characters from adm3  strings that prevent geocoding"""
    
    municipal_name = unidecode(str(municipal_name).lower())
    municipal_name = municipal_name.replace("/"," ")
    municipal_name = municipal_name.replace("-"," ")
    municipal_name = municipal_name.replace("  "," ")
    municipal_name= municipal_name.split(" ") 
    stp_wrds = ["cidade","da", "de", "provincia", "porto", "bau"]
    municipal_name = [x.strip() for x in municipal_name if x not in stp_wrds]
    municipal_name = " ".join(municipal_name) 
    municipal_name = municipal_name.strip()
    
    return  municipal_name

