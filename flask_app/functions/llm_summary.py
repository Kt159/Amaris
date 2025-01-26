import os
from groq import Groq

def summarize_nutrition(drinks_df, food_df):
    """
    Use Groq LLM API to summarize nutritional insights.

    Inputs:
    drinks_df (pd.DataFrame): The drinks dataframe
    food_df (pd.DataFrame): The food dataframe

    Outputs:
    str: A summary of the nutritional insights
    """

    # Get basic descriptive statistics for the datasets
    drink_summary = drinks_df.describe().to_json(orient="split") #orient="split" to maintain the structure of the DataFrame (columns, index, data)
    food_summary = food_df.describe().to_json(orient="split") 


    # Few-Shot prompt for LLM Model + Pass the summary statistics
    prompt = f"""
    Compare the nutritional data from the following datasets column by column. If a column exists in one dataset but not the other, inform the user and skip the comparison for that column. 
    Provide a concise summary of the differences for matching columns.

    Format the response using HTML tags as follows:
    - Use `<h3>` for headings.
    - Use `<ul>` and `<li>` for lists.
    - Use `<p>` for paragraphs.
    - Use `<strong>` for emphasis.

    Drinks Dataset:
    {drink_summary}

    Food Dataset:
    {food_summary}

    Your response should be structured like this:
    <h3>Column Comparison</h3>
    <ul>
        <li><strong>Column z:</strong> Comparison details...</li>
        <li><strong>Column y:</strong> Comparison details...</li>
        <li><strong>Column x:</strong> Comparison details...</li>
    </ul>
    <h3>Summary</h3>
    <p>Overall comparison summary...</p>
    """

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content



def llm_query(drinks_df, food_df, query):
    """
    Use Groq LLM API to reply to a user query.

    Inputs:
    drinks_df (pd.DataFrame): The drinks dataframe
    food_df (pd.DataFrame): The food dataframe
    query (str): The user query

    Outputs:
    str: The response to the user query
    """
    # Convert DataFrames to JSON for the LLM to analyze
    drinks_json = drinks_df.to_json(orient="split") #orient="split" to maintain the structure of the DataFrame (columns, index, data)
    food_json = food_df.to_json(orient="split")

    # Few-Shot prompt for LLM Model + Pass the summary statistics
    prompt = f"""
    You are a helpful assistant that answers questions about the Starbucks menu data.
    You have access to two datasets containing information about the nutritional contents: one for drinks and one for food. 

    Drinks Dataset:
    {drinks_json}

    Food Dataset:
    {food_json}

    User Query:
    {query}

    Instructions:
    1. Analyze the provided JSON data to answer the user query.
    2. If the query requires a comparison between the datasets, make sure to compare the relevant columns.
    3. If the query cannot be answered with the available data, inform the user.
    4. Return ONLY the answer to the user query.
    """

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content


