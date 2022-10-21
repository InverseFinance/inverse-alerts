from utils.fetchers import *
from dotenv import load_dotenv

load_dotenv()

class message():
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

        if self.web3.eth.chainId==1:explorer='etherscan'
        elif self.web3.eth.chainId==1:explorer='optimistic.etherscan'
        elif self.web3.eth.chainId==1:explorer='ftmscan'


        logging.info(str('Tx detected on ' + str(self.name)))

        self.webhook = os.getenv("WEBHOOK_GOVERNANCE")
        self.title = str('Tx detected on ' + str(self.name))
        self.fields = [{"name": 'Multisig :', "value": str(f'[{address}](https://{explorer}.io/address/{address})'),"inline": True},
                  {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://{explorer}.io/tx/{transactionHash})'), "inline": True},
                  {"name": 'Block :', "value": str(f'[{blockNumber}](https://{explorer}.io/block/{blockNumber})'), "inline": True},
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

