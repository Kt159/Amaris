# Nutrient Analysis Tool

## Overview
The Nutrient Analysis Tool is a web application built with Flask and Docker that allows users to upload food and drink datasets, filter and analyze the data, and generate insights using a large language model (LLM). The tool provides a user-friendly interface for exploring nutritional data, generating summaries, and visualizing trends.

## Features
- **Upload Datasets**: Upload CSV files containing food and drink nutritional data.
- **Filter Data**: Apply filters to the datasets based on specific columns and values.
- **Dynamic Updates**: Filtered data is displayed dynamically without reloading the page.
- **LLM Integration**: Generate summaries and insights using a large language model (e.g., Llama-3.3-70b-versatile).
- **Visualizations**: View plots and charts for nutrient comparisons and trends.

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: Pandas
- **Containerization**: Docker
- **LLM Integration**: Llama-3.3-70b-versatile (or similar model)

---

## Installation

### Prerequisites
- Docker installed on your machine.
- Python 3.12.2 or higher (for local development).

### Steps

1. **Clone the Repository**

2. **Build the Docker Image**:
   ```bash
   docker build -t nutrient-analysis-tool . 
   ```
3. **Run the Container**:
   ```bash
   docker run --env-file .env -p 5000:5000 nutrient-analysis-tool
   ```
4. **Access the Application**:
   Open your browser and navigate to:
   http://localhost:5000

## Usage

### Upload Datasets
- Use the "Upload Food CSV" and "Upload Drinks CSV" forms to upload your datasets.
- Ensure the CSV files have the required columns. (Example datasets given)

### Filter Data
- Use the filter forms to apply filters to the datasets.
- Choose a column, comparison operator (`=`, `>`, `<`), and value to filter the data.

### Explore Visualizations
- Use the dropdown to select a nutrient.
- View plots such as **average**, **total**, and **distribution**.

### Generate Insights
- View the summary in the **"Nutritional Insights"** section.
- Write your own questions and click the **"Ask"** button to get insights from the LLM about the dataset.
---
## Project Structure
```text
nutrient-analysis-tool/
├── flask-app/
|   ├── app.py
│   ├── functions
|   │     ├──__init__.py
│   │     ├── data_ingestion.py
│   │     ├── data_processing.py
|   │     ├── filter.py
|   │     └── llm_summary.py
│   ├── templates/
│   │   └── index.html
│   ├── static/uploads
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── README.md
└── .env 
```
## Configuration
### Environment Variables:
- Create a `.env` file in the root directory to store environment variable (Groq API Key)

Example `.env` file:
```.env
GROQ_API_KEY=<YOUR API KEY>
```

   
