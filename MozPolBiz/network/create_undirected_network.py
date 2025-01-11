# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 17:20:34 2021

@author: fs.egb

owner_firm Graph
"""

# import pandas as pd
#import pickle

import networkx as nx
from itertools import permutations, chain
from tqdm import tqdm
# from nameparser import HumanName
 



def create_edges(firm_dict):
    print("create edges")
    edge_dict = {}
    for k, v in tqdm(firm_dict.items()):
        perms = list(permutations(v, 2))
        edges = []
        for x in perms:
            x_ = tuple(set(x))
            if x_ not in edges:
                edges.append(x_)
        edge_dict[k] = tuple(edges)
    edge_dict = {k:v for k, v in edge_dict.items() if len(v) > 1}
    
    edgelist=  list(edge_dict.values())
    edgelist = list(chain.from_iterable(edgelist))
    edgelist = [x for x in edgelist if len(x) in [2, 3]]
    
    return  edgelist



def create_undirected_network(all_entitiy_reg, firm_dict): 
    nodeslist =  list(all_entitiy_reg.keys())
     
    edgelist = create_edges(firm_dict)
    
    # temp = []
    # for e in edgelist:
    #     temp.append(e[0])
    #     temp.append(e[1])   
        
    # missing = set(temp) - set(nodeslist)
    
    G = nx.Graph()
    G.clear()     
    G.add_nodes_from(nodeslist)
    G.add_edges_from(edgelist)
    
    return G
