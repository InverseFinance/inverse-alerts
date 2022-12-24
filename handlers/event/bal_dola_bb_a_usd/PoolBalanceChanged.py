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
        composable_stable_pool = "0x5b3240b6be3e7487d61cd1afdfc7fe4fa1d81e64"

        tokens = self.tx['args']['tokens']
        address = str(self.tx["args"]["poolId"])[0:42]
        print(address)

        if address=="0x5b3240b6be3e7487d61cd1afdfc7fe4fa1d81e64":

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


            balances = getBalancerVaultBalances(self.web3,"0x5b3240b6be3e7487d61cd1afdfc7fe4fa1d81e6400000000000000000000037b")

            i = 1
            balances_sum = 0
            for token in self.tx["args"]["tokens"][1:2]:
                self.fields.append({"name": 'Total ' + str(getSymbol(self.web3, token)), "value": str(
                    formatCurrency(balances[1][i] / getDecimals(self.web3, token))), "inline": True})
                balances_sum = balances_sum + balances[1][i] / getDecimals(self.web3, token)
                i = i + 1

            self.fields.append({"name": 'Total Balances :',"value": str(formatCurrency(balances_sum)),"inline": False})
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

            self.title = "Balancer Liquidity "+event+" Event Detected"

            if abs(deltas_sum)>10000:
                self.send = True

            if abs(deltas_sum)>300000:
                self.content = '<@&945071604642222110>'

        self.result = {"webhook":self.webhook,
                  "title":self.title,
                  "content":self.content,
                  "fields":self.fields,
                  "color":self.color,
                  "image":self.image,
                  "send":self.send}

        return self.result

