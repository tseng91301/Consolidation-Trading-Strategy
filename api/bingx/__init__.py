import os
import json

from . import web_request

api_inf = {}

def read_secret_key():
    # Assuming the script is run from the project root directory
    # The path to the file relative to the root is '.env/secret_key'
    secret_file_path = os.path.join('.env', 'api_key.json')

    try:
        with open(secret_file_path, 'r') as f:
            secret_key = f.read().strip() # .strip() removes leading/trailing whitespace/newlines
            api_inf = json.loads(secret_key)
            try:
                api_inf['api_key'] = api_inf['api_key']
                api_inf['secret_key'] = api_inf['secret_key']
            except KeyError as e:
                print(f"KeyError: {e} not found - Please check the structure of your JSON file.")
                exit(1)
            print(f"Successfully read secret key from {secret_file_path}")
            try:
                simulation_key = api_inf['simulation']
                simulation(simulation_key)
            except:
                simulation(False)
            return api_inf
    except FileNotFoundError:
        print(f"Error: The file {secret_file_path} was not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        exit(1)
    
def simulation(on = False):
    if on:
        print("Simulation mode is ON")
        web_request.APIURL = "https://open-api-vst.bingx.com"
    else:
        print("Simulation mode is OFF")
        web_request.APIURL = "https://open-api.bingx.com"
        pass
    return


# Read the secret key from the file and set the API URL
api_inf = read_secret_key()
web_request.APIKEY = api_inf['api_key']
web_request.SECRETKEY = api_inf['secret_key']

def get_trade_symbols():
    """
    Get the trade symbols from the API.
    Return: Trading symbols in List format.
    """
    path = '/openApi/swap/v2/quote/contracts'
    method = "GET"
    paramsMap = {}
    paramsStr = web_request.parseParam(paramsMap)
    response: dict = web_request._send_request(method, path, paramsStr, {})
    if response.get('code') == 0:
        symbols_detail = response.get('data')
        symbols = []
        for v in symbols_detail:
            if v['apiStateOpen']:
                symbols.append(v['symbol'])
                pass
            pass
        return symbols
    else:
        print(f"Error: {response.get('msg')}")
        return []

def get_current_price(symbol: str):
    """
    Get the current price of a trading symbol.
    :param symbol: Trading symbol.
    :return: Current price (mark price) as float type.
    """
    path = '/openApi/swap/v2/quote/premiumIndex'
    method = "GET"
    paramsMap = {'symbol': symbol}
    paramsStr = web_request.parseParam(paramsMap)
    response: dict = web_request._send_request(method, path, paramsStr, {})
    if response.get('code') == 0:
        return float(response.get('data').get('markPrice'))
    else:
        print(f"Error: {response.get('msg')}")
        return None
    
def get_kLine_data(symbol: str, interval: str, limit: int = 100):
    """
    Get K-line data for a trading symbol.
    :param symbol: Trading symbol.
    :param interval: Time interval (e.g., '1m', '5m', '15m', '30m', '1h', '4h', '1d').
    :param limit: Number of data points to retrieve (default is 100).
    :return: K-line data as a list of dictionaries (sorted by time, descend order).
    {"open": float, "high": float, "low": float, "close": float, "volume": float, "time": int64}
    """
    path = '/openApi/swap/v3/quote/klines'
    method = "GET"
    paramsMap = {'symbol': symbol, 'interval': interval, 'limit': limit}
    paramsStr = web_request.parseParam(paramsMap)
    response: dict = web_request._send_request(method, path, paramsStr, {})
    if response.get('code') == 0:
        return response.get('data')
    else:
        print(f"Error: {response.get('msg')}")
        return None