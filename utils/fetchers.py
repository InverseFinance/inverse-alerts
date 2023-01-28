import json,os,requests,logging
import pandas as pd
from ens import ENS
from dotenv import load_dotenv
from utils.helpers import *
from web3._utils.events import construct_event_topic_set

LoggerParams()
load_dotenv()
ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

# Catch the token where the tx of RemoveLiquidityOne happens
def getRemovedTokenSymbol(web3, txHash,poolAddress):
    USDC = web3.toChecksumAddress('0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48')
    DOLA =web3.toChecksumAddress('0x865377367054516e17014ccded1e7d814edc9ce4')
    DAI = web3.toChecksumAddress('0x6b175474e89094c44da98b954eedeac495271d0f')
    crvFRAX = web3.toChecksumAddress('0x3175Df0976dFA876431C2E9eE6Bc45b65d3473CC')
    CRV3 = web3.toChecksumAddress('0x6c3f90f043a72fa612cbac8115ee7e52bde6e490')
    USDT = web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')

    tx = json.loads(web3.toJSON(web3.eth.get_transaction(txHash)))
    blockHash = tx["blockHash"]

    for token in [USDC,DOLA,DAI,crvFRAX,CRV3,USDT]:
        contract = web3.eth.contract(address=token, abi=getABI2(token))
        filters = {"from": poolAddress}

        topics = construct_event_topic_set(contract.events.Transfer().abi, web3.codec, filters)
        logs = web3.eth.get_logs({"address":contract.address,"topics":topics,"blockHash": blockHash})
        if logs==[]:
            pass
        else:
            events = contract.events.Transfer().processReceipt({"logs": logs})
            for event in events:
                if web3.toChecksumAddress(poolAddress) in str(event['args']):
                    return getSymbol(web3,contract.address)
                    break

# Common used functions
def getBalance(web3,address, token_address):

    address = web3.toChecksumAddress(address)
    token_address = web3.toChecksumAddress(token_address)
    token_ABI = getABI2(token_address)
    contract = web3.eth.contract(address=token_address, abi=token_ABI)

    balance = contract.functions.balanceOf(address).call()
    balance = balance / getDecimals(web3,token_address)
    if (balance == 0): balance = 0

    return balance


def getDecimals(web3,address):
    
    if (address in [web3.toChecksumAddress(ZERO_ADDRESS),"0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"]):
        decimals = 1e18
    else:
        address = web3.toChecksumAddress(address)
        ABI = getABI2(address)
        contract = web3.eth.contract(address=address, abi=ABI)

        decimals = contract.functions.decimals().call()
        decimals = eval(f'1e{decimals}')
    return decimals


def getSupply(web3, address):
    
    address = web3.toChecksumAddress(address)
    ABI = getABI2(address)
    contract = web3.eth.contract(address=address, abi=ABI)

    supply = contract.functions.totalSupply().call()
    supply = supply / getDecimals(web3,address)

    if (supply == 0): supply = 0

    return supply


def getName(web3,address):
    
    if (address == web3.toChecksumAddress(ZERO_ADDRESS)):
        name = 'Ether'
    else:
        address = web3.toChecksumAddress(address)
        ABI = getABI2(address)
        contract = web3.eth.contract(address=address, abi=ABI)
        name = contract.functions.name().call()
    return name


def getSymbol(web3,address):
    
    if (address == web3.toChecksumAddress(ZERO_ADDRESS)):
        symbol = 'ETH'
    else:
        address = web3.toChecksumAddress(address)
        ABI = getABI2(address)
        contract = web3.eth.contract(address=address, abi=ABI)
        symbol = contract.functions.symbol().call()

    return symbol


def getTransaction(web3,tx):
    
    tx = web3.eth.get_transaction(tx)
    return tx

def getENS(web3, address):
    
    ns = ENS.fromWeb3(web3)
    address = web3.toChecksumAddress(address)

    address_ens = ns.name(address)

    if str(address_ens) == 'None':
        address_ens = address

    return address_ens

