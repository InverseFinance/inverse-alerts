# import the following dependencies
import json
import os
import pandas as pd
from utils import Listener
from dotenv import load_dotenv
from web3 import Web3
from discord import Webhook, RequestsWebhookAdapter
from threading import Thread
from datetime import datetime

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

# First loop to cover all alerts type
for alert in alerts:

    # Define webhook corresponding to alert
    use_webhook = eval(f'webhook_{alert}')
    webhook = Webhook.from_url(use_webhook, adapter=RequestsWebhookAdapter())

    state_functions = eval(f'state_{alert}')

    # Get contracts filter ABIs and contract by alert name
    contracts = pd.read_excel('contracts.xlsx', sheet_name='contracts')
    contracts = contracts[contracts['tags'].str.contains(str(alert))]

    # Load token addresses and ABIs corresponding to the alerts
    filters = {"id": []}
    for i in range(0, len(contracts['contract_address'])):

        contract_name = web3.toChecksumAddress(contracts.iloc[i]['contract_address'])
        contract_abi = json.loads(str(contracts.iloc[i]['ABI']))
        contract = web3.eth.contract(address=contract_name, abi=contract_abi)
        filters["id"].append(contract)


    functions = eval(f'functions_{alert}')

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
