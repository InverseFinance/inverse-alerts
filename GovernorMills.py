# import the following dependencies
import json
import asyncio
import os
from dotenv import load_dotenv
from web3 import Web3
from threading import Thread
import pandas as pd
from discord import Webhook, RequestsWebhookAdapter

load_dotenv()
ENDPOINT = os.getenv('LOCALHOST')  # Add blockchain connection information
WEBHOOK = os.getenv('GOVERNANCE_WEBHOOK')  # Discord : analytics alert webhook

web3 = Web3(Web3.HTTPProvider(ENDPOINT))
webhook = Webhook.from_url(WEBHOOK, adapter=RequestsWebhookAdapter())

# Get contracts filter ABIs and contract by alert name
contracts = pd.read_excel('contracts.xlsx', sheet_name='contracts')
contracts = contracts[contracts['tags'].str.contains("governance")]

functions = ['ProposalCreated',
             'ProposalCanceled',
             'ProposalQueued',
             'ProposalExecuted']

# Load token addresses and ABIs
# Add contract in dictionnary to run main() iteratively
filters ={"id":[]}
for i in range(0, len(contracts['contract_address'])):
    contract_name = web3.toChecksumAddress(contracts.iloc[i]['contract_address'])
    contract_abi = json.loads(contracts.iloc[i]['ABI'])
    filters["id"].append(web3.eth.contract(address=contract_name, abi=contract_abi))

class MyThread(Thread):
    def __init__(self,argument1,argument2, **kwargs):
        super(MyThread, self).__init__(**kwargs)
        self.argument1 = argument1
        self.argument2 = argument2
        self.event_filter = []

    def run(self):
        exec(f"self.event_filter = self.argument1.events.{self.argument2}.createFilter(fromBlock='latest')")
        while True:
            for handler in self.event_filter.get_new_entries():
                handle_event(handler)


# define function to handle events and print to the console
def handle_event(event):
    print(Web3.toJSON(event))
    tx = json.loads(Web3.toJSON(event))
    title = "Governor Mills : New " + tx['event']

    webhook.send(title +
                 "\n" + "Block Number : " + str(tx['blockNumber']) +
                 "\n" + "Transaction Hash : " + tx['transactionHash'] +
                 "\n" + "Etherscan : https://etherscan.io/tx/" + tx['transactionHash']+
                 "\n" + "Full tx" + str(tx)+
                 "\n" + "Tag Test <@578956365205209098>")

def main():
    for i in filters["id"]:
        contract = i
        for j in functions:
            function = j
            MyThread(contract, function).start()
            print('Started listening at function '+function+' on contract '+contract.address)

if __name__ == "__main__":
    main()