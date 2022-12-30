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

        self.webhook = os.getenv('WEBHOOK_VELOUSDC')
        from_address = self.tx["args"]["from"]
        to_address = self.tx["args"]["to"]
        value = self.tx["args"]["value"] / 1e6

        usdc_balance = getBalance(self.web3, "0xe8537b6ff1039cb9ed0b71713f697ddbadbb717d",
                                  "0x7f5c764cbc14f9669b88837ca1490cca17c31607")
        ratio = float(value) / float(usdc_balance)
        if ratio > int(os.getenv('FRAX_USDC_RATIO')):
            self.title = "VELOUSDC High activity detected"
            self.content = '<@&945071604642222110>'
            self.fields = [
                {"name": 'Block Number :', "value": str(f'[{blockNumber}](https://optimistic.etherscan.io/block/{blockNumber})'),"inline": False},
                {"name": 'From :', "value": str(f'[{from_address}](https://optimistic.etherscan.io/address/{from_address})'),"inline": False},
                {"name": 'To :', "value": str(f'[{to_address}](https://optimistic.etherscan.io/address/{to_address})'),"inline": False},
                {"name": 'Value :', "value": str(formatCurrency(value)), "inline": False},
                {"name": 'USDC Balance :', "value": str(formatCurrency(usdc_balance)), "inline": False},
                {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://optimistic.etherscan.io/tx/{transactionHash})'), "inline": False}]
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

