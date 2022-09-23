# import the following dependencies
import os
import json
import re
import fetchers
from threading import Thread
from web3 import Web3
from web3._utils.events import construct_event_topic_set
from datetime import datetime
import logging
from helpers import colors, sendError, sendWebhook, formatPercent, formatCurrency
from dotenv import load_dotenv
import requests
import pandas as pd
import sys

# Define state change to handle and logs to the console/send to discord
class HandleStateVariation(Thread):
    def __init__(self, web3,old_value,value, change, alert, contract, state_function, state_argument, **kwargs):
        super(HandleStateVariation, self).__init__(**kwargs)
        self.web3 = web3
        self.value = value
        self.change = change
        self.contract = contract
        self.alert = alert
        self.state_function = state_function
        self.state_argument = state_argument
        self.old_value = old_value

    def run(self):
        try:
            send = False
            image = ''
            content = ''
            webhook = ''
            title = ''
            fields = []
            color = colors.blurple
            level = 0
            if (self.alert == 'oracle'):
                webhook = os.getenv('WEBHOOK_MARKETS')
                if self.state_function == 'getUnderlyingPrice':
                    logging.info(str(self.change) + '% change detected on ' + str(
                        fetchers.getSymbol(self.web3,fetchers.getUnderlying(self.web3,self.state_argument))))
                    title = str(formatPercent(self.change)) + ' change detected on ' + str(
                        fetchers.getSymbol(self.web3,fetchers.getUnderlying(self.web3,self.state_argument))) + ' Oracle'

                    if abs(self.change) > 0.2:
                        content = '<@&945071604642222110>'
                        level = 3
                        color = colors.red
                        send = True
                    elif abs(self.change) > 0.1:
                        level = 2
                        color = colors.dark_orange
                        send = True
                    elif abs(self.change) > 0.05:
                        level = 1
                        color = colors.orange
                        send = True
                    if send:
                        fields = [{"name": 'Alert Level :',"value": str(level),"inline": True},
                                  {"name": 'Variation :', "value": str(formatPercent(self.change)),"inline": True},
                                  {"name": 'Old Value :', "value": str(formatCurrency(self.old_value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.state_argument)))), "inline": True},
                                  {"name": 'New Value :', "value": str(formatCurrency(self.value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.state_argument)))), "inline": True},
                                  {"name": 'Link to Market :', "value": 'https://etherscan.io/address/' + str(self.state_argument), "inline": False}]


            if (self.alert == 'cash'):
                webhook = os.getenv('WEBHOOK_MARKETS')
                if self.state_function == 'getCash':
                    logging.info(str(self.change) + '% change detected on ' + str(
                        fetchers.getName(self.web3,self.contract.address)) + ' balance')
                    title = str(formatPercent(self.change)) + ' change detected on ' + str(
                        fetchers.getSymbol(self.web3,fetchers.getUnderlying(self.web3,self.contract.address))) + ' Cash balance'

                    if abs(self.change) > 0.2:
                        content = '<@&945071604642222110>'
                        level = 3
                        color = colors.red
                        send = True
                    elif abs(self.change) > 0.1:
                        level = 2
                        color = colors.dark_orange
                        send = True
                    elif abs(self.change) > 0.05:
                        level = 1
                        color = colors.orange
                        send = True

                    if send:
                        fields = [{"name": 'Alert Level :',"value": str(level),"inline": True},
                                  {"name": 'Variation :',"value": str(formatPercent(self.change)), "inline" : True},
                                  {"name": 'Old Value :',"value": str(formatCurrency(self.old_value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.contract.address)))), "inline" : True},
                                  {"name": 'New Value :',"value": str(formatCurrency(self.value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.contract.address)))), "inline" : True},
                                  {"name": 'Link to Market :',"value":'https://etherscan.io/address/' + str(self.contract.address), "inline" : False}]


            if (self.alert == 'supply'):
                webhook = os.getenv('WEBHOOK_DOLA3CRV')
                if self.state_function == 'totalSupply':
                    logging.info(str(self.change) + '% change detected on ' + str(
                        fetchers.getName(self.web3,self.contract.address))+ ' total supply')
                    title = str(formatPercent(self.change)) + ' change detected on ' + str(
                        fetchers.getSymbol(self.web3,fetchers.getUnderlying(self.web3,self.state_argument))) + ' Supply'

                    if abs(self.change) > 0.015:
                        content = '<@&945071604642222110>'
                        level = 3
                        color = colors.red
                        send = True
                    elif abs(self.change) > 0.01:
                        level = 2
                        color = colors.dark_orange
                        send = True
                    elif abs(self.change) > 0.005:
                        level = 1
                        color = colors.orange
                        send = True
                    if send:
                        fields = [{"name":'Alert Level :',"value":str(level),"inline": True},
                        {"name":'Variation :', "value":str(formatPercent(self.change)), "inline": True},
                        {"name":'Old Value :', "value":str(formatCurrency(self.old_value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.contract.address)))), "inline": True},
                        {"name":'New Value :', "value":str(formatCurrency(self.value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.contract.address)))), "inline": True},
                        {"name":'Link to Pool :', "value":'https://etherscan.io/address/' + str(self.contract.address), "inline": False}]

            if (self.alert == 'liquidation_incentive'):
                webhook = os.getenv('WEBHOOK_MARKETS')
                if self.state_function == 'liquidationIncentiveMantissa':
                    logging.info(str(self.change) + '% change detected on ' + str(
                        fetchers.getName(self.web3,self.contract.address))+ ' Liquidation incentive')
                    title = str(formatPercent(self.change)) + ' change detected on ' + str(
                        fetchers.getSymbol(self.web3,fetchers.getUnderlying(self.web3,self.state_argument))) + ' Liquidation incentive'

                    content = '<@&945071604642222110>'
                    level = 3
                    color = colors.red
                    send = True

                    fields = [{"name": 'Alert Level :',"value": str(level),"inline": True},
                    {"name": 'Variation :',"value": str(formatPercent(self.change)),"inline": True},
                    {"name": 'Old Value :',"value": str(formatCurrency(self.old_value / 1e18)),"inline": True},
                    {"name": 'New Value :',"value":str(formatCurrency(self.value / 1e18)),"inline": True},
                    {"name": 'Link to Pool :',"value":'https://etherscan.io/address/' + str(self.contract.address),"inline": False}]

            if send:
                sendWebhook(webhook, title, fields, content, image, color)


        except Exception as e:
            logging.warning(f'Error in state variation handler')
            logging.error(e)
            #sendError(f'Error in state variation handler : {str(e)}')
            pass

