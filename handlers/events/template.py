from utils.fetchers import *
from dotenv import load_dotenv

load_dotenv()

class message():
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

        self.webhook = os.getenv("WEBHOOK_TESTING")
        self.tx = fixFromToValue(self.tx)

        self.title = ""
        self.content = ""
        self.fields = ""
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

