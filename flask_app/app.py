from flask import Flask, render_template, request, jsonify
import os
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' 

from functions.data_ingestion import load_data, clean_df
from functions.data_processing import visualize_data, basic_descriptive_stats
from functions.filter import filter_data
from functions.llm_summary import llm_query, summarize_nutrition

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables to store the cleaned datasets
food_clean = None
drinks_clean = None

@app.route("/", methods=["GET", "POST"])
def home():
    global food_clean, drinks_clean
    plots_base64 = None
    food_summary = None
    drinks_summary = None
    llm_summary = None

    # Handle file uploads
    if request.method == "POST":

        if "food_file" in request.files:
            food_file = request.files["food_file"]
            if food_file.filename != "":
                food_path = os.path.join(app.config['UPLOAD_FOLDER'], "food.csv")
                food_file.save(food_path)

        if "drinks_file" in request.files:
            drinks_file = request.files["drinks_file"]
            if drinks_file.filename != "":
                drinks_path = os.path.join(app.config['UPLOAD_FOLDER'], "drinks.csv")
                drinks_file.save(drinks_path)

    # Check if files exist and load/process them
    food_path = os.path.join(app.config['UPLOAD_FOLDER'], "food.csv")
    drinks_path = os.path.join(app.config['UPLOAD_FOLDER'], "drinks.csv")

    if os.path.exists(food_path):
        food_df = load_data(food_path)
        food_clean = clean_df(food_df)
        food_summary = basic_descriptive_stats(food_clean)

    if os.path.exists(drinks_path):
        drinks_df = load_data(drinks_path)
        drinks_clean = clean_df(drinks_df)
        drinks_summary = basic_descriptive_stats(drinks_clean)

    # Generate plots if both datasets are uploaded
    if food_clean is not None and drinks_clean is not None:
        plots_base64 = visualize_data(drinks_clean, food_clean, "Calories")
        llm_summary = summarize_nutrition(drinks_clean, food_clean)

    # Render the template with data
    return render_template(  #Add basic descriptive statistics to the template (basic_descriptive_stats(df)) + LLM based summary statistics
        "index.html", 
        food_df=food_clean,
        drinks_df=drinks_clean,
        plots=plots_base64,
        food_summary=food_summary,
        drinks_summary=drinks_summary,
        llm_summary=llm_summary,
    )

@app.route("/update_plots", methods=["POST"])
def update_plots():
    # Get the selected nutrient from the request
    nutrient = request.form.get("nutrient")

    # Load and clean the data
    food_path = os.path.join(app.config['UPLOAD_FOLDER'], "food.csv")
    drinks_path = os.path.join(app.config['UPLOAD_FOLDER'], "drinks.csv")

    if os.path.exists(food_path) and os.path.exists(drinks_path):
        food_df = load_data(food_path)
        drinks_df = load_data(drinks_path)
        food_clean = clean_df(food_df)
        drinks_clean = clean_df(drinks_df)

        # Generate plots for the selected nutrient
        plots_base64 = visualize_data(drinks_clean, food_clean, nutrient)
        return plots_base64  

    return {"error": "Data not found"}, 400

@app.route("/filter", methods=["POST"])
def handle_filter():
    global food_clean, drinks_clean

    # Get the filter parameters from the request
    dataset = request.form.get("dataset")  # "food" or "drink"
    sign = request.form.get("sign")
    column = request.form.get("column")
    value = float(request.form.get("value"))

    if dataset not in ["food", "drink"]:
            return jsonify({"error": "Invalid dataset. Use 'food' or 'drink'."}), 400

    # Get the appropriate dataset
    if dataset == "food":
        data = food_clean
    else:
        data = drinks_clean

    # Check if data is available
    if data is None:
        return jsonify({"error": f"No {dataset} data available. Please upload the dataset first."}), 400

    try:
        # Filter the data
        filtered_data = filter_data(data, column, sign, value)
        filtered_html = filtered_data.to_html(classes="table", index=False)

        return jsonify({
            "filtered_html": filtered_html
        }), 200

    except ValueError as e:
        # Handle invalid value (e.g., non-numeric value)
        return jsonify({"error": f"Invalid value: {str(e)}"}), 400
    except KeyError as e:
        # Handle invalid column name
        return jsonify({"error": f"Invalid column: {str(e)}"}), 400
    except Exception as e:
        # Log the error for debugging
        print(f"Error in /filter route: {str(e)}")
        return jsonify({"error": "An internal server error occurred."}), 500


@app.route("/query", methods=["POST"])
def handle_query():
    global food_clean, drinks_clean

    # Get the user's query
    user_query = request.form.get("query")

    # Ensure both datasets are loaded
    if food_clean is not None and drinks_clean is not None:
        # Call the llm_query function
        response = llm_query(drinks_clean, food_clean, user_query)
        return jsonify({"response": response})
    else:
        return jsonify({"error": "Data not loaded. Please upload both datasets first."})
    

if __name__ == "__main__":
    app.run(debug=True)