# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:53:51 2022

@author: fs.egb

firm performance

map assets/contracts/licenses/projects to firms in the bulletin
"""




import pandas as pd

from string_grouper import match_strings
#  own modules

import  firm_register
import manage_entities


# HERE = Path(__file__).parent.parent.parent.absolute()


def classify_mining_entity_type(m_l, name_col):
    """ clean strings and map firm keywords"""
    
    m_l['parties_clean'] = m_l[name_col].apply \
                    (lambda x: firm_register.norm_firm_names(x))
                    
    uniuqe_entities = list(m_l['parties_clean'].unique())
    firm_mapper = firm_register.identify_firm_entities(uniuqe_entities)
    m_l['firm'] = m_l['parties_clean'].map(firm_mapper)
    
    m_l['parties_clean'] =  m_l['parties_clean'].apply(lambda x: str(x))
    
    
    mapper = firm_register.fuzzy_entity_norm(m_l['parties_clean'])

    m_l['entity_fuzz'] =  m_l['parties_clean'].map(mapper)
    
                           
    return m_l
    

def link_on_bltn_id(entity_ids, m_l):
    """ 
    normalizes both bulletin and flexi mining entities 
    
    fuzzy match between another
    
    map bulletin entitiy ID on flexi mining licenses
    
    """
    
    bltn_mapper = pd.DataFrame.from_dict(entity_ids, orient= 'index').reset_index()
    bltn_mapper.columns = ["raw","id"]
    
    bltn_mapper['enitiy_clean'] = bltn_mapper.raw.apply(lambda x: firm_register.norm_firm_names(x))
    
    
           
    matches = match_strings(bltn_mapper['enitiy_clean'], m_l['entity_fuzz'], min_similarity = 0.85)
    mapper_match = dict(zip(matches['right_entity_fuzz'], matches['left_enitiy_clean']))
    mapper_bltn = dict(zip(bltn_mapper['enitiy_clean'], bltn_mapper['id']))
    mapper_match = { k : mapper_bltn[v] for k, v in mapper_match.items()}
    
    
    m_l['bltn_id'] = m_l['entity_fuzz'].map(mapper_match)
    
    return m_l


def map_flexi_on_bulletin(entity_ids,m_l):
    
    m_l = m_l[m_l['parties'].apply( lambda x : isinstance(x,str))]

    m_l = classify_mining_entity_type(m_l, 'parties')
    m_l = link_on_bltn_id(entity_ids, m_l)
    m_l.loc[m_l['entity_fuzz'].str.contains('nacional de'),'bltn_id'] = "public_entity"
    m_l.loc[m_l['entity_fuzz'].str.contains('mireme'),'bltn_id'] = 'public_entity'
    # t = m_l[m_l['entity_fuzz'].str.contains()]
   
    potential_persons = m_l[m_l['bltn_id'].isna()]  
    # unique_p =  set(potential_persons['entity_fuzz'])
       
    return m_l


def fuzzy_match_on_corpus(entity_mapper,flexi):
    
    fehlt = pd.Series(
            flexi[flexi['bltn_id'].isna()]
            .assign(entitiy_count = lambda x: x['parties'].map(x['parties'].value_counts()))
            .set_index('parties')        
            .drop_duplicates(subset =['parties_clean' ])
            ['parties_clean' ]
            )
                
    corpi = pd.Series(entity_mapper['corpus'])  
    
    corpi_dict = {v: k for k, v in corpi.to_dict().items()}
    
      
    fuzzy_mapper = (match_strings(fehlt, corpi, min_similarity = 0.8009) 
               .groupby("left_parties_clean")['right_side'].unique()
               .to_dict()
               )
    
    fuzzy_mapper = {k:v.tolist() for k,v in fuzzy_mapper.items()}
      
    
    fuzzy_mapper = {k: [corpi_dict[x] for x in v] for k,v in fuzzy_mapper.items()}         
    fuzzy_mapper = {k: [entity_mapper['all_entity_mapper'][x] for x in v] for k,v in fuzzy_mapper.items()}
    
    
    gefunden = flexi.dropna( subset =['bltn_id'])
    flexi_mapper = dict(zip(gefunden['parties'], gefunden['bltn_id']))
    flexi_mapper = {k: str(v).replace(".0", "").split(",") for k, v in flexi_mapper.items()}
    flexi_mapper.update(fuzzy_mapper)
    
    return flexi_mapper 
  
def map_on_individuals_on_flex(flexi,entity_mapper):
    
    fehlt = (flexi
             .query("all_ids != all_ids")
             .set_index('parties')
             .drop_duplicates(subset =['parties_clean'])
             ['parties_clean']
             # ['parties'].value_counts()
             )


    ppl = (
            entity_mapper['individual_mappings']
            .set_index('id')
            ['clean'])
    
    ppl = ppl[[isinstance(x, str) for x in ppl]]

    
    fuzzy_mapper = (match_strings(fehlt, ppl, min_similarity = 0.9) 
                    .groupby("left_parties")['right_id'].unique()
                    .to_dict()
                    )
    fuzzy_mapper = {k:v.tolist() for k,v in fuzzy_mapper.items()}
    
    return fuzzy_mapper
  

def include_famous_gas_fields(flexi_mapper, flexi, keywrds,entity_mapper): 
    
    flexi_mapper.update(
            keywrds.parse("fleix_to_inp")
            .set_index('felix_entity')
            .dropna(subset = ['inp_shareholder'])
            ['inp_shareholder'].to_dict()
            )
    
    flexi["all_ids"] = flexi['parties'].map(flexi_mapper)
    fehlt = (flexi
             .query("all_ids != all_ids")
             .assign(entity_counter = lambda x: x['parties_clean']
                             .map(x['parties_clean'].value_counts()))
             .set_index('parties')
             .drop_duplicates(subset =['parties_clean'])
              [['parties_clean']]
 #             ,'commodities'
             )

    flexi_mapper.update((
                        firm_register.map_inp(fehlt.index, keywrds, entity_mapper)
                        .dropna(subset = ['FDI_link'])
                        .set_index('FDI_link')
                        ['affi_gas_fields']
                        .to_dict()
                        ))

    
    
    return flexi_mapper                    

def manual_buleltin_matches(flexi_mapper, keywrds, entity_mapper):
    

    blthn_mapper = (
            keywrds.parse("fleix_to_inp")
            .set_index('felix_entity')
            .dropna(subset = [ 'bltn_firm ( with line seperator)'])
            ['bltn_firm ( with line seperator)'].to_dict()
            )
    blthn_mapper = {k: v.split("|") for k,v in blthn_mapper.items()}
    blthn_mapper = {k: [x.strip() for x in v if x != ""] for k,v in blthn_mapper.items()}
    flexi_mapper.update({k: [entity_mapper['all_entity_mapper'][x]
                             for x in v if x in entity_mapper['all_entity_mapper'].keys()] for k,v in blthn_mapper.items()}  ) 
    return flexi_mapper
    
    
    
     
    

# with open(HERE/Path("data","interim","all_entity_mappings.pkl") , 'rb') as f:
#     entity_mapper = pickle.load(f)


# keywrds = pd.ExcelFile(HERE/Path("data","raw","keywords",
#             "all_keywords_mapper.xlsx")) 



# felxi =  pd.read_pickle(HERE/Path("data","external","flexicadastre",
#                                 "national_flexi_full.pkl"))




def flexicadastre_mapping(keywrds, flexi, entity_mapper):
    
    entity_mapper['corpus'] = manage_entities.get_corpus_all_enties(entity_mapper)

    entity_mapper = manage_entities.get_all_entitiy_mapper(entity_mapper)




    flexi = map_flexi_on_bulletin(entity_ids = entity_mapper['bulletin_entities'], 
                                   m_l =  flexi)
    
    flexi_mapper = fuzzy_match_on_corpus(entity_mapper,flexi)
    
    flexi["all_ids"] = flexi['parties'].map(flexi_mapper)
    indiv_mapper = map_on_individuals_on_flex(flexi,entity_mapper)
    
    # TODO: add individual matcher to 
    
    flexi_mapper = manual_buleltin_matches(flexi_mapper, keywrds, entity_mapper)
    
    flexi_mapper.update(indiv_mapper)
    flexi["all_ids"] = flexi['parties'].map(flexi_mapper)
    
    
    flexi_mapper = include_famous_gas_fields(flexi_mapper, flexi, keywrds, entity_mapper)
    
    return flexi_mapper, indiv_mapper
             
    
    
    # fehlt = (flexi
    #          .query("all_ids != all_ids")
    #          .assign(entity_counter = lambda x: x['parties_clean']
    #                          .map(x['parties_clean'].value_counts()))
    #          # .set_index('parties')
    #          .drop_duplicates(subset =['parties_clean'])
    #          [['parties','entity_counter']]
    #          )


# # look up in FDI affilaitons, if Concession is listed as an FDI


# # fdi = {k:v for k,v in  entity_mapper['fdi_projects'].items()}

# # fdi = {k: [x for x in v if x  if "inst" not in x] for k,v in fdi.items() if v}


# gas = firm_register.map_inp(fehlt.index, keywrds, entity_mapper)


# uniuqe_missing = (group_similar_strings(fehlt, min_similarity=0.8)        
#         .assign(cluster_size = lambda x: x['group_rep_parties_clean'].map( x['group_rep_parties_clean'].value_counts()))
#         # ['group_rep_parties_clean']
#         # .to_dict()
#         )

# fdi = entity_mapper['fdi_projects']


# bltn = {k:v for k,v in entity_mapper['corpus'].items() if "focus mi".lower() in v}

# for k in bltn.keys():
#     print(k, end = "|")
    
    
