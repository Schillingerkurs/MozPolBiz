# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 14:29:46 2022

@author: fs.egb
"""

import accounting_matrix

def get_both(HERE):
    
    sam = {}
    sam['12'] = accounting_matrix.get_matrix_12(HERE)
    sam['15'] = accounting_matrix.get_matrix_15(HERE)
    
    return sam 