import fetchers
import json
from utils import formatCurrency,formatPercent
import requests #dependency
from utils import sendWebhook,makeFields

price =0
while True:
    price = fetchers.getUnderlyingPrice('0x1637e4e9941D55703a7A5E7807d6aDA3f7DCD61B')
    print(price)