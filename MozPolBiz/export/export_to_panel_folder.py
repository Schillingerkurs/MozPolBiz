# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 06:31:59 2022

@author: fs.egb
"""

import pyreadr
from pathlib import Path



def export_to_panel_folder(export, filename, HERE):
    """
    Exports panel to R or Stata

    Parameters
    ----------
    panel_full : pd.DataFrame
        panel to export

    filename : String
        name of the panel
    pipeline_folder : String
        folder in the pipeline directory for export.       

    Returns
    -------
    None.

    """
    if "m" in export.keys():
        export = export.drop(columns = ['m'])

    local_path  = HERE/Path("data","processed")
    

    pyreadr.write_rdata(local_path/Path(f"{filename}.RData"), export, \
                          df_name = filename, compress="gzip")
            
    print(f"Saved panel as {filename}.RData in {local_path}")
    return 