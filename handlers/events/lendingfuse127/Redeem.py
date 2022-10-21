import os, json
from helpers import *
from fetchers import *
from dotenv import load_dotenv

load_dotenv()


class message():
    def __init__(self, web3, tx):
        self.web3 = web3
        self.tx = tx
        self.webhook = ''
        self.title = ''
        self.content = ''
        self.fields = ''
        self.color = colors.blurple
        self.image = ''
        self.send = False

    def compose(self):
        address = self.tx["address"]
        blockNumber = self.tx["blockNumber"]
        transactionHash = self.tx["transactionHash"]

        market_symbol = getSymbol(self.web3, address)
        market_decimals = getDecimals(self.web3, address)
        underlying_address = getUnderlyingFuse(self.web3, address)
        underlying_decimals = getDecimals(self.web3, underlying_address)
        underlying_price = getUnderlyingPriceFuse(self.web3, address)
        market_supply = getSupply(self.web3, address)
        market_cash = getCash(self.web3, address)

        self.webhook = os.getenv('WEBHOOK_127')
        self.title = "Lending Market : New Withdrawal event detected for " + str(market_symbol)
        self.fields = [{"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline": False},
                  {"name": 'Redeemer :', "value": str(f'[{self.tx["args"]["redeemer"]}](https://etherscan.io/address/{self.tx["args"]["redeemer"]})'),"inline": True},
                  {"name": 'Market Symbol :', "value": str(market_symbol), "inline": True},
                  {"name": 'Market Address :', "value": str(f'[{address}](https://etherscan.io/address/{address})'),"inline": False},
                  {"name": 'ETH Value', "value": str(formatCurrency(self.tx["args"]["redeemAmount"] / underlying_decimals * underlying_price)),"inline": True},
                  {"name": 'Redeem Amount :',"value": str(formatCurrency(self.tx["args"]["redeemAmount"] / underlying_decimals)), "inline": True},
                  {"name": 'Redeem Tokens :',"value": str(formatCurrency(self.tx["args"]["redeemTokens"] / market_decimals)), "inline": True},
                  {"name": 'Total Supply', "value": str(formatCurrency(market_supply)), "inline": True},
                  {"name": 'Total Cash :', "value": str(formatCurrency(market_cash)), "inline": True},
                  {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]

        if ((self.tx["args"]["redeemAmount"] / underlying_decimals * underlying_price) > 100000):
            self.content = '<@&945071604642222110>'

        self.color = colors.blurple
        self.send = True

        self.result = {"webhook": self.webhook,
                       "title": self.title,
                       "content": self.content,
                       "fields": self.fields,
                       "color": self.color,
                       "image": self.image,
                       "send": self.send}

        return self.result

