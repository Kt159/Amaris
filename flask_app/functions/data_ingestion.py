import pandas as pd
import numpy as np
import chardet

def load_data(file_path):
    """
    This function loads the data from the specified file path.
    The encoding of the file is detected using the chardet package.

    Inputs:
    file_path (str): The path to the file

    Outputs:
    pd.DataFrame: The loaded dataframe
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read()) #Detect the file encoding 
        encoding = result['encoding']
    df = pd.read_csv(file_path, encoding=encoding)

    return df

def clean_df(df):
    """
    This function cleans the dataframe by:
    1. Rename the first column to 'Item'
    2. Strip leading/trailing whitespaces from column names
    3. Remove units from column names
    4. Converting all columns to numeric
    5. Removing rows with NaN values
    6. Removing duplicate rows (if any)
    7. Removing rows with all 0 values

    Inputs:
    df (pd.DataFrame): The dataframe to be cleaned

    Outputs:
    pd.DataFrame: The cleaned dataframe
    """
    df.rename(columns={df.columns[0]: 'Item'}, inplace=True) #Rename the first column to 'Item'
    df.columns = [name.strip().split(' ')[0] for name in df.columns] #Strip leading/trailing whitespaces from column names + Remove units from column names
    numeric = df.iloc[:, 1:].apply(lambda x: pd.to_numeric(x, errors='coerce')) #Convert non-item columns to numeric (coerce errors to NaN)
    df = pd.concat([df['Item'], numeric], axis=1) #Concatenate the 'Item' column with the numeric columns
    df.dropna(inplace=True) 
    df.drop_duplicates(inplace=True)
    df = df[[not all(row == 0) for row in df.iloc[:, 1:].values]] #Remove rows with all 0 values

    return df