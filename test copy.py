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
address = Web3.toChecksumAddress("0x6c5019d345ec05004a7e7b0623a91a0d9b8d590d")

print(getSushiTokens(web3,address))