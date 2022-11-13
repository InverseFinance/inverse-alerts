from utils.fetchers import *
from dotenv import load_dotenv
import sys
import struct

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
        print(self.tx)
        dola_address = "0x865377367054516e17014CcdED1e7d814EDC9ce4"
        composable_stable_pool = "0x5b3240b6be3e7487d61cd1afdfc7fe4fa1d81e64"

        if dola_address in self.tx['args']['tokens'] or composable_stable_pool in self.tx['args']['tokens']:

            address = self.tx["address"]
            blockNumber = self.tx["blockNumber"]
            transactionHash = self.tx["transactionHash"]
            event = "Liquidity"
            arg1 = self.tx["args"]["poolId"]
            arg2 = getENS(self.web3,self.tx["args"]["liquidityProvider"])
            arg2_bis = self.tx["args"]["liquidityProvider"]
            #arg3 = self.tx["args"]["tokens"]
            arg4 = self.tx["args"]["deltas"][0]
            arg5 = self.tx["args"]["deltas"][1]
            #arg5 = self.tx["args"]["protocolFeeAmounts"]

            if arg4<0 or arg5 < 0:
                event = 'Withdrawal'
                self.color = colors.dark_red
            if arg4>0 or arg5 > 0 :
                event = 'Deposit'
                self.color = colors.dark_green

            self.webhook = os.getenv("WEBHOOK_BAL_DOLA")

            self.title = "BAL_DOLA_BB_A_USD "+event+" Detected"

            self.fields = [{"name": 'Block :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'), "inline": False},
                           {"name": 'Pool Address :', "value": str(f'[0x5b3240b6be3e7487d61cd1afdfc7fe4fa1d81e64](https://etherscan.io/address/0x5b3240b6be3e7487d61cd1afdfc7fe4fa1d81e64)'),"inline": False},
                           {"name": 'Provider :', "value": str(f'[{arg2}](https://etherscan.io/address/{arg2_bis})'), "inline": False},
                           {"name": 'DOLA amount :', "value": str(formatCurrency(arg4/1e18)), "inline": False},
                           {"name": 'DOLA bb-a-usd amount :', "value": str(formatCurrency(arg5/1e18)), "inline": False},
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

