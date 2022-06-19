import time
import logging
from threading import Thread
from pycoingecko import CoinGeckoAPI
from datetime import datetime
import json
import sys
import requests
from dotenv import load_dotenv
from web3 import Web3
from handlers import HandleTx, HandleEvent, HandleStateVariation, HandleCoingecko
from helpers import sendError, formatPercent
cg = CoinGeckoAPI()
tickers = cg.get_coin_by_id(id='inverse-finance', vs_currency='usd', days=1)['tickers']
volume_usd=0
for i in range(0,len(tickers)):
    volume_usd += tickers[i]['converted_volume']['usd']

print(volume_usd)