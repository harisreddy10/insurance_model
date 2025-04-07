# server/util.py
import pickle
import json
import numpy as np
import os

__model = None
__data_columns = None
__categorical_options = {
    "sex": ["male", "female"],
    "smoker": ["yes", "no"],
    "region": ["northeast", "northwest", "southeast", "southwest"]
}

def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global __data_columns
    global __model

    base_path = os.path.dirname(__file__)
    columns_path = os.path.join(base_path, 'artifacts', 'columns.json')
    model_path = os.path.join(base_path, 'artifacts', 'insurance_expense_model.pickle')

    with open(columns_path, "r") as f:
        __data_columns = json.load(f)["data_columns"]

    with open(model_path, "rb") as f:
        __model = pickle.load(f)

    print("Loading saved artifacts...done")

def get_data_columns():
    return __data_columns

def get_categorical_options():
    return __categorical_options

def get_estimated_expense(age, bmi, children, sex, smoker, region):
    x = np.zeros(len(__data_columns))
    x[0] = age
    x[1] = bmi
    x[2] = children

    try:
        sex_col = f"sex_{sex.lower()}"
        smoker_col = f"smoker_{smoker.lower()}"
        region_col = f"region_{region.lower()}"

        for col in [sex_col, smoker_col, region_col]:
            if col in __data_columns:
                idx = __data_columns.index(col)
                x[idx] = 1
    except:
        pass

    log_prediction = __model.predict([x])[0]
    return round(np.exp(log_prediction), 2)

if __name__ == "__main__":
    load_saved_artifacts()

    print("\n🔍 Test Case 1 – Smoker, Male, Northwest")
    print("Estimated Expense:", get_estimated_expense(30, 28.5, 2, "male", "yes", "northwest"))

    print("\n🔍 Test Case 2 – Non-Smoker, Female, Southeast")
    print("Estimated Expense:", get_estimated_expense(45, 22.0, 1, "female", "no", "southeast"))

    print("\n🔍 Test Case 3 – Young Non-Smoker, No Kids")
    print("Estimated Expense:", get_estimated_expense(23, 18.4, 0, "male", "no", "southwest"))

    print("\n🔍 Test Case 4 – Invalid Input (unknown region)")
    try:
        print("Estimated Expense:", get_estimated_expense(35, 25.0, 2, "male", "yes", "moonbase"))
    except Exception as e:
        print("Error:", str(e))
