import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

def _long_or_short(data: pd.Series):
    if data["open"] > data["close"]:
        return 0
    elif data["open"] < data["close"]:
        return 1
    pass

def calculate(data: pd.DataFrame) -> list:
    current_trend = _long_or_short(data.iloc[0])
    ret_data = [] # [type(1:bos long, 2: bos short, 3: mss to long, 4: mss to short), start_x, start_y, end_x]
    the_most_high = data.iloc[0]["high"]
    the_most_low = data.iloc[0]["low"]
    the_most_high_i = 0
    the_most_low_i = 0
    l = len(data)
    has_callback = False
    for i in range(l):
        trend_t = _long_or_short(data.iloc[i])
        if current_trend == 1:
            if trend_t != current_trend:
                if data.iloc[i]["close"] < the_most_low: # MSS
                    ret_data.append([4, the_most_low_i, the_most_low, i])
                    current_trend = 0
                    has_callback = False
                elif has_callback == False:
                    has_callback = True
            else:
                if has_callback and data.iloc[i]["close"] > the_most_high: # BOS Long
                    ret_data.append([1, the_most_high_i, the_most_high, i])
                    has_callback = False
                    the_most_low = data.iloc[i]["low"]
                    the_most_low_i = i
            if data.iloc[i]["high"] > the_most_high:
                the_most_high = data.iloc[i]["high"]
                the_most_high_i = i
            if data.iloc[i]["low"] < the_most_low:
                the_most_low = data.iloc[i]["low"]
                the_most_low_i = i
        else:
            if trend_t != current_trend:
                if data.iloc[i]["close"] > the_most_high: # MSS
                    ret_data.append([3, the_most_high_i, the_most_high, i])
                    current_trend = 1
                    has_callback = False
                elif has_callback == False:
                    has_callback = True
            else:
                if has_callback and data.iloc[i]["close"] < the_most_low: # BOS Short
                    ret_data.append([2, the_most_low_i, the_most_low, i])
                    has_callback = False
                    the_most_high = data.iloc[i]["high"]
                    the_most_high_i = i
            if data.iloc[i]["high"] > the_most_high:
                the_most_high = data.iloc[i]["high"]
                the_most_high_i = i
            if data.iloc[i]["low"] < the_most_low:
                the_most_low = data.iloc[i]["low"]
                the_most_low_i = i
    return ret_data