# import the following dependencies
import json
import os
import pandas as pd
import fetchers
from threading import Thread
from utils import EventListener,StateChangeListener,TxListener,LoggerParams
from dotenv import load_dotenv
from web3 import Web3
from datetime import datetime
import logging
import sys

# Load locals and web3 provider
load_dotenv()
LoggerParams()
web3 = Web3(Web3.HTTPProvider(os.getenv('LOCALHOST')))

# Get contracts metadata from excel
sheet_contracts = pd.read_excel('contracts.xlsx', sheet_name='contracts')
sheet_events = pd.read_excel('contracts.xlsx', sheet_name='alerts_events')
sheet_state = pd.read_excel('contracts.xlsx', sheet_name='alerts_state')
sheet_tx = pd.read_excel('contracts.xlsx', sheet_name='alerts_tx')
#sheet_state_arguments = pd.read_excel('contracts.xlsx', sheet_name='state_arguments')

events_alerts = sheet_events.columns.array
state_alerts = sheet_state.columns.array
tx_alerts = sheet_tx.columns.array

# Init count of alerts
n_alert = 0

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
        logging.info(str(datetime.now())+' '+ alert+'-'+str(contract_name)+'-'+ str(n_alert) + ' started listening at transactions on Multisig ' + str(contract_name))

logging.info(str(datetime.now())+' '+'Total alerts running : ' + str(n_alert))

