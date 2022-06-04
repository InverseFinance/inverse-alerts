# import the following dependencies
import json
import os
import logging
import sys
import requests
from datetime import datetime
import pandas as pd
from helpers import LoggerParams, sendError,patch_http_connection_pool
from dotenv import load_dotenv
import fetchers
from web3 import Web3
from listeners import EventListener, StateChangeListener, TxListener
#patch_http_connection_pool(maxsize=1000)
# Load locals and web3 provider
load_dotenv()
LoggerParams()
web3 = Web3(Web3.HTTPProvider(os.getenv('LOCALHOST')))

# Get contracts metadata from excel
sheet_contracts = pd.read_excel('contracts.xlsx', sheet_name='contracts')
sheet_events = pd.read_excel('contracts.xlsx', sheet_name='alerts_events')
sheet_state = pd.read_excel('contracts.xlsx', sheet_name='alerts_state')
sheet_tx = pd.read_excel('contracts.xlsx', sheet_name='alerts_tx')

events_alerts = sheet_events.columns.array
state_alerts = sheet_state.columns.array
tx_alerts = sheet_tx.columns.array


try:
    # Init count of alerts
    n_alert = 0

    # First loop to cover all alert tags  (then contract and events)
    for alert in events_alerts:
        # Define events corresponding to alert tag
        events = eval(f'''sheet_events['{alert}'].dropna()''')

        # Get contracts filtering by alert tag and load their ABIs
        alert_contracts = sheet_contracts[sheet_contracts['tags_events'].str.contains(alert)]

        # Construct all contracts objects and put them in filter array
        filters = {"id": []}
        for i in range(0, len(alert_contracts['contract_address'])):
            contract_name = web3.toChecksumAddress(alert_contracts.iloc[i]['contract_address'])
            contract_abi = json.loads(str(alert_contracts.iloc[i]['ABI']))
            contract = web3.eth.contract(address=contract_name, abi=contract_abi)
            filters["id"].append(contract)

        # Second loop to cover all contracts in the filter array/alert tag
        for contract in filters["id"]:
            # Third loop to cover all events, in contract, in alert tag
            for event_name in events:
                # Initiate Thread per alert/contract/event listened
                EventListener(web3, alert, contract, event_name).start()
                n_alert += 1

                # Log alert-contract-event
                logging.info(str(datetime.now()) + ' ' + alert + '-' + contract.address + '-' + event_name + '-' + str(
                    n_alert) + ' started listening at event ' + event_name + ' on contract ' + contract.address)

    logging.info(str(datetime.now()) + ' ' + 'Total alerts running : ' + str(n_alert))

    for alert in state_alerts:
        # Define state functions corresponding to alert tag
        state_functions = eval(f'''sheet_state['{alert}'].dropna()''')

        # Get contracts filtering by alert tag and load their ABIs
        alert_contracts = sheet_contracts[sheet_contracts['tags_state'].str.contains(alert)]

        # Define a set of filters containing the contract we are going to call (in oracle case only one)
        filters = {"id": []}
        for i in range(0, len(alert_contracts['contract_address'])):
            contract_name = web3.toChecksumAddress(alert_contracts.iloc[i]['contract_address'])
            contract_abi = json.loads(str(alert_contracts.iloc[i]['ABI']))
            contract = web3.eth.contract(address=contract_name, abi=contract_abi)
            filters["id"].append(contract)

        # Second loop to cover all contracts in the alert tag
        for contract in filters["id"]:
            # Third loop to cover all events, in contract, in alert tag
            for state_function in state_functions:
                # Organise state args for reading function

                if alert == 'oracle':
                    # Get an array of all markets to use in the Oracle calling
                    state_arguments = fetchers.getAllMarkets('0x4dcf7407ae5c07f8681e1659f626e114a7667339')
                elif alert == 'cash':
                    state_arguments = None

                if state_arguments is not None:
                    # Initiate Thread per alert/contract/state function listened
                    for argument in state_arguments:
                        StateChangeListener(web3, alert, contract, state_function, argument).start()
                        n_alert += 1

                        # Log alert-contract-event
                        logging.info(
                            str(datetime.now()) + ' ' + alert + '-' + contract.address + '-' + state_function + '-' + str(
                                n_alert) + ' started listening at state function ' + state_function + ' on contract ' + contract.address)
                else:
                    StateChangeListener(web3, alert, contract, state_function, None).start()
                    n_alert += 1

                    # Log alert-contract-event
                    logging.info(
                        str(datetime.now()) + ' ' + alert + '-' + contract.address + '-' + state_function + '-' + str(
                            n_alert) + ' started listening at state function ' + state_function + ' on contract ' + contract.address)

    logging.info(str(datetime.now()) + ' ' + 'Total alerts running : ' + str(n_alert))

    # First loop to cover all alert tags
    for alert in tx_alerts:
        # Define addresses corresponding to alert tag
        addresses = sheet_contracts[sheet_contracts['tags_tx'].str.contains(alert)]

        # Construct all address array
        for i in range(0, len(addresses['contract_address'])):
            contract_name = web3.toChecksumAddress(addresses.iloc[i]['contract_address'])
            TxListener(web3, alert, contract_name).start()
            n_alert += 1

            # Log alerts-contract
            logging.info(str(datetime.now()) + ' ' + alert + '-' + str(contract_name) + '-' + str(
                n_alert) + ' started listening at transactions on Multisig ' + str(contract_name))

    logging.info(str(datetime.now()) + ' ' + 'Total alerts running : ' + str(n_alert))


except Exception as e:
    logging.error(e)
    sendError("Error alert :" + str(e))
    pass
