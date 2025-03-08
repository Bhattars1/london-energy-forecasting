import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
import os

from src.exception_handler import CustomException
from src.logger import logging
from src.utils import save_object

class CyclicDateEncoder:
    def __init__(self, date_column='date'):
        self.date_column = date_column

    def _cyclic_encode(self, values, max_value):
        """
        Generates sine and cosine encoding for cyclic values.
        """
        sin_values = np.sin(2 * np.pi * values / max_value)
        cos_values = np.cos(2 * np.pi * values / max_value)
        return sin_values, cos_values

    def add_cyclic_features(self, df):
        """
        Adds cyclic encoding columns for month, day of month, and day of week.
        """
        df[self.date_column] = pd.to_datetime(df[self.date_column], errors='coerce')
        # Extract date parts
        df['day_of_month'] = df[self.date_column].dt.day
        df['month'] = df[self.date_column].dt.month
        df['day_of_week'] = df[self.date_column].dt.weekday

        # Cyclic encoding
        df['month_sin'], df['month_cos'] = self._cyclic_encode(df['month'], 12)
        df['day_of_week_sin'], df['day_of_week_cos'] = self._cyclic_encode(df['day_of_week'], 7)

        # Drop the intermediate columns if you only want sin/cos
        df.drop(columns=['month', 'day_of_month', 'day_of_week'], inplace=True)

        return df



@dataclass
class DataPreprocessingConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")

class DataPreprocessing(CyclicDateEncoder):

    """ 
    This class is for data preprocessing
    """
    def __init__(self):
        self.data_preprocessing_config = DataPreprocessingConfig()

    def get_data_preprocessor_object(self):
        try:
            cyclic_encoder = CyclicDateEncoder(date_column="date")
        except Exception as e:
            raise CustomException(e, sys)
        
        return cyclic_encoder.add_cyclic_features
    
    def data_preprocessor(self, data_path):
        try:
            df = pd.read_csv(data_path)
    
            logging.info("Read the data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_preprocessor_object()

            target_columns = ['mean_consumption', 'median_consumption', 'std_consumption']
            target_features = df[target_columns]
            input_features = df.drop(columns = list(target_features.columns), axis=1)
            

            logging.info("Applying preprocessing object on the dataframe")   

            input_features_df = preprocessing_obj(input_features)

            data_arr = np.c_[input_features_df, np.array(target_features)]
            logging.info("Preprocessing completed") 

            save_object(

                    file_path=self.data_preprocessing_config.preprocessor_obj_file_path,
                    obj=preprocessing_obj

                        )
            return(
                    data_arr,
                    self.data_preprocessing_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)
    