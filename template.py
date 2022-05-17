# import the following dependencies
import json
import os
from dotenv import load_dotenv
from web3 import Web3
from threading import Thread
import pandas as pd
from discord import Webhook, RequestsWebhookAdapter

load_dotenv()
ENDPOINT = os.getenv('ALCHEMY_URL')  # Add blockchain connection information
WEBHOOK = os.getenv('ANALYTICS_WEBHOOK')  # Discord : analytics alert webhook

web3 = Web3(Web3.HTTPProvider(ENDPOINT))
webhook = Webhook.from_url(WEBHOOK, adapter=RequestsWebhookAdapter())

# Get contracts filter ABIs and contract by alert name
contracts = pd.read_excel('contracts.xlsx', sheet_name='contracts')
contracts = contracts[contracts['tags'].str.contains("lending")]

# Load token addresses and ABIs
# Add contract in dictionnary to run main() iteratively
filters ={"id":[]}
for i in range(0, len(contracts['Contract Address'])):
    contract_name = web3.toChecksumAddress(contracts.iloc[i]['Contract Address'])
    contract_abi = json.loads(contracts.iloc[i]['ABI'])
    filters["id"].append(web3.eth.contract(address=contract_name, abi=contract_abi))

# Create homemade thread to parallelize contracts listeners/filters
class MyThread(Thread):
    def __init__(self,argument, **kwargs):
        super(MyThread, self).__init__(**kwargs)
        self.argument = argument

    def run(self):
        event_filter = self.argument.events.Transfer.createFilter(fromBlock='latest')
        while True:
            for Transfer in event_filter.get_new_entries():
                handle_event(Transfer)

# define function to handle events and print to the console
def handle_event(event):
    print(Web3.toJSON(event))
    tx = json.loads(Web3.toJSON(event))

    webhook.send("Token Transfer Detected" +
                 "\n" + "Block Number : " + str(tx['blockNumber']) +
                 "\n" + "Event Type : " + tx['event'] +
                 "\n" + "From : " + str(tx['args']) +
                 "\n" + "Transaction Hash : " + tx['transactionHash'] +
                 "\n" + "Etherscan : https://etherscan.io/tx/" + tx['transactionHash'])

# define worker to listen on a specific event of a specific contract
def worker(contract):
    event_filter = contract.events.Transfer.createFilter(fromBlock='latest')
    while True:
        for Transfer in event_filter.get_new_entries():
            handle_event(Transfer)

def main():
    for i in filters["id"]:
        contract = i
        MyThread(contract).start()

if __name__ == "__main__":
    main()