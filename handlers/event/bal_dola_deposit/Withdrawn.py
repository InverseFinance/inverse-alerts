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
        if self.tx["args"]["poolid"] == "0xff4ce5aaab5a627bf82f4a571ab1ce94aa365ea6000200000000000000000426":
            self.title = "Balancer DOLA USDC " + self.tx["event"] + " Event Detected"

            address = self.tx["address"]
            blockNumber = self.tx["blockNumber"]
            transactionHash = self.tx["transactionHash"]

            self.tx = fixFromToValue(self.tx)
            self.webhook = os.getenv("WEBHOOK_BAL_DOLA")

            self.fields = [{"name": 'Block :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline": False},
                           {"name": 'Market Address :',"value": str(f'[{address}](https://etherscan.io/address/{address})'),"inline": False}]

            for arg in self.tx["args"]:
                if str(arg) == 'amount':
                    self.fields.append({"name": str(arg), "value": str(formatCurrency(self.tx["args"][arg] / 1e18)), "inline": True})
                else:
                    self.fields.append({"name": str(arg), "value": str(formatCurrency(self.tx["args"][arg]/1e18)), "inline": True})



            balances = getBalancerVaultBalances(self.web3,"0xff4ce5aaab5a627bf82f4a571ab1ce94aa365ea6000200000000000000000426")

            self.fields.append({"name": 'Total 1 :', "value": str(formatCurrency(balances[0]/1e18)), "inline": True})
            self.fields.append({"name": 'Total 2 :', "value": str(formatCurrency(balances[1]/1e18)), "inline": True})
               
            self.fields.append({"name": 'Total Balances :',"value": str(formatCurrency((balances[0]+balances[1])/1e18)), "inline": False})
            self.fields.append({"name": 'Transaction :', "value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline": False})

            self.image = ""
            self.color = colors.dark_red
            self.send = True

        self.result = {"webhook": self.webhook,
                        "title": self.title,
                        "content": self.content,
                        "fields": self.fields,
                        "color": self.color,
                        "image": self.image,
                        "send": self.send}

        return self.result

