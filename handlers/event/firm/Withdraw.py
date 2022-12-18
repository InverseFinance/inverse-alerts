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
        self.title = "Firm " + self.tx["event"] + " Event Detected"

        address = self.tx["address"]
        blockNumber = self.tx["blockNumber"]
        transactionHash = self.tx["transactionHash"]

        self.webhook = os.getenv("WEBHOOK_FIRM")
        self.tx = fixFromToValue(self.tx)

        blockNumber = self.tx["blockNumber"]
        transactionHash = self.tx["transactionHash"]

        self.webhook = os.getenv("WEBHOOK_BAL_DOLA")

        self.fields = [{"name": 'Block :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),
                        "inline": False},
                       {"name": 'Market Address :', "value": str(f'[{address}](https://etherscan.io/address/{address})'),
                        "inline": False}]

        for arg in self.tx["args"]:
            self.fields.append({"name": str(arg), "value": str(self.tx["args"][arg]), "inline": True})

        self.fields.append(
            {"name": 'Transaction :', "value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),
             "inline": False})

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

