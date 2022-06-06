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
    def __init__(self, value, change, alert, contract, state_function, state_argument, **kwargs):
        super(HandleStateVariation, self).__init__(**kwargs)
        self.value = value
        self.change = change
        self.contract = contract
        self.alert = alert
        self.state_function = state_function
        self.state_argument = state_argument

    def run(self):
        try:
            send = False
            image = ''
            content = ''
            webhook = ''
            title = ''
            fields = []
            color = colors.blurple
            if (self.alert == 'oracle'):
                webhook = os.getenv('WEBHOOK_MARKETS')
                if self.state_function == 'getUnderlyingPrice':
                    logging.info(str(self.change) + '% change detected on ' + str(
                        fetchers.getSymbol(fetchers.getUnderlying(self.state_argument))))
                    title = str(formatPercent(self.change)) + ' change detected on ' + str(
                        fetchers.getSymbol(fetchers.getUnderlying(self.state_argument))) + ' Oracle'

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

                    fields = f'''makeFields(
                         ['Alert Level :',
                         'Variation :',
                         'Last Value :',
                         'Link to Market :'], 
                         ['{str(level)}',
                         '{str(formatPercent(self.change))}',
                         '{str(formatCurrency(self.value / fetchers.getDecimals(fetchers.getUnderlying(self.state_argument))))}',
                         '{'https://etherscan.io/address/' + str(self.state_argument)}'], 
                         [True, True,True,False])'''

            if (self.alert == 'cash'):
                webhook = os.getenv('WEBHOOK_MARKETS')
                if self.state_function == 'getCash':
                    logging.info(str(self.change) + '% change detected on ' + str(
                        fetchers.getName(self.contract.address))) + ' balance'
                    title = str(formatPercent(self.change)) + ' change detected on ' + str(
                        fetchers.getSymbol(fetchers.getUnderlying(self.contract.address))) + ' Cash balance'

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

                    fields = f'''makeFields(
                         ['Alert Level :',
                         'Variation :',
                         'Last Value :',
                         'Link to Market :'], 
                         ['{str(level)}',
                         '{str(formatPercent(self.change))}',
                         '{str(formatCurrency(self.value / fetchers.getDecimals(fetchers.getUnderlying(self.contract.address))))}',
                         '{'https://etherscan.io/address/' + str(self.contract.address)}'], 
                         [True, True,True,False])'''

                if send:
                    sendWebhook(webhook, title, fields, content, image, color)
                    logging.info(f'Message sent to {webhook}')

            if (self.alert == 'supply'):
                webhook = os.getenv('WEBHOOK_DOLA3CRV')
                if self.state_function == 'totalSupply':
                    logging.info(str(self.change) + '% change detected on ' + str(
                        fetchers.getName(self.contract.address))) + ' total supply'
                    title = str(formatPercent(self.change)) + ' change detected on ' + str(
                        fetchers.getSymbol(fetchers.getUnderlying(self.state_argument))) + ' Supply'

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

                    fields = f'''makeFields(
                         ['Alert Level :',
                         'Variation :',
                         'Last Value :',
                         'Link to Pool :'], 
                         ['{str(level)}',
                         '{str(formatPercent(self.change))}',
                         '{str(formatCurrency(self.value / fetchers.getDecimals(fetchers.getUnderlying(self.contract.address))))}',
                         '{'https://etherscan.io/address/' + str(self.contract.address)}'], 
                         [True, True,True,False])'''

                if send:
                    sendWebhook(webhook, title, fields, content, image, color)
                    logging.info(f'Message Sent to {webhook}')

            if send:
                sendWebhook(webhook, title, fields, content, image, color)


        except Exception as e:
            logging.warning(f'Error in state variation handler')
            logging.error(e)
            #sendError(f'Error in state variation handler : {str(e)}')
            pass

