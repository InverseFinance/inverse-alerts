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

        self.image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/838610/1466237/8e64e858-5db5-4692-922d-5f9fe6b7a8c6.jpg"
        if self.tx["args"]['amount0In'] == 0:
            operation = 'Buy ' + str(formatCurrency(self.tx["args"]['amount0Out'] / getDecimals(self.web3,getSushiTokens(self.web3, address)[0]))) + " " + str(getSushiTokensSymbol(self.web3, address)[0])
            self.color = colors.dark_green
            self.title = "Sushiswap New Buy event detected"
            self.send = True
        else:
            operation = 'Sell ' + str(formatCurrency(self.tx["args"]['amount0In'] / getDecimals(self.web3,getSushiTokens(self.web3, address)[0]))) + " " + str(getSushiTokensSymbol(self.web3, address)[0])
            self.color = colors.dark_red
            self.title = "Sushiswap New Sell event detected"
            self.send = True

        self.fields = [{"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline": False},
                  {"name": 'Address :', "value": str(f'[{address}](https://etherscan.io/address/{address})'), "inline": True},
                  {"name": 'Name :', "value": str(getName(self.web3, address)), "inline": True},
                  {"name": 'Symbol :', "value": str(getSymbol(self.web3, address)), "inline": True},
                  {"name": 'Operation :', "value": str(operation), "inline": True},
                  {"name": 'USD value :', "value": str(formatCurrency(((self.tx["args"]["amount0Out"] + self.tx["args"]["amount0In"]) / getDecimals(self.web3,getSushiTokens(self.web3, address)[0])) * getUnderlyingPrice(self.web3, '0x1637e4e9941d55703a7a5e7807d6ada3f7dcd61b'))), "inline": True},
                  {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]

        self.result = {"webhook": self.webhook,
                       "title": self.title,
                       "content": self.content,
                       "fields": self.fields,
                       "color": self.color,
                       "image": self.image,
                       "send": self.send}

        return self.result

