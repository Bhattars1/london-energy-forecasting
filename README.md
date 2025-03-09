# Energy Demand Forcasting Based on Weather and Time-Based Patterns in London Households

## Introduction
Accurately predicting household energy consumption is essential for efficient energy management and promoting sustainability, particularly in a dynamic urban environment like London. This project aims to investigate the relationship between weather patterns, time-based patterns (including day of the week, weekdays vs. weekends, and holidays), and household energy consumption across London. This project primarily focuses on developing modular structure of production standard with basic logging and exception handling. 

## Data and Preprocessing
### Weather Data
The weather data used in this project was collected from the **Centre for Environmental Data Analysis (CEDA)** (https://data.ceda.ac.uk/), an archive repository of atmospheric and Earth observation data. While CEDA observes hundreds of parameters, it was not feasible to use all of them in this analysis. Therefore, only the following seven key parameters were considered:
1. Mean, Minimum, and Maximum Air Temperature
2. Mean Dewpoint
3. Mean and Minimum Relative Humidity
4. Hourly Precipitation Counts

The data cleaning and preprocessing were conducted in notebooks, where several techniques were applied to handle missing or inconsistent data:

**Missing Parameters (N/A values)**: If a parameter was missing, it was imputed using data from the previous year at the exact same time (i.e., t – 365 days).

**Missing Dates**: If a date was missing, the first option was to fill the gap with data from the previous year. If that data wasn’t available, the gap was filled using the monthly-hourly average across all available years.

### Energy Data
The energy consumption data was obtained from the **London Government Data Portal**, specifically the SmartMeter Energy Consumption Data in London Households dataset. This dataset includes energy consumption readings from a sample of 5,567 households in London, spanning from November 2011 to February 2014. 
Similar to the weather data, the energy consumption dataset was cleaned, formatted, and merged with the weather dataset. Additionally, the **day of the week and bank holiday** information were integrated into the combined dataset.
After cleaning and merging the datasets, an exploratory data analysis (EDA) was conducted using various visualization techniques. One significant insight from the EDA was that average energy consumption tends to be higher on weekends and bank holidays, highlighting the importance of these two factors in model development.

*The temperatures and dewpoint were measured in degree celcius, relative humidity was in percentage, and energy consumption in Kilo Watt Hour (kWh).*

### Further Preprocessing
In addition to the previous steps, further preprocessing was performed to extract useful temporal features for the model:

1. **Day of the Month**: The day of the month was extracted and stored in a separate column to capture the specific day within the month.

2. **Month of the Year**: The month of the year was also extracted and stored in a separate column. However, since weather conditions are often dependent on the month, this feature was encoded cyclically using sine and cosine trigonometric functions. This encoding ensures that the model can effectively capture the cyclic nature of months (i.e., December and January are close to each other in terms of seasonal patterns).

3. **Day of the Week**: Similarly, the day of the week was encoded in a cyclic manner using sine and cosine functions. This allows the model to capture the cyclical pattern of days (e.g., Monday is close to Sunday in terms of weekly trends).

## Model Development, Deployment and Dockerization
The baseline model development was carried out in a Jupyter notebook, where multiple machine learning models were trained and evaluated. The following models were used:

1. **Linear Regression**
2. **Polynomial Regression**
3. **XGBoost**

To evaluate model performance, cross-validation was employed, ensuring robust validation across different data subsets. All models showed promising results. However, XGBoost performed the best after fine-tuning key hyperparameters, such as gamma and eta, which improved its MSE and r-squared score.

The following table shows the performance of each model:
### Model Performance Comparison

| Model                | MSE   | r-squared score |
|----------------------|------------|-----------------------|
| Linear Regression    | 0.561       | 0.862                  |
| Polynomial Regression | 0.561        | 0.729  |
| XGBoost              | 0.565      | 0.885            |

Thus it was decided that XGBOOST will be used for the model development and deployment. After developing and training the model, a modular structure was implemented using Flask for deployment. Once the model was finalized, a Docker image was created to package the application for easy deployment.

The Docker image was then pushed to Docker Hub for sharing and deployment. To pull the image, use the following command:

``docker pull bhattars1/london-energy-forcasting-version-1.0``