# Governor Mills and multisig related function
def getProposal(web3,proposal_id):
    
    address = web3.toChecksumAddress('0xbeccb6bb0aa4ab551966a7e4b97cec74bb359bf6')
    ABI = getABI2(address)

    contract = web3.eth.contract(address=address, abi=ABI)

    proposal = contract.functions.proposals(proposal_id).call()

    if (proposal == 0): proposal = 0

    return proposal

def getProposalCount(web3):
    
    address = web3.toChecksumAddress('0xbeccb6bb0aa4ab551966a7e4b97cec74bb359bf6')
    ABI = getABI2(address)
    contract = web3.eth.contract(address=address, abi=ABI)

    proposal = contract.functions.proposalCount().call()

    if (proposal == 0): proposal = 0

    return proposal

## Sushi related functions
def getSushiTokens(web3,address):
    
    tokens = []
    address = web3.toChecksumAddress(address)
    ABI = getABI2(address)
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
    
    balances = []
    address = web3.toChecksumAddress(address)

    balances.append(getBalance(web3,address, getDola3crvTokens(web3)[0]))
    balances.append(getBalance(web3,address, getDola3crvTokens(web3)[1]))

    return balances

def getDola3crvTokens(web3,pooladdress):
    
    balances = []
    address = web3.toChecksumAddress(pooladdress)
    ABI = getABI2(address)
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
    
    address = web3.toChecksumAddress(address)
    ABI = getABI2(address)
    contract = web3.eth.contract(address=address, abi=ABI)

    allMarkets = contract.functions.getAllMarkets().call()

    return allMarkets

def getComptroller(web3,address):
 
    address = web3.toChecksumAddress(address)
    ABI = getABI2(address)
    contract = web3.eth.contract(address=address, abi=ABI)

    comptroller = contract.functions.comptroller().call()

    return comptroller

def getUnderlyingPrice(web3,address):
    
    address = web3.toChecksumAddress(address)

    oracle_name = web3.toChecksumAddress('0xe8929afd47064efd36a7fb51da3f8c5eb40c4cb4')
    oracle_ABI = getABI2(oracle_name)

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
    
    address = web3.toChecksumAddress(address)

    oracle_name = web3.toChecksumAddress('0xe980efb504269ff53f7f4bc92a2bd1e31b43f632')
    oracle_ABI = getABI2(address)

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
    
    if address in ['0x697b4acAa24430F254224eB794d2a85ba1Fa1FB8','0x8e103Eb7a0D01Ab2b2D29C91934A9aD17eB54b86']:
        underlying = ZERO_ADDRESS
    else:
        address = web3.toChecksumAddress(address)
        ABI = getABI2(address)
        contract = web3.eth.contract(address=address, abi=ABI)
        underlying = contract.functions.underlying().call()
    return underlying

def getUnderlyingFuse(web3,address):
    
    if (address == web3.toChecksumAddress('0x26267e41ceca7c8e0f143554af707336f27fa051')):
        underlying = ZERO_ADDRESS
    else:
        address = web3.toChecksumAddress(address)
        ABI = getABI2(address)
        contract = web3.eth.contract(address=address, abi=ABI)
        underlying = contract.functions.underlying().call()
    return underlying


def getCash(web3, address):
    address = web3.toChecksumAddress(address)
    ABI = getABI2(address)
    contract = web3.eth.contract(address=address, abi=ABI)

    cash = contract.functions.getCash().call()
    cash = cash / getDecimals(web3, contract.functions.underlying().call())

    if (cash == 0): cash = 0

    return cash
def getExchangeRateStored(web3,address):

    address = web3.toChecksumAddress(address)
    ABI = getABI2(address)
    contract = web3.eth.contract(address=address, abi=ABI)

    rate = contract.functions.exchangeRateStored().call()
    rate = rate / getDecimals(web3,getUnderlying(web3,contract.address))

    if (rate == 0): rate = 0

    return rate

