import pandas as pd
import numpy as np

def extract_year(date_text):
    """
      numerical encoding the eruption year
      input: text format of date
      output: the float representation of the year
    """
    y = int(date_text.strip()[:4])
    return y*np.sign(0.5-('BCE' in date_text))

def update_data(data_folder):
    """
      Prepare data from files
      input: the folder location of data
      output: data frame after cleaning
    """
    # Clean eruption Data
    eruption = pd.read_csv(f'{data_folder}/GVP_Eruption_Results.csv')
    eruption = eruption.dropna(subset=['Start Date'])
    eruption['Max VEI'] = eruption['Max VEI'].replace('--',np.nan).astype(float)
    eruption['Year'] = eruption['Start Date'].apply(extract_year)

    # clean volcano data 
    volcano = pd.read_csv(f'{data_folder}/GVP_Volcano_List.csv')
    volcano = volcano.drop_duplicates(subset=['Volcano Name'], keep = False)
    nan_symbol = volcano.iloc[0]['Major Rock 5']
    volcano = volcano.replace(nan_symbol, np.nan)

    # Join two datasets.
    df = eruption.merge(volcano, on = 'Volcano Name')
    # attach time columns
    df['Centry'] = df['Year']//100
    df['Decades'] = df['Year']//10
    
    return df
