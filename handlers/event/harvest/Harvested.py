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

        if address == '0x64e4fC597C70B26102464B7F70B1F00C77352910':
            self.webhook = os.getenv('WEBHOOK_FED')
            pool_address = '0xAA5A67c256e27A5d80712c51971408db3370927D'
            token_0 = 'DOLA'
            token_1 = '3CRV'
            token_0_address = '0x865377367054516e17014CcdED1e7d814EDC9ce4'
            token_1_address = '0x6c3f90f043a72fa612cbac8115ee7e52bde6e490'
            token_0_total = getBalance(self.web3, pool_address, token_0_address)
            token_1_total = getBalance(self.web3, pool_address, token_1_address)
            share = 0.2
        elif address== '0x00Ca07f4012dEbb0BD17cF15B1C2841928Da0484':
            self.webhook = os.getenv('WEBHOOK_FED')
            pool_address = '0xAA5A67c256e27A5d80712c51971408db3370927D'
            token_0 = 'DOLA'
            token_1 = 'crvFRAX'
            token_0_address = '0x865377367054516e17014CcdED1e7d814EDC9ce4'
            token_1_address = '0x3175Df0976dFA876431C2E9eE6Bc45b65d3473CC'
            token_0_total = getBalance(self.web3, pool_address, token_0_address)
            token_1_total = getBalance(self.web3, pool_address, token_1_address)
            share = 1

        self.title = "Harvest detected"
        self.fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
        {"name": 'Pool Address :', "value": str(f'[{pool_address}](https://etherscan.io/address/{pool_address})'), "inline": False},
        {"name": 'Strategy Address :', "value": str(f'[{address}](https://etherscan.io/address/{address})'), "inline": False},
        {"name":'Total Profit :',"value": str(formatCurrency(self.tx["args"]["profit"]/1e18)) ,"inline":True},
        {"name":'Inverse Profit :',"value": str(formatCurrency(self.tx["args"]["profit"]*share/1e18)) ,"inline":True},
        {"name":'Yearn Profit :',"value": str(formatCurrency(self.tx["args"]["profit"]*(1-share)/1e18)) ,"inline":True},
        {"name":'Loss :',"value": str(formatCurrency(self.tx["args"]["loss"]/1e18)) ,"inline":True},
        {"name":'Debt Payment :',"value": str(formatCurrency(self.tx["args"]["debtPayment"]/1e18)) ,"inline":True},
        {"name":'Debt Outstanding :',"value": str(formatCurrency(self.tx["args"]["debtOutstanding"]/1e18)) ,"inline":True},
        {"name":token_0+' in Pool :',"value":str(formatCurrency(token_0_total)),"inline":True},
        {"name":token_1+' in Pool :',"value":str(formatCurrency(token_1_total)),"inline":True},
        {"name":token_0+'+'+token_1+' in Pool',"value":str(formatCurrency(token_0_total + token_1_total)),"inline":False},
        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

        self.content = '<@&945071604642222110>'
        self.image = 'https://dune.com/api/screenshot?url=https://dune.com/embeds/1382819/2351787/0e47fbff-397e-43b5-94f3-a4e40067dffa.jpg'
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

