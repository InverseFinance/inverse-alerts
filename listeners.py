import time
import logging
from helpers import sendError
from threading import Thread
from datetime import datetime
from priority_thread_pool_executor import PriorityThreadPoolExecutor
from handlers import HandleTx,HandleEvent,HandleStateVariation
import sys
from dotenv import load_dotenv
from web3 import Web3

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
                    logging.info(str(datetime.now()) + " Tx found in " + str(self.alert) + "-" + str(self.contract))
                    with PriorityThreadPoolExecutor() as executor:
                        executor.submit(HandleTx, (tx, self.alert, self.contract),priority=0)
                time.sleep(1)

            except Exception as e:
                logging.warning("Error in Tx Listener " + str(self.alert) + "-" + str(self.contract))
                logging.error(e)
                sendError("Error in Tx Listener " + str(e))
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
                    logging.info(str(datetime.now()) + " Event found in " + str(self.alert) + "-" + str(
                        self.contract.address) + "-" + str(self.event_name))
                    with PriorityThreadPoolExecutor() as executor:
                        executor.submit(HandleEvent, (event, self.alert, self.event_name),priority=0)
                time.sleep(1)

            except Exception as e:
                logging.warning(
                    "Error in Event Listener " + str(self.alert) + "-" + str(self.contract.address) + "-" + str(
                        self.event_name))
                logging.error(e)
                sendError("Error in Event Listener " + str(e))
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
        else:
            self.value = eval(f'''self.contract.functions.{self.state_function}('{self.argument}').call()''')

    def run(self):
        self.old_value = self.value
        while True:
            try:
                if self.old_value != 0:
                    # If condition to take into account state function with no input params
                    if self.argument is None:
                        self.value = eval(f'''self.contract.functions.{self.state_function}().call()''')
                    else:
                        self.value = eval(
                            f'''self.contract.functions.{self.state_function}('{self.argument}').call()''')

                    self.change = (self.value / self.old_value) - 1
                    self.old_value = self.value

                    if self.change > 0.05 and self.value > 0:
                        with PriorityThreadPoolExecutor() as executor:
                            executor.submit(HandleStateVariation, (self.value, self.change, self.alert, self.contract, self.state_function,
                                             self.argument),priority=0)
                    time.sleep(1)

            except Exception as e:
                # logging.warning("Error in State Change Listener " + str(self.alert) + "-" + str(self.contract.address) + "-" + str(
                #    self.event))
                logging.error(e)
                sendError("Error in State Change Listener :" + str(e))
                pass


