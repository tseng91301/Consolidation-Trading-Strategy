## API Function Call
### API setup
Configure the environment of API (eg: API Key, API Secret)
Files of environment settings that have to store at /.env/
```
Project Directory/
└── .env/
    ├── api_key.json
    └── [Some other files]
```
In the main code of project, import the specified library of api
```
Project Directory/
├── .env/
├── api/
└── main.py
```
`main.py` (eg: bingX):
```python
from api import bingx as api_entry
```
#### BingX
`api_key.json`:
```json
{
    "api_key": "[Your API Key]",
    "secret_key": "[Your Secret Key]",
    "simulation": true /* Setting of vst-trade */
}
```

### API entry
#### See all Trading Symbols
```python
get_trade_symbols()
```
input: None
output: All trading symbols in `Array` type(eg: `['BTC-USDT', 'ETH-USDT', ...]`)
#### Get Current Price of a Symbol
```python
get_current_price(str)
```
input: The symbol string you want to look.(eg: `"BTC-USDT"`)
output: The price of input symbol (float).(eg: `79040.2`)
#### Get K-Lines of a Symbol
```python
get_kLine_data(str, str, int)
```
input:
1. The trading symbol you want to look.
2. The time interval.
3. The number of k-lines.
eg: `get_kLine_data("BTC-USDT", "15m", 10)`

output: The K-Line data as `Array` type.
eg: `[{'open': '94233.2', 'close': '94168.5', 'high': '94259.8', 'low': '94164.6', 'volume': '15.12', 'time': 1745727300000}, {'open': '94119.3', 'close': '94233.0', 'high': '94241.5', 'low': '94082.4', 'volume': '26.77', 'time': 1745726400000}, ...]`

## Reference
### Indicator Coding Demonstration
Go to [indicator_demonstration.ipynb](indicator_demonstration.ipynb) for further information.