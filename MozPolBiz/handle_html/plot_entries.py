# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 14:11:12 2022

@author: fs.egb
"""
import numpy as np

import plotly.express as px
import missingno as msno
from datetime import datetime
from pathlib import Path



import handle_html

def plot_annually_registered(raw, y_i, HERE):
       
    first_y = datetime(year= min(y_i), month = 1 , day = 1)
    
    publ_dates = handle_html.define_publication_file(raw)
    
    x =  len(publ_dates)
    df = publ_dates.loc[~publ_dates['publication_date'].isna()]
    y = len(df)
    diff = x - y
    share = 100 - round(y/x *100, 3) 
    print (f"{diff}({share} %) of the publication dates are not readable")
    p_d = sorted(list(df['publication_date'].unique()))
    difs = []
    for n, p in enumerate(p_d):
        if (n > 0 ) & (n < len(p_d)-1 ):
            delta = p_d[n] - p_d[n-1]  
            difs.append(int(delta/np.timedelta64(1, 'D')))
     
    difs.sort()
    print("Shortes period between publications:", difs[0], "days")
    print("Longest period between publications:", difs[-1], "days")
    print("2nd Longest period between publications:", difs[-2], "days")
    
    entries_per_date = publ_dates['publication_date'].value_counts().reset_index()
    entries_per_date = entries_per_date.sort_values( by = ['index'])
    entries_per_date = entries_per_date[entries_per_date['index'] > first_y]
    
    

    
    fig = px.line(entries_per_date, x = 'index', y = 'publication_date')
    fig.update_yaxes(title_text="Date")
    fig.update_xaxes(title_text="Entries per day")
    plot_path= HERE/Path("reports","figures","bulletin_parser")
    
    fig.write_image(str(plot_path/Path("entries_per_day.png")))

    print("plot per day done")



def plot_missing_entities(df,HERE):
    fig = msno.matrix(df)
    fig_copy = fig.get_figure()
    plot_path = HERE/Path("reports","figures", "bulletin_parser", 'nan_values.png')
    fig_copy.savefig(plot_path, bbox_inches = 'tight')