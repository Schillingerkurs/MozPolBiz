# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 09:21:37 2022

@author: fs.egb

Imputation organization type

"""
import numpy as np

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'



def count_shareholders(df):
    """
    count number of shareholders for each (former) shareholder column
    """
    cols = ['Beneficial owner','Institution owner',
            'Previous_partners','Previous members institutions']

    for c in cols:
        d = dict(zip(df.index, df[c]))
        d = {k:v.split(", ") for k,v in d.items() if isinstance(v, str)}
        d = {k: len(v) for k,v in d.items()}
        df[f'len_{c}'] = df.index.map(d)

    return df



def get_name_dict(df):
    name_dict = {}
    for c in df['orga_type'].unique():
        temp = df[df['orga_type'] == c]
        name_dict[c] = list(set(temp['norm_name']))
    return name_dict


def main(df, bayes_classifier):
    #  check if entries w/o orga type of a NUIT or NUEL.
    m_o = df[(df["orga_type"]=='') ]
    m_o["orga_type"] = m_o["orga_type"].replace('', np.nan)
    print(f'{len(m_o)} of {len(df)} row  report no orga type \n')

    # select rows with orga
    temp = df[(df['orga_type'] != '')]
    # temp = temp.sort_index()

    for col in ['NUEL_id','norm_name']:

        mapper_col = dict(zip(temp[col],temp["orga_type"]))

        m_o['orga_type'] = m_o['orga_type'].fillna(m_o[col].map(mapper_col))

        print(f"match on {col} lead to: \n",
            m_o['orga_type'].value_counts(dropna= False))

    orga_mapper = dict(zip(m_o.index, m_o['orga_type']))


    df["orga_type"] = df["orga_type"].replace('', np.nan)


    df['orga_type'] = df['orga_type'].fillna(orga_mapper)

    missing = round(len(df[df['orga_type'].isna()])/ len(df), 4)
    print(f"{missing} % of the sample have still no orga type")




    return df




