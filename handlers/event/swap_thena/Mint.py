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
        addresses = getSushiTokens(self.web3,address)
        blockNumber = self.tx["blockNumber"]
        transactionHash = self.tx["transactionHash"]

        amount_a = self.tx["args"]["amount0"]/1e18
        amount_b = self.tx["args"]["amount1"]/1e18
        total_amount = abs(amount_a + amount_b)
        token_a = getSymbol(self.web3, getSushiTokens(self.web3, address)[0])
        token_b = getSymbol(self.web3, getSushiTokens(self.web3, address)[1])
        balance_a = getBalance(self.web3, address, getSushiTokens(self.web3, address)[0])
        balance_b = getBalance(self.web3, address, getSushiTokens(self.web3, address)[1])


        self.webhook = os.getenv('WEBHOOK_SWAP_THENA')

        self.title = "Thena New Liquidity Add event detected"
        self.fields = [{"name": 'Block Number :', "value": str(f'[{blockNumber}](https://bscscan.com/block/{blockNumber})'),"inline": False},
                  {"name": 'Address :', "value": str(f'[{address}](https://bscscan.com/address/{address})'),"inline": False},
                  {"name": 'Symbol :', "value": str(getSymbol(self.web3, address)), "inline": True},
                  {"name": token_a+ ' amount', "value": str(formatCurrency(amount_a)), "inline": True},
                  {"name": token_b+ ' amount', "value": str(formatCurrency(amount_b)), "inline": True},
                  {"name": token_a+ ' balance',"value": str(formatCurrency(balance_a)),"inline": True},
                  {"name": token_b+ ' balance', "value": str(formatCurrency(balance_b)), "inline": True},
                  {"name": 'Transaction :', "value": str(f'[{transactionHash}](https://bscscan.com/tx/{transactionHash})'), "inline": False}]

        self.color = colors.dark_green
        
        
        if total_amount>float(50000):
            self.send = True

        self.result = {"webhook": self.webhook,
                       "title": self.title,
                       "content": self.content,
                       "fields": self.fields,
                       "color": self.color,
                       "image": self.image,
                       "send": self.send}

        return self.result

