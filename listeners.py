import time
import logging
import random
from threading import Thread
from pycoingecko import CoinGeckoAPI
from datetime import datetime
import json
import sys
import requests
from dotenv import load_dotenv
from web3 import Web3
from handlers import HandleTx, HandleEvent, HandleStateVariation, HandleCoingecko,HandleCoingeckoVolume
from helpers import sendError, formatPercent, patch_http_connection_pool

# Define a Thread to listen separately on each contract/event in the contract file
class TxListener(Thread):
    def __init__(self, web3, alert, contract,name, **kwargs):
        super(TxListener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.name = name
        self.tx_filter = []
        self.block0 = self.web3.eth.get_block_number()
        self.block1 = self.block0
    def run(self):
        while True:
            try:
                self.block1 = self.block0
                self.tx_filter = self.web3.eth.filter({"fromBlock": self.block0, "address": self.contract})
                block0 = self.web3.eth.get_block_number()
                for tx in self.tx_filter.get_all_entries():
                    logging.info(f'Tx found in {str(self.alert)}-{str(self.name)}')
                    logging.info(json.dumps(tx))
                    HandleTx(self.web3,tx, self.alert, self.contract,self.name).start()
                time.sleep(random.uniform(30,60))

            except Exception as e:
                logging.warning(f'Error in tx listener {str(self.alert)}-{str(self.contract)}')
                logging.error(e)
                self.block0 = self.block1
                sendError(f'Error in tx listener {str(self.alert)}-{str(self.contract)}')
                sendError(e)
                time.sleep(random.uniform(5,11))
                continue


# Define a Thread to listen separately on each contract/event in the contract file
class EventListener(Thread):
    def __init__(self, web3, alert, contract, event_name, **kwargs):
        super(EventListener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.event_name = event_name
        self.event_filter = []
        self.block0 = self.web3.eth.get_block_number()
        self.block1 = self.block0

    def run(self):
        while True:
            try:
                self.block1 = self.block0
                self.event_filter = eval(f'self.contract.events.{self.event_name}.createFilter(fromBlock={self.block0})')
                self.block0 = self.web3.eth.get_block_number()
                #logging.warning(self.event_filter)
                for event in self.event_filter.get_all_entries():
                    logging.info(f'Event found in {str(self.alert)}-{str(self.contract.address)}-{str(self.event_name)}')
                    HandleEvent(self.web3, event, self.alert, self.event_name).start()
                time.sleep(random.uniform(30,60))
            except Exception as e:
                logging.warning(f'Error in Event Listener {str(self.alert)}-{str(self.contract.address)}-{str(self.event_name)}')
                logging.error(e)
                sendError(f'Error in Event Listener {str(self.alert)}-{str(self.contract.address)}-{str(self.event_name)}')
                sendError(e)
                self.block0 = self.block1
                time.sleep(random.uniform(5,11))
                continue


# Define a Thread to listen separately on each state change
class StateChangeListener(Thread):
    def __init__(self, web3, alert, contract, state_function, argument, **kwargs):
        super(StateChangeListener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.state_function = state_function
        self.argument = argument
        patch_http_connection_pool(maxsize=1000)
        # If condition to take into account state function with no input params
        if self.argument is None:
            self.value = eval(f'''self.contract.functions.{self.state_function}().call()''')
        elif self.argument is not None:
            self.value = eval(f'''self.contract.functions.{self.state_function}('{self.argument}').call()''')

    def run(self):
        self.old_value = self.value
        while True:
            try:
                if self.old_value > 0:
                    # If condition to take into account state function with no input params
                    if self.argument is None:
                        self.value = eval(f'''self.contract.functions.{self.state_function}().call()''')
                    elif self.argument is not None:
                        self.value = eval(f'''self.contract.functions.{self.state_function}('{self.argument}').call()''')

                    self.change = (self.value / self.old_value) - 1

                    if abs(self.change) > 0 and self.value > 0:
                        logging.info(f'State Change matching criteria found in {str(self.alert)}-{str(self.contract.address)}-{str(self.state_function)}')
                        logging.info(formatPercent(self.change))
                        HandleStateVariation(self.web3,self.old_value,self.value, self.change, self.alert, self.contract, self.state_function, self.argument).start()
                    self.old_value = self.value
                time.sleep(random.uniform(30,60))
            except Exception as e:
                logging.error(f'Error in State Change Listener : {self.alert}-{self.contract.address}-{self.state_function}-{self.argument}')
                logging.error(str(e))
                sendError(f'Error in State Change Listener : {self.alert}-{self.contract.address}-{self.state_function}-{self.argument}')
                sendError(e)
                time.sleep(random.uniform(5,11))
                continue

# Define a Thread to listen separately to price/volume variation
class CoinGeckoListener(Thread):
    def __init__(self, id, **kwargs):
        super(CoinGeckoListener, self).__init__(**kwargs)
        self.id = id
        self.cg = CoinGeckoAPI()

    def run(self):
        self.old_value = self.cg.get_price(ids=self.id, vs_currencies='usd')[self.id]['usd']
        while True:
            try:
                self.price = self.cg.get_price(ids=self.id, vs_currencies='usd')[self.id]['usd']
                self.change = (self.price / self.old_value) - 1
                logging.info('change : ' + str(formatPercent(self.change))+ ' / price : ' + str(self.price) + ' / old price : ' + str(self.old_value))
                HandleCoingecko(self.id, self.old_value, self.price, self.change).start()
                self.old_value = self.price
                time.sleep(60)

            except Exception as e:
                logging.error(f'Error in CoinGecko Price Listener : {self.id}')
                logging.error(str(e))
                sendError(f'Error in CoinGecko Price Listener : {self.id}')
                sendError(e)
                time.sleep(random.uniform(5,11))
                continue

# Define a Thread to listen separately to price variation
class CoinGeckoVolumeListener(Thread):
    def __init__(self, id, **kwargs):
        super(CoinGeckoVolumeListener, self).__init__(**kwargs)
        self.id = id
        self.cg = CoinGeckoAPI()
    def run(self):
        self.tickers = self.cg.get_coin_by_id(id=self.id, vs_currency='usd', days=1)['tickers']
        self.old_value = 0
        for i in range(0, len(self.tickers)):
            self.old_value += self.tickers[i]['converted_volume']['usd']
        while True:

            try:
                self.tickers = self.cg.get_coin_by_id(id=self.id, vs_currency='usd', days=1)['tickers']
                self.volume = 0
                for i in range(0, len(self.tickers)):
                    self.volume += self.tickers[i]['converted_volume']['usd']

                self.change = (self.volume / self.old_value) - 1
                logging.info('change : ' + str(formatPercent(self.change))+ ' / volume : ' + str(self.volume) + ' / old volume : ' + str(self.old_value))
                HandleCoingeckoVolume(self.id, self.old_value, self.volume, self.change).start()
                self.old_value = self.volume
                time.sleep(60)

            except Exception as e:
                logging.error(f'Error in CoinGecko Volume Listener : {self.id}')
                logging.error(str(e))
                sendError(f'Error in CoinGecko Volume Listener : {self.id}')
                sendError(e)
                time.sleep(random.uniform(5,11))
                continue
            



