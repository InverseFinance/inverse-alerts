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
from handlers import HandleTx,HandleEvent,HandleStateVariation,HandleCoingecko
from helpers import sendError,formatPercent

# Define a Thread to listen separately on each contract/event in the contract file
class TxListener(Thread):
    def __init__(self, web3, alert, contract, **kwargs):
        super(TxListener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.tx_filter = []

    def run(self):
        self.tx_filter = eval(f'''self.web3.eth.filter({{"address":'{self.contract}'}})''')
        while True:
            try:
                for tx in self.tx_filter.get_new_entries():
                    logging.info(f'Tx found in {str(self.alert)}-{str(self.contract)}')
                    logging.info(str(tx))
                    HandleTx(tx, self.alert, self.contract).start()
                time.sleep(2)

            except Exception as e:
                logging.warning(f'Error in listener {str(self.alert)}-{str(self.contract)}')
                #sendError(f'Error in Tx Listener : {str(e)}')
                logging.error(e)
                pass

# Define a Thread to listen separately on each contract/event in the contract file
class EventListener(Thread):
    def __init__(self, web3, alert, contract, event_name, **kwargs):
        super(EventListener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.event_name = event_name
        self.event_filter = []

    def run(self):
        self.event_filter = eval(f'self.contract.events.{self.event_name}.createFilter(fromBlock="latest")')
        while True:
            try:
                for event in self.event_filter.get_new_entries():
                    logging.info(f'Event found in {str(self.alert)}-{str(self.contract.address)}-{str(self.event_name)}')
                    HandleEvent(event, self.alert, self.event_name).start()
                time.sleep(2)

            except Exception as e:
                logging.warning(f'Error in Event Listener {str(self.alert)}-{str(self.contract.address)}-{str(self.event_name)}')
                logging.error(e)
                #sendError(f'Error in Event Listener : {str(e)}')
                pass

# Define a Thread to listen separately on each state change
class StateChangeListener(Thread):
    def __init__(self, web3, alert, contract, state_function, argument, **kwargs):
        super(StateChangeListener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.state_function = state_function
        self.argument = argument
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

                    if abs(self.change) > 0.05 and self.value > 0:
                        logging.info(f'State Change matching criteria found in {str(self.alert)}-{str(self.contract.address)}-{str(self.state_function)}')
                        logging.info(formatPercent(self.change))
                        HandleStateVariation(self.old_value,self.value, self.change, self.alert, self.contract, self.state_function, self.argument).start()
                    self.old_value = self.value
                time.sleep(60)

            except Exception as e:
                logging.error(f'Error in State Change Listener : {self.alert}-{self.contract.address}-{self.state_function}-{self.argument}')
                logging.error(str(e))
                #sendError(f'Error in State Change Listener : {str(e)}')
                pass

# Define a Thread to listen separately on each state change
class CoinGeckoListener(Thread):
    def __init__(self, id, **kwargs):
        super(CoinGeckoListener, self).__init__(**kwargs)
        self.id = id
        self.cg = CoinGeckoAPI()

    def run(self):
        try:
            self.old_value = self.cg.get_price(ids=self.id, vs_currencies='usd')[self.id]['usd']
            while True:
                self.price = self.cg.get_price(ids=self.id, vs_currencies='usd')[self.id]['usd']
                self.change = (self.old_value / self.price) - 1
                logging.info('change : ' + str(formatPercent(self.change))+ ' / price : ' + str(self.price) + ' / old price : ' + str(self.old_value))
                HandleCoingecko(self.id, self.old_value, self.price, self.change).start()
                old_value = price
                time.sleep(60)

        except Exception as e:
            logging.error(f'Error in CoinGecko Listener : {self.id}')
            logging.error(str(e))
            #sendError(f'Error in State Change Listener : {str(e)}')
            pass



