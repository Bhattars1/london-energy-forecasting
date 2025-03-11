import sys
import os
import dill
import pickle

import pandas as pd
import numpy as np
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

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def recognize_holiday(date_):
    try:
        bank_holidays = pd.read_excel("../data/public holiday/ukbankholidays-jul19.xls")
        bank_holidays["UK BANK HOLIDAYS"] = pd.to_datetime(bank_holidays["UK BANK HOLIDAYS"], format = "%Y/%m/%d")
        date_=pd.to_datetime(date_)
        if date_ in bank_holidays["UK BANK HOLIDAYS"].values:
            return 1
        else:
            return 0
        
    except Exception as e:
        raise CustomException(e, sys)




def recognize_day(date_):
    try:
        date_=pd.to_datetime(date_)
        day = date_.weekday()
        return day
    except Exception as e:
        raise CustomException(e, sys)
        


