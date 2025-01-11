# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 11:21:21 2022

@author: fs.egb
"""


def map_initials(base):
    
    inditials = [x.split(" ") for x in base['raw'] ]
    inditials = [" ".join(x) for x in inditials if len(x[0]) <2]
    fam = dict(zip(base['raw'],base['family']))
    mapper = {}
    for i in inditials:
        pool = base[base['family'] == fam[i]]
        pool['initials'] = [x.split(" ") for x in pool['raw'] ]
        pool['initials'] = pool['initials'].apply(lambda y: [x for x in y if x!= ""])
        pool['initials'] = pool['initials'].apply(lambda y: [x[0] for x in y ])
        pool['initials'] = pool['initials'].apply(lambda y:" ".join(y))
        inl = pool[pool['raw'] == i]['initials']
        plausible = pool[pool['initials'].isin(inl)]
        
    
        mapper[i] = max(list(plausible['beta_clean']), key=len)

    base['gamma_clean'] = base['raw'].map(mapper)
    base['gamma_clean'] = base['gamma_clean'].fillna(base['beta_clean'])
    
    return base