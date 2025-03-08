import os
import sys
import pandas as pd
from dataclasses import dataclass

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))



from src.exception_handler import CustomException
from src.logger import logging
from src.components.data_preprocessing import DataPreprocessing, DataPreprocessingConfig


@dataclass
class DataIngestionConfig:
    data_path: str = os.path.join("artifacts", "data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_ingestion(self):
        logging.info("Data ingestion Initiated")
        try:
            df = pd.read_csv(r"data\processed data\processed_data.csv")
            logging.info("Read the data successfully!")

            os.makedirs(os.path.dirname(self.ingestion_config.data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.data_path, index=False, header=True)
            logging.info("Data Ingestion is Successful")

            return self.ingestion_config.data_path
            
        except Exception as e:
            raise CustomException(e, sys)
        

if __name__ == "__main__":
    obj = DataIngestion()
    data_path = obj.initiate_ingestion()
    data_preprocessing = DataPreprocessing()
    data_preprocessing.data_preprocessor(data_path)


    