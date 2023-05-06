import json
import pickle
import numpy as np
import pandas as pd

__locations = None
__data_columns = None
__model = None

def get_estimated_price(area, bedroom, bathroom, area_sq_ft):
    try:
        loc_index = __data_columns.index(area)
    except:
        loc_index = -1

    input_data = {'bedroom': bedroom, 'bathroom': bathroom, 'area_sq_ft': area_sq_ft}
    input_data.update({col:0 for col in __data_columns if col not in ['bedroom', 'bathroom', 'area_sq_ft']})
    if loc_index >= 0:
        input_data[area] = 1
    input_df = pd.DataFrame([input_data], columns=__data_columns)
    
    # convert input_df to numpy array before making predictions
    input_np = input_df.to_numpy()

    return round(__model.predict(input_np)[0], 2)


def get_location_names():
    return __locations


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    with open("/home/subash/Desktop/Nepal-Homes-master/model/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    # add the one-hot encoded columns to __data_columns
    with open('/home/subash/Desktop/Nepal-Homes-master/model/nepal_home_prices_model_new.pickle', 'rb') as f:
        __model = pickle.load(f)

    print("loading saved artifacts...done")


if __name__ == "__main__":
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('Balkumari', 3, 3,1000))
