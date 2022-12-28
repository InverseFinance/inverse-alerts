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
alert = 'transf_inv'
event_name = 'Transfer'
tx_hash= '0x74b7dae6a0fde13183f6002085b4a601839cd77b7a41ba5833aedb02a24201d2'
contract_address = web3.toChecksumAddress('0x41d5d79431a913c4ae7d69a668ecdfe5ff9dfb68')

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

