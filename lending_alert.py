# import the following dependencies
import json
import os
from dotenv import load_dotenv
from web3 import Web3
from threading import Thread
import pandas as pd
import asyncio
from discord import Webhook, RequestsWebhookAdapter

load_dotenv()
ENDPOINT = os.getenv('LOCALHOST')  # Add blockchain connection information
WEBHOOK = os.getenv('ANALYTICS_WEBHOOK')  # Discord : analytics alert webhook

web3 = Web3(Web3.HTTPProvider(ENDPOINT))
webhook = Webhook.from_url(WEBHOOK, adapter=RequestsWebhookAdapter())

# Get contracts filter ABIs and contract by alert name
contracts = pd.read_excel('contracts.xlsx', sheet_name='contracts')
contracts = contracts[contracts['tags'].str.contains("lending")]

# Load token addresses and ABIs
# Add contract in dictionnary to run main() iteratively
filters ={"id":[]}
for i in range(0, len(contracts['contract_address'])):
    contract_name = web3.toChecksumAddress(contracts.iloc[i]['contract_address'])
    contract_abi = json.loads(contracts.iloc[i]['ABI'])
    filters["id"].append(web3.eth.contract(address=contract_name, abi=contract_abi))

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

    webhook.send("Borrow Event Detected" +
                 "\n" + "Block Number : " + str(tx['blockNumber']) +
                 "\n" + "Event Type : " + tx['event'] +
                 "\n" + "Args : " + str(tx['args']) +
                 "\n" + "Transaction Hash : " + tx['transactionHash'] +
                 "\n" + "Etherscan : https://etherscan.io/tx/" + tx['transactionHash']+
                 "\n" + "Full tx : " + str(tx))

# define worker to listen on a specific event of a specific contract
async def worker(contract):
    event_filter = contract.events.Borrow.createFilter(fromBlock='latest')
    while True:
        for Borrow in event_filter.get_new_entries():
            handle_event(Borrow)
        await asyncio.sleep(5)

def main():
    for i in filters["id"]:
        contract = i
        MyThread(contract).start()

if __name__ == "__main__":
    main()