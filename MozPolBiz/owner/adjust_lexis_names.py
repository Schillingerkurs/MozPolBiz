# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 19:48:12 2022

@author: fs.egb
"""


def adjust_lexis_names(pep_mandates):
    lexis = pep_mandates['lexis']
    lexis = lexis.drop(columns=['name'])
    lexis['name'] = lexis['firstname']+ " " + lexis['lastname']
    pep_mandates['lexis'] = lexis
    return pep_mandates