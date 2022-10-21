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

        self.webhook = os.getenv('WEBHOOK_SWAP')
        self.tx = fixFromToValue(self.tx)

        self.title = "Sushi New Liquidity Add event detected"
        self.fields = [{"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),
                   "inline": False},
                  {"name": 'Address :', "value": str(f'[{address}](https://etherscan.io/address/{address})'),
                   "inline": False},
                  {"name": 'Name :', "value": str(getName(self.web3, address)), "inline": True},
                  {"name": 'Symbol :', "value": str(getSymbol(self.web3, address)), "inline": True},
                  {"name": 'amountAMin :', "value": str(self.tx["args"]["amount0"] / 1e18), "inline": False},
                  {"name": 'amountBMin :', "value": str(self.tx["args"]["amount1"] / 1e18), "inline": True},
                  {"name": 'Token 0 :',
                   "value": str(getBalance(self.web3, address, getSushiTokens(self.web3, address[0]))),
                   "inline": False},
                  {"name": 'Token 1 :',
                   "value": str(getBalance(self.web3, address, getSushiTokens(self.web3, address[1]))), "inline": True},
                  {"name": 'Total Supply :', "value": str(getSupply(self.web3, address)), "inline": False},
                  {"name": 'Transaction :',
                   "value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]

        self.color = colors.dark_green
        self.send = True

        self.result = {"webhook": self.webhook,
                       "title": self.title,
                       "content": self.content,
                       "fields": self.fields,
                       "color": self.color,
                       "image": self.image,
                       "send": self.send}

        return self.result

