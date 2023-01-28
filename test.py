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
alert = 'bal_dola_bb_a_usd'
event_name = 'PoolBalanceChanged'
tx_hash= '0xa94e7a18abf47c26536cac8192dee0d9468aeea5c56f92f6cbb3929d80593575'
contract_address = web3.toChecksumAddress('0xBA12222222228d8Ba445958a75a0704d566BF2C8')

# Fetch tx_info to get blockHash for log filter
tx_info = json.loads(Web3.toJSON(web3.eth.get_transaction(tx_hash)))
block_hash=tx_info["blockHash"]

# Get ABI file from etherscan
contract_abi = getABI2(contract_address)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

topics = eval(f'construct_event_topic_set(contract.events.{event_name}().abi, web3.codec, {{}})')
logs = web3.eth.get_logs({"blockhash": block_hash,"transactionHash": tx_hash })

for log in logs:
    if  log['transactionHash'].hex()==tx_hash :
        print('found it')
        tx = contract.events.PoolBalanceChanged().processLog(log)
        handler = HandleEvent(web3,tx,alert,event_name)
        handler.compose()



#events = eval(f'contract.events.{event_name}().processReceipt({{"logs": logs}})')

    #HandleEvent(web3, event, alert, contract, event_name).start()
