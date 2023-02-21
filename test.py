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
tx_hash= '0xff5007e394b2759a33f3308064a22be7fdd71abf84b42a7f2d1868817eb27367'
contract_address = web3.toChecksumAddress('0xBA12222222228d8Ba445958a75a0704d566BF2C8')

# Fetch tx_info to get blockHash for log filter
tx_info = json.loads(Web3.toJSON(web3.eth.get_transaction(tx_hash)))
block_hash=tx_info["blockHash"]

# Get ABI file from etherscan
contract_abi = getABI2(contract_address)
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

topics = eval(f'construct_event_topic_set(contract.events.{event_name}().abi, web3.codec, {{}})')
logs = web3.eth.get_logs({"blockhash": block_hash,"transactionHash": tx_hash })

#events = eval(f'contract.events.{event_name}().processReceipt({{"logs": logs}})')
events = [{'args': {'poolId': '0xff4ce5aaab5a627bf82f4a571ab1ce94aa365ea6000200000000000000000426', 'liquidityProvider': '0x71F12a5b0E60d2Ff8A87FD34E7dcff3c10c914b0', 'tokens': ['0x865377367054516e17014CcdED1e7d814EDC9ce4', '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'], 'deltas': [0, 159812814205], 'protocolFeeAmounts': [526411670823578783, 0]}, 'event': 'PoolBalanceChanged', 'logIndex': 55, 'transactionIndex': 29, 'transactionHash': '0xff5007e394b2759a33f3308064a22be7fdd71abf84b42a7f2d1868817eb27367', 'address': '0xBA12222222228d8Ba445958a75a0704d566BF2C8', 'blockHash': '0x35c77e35f3a3bd13373d5031332383c731c6529ce9fc045f99cdd1c4e601728e', 'blockNumber': 16516689}]
for event in events:
    if event["transactionHash"]==tx_hash:
        logging.info(event)
        HandleEvent(web3, event, alert, contract, event_name).start()
