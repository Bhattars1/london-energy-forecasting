import os
import sys
from dataclasses import dataclass
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import r2_score

from src.exception_handler import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

xgb = XGBRegressor(eta = 0.1, gamma = 4)
multioutput_model = MultiOutputRegressor(xgb)


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def model_trainer(self, data_array):
        try:
            logging.info("Training started,")
            features, target = (data_array[:,:-3], data_array[:,-3:])
            model = multioutput_model
            model_report:dict = evaluate_models(X_train= features, y_train = target, model=model)
            logging.info("Model training complete")
            save_object(file_path=self.model_trainer_config.trained_model_file_path,
                        obj = model)
            
            predicted = model.predict(features)
            r2 = r2_score(target, predicted)
            return r2

        except Exception as e:
            raise CustomException(e,sys)


