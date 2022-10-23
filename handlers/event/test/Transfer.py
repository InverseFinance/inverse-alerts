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
        self.color = ''
        self.image = ''
        self.send = False

    def compose(self):
        address = self.tx["address"]
        blockNumber = self.tx["blockNumber"]
        transactionHash = self.tx["transactionHash"]

        self.webhook = os.getenv("WEBHOOK_TESTING")
        self.tx = fixFromToValue(self.tx)

        from_address = self.tx["args"]["from"]
        to_address = self.tx["args"]["to"]
        value = self.tx["args"]["value"]

        self.title = "Test : Transfer activity detected"
        self.content = ""
        self.fields = [{"name": "Block Number :","value": str(f"[{blockNumber}](https://etherscan.io/block/{blockNumber})"),"inline": False},
                  {"name": "Transfer :", "value": str(formatCurrency(value / getDecimals(self.web3, address))) + " " + str(getSymbol(self.web3, address)), "inline": False},
                  {"name": "From :","value": str(f"[{from_address}](https://etherscan.io/address/{from_address})"),"inline": False},
                  {"name": "To :","value": str(f"[{to_address}](https://etherscan.io/address/{to_address})"),"inline": False},
                  {"name": "Transaction :", "value": str(f"[{transactionHash}](https://etherscan.io/tx/{transactionHash})"),"inline": False}]

        self.color = colors.dark_orange
        self.image = ''
        self.send = True

        self.result = {"webhook":self.webhook,
                  "title":self.title,
                  "content":self.content,
                  "fields":self.fields,
                  "color":self.color,
                  "image":self.image,
                  "send":self.send}

        return self.result