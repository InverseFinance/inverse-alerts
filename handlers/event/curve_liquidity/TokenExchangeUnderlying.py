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

        pool_address = address

        if pool_address == "0xAA5A67c256e27A5d80712c51971408db3370927D":
            self.webhook = os.getenv('WEBHOOK_DOLA3CRV')
            token_0 = 'DOLA'
            token_1 = '3CRV'
            token_0_address = '0x865377367054516e17014CcdED1e7d814EDC9ce4'
            token_1_address = '0x6c3f90f043a72fa612cbac8115ee7e52bde6e490'
            token_0_total = getBalance(self.web3, pool_address, token_0_address)
            token_1_total = getBalance(self.web3, pool_address, token_1_address)
            self.image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/833844/1457892/c8141b30-aa8c-4588-8d42-877ce649abee.jpg"
        elif pool_address == "0xE57180685E3348589E9521aa53Af0BCD497E884d":
            self.webhook = os.getenv('WEBHOOK_DOLAFRAXBP')
            token_0 = 'DOLA'
            token_1 = 'crvFRAX'
            token_0_address = '0x865377367054516e17014CcdED1e7d814EDC9ce4'
            token_1_address = '0x3175Df0976dFA876431C2E9eE6Bc45b65d3473CC'
            token_0_total = getBalance(self.web3, pool_address, token_0_address)
            token_1_total = getBalance(self.web3, pool_address, token_1_address)
            self.image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/1300762/2228671/f10870d8-4e95-474d-a47a-d75b05cd2a99.jpg"
        else:
            return

        buyer = self.tx["args"]["buyer"]
        sold_id = self.tx["args"]["sold_id"]
        tokens_sold = self.tx["args"]["tokens_sold"]/1e18
        bought_id = self.tx["args"]["bought_id"]
        tokens_bought = self.tx["args"]["tokens_bought"]/1e18

        if sold_id==0:
            tokens_sold_symbol = token_0
            tokens_bought_symbol = token_1
        else:
            tokens_sold_symbol = token_1
            tokens_bought_symbol = token_0

        self.title = token_0 + token_1 + " Pool Swap event detected"
        self.content = ""
        self.fields = [{"name": 'Block :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'), "inline": False},
                       {"name": 'Address :', "value": str(f'[{address}](https://etherscan.io/address/{address})'),"inline": False},
                       {"name": 'Trader :', "value": str(f'[{buyer}](https://etherscan.io/address/{buyer})'),"inline": False},
                       {"name": tokens_bought_symbol+' Bought', "value": str(formatCurrency(tokens_bought)), "inline": True},
                       {"name": tokens_sold_symbol+' Sold', "value": str(formatCurrency(tokens_sold)), "inline": True},
                       {"name": token_0 + ' in Pool :', "value": str(formatCurrency(token_0_total)), "inline": True},
                       {"name": token_1 + ' in Pool :', "value": str(formatCurrency(token_1_total)), "inline": True},
                       {"name": token_0 + '+' + token_1 + ' in Pool',"value": str(formatCurrency(token_0_total + token_1_total)), "inline": False},
                       {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline": False}]

        self.color = colors.dark_orange

        if tokens_sold > 500000 or tokens_bought > 500000:
            self.send = True


        self.result = {"webhook":self.webhook,
                  "title":self.title,
                  "content":self.content,
                  "fields":self.fields,
                  "color":self.color,
                  "image":self.image,
                  "send":self.send}

        return self.result

