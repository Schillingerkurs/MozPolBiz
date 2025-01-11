# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 22:05:18 2022

@author: fs.egb

handle_html
"""



#%%
import re

from tqdm import tqdm
from pathlib import Path

import pandas as pd
from prettytable import PrettyTable
from datetime import datetime as dt
from bs4 import BeautifulSoup


#ERE = Path(__file__).parent.parent.parent.absolute()

#file_name = "id_44.html"
def load_data(file_name, HERE):

    d = Path(HERE/Path("data","raw","pandora_raw_html"))
    with open(d/Path(file_name), encoding='iso-8859-1') as f:
        soup = BeautifulSoup(f, "lxml")

    return soup


#soup = load_data(file_name, HERE)

#%%
def get_month_mapper():
    month_mapper = {}
    for num in range(1,13,1):
        num = str(num).zfill(2)
        month_mapper.update({f'de  MesExtenso("{num}")  de':f"{num}"})
    return month_mapper

def percent_in_fetch(percent, fetch):
    """
    rename column names with percentages, inlcuded them in fetch dict
    ----------
    percent : dict
        string columns with "%" in string
    fetch : dict
        all other columns.

    Returns
    -------
    fetch : fetch
        all columns in a single dict combined.
    """
    percent = {k: v for k,v in percent.items() if v}
    cols = []
    for e in percent:
        percent[e] = {k: v for k, v in percent[e].items() if v != []}
        cols.extend(list(percent[e]))


    percent = {k: v for k, v in percent.items() if v != {}}

    rename_cols = {'Sócios pessoas e quotas': 'person_shares',
                   'Sócios instituições e quotas':'institution_shares'}

    for nested_d in percent.values():
        for c in list(rename_cols):
            if c in list(nested_d):
                nested_d[rename_cols[c]] = nested_d.pop(c)

    relevent = set.intersection(set(list(fetch)), set(list(percent)))
    for e in relevent:
        fetch[e].update(percent[e])
    return fetch

def check_for_additional_tables(sample,HERE):
    fetch = {}
    month_mapper = get_month_mapper()
    percent = {}

    for id in tqdm(sample):
        try:
            percent[id] = {}
            soup = load_data(f"id_{id}.html",HERE)
            table = soup.find_all("table", {"width": "100%"})[1]
            out = {}
            for n, tr in enumerate(table.find_all('tr')):
                if n > 0:
                    cellLHS = tr.find('td', {"align" : "right"})
                    currentKey = cellLHS.get_text().replace(':', '').strip()
                    cellRHS = tr.find('td', {"align" : "left"})
                    currentValue = re.findall('(?<=\>)(.*?)(?=\<)',str(cellRHS))
                    currentValue = " ".join(currentValue)
                    if "%" in str(currentValue):
                            percent[id][currentKey] = re.findall('(?<=<\/script><\/b>)(.*?)(?=<br)',str(cellRHS))
                    if "Relaciona" in str(currentValue):
                        currentValue = re.findall('(?<="10")(.*?)(?="1FS2021")',str(cellRHS))
                        currentValue = "".join(currentValue)
                        currentValue = currentValue.split(",")
                        currentValue = list(set(currentValue))
                        currentValue = ", ".join(currentValue)
                        currentValue = currentValue.lstrip(",")
                        currentValue = currentValue.strip()
                        currentValue = currentValue.replace('"',"")
                    if "MesEx" in str(currentValue):
                         for m, v in month_mapper.items():
                            currentValue = currentValue.replace(m,v)
                         currentValue = currentValue.strip()
                         currentValue = currentValue.replace(" ","/")
                         currentValue = currentValue.replace(",/",", ")
                    if currentKey =='Sócios instituições e quotas':
                        currentValue = re.findall('(?<=,")(.*?)(?="\n)',str(cellRHS))
                        currentValue = ", ".join(list(set(currentValue)))
                    out[currentKey] = currentValue
            fetch[id] = out
        except IndexError:
            continue

    out = percent_in_fetch(percent, fetch)

    for k in list(out):
        newkey = f'999999{k}'
        out[newkey] = out.pop(k)

    return out


def get_columns(sample, HERE):
    fetch = {}
    month_mapper = get_month_mapper()
    percent = {}
    number_of_tables = {}

    for id in tqdm(sample):
        try:
            percent[id] = {}
            soup = load_data(f"id_{id}.html", HERE)
            table = soup.find_all("table", {"width": "100%"})[0]
            number_of_tables[id] = len(soup.find_all("table", {"width": "100%"}))
            out = {}
            for n, tr in enumerate(table.find_all('tr')):
                if n > 0:
                    cellLHS = tr.find('td', {"align" : "right"})
                    currentKey = cellLHS.get_text().replace(':', '').strip()
                    cellRHS = tr.find('td', {"align" : "left"})
                    currentValue = re.findall('(?<=\>)(.*?)(?=\<)',str(cellRHS))
                    currentValue = " ".join(currentValue)
                    if "%" in str(currentValue):
                            percent[id][currentKey] = re.findall('(?<=<\/script><\/b>)(.*?)(?=<br)',str(cellRHS))
                    if "Relaciona" in str(currentValue):
                        currentValue = re.findall('(?<="10")(.*?)(?="1FS2021")',str(cellRHS))
                        currentValue = "".join(currentValue)
                        currentValue = currentValue.split(",")
                        currentValue = list(set(currentValue))
                        currentValue = ", ".join(currentValue)
                        currentValue = currentValue.lstrip(",")
                        currentValue = currentValue.strip()
                        currentValue = currentValue.replace('"',"")
                    if "MesEx" in str(currentValue):
                         for m, v in month_mapper.items():
                            currentValue = currentValue.replace(m,v)
                         currentValue = currentValue.strip()
                         currentValue = currentValue.replace(" ","/")
                         currentValue = currentValue.replace(",/",", ")
                    if currentKey =='Sócios instituições e quotas':
                        currentValue = re.findall('(?<=,")(.*?)(?="\n)',str(cellRHS))
                        currentValue = ", ".join(list(set(currentValue)))
                    out[currentKey] = currentValue
            fetch[id] = out
        except IndexError:
            continue

    out = percent_in_fetch(percent, fetch)

    multi_tab = {k:v for k,v in number_of_tables.items() if v>1}

    return out, multi_tab

def check_date_errors(date):
    """
    Drops date entries that do not make sense.

    Parameters
    ----------
    date : TYPE
        DESCRIPTION.

    Returns
    -------
    date : TYPE
        DESCRIPTION.

    """
    nodate = {k:v for k,v in date.items() if len(v.split("/")[-1]) != 4}

    date = {k:v for k,v in date.items() if len(v.split("/")[-1]) == 4}

    nodate.update({k:v for k,v in date.items() if int(v.split("/")[0]) > 31
                  })

    for d in  ['31','29']:
        date = {k: v.replace(f"{d}/2/", "27/2/") for k,v in date.items()}
        nodate.update({k:v for k,v in date.items() if f"{d}/2/" in v})


    date = {k:v for k,v in date.items() if int(v.split("/")[0]) < 32}

    date = {k: dt.strptime(v, '%d/%m/%Y') for k, v in date.items()}
    x = PrettyTable()
    x.field_names = ["ID do Registo", "Date value"]
    for e in nodate:
        x.add_row([e, nodate[e]])

    print("Column dates that do not work: \n", x,
          "\n", len(nodate), "rows")
    return date



def define_publication_file(df):
    """
    Convert the "Publicado em" column in df with
    date, name  and page of puplication

    Parameters
    ----------
    df : fetched entry column (pd.DataFramae)

    Returns
    -------
    out : Annocument details (pd.DataFrame)

    """
    full_months = {'janeiro': 1,  'fevereiro': 2, u'março': 3,    'abril': 4,
               'maio': 5,     'junho': 6,     'julho': 7,     'agosto': 8,
               'setembro': 9, 'outubro': 10,  'novembro': 11, 'dezembro': 12}

    full_months = {f"de {k} de": str(v) for k,v in full_months.items()}
    puplc = dict(zip(df.index,df['Publicado em']))
    for e in list(full_months):
        puplc = {k: v.lower().replace(e, full_months[e]) for k,v in puplc.items()}

    puplc = {k: v.split(" - ") for k,v in puplc.items()}
    page = {k: v[1] for k,v in puplc.items() if len(v) > 1}
    page = {k: v.replace("pág. ","") for k,v in page.items()}

    doc = {k: v[0] for k,v in puplc.items() }

    doc = {k: v.replace("iii série", "") for k,v in doc.items()}
    date = {k: v.split(" de ")[1] for k,v in doc.items() }
    date = {k: v.strip().replace(" ","/") for k,v in date.items()}
    date = {k: v.strip().replace("."," ") for k,v in date.items()}
    date = {k: v.strip().strip() for k,v in date.items()}

    date = check_date_errors(date)


    year = {k: str(v.year) for k, v in date.items()}
    doc = {k: v.split(" de ")[0] for k,v in doc.items() }
    doc = {k: v.replace(", ,",",") for k,v in doc.items()}
    doc = {k: v.replace("br nº ","") for k,v in doc.items()}
    doc = {k: v.strip() for k,v in doc.items()}
 # check out if I convert this to a year dunno if its  agood idea to add the year
    print (" \n Report BR number with year: \n")
    br_3_num = {k: v+"("+year[k]+")" for k,v in tqdm(doc.items()) if k in list(year)}
    br_3_num = {k: v.replace(",,",", ") for k,v in br_3_num.items()}
    br_3_num = {k: v.replace(",("," (") for k,v in br_3_num.items()}

    out = pd.DataFrame(index = df.index)
    out["BR_III_number"] = out.index.map(br_3_num)
    out['publication_date'] = out.index.map(date)
    out['page'] = out.index.map(page)


    return out


