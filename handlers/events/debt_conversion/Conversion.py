from utils.fetchers import *
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

        self.webhook = os.getenv('WEBHOOK_DEBTREPAYMENT')
        self.image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/1291809/2213790/9e5c3845-66c0-496f-b42a-49a2fbd20df9.jpg"

        self.title = "Debt Conversion  detected"
        self.fields = [{"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),
                   "inline": False},
                  {"name": 'User :',
                   "value": str(f'[{self.tx["args"]["user"]}](https://etherscan.io/address/{self.tx["args"]["user"]})'),
                   "inline": True},
                  {"name": 'Token Repaid :', "value": str(getSymbol(self.web3, self.tx["args"]["anToken"])),
                   "inline": True},
                  {"name": 'DOLA Amount :', "value": str(formatCurrency(self.tx["args"]["dolaAmount"] / 1e18)),
                   "inline": True},
                  {"name": 'Underlying Amount :', "value": str(formatCurrency(
                      self.tx["args"]["underlyingAmount"] / getDecimals(self.web3, self.tx["args"]["anToken"]))),
                   "inline": True},
                  {"name": 'Transaction :',
                   "value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False},
                  {"name": 'Debt Conversion Contract :',
                   "value": str(f'[{address}](https://etherscan.io/address/{address})'), "inline": False}]
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

