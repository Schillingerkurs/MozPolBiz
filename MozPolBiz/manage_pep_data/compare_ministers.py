# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 12:24:56 2022

@author: fs.egb

"""

import owner

def compare_ministers(pep_mandates):
    """ 
    compares our handcoded minister mandates with the Who Gov database
    1.) fuzzy match on all mininster names. ( 65 % ), all matches plausible
    2.) grouphy famil name. If First and last year in business are similar 
    -> same person
    
    """
    
    
    who_gov_mnstr = pep_mandates['Who_Gov']
    who_gov_mnstr = who_gov_mnstr[who_gov_mnstr['minister'] ==1]
    hand_mnstr =  pep_mandates['executive_mandates']
    hand_mnstr = hand_mnstr[hand_mnstr['position'] =="Minister"]
    
    all_names = set(hand_mnstr['name'])
    all_names.update(set(who_gov_mnstr['name']))
    all_names = set( x for x in all_names if isinstance(x,str))
    
    mapper, matches =  owner.map_name_list(all_names, 0.65)
    base = owner.map_family_subsets(all_names, 0.65) 
    ids = owner.set_id(base[ 'beta_clean'], "mnstr")
    base['id'] = base['beta_clean'].map(ids) 
    base = base.set_index('raw')
      
    return base['id']
