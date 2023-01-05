import re
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

        self.content = "<@&899302193608409178>"
        self.webhook = os.getenv('WEBHOOK_GOVPUBLIC')
        self.title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(self.tx["event"]))

        self.fields = [{"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),
                   "inline": True},
                  {"name": 'Start Block :', "value": str(
                      f'[{self.tx["args"]["startBlock"]}](https://etherscan.io/block/{self.tx["args"]["startBlock"]})'),
                   "inline": True},
                  {"name": 'End Block :', "value": str(
                      f'[{self.tx["args"]["endBlock"]}](https://etherscan.io/block/{self.tx["args"]["endBlock"]})'),
                   "inline": True},
                  {"name": 'Proposal :', "value": "https://www.inverse.finance/governance/proposals/mills/" + str(
                      getProposalCount(self.web3)), "inline": False},
                  {"name": 'Proposer :', "value": str(
                      f'[{self.tx["args"]["proposer"]}](https://etherscan.io/address/{self.tx["args"]["proposer"]})'),
                   "inline": False},
                  # {"name":'Targets :', "value":str({self.tx["args"]["targets"]}), "inline": False},
                  # {"name":'Values :', "value":str({self.tx["args"]["values"]}), "inline": False},
                  {"name": 'Description :', "value": str(f'{self.tx["args"]["description"][0:400]}...'),
                   "inline": False},
                  {"name": 'Transaction :',
                   "value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]

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

