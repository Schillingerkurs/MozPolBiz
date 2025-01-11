# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 13:14:03 2022

@author: fs.egb
"""






import networkx as nx
import pandas as pd
from  tqdm import tqdm

def godfathter(G):
    out = {}
    for x in tqdm(G.nodes()):
    
#  get all business partners
        first = list(set(G.neighbors(x)))
    #    consider a subgraph of only bussiness partners   
        H = G.subgraph(first)
        new_contacts = 0
        for y in first:    
    #        get the contacts a node already has
                temp = list(H.neighbors(y))
                temp = len (temp)
    #            subtrac the contact a node already and herself
                new_contacts = new_contacts + len(first) - temp - 1
    #  of a person’s friends who are not friends with each other.  
        new_contacts = new_contacts /2 
        out[x]= new_contacts
        
    return out

def set_up_decay(G):
#    TOD: alternative approach:
#    consider only neighoring nodes
#    review if they 
    out = {}
    for x in tqdm(G.nodes()):  
        
        first =  set(G.neighbors(x))
        second = set()
        eins = len(first)
        for y in first:
            temp = G.neighbors(y)
            second.update(temp)
            second = set(second) - set(first) 
            second.discard(x)

        zwei = len(second)
        third = set()
        for z in second:
            temp2 = G.neighbors(z)
            third.update(temp2)
            third = set(third) - set(second) - set(first)
            third.discard(x)
        
        drei = len(third)
                                  
        # (f**3)*  = len(third)
            
        f = 0.5
        dc = (f**1)*eins + (f**2) * zwei + (f**3)*drei 
        
        out[x] = [eins, zwei, drei , dc ]
        
    return out
        


def collect_centralities(G):
    d1 = nx.degree_centrality(G)
    print('degree done')
    d5 = godfathter(G)
    print('godfather done')
    d6 = set_up_decay(G)
    print ("decay done")
    ds = [d1, d5,d6]
    d = {}
    for k in d5:
        d[k] = tuple(d[k] for d in ds)
    centralities = pd.DataFrame.from_dict(d, orient='index')
    centralities.columns = ['c_degree','c_gf',"c_decay"]
    
    centralities[['prtnr1', 'prtnr2','prtnr3','decay']] = pd.DataFrame(centralities.c_decay.values.tolist(), index= centralities.index)
    centralities = centralities.drop(columns=['c_decay'])

    return centralities