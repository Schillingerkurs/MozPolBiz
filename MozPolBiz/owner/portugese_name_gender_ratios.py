# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 12:33:07 2022

@author: fs.egb
"""

from pathlib import Path
import random
import pandas as pd
import json
pd.options.mode.chained_assignment = None  # default='warn'
import pickle
import math
from PyPDF2 import PdfFileReader



# HERE = Path(__file__).parent.parent.parent.absolute()


def load_portugese_names(HERE):
    d = HERE/Path("data", "external","name_characteristics")
    pdf_path = d/Path("national_gender_portugal.pdf")
    pdfFileObject = open(pdf_path, 'rb')
    pdfReader = PdfFileReader(pdfFileObject,strict=False)
    
    return pdfReader

def formate_portugese_list(t):
    text=''
  
    for i in range(0,t.numPages):
        # creating a page object
        pageObj = t.getPage(i)
        # extracting text from page
        text = text+pageObj.extractText()
      
    for s in ['GÉNERO','NOME', ""]:
        text = text.replace(s, "")
    
    binary_map = {"Femininos ":"1", "Masculinos ":"0"}
    for b in binary_map.keys():
        text = text.replace(b, binary_map[b])
        

    names = [x for x in text.split()  ]
    names = [x for x in names   if "/" not in x ] 
    mapper = {k[1:]: float(k[0]) for k in names}
    print(f"number of porstugese names : {len(mapper)}")
    
    return mapper


def load_brazilian_names(HERE):
    d = HERE/Path("data","external",\
        "name_characteristics","brazilNamesGenderRatio.csv")

    brazil = pd.read_csv(d, on_bad_lines='skip',
                      low_memory = False, encoding = "iso-8859-1")  
    # d = HERE/Path("data","pep_data")

    return brazil
    


def portugese_name_gender_ratios(HERE):
    t = load_portugese_names(HERE)
    
    brazil = load_brazilian_names(HERE)
    brazil = dict(zip(brazil["firstName"],brazil['prFemale']))
    
    brazil = {k:v for k,v in  brazil.items() if not math.isnan(v)}
    
    portugal = formate_portugese_list(t)
    
    portugal.update(brazil)
    
    
    return portugal


