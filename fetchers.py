import json,os,requests
import pandas as pd
from ens import ENS
from dotenv import load_dotenv
from helpers import getABI
from web3._utils.events import construct_event_topic_set
#from web3 import Web3

load_dotenv()


# Catch the token where the tx of RemoveLiquidityOne happens
def getRemovedTokenSymbol(web3, txHash,poolAddress):
    usdc_address = web3.toChecksumAddress('0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48')
    dola_address =web3.toChecksumAddress('0x865377367054516e17014ccded1e7d814edc9ce4')
    dai_address = web3.toChecksumAddress('0x6b175474e89094c44da98b954eedeac495271d0f')
    crvFRAX_address = web3.toChecksumAddress('0x3175Df0976dFA876431C2E9eE6Bc45b65d3473CC')
    crv3_address = web3.toChecksumAddress('0x6c3f90f043a72fa612cbac8115ee7e52bde6e490')
    usdt_address = web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')

    tx = json.loads(web3.toJSON(web3.eth.get_transaction(txHash)))
    blockHash = tx["blockHash"]
    for token in ('dola','usdc','dai','crvFRAX','crv3','usdt'):
        contract = web3.eth.contract(address=eval(f'{token}_address'), abi=eval(f'getABI({token}_address)'))

        topics = construct_event_topic_set(contract.events.Transfer().abi, web3.codec, {})
        logs = web3.eth.get_logs({"address":contract.address,"blockHash": blockHash})
        events = contract.events.Transfer().processReceipt({"logs": logs})
        for event in events:
            if web3.toChecksumAddress(poolAddress) in str(event['args']):
                return getSymbol(web3,contract.address)

# Common used functions
def getBalance(web3,address, token_address):

    address = web3.toChecksumAddress(address)
    token_address = web3.toChecksumAddress(token_address)
    token_ABI = getABI(token_address)
    contract = web3.eth.contract(address=token_address, abi=token_ABI)

    balance = contract.functions.balanceOf(address).call()
    balance = balance / getDecimals(web3,token_address)
    if (balance == 0): balance = 0

    return balance


