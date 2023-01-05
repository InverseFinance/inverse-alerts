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
alert = 'governance'
event_name = 'ProposalExecuted'
tx_hash= '0xcddba54afa4433ac89507b01eeea4c4b5e825a8ddb95c5d0fe45e25ba3976d50'
contract_address = web3.toChecksumAddress('0xbeccb6bb0aa4ab551966a7e4b97cec74bb359bf6')

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
    time.sleep(15)

list