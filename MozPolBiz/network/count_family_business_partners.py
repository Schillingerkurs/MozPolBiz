# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:20:29 2022

@author: fs.egb
"""

import networkx as nx



def count_family_business_partners(graphs,HERE,panel,entity_mapper):
    fam = dict(zip(entity_mapper['individual_mappings']['id'],
                   entity_mapper['individual_mappings']['family']))
    
    family_partner = {}
    for year in  graphs.keys():
        G = graphs[year]
        nx.set_node_attributes(G, fam, "family")
        for dude in G.nodes():
           family = G.nodes[dude]['family']
           counter = 0
           for neighbor in G.neighbors(dude):
               if G.nodes[neighbor]['family'] == family:
                   counter +=1
               else:
                   continue
           family_partner[(dude, year)] = counter
           
    return family_partner
   
   
           
           
