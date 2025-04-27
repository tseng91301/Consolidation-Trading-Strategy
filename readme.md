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