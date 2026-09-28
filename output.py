import csv 
import config 
import numpy
import pandas as pd 

def dict_to_df(master_list) : 

    # 1. Flatten into a single list of dictionaries
    flattened_data = [d for sublist in master_list for d in sublist]
    # 2. Convert directly to a single DataFrame
    df = pd.DataFrame(flattened_data)
    return df 
    
    
    