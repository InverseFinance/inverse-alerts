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
        self.title = "Bal_dola " + self.tx["event"] + " Event Detected"

        address = self.tx["address"]
        blockNumber = self.tx["blockNumber"]
        transactionHash = self.tx["transactionHash"]

        # The following resolve non standard event fields name for sending/receiveing ERC20 tokens
        self.tx = fixFromToValue(self.tx)

        # Input webhook url desitntion : to be specified in .env
        self.webhook = os.getenv("WEBHOOK_BAL_DOLA")

        # Standard fields for all tx
        self.fields = [{"name": 'Block :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline": False},
                        {"name": 'Market Address :',"value": str(f'[{address}](https://etherscan.io/address/{address})'),"inline": False}]

        # Add event fields
        for arg in self.tx["args"]:
            if str(arg) == 'amount':
                self.fields.append(
                    {"name": str(arg), "value": str(formatCurrency(self.tx["args"][arg] / 1e18)), "inline": True})
            else:
                self.fields.append({"name": str(arg), "value": str(self.tx["args"][arg]), "inline": True})

        # Add Tx field
        self.fields.append(
            {"name": 'Transaction :', "value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),
                "inline": False})

        # Insert custom logic for attributes/sending here
        self.image = ""
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

