import os
import json
import re
import pandas as pd
import logging
import requests
import fetchers
from web3 import Web3
from threading import Thread
from datetime import datetime


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
            self.event_filter = eval(f'self.contract.events.{self.function}.createFilter(fromBlock="latest")')
            while True:
                for event in self.event_filter.get_new_entries():
                    print(str(datetime.now()) + " Event found in " + str(self.alert) + "-" + str(
                        self.contract.address) + "-" + str(self.function))

                    handle_event(event, self.web3, self.alert, self.contract, self.function, self.state_functions,
                                 self.webhook)
        except Exception as e:
            print("Error in Event Listener " + str(self.alert) + "-" + str(self.contract.address) + "-" + str(
                self.function))
            print(e)
            pass


# Define function to handle events and print to the console/send to discord
def handle_event(event, web3, alert, contract, function, state_functions, webhook):
    try:
        tx = json.loads(Web3.toJSON(event))
        print(str(datetime.now()) + " " + str(tx))
        results = []

        # Collect state function results
        for i in state_functions:
            state_result = eval(f"contract.functions.{i}.call()")
            results.append(state_result)

        # Build table
        state_results = pd.DataFrame([results])
        state_results = state_results.set_axis(state_functions, axis=1, inplace=False)

        # Print result table and go to trigger routine
        print(str(datetime.now()) + " " + str(state_results))
        handle_trigger(alert, tx, function, state_results, webhook)

    except Exception as e:
        print('Error in event handler')
        print(e)
        pass


