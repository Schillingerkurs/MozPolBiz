# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:28:32 2022

@author: fs.egb
"""

import pickle


def store_pickle(output, lp):
    with  open(lp,'wb') as f:
        pickle.dump(output,f)
    print(f"saved in {lp}")  
