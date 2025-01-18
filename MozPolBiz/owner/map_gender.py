# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 12:51:05 2022

@author: fs.egb
"""

def map_gender(base, other):
    """
    Maps Gender estimates on the first name of each name string.

    Parameters
    ----------
    base : DataFrame
        Contains all mapping on unqiue names, raw string, clean string etc.
    other : dict
        name data from portugese and brazilian first names.

    Returns
    -------
    base : TYPE
        DESCRIPTION.

    """

    # gender = other['gender']
    base['first'] = base['gamma_clean'].apply(lambda x: x.split(" ")[0])


    count_first_names = base['first'].value_counts()
    base['freq_first_name'] =  base['first'].map(count_first_names)

    base['gender'] =  base['first'].map(gender)

    base['last_two']= base['first'].apply(lambda x: x[-2:])


    base['last_one']= base['first'].apply(lambda x: x[-1:])

    for x in ['us','ed']:
        base.loc[base['last_two'] ==x, 'prFemale'] = 0

    for x in ['o']:
        base.loc[base['last_one']==x, 'prFemale'] = 0

 # map explicit males
    for x in ['muhammad','mahomed','momade','mohammad','mamadou','momad',
              'samora','zacaria','sousa', 'ragendra','faruk','kenneth', 'colin',
              'christiaan', "josa(c)"]:
        base.loc[base['first']==x, 'prFemale'] = 0

 # map explicit females
    for x in ['amina','saquina']:
        base.loc[base['first']==x, 'prFemale'] = 1

    base['gender'] = base['gender'].fillna(base['prFemale'])


    missing = base.loc[base['gender'].isna()]

    print("two most commen first names defined as 0.5: \n",
         missing['first'].value_counts().head(20))

    base['gender'] = base['gender'].fillna(0.5)

    base = base.drop(columns = ['gamma_clean', 'first', 'freq_first_name',
                                'last_two', 'last_one', 'prFemale'])

    return base
