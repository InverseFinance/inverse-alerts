import pandas as pd
from dotenv import load_dotenv
from web3 import Web3
from web3._utils.events import construct_event_topic_set
from handlers.handlers import HandleEvent
from utils.helpers import LoggerParams
import  os, sys, requests,warnings,json

# Load locals and web3 provider
load_dotenv()
LoggerParams()

web3 = Web3(Web3.HTTPProvider(os.getenv('QUICKNODE_ETH')))

# Provide alert to be used, event Name, contract and transaction where the event happened
alert = 'bal_dola_deposit'
event_name = 'Deposited'
tx_hash= '0x9ca239eff9286e0448c5829517fcc4c26ad967105faa67a05619f2e743147394'
contract_address = web3.toChecksumAddress('0xa57b8d98dae62b26ec3bcc4a365338157060b234')

# Fetch tx_info to get blockHash for log filter
tx_info = json.loads(Web3.toJSON(web3.eth.get_transaction(tx_hash)))
block_hash=tx_info["blockHash"]

# Get ABI file from etherscan
contract_abi = requests.get('https://api.etherscan.io/api?module=contract&action=getabi&address='+contract_address+'&apikey='+os.getenv('ETHERSCAN')).json()['result']
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

topics = eval(f'construct_event_topic_set(contract.events.{event_name}().abi, web3.codec, {{}})')
logs = web3.eth.get_logs({"blockhash": block_hash})
events = eval(f'contract.events.{event_name}().processReceipt({{"logs": logs}})')


for event in events:
    print(Web3.toJSON(event))
    HandleEvent(web3, event, alert, contract, event_name).start()

