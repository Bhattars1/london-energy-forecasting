import sys
import os
import pandas as pd
import numpy as np
import dill
from sklearn.metrics import r2_score

from src.exception_handler import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    



def evaluate_models(X_train, y_train, model):
    try:
        report = {}
        model.fit(X_train,y_train)
        y_train_pred = model.predict(X_train)
        train_model_score = r2_score(y_train, y_train_pred)
        report["r-squared score"] = train_model_score

       

    except Exception as e:
        raise CustomException(e, sys)