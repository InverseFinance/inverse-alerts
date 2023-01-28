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
        dola_address = "0x865377367054516e17014CcdED1e7d814EDC9ce4"
        composable_stable_pool = "0xff4ce5aaab5a627bf82f4a571ab1ce94aa365ea6000200000000000000000426 "

        tokens = self.tx['args']['tokens']
        address = str(self.tx["args"]["poolId"])
        logging.info("PoolBalanceChanged address: " + address,' type :',type(address))

        if address==composable_stable_pool:

            blockNumber = self.tx["blockNumber"]
            transactionHash = self.tx["transactionHash"]

            provider_address = getENS(self.web3,self.tx["args"]["liquidityProvider"])
            self.webhook = os.getenv("WEBHOOK_BAL_DOLA")

            self.fields = [{"name": 'Block :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'), "inline": False},
                           {"name": 'Pool Address :', "value": str(f'[{address}](https://etherscan.io/address/{address})'),"inline": False},
                           {"name": 'Provider :', "value": str(f'[{provider_address}](https://etherscan.io/address/{provider_address})'), "inline": False}]
            i =0
            deltas_sum = 0
            for token in self.tx["args"]["tokens"]:
                self.fields.append({"name":str(getSymbol(self.web3,token)),"value":str(formatCurrency(self.tx["args"]["deltas"][i]/getDecimals(self.web3,token))),"inline":True})
                deltas_sum =deltas_sum + self.tx["args"]["deltas"][i]/getDecimals(self.web3,token)
                i = i+ 1

            balances = getBalancerVaultBalances(self.web3,"0xff4ce5aaab5a627bf82f4a571ab1ce94aa365ea6000200000000000000000426 ")

            self.fields.append({"name": 'Total 1 :', "value": str(formatCurrency(balances[0]/1e18)), "inline": True})
            self.fields.append({"name": 'Total 2 :', "value": str(formatCurrency(balances[1]/1e18)), "inline": True})
               
            self.fields.append({"name": 'Total Balances :',"value": str(formatCurrency((balances[0]+balances[1])/1e18)), "inline": False})
            self.fields.append({"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline": False})

            if deltas_sum > 0:
                self.color = colors.dark_green
                event = "Add"
            elif deltas_sum <0:
                self.color = colors.dark_red
                event = "Withdraw"
            else:
                self.color = colors.blurple
                event = "Other"

            self.title = "Balancer DOLA USDC "+event+" Event Detected"

            if abs(deltas_sum)>float(os.getenv("SENDING_THRESHOLD_BAL")):
                self.send = True

            if abs(deltas_sum)>float(os.getenv("RISK_THRESHOLD_BAL")):
                self.content = '<@&945071604642222110>'

        self.result = {"webhook":self.webhook,
                  "title":self.title,
                  "content":self.content,
                  "fields":self.fields,
                  "color":self.color,
                  "image":self.image,
                  "send":self.send}

        return self.result

