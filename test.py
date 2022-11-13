# import the following dependencies
from utils.listeners import *
from utils.helpers import *
from contracts.contracts import Contract
from dotenv import load_dotenv
import logging
import asyncio

# Load locals and web3 provider
load_dotenv()
LoggerParams()
import panoramix
WEB3_PROVIDER_URI=os.getenv('QUICKNODE_ETH')
panoramix 0x0d94D81FD712126E7f320b5B10537D01d6a01563