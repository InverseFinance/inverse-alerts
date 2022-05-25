# import the following dependencies
import json
import os
import pandas as pd
import fetchers
from threading import Thread
from utils import EventListener,StateChangeListener,LoggerParams
from dotenv import load_dotenv
from web3 import Web3
from datetime import datetime
import logging
import sys

# Load Web3 instance and import logger parameters for error display
load_dotenv()
LoggerParams()
web3 = Web3(Web3.HTTPProvider(os.getenv('LOCALHOST'))) # Or infura key
# Get contracts metadata from excel
contracts = pd.read_excel('contracts.xlsx', sheet_name='contracts')

# Get alerts, events, to read from
sheet_events = pd.read_excel('contracts.xlsx', sheet_name='alerts_events')
events_alerts = sheet_events.columns.array
# Get alerts, state function, to read from
sheet_state = pd.read_excel('contracts.xlsx', sheet_name='alerts_state')
state_alerts = sheet_state.columns.array

n_alert = 0

for alert in state_alerts:
    # Define state functions corresponding to alert tag
    state_functions = eval(f'''sheet_state['{alert}'].dropna()''')

    # Get contracts filtering by alert tag and load their ABIs
    contracts_instance = contracts[contracts['tags_state'].str.contains(alert)]

    filters = {"id": []}
    for i in range(0, len(contracts_instance['contract_address'])):
        contract_name = web3.toChecksumAddress(contracts_instance.iloc[i]['contract_address'])
        contract_abi = json.loads(str(contracts_instance.iloc[i]['ABI']))
        contract = web3.eth.contract(address=contract_name, abi=contract_abi)
        filters["id"].append(contract)

    # Second loop to cover all contracts in the alert tag
    for contract in filters["id"]:
        # Third loop to cover all events, in contract, in alert tag
        for state_function in state_functions:

            state_arguments = fetchers.getAllMarkets('0x4dcf7407ae5c07f8681e1659f626e114a7667339')
            # Initiate Thread per alert/contract/event listened
            for argument in state_arguments:
                StateChangeListener(web3, alert, contract, state_function,argument).start()
                n_alert += 1

                # Log alert-contract-event
                logging.info(str(datetime.now()) + ' ' + alert+'-'+contract.address+'-'+ state_function + '-' + str(n_alert) + ' started listening at state function ' + state_function + ' on contract ' + contract.address)

logging.info(str(datetime.now())+' '+'Total alerts running : ' + str(n_alert))
