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

web3 = getWeb3(10)

# Provide alert to be used, event Name, contract and transaction where the event happened
alert = 'swap'
event_name = 'Mint'
tx_hash= '0xdea54c8c0360fef4c6714115872f73d4786df11cf536aa1988b5fffd99d31f63'
contract_address = web3.toChecksumAddress('0x6c5019d345ec05004a7e7b0623a91a0d9b8d590d')

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

