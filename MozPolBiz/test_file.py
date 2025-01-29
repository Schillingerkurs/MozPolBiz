#%%

import pandas as pd



df = pd.read_pickle("../data/interim/firmregister_full.pkl")


df = format_stata_vars(df)





#%%