# Define event to handle and logs to the console/send to discord
class HandleEvent(Thread):
    def __init__(self, event, alert, event_name, **kwargs):
        super(HandleEvent, self).__init__(**kwargs)
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
                    '{str(formatCurrency(fetchers.getDola3crvBalances()[0]))}',
                    '{str(formatCurrency(fetchers.getDola3crvBalances()[1]))}',
                    '{str(formatCurrency(fetchers.getDola3crvBalances()[0] + fetchers.getDola3crvBalances()[1]))}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [True,True,True,False,True,True,False,False])'''

                    color = colors.red
                    send = True
                elif (self.event_name == "RemoveLiquidityOne"):
                    title = "DOLA3CRV Pool Liquidity Removal event detected"
                    fields = f'''makeFields(
                    ['Block :',
                    'DOLA Amount :',
                    '3CRV Amount :',
                    'Token Supply :',
                    'DOLA in Pool :',
                    '3CRV in Pool :',
                    'DOLA+3CRV in Pool',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(formatCurrency(tx["args"]["token_amount"] / 1e18))}',
                    '{str(formatCurrency(tx["args"]["coin_amount"] / 1e18))}',
                    '{str(formatCurrency(tx["args"]["token_supply"] / 1e18))}',
                    '{str(formatCurrency(fetchers.getDola3crvBalances()[0]))}',
                    '{str(formatCurrency(fetchers.getDola3crvBalances()[1]))}',
                    '{str(formatCurrency(fetchers.getDola3crvBalances()[0] + fetchers.getDola3crvBalances()[1]))}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                    [True,False,True,False,True,True,False,False])'''
                    color = colors.red
                    send = True
                elif (self.event_name == "AddLiquidity"):
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
                    '{str(formatCurrency(fetchers.getDola3crvBalances()[0]))}',
                    '{str(formatCurrency(fetchers.getDola3crvBalances()[1]))}',
                    '{str(formatCurrency(fetchers.getDola3crvBalances()[0] + fetchers.getDola3crvBalances()[1]))}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                    [True,True,True,False,True,True,False,False])'''

                    color = colors.dark_green
                    send = True
            elif (self.alert in ["lending1", "lending2"]):
                webhook = os.getenv('WEBHOOK_LENDING')
                if (self.event_name == "Mint"):
                    title = "Lending Market : New Deposit event detected for " + str(fetchers.getSymbol(tx["address"]))
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
                                '{str(fetchers.getSymbol(tx["address"]))}',
                                '{str(tx["address"])}',
                                '{str(formatCurrency(tx["args"]["mintAmount"] / fetchers.getDecimals(fetchers.getUnderlying(tx["address"])) * fetchers.getUnderlyingPrice(tx["address"])))}',
                                '{str(formatCurrency(tx["args"]["mintAmount"] / fetchers.getDecimals(fetchers.getUnderlying(tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["mintTokens"] / fetchers.getDecimals(tx["address"])))}',
                                '{str(formatCurrency(fetchers.getSupply(tx["address"])))}',
                                '{str(formatCurrency(fetchers.getCash(tx["address"])))}',
                                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                [True,True,True,False,True,True,True,True,True,False])'''

                    color = colors.blurple
                    send = True
                elif (self.event_name == "Redeem"):
                    title = "Lending Market : New Withdrawal event detected for " + str(fetchers.getSymbol(tx["address"]))
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
                                '{str(fetchers.getSymbol(tx["address"]))}',
                                '{str(tx["address"])}',
                                '{str(formatCurrency(tx["args"]["redeemAmount"] / fetchers.getDecimals(fetchers.getUnderlying(tx["address"])) * fetchers.getUnderlyingPrice(tx["address"])))}',
                                '{str(formatCurrency(tx["args"]["redeemAmount"] / fetchers.getDecimals(fetchers.getUnderlying(tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["redeemTokens"] / fetchers.getDecimals(tx["address"])))}',
                                '{str(formatCurrency(fetchers.getSupply(tx["address"])))}',
                                '{str(formatCurrency(fetchers.getCash(tx["address"])))}',
                                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                [True,True,True,False,True,True,True,True,True,False])'''

                    color = colors.blurple
                    send = True
                elif (self.event_name == "Borrow"):
                    title = "Lending Market : New Borrow event detected for " + str(fetchers.getSymbol(tx["address"]))
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
                                '{str(fetchers.getSymbol(tx["address"]))}',
                                '{str(tx["address"])}',
                                '{str(formatCurrency(tx["args"]["borrowAmount"] / fetchers.getDecimals(fetchers.getUnderlying(tx["address"])) * fetchers.getUnderlyingPrice(tx["address"])))}',
                                '{str(formatCurrency(tx["args"]["borrowAmount"] / fetchers.getDecimals(fetchers.getUnderlying(tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["accountBorrows"] / fetchers.getDecimals(fetchers.getUnderlying(tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["totalBorrows"] / fetchers.getDecimals(fetchers.getUnderlying(tx["address"]))))}',
                                '{str(formatCurrency(fetchers.getSupply(tx["address"])))}',
                                '{str(formatCurrency(fetchers.getCash(tx["address"])))}',
                                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                [True,True,False,True,True,True,True,True,True,True,False])'''

                    color = colors.blurple
                    send = True
                elif (self.event_name == "RepayBorrow"):
                    title = "Lending Market : New Repayment event detected for " + str(fetchers.getSymbol(tx["address"]))

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
                                '{str(fetchers.getSymbol(tx["address"]))}',
                                '{str(tx["address"])}',
                                '{str(formatCurrency(tx["args"]["repayAmount"] / fetchers.getDecimals(fetchers.getUnderlying(tx["address"])) * fetchers.getUnderlyingPrice(tx["address"])))}',
                                '{str(formatCurrency(tx["args"]["repayAmount"] / fetchers.getDecimals(fetchers.getUnderlying(tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["accountBorrows"] / fetchers.getDecimals(fetchers.getUnderlying(tx["address"]))))}',
                                '{str(formatCurrency(tx["args"]["totalBorrows"] / fetchers.getDecimals(fetchers.getUnderlying(tx["address"]))))}',
                                '{str(formatCurrency(fetchers.getSupply(tx["address"])))}',
                                '{str(formatCurrency(fetchers.getCash(tx["address"])))}',
                                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                [True,True,False,True,True,True,True,True,True,True,False])'''

                    color = colors.blurple
                    send = True
                elif (self.event_name == "LiquidateBorrow"):
                    title = "Lending Market New Liquidation event detected for " + str(fetchers.getSymbol(tx["address"]))
                    webhook = os.getenv('WEBHOOK_LIQUIDATIONS')
                    fields = f'''makeFields(
                                ['Block Number :',
                                'Liquidator :',
                                'Borrower :',
                                'Address :',
                                'Seized Token Address :',
                                'Repay Amount :',
                                'Seized Tokens Amount',
                                'Transaction :'],
                                ['{str(tx["blockNumber"])}',
                                '{str(tx["args"]["liquidator"])}',
                                '{str(tx["args"]["borrower"])}',
                                '{str(tx["address"])}',
                                '{str(tx["args"]["cTokenCollateral"])}',
                                '{str(tx["args"]["repayAmount"])}',
                                '{str(tx["args"]["seizeTokens"])}',
                                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                                [True,False,True,True,False,True,True,False])'''

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
                    '{"https://www.inverse.finance/governance/proposals/mills/" + str(fetchers.getProposalCount())}',
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
                content = '<@&945071604642222110>'
                if (self.event_name in ["Expansion"]):
                    title = "Fed " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"

                    fields = f'''makeFields([
                    'Block Number :',
                    'Fed Address :',
                    'Sender :',
                    'Total Supply :',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(tx["address"])}',
                    '{str(tx["args"]["amount"] / 1e18)}',
                    '{str(fetchers.getSupply('0x865377367054516e17014ccded1e7d814edc9ce4') / 1e18)}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [False,False,False,False,False])'''

                    color = colors.dark_red
                    send = True
                if (self.event_name in ["Contraction"]):
                    title = "Fed " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"

                    fields = f'''makeFields([
                    'Block Number :',
                    'Fed Address :',
                    'Sender :',
                    'Total Supply :',
                    'Transaction :'],
                    ['{str(tx["blockNumber"])}',
                    '{str(tx["address"])}',
                    '{str(tx["args"]["amount"] / 1e18)}',
                    '{str(fetchers.getSupply('0x865377367054516e17014ccded1e7d814edc9ce4') / 1e18)}',
                    '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                    [False,False,False,False,False])'''

                    color = colors.dark_green
                    send = True
            elif (self.alert == "swap"):
                webhook = os.getenv('WEBHOOK_SWAP')
                if (self.event_name == "Swap"):
                    image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/838610/1466237/8e64e858-5db5-4692-922d-5f9fe6b7a8c6.jpg"
                    if tx["args"]['amount0In'] == 0:
                        operation = 'Buy ' + str(formatCurrency(tx["args"]['amount0Out'] / fetchers.getDecimals(
                            fetchers.getSushiTokens(tx["address"])[0]))) + " " + str(
                            fetchers.getSushiTokensSymbol(tx["address"])[0])
                        color = colors.dark_green
                        title = "Sushiswap New Buy event detected"
                        send = True
                    else:
                        operation = 'Sell ' + str(formatCurrency(tx["args"]['amount0In'] / fetchers.getDecimals(
                            fetchers.getSushiTokens(tx["address"])[0]))) + " " + str(
                            fetchers.getSushiTokensSymbol(tx["address"])[0])
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
                                '{str(fetchers.getName(tx["address"]))}',
                                '{str(fetchers.getSymbol(tx["address"]))}',
                                '{str(tx["address"])}',
                                '{str(operation)}',
                                '{str(formatCurrency(((tx["args"]["amount0Out"] + tx["args"]["amount0In"]) / fetchers.getDecimals(fetchers.getSushiTokens(tx["address"])[0])) * fetchers.getUnderlyingPrice('0x1637e4e9941d55703a7a5e7807d6ada3f7dcd61b')))}',
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
                            '{str(fetchers.getName(tx["address"]))}',
                            '{str(fetchers.getSymbol(tx["address"]))}',
                            '{str(tx["address"])}',
                            '{str(tx["args"]["amountADesired"] / 1e18)}',
                            '{str(tx["args"]["amountBDesired"] / 1e18)}',
                            '{str(tx["args"]["amountAMin"] / 1e18)}',
                            '{str(tx["args"]["amountBMin"] / 1e18)}',
                            '{str(fetchers.getBalance(tx["address"], fetchers.getSushiTokens(tx["address"][0])))}',
                            '{str(fetchers.getBalance(tx["address"], fetchers.getSushiTokens(tx["address"][1])))}',
                            '{str(fetchers.getSupply(tx["address"]))}',
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
                            '{str(fetchers.getName(tx["address"]))}',
                            '{str(fetchers.getSymbol(tx["address"]))}',
                            '{str(tx["address"])}',
                            '{str(tx["args"]["amount0"] / 1e18)}',
                            '{str(tx["args"]["amount1"] / 1e18)}',
                            '{str(fetchers.getBalance(tx["address"], fetchers.getSushiTokens(tx["address"][0])))}',
                            '{str(fetchers.getBalance(tx["address"], fetchers.getSushiTokens(tx["address"][1])))}',
                            '{str(fetchers.getSupply(tx["address"]))}',
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
            elif (self.alert == "test"):
                webhook = os.getenv('WEBHOOK_TESTING')
                if (self.event_name in ["Transfer"]):
                    title = "Test Transfer event detected"
                    content = '<@578956365205209098>'
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

            if send:
                sendWebhook(webhook, title, fields, content, image, color)
                logging.info(f'Message Sent to {webhook}')

        except Exception as e:
            logging.warning('Error in event handler')
            logging.error(e)
            #sendError(f'Error in event handler : {str(e)}')
            pass

# Define state change to handle and logs to the console/send to discord
class HandleTx(Thread):
    def __init__(self, tx, alert, contract, **kwargs):
        super(HandleTx, self).__init__(**kwargs)
        self.contract = contract
        self.alert = alert
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
                title = str('Tx detected on ' + str(self.tx["address"]) + ' Multisig')
                content = ''
                send = True
                fields = f'''makeFields(
                     ['Multisig :',
                     'Link to transaction :'], 
                     ['{str(self.tx["address"])}',
                     '{"https://etherscan.io/tx/" + str(self.tx["transactionHash"])}'], 
                     [False,False])'''

            if send:
                sendWebhook(webhook, title, fields, content, image, color)
                logging.info(f'Message Sent to {str(webhook)}')


        except Exception as e:
            logging.warning('Error in tx handler')
            logging.error(e)
            #sendError(str(f'Error in tx handler : {str(e)}'))
            pass