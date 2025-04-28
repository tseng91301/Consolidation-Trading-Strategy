# Importing required libraries
import talib as ta

from . import plotting

import pandas as pd
from datetime import datetime

class Indicators:
    def __init__(self, symbol:str, time_frame_in_ms:int, rsi_kLines_count:int = 14, ema_s_count:int = 20, ema_m_count:int = 40, ema_l_count:int = 60):
        self.symbol = symbol
        self.rsi_kLines_count = rsi_kLines_count
        self.ema_s_count = ema_s_count
        self.ema_m_count = ema_m_count
        self.ema_l_count = ema_l_count
        self.time_frame_in_ms = time_frame_in_ms

        self.kLines_pd: pd.DataFrame = pd.DataFrame({"open":[], "high":[], "low":[], "close":[], "volume":[], "time":[], "timeStamp":[], "RSI": [], "EMA_S": [], "EMA_M": [], "EMA_L": []})
        self.kLines_num = 0
        self.kLines_min_timeStamp = -1
        self.kLines_max_timeStamp = -1
        pass

    def reset_values(self):
        self.kLines_pd = pd.DataFrame({"open":[], "high":[], "low":[], "close":[], "volume":[], "time":[], "timeStamp":[], "RSI": [], "EMA_S": [], "EMA_M": [], "EMA_L": []})
        self.kLines_num = 0
        pass

    def _kLine_convert(self, kLines: list):
        # Convert sorted k-line list into pd.dataframe
        # 將字串欄位轉成 float
        kLines_df = pd.DataFrame(kLines)
        for col in ['open', 'close', 'high', 'low', 'volume']:
            kLines_df[col] = kLines_df[col].astype(float)
        # timeStamp, time converting
        kLines_df["timeStamp"] = kLines_df["time"]
        kLines_df["time"] = pd.to_datetime(kLines_df["time"], unit='ms')
        return kLines_df

    def import_kLines(self, data:list, reverse = True):
        # Function to FIRST import multiple k-lines into EMPTY dataframe
        # If dataset is not NULL, reset it.
        if(self.kLines_num != 0):
            self.reset_values()
            pass
        # In this step, sort the kLine data in time ascend.
        if(reverse):
            data = data[::-1]  # 複製並反轉 list
            pass
        self.kLines_min_timeStamp = int(data[0]["time"])
        self.kLines_max_timeStamp = int(data[-1]["time"])
        self.kLines_pd = self._kLine_convert(data)
        self.kLines_num = len(data)
        self.calculate_ema()
        self.calculate_rsi()
        pass
    
    def append_kLines(self, data:list, reverse = True):
        # Function to append k-lines to the end of original dataframe
        # In this step, sort the kLine data in time ascend.
        if(reverse):
            data = data[::-1]  # 複製並反轉 list
            pass
        append_min_time = int(data[0]["time"])
        append_max_time = int(data[-1]["time"])
        if append_min_time - self.kLines_max_timeStamp > self.time_frame_in_ms:
            print("There is some gap between min time in append data and max time in original data")
            print("Min time in append data: ", datetime.fromtimestamp(append_min_time / 1000))
            print("Max time in original data: ", datetime.fromtimestamp(self.kLines_max_timeStamp / 1000))
            return
        append_min_index = 0
        for i in range(len(data)):
            if int(data[i]["time"]) <= self.kLines_max_timeStamp:
                append_min_index += 1
        if(append_min_index >= len(data)):
            print("All append data has been stored into original data")
            return
        data = data[append_min_index:]
        self.kLines_max_timeStamp = append_max_time
        self.kLines_pd = pd.concat([self.kLines_pd, self._kLine_convert(data)], ignore_index=True)
        self.calculate_ema()
        self.calculate_rsi()
        pass

    def calculate_rsi(self):
        # Calculate RSI
        self.kLines_pd["RSI"] = ta.RSI(self.kLines_pd["close"], timeperiod=self.rsi_kLines_count)
    
    def calculate_ema(self):
        # Calculate the EMA Values
        # 計算 EMA
        self.kLines_pd['EMA20'] = self.kLines_pd['close'].ewm(span=self.ema_s_count, adjust=False).mean()
        self.kLines_pd['EMA40'] = self.kLines_pd['close'].ewm(span=self.ema_m_count, adjust=False).mean()
        self.kLines_pd['EMA60'] = self.kLines_pd['close'].ewm(span=self.ema_l_count, adjust=False).mean()

    def plot(self, included_i: list):
        if "kl" in included_i:
            plotting.draw_kLine(self.kLines_pd)
        if "all" in included_i:
            plotting.draw_all(self.kLines_pd)
        return
