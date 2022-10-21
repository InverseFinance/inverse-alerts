from utils.fetchers import *
from dotenv import load_dotenv

load_dotenv()


class message():
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

        market_symbol = getSymbol(self.web3,address)
        market_decimals = getDecimals(self.web3,address)
        underlying_address = getUnderlying(self.web3,address)
        underlying_decimals = getDecimals(self.web3,underlying_address)
        underlying_price = getUnderlyingPrice(self.web3,address)
        market_supply = getSupply(self.web3,address)
        market_cash = getCash(self.web3,address)

        self.title = "Lending Market New Liquidation event detected for " + str(market_symbol)
        self.webhook = os.getenv('WEBHOOK_LIQUIDATIONS')
        self.fields = [{"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline": False},
                  {"name": 'Liquidator :', "value": str(f'[{self.tx["args"]["liquidator"]}](https://etherscan.io/address/{self.tx["args"]["liquidator"]})'),"inline": False},
                  {"name": 'Borrower :', "value": str(f'[{self.tx["args"]["borrower"]}](https://etherscan.io/address/{self.tx["args"]["borrower"]})'),"inline": False},
                  {"name": 'Market Address :', "value": str(f'[{address}](https://etherscan.io/address/{address})'),"inline": False},
                  {"name": 'Seized Amount :', "value": str(formatCurrency( self.tx["args"]["seizeTokens"] / getDecimals(self.web3, self.tx["args"]["cTokenCollateral"]))),"inline": True},
                  {"name": 'Seized Token  :', "value": str(getSymbol(self.web3, self.tx["args"]["cTokenCollateral"])),"inline": True},
                  {"name": 'Repay Amount :',"value": str(formatCurrency(self.tx["args"]["repayAmount"] / underlying_decimals)), "inline": False},
                  {"name": 'Repay Amount USD:', "value": str(formatCurrency(self.tx["args"]["repayAmount"] * underlying_price / underlying_decimals)),"inline": True},
                  {"name": 'Repay Token  :', "value": str(market_symbol), "inline": True},
                  {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]

        if ((self.tx["args"]["repayAmount"] / underlying_decimals) > 100000):
            self.content = '<@&945071604642222110>'

        self.color = colors.blurple
        self.send = True

        self.result = {"webhook": self.webhook,
                       "title": self.title,
                       "content": self.content,
                       "fields": self.fields,
                       "color": self.color,
                       "image": self.image,
                       "send": self.send}

        return self.result

