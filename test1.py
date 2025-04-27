from api import bingx as api_entry
# print(api_entry.get_trade_symbols())
# print(api_entry.get_current_price("BTC-USDT"))
print(len(api_entry.get_kLine_data("BTC-USDT", "15m", 10)))