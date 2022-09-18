# import the following dependencies
import os
import json
import re
import fetchers
from threading import Thread
from web3 import Web3
from datetime import datetime
import logging
from helpers import colors, makeFields, sendError, sendWebhook, formatPercent, formatCurrency
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
                        fields = f'''makeFields(
                             ['Alert Level :',
                             'Variation :',
                             'Old Value :',
                             'New Value :',
                             'Link to Market :'], 
                             ['{str(level)}',
                             '{str(formatPercent(self.change))}',
                             '{str(formatCurrency(self.old_value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.state_argument))))}',
                             '{str(formatCurrency(self.value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.state_argument))))}',
                             '{'https://etherscan.io/address/' + str(self.state_argument)}'], 
                             [True, True,True,True,False])'''

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
                        fields = f'''makeFields(
                             ['Alert Level :',
                             'Variation :',
                             'Old Value :',
                             'New Value :',
                             'Link to Market :'], 
                             ['{str(level)}',
                             '{str(formatPercent(self.change))}',
                             '{str(formatCurrency(self.old_value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.contract.address))))}',
                             '{str(formatCurrency(self.value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.contract.address))))}',
                             '{'https://etherscan.io/address/' + str(self.contract.address)}'], 
                             [True, True,True,True,False])'''

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
                        fields = f'''makeFields(
                             ['Alert Level :',
                             'Variation :',
                             'Old Value :',
                             'New Value :',
                             'Link to Pool :'], 
                             ['{str(level)}',
                             '{str(formatPercent(self.change))}',
                             '{str(formatCurrency(self.old_value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.contract.address))))}',
                             '{str(formatCurrency(self.value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.contract.address))))}',
                             '{'https://etherscan.io/address/' + str(self.contract.address)}'], 
                             [True, True,True,True,False])'''

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

                    fields = f'''makeFields(
                         ['Alert Level :',
                         'Variation :',
                         'Old Value :',
                         'New Value :',
                         'Link to Pool :'], 
                         ['{str(level)}',
                         '{str(formatPercent(self.change))}',
                         '{str(formatCurrency(self.old_value / 1e18))}',
                         '{str(formatCurrency(self.value / 1e18))}',
                         '{'https://etherscan.io/address/' + str(self.contract.address)}'], 
                         [True, True,True,True,False])'''

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
            fields = []
            image = ''
            color = colors.blurple
            content = ''
            webhook = ''

            if (self.alert == "dola3crv"):
                webhook = os.getenv('WEBHOOK_DOLA3CRV')
                image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/833844/1457892/bccc1e5b-4b60-4b28-85da-fbd558a2fd69.jpg"
                if (self.event_name == "RemoveLiquidity"):

                    if (tx["args"]["token_amounts"][0] + tx["args"]["token_amounts"][1])/1e18 > 300000:
                        content = '<@&945071604642222110>'
                    color = colors.red
                    send = True
                    if send:
                        title = "DOLA3CRV Pool Liquidity Removal event detected"
                        fields = f'''makeFields(
                        ['Block :',
                        'DOLA Amount :',
                        '3CRV Amount :',
                        'Address :',
                        'DOLA in Pool :',
                        '3CRV in Pool :',
                        'DOLA+3CRV in Pool',
                        'Transaction :'],
                        ['{str(tx["blockNumber"])}',
                        '{str(formatCurrency(tx["args"]["token_amounts"][0] / 1e18))}',
                        '{str(formatCurrency(tx["args"]["token_amounts"][1] / 1e18))}',
                        '{str(tx["address"])}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0]))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0] + fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                        '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                        [True,True,True,False,True,True,False,False])'''
                elif (self.event_name == "RemoveLiquidityOne"):
                    if tx["args"]["coin_amount"]/1e18 > 300000:
                        content = '<@&945071604642222110>'
                    color = colors.red
                    send = True
                    if send:
                        title = "DOLA3CRV Pool Liquidity Removal event detected"
                        fields = f'''makeFields(
                        ['Block :',
                        'Token Amount :',
                        'DOLA in Pool :',
                        '3CRV in Pool :',
                        'DOLA+3CRV in Pool',
                        'Transaction :'],
                        ['{str(tx["blockNumber"])}',
                        '{str(formatCurrency(tx["args"]["coin_amount"] / 1e18))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0]))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0] + fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[1]))}',
                        '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                        [True,False,True,False,True,False,False])'''
                elif (self.event_name == "AddLiquidity"):
                    if (tx["args"]["token_amounts"][0] + tx["args"]["token_amounts"][1])/1e18 > 300000:
                        content = '<@&945071604642222110>'

                    color = colors.dark_green
                    send = True
                    if send:
                        title = "DOLA3CRV Pool Liquidity Add event detected"
                        fields = f'''makeFields(
                        ['Block :',
                        'DOLA Amount :',
                        '3CRV Amount :',
                        'Address :',
                        'DOLA in Pool :',
                        '3CRV in Pool :',
                        'DOLA+3CRV in Pool',
                        'Transaction :'],
                        ['{str(tx["blockNumber"])}',
                        '{str(formatCurrency(tx["args"]["token_amounts"][0] / 1e18))}',
                        '{str(formatCurrency(tx["args"]["token_amounts"][1] / 1e18))}',
                        '{str(tx["address"])}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0]))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0] + fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                        '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                        [True,True,True,False,True,True,False,False])'''
            elif (self.alert == "dola3crv_zap"):
                webhook = os.getenv('WEBHOOK_DOLA3CRV')
                image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/833844/1457892/bccc1e5b-4b60-4b28-85da-fbd558a2fd69.jpg"
                if (self.event_name == "RemoveLiquidity"):
                    if (tx["args"]["token_amounts"][0] + tx["args"]["token_amounts"][1])/1e18 > 300000:
                        content = '<@&945071604642222110>'
                    color = colors.red
                    send = True
                    if send:
                        title = "DOLA3CRV Pool Liquidity Removal event detected"
                        fields = f'''makeFields(
                        ['Block :',
                        'DOLA Amount :',
                        '3CRV Amount :',
                        'Address :',
                        'DOLA in Pool :',
                        '3CRV in Pool :',
                        'DOLA+3CRV in Pool',
                        'Transaction :'],
                        ['{str(tx["blockNumber"])}',
                        '{str(formatCurrency(tx["args"]["token_amounts"][0] / 1e18))}',
                        '{str(formatCurrency(tx["args"]["token_amounts"][1] / 1e18))}',
                        '{str(tx["address"])}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0]))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0] + fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                        '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                        [True,True,True,False,True,True,False,False])'''
                elif (self.event_name == "RemoveLiquidityOne"):
                    if tx["args"]["coin_amount"]/1e18 > 300000:
                        content = '<@&945071604642222110>'
                    color = colors.red
                    send = True
                    if send:
                        title = "DOLA3CRV Pool Liquidity Removal event detected"
                        fields = f'''makeFields(
                        ['Block :',
                        'Token Amount :',
                        'DOLA in Pool :',
                        '3CRV in Pool :',
                        'DOLA+3CRV in Pool',
                        'Transaction :'],
                        ['{str(tx["blockNumber"])}',
                        '{str(formatCurrency(tx["args"]["coin_amount"] / 1e18))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0]))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0] + fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[1]))}',
                        '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                        [True,False,True,False,True,False,False])'''
                elif (self.event_name == "AddLiquidity"):

                    if (tx["args"]["token_amounts"][0] + tx["args"]["token_amounts"][1])/1e18 > 300000:
                        content = '<@&945071604642222110>'

                    color = colors.dark_green
                    send = True
                    if send:
                        title = "DOLA3CRV Pool Liquidity Add event detected"
                        fields = f'''makeFields(
                        ['Block :',
                        'DOLA Amount :',
                        '3CRV Amount :',
                        'Address :',
                        'DOLA in Pool :',
                        '3CRV in Pool :',
                        'DOLA+3CRV in Pool',
                        'Transaction :'],
                        ['{str(tx["blockNumber"])}',
                        '{str(formatCurrency(tx["args"]["token_amounts"][0] / 1e18))}',
                        '{str(formatCurrency(tx["args"]["token_amounts"][1] / 1e18))}',
                        '{str(tx["address"])}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0]))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0] + fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                        '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                        [True,True,True,False,True,True,False,False])'''
            elif (self.alert == "dolafraxbp_pool"):
                webhook = os.getenv('WEBHOOK_DOLAFRAXBP')
                image = ""
                if (self.event_name == "RemoveLiquidity" and (tx["args"]["token_amounts"][0] + tx["args"]["token_amounts"][1]) / 1e18 > 50000):
                    if (tx["args"]["token_amounts"][0] + tx["args"]["token_amounts"][1]) / 1e18 > 500000:
                        content = '<@&945071604642222110>'
                    color = colors.red
                    send = True
                    title = "DOLAFRAX Pool Liquidity Removal event detected"
                    fields = f'''makeFields(
                    ['Block :',
                    'DOLA Amount :',
                    'FRAX Amount :',
                    'Address :',
                    'DOLA in Pool :',
                    'FRAX in Pool :',
                    'DOLA+FRAX in Pool',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(formatCurrency(tx["args"]["token_amounts"][0] / 1e18))}',
                    '{str(formatCurrency(tx["args"]["token_amounts"][1] / 1e18))}',
                    '{str(tx["address"])}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[0]))}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[1]))}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[0] + fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[1]))}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [True,True,True,False,True,True,False,False])'''
                elif (self.event_name == "RemoveLiquidityOne" and tx["args"]["coin_amount"] / 1e18 > 50000):
                    if tx["args"]["coin_amount"] / 1e18 > 500000:
                        content = '<@&945071604642222110>'
                    color = colors.red
                    send = True
                    title = "DOLAFRAX Pool Liquidity Removal event detected"
                    fields = f'''makeFields(
                    ['Block :',
                    'Token Amount :',
                    'DOLA in Pool :',
                    'FRAX in Pool :',
                    'DOLA+FRAX in Pool',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(formatCurrency(tx["args"]["coin_amount"] / 1e18))}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[0]))}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[1]))}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[0] + fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[1]))}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                    [True,False,True,False,True,False,False])'''
                elif (self.event_name == "AddLiquidity" and (tx["args"]["token_amounts"][0] + tx["args"]["token_amounts"][1]) / 1e18 > 50000):
                    title = "DOLAFRAX Pool Liquidity Add event detected"
                    fields = f'''makeFields(
                    ['Block :',
                    'DOLA Amount :',
                    'FRAX Amount :',
                    'Address :',
                    'DOLA in Pool :',
                    'FRAX in Pool :',
                    'DOLA+FRAX in Pool',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(formatCurrency(tx["args"]["token_amounts"][0] / 1e18))}',
                    '{str(formatCurrency(tx["args"]["token_amounts"][1] / 1e18))}',
                    '{str(tx["address"])}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[0]))}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[1]))}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[0] + fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[1]))}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                    [True,True,True,False,True,True,False,False])'''
            elif (self.alert == "dolafraxbp_gauge"):
                webhook = os.getenv('WEBHOOK_DOLAFRAXBP')
                image = ""
                if (self.event_name == "NewGaugeWeight" and tx["args"]["gauge_addr"]=='0xBE266d68Ce3dDFAb366Bb866F4353B6FC42BA43c'):
                    title = "DOLAFRAX New Gauge Weight detected"
                    fields = f'''makeFields(
                    ['Block :',
                    'Gauge Address :',
                    'Weight :',
                    'Total Weight :',
                    'DOLA in Pool :',
                    'crvFRAX in Pool :',
                    'DOLA+crvFRAX in Pool',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(tx["args"]["gauge_addr"])}',
                    '{str(tx["args"]["weight"])}',
                    '{str(tx["args"]["total_weight"])}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[0]))}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[1]))}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[0] + fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[1]))}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [True,False,False,False,True,True,False,False])'''
                    content = '<@&945071604642222110>'
                    color = colors.red
                    send = True
                elif (self.event_name == "VoteForGauge" and tx["args"]["gauge_addr"]=='0xBE266d68Ce3dDFAb366Bb866F4353B6FC42BA43c'):
                    title = "DOLAFRAX Pool Vote For Gauge detected"
                    fields = f'''makeFields(
                                        ['Block :',
                                        'User :',
                                        'Gauge Address :',
                                        'Weight :',
                                        'DOLA in Pool :',
                                        'crvFRAX in Pool :',
                                        'DOLA+crvFRAX in Pool',
                                        'Transaction :'],
                                        ['{str(tx["blockNumber"])}',
                                        '{str(tx["args"]["user"])}',
                                        '{str(tx["args"]["gauge_addr"])}',
                                        '{str(tx["args"]["weight"])}',
                                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[0]))}',
                                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[1]))}',
                                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[0] + fetchers.getCurveBalances(self.web3,'0xE57180685E3348589E9521aa53Af0BCD497E884d')[1]))}',
                                        '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                        [True,False,False,False,True,True,False,False])'''
                    content = '<@&945071604642222110>'
                    color = colors.red
                    send = True
            elif (self.alert == "dola3crv_gauge"):
                webhook = os.getenv('WEBHOOK_DOLA3CRV')
                image = ""
                if (self.event_name == "NewGaugeWeight" and tx["args"]["gauge_addr"]=='0x8Fa728F393588E8D8dD1ca397E9a710E53fA553a'):
                    title = "DOLA3CRV New Gauge Weight detected"
                    fields = f'''makeFields(
                    ['Block :',
                    'Gauge Address :',
                    'Weight :',
                    'Total Weight :',
                    'DOLA in Pool :',
                    'DOLA3CRV in Pool :',
                    'DOLA+DOLA3CRV in Pool',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(tx["args"]["gauge_addr"])}',
                    '{str(tx["args"]["weight"])}',
                    '{str(tx["args"]["total_weight"])}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0]))}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                    '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0] + fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [True,False,False,False,True,True,False,False])'''
                    content = '<@&945071604642222110>'
                    color = colors.dark_orange
                    send = True
                elif (self.event_name == "VoteForGauge" and tx["args"]["gauge_addr"]=='0x8Fa728F393588E8D8dD1ca397E9a710E53fA553a'):
                    title = "DOLA3CRV Pool Vote For Gauge detected"
                    fields = f'''makeFields(
                                        ['Block :',
                                        'User :',
                                        'Gauge Address :',
                                        'Weight :',
                                        'DOLA in Pool :',
                                        '3CRV in Pool :',
                                        'DOLA+3CRV in Pool',
                                        'Transaction :'],
                                        ['{str(tx["blockNumber"])}',
                                        '{str(tx["args"]["user"])}',
                                        '{str(tx["args"]["gauge_addr"])}',
                                        '{str(tx["args"]["weight"])}',
                                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0]))}',
                                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                                        '{str(formatCurrency(fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[0] + fetchers.getCurveBalances(self.web3,'0xaa5a67c256e27a5d80712c51971408db3370927d')[1]))}',
                                        '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                        [True,False,False,False,True,True,False,False])'''
                    content = '<@&945071604642222110>'
                    color = colors.dark_orange
                    send = True
            elif (self.alert in ["lending1", "lending2"]):
                if (self.event_name == "Mint"):
                    webhook = os.getenv('WEBHOOK_SUPPLY')
                    title = "Lending Market : New Deposit event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    fields = f'''makeFields(
                                ['Block Number :',
                                'Minter :',
                                'Market Symbol :',
                                'Market Address :',
                                'USD Value',
                                'Mint Amount :',
                                'Mint Tokens :',
                                'Total Supply',
                                'Total Cash :',
                                'Transaction :'],
                                ['{str(tx["blockNumber"])}',
                                '{str(tx["args"]["minter"])}',
                                '{str(fetchers.getSymbol(self.web3,tx["address"]))}',
                                '{str(tx["address"])}',
                                '{str(formatCurrency(tx["args"]["mintAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"])))}',
                                '{str(formatCurrency(tx["args"]["mintAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["mintTokens"] / fetchers.getDecimals(self.web3,tx["address"])))}',
                                '{str(formatCurrency(fetchers.getSupply(self.web3,tx["address"])))}',
                                '{str(formatCurrency(fetchers.getCash(self.web3,tx["address"])))}',
                                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                [True,True,True,False,True,True,True,True,True,False])'''
                    if ((tx["args"]["mintAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"]))>100000):
                        content = '<@&945071604642222110>'
                    color = colors.blurple
                    send = True
                elif (self.event_name == "Redeem"):
                    webhook = os.getenv('WEBHOOK_SUPPLY')
                    title = "Lending Market : New Withdrawal event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    fields = f'''makeFields(
                                ['Block Number :',
                                'Redeemer :',
                                'Market Symbol :',
                                'Market Address :',
                                'USD Value',
                                'Redeem Amount :',
                                'Redeem Tokens :',
                                'Total Supply',
                                'Total Cash :',
                                'Transaction :'],
                                ['{str(tx["blockNumber"])}',
                                '{str(tx["args"]["redeemer"])}',
                                '{str(fetchers.getSymbol(self.web3,tx["address"]))}',
                                '{str(tx["address"])}',
                                '{str(formatCurrency(tx["args"]["redeemAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"])))}',
                                '{str(formatCurrency(tx["args"]["redeemAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["redeemTokens"] / fetchers.getDecimals(self.web3,tx["address"])))}',
                                '{str(formatCurrency(fetchers.getSupply(self.web3,tx["address"])))}',
                                '{str(formatCurrency(fetchers.getCash(self.web3,tx["address"])))}',
                                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                [True,True,True,False,True,True,True,True,True,False])'''
                    if ((tx["args"]["redeemAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"]))>100000):
                        content = '<@&945071604642222110>'

                    color = colors.blurple
                    send = True
                elif (self.event_name == "Borrow"):
                    webhook = os.getenv('WEBHOOK_BORROW')
                    title = "Lending Market : New Borrow event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    fields = f'''makeFields(
                                ['Block Number :',
                                'Borrower :',
                                'Market Symbol :',
                                'Market Address :',
                                'USD Value :',
                                'Borrow Amount :',
                                'Account Borrows :',
                                'Total Borrows :',
                                'Total Supply :',
                                'Total Cash :',
                                'Transaction :'],
                                ['{str(tx["blockNumber"])}',
                                '{str(tx["args"]["borrower"])}',
                                '{str(fetchers.getSymbol(self.web3,tx["address"]))}',
                                '{str(tx["address"])}',
                                '{str(formatCurrency(tx["args"]["borrowAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"])))}',
                                '{str(formatCurrency(tx["args"]["borrowAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["accountBorrows"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["totalBorrows"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"]))))}',
                                '{str(formatCurrency(fetchers.getSupply(self.web3,tx["address"])))}',
                                '{str(formatCurrency(fetchers.getCash(self.web3,tx["address"])))}',
                                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                [True,True,False,True,True,True,True,True,True,True,False])'''
                    if ((tx["args"]["borrowAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"]))>100000):
                        content = '<@&945071604642222110>'

                    color = colors.blurple
                    send = True
                elif (self.event_name == "RepayBorrow"):
                    webhook = os.getenv('WEBHOOK_BORROW')
                    title = "Lending Market : New Repayment event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))

                    fields = f'''makeFields(
                                ['Block Number :',
                                'Borrower :',
                                'Market Symbol :',
                                'Market Address :',
                                'USD Value :',
                                'Borrow Amount :',
                                'Account Borrows :',
                                'Total Borrows :',
                                'Total Supply :',
                                'Total Cash :',
                                'Transaction :'],
                                ['{str(tx["blockNumber"])}',
                                '{str(tx["args"]["borrower"])}',
                                '{str(fetchers.getSymbol(self.web3,tx["address"]))}',
                                '{str(tx["address"])}',
                                '{str(formatCurrency(tx["args"]["repayAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"])))}',
                                '{str(formatCurrency(tx["args"]["repayAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["accountBorrows"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["totalBorrows"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"]))))}',
                                '{str(formatCurrency(fetchers.getSupply(self.web3,tx["address"])))}',
                                '{str(formatCurrency(fetchers.getCash(self.web3,tx["address"])))}',
                                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                [True,True,False,True,True,True,True,True,True,True,False])'''
                    if ((tx["args"]["repayAmount"] / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])) * fetchers.getUnderlyingPrice(self.web3,tx["address"]))>100000):
                        content = '<@&945071604642222110>'

                    color = colors.blurple
                    send = True
                elif (self.event_name == "LiquidateBorrow"):
                    title = "Lending Market New Liquidation event detected for " + str(fetchers.getSymbol(self.web3,tx["address"]))
                    webhook = os.getenv('WEBHOOK_LIQUIDATIONS')
                    fields = f'''makeFields(
                                ['Block Number :',
                                'Liquidator :',
                                'Borrower :',
                                'Market Address :',
                                'Seized Amount :',
                                'Seized Token  :',
                                'Repay Amount :',
                                'Repay Amount USD:',
                                'Repay Token  :',
                                'Transaction :'],
                                ['{str(tx["blockNumber"])}',
                                '{str(tx["args"]["liquidator"])}',
                                '{str(tx["args"]["borrower"])}',
                                '{str(tx["address"])}',
                                '{str(formatCurrency(tx["args"]["seizeTokens"]/ fetchers.getDecimals(self.web3,tx["args"]["cTokenCollateral"])))}',
                                '{str(fetchers.getSymbol(self.web3,tx["args"]["cTokenCollateral"]))}',
                                '{str(formatCurrency(tx["args"]["repayAmount"]/ fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["repayAmount"]* fetchers.getUnderlyingPrice(self.web3,tx["address"])/ fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"]))))}',
                                '{str(fetchers.getSymbol(self.web3,tx["address"]))}',
                                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                [False,False,False,False,True,True,False,True,True,False])'''
                    if ((tx["args"]["repayAmount"]/ fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,tx["address"])))>100000):
                        content = '<@&945071604642222110>'

                    color = colors.blurple
                    send = True
            elif (self.alert == "governance"):
                content = "<@&899302193608409178>"
                webhook = os.getenv('WEBHOOK_GOVERNANCE')
                if (self.event_name == "ProposalCreated"):
                    title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"]))

                    fields = f'''makeFields(
                    ['Block Number :',
                    'Proposal :',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{"https://www.inverse.finance/governance/proposals/mills/" + str(fetchers.getProposalCount(self.web3))}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [False,False,False])'''

                    color = colors.blurple
                    send = True
                elif (self.event_name in ["ProposalCanceled"]):
                    title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"]))
                    fields = f'''makeFields(
                    ['Block Number :',
                    'Proposal :',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{"https://www.inverse.finance/governance/proposals/mills/" + str(tx["args"]["id"])}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [False,False,False])'''

                    color = colors.dark_red
                    send = True
                elif (self.event_name in ["ProposalQueued"]):
                    title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",str(tx["event"]))

                    fields = f'''makeFields(
                    ['Block Number :',
                    'Proposal :',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{"https://www.inverse.finance/governance/proposals/mills/" + str(tx["args"]["id"])}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [False,False,False])'''

                    color = colors.blurple
                    send = True
                elif (self.event_name in ["ProposalExecuted"]):
                    title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",str(tx["event"]))

                    fields = f'''makeFields(
                    ['Block Number :',
                    'Proposal :',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{"https://www.inverse.finance/governance/proposals/mills/" + str(tx["args"]["id"])}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [False,False,False])'''

                    color = colors.dark_green
                    send = True
            elif (self.alert == "fed"):
                webhook = os.getenv('WEBHOOK_FED')
                image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/22517/1128427/3084f915-b906-4fdf-ac8c-ad5c0ce57e2b.jpg"
                content = ''
                if (self.event_name in ["Expansion"]):
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
                        operation = 'Sell ' + str(formatCurrency(tx["args"]['amount0In'] / fetchers.getDecimals(
                            fetchers.getSushiTokens(self.web3,tx["address"])[0]))) + " " + str(
                            fetchers.getSushiTokensSymbol(self.web3,tx["address"])[0])
                        color = colors.dark_red
                        title = "Sushiswap New Sell event detected"
                        send = True

                    fields = f'''makeFields(
                                ['Block Number :',
                                'Name :',
                                'Symbol :',
                                'Address :',
                                'Operation :',
                                'USD value :',
                                'Transaction :'],
                                ['{str(tx["blockNumber"])}',
                                '{str(fetchers.getName(self.web3,tx["address"]))}',
                                '{str(fetchers.getSymbol(self.web3,tx["address"]))}',
                                '{str(tx["address"])}',
                                '{str(operation)}',
                                '{str(formatCurrency(((tx["args"]["amount0Out"] + tx["args"]["amount0In"]) / fetchers.getDecimals(self.web3,fetchers.getSushiTokens(self.web3,tx["address"])[0])) * fetchers.getUnderlyingPrice(self.web3,'0x1637e4e9941d55703a7a5e7807d6ada3f7dcd61b')))}',
                                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                [True,True,True,False,True,True,False])'''

                elif (self.event_name in ["Mint"]):
                    title = "Sushi New Liquidity Add event detected"
                    content = ''
                    fields = f'''makeFields(
                            ['Block Number :',
                            'Name :',
                            'Symbol :',
                            'Address :',
                            'amountADesired :',
                            'amountBDesired :',
                            'amountAMin :',
                            'amountBMin :',
                            'Token 0 :',
                            'Token 1 :',
                            'Total Supply :',
                            'Transaction :'],
                            ['{str(tx["blockNumber"])}',
                            '{str(fetchers.getName(self.web3,tx["address"]))}',
                            '{str(fetchers.getSymbol(self.web3,tx["address"]))}',
                            '{str(tx["address"])}',
                            '{str(tx["args"]["amountADesired"] / 1e18)}',
                            '{str(tx["args"]["amountBDesired"] / 1e18)}',
                            '{str(tx["args"]["amountAMin"] / 1e18)}',
                            '{str(tx["args"]["amountBMin"] / 1e18)}',
                            '{str(fetchers.getBalance(self.web3,tx["address"], fetchers.getSushiTokens(self.web3,tx["address"][0])))}',
                            '{str(fetchers.getBalance(self.web3,tx["address"], fetchers.getSushiTokens(self.web3,tx["address"][1])))}',
                            '{str(fetchers.getSupply(self.web3,tx["address"]))}',
                            '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                            [True,True,True,False,False,True,False,True,True,True,True,False])'''

                    color = colors.dark_green
                    send = True
                elif (self.event_name in ["Burn"]):
                    title = "Sushi New Liquidity Removal detected"
                    content = ''
                    fields = f'''makeFields(
                            ['Block Number :',
                            'Name :',
                            'Symbol :',
                            'Address :',
                            'Amount 0 :',
                            'Amount 1 :',
                            'Total Reserves 0 :',
                            'Total Reserves 1 :',
                            'Total Supply :',
                            'Transaction :'],
                            ['{str(tx["blockNumber"])}',
                            '{str(fetchers.getName(self.web3,tx["address"]))}',
                            '{str(fetchers.getSymbol(self.web3,tx["address"]))}',
                            '{str(tx["address"])}',
                            '{str(tx["args"]["amount0"] / 1e18)}',
                            '{str(tx["args"]["amount1"] / 1e18)}',
                            '{str(fetchers.getBalance(self.web3,tx["address"], fetchers.getSushiTokens(self.web3,tx["address"][0])))}',
                            '{str(fetchers.getBalance(self.web3,tx["address"], fetchers.getSushiTokens(self.web3,tx["address"][1])))}',
                            '{str(fetchers.getSupply(self.web3,tx["address"]))}',
                            '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                            [True,True,False,True,True,True,True,False])'''
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
                    fields = f'''makeFields(
                        ['Block Number :',
                        'Address :',
                        'Transaction :'],
                        ['{str(tx["blockNumber"])}',
                        '{str(tx["address"])}',
                        '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                        [False,False,False])'''

                color = colors.dark_orange
                send = True
            elif (self.alert == "transfer"):
                webhook = os.getenv('WEBHOOK_CONCAVE')
                watch_addresses =["0x6fF51547f69d05d83a7732429cfe4ea1E3299E10","0x226e7AF139a0F34c6771DeB252F9988876ac1Ced"]
                if (self.event_name in ["Transfer"] and (((str(tx["args"]["from"]) or str(tx["args"]["sender"])) in watch_addresses) or ((str(tx["args"]["to"] or str(tx["args"]["receiver"]))) in watch_addresses))):
                    title = "Concave DOLA/3CRV activity detected"
                    content = '' # '<@&945071604642222110>'
                    fields = f'''makeFields(
                    ['Block Number :',
                    'Transfer :',
                    'From :',
                    'To :',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(formatCurrency(tx["args"]["value"]/fetchers.getDecimals(self.web3,tx["address"])))+' '+str(fetchers.getSymbol(self.web3,tx["address"]))}',
                    '{str(tx["args"]["from"]) or str(tx["args"]["sender"])}',
                    '{str(tx["args"]["to"]) or str(tx["args"]["receiver"])}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [False,False,False,False,False])'''

                    color = colors.dark_orange

                    send = True
            elif (self.alert == "transfer_temp"):
                webhook = os.getenv('WEBHOOK_DOLA3CRV')
                watch_addresses =["0xA79828DF1850E8a3A3064576f380D90aECDD3359"]
                if (self.event_name in ["Transfer"] and (((str(tx["args"]["from"]) or str(tx["args"]["sender"])) in watch_addresses) or ((str(tx["args"]["to"] or str(tx["args"]["receiver"]))) in watch_addresses))):
                    title = "Zap Activity detected"
                    content = ''#'<@&945071604642222110>'
                    fields = f'''makeFields(
                    ['Block Number :',
                    'Transfer :',
                    'From :',
                    'To :',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(formatCurrency(tx["args"]["value"]/fetchers.getDecimals(self.web3,tx["address"])))+' '+str(self.web3,fetchers.getSymbol(tx["address"]))}',
                    '{str(tx["args"]["from"]) or str(tx["args"]["sender"])}',
                    '{str(tx["args"]["to"]) or str(tx["args"]["receiver"])}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [False,False,False,False,False])'''

                    color = colors.dark_orange

                    send = True
            elif (self.alert == "profits"):
                webhook = os.getenv('WEBHOOK_DOLA3CRV')
                feds =["0xcc180262347F84544c3a4854b87C34117ACADf94"]

                if (self.event_name in ["Transfer"] and (str(tx["args"]["from"]) in feds and str(tx["args"]["to"])=='0x926dF14a23BE491164dCF93f4c468A50ef659D5B')):
                    title = "Fed Profit Taking detected"
                    content = '<@&945071604642222110>'
                    fields = f'''makeFields(
                    ['Block Number :',
                    'Transfer :',
                    'From :',
                    'To :',
                    'Transaction :'
                    'Fed Address :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(formatCurrency(tx["args"]["value"]/fetchers.getDecimals(self.web3,tx["address"])))+' '+str(fetchers.getSymbol(self.web3,tx["address"]))}',
                    '{str(tx["args"]["from"])}',
                    '{str(tx["args"]["to"])}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}',
                    '{"https://etherscan.io/address/" + str(tx["args"]["from"])}'],
                    [False,False,False,False,False])'''

                    color = colors.dark_orange

                    send = True
            elif (self.alert == "debt_repayment"):
                webhook = os.getenv('WEBHOOK_DEBTREPAYMENT')
                if (self.event_name in ["debtRepayment"]):
                    title = "Debt Repayment detected"
                    content = ''
                    fields = f'''makeFields(
                    ['Block Number :',
                    'Token Repaid :',
                    'Amount Received :',
                    'Amount Paid :',
                    'Received/Paid ratio :',
                    'Transaction :',
                    'Debt Repayment Contract :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(fetchers.getSymbol(self.web3,tx["args"]["underlying"]))}',
                    '{str(formatCurrency(tx["args"]["receiveAmount"]/fetchers.getDecimals(self.web3,tx["args"]["underlying"])))}',
                    '{str(formatCurrency(tx["args"]["paidAmount"]/fetchers.getDecimals(self.web3,tx["args"]["underlying"])))}',
                    '{str(formatPercent(tx["args"]["receiveAmount"]/tx["args"]["paidAmount"]))}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}',
                    '{"https://etherscan.io/address/0x9eb6BF2E582279cfC1988d3F2043Ff4DF18fa6A0"}'],
                    [False,True,True,True,True,False,False])'''

                    color = colors.dark_orange

                    send = True
            elif (self.alert == "debt_conversion"):
                webhook = os.getenv('WEBHOOK_DEBTREPAYMENT')
                if (self.event_name in ["Conversion"]):
                    title = "Debt Conversion  detected"
                    content = ''
                    fields = f'''makeFields(
                                        ['Block Number :',
                                        'User :',
                                        'Token Repaid :',
                                        'DOLA Amount :',
                                        'Underlying Amount :',
                                        'Transaction :',
                                        'Debt Conversion Contract :'],
                                        ['{str(tx["blockNumber"])}',
                                        '{str(tx["args"]["user"])}',
                                        '{str(fetchers.getSymbol(self.web3,tx["args"]["anToken"]))}',
                                        '{str(formatCurrency(tx["args"]["dolaAmount"] / 1e18))}',
                                        '{str(formatCurrency(tx["args"]["underlyingAmount"] / fetchers.getDecimals(self.web3,tx["args"]["anToken"])))}',
                                        '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}',
                                        '{"https://etherscan.io/address/0x1ff9c712B011cBf05B67A6850281b13cA27eCb2A"}'],
                                        [False,True,True,True,True,False,False])'''
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
            if (self.alert == 'multisig'):
                webhook = os.getenv('WEBHOOK_GOVERNANCE')

                logging.info(str('Tx detected on ' + str(self.tx["address"])))
                title = str('Tx detected on ' + str(self.name))
                content = ''
                send = True
                fields = f'''makeFields(
                     ['Multisig :',
                     'Link to transaction :'], 
                     ['{str(self.tx["address"])}',
                     '{"https://etherscan.io/tx/" + str(self.tx["transactionHash"])}'], 
                     [False,False])'''
            if (self.alert == 'shortfall'):
                webhook = os.getenv('WEBHOOK_SHORTFALL')

                logging.info(str('Shortfall address tx detected on ' + str(self.tx["address"])))
                title = str('Shortfall address  detected on ' + str(self.tx["address"]))
                content = ''
                send = True
                fields = f'''makeFields(
                     ['Address :',
                     'Link to transaction :'], 
                     ['{str(self.tx["address"])}',
                     '{"https://etherscan.io/tx/" + str(self.tx["transactionHash"])}'], 
                     [False,False])'''

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
                content = ''
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
                    fields = f'''makeFields(
                                 ['Alert Level :',
                                 'Variation :',
                                 'Old Value :',
                                 'New Value :',
                                 'Link to Market :'], 
                                 ['{str(level)}',
                                 '{str(formatPercent(self.change))}',
                                 '{str(formatCurrency(self.old_value))}',
                                 '{str(formatCurrency(self.value))}',
                                 '{'https://www.coingecko.com/en/coins/inverse-finance'}'], 
                                 [True, True,True,True,False])'''

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
                content = ''
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
                    fields = f'''makeFields(
                                 ['Alert Level :',
                                 'Variation :',
                                 'Old Value :',
                                 'New Value :',
                                 'Link to Market :'], 
                                 ['{str(level)}',
                                 '{str(formatPercent(self.change))}',
                                 '{str(formatCurrency(self.old_value))}',
                                 '{str(formatCurrency(self.value))}',
                                 '{'https://www.coingecko.com/en/coins/inverse-finance'}'], 
                                 [True, True,True,True,False])'''

                    sendWebhook(webhook, title, fields, content, image, color)

        except Exception as e:
            logging.warning(f'Error in coingecko variation handler')
            logging.error(e)
            #sendError(f'Error in state variation handler : {str(e)}')
            pass