# Define event to handle and logs to the console/send to discord
class HandleEvent(Thread):
    def __init__(self, web3,event, alert, event_name, **kwargs):
        super(HandleEvent, self).__init__(**kwargs)
        self.web3 = web3
        self.event = event
        self.alert = alert
        self.event_name = event_name

    def run(self):
        try:
            tx = json.loads(Web3.toJSON(self.event))

            # logs result table and start writing message
            logging.info(str(datetime.now()) + " " + str(tx))
            send = False
            title = ''
            content= ''
            fields = []
            image = ''
            color = colors.blurple

            webhook = ''


            if (self.alert == "curve_liquidity"):
                pool_address = tx["address"]

                if pool_address=="0xAA5A67c256e27A5d80712c51971408db3370927D":
                    webhook = os.getenv('WEBHOOK_DOLA3CRV')
                    token_0 = 'DOLA'
                    token_1 = '3CRV'
                    token_0_address = '0x865377367054516e17014CcdED1e7d814EDC9ce4'
                    token_1_address = '0x6c3f90f043a72fa612cbac8115ee7e52bde6e490'
                    token_0_total = fetchers.getBalance(self.web3,pool_address,token_0_address)
                    token_1_total = fetchers.getBalance(self.web3, pool_address, token_1_address)
                    image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/833844/1457892/c8141b30-aa8c-4588-8d42-877ce649abee.jpg"
                elif pool_address=="0xE57180685E3348589E9521aa53Af0BCD497E884d":
                    webhook = os.getenv('WEBHOOK_DOLAFRAXBP')
                    token_0 = 'DOLA'
                    token_1 = 'crvFRAX'
                    token_0_address = '0x865377367054516e17014CcdED1e7d814EDC9ce4'
                    token_1_address = '0x3175Df0976dFA876431C2E9eE6Bc45b65d3473CC'
                    token_0_total = fetchers.getBalance(self.web3,pool_address,token_0_address)
                    token_1_total = fetchers.getBalance(self.web3, pool_address, token_1_address)
                    image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/1300762/2228671/f10870d8-4e95-474d-a47a-d75b05cd2a99.jpg"

                if (self.event_name == "RemoveLiquidity"):
                    if (tx["args"]["token_amounts"][0] + tx["args"]["token_amounts"][1]) / 1e18 > 500000:
                        content = '<@&945071604642222110>'
                    color = colors.red
                    send = True
                    title = token_0 + token_1+ " Pool Liquidity Removal event detected"
                    fields = [{"name":'Block :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name": token_0+' Amount :',"value":str(formatCurrency(tx["args"]["token_amounts"][0] / 1e18)),"inline":True},
                    {"name":token_1+' Amount :',"value":str(formatCurrency(tx["args"]["token_amounts"][1] / 1e18)),"inline":True},
                    {"name":'Address :',"value":str(tx["address"]),"inline":False},
                    {"name":token_0+' in Pool :',"value":str(formatCurrency(token_0_total)),"inline":True},
                    {"name":token_1+' in Pool :',"value":str(formatCurrency(token_1_total)),"inline":True},
                    {"name":token_0+'+'+token_1+' in Pool',"value":str(formatCurrency(token_0_total + token_1_total)),"inline":False},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                elif (self.event_name == "RemoveLiquidityOne" ):
                    if tx["args"]["coin_amount"] / 1e18 > 500000:
                        content = '<@&945071604642222110>'
                    color = colors.red
                    send = True
                    title = token_0+token_1+" Pool Liquidity Removal event detected"
                    fields = [
                    {"name":'Block :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Token Amount :',"value":str(formatCurrency(tx["args"]["coin_amount"] / 1e18)),"inline":True},
                    {"name":token_0+' in Pool :',"value":str(formatCurrency(token_0_total)),"inline":True},
                    {"name":token_1+' in Pool :',"value":str(formatCurrency(token_1_total)),"inline":True},
                    {"name":token_0+'+'+token_1+' in Pool',"value":str(formatCurrency(token_0_total + token_1_total)),"inline":False},
                    {"name": 'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]
                elif (self.event_name == "AddLiquidity"):
                    if (tx["args"]["token_amounts"][0] + tx["args"]["token_amounts"][1]) / 1e18 > 500000:
                        content = '<@&945071604642222110>'

                    title = token_0+token_1+" Pool Liquidity Add event detected"
                    fields = [{"name":'Block :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":token_0+' Amount :',"value":str(formatCurrency(tx["args"]["token_amounts"][0] / 1e18)),"inline":True},
                    {"name":token_1+' Amount :',"value":str(formatCurrency(tx["args"]["token_amounts"][1] / 1e18)),"inline":True},
                    {"name":'Address :',"value":str(tx["address"]),"inline":True},
                    {"name":token_0+' in Pool :',"value":str(formatCurrency(token_0_total)),"inline":True},
                    {"name":token_1+' in Pool :',"value":str(formatCurrency(token_1_total)),"inline":True},
                    {"name":token_0+'+'+token_1+' in Pool',"value":str(formatCurrency(token_0_total + token_1_total)),"inline":False},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    color = colors.dark_green
                    send = True
            elif (self.alert == "gauge_controller"):
                if tx["args"]["gauge_addr"]=="0xBE266d68Ce3dDFAb366Bb866F4353B6FC42BA43c":
                    webhook = os.getenv('WEBHOOK_DOLAFRAXBP')
                    pool_address="0xE57180685E3348589E9521aa53Af0BCD497E884d"
                    token_0 = 'DOLA'
                    token_1 = 'crvFRAX'
                    token_0_address = '0x865377367054516e17014CcdED1e7d814EDC9ce4'
                    token_1_address = '0x3175Df0976dFA876431C2E9eE6Bc45b65d3473CC'
                    token_0_total = fetchers.getBalance(self.web3,pool_address,token_0_address)
                    token_1_total = fetchers.getBalance(self.web3, pool_address, token_1_address)

                elif tx["args"]["gauge_addr"]=="0x8Fa728F393588E8D8dD1ca397E9a710E53fA553a":
                    webhook = os.getenv('WEBHOOK_DOLA3CRV')
                    pool_address = "0xAA5A67c256e27A5d80712c51971408db3370927D"
                    token_0 = 'DOLA'
                    token_1 = '3CRV'
                    token_0_address = '0x865377367054516e17014CcdED1e7d814EDC9ce4'
                    token_1_address = '0x6c3f90f043a72fa612cbac8115ee7e52bde6e490'
                    token_0_total = fetchers.getBalance(self.web3,pool_address,token_0_address)
                    token_1_total = fetchers.getBalance(self.web3, pool_address, token_1_address)


                if (self.event_name == "NewGaugeWeight"):
                    title = token_0+token_1+" New Gauge Weight detected"
                    fields = [{"name":'Block :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Gauge Address :',"value":str(tx["args"]["gauge_addr"]),"inline":False},
                    {"name":'Weight :',"value":str(tx["args"]["weight"]),"inline":False},
                    {"name": 'Total Weight :',"value":str(tx["args"]["total_weight"]),"inline":False},
                    {"name": 'Address :', "value": str(tx["address"]), "inline": True},
                    {"name":token_0+' in Pool :',"value":str(formatCurrency(token_0_total)),"inline":True},
                    {"name":token_1+' in Pool :',"value":str(formatCurrency(token_1_total)),"inline":True},
                    {"name":token_0+'+'+token_1+' in Pool',"value":str(formatCurrency(token_0_total + token_1_total)),"inline":False},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    content = '<@&945071604642222110>'
                    color = colors.dark_green
                    send = True
                elif (self.event_name == "VoteForGauge"):
                    title = token_0+token_1+" Pool Vote For Gauge detected"
                    fields = [{"name":'Block :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'User :',"value":str(tx["args"]["user"]),"inline":False},
                    {"name":'Gauge Address :',"value":str(tx["args"]["gauge_addr"]),"inline":False},
                    {"name":'Weight :',"value":str(tx["args"]["weight"]),"inline":False},
                    {"name": 'Address :', "value": str(tx["address"]), "inline": True},
                    {"name":token_0+' in Pool :',"value":str(formatCurrency(token_0_total)),"inline":True},
                    {"name":token_1+' in Pool :',"value":str(formatCurrency(token_1_total)),"inline":True},
                    {"name":token_0+'+'+token_1+' in Pool',"value":str(formatCurrency(token_0_total + token_1_total)),"inline":False},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    content = '<@&945071604642222110>'
                    color = colors.dark_green
                    send = True

            elif (self.alert in ["lending1", "lending2"]):
                if (self.event_name == "Mint"):
                    webhook = os.getenv('WEBHOOK_SUPPLY')
                    title = "Lending Market : New Deposit event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Minter :',"value":str(tx["args"]["minter"]),"inline":True},
                    {"name":'Market Symbol :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":True},
                    {"name":'Market Address :',"value":str(tx["address"]),"inline":False},
                    {"name":'USD Value',"value":str(formatCurrency(tx["args"]["mintAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"]))),"inline":True},
                    {"name":'Mint Amount :',"value":str(formatCurrency(tx["args"]["mintAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])))),"inline":True},
                    {"name":'Mint Tokens :',"value":str(formatCurrency(tx["args"]["mintTokens"] / fetchers.getDecimals(self.web3,tx["address"]))),"inline":True},
                    {"name":'Total Supply',"value":str(formatCurrency(fetchers.getSupply(self.web3,tx["address"]))),"inline":True},
                    {"name":'Total Cash :',"value":str(formatCurrency(fetchers.getCash(self.web3,tx["address"]))),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    if ((tx["args"]["mintAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"]))>100000):
                        content = '<@&945071604642222110>'
                    color = colors.blurple
                    send = True
                elif (self.event_name == "Redeem"):
                    webhook = os.getenv('WEBHOOK_SUPPLY')
                    title = "Lending Market : New Withdrawal event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Redeemer :',"value":str(tx["args"]["redeemer"]),"inline":True},
                    {"name":'Market Symbol :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":True},
                    {"name":'Market Address :',"value":str(tx["address"]),"inline":False},
                    {"name":'USD Value',"value":str(formatCurrency(tx["args"]["redeemAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"]))),"inline":True},
                    {"name":'Redeem Amount :',"value":str(formatCurrency(tx["args"]["redeemAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])))),"inline":True},
                    {"name":'Redeem Tokens :',"value":str(formatCurrency(tx["args"]["redeemTokens"] / fetchers.getDecimals(self.web3,tx["address"]))),"inline":True},
                    {"name":'Total Supply',"value":str(formatCurrency(fetchers.getSupply(self.web3,tx["address"]))),"inline":True},
                    {"name":'Total Cash :',"value":str(formatCurrency(fetchers.getCash(self.web3,tx["address"]))),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    if ((tx["args"]["redeemAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"]))>100000):
                        content = '<@&945071604642222110>'

                    color = colors.blurple
                    send = True
                elif (self.event_name == "Borrow"):
                    webhook = os.getenv('WEBHOOK_BORROW')
                    title = "Lending Market : New Borrow event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Borrower :',"value":str(tx["args"]["borrower"]),"inline":True},
                    {"name":'Market Symbol :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":False},
                    {"name":'Market Address :',"value":str(tx["address"]),"inline":True},
                    {"name":'USD Value :',"value":str(formatCurrency(tx["args"]["borrowAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"]))),"inline":True},
                    {"name":'Borrow Amount :',"value":str(formatCurrency(tx["args"]["borrowAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])))),"inline":True},
                    {"name":'Account Borrows :',"value":str(formatCurrency(tx["args"]["accountBorrows"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])))),"inline":True},
                    {"name":'Total Borrows :',"value":str(formatCurrency(tx["args"]["totalBorrows"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])))),"inline":True},
                    {"name":'Total Supply :',"value":str(formatCurrency(fetchers.getSupply(self.web3,tx["address"]))),"inline":True},
                    {"name":'Total Cash :',"value":str(formatCurrency(fetchers.getCash(self.web3,tx["address"]))),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]


                    if ((tx["args"]["borrowAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"]))>100000):
                        content = '<@&945071604642222110>'

                    color = colors.blurple
                    send = True
                elif (self.event_name == "RepayBorrow"):
                    webhook = os.getenv('WEBHOOK_BORROW')
                    title = "Lending Market : New Repayment event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Borrower :',"value":str(tx["args"]["borrower"]),"inline":True},
                    {"name":'Market Symbol :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":False},
                    {"name":'Market Address :',"value":str(tx["address"]),"inline":True},
                    {"name":'USD Value :',"value":str(formatCurrency(tx["args"]["repayAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"]))),"inline":True},
                    {"name": 'Borrow Amount :',"value":str(formatCurrency(tx["args"]["repayAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])))),"inline":True},
                    {"name":'Account Borrows :',"value":str(formatCurrency(tx["args"]["accountBorrows"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])))),"inline":True},
                    {"name":'Total Borrows :',"value":str(formatCurrency(tx["args"]["totalBorrows"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])))),"inline":True},
                    {"name":'Total Supply :',"value":str(formatCurrency(fetchers.getSupply(self.web3,tx["address"]))),"inline":True},
                    {"name":'Total Cash :',"value":str(formatCurrency(fetchers.getCash(self.web3,tx["address"]))),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    if ((tx["args"]["repayAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"]))>100000):
                        content = '<@&945071604642222110>'

                    color = colors.blurple
                    send = True
                elif (self.event_name == "LiquidateBorrow"):
                    title = "Lending Market New Liquidation event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    webhook = os.getenv('WEBHOOK_LIQUIDATIONS')
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                    {"name":'Liquidator :',"value":str(tx["args"]["liquidator"]),"inline":False},
                    {"name":'Borrower :',"value":str(tx["args"]["borrower"]),"inline":False},
                    {"name":'Market Address :',"value":str(tx["address"]),"inline":False},
                    {"name":'Seized Amount :',"value":str(formatCurrency(tx["args"]["seizeTokens"]/ fetchers.getDecimals(self.web3,tx["args"]["cTokenCollateral"]))),"inline":True},
                    {"name":'Seized Token  :',"value":str(fetchers.getSymbol(self.web3,tx["args"]["cTokenCollateral"])),"inline":True},
                    {"name":'Repay Amount :',"value":str(formatCurrency(tx["args"]["repayAmount"]/ fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])))),"inline":False},
                    {"name":'Repay Amount USD:',"value":str(formatCurrency(tx["args"]["repayAmount"]* fetchers.getUnderlyingPrice(self.web3,tx["address"])/ fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])))),"inline":True},
                    {"name":'Repay Token  :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    if ((tx["args"]["repayAmount"]/ fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])))>100000):
                        content = '<@&945071604642222110>'

                    color = colors.blurple
                    send = True
            elif (self.alert in ["lendingfuse127"]):
                if (self.event_name == "Mint"):
                    webhook = os.getenv('WEBHOOK_127')
                    title = "Lending Market : New Deposit event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Minter :',"value":str(tx["args"]["minter"]),"inline":True},
                    {"name":'Market Symbol :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":True},
                    {"name":'Market Address :',"value":str(tx["address"]),"inline":False},
                    {"name":'ETH Value',"value":str(formatCurrency(tx["args"]["mintAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])) * fetchers.getUnderlyingPriceFuse(self.web3,tx["address"]))),"inline":True},
                    {"name":'Mint Amount :',"value":str(formatCurrency(tx["args"]["mintAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])))),"inline":True},
                    {"name":'Mint Tokens :',"value":str(formatCurrency(tx["args"]["mintTokens"] / fetchers.getDecimals(self.web3,tx["address"]))),"inline":True},
                    {"name":'Total Supply',"value":str(formatCurrency(fetchers.getSupply(self.web3,tx["address"]))),"inline":True},
                    {"name":'Total Cash :',"value":str(formatCurrency(fetchers.getCash(self.web3,tx["address"]))),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    if ((tx["args"]["mintAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])) * fetchers.getUnderlyingPriceFuse(self.web3,tx["address"]))>100000):
                        content = '<@&945071604642222110>'
                    color = colors.blurple
                    send = True
                elif (self.event_name == "Redeem"):
                    webhook = os.getenv('WEBHOOK_127')
                    title = "Lending Market : New Withdrawal event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Redeemer :',"value":str(tx["args"]["redeemer"]),"inline":True},
                    {"name":'Market Symbol :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":True},
                    {"name":'Market Address :',"value":str(tx["address"]),"inline":False},
                    {"name":'ETH Value',"value":str(formatCurrency(tx["args"]["redeemAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])) * fetchers.getUnderlyingPriceFuse(self.web3,tx["address"]))),"inline":True},
                    {"name":'Redeem Amount :',"value":str(formatCurrency(tx["args"]["redeemAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])))),"inline":True},
                    {"name":'Redeem Tokens :',"value":str(formatCurrency(tx["args"]["redeemTokens"] / fetchers.getDecimals(self.web3,tx["address"]))),"inline":True},
                    {"name":'Total Supply',"value":str(formatCurrency(fetchers.getSupply(self.web3,tx["address"]))),"inline":True},
                    {"name":'Total Cash :',"value":str(formatCurrency(fetchers.getCash(self.web3,tx["address"]))),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    if ((tx["args"]["redeemAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])) * fetchers.getUnderlyingPriceFuse(self.web3,tx["address"]))>100000):
                        content = '<@&945071604642222110>'

                    color = colors.blurple
                    send = True
                elif (self.event_name == "Borrow"):
                    webhook = os.getenv('WEBHOOK_127')
                    title = "Lending Market : New Borrow event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Borrower :',"value":str(tx["args"]["borrower"]),"inline":True},
                    {"name":'Market Symbol :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":False},
                    {"name":'Market Address :',"value":str(tx["address"]),"inline":True},
                    {"name":'ETH Value :',"value":str(formatCurrency(tx["args"]["borrowAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])) * fetchers.getUnderlyingPriceFuse(self.web3,tx["address"]))),"inline":True},
                    {"name":'Borrow Amount :',"value":str(formatCurrency(tx["args"]["borrowAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])))),"inline":True},
                    {"name":'Account Borrows :',"value":str(formatCurrency(tx["args"]["accountBorrows"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])))),"inline":True},
                    {"name":'Total Borrows :',"value":str(formatCurrency(tx["args"]["totalBorrows"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])))),"inline":True},
                    {"name":'Total Supply :',"value":str(formatCurrency(fetchers.getSupply(self.web3,tx["address"]))),"inline":True},
                    {"name":'Total Cash :',"value":str(formatCurrency(fetchers.getCash(self.web3,tx["address"]))),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]


                    if ((tx["args"]["borrowAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])) * fetchers.getUnderlyingPriceFuse(self.web3,tx["address"]))>100000):
                        content = '<@&945071604642222110>'

                    color = colors.blurple
                    send = True
                elif (self.event_name == "RepayBorrow"):
                    webhook = os.getenv('WEBHOOK_127')
                    title = "Lending Market : New Repayment event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Borrower :',"value":str(tx["args"]["borrower"]),"inline":True},
                    {"name":'Market Symbol :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":False},
                    {"name":'Market Address :',"value":str(tx["address"]),"inline":True},
                    {"name":'ETH Value :',"value":str(formatCurrency(tx["args"]["repayAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])) * fetchers.getUnderlyingPriceFuse(self.web3,tx["address"]))),"inline":True},
                    {"name":'Borrow Amount :',"value":str(formatCurrency(tx["args"]["repayAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])))),"inline":True},
                    {"name":'Account Borrows :',"value":str(formatCurrency(tx["args"]["accountBorrows"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])))),"inline":True},
                    {"name":'Total Borrows :',"value":str(formatCurrency(tx["args"]["totalBorrows"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])))),"inline":True},
                    {"name":'Total Supply :',"value":str(formatCurrency(fetchers.getSupply(self.web3,tx["address"]))),"inline":True},
                    {"name":'Total Cash :',"value":str(formatCurrency(fetchers.getCash(self.web3,tx["address"]))),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    if ((tx["args"]["repayAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])) * fetchers.getUnderlyingPriceFuse(self.web3,tx["address"]))>100000):
                        content = '<@&945071604642222110>'

                    color = colors.blurple
                    send = True
                elif (self.event_name == "LiquidateBorrow"):
                    title = "Lending Market New Liquidation event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    webhook = os.getenv('WEBHOOK_127')
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                    {"name":'Liquidator :',"value":str(tx["args"]["liquidator"]),"inline":False},
                    {"name":'Borrower :',"value":str(tx["args"]["borrower"]),"inline":False},
                    {"name":'Market Address :',"value":str(tx["address"]),"inline":False},
                    {"name":'Seized Amount :',"value":str(formatCurrency(tx["args"]["seizeTokens"]/ fetchers.getDecimals(self.web3,tx["args"]["cTokenCollateral"]))),"inline":True},
                    {"name":'Seized Token  :',"value":str(fetchers.getSymbol(self.web3,tx["args"]["cTokenCollateral"])),"inline":True},
                    {"name":'Repay Amount :',"value":str(formatCurrency(tx["args"]["repayAmount"]/ fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])))),"inline":False},
                    {"name":'Repay Amount ETH:',"value":str(formatCurrency(tx["args"]["repayAmount"]* fetchers.getUnderlyingPriceFuse(self.web3,tx["address"])/ fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])))),"inline":True},
                    {"name":'Repay Token  :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    if ((tx["args"]["repayAmount"]/ fetchers.getDecimals(self.web3,fetchers.getUnderlyingFuse(self.web3,tx["address"])))>100000):
                        content = '<@&945071604642222110>'

                    color = colors.blurple
                    send = True

            elif (self.alert == "governance"):
                content = "<@&899302193608409178>"
                webhook = os.getenv('WEBHOOK_GOVERNANCE')
                if (self.event_name == "ProposalCreated"):
                    title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"]))

                    fields = [{"name":'Block Number :', "value":str(tx["blockNumber"]), "inline": False},
                    {"name":'Proposal :', "value":"https://www.inverse.finance/governance/proposals/mills/" + str(fetchers.getProposalCount(self.web3)), "inline": False},
                    {"name":'Transaction :', "value":"https://etherscan.io/tx/" + str(tx["transactionHash"]), "inline": False}]

                    color = colors.blurple
                    send = True
                elif (self.event_name in ["ProposalCanceled"]):
                    title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"]))
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                    {"name":'Proposal :',"value":"https://www.inverse.finance/governance/proposals/mills/" + str(tx["args"]["id"]),"inline":False},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    color = colors.dark_red
                    send = True
                elif (self.event_name in ["ProposalQueued"]):
                    title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",str(tx["event"]))
                    fields = [{"name": 'Block Number :', "value": str(tx["blockNumber"]), "inline": False},
                              {"name": 'Proposal :',"value": "https://www.inverse.finance/governance/proposals/mills/" + str(tx["args"]["id"]), "inline": False},
                              {"name": 'Transaction :',"value": "https://etherscan.io/tx/" + str(tx["transactionHash"]), "inline": False}]


                    color = colors.blurple
                    send = True
                elif (self.event_name in ["ProposalExecuted"]):
                    title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",str(tx["event"]))
                    fields = [{"name": 'Block Number :', "value": str(tx["blockNumber"]), "inline": False},
                              {"name": 'Proposal :',"value": "https://www.inverse.finance/governance/proposals/mills/" + str( tx["args"]["id"]), "inline": False},
                              {"name": 'Transaction :',"value": "https://etherscan.io/tx/" + str(tx["transactionHash"]), "inline": False}]
                    color = colors.dark_green
                    send = True
            elif (self.alert == "fed"):
                webhook = os.getenv('WEBHOOK_FED')
                image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/22517/1128427/3084f915-b906-4fdf-ac8c-ad5c0ce57e2b.jpg"

                if (self.event_name in ["Expansion"]):
                    title = "Fed " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                    {"name":'Fed Address :',"value":str(tx["address"]),"inline":False},
                    {"name":'Amount :',"value": str(formatCurrency(tx["args"]["amount"] / 1e18)),"inline":True},
                    {"name":'Total Supply :',"value":str(formatCurrency(fetchers.getSupply(self.web3,'0x865377367054516e17014ccded1e7d814edc9ce4') / 1e18)),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                    color = colors.dark_red
                    send = True
                if (self.event_name in ["Contraction"]):
                    title = "Fed " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"

                    fields = f'''makeFields([
                    'Block Number :',
                    'Fed Address :',
                    'Amount :',
                    'Total Supply :',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(tx["address"])}',
                    '{str(formatCurrency(tx["args"]["amount"] / 1e18))}',
                    '{str(formatCurrency(fetchers.getSupply(self.web3,'0x865377367054516e17014ccded1e7d814edc9ce4') / 1e18))}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [False,False,True,True,False])'''

                    color = colors.dark_green
                    send = True
            elif (self.alert == "swap"):
                webhook = os.getenv('WEBHOOK_SWAP')
                if (self.event_name == "Swap"):
                    image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/838610/1466237/8e64e858-5db5-4692-922d-5f9fe6b7a8c6.jpg"
                    if tx["args"]['amount0In'] == 0:
                        operation = 'Buy ' + str(formatCurrency(tx["args"]['amount0Out'] / fetchers.getDecimals(self.web3,
                            fetchers.getSushiTokens(self.web3,tx["address"])[0]))) + " " + str(
                            fetchers.getSushiTokensSymbol(self.web3,tx["address"])[0])
                        color = colors.dark_green
                        title = "Sushiswap New Buy event detected"
                        send = True
                    else:
                        operation = 'Sell ' + str(formatCurrency(tx["args"]['amount0In'] / fetchers.getDecimals(self.web3,
                            fetchers.getSushiTokens(self.web3,tx["address"])[0]))) + " " + str(
                            fetchers.getSushiTokensSymbol(self.web3,tx["address"])[0])
                        color = colors.dark_red
                        title = "Sushiswap New Sell event detected"
                        send = True

                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Name :',"value":str(fetchers.getName(self.web3,tx["address"])),"inline":True},
                    {"name":'Symbol :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":True},
                    {"name":'Address :',"value":str(tx["address"]),"inline":True},
                    {"name":'Operation :',"value":str(operation),"inline":True},
                    {"name":'USD value :',"value":str(formatCurrency(((tx["args"]["amount0Out"] + tx["args"]["amount0In"]) / fetchers.getDecimals(self.web3,fetchers.getSushiTokens(self.web3,tx["address"])[0])) * fetchers.getUnderlyingPrice(self.web3,'0x1637e4e9941d55703a7a5e7807d6ada3f7dcd61b'))),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":True}]

                elif (self.event_name in ["Mint"]):
                    title = "Sushi New Liquidity Add event detected"
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Name :',"value":str(fetchers.getName(self.web3,tx["address"])),"inline":True},
                    {"name":'Symbol :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":True},
                    {"name":'Address :',"value":str(tx["address"]),"inline":False},
                    {"name":'amountADesired :',"value":str(tx["args"]["amountADesired"] / 1e18),"inline":True},
                    {"name":'amountBDesired :',"value":str(tx["args"]["amountBDesired"] / 1e18),"inline":True},
                    {"name":'amountAMin :',"value":str(tx["args"]["amountAMin"] / 1e18),"inline":False},
                    {"name":'amountBMin :',"value":str(tx["args"]["amountBMin"] / 1e18),"inline":True},
                    {"name":'Token 0 :',"value":str(fetchers.getBalance(self.web3,tx["address"], fetchers.getSushiTokens(self.web3,tx["address"][0]))),"inline":False},
                    {"name":'Token 1 :',"value":str(fetchers.getBalance(self.web3,tx["address"], fetchers.getSushiTokens(self.web3,tx["address"][1]))),"inline":True},
                    {"name":'Total Supply :',"value":str(fetchers.getSupply(self.web3,tx["address"])),"inline":False},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]


                    color = colors.dark_green
                    send = True
                elif (self.event_name in ["Burn"]):
                    title = "Sushi New Liquidity Removal detected"

                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":True},
                    {"name":'Name :',"value":str(fetchers.getName(self.web3,tx["address"])) ,"inline":True},
                    {"name":'Symbol :',"value":str(fetchers.getSymbol(self.web3,tx["address"])),"inline":False},
                    {"name":'Address :',"value":str(tx["address"]),"inline":True},
                    {"name":'Amount 0 :',"value":str(tx["args"]["amount0"] / 1e18),"inline":True},
                    {"name":'Amount 1 :',"value":str(tx["args"]["amount1"] / 1e18),"inline":True},
                    {"name":'Total Reserves 0 :',"value":str(fetchers.getBalance(self.web3,tx["address"], fetchers.getSushiTokens(self.web3,tx["address"][0]))),"inline":True},
                    {"name":'Total Reserves 1 :',"value":str(fetchers.getBalance(self.web3,tx["address"], fetchers.getSushiTokens(self.web3,tx["address"][1]))),"inline":True},
                    {"name":'Total Supply :',"value":str(fetchers.getSupply(self.web3,tx["address"])),"inline":True},
                    {"name": 'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]
                    color = colors.dark_red
                    send = True
            elif (self.alert == "unitroller"):
                webhook = os.getenv('WEBHOOK_UNITROLLER')
                if (self.event_name in ["NewBorrowCap", "NewSupplyCap", "NewCollateralFactor", "NewPriceOracle",
                                        "MarketListed",
                                        "MarketUnlisted"]):
                    title = "Comptroller Markets " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                            str(tx["event"])) + " event detected"
                    content = '<@&945071604642222110>'
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                    {"name":'Address :',"value":str(tx["address"]),"inline":False},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]

                color = colors.dark_orange
                send = True

            elif (self.alert == "transfer"):
                webhook = os.getenv('WEBHOOK_CONCAVE')
                watch_addresses =["0x6fF51547f69d05d83a7732429cfe4ea1E3299E10","0x226e7AF139a0F34c6771DeB252F9988876ac1Ced"]
                if self.event_name in ["Transfer"] and ((str(tx["args"]["from"] or tx["args"]["sender"]) in watch_addresses) or (str(tx["args"]["to"] or tx["args"]["receiver"]) in watch_addresses)):
                    title = "Concave DOLA/3CRV activity detected"
                     # '<@&945071604642222110>'
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                    {"name":'Transfer :',"value":str(formatCurrency(tx["args"]["value"]/fetchers.getDecimals(self.web3,tx["address"])))+' '+str(fetchers.getSymbol(self.web3,tx["address"])),"inline":False},
                    {"name":'From :',"value":str(tx["args"]["from"] or tx["args"]["sender"]),"inline":False},
                    {"name":'To :',"value":str(tx["args"]["to"] or tx["args"]["receiver"]),"inline":False},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]
                    color = colors.dark_orange
                    send = True
            elif (self.alert == "transfer_temp"):
                webhook = os.getenv('WEBHOOK_DOLA3CRV')
                watch_addresses =["0xA79828DF1850E8a3A3064576f380D90aECDD3359"]
                if (self.event_name in ["Transfer"] and (((str(tx["args"]["from"]) or str(tx["args"]["sender"])) in watch_addresses) or ((str(tx["args"]["to"] or str(tx["args"]["receiver"]))) in watch_addresses))):
                    title = "Zap Activity detected"
                    #'<@&945071604642222110>'
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                    {"name":'Transfer :',"value":str(formatCurrency(tx["args"]["value"]/fetchers.getDecimals(self.web3,tx["address"])))+' '+str(fetchers.getSymbol(self.web3,tx["address"])),"inline":False},
                    {"name":'From :',"value":str(tx["args"]["from"]) or str(tx["args"]["sender"]),"inline":False},
                    {"name":'To :',"value":str(tx["args"]["to"]) or str(tx["args"]["receiver"]),"inline":False},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]
                    color = colors.dark_orange
                    send = True
            elif (self.alert == "profits"):
                webhook = os.getenv('WEBHOOK_DOLA3CRV')
                feds =["0xcc180262347F84544c3a4854b87C34117ACADf94","0x7765996dAe0Cf3eCb0E74c016fcdFf3F055A5Ad8","0x5Fa92501106d7E4e8b4eF3c4d08112b6f306194C"]

                if (self.event_name in ["Transfer"] and (str(tx["args"]["from"] or tx["args"]["sender"] ) in feds and str(tx["args"]["to"] or tx["args"]["receiver"])=='0x926dF14a23BE491164dCF93f4c468A50ef659D5B')):
                    title = "Fed Profit Taking detected"
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                    {"name":'Transfer :',"value":str(formatCurrency(tx["args"]["value"]/fetchers.getDecimals(self.web3,tx["address"])))+' '+str(fetchers.getSymbol(self.web3,tx["address"])),"inline":False},
                    {"name":'From :',"value":str(tx["args"]["from"]) or str(tx["args"]["sender"]),"inline":False},
                    {"name":'To :',"value":str(tx["args"]["to"]) or str(tx["args"]["receiver"]),"inline":False},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False},
                    {"name":'Fed Address :',"value":"https://etherscan.io/address/" + str(tx["args"]["from"]),"inline":False}]
                    content = '<@&945071604642222110>'
                    color = colors.dark_orange
                    send = True
            elif (self.alert == "harvest"):
                webhook = os.getenv('WEBHOOK_DOLA3CRV')

                if (self.event_name in ["Harvested"]):
                    title = "Yearn Harvest detected"
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                    {"name":'Tx :',"value": json.dumps(tx) ,"inline":False},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]
                    content = '<@&945071604642222110>'
                    color = colors.dark_orange
                    send = True

            elif (self.alert == "debt_repayment"):
                webhook = os.getenv('WEBHOOK_DEBTREPAYMENT')
                image = "https://dune.com/embeds/1291754/2213835/4c5b629f-a6b0-4575-98a1-9d5fae4fab33"
                if (self.event_name in ["debtRepayment"]):
                    title = "Debt Repayment detected"

                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                    {"name":'Token Repaid :',"value":str(fetchers.getSymbol(self.web3,tx["args"]["underlying"])),"inline":True},
                    {"name":'Amount Received :',"value":str(formatCurrency(tx["args"]["receiveAmount"]/fetchers.getDecimals(self.web3,tx["args"]["underlying"]))),"inline":True},
                    {"name":'Amount Paid :',"value":str(formatCurrency(tx["args"]["paidAmount"]/fetchers.getDecimals(self.web3,tx["args"]["underlying"]))),"inline":True},
                    {"name": 'Received/Paid ratio :',"value":str(formatPercent(tx["args"]["receiveAmount"]/tx["args"]["paidAmount"])),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False},
                    {"name":'Debt Repayment Contract :',"value":"https://etherscan.io/address/0x9eb6BF2E582279cfC1988d3F2043Ff4DF18fa6A0","inline":False}]
                    color = colors.dark_orange

                    send = True
            elif (self.alert == "debt_conversion"):
                webhook = os.getenv('WEBHOOK_DEBTREPAYMENT')
                image = "https://dune.com/embeds/1291809/2213790/9e5c3845-66c0-496f-b42a-49a2fbd20df9"
                if (self.event_name in ["Conversion"]):
                    title = "Debt Conversion  detected"
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                    {"name":'User :',"value":str(tx["args"]["user"]),"inline":True},
                    {"name":'Token Repaid :',"value":str(fetchers.getSymbol(self.web3,tx["args"]["anToken"])),"inline":True},
                    {"name": 'DOLA Amount :',"value":str(formatCurrency(tx["args"]["dolaAmount"] / 1e18)),"inline":True},
                    {"name":'Underlying Amount :',"value":str(formatCurrency(tx["args"]["underlyingAmount"] / fetchers.getDecimals(self.web3,tx["args"]["anToken"]))),"inline":True},
                    {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False},
                    {"name":'Debt Conversion Contract :',"value":"https://etherscan.io/address/0x1ff9c712B011cBf05B67A6850281b13cA27eCb2A","inline":False}]
                    color = colors.dark_orange
                    send = True
                elif (self.event_name in ["Redemption"]):
                    title = "Debt Conversion  detected - Redemption"
                    content = json.dumps(tx)
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                   {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]
                    color = colors.dark_orange
                    send = True
                elif (self.event_name in ["Repayment"]):
                    title = "Debt Conversion  detected - Repayment"
                    content = json.dumps(tx)
                    fields = [{"name":'Block Number :',"value":str(tx["blockNumber"]),"inline":False},
                   {"name":'Transaction :',"value":"https://etherscan.io/tx/" + str(tx["transactionHash"]),"inline":False}]
                    color = colors.dark_orange
                    send = True

            if send:
                sendWebhook(webhook, title, fields, content, image, color)

        except Exception as e:
            logging.warning('Error in event handler')
            logging.error(e)
            #sendError(f'Error in event handler : {str(e)}')
            pass

# Define state change to handle and logs to the console/send to discord
class HandleTx(Thread):
    def __init__(self,web3, tx, alert, contract, name, **kwargs):
        super(HandleTx, self).__init__(**kwargs)
        self.web3 = web3
        self.contract = contract
        self.alert = alert
        self.name = name
        self.tx = tx

    def run(self):
        try:
            self.tx = json.loads(Web3.toJSON(self.tx))
            # logs result table and start writing message
            logging.info(str(datetime.now()) + " " + str(self.tx))

            send = False
            image = ''
            content = ''
            webhook = ''
            title = ''
            fields = []
            color = colors.blurple
            if (self.alert == 'multisig' and self.web3.eth.chainId==1):
                webhook = os.getenv('WEBHOOK_GOVERNANCE')

                logging.info(str('Tx detected on ' + str(self.tx["address"])))
                title = str('Tx detected on ' + str(self.name))
                
                send = True
                fields = [{"name":'Multisig :',"value":str(self.tx["address"]),"inline":True},
                {"name":'Link to transaction :',"value":"https://etherscan.io/tx/" + str(self.tx["transactionHash"]),"inline":True},
                {"name":'Transaction :',"value":json.dumps(self.tx),"inline":False}]
            if (self.alert == 'multisig' and self.web3.eth.chainId==10):
                webhook = os.getenv('WEBHOOK_GOVERNANCE')

                logging.info(str('Tx detected on ' + str(self.tx["address"])))
                title = str('Tx detected on ' + str(self.name))

                send = True
                fields = [{"name":'Multisig :',"value":str(self.tx["address"]),"inline":True},
                {"name":'Link to transaction :',"value":"https://optimistic.etherscan.io/tx/" + str(self.tx["transactionHash"]),"inline":True},
                {"name":'Transaction :',"value":json.dumps(self.tx),"inline":False}]
            if (self.alert == 'multisig' and self.web3.eth.chainId==250):
                webhook = os.getenv('WEBHOOK_GOVERNANCE')

                logging.info(str('Tx detected on ' + str(self.tx["address"])))
                title = str('Tx detected on ' + str(self.name))

                send = True
                fields = [{"name":'Multisig :',"value":str(self.tx["address"]),"inline":True},
                {"name":'Link to transaction :',"value":"https://ftmscan.io/tx/" + str(self.tx["transactionHash"]),"inline":True},
                {"name":'Transaction :',"value":json.dumps(self.tx),"inline":False}]

            if send:
                sendWebhook(webhook, title, fields, content, image, color)
        except Exception as e:
            logging.warning('Error in tx handler')
            logging.error(e)
            #sendError(str(f'Error in tx handler : {str(e)}'))
            pass

# Listen to coingecko  price changes every 60 seconds
class HandleCoingecko(Thread):
    def __init__(self, id, old_value,value, change,  **kwargs):
        super(HandleCoingecko, self).__init__(**kwargs)
        self.value = value
        self.id = id
        self.old_value = old_value
        self.change = change


    def run(self):
        try:
            if abs(self.change) > 0:
                send = False
                image = ''
                content=''
                title = ''
                fields = []
                color = colors.blurple
                webhook = os.getenv('WEBHOOK_MARKETS')
                logging.info(str(formatPercent(self.change)) + ' change detected on Coingecko '+str(self.id)+' Price')
                title = str(formatPercent(self.change)) + ' change detected on Coingecko '+str(self.id)+' Price'

                if abs(self.change) > 0.2:
                    content = '<@&945071604642222110>'
                    level = 3
                    color = colors.red
                    send = True
                elif abs(self.change) > 0.1:
                    level = 2
                    color = colors.dark_orange
                    send = True
                elif abs(self.change) > 0.05:
                    level = 1
                    color = colors.orange
                    send = True

                if send:
                    fields = [{"name":'Alert Level :',"value":str(level),"inline":False},
                    {"name":'Variation :',"value":str(formatPercent(self.change)),"inline":True},
                    {"name":'Old Value :',"value":str(formatCurrency(self.old_value)),"inline":True},
                    {"name":'New Value :',"value":str(formatCurrency(self.value)),"inline":True},
                    {"name":'Link to Market :',"value": 'https://www.coingecko.com/en/coins/inverse-finance',"inline":False}]
                    sendWebhook(webhook, title, fields, content, image, color)

        except Exception as e:
            logging.warning(f'Error in coingecko variation handler')
            logging.error(e)
            #sendError(f'Error in state variation handler : {str(e)}')
            pass

# Listen to coingecko  price changes every 60 seconds
class HandleCoingeckoVolume(Thread):
    def __init__(self, id, old_value,value, change,  **kwargs):
        super(HandleCoingeckoVolume, self).__init__(**kwargs)
        self.value = value
        self.id = id
        self.old_value = old_value
        self.change = change


    def run(self):
        try:
            if abs(self.change) > 0:
                send = False
                image = ''
                content=''
                title = ''
                fields = []
                color = colors.blurple
                webhook = os.getenv('WEBHOOK_MARKETS')
                logging.info(str(formatPercent(self.change)) + ' change detected on Coingecko '+str(self.id)+' 24H volume')
                title = str(formatPercent(self.change)) + ' change detected on Coingecko '+str(self.id)+'  24H volume'

                if abs(self.change) > 0.9:
                    content = '<@&945071604642222110>'
                    level = 3
                    color = colors.red
                    send = True
                elif abs(self.change) > 0.8:
                    level = 2
                    color = colors.dark_orange
                    send = True
                elif abs(self.change) > 0.7:
                    level = 1
                    color = colors.orange
                    send = True

                if send:
                    fields = [{"name": 'Alert Level :', "value": str(level), "inline": False},
                              {"name": 'Variation :', "value": str(formatPercent(self.change)), "inline": True},
                              {"name": 'Old Value :', "value": str(formatCurrency(self.old_value)), "inline": True},
                              {"name": 'New Value :', "value": str(formatCurrency(self.value)), "inline": True},
                              {"name": 'Link to Market :',"value": 'https://www.coingecko.com/en/coins/inverse-finance', "inline": False}]

                    sendWebhook(webhook, title, fields, content, image, color)

        except Exception as e:
            logging.warning(f'Error in coingecko volume variation handler')
            logging.error(e)
            #sendError(f'Error in coingecko volume variation handler : {str(e)}')
            pass
