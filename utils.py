import os
import json
import re
import pandas as pd
import requests
import fetchers
import os
import logging
import sys

from dotenv import load_dotenv
from web3 import Web3
from threading import Thread
from datetime import datetime


# Define a Thread to listen separately on each state change
class StateChangeListener(Thread):
    def __init__(self, web3, alert, contract, state_function,argument, **kwargs):
        super(StateChangeListener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.state_function = state_function
        self.argument = argument
        self.value = eval(f'''self.contract.functions.{self.state_function}('{self.argument}').call()''')

    def run(self):
        old_value = self.value
        while True:
            try:
                #print(f'''self.contract.functions.{self.function}('{str(self.argument)}').call()''')
                self.value = eval(f'''self.contract.functions.{self.state_function}('{self.argument}').call()''')
                change = (self.value  / old_value) - 1
                old_value = self.value
                if change != 0:
                    handle_state_variation(change)

            except Exception as e:
                #logging.warning("Error in State Change Listener " + str(self.alert) + "-" + str(self.contract.address) + "-" + str(
                #    self.event))
                logging.error(e)
                sendError("Error in State Change Listener " + "\n"+str(e))
                pass

# Define a Thread to listen separately on each contract/event in the contract file
class EventListener(Thread):
    def __init__(self, web3, alert, contract, event_name, **kwargs):
        super(EventListener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.event_name = event_name
        self.event_filter = []

    def run(self):
        self.event_filter = eval(f'self.contract.events.{self.event_name}.createFilter(fromBlock="latest")')
        while True:
            try:
                for event in self.event_filter.get_new_entries():
                    logging.info(str(datetime.now()) + " Event found in " + str(self.alert) + "-" + str(
                        self.contract.address) + "-" + str(self.event_name))

                    handle_event(event, self.alert, self.event_name)
                    # Add triggers here
            except Exception as e:
                logging.warning("Error in Event Listener " + str(self.alert) + "-" + str(self.contract.address) + "-" + str(
                    self.event_name))
                logging.error(e)
                sendError("Error in Event Listener " + "\n"+str(e))
                pass

# Define event to handle and print to the console/send to discord
# Need to pass the web3 and contract args to load proper events functions
# Get an event and decide if it sends a message or not to the appropriate webhook base on the condition 'send'
# defined in the event
def handle_event(event, alert, event_name):
    try:
        tx = json.loads(Web3.toJSON(event))

        # Print result table and start writing message
        logging.info(str(datetime.now()) + " " + str(tx))
        send = False
        image = ''
        color = ''
        content = ''

        if (alert == "dola3crv"):
            webhook = os.getenv('WEBHOOK_DOLA3CRV')
            image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/833844/1457892/bccc1e5b-4b60-4b28-85da-fbd558a2fd69.jpg"
            if (event_name == "RemoveLiquidity"):
                title = "DOLA3CRV Pool Liquidity Removal event detected"
                fields = f'''makeFields(
                ['Block :',
                'DOLA Amount :',
                '3CRV Amount :',
                'Address :',
                'DOLA in Pool :',
                '3CRV in Pool :',
                'Transaction :'],
                ['{str(tx["blockNumber"])}',
                '{str(formatCurrency(tx["args"]["token_amounts"][0] / 1e18))}',
                '{str(formatCurrency(tx["args"]["token_amounts"][1] / 1e18))}',
                '{str(tx["address"])}',
                '{str(formatCurrency(fetchers.getDola3crvBalances()[0]))}',
                '{str(formatCurrency(fetchers.getDola3crvBalances()[1]))}',
                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                [True,True,True,False,True,True,False])'''

                color = colors.red
                send = True
            elif (event_name == "RemoveLiquidityOne"):
                title = "DOLA3CRV Pool Liquidity Removal event detected"
                fields = f'''makeFields(
                ['Block :',
                'DOLA Amount :',
                '3CRV Amount :',
                'Token Supply :',
                'DOLA in Pool :',
                '3CRV in Pool :',
                'Transaction :'],
                ['{str(tx["blockNumber"])}',
                '{str(formatCurrency(tx["args"]["token_amount"] / 1e18))}',
                '{str(formatCurrency(tx["args"]["coin_amount"] / 1e18))}',
                '{str(formatCurrency(tx["args"]["token_supply"] / 1e18))}',
                '{str(formatCurrency(fetchers.getDola3crvBalances()[0]))}',
                '{str(formatCurrency(fetchers.getDola3crvBalances()[1]))}',
                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                [True,False,True,False,True,True,False])'''
                color = colors.red
                send = True
            elif (event_name == "AddLiquidity"):
                title = "DOLA3CRV Pool Liquidity Add event detected"
                fields = f'''makeFields(
                ['Block :',
                'DOLA Amount :',
                '3CRV Amount :',
                'Address :',
                'DOLA in Pool :',
                '3CRV in Pool :',
                'Transaction :'],
                ['{str(tx["blockNumber"])}',
                '{str(formatCurrency(tx["args"]["token_amounts"][0] / 1e18))}',
                '{str(formatCurrency(tx["args"]["token_amounts"][1] / 1e18))}',
                '{str(tx["address"])}',
                '{str(formatCurrency(fetchers.getDola3crvBalances()[0]))}',
                '{str(formatCurrency(fetchers.getDola3crvBalances()[1]))}',
                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                [True,True,True,False,True,True,False])'''

                color = colors.dark_green
                send = True
        elif (alert == "lending"):
            webhook = os.getenv('WEBHOOK_LENDING')
            if (event_name == "Mint"):
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
            elif (event_name == "Redeem"):
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
            elif (event_name == "Borrow"):
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
            elif (event_name == "RepayBorrow"):
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
            elif (event_name == "LiquidateBorrow"):
                title = "Lending Market New Liquidation event detected for " + + str(fetchers.getSymbol(tx["address"]))
                webhook = os.getenv('WEBHOOK_LIQUIDATIONS')
                fields = f'''makeFields(
                            ['Block Number :',
                            'Liquidator :',
                            'Borrower :',
                            'Address :',
                            'Seized Token Address :',
                            'Repay Amount :',
                            'Seized Tokens Amount',
                            'Total Supply :',
                            'Transaction :'],
                            ['{str(tx["blockNumber"])}',
                            '{str(tx["args"]["liquidator"])}',
                            '{str(tx["args"]["borrower"])}',
                            '{str(tx["address"])}',
                            '{str(tx["args"]["cTokenCollateral"])}',
                            '{str(tx["args"]["repayAmount"])}',
                            '{str(tx["args"]["seizeTokens"])}',
                            '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                            [True,False,True,True,False,True,True,True,False])'''

                color = colors.blurple
                send = True
        elif (alert == "governance"):
            content = "<@899302193608409178>"
            webhook = os.getenv('WEBHOOK_GOVERNANCE')
            if (event_name == "ProposalCreated"):
                title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event "]))

                fields = f'''makeFields(
                ['Block Number :',
                'Targets :',
                'Description :',
                'Transaction :'],
                ['{str(tx["blockNumber"])}',
                '{str(tx["args"]["calldatas"])}',
                '{str(tx["args"]["description"])[0:30]}',
                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                [False,False,False,False,False,False,False])'''

                color = colors.blurple
                send = True
            elif (event_name in ["ProposalCanceled"]):
                title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event"]))

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
            elif (event_name in ["ProposalQueued"]):
                title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event"]))

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
            elif (event_name in ["ProposalExecuted"]):
                title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event"]))

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
        elif (alert == "fed"):
            webhook = os.getenv('WEBHOOK_FED')
            image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/22517/1128427/3084f915-b906-4fdf-ac8c-ad5c0ce57e2b.jpg"
            content = '<@945071604642222110>'
            if (event_name in ["Expansion"]):
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
            if (event_name in ["Contraction"]):
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
        elif (alert == "swap"):
            webhook = os.getenv('WEBHOOK_SWAP')
            if (event_name == "Swap"):
                image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/838610/1466237/8e64e858-5db5-4692-922d-5f9fe6b7a8c6"
                title = "Sushi New Swap event detected"
                content = ''
                if tx["args"]['amount0In'] == 0:
                    operation = 'Buy ' + \
                                str(formatCurrency(tx["args"]['amount0Out'] / fetchers.getDecimals(
                                    fetchers.getSushiTokens(tx["address"])[0]))) + \
                                ' ' + str(fetchers.getSushiTokensSymbol(tx["address"])[0]) + \
                                ' with ' + \
                                str(formatCurrency(tx["args"]['amount0In'] / fetchers.getDecimals(
                                    fetchers.getSushiTokens(tx["address"])[1])) + \
                                    ' ' + str(fetchers.getSushiTokensSymbol(tx["address"])[1]))
                else:
                    operation = 'Sell ' + \
                                str(formatCurrency(tx["args"]['amount0In'] / fetchers.getDecimals(
                                    fetchers.getSushiTokens(tx["address"])[0]))) + \
                                ' ' + str(fetchers.getSushiTokensSymbol(tx["address"])[0]) + \
                                ' for ' + \
                                str(formatCurrency(tx["args"]['amount0Out'] / fetchers.getDecimals(
                                    fetchers.getSushiTokens(tx["address"])[1]))) + \
                                ' ' + str(fetchers.getSushiTokensSymbol(tx["address"])[1])

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
                '{str((formatCurrency(tx["args"]['amount0Out'] / fetchers.getDecimals(fetchers.getSushiTokens(tx["address"])[0])) + formatCurrency(tx["args"]['amount0In'] / fetchers.getDecimals(fetchers.getSushiTokens(tx["address"])[0]))) * fetchers.getUnderlyingPrice(fetchers.getUnderlying(fetchers.getSushiTokens(tx["address"])[0])))}',
                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                [True,True,True,False,False,False])'''

                color = colors.blurple
                send = True
            elif (event_name in ["Mint"]):
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
            elif (event_name in ["Burn"]):
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
        elif (alert == "unitroller"):
            webhook = os.getenv('WEBHOOK_UNITROLLER')
            if (event_name in ["NewBorrowCap", "NewSupplyCap", "NewCollateralFactor", "NewPriceOracle", "MarketListed",
                             "MarketUnlisted"]):
                title = "Comptroller Markets " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"
                content = '<@945071604642222110>'
                fields = f'''makeFields(
                ['Block Number :',
                'Address :',
                'All Markets :',
                'Comptroller :',
                'Transaction :'],
                ['{str(tx["blockNumber"])}',
                '{str(tx["address"])}',
                '{str(fetchers.getAllMarkets())}',
                '{str(fetchers.getComptroller())}',
                '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                [False,False,False,False,False])'''

                color = colors.dark_orange
                send = True
        if send:
            sendWebhook(webhook, title, fields, content, image, color)

    except Exception as e:
        logging.warning('Error in event handler')
        sendError("Error in event handler " + "\n" + str(e))
        logging.error(e)
        pass

def handle_state_variation(value,alert,state_function):
    try:
        send = False
        image = ''
        color = colors.blurple
        if alert=='oracle':
            if state_function =='getUnderlyingPrice':
                content = formatPercent(value) + ' change detected !'
                print(str(value) + ' change detected on ' + str(self.argument))
                fields = makeFields(['Test', 'Test2'], ['1', '2'], [True, True])
                webhook = os.getenv('WEBHOOK_TESTING')
                title = "Test State Price Alert"
                image = ""
                send = True

        if send == True:
             sendWebhook(webhook, title, fields, content, image, color)
        print('Message Sent !')
    except Exception as e:
        logging.warning('Error in state variation handler')
        sendError("Error in state variation handler " + "\n" + str(e))
        logging.error(e)
        pass

# Create fields for the embed content
def makeFields(names, values, inline):
    try:
        fields = []
        a = names
        b = values
        c = inline

        for i in range(0, len(a)):
            fields.append({"name": a[i], "value": b[i], "inline": c[i]})

        # print(fields = json.dumps(fields, indent=1))
        return fields
    except Exception as e:
        logging.warning('Error in makeFields ')
        sendError("Error in sending makeFields " + "\n" + str(e))
        logging.error(e)
        pass

# Send a webhook with embed (title,fields,image,url,color)
# content is used for the body of the message and tagging roles
def sendWebhook(webhook, title, fields, content, imageurl, color):
    try:
        data = f"""{{"content": '{content}'}}"""
        data = eval(data)
        embed = f"""[{{"fields":{fields},"title": '{title}',"color": '{color}',"image":{{"url": '{imageurl}'}}}}]"""
        data["embeds"] = eval(embed)
        result = requests.post(webhook, json=data)

        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(err)
        sendError("Error in sending message to webhook " + "\n" + str(err))
        pass
    else:
        logging.info("Embed delivered successfully to webhook code {}.".format(result.status_code))

# Send an error to the appropriate discord webhook (modify in .env file)
def sendError(content):
    load_dotenv()
    webhook = os.getenv('WEBHOOK_ERRORS')
    try:
        data = f"""{{"content": '{content}'}}"""
        data = eval(data)
        result = requests.post(webhook, json=data)

        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(err)
        sendError("Error in sending error to webhook " + "\n" + str(err))
        pass
    else:
        logging.info("Error delivered successfully to error channel code {}.".format(result.status_code))

# Format to 0,000.00
def formatCurrency(value):
    value = "{:,.2f}".format(value)
    return value

# Format to 00.00 %
def formatPercent(value):
    value = "{:.2%}".format(value)
    return value

def LoggerParams():
    # Logger config
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    # Mute warning when pool is full
    logging.getLogger("urllib3").setLevel(logging.ERROR)

# Color shortcut-class for discord embed notification
class colors:
    default = 0
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da
    greyple = 0x99aab5
