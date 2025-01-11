# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 19:03:20 2022

@author: fs.egb
"""




def get_executive_tenure(y_i):
    """ 
    Define start and end of  ruling periods
    mandates: < 1986 end with the death of Machel
    19896-1995 end with the first election.
    >1995 determined by new election.
    
    """
    exe_tenure = {}
    
    for x in list(range(1970,1987,1)):
        exe_tenure[x] = list(range(x,1987,1))
    
    for x in list(range(1987,1995,1)):
        exe_tenure[x] = list(range(x,1995,1))
    i = 0
    for x in range(1995,max(y_i),1):
        i = 0 if i == 5 else i
        end_y = list((range(1,6,1)))
        end_y.sort(reverse = True)
        stop_year = x + end_y[i]
        i += 1
        exe_tenure[x] = list(range(x,stop_year ,1))
        
    return exe_tenure


def executive_dummies(panel,pep_mandates, y_i, name_mapper):
    
    exe = pep_mandates['executive_mandates'][['Year_position','name', 'position']]
    exe['id'] = exe['name'].map(name_mapper)
    
    tenure = get_executive_tenure(y_i)

    for ex in exe['position'].unique():
        temp = exe[exe['position']== ex]
        f_t = dict(temp.groupby('id')['Year_position'].unique())
        f_t = {k: v.tolist() for k,v in f_t.items()}
        f_t = {k: [tenure[x] for x in v] for k,v in f_t.items()}
        f_t = {k: list(set([f for s in v for f in s])) for k,v in f_t.items()}
        unique_combos = {}
        for p in f_t:
            for y in f_t[p]:
                unique_combos[(p,y)] = 1
        panel[f"{ex}"] = panel["m"].map(unique_combos)
        
    return panel
                
                