# import the following dependencies
import json
import os
import pandas as pd

from utils import Listener
from dotenv import load_dotenv
from web3 import Web3

from discord import Webhook, RequestsWebhookAdapter

load_dotenv()

web3 = Web3(Web3.HTTPProvider(os.getenv('LOCALHOST')))

alerts = ['dola3crv', 'lending', 'governance']

# Function to monitor event on by alert tag
functions_lending = ['Mint', 'Redeem', 'Borrow', 'RepayBorrow']
functions_governance = ['ProposalCreated', 'ProposalCanceled', 'ProposalQueued', 'ProposalExecuted']
functions_dola3crv = ['AddLiquidity', 'RemoveLiquidity', 'RemoveLiquidityOne']

# State variable to get the result from when event is triggered by alert tag
state_lending = ['name', 'totalSupply']
state_governance = ['proposalCount']
state_dola3crv = ['name', 'symbol', 'totalSupply']

# Webhook per alert tag
webhook_dola3crv = os.getenv('WEBHOOK_DOLA3CRV')
webhook_governance = os.getenv('WEBHOOK_GOVERNANCE')
webhook_lending = os.getenv('WEBHOOK_LENDING')

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

        # Third loop to cover all functions
        for j in functions:
            function = j

            # Initiate Threads
            Listener(web3, alert, contract, function, state_functions, webhook).start()
            n_alert += 1

            print('Alert ' + alert + ' started listening at function ' + function + ' on contract ' + contract.address + ' (n.' + str(n_alert) + ')')

print('Alerts running : ' + str(n_alert))
