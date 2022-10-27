from utils.fetchers import *
from dotenv import load_dotenv

load_dotenv()

class handler():
    def __init__(self,web3,tx,name):
        self.web3 = web3
        self.tx = tx
        self.name = name
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

        if self.web3.eth.chainId==1:explorer='etherscan.io'
        elif self.web3.eth.chainId==5:explorer='goerli.etherscan.io'
        elif self.web3.eth.chainId==10:explorer='optimistic.etherscan.io'
        elif self.web3.eth.chainId==250:explorer='ftmscan.com'

        logging.info(str('Tx detected on ' + str(self.name)))
        logging.info(str(self.tx))

        self.webhook = os.getenv("WEBHOOK_GOVERNANCE")
        self.title = str('Tx detected on ' + str(self.name))
        self.fields = [{"name": 'Multisig :', "value": str(f'[{address}](https://{explorer}/address/{address})'),"inline": True},
                  {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://{explorer}/tx/{transactionHash})'), "inline": True},
                  {"name": 'Block :', "value": str(f'[{blockNumber}](https://{explorer}/block/{blockNumber})'), "inline": True},
                  {"name": 'Transaction Log :', "value": str(self.tx), "inline": False}]
        self.send = True

        self.result = {"webhook":self.webhook,
                  "title":self.title,
                  "content":self.content,
                  "fields":self.fields,
                  "color":self.color,
                  "image":self.image,
                  "send":self.send}

        return self.result

