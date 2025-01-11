# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 17:18:06 2022

@author: fs.egb
"""
from numpy import arange
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV


# def select_features_for_classifier(df):
#     temp = df[['orga_type', 'limitada_dummy', 'lda_dummy', 'scrl_dummy',
#        's. a. r. l._dummy', 'cooperativa_dummy', ' s.a._dummy',
#        'len_Beneficial owner', 'len_Institution owner',
#        'len_Previous_partners', 'len_Previous members institutions']]

    
#     for_lasso = temp[temp['orga_type']!='']
    
#     for_lasso = for_lasso.fillna(0)
    
       
#     X =  for_lasso[['limitada_dummy', 'lda_dummy', 'scrl_dummy',
#        's. a. r. l._dummy', 'cooperativa_dummy', ' s.a._dummy',
#        'len_Beneficial owner', 'len_Institution owner',
#        'len_Previous_partners', 'len_Previous members institutions']].to_numpy()
    
    
#     outcome_mapper ={}
#     features = list(for_lasso['orga_type'].unique())
#     for e,k in enumerate(features):
#         outcome_mapper[k] = e 
        
#     for_lasso['orga_type'] = for_lasso['orga_type'].replace(outcome_mapper)
   
        
    
    
#         # set panel for the LASSO
    

#     return df




def impute_with_lasso(df):
 temp
    prepared = prepared.copy()
   
    

        
    y = for_lasso['orga_type'].to_numpy()
    
    model = Lasso()
    
    # define model evaluation method
    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    # define grid
    grid = dict()
    grid['alpha'] = arange(0.1, 1, 0.01)
    # define search
    search = GridSearchCV(model, grid, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
    # perform the search
    results = search.fit(X, y)
    # summarize
    print('MAE: %.3f' % results.best_score_)
    print('Config: %s' % results.best_params_)
    
    print('Predicted: %.3f' % yhat)