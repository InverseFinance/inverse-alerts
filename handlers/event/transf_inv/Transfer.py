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
        self.tx = fixFromToValue(self.tx)

        self.webhook = os.getenv('WEBHOOK_ALAMEDA')
        from_address = self.tx["args"]["from"]
        to_address = self.tx["args"]["to"]
        amount = self.tx["args"]["amount"] / 1e18

        if from_address == "0xF02e86D9E0eFd57aD034FaF52201B79917fE0713" or to_address == "0xF02e86D9E0eFd57aD034FaF52201B79917fE0713":
            
            inv_balance = getBalance(self.web3, "0xF02e86D9E0eFd57aD034FaF52201B79917fE0713",
                                    "0x41d5d79431a913c4ae7d69a668ecdfe5ff9dfb68")

            self.title = "Alameda - INV activity detected"
            #self.content = '<@&945071604642222110>'
            self.fields = [
                {"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline": False},
                {"name": 'From :', "value": str(f'[{from_address}](https://etherscan.io/address/{from_address})'),"inline": False},
                {"name": 'To :', "value": str(f'[{to_address}](https://etherscan.io/address/{to_address})'),"inline": False},
                {"name": 'Value :', "value": str(formatCurrency(amount)), "inline": False},
                {"name": 'INV  Balance :', "value": str(formatCurrency(inv_balance)), "inline": False},
                {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]
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

