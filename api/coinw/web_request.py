import requests
import hashlib
import json

class CoinWAPI:
    BASE_URL = "https://api.coinw.sh/appApi.html"

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def generate_sign(self, params):
        # 生成簽名
        params['api_key'] = self.api_key
        sorted_params = sorted(params.items())
        sign_str = '&'.join(f"{key}={value}" for key, value in sorted_params)
        sign_str += f"&secret_key={self.secret_key}"
        return hashlib.md5(sign_str.encode()).hexdigest().upper()

    def register(self, username, password):
        # 使用者註冊
        params = {
            "action": "register",
            "username": username,
            "password": password
        }
        params['sign'] = self.generate_sign(params)
        response = requests.post(self.BASE_URL, data=params)
        return response.json()

    def login(self, username, password):
        # 登入功能
        params = {
            "action": "login",
            "username": username,
            "password": password
        }
        params['sign'] = self.generate_sign(params)
        response = requests.post(self.BASE_URL, data=params)
        return response.json()

    def get_market_info(self):
        # 查詢市場行情
        params = {
            "action": "currencys"
        }
        params['sign'] = self.generate_sign(params)
        response = requests.post(self.BASE_URL, data=params)
        return response.json()

    def place_order(self, symbol, order_type, amount, price):
        # 下單
        params = {
            "action": "trade",
            "symbol": symbol,
            "type": order_type,
            "amount": amount,
            "price": price
        }
        params['sign'] = self.generate_sign(params)
        response = requests.post(self.BASE_URL, data=params)
        return response.json()

    def cancel_order(self, order_id):
        # 撤單
        params = {
            "action": "cancel_entrust",
            "id": order_id
        }
        params['sign'] = self.generate_sign(params)
        response = requests.post(self.BASE_URL, data=params)
        return response.json()

    def get_trade_history(self, symbol):
        # 查詢交易歷史
        params = {
            "action": "entrust",
            "symbol": symbol
        }
        params['sign'] = self.generate_sign(params)
        response = requests.post(self.BASE_URL, data=params)
        return response.json()
