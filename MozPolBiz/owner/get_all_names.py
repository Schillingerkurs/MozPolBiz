# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:02:22 2022

@author: fs.egb
"""


def add_lawyers(other):
     lwy = other['lawyer']['full_name']
     lwy = [x.strip() for x in lwy if isinstance(x,str)]
     print( f"Lawyers: \n     {len(lwy)} names ")
     return lwy


def get_all_names(pep_mandates, entry_names, other):

    """ get  name strings from all sources"""

    local_file = dict(pep_mandates)
    all_names = []


    offshore_names =  set(local_file['offshore_acounts']['nodes-officers']['name'])
    offshore_names.update(set(local_file['offshore_acounts']['nodes-intermediaries']['name']))


    offshore_names.update(set(local_file['offshore_acounts']['nodes-intermediaries']['name']))


    local_file.pop('offshore_acounts')
    for c in local_file.keys():
        print(f"{c}: \n  {len(local_file[c]['name'].unique())} names")
        all_names.extend(local_file[c]["name"])


    all_names = [ x for x in  set(all_names) if isinstance(x,str)]

    blltn_owner = [f for s in entry_names.values() for f in s]
    blltn_owner = set(blltn_owner)
    all_names.extend(blltn_owner)
    all_names.extend(add_lawyers(other))

    print(f"DBR_experts: \n   {len(other['dbr_experts'])} names")
    all_names.extend(other['dbr_experts'])
    all_names = set(all_names)

    print(f"offshore accounts: \n   {len(offshore_names)} names")
    all_names.update(offshore_names)
    all_names = list(all_names)

    return all_names

