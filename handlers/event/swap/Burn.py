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

        amount_a = self.tx["args"]["amount0"]/1e6
        amount_b = self.tx["args"]["amount1"]/1e18

        total_amount = abs(amount_a + amount_b)

        token_a = getSymbol(self.web3, getSushiTokens(self.web3, address)[0])
        token_b = getSymbol(self.web3, getSushiTokens(self.web3, address)[1])

        balance_a = getBalance(self.web3, address, getSushiTokens(self.web3, address)[0])
        balance_b = getBalance(self.web3, address, getSushiTokens(self.web3, address)[1])

        self.webhook = os.getenv('WEBHOOK_VELOUSDC')

        self.title = "Velo New Liquidity Removal detected"

        self.fields = [{"name": 'Block Number :', "value": str(f'[{blockNumber}](https://optimistic.etherscan.io/block/{blockNumber})'),"inline": False},
                  {"name": 'Address :', "value": str(f'[{address}](https://optimistic.etherscan.io/address/{address})'),"inline": True},
                  {"name": 'Name :', "value": str(getName(self.web3, address)), "inline": True},
                  {"name": 'Symbol :', "value": str(getSymbol(self.web3, address)), "inline": False},
                  {"name": token_a+ ' amount', "value": str(formatCurrency(amount_a)), "inline": True},
                  {"name": token_b+ ' amount', "value": str(formatCurrency(amount_b)), "inline": True},
                  {"name": token_a+ ' balance',"value": str(formatCurrency(balance_a)),"inline": True},
                  {"name": token_b+ ' balance', "value": str(formatCurrency(balance_b)), "inline": True},
                  {"name": 'Total Supply :', "value": str(formatCurrency(getSupply(self.web3, address))), "inline": True},
                  {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://optimistic.etherscan.io/tx/{transactionHash})'), "inline": False}]
        self.color = colors.dark_red

        if total_amount>int(os.getenv("SENDING_THRESHOLD_OPTI")):
            self.send = True
            
        if total_amount>int(os.getenv("RISK_THRESHOLD_OPTI")):
            self.content = '<@&945071604642222110>'

        self.result = {"webhook": self.webhook,
                       "title": self.title,
                       "content": self.content,
                       "fields": self.fields,
                       "color": self.color,
                       "image": self.image,
                       "send": self.send}

        return self.result

