import pandas as pd
from dotenv import load_dotenv
from web3 import Web3
from web3._utils.events import construct_event_topic_set
from handlers.handlers import HandleEvent
from utils.helpers import LoggerParams
import  os, sys, requests,warnings,json
from utils.fetchers import *
# Load locals and web3 provider
load_dotenv()
LoggerParams()

web3 = getWeb3(1)

# Provide alert to be used, event Name, contract and transaction where the event happened
alert = 'bal_dola_deposit'
event_name = 'Withdrawn'
tx_hash= '0xd70a3f767c6bc1e9fe700b8ef18665b5058d39189640b28dfe2308d5aa0d080e'
contract_address = web3.toChecksumAddress('0xa57b8d98dae62b26ec3bcc4a365338157060b234')

# Fetch tx_info to get blockHash for log filter
tx_info = json.loads(Web3.toJSON(web3.eth.get_transaction(tx_hash)))
block_hash=tx_info["blockHash"]

# Get ABI file from etherscan
contract_abi = getABI2(contract_address)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

topics = eval(f'construct_event_topic_set(contract.events.{event_name}().abi, web3.codec, {{}})')
logs = web3.eth.get_logs({"blockhash": block_hash})
events = eval(f'contract.events.{event_name}().processReceipt({{"logs": logs}})')


for event in events:
    print(Web3.toJSON(event))
    HandleEvent(web3, event, alert, contract, event_name).start()
