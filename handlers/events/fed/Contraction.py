import os, json,re
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

        self.webhook = os.getenv('WEBHOOK_FED')
        self.image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/22517/1128427/3084f915-b906-4fdf-ac8c-ad5c0ce57e2b.jpg"
        amount = self.tx["args"]["amount"]
        event = self.tx["event"]
        dola_address = self.web3.toChecksumAddress('0x865377367054516e17014ccded1e7d814edc9ce4')
        dola_supply = getSupply(self.web3, dola_address)

        self.title = "Fed " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(event)) + " event detected"
        self.fields = [{"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),
                   "inline": False},
                  {"name": 'Fed Address :', "value": str(f'[{address}](https://etherscan.io/address/{address})'),
                   "inline": False},
                  {"name": 'Amount :', "value": str(formatCurrency(amount / 1e18)), "inline": True},
                  {"name": 'Total Supply :', "value": str(formatCurrency(dola_supply)), "inline": True},
                  {"name": 'Transaction :',
                   "value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]

        self.color = colors.dark_red
        self.send = True

        self.result = {"webhook": self.webhook,
                       "title": self.title,
                       "content": self.content,
                       "fields": self.fields,
                       "color": self.color,
                       "image": self.image,
                       "send": self.send}

        return self.result

