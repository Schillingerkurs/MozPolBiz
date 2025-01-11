# -*- coding: utf-8 -*-
"""
Created on Fri May 27 13:07:29 2022

@author: fs.egb
"""


import setup_panel
import manage_pep_data




def setup_pep_panel(y_i, all_owners, pep_mandates, name_mapper):
    """ 
    set executive_dummies, select who gov, mps, cc, pb 
    """
    panel = setup_panel.get_panel_identifier(y_i, all_owners)
    panel = manage_pep_data.executive_dummies(panel,pep_mandates, y_i, name_mapper)
    panel = manage_pep_data.select_who_gov(pep_mandates, name_mapper, panel)
    panel = manage_pep_data.map_mps(pep_mandates,name_mapper, panel)
    panel = manage_pep_data.map_cc(pep_mandates,name_mapper, panel, y_i)
    panel = manage_pep_data.map_pb(pep_mandates,name_mapper, panel, y_i)
    
    return panel
    




