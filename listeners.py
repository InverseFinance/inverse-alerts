import time,logging,random,json,sys,requests
from threading import Thread
from pycoingecko import CoinGeckoAPI
from web3._utils.events import construct_event_topic_set
from handlers import *
from helpers import *


# Define a Thread to listen separately on each contract/event in the contract file
class EventListener(Thread):
    def __init__(self, web3, alert, contract, event_name,filters, frequency, **kwargs):
        super(EventListener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.event_name = event_name
        self.filters = filters
        self.frequency = frequency
        self.subtopics = list()
        self.topics = list()
        self.logs = list()
        self.events = tuple()
        self.block0 = self.web3.eth.get_block_number()
        self.block1 = self.block0

        logging.info('Starting Event Listener '+str(alert)+'-'+str(contract.address)+'-'+str(event_name)+' with filters '+str(filters))

    def run(self):
        while True:
            try:
                self.topics = []

                #create a topic for every filter in alerts.py and bundle them in self.topics
                for filter in self.filters:
                    self.block1 = self.block0
                    self.sub_topic = eval(f'construct_event_topic_set(self.contract.events.{self.event_name}().abi, self.web3.codec, {str(filter)})')
                    self.topics.append(self.sub_topic)

                # Fetch logs for every subtopic and bundle logs together
                for subtopic in self.topics:
                    new_logs = self.web3.eth.get_logs({"address": self.contract.address, "topics": subtopic, "fromBlock": self.block0})
                    if new_logs != []:
                        for item in new_logs:
                            self.logs.append(item)

                self.block0 = self.web3.eth.get_block_number()

                # Fetch for event in the filtered logs
                if self.logs != []:
                    self.events = eval(f'self.contract.events.{self.event_name}().processReceipt({{"logs": self.logs}})')
                    for event in self.events:
                        logging.info(f'Event found in {self.alert}-{self.contract.address}-{self.event_name}')
                        logging.info(event)
                        HandleEvent(self.web3, event, self.alert,self.contract, self.event_name).start()

                self.logs = list()
                time.sleep(self.frequency)

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
    def __init__(self, web3, alert, contract, state_function, argument, frequency, **kwargs):
        super(StateChangeListener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.state_function = state_function
        self.argument = argument
        self.frequency = frequency
        # If condition to take into account state function with no input params

        logging.info('Starting State Listener '+str(alert)+'-'+str(contract.address)+'-'+str(state_function)+' with filters '+str(argument))

        if self.argument is None:
            #print(f'''self.contract.functions.{self.state_function}().call()''')
            self.value = eval(f'''self.contract.functions.{self.state_function}().call()''')
        elif self.argument is not None:
            #print(f'''self.contract.functions.{self.state_function}('{self.argument}').call()''')
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
                        HandleStateVariation(self.web3,
                                             self.old_value,
                                             self.value,
                                             self.change,
                                             self.alert,
                                             self.contract,
                                             self.state_function,
                                             self.argument).start()
                    self.old_value = self.value
                time.sleep(self.frequency)

            except Exception as e:
                logging.error(f'Error in State Change Listener : {self.alert}-{self.contract.address}-{self.state_function}-{self.argument}')
                logging.error(str(e))
                sendError(f'Error in State Change Listener : {self.alert}-{self.contract.address}-{self.state_function}-{self.argument}')
                sendError(e)
                time.sleep(random.uniform(5,11))
                continue


# Define a Thread to listen separately on each state change
class StateChangeListener2(Thread):
    def __init__(self, web3, alert, contract, state_function, argument, frequency, **kwargs):
        super(StateChangeListener2, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.state_function = state_function
        self.argument = argument
        self.frequency = frequency
        # If condition to take into account state function with no input params

        logging.info('Starting State Listener '+str(alert)+'-'+str(contract.address)+'-'+str(state_function)+' with filters '+str(argument))
        function = eval(f'self.contract.functions.{self.state_function}')
        print(f'function({self.argument}).call()')
        self.value = function(self.argument).call()

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
                        HandleStateVariation(self.web3,
                                             self.old_value,
                                             self.value,
                                             self.change,
                                             self.alert,
                                             self.contract,
                                             self.state_function,
                                             self.argument).start()
                    self.old_value = self.value
                time.sleep(self.frequency)

            except Exception as e:
                logging.error(f'Error in State Change Listener : {self.alert}-{self.contract.address}-{self.state_function}-{self.argument}')
                logging.error(str(e))
                sendError(f'Error in State Change Listener : {self.alert}-{self.contract.address}-{self.state_function}-{self.argument}')
                sendError(e)
                time.sleep(random.uniform(5,11))
                continue

# Define a Thread to listen separately on each contract/event in the contract file
class TxListener(Thread):
    def __init__(self, web3, alert, contract, name, frequency, **kwargs):
        super(TxListener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.name = name
        self.tx_filter = []
        self.frequency = frequency
        self.block0 = self.web3.eth.get_block_number()
        self.block1 = self.block0

        logging.info('Starting State Listener '+str(alert)+'-'+str(contract.address)+'-'+str(name))
    def run(self):
        while True:
            try:
                self.block1 = self.block0
                self.tx_filter = self.web3.eth.filter({"fromBlock": self.block0, "address": self.contract})
                self.block0 = self.web3.eth.get_block_number()
                for tx in self.tx_filter.get_all_entries():
                    logging.info(f'Tx found in {str(self.alert)}-{str(self.name)}')
                    HandleTx(self.web3,tx, self.alert, self.contract,self.name).start()
                time.sleep(self.frequency)

            except Exception as e:
                logging.warning(f'Error in tx listener {str(self.alert)}-{str(self.contract)}-{str(self.name)}')
                logging.error(e)
                self.block0 = self.block1
                sendError(f'Error in tx listener {str(self.alert)}-{str(self.contract)}-{str(self.name)}')
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

                logging.info('change : ' + str(formatPercent(self.change))+
                             ' / volume : ' + str(self.volume) +
                             ' / old volume : ' + str(self.old_value))

                HandleCoingeckoVolume(self.id,
                                      self.old_value,
                                      self.volume,
                                      self.change).start()

                self.old_value = self.volume
                time.sleep(60)

            except Exception as e:
                logging.error(f'Error in CoinGecko Volume Listener : {self.id}')
                logging.error(str(e))
                sendError(f'Error in CoinGecko Volume Listener : {self.id}')
                sendError(e)
                time.sleep(random.uniform(5,11))
                continue