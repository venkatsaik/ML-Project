import pickle
from flask import Flask, request, jsonify
import json
import numpy as np

__locations = None
__data_columns = None
__model = None
__months = None

def get_estimated_price(location,t_month,bhk,t_month2,t_month3,month):
    try:
        loc_index_1 = __data_columns.index(location.lower())
        loc_index_2 = __data_columns.index(month.lower())
    except:
        loc_index_1 = -1
        loc_index_2 = -1

    x = np.zeros(len(__data_columns))
    x[0] = t_month
    x[1] = bhk
    x[2]=t_month2
    x[3]=t_month3
    if loc_index_1 >= 0:
        x[loc_index_1] = 1
    if loc_index_2 >= 0:
        x[loc_index_2] = 1
    # print(x)

    return round(__model.predict([x])[0],2)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations
    global __months

    with open("server/artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __months = __data_columns[4:15]
        __locations = __data_columns[15:]

    global __model
    if __model is None:
        with open('server/artifacts/ct_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

def get_location_names():
    return __locations

def get_month_names():
    return __months

def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_data_columns())
    print(get_location_names())
    print(get_month_names())
    print(get_estimated_price('East Haven',236,4,236**2,236**3,'Aug'))
    print(get_estimated_price('East Haven',237,4,237**2,237**3,'Aug'))
    print(get_estimated_price('Branford', 253,3,253**2,253**3,'Jan')) # other location
    print(get_estimated_price('Branford',252,3,252**2,252**3,'Dec'))  # other location