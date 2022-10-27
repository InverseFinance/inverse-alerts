from utils.fetchers import *
from dotenv import load_dotenv

load_dotenv()

class handler():
    def __init__(self,web3,tx):
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

        arg1 = self.tx["args"]["arg1"]
        arg2 = self.tx["args"]["arg2"]
        arg3 = self.tx["args"]["arg3"]
        arg4 = self.tx["args"]["arg4"]

        self.webhook = os.getenv("WEBHOOK_TESTING")
        self.tx = fixFromToValue(self.tx)

        self.title = ""
        self.content = ""
        self.fields = [{"name": 'Block :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'), "inline": False},
                       {"name": 'Address :', "value": str(f'[{address}](https://etherscan.io/address/{address})'),"inline": False},
                       {"name": 'Arg1 :', "value": str(arg1),"inline": False},
                       {"name": 'Arg2 :', "value": str(arg2), "inline": True},
                       {"name": 'Arg3 :', "value": str(arg3), "inline": True},
                       {"name": 'Arg4 :', "value": str(arg4), "inline": True},
                       {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline": False}]
        self.image = ""
        self.color = colors.dark_orange
        self.send = True

        self.result = {"webhook":self.webhook,
                  "title":self.title,
                  "content":self.content,
                  "fields":self.fields,
                  "color":self.color,
                  "image":self.image,
                  "send":self.send}

        return self.result

