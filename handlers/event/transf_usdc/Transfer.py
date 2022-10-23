from utils.fetchers import *
from dotenv import load_dotenv

load_dotenv()


class handler():
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

        self.webhook = os.getenv('WEBHOOK_FRAXUSDC')
        from_address = self.tx["args"]["from"]
        to_address = self.tx["args"]["to"]
        value = self.tx["args"]["value"] / 1e6

        usdc_balance = getBalance(self.web3, "0xDcEF968d416a41Cdac0ED8702fAC8128A64241A2",
                                  "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
        ratio = float(value) / float(usdc_balance)
        if ratio > 0.01:
            self.title = "fraxUSDC High activity detected"
            self.content = '<@&945071604642222110>'
            self.fields = [
                {"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline": False},
                {"name": 'From :', "value": str(f'[{from_address}](https://etherscan.io/address/{from_address})'),"inline": False},
                {"name": 'To :', "value": str(f'[{to_address}](https://etherscan.io/address/{to_address})'),"inline": False},
                {"name": 'Value :', "value": str(formatCurrency(value)), "inline": False},
                {"name": 'USDC Balance :', "value": str(formatCurrency(usdc_balance)), "inline": False},
                {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]
            self.color = colors.dark_orange
            self.send = True

        self.result = {"webhook": self.webhook,
                       "title": self.title,
                       "content": self.content,
                       "fields": self.fields,
                       "color": self.color,
                       "image": self.image,
                       "send": self.send}

        return self.result

