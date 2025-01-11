# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 12:26:21 2022

@author: fs.egb
"""

import owner
import operator
from itertools import combinations
from collections import Counter

def get_surnames(all_names):
    """ 
    returns last name from each string in a list of strings
    
    cleans each name strings
    
    excludes junior
    """

    surname_dict = owner.clean_name_strings(all_names) 
    surname_dict = {k: v.split(" ")[-2] if "junior" in v else v for k, v in surname_dict.items() }
    surname_dict = {k: v.split(" ")[-2] if "(quarentinha)" in v else v for k, v in surname_dict.items()}
    surname_dict = {k: v.split(" ")[-2] if "(senior)" in v else v for k, v in surname_dict.items()} 
    surname_dict = {k: v.split(" ")[-1] for k, v in surname_dict.items()}
    
    counter = Counter(surname_dict.values())
    l = max(counter.items(), key=operator.itemgetter(1))[0]
    
    print(f"{l}: {counter[l]} times")

    return surname_dict

