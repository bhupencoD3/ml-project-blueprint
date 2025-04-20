from flask import Flask, render_template, request
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Flask app instance
application = Flask(__name__)
app = application


@app.route("/", methods=["GET"])
def index():
    """
    Serves the landing page (index.html)
    """
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
    Handles both GET (form page) and POST (prediction request) methods.

    GET: Shows form to user
    POST: Takes form input, runs model prediction, renders result
    """
    if request.method == "GET":
        return render_template("home.html")
    else:
        # Extract data from the form submitted by user
        data = CustomData(
            gender=request.form.get("gender"),
            race_ethnicity=request.form.get("race_ethnicity"),
            parental_level_of_education=request.form.get("parental_level_of_education"),
            lunch=request.form.get("lunch"),
            test_course=request.form.get("test_preparation_course"),
            reading_score=request.form.get("reading_score"),
            writing_score=request.form.get("writing_score"),
        )

        # Convert user data to DataFrame
        pred_df = data.get_data_as_dataframe()
        print(pred_df)

        # Run prediction using our pipeline
        predict_pipeline = PredictPipeline()
        result = predict_pipeline.predict(pred_df)

        # Clean the result (ensure it's within [0, 100] range)
        result = min(100, max(0, round(result[0], 2)))
        print(result)

        return render_template("result.html", prediction=result)


@app.route("/about")
def about():
    """
    Renders the About Us page
    """
    return render_template("about.html")


@app.route("/contact")
def contact():
    """
    Renders the Contact page
    """
    return render_template("contact.html")


if __name__ == "__main__":
    # Run app on all IPs of host machine (e.g., for deployment)
    app.run(host="0.0.0.0")
