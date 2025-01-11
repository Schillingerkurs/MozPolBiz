# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 11:01:33 2022

@author: fs.egb
"""

from pathlib import Path
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import pickle

from string_grouper import group_similar_strings, match_strings
import sys

HERE = Path(__file__).parent.parent.parent.parent.absolute()




sys.path.insert(0, str(HERE/Path("src", "features")))

# own modules
import owner
# import test_name_mapper
import firm_register
import secondary_firm_data
import manage_entities
import adm0_stuff



def load_nat_peps(HERE):
    # load all files in pep_directory
    d = HERE/Path("data","external","pep_data")
    pep_mandates = {}
    pep_mandates['CIP3']  = pd.ExcelFile(d/Path("CIP_Borges",
                            "cip3.xlsm")).parse("Sheet1")
    temp = pd.ExcelFile(d/Path("hand_coded_mandates","PEP_database.xlsx"))
    for i in temp.sheet_names:
        pep_mandates[i] = temp.parse(i)

    pep_mandates["lexis"] = pd.read_stata(d/Path("LexisNexis_World_Compliance",\
                                             "mozambique_pep_list.dta"))

    return pep_mandates


def add_international_pep_names(HERE, iso3_cntry):
    """
    select national PEPS from itern databases
    """
    d = HERE/Path("data","external","pep_data")

    national_pep = {}

    national_pep["Who_Gov"] = (
                    pd.read_csv(d/Path("WhoGov","WhoGov_within_V2.0.csv"), \
                                  on_bad_lines='skip' , index_col = 0,
                                 low_memory = False, encoding = "iso-8859-1")
                    .query('country_isocode in @ iso3_cntry')
                    )

    national_pep["offshore_acounts"] = \
    adm0_stuff.select_national_offshore_accounts(HERE, iso3_cntry)

    return national_pep




def load_hand_duplicates(HERE):
    d = HERE/Path("data","external","pep_data","hand_coded_mandates")
    with open(d/Path("duplicates.txt"), 'r') as f2:
        duplicates = f2.read()
    return duplicates




def select_dbr_experts(HERE):
    dbr = (pd.read_parquet(HERE/Path("data",
                                     "interim", 'dbr_experts_moz.parquet.gzip'))
           .assign(fullName = lambda x : x['firstName']+" " +x['lastName'] )
           )

    return dbr['fullName']


def other_name_characteristics(HERE):

    other = {}
    # gender = owner.portugese_name_gender_ratios(HERE)
    # gender = {k.strip(): v for k,v in gender.items()}
    # mpr = owner.clean_name_strings(gender.keys())

    # other['gender'] = {mpr[k]: v for k,v in gender.items() }

    d = HERE/Path("data","external","pep_data")
    other['lawyer'] = pd.read_csv(d/Path("lawyer_parser_raw.csv"), on_bad_lines='skip' ,
                     low_memory = False, encoding = "iso-8859-1", sep = ";")


    other['dbr_experts'] = select_dbr_experts(HERE)
    return other






def map_individual_characteristics(HERE):

    bulletin = pd.read_pickle(HERE/Path("data","interim","firmregister_full.pkl"))
    pep_mandates = load_nat_peps(HERE)
    pep_mandates  =  owner.clean_cip3(pep_mandates)
    pep_mandates = owner.adjust_lexis_names(pep_mandates)

    international_peps = add_international_pep_names(HERE, "MOZ")


    pep_mandates.update(international_peps)


    other =  other_name_characteristics(HERE)



    # TODO: allow for indvidual duplicates
    duplicates = load_hand_duplicates(HERE)

    entry_names = owner.add_blltn_owner(bulletin)



    all_names =  owner.get_all_names(pep_mandates, entry_names, other)

    base = owner.get_name_base(all_names, other)

    base = owner.get_og_network(bulletin, base)


    return base