# Get an event and define if it sends a message or not to the appropriate webhook
def handle_trigger(alert, tx, function, state_results, webhook):
    try:
        send = False
        image = ''
        color = ''

        if (alert == "dola3crv"):
            image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/833844/1457892/bccc1e5b-4b60-4b28-85da-fbd558a2fd69.jpg"
            if (function == "RemoveLiquidity"):
                title = "DOLA3CRV Pool " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"
                body = f'''makeFields(['Block :','Value :','Total Supply :','Address :','Sender :','Receiver :','Transaction :'],
                ['{str(tx["blockNumber"])}', '{str(tx["args"]["value"])/1e18}','{str(state_results.at[0, "totalSupply()"] / 1e18)}', '{str(tx["address"]) }',
                '{str(tx["args"]["sender"])}', '{str(tx["args"]["receiver"])}', '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                [True,True,True,False,True,True,False])'''

                color = colors.red
                send = True
            elif (function == "RemoveLiquidityOne"):
                title = "DOLA3CRV Pool " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"
                body = f'''makeFields(['Block :','Token Amount :','Coin Amount :','Token Supply :','Provider :','Transaction :'],
                ['{str(tx["blockNumber"])}', '{str(tx["args"]["token_amount"])/1e18}','{str(tx["args"]["coin_amount"])/1e18}','{str(tx["args"]["token_supply"])/1e18}',
                '{str(tx["args"]["provider"])}', '{"https://etherscan.io/tx/" + str(tx["transactionHash"])}' ],
                [True,False,True,False,True,False])'''
                color = colors.red
                send = True
            elif (function == "AddLiquidity"):
                title = "DOLA3CRV Pool " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"
                body = f'''makeFields(['Block :','Token 0 Amount :','Token 1 Amount :','Fees 0 Amount :','Fees 1 Amount :','Balance 0 :','Balance 1 :','Token Supply :','Address :','Transaction :'],
                ['{str(tx["blockNumber"])}', '{str(tx["args"]["token_amounts"][0])/1e18}','{str(tx["args"]["token_amounts"][1])/1e18}','{str(tx["args"]["fees"][0] / 1e18)}',
                '{str(tx["args"]["fees"][1] / 1e18)}','{str(state_results.at[0, "balances(0)"] / 1e18)}',{str(state_results.at[0, "balances(1)"] / 1e18)},
                '{str(tx["address"])}','{ "https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                [False,True,True,True,True,False,True,True,False,False])'''

                color = colors.dark_green
                send = True
        elif (alert == "lending"):
            if (function == "Mint"):
                title = "Lending Market : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event"])) + " event detected for " + str(
                    state_results.at[0, "name()"])

                body = f''''makeFields(['Block Number :','Minter :','Address :','Mint Amount :','Mint Tokens :','Total Supply','Total Cash :','Transaction :'],
                ['{str(tx["blockNumber"])}','{str(tx["args"]["minter"])}','{str(tx["address"])}','{str(tx["args"]["mintAmount"])}','{str(tx["args"]["mintTokens"])}',
                '{str(state_results.at[0, "totalSupply()"])}','{str(state_results.at[0, "getCash()"])}','{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                [True,True,True,False,True,True,True,False])'''

                color = colors.blurple
                send = True
            elif (function == "Redeem"):
                title = "Lending Market : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event"])) + " event detected for " + str(
                    state_results.at[0, "name()"])

                body = f''''makeFields(['Block Number :','Minter :','Address :','Redeem Amount :','Redeem Tokens :','Total Supply','Total Cash :','Transaction :'],
                ['{str(tx["blockNumber"])}','{str(tx["args"]["redeemer"])}','{str(tx["address"])}','{str(tx["args"]["redeemAmount"])}','{str(tx["args"]["redeemTokens"])}',
                '{str(state_results.at[0, "totalSupply()"])}','{str(state_results.at[0, "getCash()"])}','{"https://etherscan.io/tx/" + str(tx["transactionHash"])}'],
                [True,True,True,False,True,True,True,False])'''

                color = colors.blurple
                send = True
            elif (function == "Borrow"):
                title = "Lending Market : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event"])) + " event detected for " + str(
                    state_results.at[0, "name()"])

                body = f''''makeFields(['Block Number :','Borrower :','Address :','Borrow Amount :','Account Borrows :','Total Borrows :','Total Supply :','Total Cash :','Transaction :'],
                ['{str(tx["args"]["borrower"]) }','{str(tx["address"])}','{str(tx["args"]["borrowAmount"])}','{str(tx["args"]["accountBorrows"])}','{str(tx["args"]["totalBorrows"])}',
                '{str(state_results.at[0, "totalSupply()"]) }','{str(state_results.at[0, "getCash()"]) }','{"https://etherscan.io/tx/" + str(tx["transactionHash"])}','{}'],
                [True,True,False,True,True,True,True,False])'''

                color = colors.blurple
                send = True
            elif (function == "RepayBorrow"):
                title = "Lending Market : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event"])) + " event detected for " + str(
                    state_results.at[0, "name()"])

                body = f''''makeFields(['','','','','','','',''],
                ['{}','{}','{}','{}','{}','{}','{}','{}'],
                [True,True,True,True,True,True,True,True])'''

                body = ("Block Number : " + str(tx["blockNumber"]) +
                        "\n" + "Payer : " + str(tx["args"]["payer"]) +
                        "\n" + "Address : " + str(tx["address"]) +
                        "\n" + "Repaid Amount : " + str(tx["args"]["repayAmount"]) +
                        "\n" + "Account Borrows : " + str(tx["args"]["accountBorrows"]) +
                        "\n" + "Total Borrows : " + str(tx["args"]["totalBorrows"]) +
                        "\n" + "Total Supply : " + str(state_results.at[0, "totalSupply()"]) +
                        "\n" + "Transaction : https://etherscan.io/tx/" + str(tx["transactionHash"]))
                color = colors.blurple
            elif (function == "LiquidateBorrow"):
                title = "Lending Market New : " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event"])) + " event detected for " + str(
                    state_results.at[0, "name()"])

                body = f''''makeFields(['','','','','','','',''],
                ['{}','{}','{}','{}','{}','{}','{}','{}'],
                [True,True,True,True,True,True,True,True])'''

                body = ("Block Number : " + str(tx["blockNumber"]) +
                        "\n" + "Liquidator : " + str(tx["args"]["liquidator"]) +
                        "\n" + "Borrower : " + str(tx["args"]["borrower"]) +
                        "\n" + "Address : " + str(tx["address"]) +
                        "\n" + "Seized Token Address: " + str(tx["args"]["cTokenCollateral"]) +
                        "\n" + "Repay Amount : " + str(tx["args"]["repayAmount"]) +
                        "\n" + "Seized Tokens Amount : " + str(tx["args"]["seizeTokens"]) +
                        "\n" + "Total Supply : " + str(state_results.at[0, "totalSupply()"]) +
                        "\n" + "Transaction : https://etherscan.io/tx/" + str(tx["transactionHash"]))
                color = colors.blurple
        elif (alert == "governance"):
            if (function == "ProposalCreated"):
                title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event <@899302193608409178>"]))

                body = f''''makeFields(['','','','','','','',''],
                ['{}','{}','{}','{}','{}','{}','{}','{}'],
                [True,True,True,True,True,True,True,True])'''

                body = ("Block Number : " + str(tx["blockNumber"]) +
                        "\n" + "Targets : " + str(tx["args"]["targets"]) +
                        "\n" + "Values : " + str(tx["args"]["values"]) +
                        "\n" + "Signatures : " + str(tx["args"]["signatures"]) +
                        "\n" + "Call Data : " + str(tx["args"]["calldatas"]) +
                        "\n" + "Description : " + str(tx["args"]["description"]) +
                        "\n" + "Transaction : https://etherscan.io/tx/" + str(tx["transactionHash"]))
                color = colors.blurple
            elif (function in ["ProposalCanceled"]):
                title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event <@899302193608409178>"]))

                body = f''''makeFields(['','','','','','','',''],
                ['{}','{}','{}','{}','{}','{}','{}','{}'],
                [True,True,True,True,True,True,True,True])'''

                body = ("Block Number : " + str(tx["blockNumber"]) +
                        "\n" + "Proposal Number : " + str(tx["args"]["id"]) +
                        "\n" + "Proposal : https://www.inverse.finance/governance/proposals/mills/" + str(
                            tx["args"]["id"]) +
                        "\n" + "Transaction : https://etherscan.io/tx/" + str(tx["transactionHash"]))
                color = colors.dark_red
            elif (function in ["ProposalQueued"]):
                title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event <@899302193608409178>"]))

                body = f''''makeFields(['','','','','','','',''],
                ['{}','{}','{}','{}','{}','{}','{}','{}'],
                [True,True,True,True,True,True,True,True])'''

                body = ("Block Number : " + str(tx["blockNumber"]) +
                        "\n" + "Proposal Number : " + str(tx["args"]["id"]) +
                        "\n" + "Proposal : https://www.inverse.finance/governance/proposals/mills/" + str(
                            tx["args"]["id"]) +
                        "\n" + "Transaction : https://etherscan.io/tx/" + str(tx["transactionHash"]))
                color = colors.blurple
            elif (function in ["ProposalExecuted"]):
                title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                         str(tx["event <@899302193608409178>"]))

                body = f''''makeFields(['','','','','','','',''],
                ['{}','{}','{}','{}','{}','{}','{}','{}'],
                [True,True,True,True,True,True,True,True])'''

                body = ("Block Number : " + str(tx["blockNumber"]) +
                        "\n" + "Proposal Number : " + str(tx["args"]["id"]) +
                        "\n" + "Proposal : https://www.inverse.finance/governance/proposals/mills/" + str(
                            tx["args"]["id"]) +
                        "\n" + "Transaction : https://etherscan.io/tx/" + str(tx["transactionHash"]))
                color = colors.dark_green
        elif (alert == "fed"):
            image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/22517/1128427/3084f915-b906-4fdf-ac8c-ad5c0ce57e2b.jpg"
            if (function in ["Expansion"]):
                title = "Fed " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"

                body = f''''makeFields(['','','','','','','',''],
                ['{}','{}','{}','{}','{}','{}','{}','{}'],
                [True,True,True,True,True,True,True,True])'''

                body = ("Block Number : " + str(tx["blockNumber"]) +
                        "\n" + "Fed Address : " + str(tx["address"]) +
                        "\n" + "Sender : " + str(tx["args"]["amount"] / 1e18) +
                        "\n" + "Total Supply : " + str(state_results.at[0, "supply()"] / 1e18) +
                        "\n" + "Transaction : https://etherscan.io/tx/" + str(tx["transactionHash"]))
                color = colors.dark_red
            if (function in ["Expansion"]):
                title = "Fed " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"

                body = f''''makeFields(['','','','','','','',''],
                ['{}','{}','{}','{}','{}','{}','{}','{}'],
                [True,True,True,True,True,True,True,True])'''

                body = ("Block Number : " + str(tx["blockNumber"]) +
                        "\n" + "Fed Address : " + str(tx["address"]) +
                        "\n" + "Sender : " + str(tx["args"]["amount"] / 1e18) +
                        "\n" + "Total Supply : " + str(state_results.at[0, "supply()"] / 1e18) +
                        "\n" + "Transaction : https://etherscan.io/tx/" + str(tx["transactionHash"]))
                color = colors.dark_green
        elif (alert == "sushi"):
            if (function == "Swap"):
                title = "Sushi New " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"

                body = f''''makeFields(['','','','','','','',''],
                ['{}','{}','{}','{}','{}','{}','{}','{}'],
                [True,True,True,True,True,True,True,True])'''

                body = ("Block Number : " + str(tx["blockNumber"]) +
                        "\n" + "Address : " + str(tx["address"]) +
                        "\n" + "Sender : " + str(tx["args"]["sender"]) +
                        "\n" + "To : " + str(tx["args"]["to"]) +
                        "\n" + "Amount0In : " + str(tx["args"]["amount0In"] / 1e18) +
                        "\n" + "Amount0Out : " + str(tx["args"]["amount0Out"] / 1e18) +
                        "\n" + "Amount1In : " + str(tx["args"]["amount1In"] / 1e18) +
                        "\n" + "Amount1Out : " + str(tx["args"]["amount1Out"] / 1e18) +
                        "\n" + "Symbol : " + str(state_results.at[0, "symbol()"]) +
                        "\n" + "Name : " + str(state_results.at[0, "name()"]) +
                        # "\n" + "price0CumulativeLast : " + str(state_results.at[0, "price0CumulativeLast()"]) +
                        # "\n" + "price1CumulativeLast : " + str(state_results.at[0, "price1CumulativeLast()"]) +
                        "\n" + "Token 0 : " + str(state_results.at[0, "token0()"]) +
                        "\n" + "Token 1 : " + str(state_results.at[0, "token1()"]) +
                        "\n" + "Total Supply : " + str(state_results.at[0, "totalSupply()"] / 1e18) +
                        "\n" + "Total Reserves 0 : " + str(state_results.at[0, "getReserves()"][0] / 1e18) +
                        "\n" + "Total Reserves 1 : " + str(state_results.at[0, "getReserves()"][1] / 1e18) +
                        "\n" + "Transaction : https://etherscan.io/tx/" + str(tx["transactionHash"]))
                color = colors.blurple
            elif (function in ["Mint"]):
                title = "Sushi New " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"

                body = f''''makeFields(['','','','','','','',''],
                ['{}','{}','{}','{}','{}','{}','{}','{}'],
                [True,True,True,True,True,True,True,True])'''


                body = ("Block Number : " + str(tx["blockNumber"]) +
                        "\n" + "Address : " + str(tx["address"]) +
                        "\n" + "Sender : " + str(tx["args"]["sender"]) +
                        "\n" + "To : " + str(tx["args"]["to"]) +
                        "\n" + "tokenA : " + str(tx["args"]["tokenA"]) +
                        "\n" + "tokenB : " + str(tx["args"]["tokenB"]) +
                        "\n" + "amountADesired : " + str(tx["args"]["amountADesired"] / 1e18) +
                        "\n" + "amountBDesired : " + str(tx["args"]["amountBDesired"] / 1e18) +
                        "\n" + "amountADesired : " + str(tx["args"]["amountAMin"] / 1e18) +
                        "\n" + "amountBDesired : " + str(tx["args"]["amountBMin"] / 1e18) +
                        # "\n" + "price0CumulativeLast : " + str(state_results.at[0, "price0CumulativeLast()"]) +
                        # "\n" + "price1CumulativeLast : " + str(state_results.at[0, "price1CumulativeLast()"]) +
                        "\n" + "Token 0 : " + str(state_results.at[0, "token0()"]) +
                        "\n" + "Token 1 : " + str(state_results.at[0, "token1()"]) +
                        "\n" + "Total Supply : " + str(state_results.at[0, "totalSupply()"] / 1e18) +
                        "\n" + "Total Reserves 0 : " + str(state_results.at[0, "getReserves()"][0] / 1e18) +
                        "\n" + "Total Reserves 1 : " + str(state_results.at[0, "getReserves()"][1] / 1e18) +
                        "\n" + "Transaction : https://etherscan.io/tx/" + str(tx["transactionHash"]))
                color = colors.dark_green
            elif (function in ["Burn"]):
                title = "Sushi New " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"

                body = f''''makeFields(['','','','','','','',''],
                ['{}','{}','{}','{}','{}','{}','{}','{}'],
                [True,True,True,True,True,True,True,True])'''


                body = ("Block Number : " + str(tx["blockNumber"]) +
                        "\n" + "Address : " + str(tx["address"]) +
                        "\n" + "Sender : " + str(tx["args"]["sender"]) +
                        "\n" + "To : " + str(tx["args"]["to"]) +
                        "\n" + "Amount 0 : " + str(tx["args"]["amount0"] / 1e18) +
                        "\n" + "Amount 1 : " + str(tx["args"]["amount1"] / 1e18) +
                        "\n" + "Total Supply : " + str(state_results.at[0, "totalSupply()"] / 1e18) +
                        "\n" + "Total Reserves 0 : " + str(state_results.at[0, "getReserves()"][0] / 1e18) +
                        "\n" + "Total Reserves 1 : " + str(state_results.at[0, "getReserves()"][1] / 1e18) +
                        "\n" + "Transaction : https://etherscan.io/tx/" + str(tx["transactionHash"]))
                color = colors.dark_red
        elif (alert == "unitroller"):
            if (function in ["NewBorrowCap", "NewSupplyCap", "NewCollateralFactor", "NewPriceOracle", "MarketListed",
                             "MarketUnlisted"]):
                title = "Comptroller Markets " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx["event"])) + " event detected"

                body = f''''makeFields(['','','','','','','',''],
                ['{}','{}','{}','{}','{}','{}','{}','{}'],
                [True,True,True,True,True,True,True,True])'''


                body = ("Block Number : " + str(tx["blockNumber"]) +
                        "\n" + "Address : " + str(tx["address"]) +
                        "\n" + "Comptroller : " + str(state_results.at[0, "getAllMarkets()"]) +
                        "\n" + "Comptroller : " + str(state_results.at[0, "comptroller()"]) +
                        "\n" + "Transaction : https://etherscan.io/tx/" + str(tx["transactionHash"]) +
                        "\n" + "Transaction : " + str(tx))
                color = colors.dark_orange

        if send:
            sendWebhook(webhook, title, body, image, color)

    except Exception as e:
        print('Error in trigger ')
        print(e)
        pass


def sendWebhook(webhook, title, fields, imageurl, color):
    data = {
        # "content": "message content"
        # "username" : "custom username"
    }

    embed = f'[{{"fields":{fields},"title": "{title}","color": "{color}","image":{{"url": "{imageurl}"}}}}]'
    data["embeds"] = eval(embed)
    result = requests.post(webhook, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Embed delivered successfully to webhook code {}.".format(result.status_code))


def formatCurrency(value):
    value = "{:,.2f}".format(value)
    return value


def formatPercent(value):
    value = "{:.2%}".format(value)
    return value


def makeFields(names, values, inline):
    fields = []

    a = names
    b = values
    c = inline

    for i in range(0, len(a)):
        fields.append({"name": a[i], "value": b[i], "inline": c[i]})

    print(json.dumps(fields, indent=1))

    return fields