def getDecimals(web3,address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    if (address == web3.toChecksumAddress('0x0000000000000000000000000000000000000000')):
        decimals = 1e18
    else:
        address = web3.toChecksumAddress(address)
        ABI = getABI(address)
        contract = web3.eth.contract(address=address, abi=ABI)

        decimals = contract.functions.decimals().call()
        decimals = eval(f'1e{decimals}')
    return decimals


def getSupply(web3, address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    address = web3.toChecksumAddress(address)
    ABI = getABI(address)
    contract = web3.eth.contract(address=address, abi=ABI)

    supply = contract.functions.totalSupply().call()
    supply = supply / getDecimals(web3,address)

    if (supply == 0): supply = 0

    return supply


def getName(web3,address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    if (address == web3.toChecksumAddress('0x0000000000000000000000000000000000000000')):
        name = 'Ether'
    else:
        address = web3.toChecksumAddress(address)
        ABI = getABI(address)
        contract = web3.eth.contract(address=address, abi=ABI)
        name = contract.functions.name().call()
    return name


def getSymbol(web3,address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    if (address == web3.toChecksumAddress('0x0000000000000000000000000000000000000000')):
        symbol = 'ETH'
    else:
        address = web3.toChecksumAddress(address)
        ABI = getABI(address)
        contract = web3.eth.contract(address=address, abi=ABI)
        symbol = contract.functions.symbol().call()

    return symbol


def getTransaction(web3,tx):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    tx = web3.eth.get_transaction(tx)
    return tx

def getENS(web3, address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    ns = ENS.fromWeb3(web3)
    address = web3.toChecksumAddress(address)

    address_ens = ns.name(address)

    if str(address_ens) == 'None':
        address_ens = address

    return address_ens

# Governor Mills and multisig related function
def getProposal(web3,proposal_id):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    address = web3.toChecksumAddress('0xbeccb6bb0aa4ab551966a7e4b97cec74bb359bf6')
    ABI = getABI(address)

    contract = web3.eth.contract(address=address, abi=ABI)

    proposal = contract.functions.proposals(proposal_id).call()

    if (proposal == 0): proposal = 0

    return proposal

def getProposalCount(web3):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    address = web3.toChecksumAddress('0xbeccb6bb0aa4ab551966a7e4b97cec74bb359bf6')
    ABI = getABI(address)
    contract = web3.eth.contract(address=address, abi=ABI)

    proposal = contract.functions.proposalCount().call()

    if (proposal == 0): proposal = 0

    return proposal

## Sushi related functions
def getSushiTokens(web3,address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    tokens = []
    address = web3.toChecksumAddress(address)
    ABI = getABI(address)
    contract = web3.eth.contract(address=address, abi=ABI)
    tokens.append(contract.functions.token0().call())
    tokens.append(contract.functions.token1().call())

    return tokens

def getSushiTokensName(web3,address):
    names = []
    names.append(getName(getSushiTokens(web3,address)[0]))
    names.append(getName(getSushiTokens(web3,address)[1]))
    return names

def getSushiTokensSymbol(web3,address):
    symbols = []

    symbols.append(getSymbol(web3,getSushiTokens(web3,address)[0]))
    symbols.append(getSymbol(web3,getSushiTokens(web3,address)[1]))

    return symbols

def getSushiBalance(web3,address):
    balances = []

    balances.append(getBalance(web3,address, getSushiTokens(web3,address)[0]))
    balances.append(getBalance(web3,address, getSushiTokens(web3,address)[1]))

    return balances


## DOLA3CRV related functions
def getCurveBalances(web3,address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    balances = []
    address = web3.toChecksumAddress(address)

    balances.append(getBalance(web3,address, getDola3crvTokens(web3)[0]))
    balances.append(getBalance(web3,address, getDola3crvTokens(web3)[1]))

    return balances

def getDola3crvTokens(web3,pooladdress):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    balances = []
    address = web3.toChecksumAddress(pooladdress)
    ABI = getABI(address)
    contract = web3.eth.contract(address=address, abi=ABI)
    balances.append(contract.functions.coins(0).call())
    balances.append(contract.functions.coins(1).call())

    return balances

def getDola3crvTokensName(web3):
    names = []

    names.append(getName(web3,getDola3crvTokens(web3)[0]))
    names.append(getName(web3,getDola3crvTokens(web3)[1]))

    return names

def getDola3crvTokensSymbol(web3):
    symbols = []

    symbols.append(getSymbol(web3,getDola3crvTokens(web3)[0]))
    symbols.append(getSymbol(web3,getDola3crvTokens(web3)[1]))

    return symbols


# Comptroller related functions
def getAllMarkets(web3,address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    address = web3.toChecksumAddress(address)
    ABI = getABI(address)
    contract = web3.eth.contract(address=address, abi=ABI)

    allMarkets = contract.functions.getAllMarkets().call()

    return allMarkets

def getComptroller(web3,address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    address = web3.toChecksumAddress(address)
    ABI = getABI(address)
    contract = web3.eth.contract(address=address, abi=ABI)

    comptroller = contract.functions.comptroller().call()

    return comptroller

def getUnderlyingPrice(web3,address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    address = web3.toChecksumAddress(address)

    oracle_name = web3.toChecksumAddress('0xe8929afd47064efd36a7fb51da3f8c5eb40c4cb4')
    oracle_ABI = getABI(oracle_name)

    contract = web3.eth.contract(address=oracle_name, abi=oracle_ABI)
    underlying_decimals = getDecimals(web3,getUnderlying(web3,address))
    price = contract.functions.getUnderlyingPrice(address).call()
    if address == web3.toChecksumAddress('0x17786f3813E6bA35343211bd8Fe18EC4de14F28b'):
        price = price / 1e28
    else:
        price = price / underlying_decimals

    if (price == 0): price = 1

    return price

def getUnderlyingPriceFuse(web3,address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    address = web3.toChecksumAddress(address)

    oracle_name = web3.toChecksumAddress('0xe980efb504269ff53f7f4bc92a2bd1e31b43f632')
    oracle_ABI = getABI(address)

    contract = web3.eth.contract(address=oracle_name, abi=oracle_ABI)
    underlying_decimals = getDecimals(web3,getUnderlying(web3,address))
    price = contract.functions.getUnderlyingPrice(address).call()

    if address == web3.toChecksumAddress('0x17786f3813E6bA35343211bd8Fe18EC4de14F28b'):
        price = price / 1e28
    else:
        price = price / underlying_decimals

    if (price == 0): price = 1

    return price

def getUnderlying(web3,address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    if address in ['0x697b4acAa24430F254224eB794d2a85ba1Fa1FB8','0x8e103Eb7a0D01Ab2b2D29C91934A9aD17eB54b86']:
        underlying = '0x0000000000000000000000000000000000000000'
    else:
        address = web3.toChecksumAddress(address)
        ABI = getABI(address)
        contract = web3.eth.contract(address=address, abi=ABI)
        underlying = contract.functions.underlying().call()
    return underlying

def getUnderlyingFuse(web3,address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    if (address == web3.toChecksumAddress('0x26267e41ceca7c8e0f143554af707336f27fa051')):
        underlying = '0x0000000000000000000000000000000000000000'
    else:
        address = web3.toChecksumAddress(address)
        ABI = getABI(address)
        contract = web3.eth.contract(address=address, abi=ABI)
        underlying = contract.functions.underlying().call()
    return underlying

def getCash(web3,address):
    #web3 = Web3(Web3.HTTPProvider(os.getenv(env)))
    address = web3.toChecksumAddress(address)
    ABI = getABI(address)
    contract = web3.eth.contract(address=address, abi=ABI)

    cash = contract.functions.getCash().call()
    cash = cash / getDecimals(web3,contract.functions.underlying().call())

    if (cash == 0): cash = 0

    return cash
