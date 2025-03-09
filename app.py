import sys
import pandas as pd
from flask import Flask, request, render_template
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline
from src.exception_handler import CustomException
from datetime import datetime
import os

application = Flask(__name__)
app = application

# Route for the homepage
@app.route("/")
def index():
    out1 = "First Output"
    out2 = "Second Output"
    out3 = "Third Output"
    return render_template("home.html")

# Route for prediction
@app.route("/predict", methods=["GET", "POST"])
def prediction():
    # Mapping for the weekdays to numeric values
    day_dict = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }

    if request.method == "POST":
        try:
            # Extract values from the form
            date = request.form.get("date")
            air_temperature_mean = float(request.form.get("air_temperature_mean"))
            dewpoint_mean = float(request.form.get("dewpoint_mean"))
            rltv_hum_mean = float(request.form.get("rltv_hum_mean"))
            air_temperature_min = float(request.form.get("air_temperature_min"))
            rltv_hum_min = float(request.form.get("rltv_hum_min"))
            air_temperature_max = float(request.form.get("air_temperature_max"))
            prcp_count = int(request.form.get("prcp_count"))
            day = day_dict[str(request.form.get("day"))]
            holiday = 1 if request.form.get("holiday") == "on" else 0

            # Creating an instance of CustomData
            data = CustomData(
                date=pd.to_datetime(date),
                air_temperature_mean=air_temperature_mean,
                dewpoint_mean=dewpoint_mean,
                rltv_hum_mean=rltv_hum_mean,
                air_temperature_min=air_temperature_min,
                rltv_hum_min=rltv_hum_min,
                air_temperature_max=air_temperature_max,
                prcp_count=prcp_count,
                day=day,
                holiday=holiday
            )

            # Convert data to DataFrame for prediction
            pred_df = data.get_data_as_frame()
            root_path = "data/user_data/"
            datetime_path = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.csv"
            user_data_path = os.path.join(root_path, datetime_path)
            pred_df.to_csv(user_data_path, index=False)

            # Create an instance of PredictPipeline and predict
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(user_data_path)

            user_data=pd.read_csv(user_data_path)
            user_data["mean_consumption"]=results[0][0]
            user_data["median_consumption"]=results[0][1]
            user_data["std_consumption"]=results[0][2]
            user_data.to_csv(user_data_path, index=False)


            # Returning the prediction results to the template
            return render_template("home.html", prediction=True, out1=results[0][0], out2=results[0][1], out3=results[0][2])

        except Exception as e:
            raise CustomException(f"Error during prediction: {str(e)}", sys)

    return render_template("home.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
