import os
import json
import re
import pandas as pd
import logging
from web3 import Web3
from threading import Thread
from datetime import datetime


# Define a Thread to listen separately on each contract/event in the contract file
class Listener(Thread):
    def __init__(self, web3, alert, contract, function, state_functions, webhook, **kwargs):
        super(Listener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.function = function
        self.state_functions = state_functions
        self.webhook = webhook
        self.event_filter = []

    def run(self):
        try:
            self.event_filter = eval(f"self.contract.events.{self.function}.createFilter(fromBlock='latest')")
            while True:
                for event in self.event_filter.get_new_entries():
                    print(str(datetime.now())+" Event found in "+str(self.alert)+"-"+str(self.contract.address)+"-"+str(self.function))
                    handle_event(event, self.web3, self.alert, self.contract, self.function, self.state_functions,self.webhook)
        except:
            print('Error in event ' + str(self.alert)+"-"+ str(self.contract.address)+"-"+ str(self.function))
            print('Check endpoint or alert parameters...')
            pass



# Define function to handle events and print to the console/send to discord
def handle_event(event, web3, alert, contract, function, state_functions, webhook):
    tx = json.loads(Web3.toJSON(event))
    #print(str(datetime.now())+" "+str(tx))
    results = []

    # Collect state function results
    for i in state_functions:

        state_result = eval(f'contract.functions.{i}.call()')
        results.append(state_result)

    # Build table
    state_results = pd.DataFrame([results])
    state_results = state_results.set_axis(state_functions, axis=1, inplace=False)

    # Print result table and go to trigger routine
    print(str(datetime.now())+" "+str(state_results))
    handle_trigger(alert, tx, function, state_results, webhook)


# Get an event and define if it sends a message or not to the appropriate webhook
def handle_trigger(alert, tx, function, state_results, webhook):
    send = True
    if (alert == 'dola3crv'):
        if (function =='RemoveLiquidity'):
            title = 'DOLA3CRV Pool ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected"
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Address : " + str(tx['address']) +
                    "\n" + "Sender : " + str(tx['args']['sender']) +
                    "\n" + "Receiver : " + str(tx['args']['receiver']) +
                    "\n" + "Value : " + str(tx['args']['value']/1e18) +
                    "\n" + "Total Supply : " + str(state_results.at[0, 'totalSupply()']/1e18) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
        elif (function == 'RemoveLiquidityOne'):
            title = 'DOLA3CRV Pool ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected"
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Address : " + str(tx['address']) +
                    "\n" + "Provider : " + str(tx['args']['provider']) +
                    "\n" + "Token Amount : " + str(tx['args']['token_amount']/1e18) +
                    "\n" + "Coin Amount : " + str(tx['args']['coin_amount']/1e18) +
                    "\n" + "Token Supply : " + str(tx['args']['token_supply']/1e18) +
                    #"\n" + "Total Supply : " + str(state_results.at[0, 'totalSupply()']/1e18) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
        elif (function == 'AddLiquidity'):
            title = 'DOLA3CRV Pool ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected"
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Address : " + str(tx['address']) +
                    "\n" + "Provider : " + str(tx['args']['provider']) +
                    "\n" + "Token 0 Amount : " + str(tx['args']['token_amounts'][0]/1e18) +
                    "\n" + "Token 1 Amount : " + str(tx['args']['token_amounts'][1]/1e18) +
                    "\n" + "Fees 0 Amount : " + str(tx['args']['fees'][0]/1e18) +
                    "\n" + "Fees 1 Amount : " + str(tx['args']['fees'][1]/1e18) +
                    "\n" + "Invariant : " + str(tx['args']['invariant']/1e18) +
                    "\n" + "Token Supply : " + str(tx['args']['token_supply']/1e18) +
                    #"\n" + "Total Supply : " + str(state_results.at[0, 'totalSupply()']/1e18) +
                    "\n" + "Balance 0 : " + str(state_results.at[0, 'balances(0)']/1e18) +
                    "\n" + "Balance 1 : " + str(state_results.at[0, 'balances(1)']/1e18) +
                    "\n" + "Address : " + str(tx['address']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
    elif (alert == 'lending'):
        if (function == 'Mint'):
            title = 'Lending Market : New ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected for " + str(state_results.at[0,'name()'])
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" +"Minter : " + str(tx['args']['minter']) +
                    "\n" +"Address : " + str(tx['address']) +
                    "\n" +"Mint Amount : " + str(tx['args']['mintAmount']) +
                    "\n" +"Mint Tokens : " + str(tx['args']['mintTokens']) +
                    "\n" +"Total Supply : " + str(state_results.at[0,'totalSupply()']) +
                    "\n" +"Total Cash : " + str(state_results.at[0,'getCash()']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
        elif (function == 'Redeem'):
            title = 'Lending Market : New ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected for " + str(state_results.at[0,'name()'])
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" +"Redeemer : " + str(tx['args']['redeemer']) +
                    "\n" +"Address : " + str(tx['address']) +
                    "\n" +"Redeem Amount : " + str(tx['args']['redeemAmount']) +
                    "\n" +"Redeem Tokens : " + str(tx['args']['redeemTokens']) +
                    "\n" +"Total Supply : " + str(state_results.at[0,'totalSupply()']) +
                    "\n" +"Total Cash : " + str(state_results.at[0,'getCash()']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
        elif (function == 'Borrow'):
            title = 'Lending Market : New ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected for " + str(state_results.at[0,'name()'])
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" +"Borrower : " + str(tx['args']['borrower']) +
                    "\n" +"Address : " + str(tx['address']) +
                    "\n" +"Borrow Amount : " + str(tx['args']['borrowAmount']) +
                    "\n" +"Account Borrows : " + str(tx['args']['accountBorrows']) +
                    "\n" +"Total Borrows : " + str(tx['args']['totalBorrows']) +
                    "\n" +"Total Supply : " + str(state_results.at[0,'totalSupply()']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
        elif (function == 'RepayBorrow'):
            title = 'Lending Market : New ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected for " + str(state_results.at[0,'name()'])
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" +"Payer : " + str(tx['args']['payer']) +
                    "\n" +"Address : " + str(tx['address']) +
                    "\n" +"Repaid Amount : " + str(tx['args']['repayAmount']) +
                    "\n" +"Account Borrows : " + str(tx['args']['accountBorrows']) +
                    "\n" +"Total Borrows : " + str(tx['args']['totalBorrows']) +
                    "\n" +"Total Supply : " + str(state_results.at[0,'totalSupply()']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
        elif (function == 'LiquidateBorrow'):
            title = 'Lending Market New : ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected for " + str(state_results.at[0,'name()'])
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" +"Liquidator : " + str(tx['args']['liquidator']) +
                    "\n" +"Borrower : " + str(tx['args']['borrower']) +
                    "\n" +"Address : " + str(tx['address']) +
                    "\n" +"Seized Token Address: " + str(tx['args']['cTokenCollateral']) +
                    "\n" +"Repay Amount : " + str(tx['args']['repayAmount']) +
                    "\n" +"Seized Tokens Amount : " + str(tx['args']['seizeTokens']) +
                    "\n" +"Total Supply : " + str(state_results.at[0,'totalSupply()']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
    elif (alert == 'governance'):
        if (function == 'ProposalCreated'):
            title = 'Governor Mills : New ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event']))
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Targets : " + str(tx['args']['targets']) +
                    "\n" + "Values : " + str(tx['args']['values']) +
                    "\n" + "Signatures : " + str(tx['args']['signatures']) +
                    "\n" + "Call Data : " + str(tx['args']['calldatas']) +
                    "\n" + "Description : " + str(tx['args']['description']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
        elif (function in ['ProposalCanceled', 'ProposalQueued', 'ProposalExecuted']):
            title = 'Governor Mills : New ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event']))
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Proposal Number : " + str(tx['args']['id']) +
                    "\n" + "Proposal : https://www.inverse.finance/governance/proposals/mills/" + str(tx['args']['id'])  +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
    elif (alert == 'fed'):
        if (function in ['Contraction','Expansion']):
            title = 'Fed ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected"
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Fed Address : " + str(tx['address']) +
                    "\n" + "Sender : " + str(tx['args']['amount']/1e18) +
                    "\n" + "Total Supply : " + str(state_results.at[0, 'supply()']/1e18) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
    elif (alert == 'sushi'):
        if (function == 'Swap'):
            title = 'Sushi New ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected"
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Address : " + str(tx['address']) +
                    "\n" + "Sender : " + str(tx['args']['sender']) +
                    "\n" + "To : " + str(tx['args']['to']) +
                    "\n" + "Amount0In : " + str(tx['args']['amount0In']/1e18) +
                    "\n" + "Amount0Out : " + str(tx['args']['amount0Out']/1e18) +
                    "\n" + "Amount1In : " + str(tx['args']['amount1In']/1e18) +
                    "\n" + "Amount1Out : " + str(tx['args']['amount1Out']/1e18) +
                    "\n" + "Symbol : " + str(state_results.at[0, 'symbol()']) +
                    "\n" + "Name : " + str(state_results.at[0, 'name()']) +
                    #"\n" + "price0CumulativeLast : " + str(state_results.at[0, 'price0CumulativeLast()']) +
                    #"\n" + "price1CumulativeLast : " + str(state_results.at[0, 'price1CumulativeLast()']) +
                    "\n" + "Token 0 : " + str(state_results.at[0, 'token0()']) +
                    "\n" + "Token 1 : " + str(state_results.at[0, 'token1()']) +
                    "\n" + "Total Supply : " + str(state_results.at[0, 'totalSupply()']/1e18) +
                    "\n" + "Total Reserves 0 : " + str(state_results.at[0, 'getReserves()'][0]/1e18) +
                    "\n" + "Total Reserves 1 : " + str(state_results.at[0, 'getReserves()'][1]/1e18) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
        elif (function in ['Mint']):
            title = 'Sushi New ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected"
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Address : " + str(tx['address']) +
                    "\n" + "Sender : " + str(tx['args']['sender']) +
                    "\n" + "To : " + str(tx['args']['to']) +
                    "\n" + "tokenA : " + str(tx['args']['tokenA']) +
                    "\n" + "tokenB : " + str(tx['args']['tokenB']) +
                    "\n" + "amountADesired : " + str(tx['args']['amountADesired']/1e18) +
                    "\n" + "amountBDesired : " + str(tx['args']['amountBDesired']/1e18) +
                    "\n" + "amountADesired : " + str(tx['args']['amountAMin']/1e18) +
                    "\n" + "amountBDesired : " + str(tx['args']['amountBMin']/1e18) +
                    #"\n" + "price0CumulativeLast : " + str(state_results.at[0, 'price0CumulativeLast()']) +
                    #"\n" + "price1CumulativeLast : " + str(state_results.at[0, 'price1CumulativeLast()']) +
                    "\n" + "Token 0 : " + str(state_results.at[0, 'token0()']) +
                    "\n" + "Token 1 : " + str(state_results.at[0, 'token1()']) +
                    "\n" + "Total Supply : " + str(state_results.at[0, 'totalSupply()']/1e18) +
                    "\n" + "Total Reserves 0 : " + str(state_results.at[0, 'getReserves()'][0]/1e18) +
                    "\n" + "Total Reserves 1 : " + str(state_results.at[0, 'getReserves()'][1]/1e18) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
        elif (function in ['Burn']):
            title = 'Sushi New ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected"
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Address : " + str(tx['address']) +
                    "\n" + "Sender : " + str(tx['args']['sender']) +
                    "\n" + "To : " + str(tx['args']['to']) +
                    "\n" + "Amount 0 : " + str(tx['args']['amount0']/1e18) +
                    "\n" + "Amount 1 : " + str(tx['args']['amount1']/1e18) +
                    "\n" + "Total Supply : " + str(state_results.at[0, 'totalSupply()']/1e18) +
                    "\n" + "Total Reserves 0 : " + str(state_results.at[0, 'getReserves()'][0]/1e18) +
                    "\n" + "Total Reserves 1 : " + str(state_results.at[0, 'getReserves()'][1]/1e18) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']))
    elif (alert == 'unitroller'):
        if (function in ['NewBorrowCap','NewSupplyCap','NewCollateralFactor','NewPriceOracle','MarketListed','MarketUnlisted']):
            title = 'Comptroller Markets ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected"
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Address : " + str(tx['address']) +
                    "\n" + "Comptroller : " + str(state_results.at[0, 'getAllMarkets()']) +
                    "\n" + "Comptroller : " + str(state_results.at[0, 'comptroller()']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + str(tx['transactionHash']) +
                    "\n" + "Transaction : " + str(tx))

    if (send ==True):
        message = title + "\n" + body

    # "\n" + "Tag Test <@578956365205209098>")

    webhook.send(message)

def getUnderlyingPrice(address, oracle_address):
    web3_oracle = Web3(Web3.HTTPProvider(os.getenv('LOCALHOST')))  # Or infura key
    address = web3_oracle.toChecksumAddress(address)
    oracle_name = web3_oracle.toChecksumAddress(oracle_address)
    oracle_ABI = json.loads(
        '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":false,"inputs":[{"internalType":"address","name":"owner_","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"feeds","outputs":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"uint8","name":"tokenDecimals","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"fixedPrices","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"contract CToken","name":"cToken_","type":"address"}],"name":"getUnderlyingPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"isPriceOracle","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"contract CToken","name":"cToken_","type":"address"}],"name":"removeFeed","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"contract CToken","name":"cToken_","type":"address"}],"name":"removeFixedPrice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"contract CToken","name":"cToken_","type":"address"},{"internalType":"address","name":"feed_","type":"address"},{"internalType":"uint8","name":"tokenDecimals_","type":"uint8"}],"name":"setFeed","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"contract CToken","name":"cToken_","type":"address"},{"internalType":"uint256","name":"price","type":"uint256"}],"name":"setFixedPrice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
    contract = web3_oracle.eth.contract(address=oracle_name, abi=oracle_ABI)

    price = contract.functions.getUnderlyingPrice(address).call()
    if (price == 0): price =1
    return price

def getDecimals(address):
    web3_oracle = Web3(Web3.HTTPProvider(os.getenv('LOCALHOST')))  # Or infura key
    address = web3_oracle.toChecksumAddress(address)
    ABI = json.loads(
        '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegator","type":"address"},{"indexed":true,"internalType":"address","name":"fromDelegate","type":"address"},{"indexed":true,"internalType":"address","name":"toDelegate","type":"address"}],"name":"DelegateChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegate","type":"address"},{"indexed":false,"internalType":"uint256","name":"previousBalance","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newBalance","type":"uint256"}],"name":"DelegateVotesChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnerChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DELEGATION_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"DOMAIN_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"abolishSeizing","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"addToWhitelist","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint32","name":"","type":"uint32"}],"name":"checkpoints","outputs":[{"internalType":"uint32","name":"fromBlock","type":"uint32"},{"internalType":"uint96","name":"votes","type":"uint96"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"closeTheGates","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"delegatee","type":"address"}],"name":"delegate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"delegatee","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"delegateBySig","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"delegates","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getCurrentVotes","outputs":[{"internalType":"uint96","name":"","type":"uint96"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"blockNumber","type":"uint256"}],"name":"getPriorVotes","outputs":[{"internalType":"uint96","name":"","type":"uint96"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"mint","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"numCheckpoints","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"openTheGates","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"removeFromWhitelist","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"seizable","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"src","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"seize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner_","type":"address"}],"name":"setOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"tradable","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"src","type":"address"},{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"rawAmount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"whitelist","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]')
    contract = web3_oracle.eth.contract(address=address, abi=ABI)

    decimals = contract.functions.decimals().call()
    decimals = eval(f'1e{decimals}')
    if (decimals == 0): decimals =1e18
    return decimals
