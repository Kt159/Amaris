import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

def basic_descriptive_stats(df):
    """
    Compute descriptive statistics for drinks and food datasets.

    Inputs:
    df (pd.DataFrame): The dataframe to compute basic statistics for

    Outputs:
    dict: A dictionary containing basic statistics
    """
    df_stats = {
        "total_calories": df["Calories"].sum(),
        "average_sugar_content": df["Carb."].mean(),
        "fat_to_protein_ratio": (df["Fat"] / df["Protein"]).mean()
    }
    return df_stats

def visualize_data(drinks_df, food_df, nutrient):
    """
    Generate visualizations comparing specific nutrient category.

    Inputs:
    drinks_df (pd.DataFrame): The drinks dataframe
    food_df (pd.DataFrame): The food dataframe
    nutrient (str): The nutrient to compare (e.g. "Calories")

    Outputs:
    dict: A dictionary containing base64 strings of the generated plots
    """
    sns.set_theme(style="whitegrid")
    colors =['#A6CEE3', '#FB9A99'] # Set color palette (blue for drinks, red for food)

    drink_copy = drinks_df.copy()
    food_copy = food_df.copy()

    # Combine drinks and food data for comparison
    drink_copy['Category'] = 'Drinks'
    food_copy['Category'] = 'Food'
    combined_df = pd.concat([drink_copy, food_copy])

    # Function to convert plot to base64 string for rendering in Flask app
    def plot_to_base64():
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode("utf-8")

    # Plot 1: Average Nutrient (Drinks vs Food)
    plt.figure(figsize=(8, 5))
    avg = {
        "Drinks": drinks_df[nutrient].mean(),
        "Food": food_df[nutrient].mean()
    }
    plt.bar(x=list(avg.keys()), height=list(avg.values()), color=colors)
    plt.title(f"Average {nutrient}: Drinks vs Food")
    plt.ylabel(nutrient)
    avg_plot_base64 = plot_to_base64()
    plt.close()

    # Plot 2: Total Nutrient (Drinks vs Food)
    plt.figure(figsize=(8, 5))
    total = {
        "Drinks": drinks_df[nutrient].sum(),
        "Food": food_df[nutrient].sum()
    }
    plt.bar(x=list(total.keys()), height=list(total.values()), color=colors)
    plt.title(f"Total {nutrient}: Drinks vs Food")
    plt.ylabel(nutrient)
    total_plot_base64 = plot_to_base64()
    plt.close()

    # Plot 3: Nutrient Distribution (Drinks vs Food)
    plt.figure(figsize=(8, 5))
    sns.boxplot(x="Category", y=nutrient, data=combined_df, hue="Category", palette=colors, legend=False)
    plt.title(f"{nutrient} Distribution: Drinks vs Food")
    dist_plot_base64 = plot_to_base64()
    plt.close()

    # Return the base64 strings
    return {
        "avg_plot": avg_plot_base64,
        "total_plot": total_plot_base64,
        "dist_plot": dist_plot_base64
    }