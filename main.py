# import the following dependencies
import json
import os
import pandas as pd
import fetchers

from utils import Listener
from dotenv import load_dotenv
from web3 import Web3
from discord import Webhook, RequestsWebhookAdapter
import requests
from threading import Thread
from datetime import datetime
from utils import sendWebhook,makeFields

#Thread(os.system('cmd /k "geth --syncmode light --http --http.addr 0.0.0.0"')).start()

load_dotenv()
web3 = Web3(Web3.HTTPProvider(os.getenv('LOCALHOST'))) # Or infura key

# Get alerts, functions, and state functions to read from
functions = pd.read_excel('contracts.xlsx', sheet_name='alerts_func')
state = pd.read_excel('contracts.xlsx', sheet_name='alerts_state')
alerts = functions.columns.array

for alert in alerts:
    exec(f"functions_{alert} = functions['{alert}'].dropna()")
    exec(f"state_{alert} = state['{alert}'].dropna()")
    exec(f"webhook_{alert} = os.getenv(str('webhook_{alert}').upper())")

n_alert = 0

# First loop to cover all alert tags  (then contract and functions)
for alert in alerts:

    # Define webhook, functions and state functions corresponding to alert name
    webhook = eval(f'webhook_{alert}')
    state_functions = eval(f'state_{alert}')
    functions = eval(f'functions_{alert}')

    # Get contracts filtering by alert tag and load their ABIs
    contracts = pd.read_excel('contracts.xlsx', sheet_name='contracts')
    contracts = contracts[contracts['tags'].str.contains(str(alert))]

    filters = {"id": []}
    for i in range(0, len(contracts['contract_address'])):
        contract_name = web3.toChecksumAddress(contracts.iloc[i]['contract_address'])
        contract_abi = json.loads(str(contracts.iloc[i]['ABI']))
        contract = web3.eth.contract(address=contract_name, abi=contract_abi)
        filters["id"].append(contract)


    # Second loop to cover all contracts in the alert tag
    for i in filters["id"]:
        contract = i

        # Third loop to cover all functions, in contract, in alert tag
        for j in functions:
            function = j

            # Initiate Thread per alert/contract/function listened
            Listener(web3, alert, contract, function, state_functions, webhook).start()
            n_alert += 1

            print(str(datetime.now())+' '+ alert+'-'+contract.address+'-'+function+'-'+ str(n_alert) + ' started listening at function ' + function + ' on contract ' + contract.address)

print(str(datetime.now())+' '+'Total alerts running : ' + str(n_alert))
