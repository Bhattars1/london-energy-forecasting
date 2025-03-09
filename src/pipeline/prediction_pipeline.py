import sys
import pandas as pd
from src.exception_handler import CustomException
from src.utils import load_object
from src.components.data_preprocessing import DataPreprocessing, DataPreprocessingConfig


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, data_path):
        try:
            model_path = "artifacts/model.pkl"
            preprocessor_path = "artifacts/preprocessor.pkl"
            model=load_object(file_path=model_path)
            preprocessor=DataPreprocessing()
            data_scaled,_ = preprocessor.data_preprocessor(data_path=data_path)
            preds = model.predict(data_scaled.iloc[:, 1:])
            return preds
        except Exception as e:
            raise CustomException(e,sys)


class CustomData:
    def __init__(self,
        date: pd.Timestamp,
        air_temperature_mean: float,
        dewpoint_mean: float,
        rltv_hum_mean: float,
        air_temperature_min: float,
        rltv_hum_min: float,
        air_temperature_max: float,
        prcp_count: int,
        day: str,
        holiday: bool):
        self.date = date
        self.air_temperature_mean= air_temperature_mean
        self.dewpoint_mean=dewpoint_mean
        self.rltv_hum_mean= rltv_hum_mean
        self.air_temperature_min=air_temperature_min
        self.rltv_hum_min=rltv_hum_min
        self.air_temperature_max=air_temperature_max
        self.prcp_count=prcp_count
        self.day=day
        self.holiday=holiday

    def get_data_as_frame(self):
        try:
            custom_data_input_dict = {
                "date": [self.date],
                "air_temperature_mean": [self.air_temperature_mean],
                "dewpoint_mean": [self.dewpoint_mean],
                "rltv_hum_mean": [self.rltv_hum_mean],
                "air_temperature_min": [self.air_temperature_min],
                "rltv_hum_min": [self.rltv_hum_min],
                "air_temperature_max": [self.air_temperature_max],
                "prcp_count": [self.prcp_count],
                "day": [self.day],
                "holiday": [self.holiday]
            }
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e,sys)


