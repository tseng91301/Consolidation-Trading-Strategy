import numpy as np
from scipy.signal import argrelextrema
import pandas as pd
def same_high_low(close: pd.Series, rsi_data: pd.Series) -> np.ndarray:
    order = 3  # 周圍看 3 根K棒作比較
    # 找出局部極大值與極小值的索引
    local_max_idx = argrelextrema(close.values, np.greater, order=order)[0]
    local_min_idx = argrelextrema(close.values, np.less, order=order)[0]
    local_max_idx_rsi = argrelextrema(rsi_data.values, np.greater, order=order)[0]
    local_min_idx_rsi = argrelextrema(rsi_data.values, np.less, order=order)[0]
    same_high = []
    min_i = 0
    l = len(local_max_idx_rsi)
    for i, v in enumerate(local_max_idx):
        for i2 in range(min_i, l):
            if abs(v - local_max_idx_rsi[i2]) <= 1: # K high index is equal to RSI high index
                same_high.append(v)
                min_i = i2
                break
            elif local_max_idx_rsi[i2] > v:
                min_i = i2
                break
    same_low = []
    min_i = 0
    l = len(local_min_idx_rsi)
    for i, v in enumerate(local_min_idx):
        for i2 in range(min_i, l):
            if abs(v - local_min_idx_rsi[i2]) <= 1: # K high index is equal to RSI high index
                same_low.append(v)
                min_i = i2
                break
            elif local_min_idx_rsi[i2] > v:
                min_i = i2
                break
    return np.array(same_high), np.array(same_low)

def find_rsi_divergences(price, rsi, high_points, low_points):
    divergences = []

    # 判斷看跌背離（高點）
    for i in range(len(high_points) - 1):
        idx1, idx2 = high_points[i], high_points[i+1]
        p1, p2 = price[idx1], price[idx2]
        r1, r2 = rsi[idx1], rsi[idx2]

        if p2 > p1 and r2 < r1:
            # divergences.append({
            #     'type': 'bearish',
            #     'start': idx1,
            #     'end': idx2,
            #     'price1': p1,
            #     'price2': p2,
            #     'rsi1': r1,
            #     'rsi2': r2
            # })
            divergences.append([
                0,
                idx1,
                r1,
                idx2,
                r2
            ])

    # 判斷看漲背離（低點）
    for i in range(len(low_points) - 1):
        idx1, idx2 = low_points[i], low_points[i+1]
        p1, p2 = price[idx1], price[idx2]
        r1, r2 = rsi[idx1], rsi[idx2]

        if p2 < p1 and r2 > r1:
            # divergences.append({
            #     'type': 'bullish',
            #     'start': idx1,
            #     'end': idx2,
            #     'price1': p1,
            #     'price2': p2,
            #     'rsi1': r1,
            #     'rsi2': r2
            # })
            divergences.append([
                1,
                idx1,
                r1,
                idx2,
                r2
            ])

    return divergences