def getBalancerVaultBalances(web3,poolId):
    address = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
    ABI = '[{"inputs":[{"internalType":"contract IAuthorizer","name":"authorizer","type":"address"},{"internalType":"contract IWETH","name":"weth","type":"address"},{"internalType":"uint256","name":"pauseWindowDuration","type":"uint256"},{"internalType":"uint256","name":"bufferPeriodDuration","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IAuthorizer","name":"newAuthorizer","type":"address"}],"name":"AuthorizerChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"ExternalBalanceTransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IFlashLoanRecipient","name":"recipient","type":"address"},{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"feeAmount","type":"uint256"}],"name":"FlashLoan","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":false,"internalType":"int256","name":"delta","type":"int256"}],"name":"InternalBalanceChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"paused","type":"bool"}],"name":"PausedStateChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"poolId","type":"bytes32"},{"indexed":true,"internalType":"address","name":"liquidityProvider","type":"address"},{"indexed":false,"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"indexed":false,"internalType":"int256[]","name":"deltas","type":"int256[]"},{"indexed":false,"internalType":"uint256[]","name":"protocolFeeAmounts","type":"uint256[]"}],"name":"PoolBalanceChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"poolId","type":"bytes32"},{"indexed":true,"internalType":"address","name":"assetManager","type":"address"},{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":false,"internalType":"int256","name":"cashDelta","type":"int256"},{"indexed":false,"internalType":"int256","name":"managedDelta","type":"int256"}],"name":"PoolBalanceManaged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"poolId","type":"bytes32"},{"indexed":true,"internalType":"address","name":"poolAddress","type":"address"},{"indexed":false,"internalType":"enum IVault.PoolSpecialization","name":"specialization","type":"uint8"}],"name":"PoolRegistered","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"relayer","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"RelayerApprovalChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"poolId","type":"bytes32"},{"indexed":true,"internalType":"contract IERC20","name":"tokenIn","type":"address"},{"indexed":true,"internalType":"contract IERC20","name":"tokenOut","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountIn","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountOut","type":"uint256"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"poolId","type":"bytes32"},{"indexed":false,"internalType":"contract IERC20[]","name":"tokens","type":"address[]"}],"name":"TokensDeregistered","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"poolId","type":"bytes32"},{"indexed":false,"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"indexed":false,"internalType":"address[]","name":"assetManagers","type":"address[]"}],"name":"TokensRegistered","type":"event"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"contract IWETH","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"enum IVault.SwapKind","name":"kind","type":"uint8"},{"components":[{"internalType":"bytes32","name":"poolId","type":"bytes32"},{"internalType":"uint256","name":"assetInIndex","type":"uint256"},{"internalType":"uint256","name":"assetOutIndex","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"userData","type":"bytes"}],"internalType":"struct IVault.BatchSwapStep[]","name":"swaps","type":"tuple[]"},{"internalType":"contract IAsset[]","name":"assets","type":"address[]"},{"components":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"bool","name":"fromInternalBalance","type":"bool"},{"internalType":"address payable","name":"recipient","type":"address"},{"internalType":"bool","name":"toInternalBalance","type":"bool"}],"internalType":"struct IVault.FundManagement","name":"funds","type":"tuple"},{"internalType":"int256[]","name":"limits","type":"int256[]"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"batchSwap","outputs":[{"internalType":"int256[]","name":"assetDeltas","type":"int256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"},{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"}],"name":"deregisterTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"address payable","name":"recipient","type":"address"},{"components":[{"internalType":"contract IAsset[]","name":"assets","type":"address[]"},{"internalType":"uint256[]","name":"minAmountsOut","type":"uint256[]"},{"internalType":"bytes","name":"userData","type":"bytes"},{"internalType":"bool","name":"toInternalBalance","type":"bool"}],"internalType":"struct IVault.ExitPoolRequest","name":"request","type":"tuple"}],"name":"exitPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IFlashLoanRecipient","name":"recipient","type":"address"},{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"userData","type":"bytes"}],"name":"flashLoan","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"selector","type":"bytes4"}],"name":"getActionId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAuthorizer","outputs":[{"internalType":"contract IAuthorizer","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getDomainSeparator","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"}],"name":"getInternalBalance","outputs":[{"internalType":"uint256[]","name":"balances","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getNextNonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPausedState","outputs":[{"internalType":"bool","name":"paused","type":"bool"},{"internalType":"uint256","name":"pauseWindowEndTime","type":"uint256"},{"internalType":"uint256","name":"bufferPeriodEndTime","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"}],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"enum IVault.PoolSpecialization","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"},{"internalType":"contract IERC20","name":"token","type":"address"}],"name":"getPoolTokenInfo","outputs":[{"internalType":"uint256","name":"cash","type":"uint256"},{"internalType":"uint256","name":"managed","type":"uint256"},{"internalType":"uint256","name":"lastChangeBlock","type":"uint256"},{"internalType":"address","name":"assetManager","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"}],"name":"getPoolTokens","outputs":[{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"internalType":"uint256[]","name":"balances","type":"uint256[]"},{"internalType":"uint256","name":"lastChangeBlock","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getProtocolFeesCollector","outputs":[{"internalType":"contract ProtocolFeesCollector","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"relayer","type":"address"}],"name":"hasApprovedRelayer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"components":[{"internalType":"contract IAsset[]","name":"assets","type":"address[]"},{"internalType":"uint256[]","name":"maxAmountsIn","type":"uint256[]"},{"internalType":"bytes","name":"userData","type":"bytes"},{"internalType":"bool","name":"fromInternalBalance","type":"bool"}],"internalType":"struct IVault.JoinPoolRequest","name":"request","type":"tuple"}],"name":"joinPool","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"enum IVault.PoolBalanceOpKind","name":"kind","type":"uint8"},{"internalType":"bytes32","name":"poolId","type":"bytes32"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct IVault.PoolBalanceOp[]","name":"ops","type":"tuple[]"}],"name":"managePoolBalance","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"enum IVault.UserBalanceOpKind","name":"kind","type":"uint8"},{"internalType":"contract IAsset","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct IVault.UserBalanceOp[]","name":"ops","type":"tuple[]"}],"name":"manageUserBalance","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"enum IVault.SwapKind","name":"kind","type":"uint8"},{"components":[{"internalType":"bytes32","name":"poolId","type":"bytes32"},{"internalType":"uint256","name":"assetInIndex","type":"uint256"},{"internalType":"uint256","name":"assetOutIndex","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"userData","type":"bytes"}],"internalType":"struct IVault.BatchSwapStep[]","name":"swaps","type":"tuple[]"},{"internalType":"contract IAsset[]","name":"assets","type":"address[]"},{"components":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"bool","name":"fromInternalBalance","type":"bool"},{"internalType":"address payable","name":"recipient","type":"address"},{"internalType":"bool","name":"toInternalBalance","type":"bool"}],"internalType":"struct IVault.FundManagement","name":"funds","type":"tuple"}],"name":"queryBatchSwap","outputs":[{"internalType":"int256[]","name":"","type":"int256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"enum IVault.PoolSpecialization","name":"specialization","type":"uint8"}],"name":"registerPool","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"},{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"internalType":"address[]","name":"assetManagers","type":"address[]"}],"name":"registerTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IAuthorizer","name":"newAuthorizer","type":"address"}],"name":"setAuthorizer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"paused","type":"bool"}],"name":"setPaused","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"relayer","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setRelayerApproval","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"bytes32","name":"poolId","type":"bytes32"},{"internalType":"enum IVault.SwapKind","name":"kind","type":"uint8"},{"internalType":"contract IAsset","name":"assetIn","type":"address"},{"internalType":"contract IAsset","name":"assetOut","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"userData","type":"bytes"}],"internalType":"struct IVault.SingleSwap","name":"singleSwap","type":"tuple"},{"components":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"bool","name":"fromInternalBalance","type":"bool"},{"internalType":"address payable","name":"recipient","type":"address"},{"internalType":"bool","name":"toInternalBalance","type":"bool"}],"internalType":"struct IVault.FundManagement","name":"funds","type":"tuple"},{"internalType":"uint256","name":"limit","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swap","outputs":[{"internalType":"uint256","name":"amountCalculated","type":"uint256"}],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
    contract = web3.eth.contract(address=address, abi=ABI)

    balances = contract.functions.getPoolTokens(poolId).call()

    return balances
