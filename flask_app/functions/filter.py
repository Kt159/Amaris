import pandas as pd

def filter_data(df, column, sign, value):
    """
    Filter the dataframe based on a specific column, comparison operator, and value.

    Inputs:
    df (pd.DataFrame): The dataframe to filter.
    column (str): The column to filter on.
    sign (str): The comparison operator (e.g."==", ">", "<").
    value: The value to filter on.
    ascending (bool): Whether to sort the filtered dataframe in ascending order. Default is False.

    Outputs:
    pd.DataFrame: The filtered and sorted dataframe. Returns an empty DataFrame if the column does not exist.
    """
    df = df.copy()

    if column not in df.columns:
        print(f"Warning: Column '{column}' does not exist in the DataFrame.")
        return pd.DataFrame()
    
    if sign == "=":
        filtered_df = df[df[column] == value]

    elif sign == ">":
        filtered_df = df[df[column] > value]
    
    elif sign == "<":
        filtered_df = df[df[column] < value]

    else:
        raise ValueError(f"Unsupported sign: '{sign}'. Use one of: '=', '>', '<'.")

    filtered_df = filtered_df.sort_values(by=column, ascending=False)

    return filtered_df