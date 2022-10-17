# import the following dependencies
import pandas as pd
from dotenv import load_dotenv
from web3 import Web3
from web3._utils.events import construct_event_topic_set
from handlers import HandleEvent
from helpers import LoggerParams
import  os, sys, requests,warnings,json

# Load locals and web3 provider
load_dotenv()
LoggerParams()

web3 = Web3(Web3.HTTPProvider(os.getenv('QUICKNODE_ETH')))

# Provide alert to be used, event Name, contract and transaction where the event happened
alert = 'harvest'
tx_hash= '0x3e33c390a5b7a60a427a9ab3c7ca4a85b6473e0aa8cf590e8dac8deef7011dcf'
contract_address = web3.toChecksumAddress('0x64e4fC597C70B26102464B7F70B1F00C77352910')
event_name = 'Harvested'
event_filter =[{}]

# Fetch tx_info to get blockHash and filter logs (cant filter on txHash)
tx = json.loads(Web3.toJSON(web3.eth.get_transaction(tx_hash)))
block_hash=tx["blockHash"]

# Get ABI file from etherscan
contract_abi = requests.get('https://api.etherscan.io/api?module=contract&action=getabi&address='+contract_address+'&apikey='+os.getenv('ETHERSCAN')).json()['result']
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
topics = []

for i in event_filter:
    sub_topic = eval(f'construct_event_topic_set(contract.events.{event_name}().abi, web3.codec, {str(i)})')
    topics.append(sub_topic)

for j in topics:
    logs = web3.eth.get_logs({"topics": j, "blockhash": block_hash})
    events = eval(f'contract.events.{event_name}().processReceipt({{"logs": logs}})')

    for event in events:
        print(Web3.toJSON(event))
    HandleEvent(web3, event, alert, contract, event_name).start()

