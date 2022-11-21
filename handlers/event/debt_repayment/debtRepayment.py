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

        self.webhook = os.getenv('WEBHOOK_DEBTREPAYMENT')
        self.image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/1291754/2213835/4c5b629f-a6b0-4575-98a1-9d5fae4fab33"

        collaterals_v1 = {
            "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": "0x697b4acAa24430F254224eB794d2a85ba1Fa1FB8",
            "0x865377367054516e17014CcdED1e7d814EDC9ce4": "0x7Fcb7DAC61eE35b3D4a51117A7c58D53f0a8a670",
            "0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272": "0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272",
            "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599": "0xE8A2eb30E9AB1b598b6a5fc4aa1B80dfB6F90753",
            "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e": "0xde2af899040536884e062D3a334F2dD36F34b4a4"}

        antoken = collaterals_v1[self.tx["args"]["underlying"]]
        exchange_rate = getExchangeRateStored(self.web3, antoken)
        received_amount = self.tx["args"]["receiveAmount"] / getDecimals(self.web3, self.tx["args"]["underlying"])
        paid_amount = self.tx["args"]["paidAmount"]
        paid_amount_underlying = exchange_rate * paid_amount / 1e18

        self.title = "Debt Repayment detected"

        self.fields = [
            {"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline": False},
            {"name": 'Token Repaid :', "value": str(getSymbol(self.web3, self.tx["args"]["underlying"])),"inline": True},
            {"name": 'Amount Received :', "value": str(formatCurrency(received_amount)), "inline": True},
            {"name": 'Amount Paid :', "value": str(formatCurrency(paid_amount_underlying)), "inline": True},
            {"name": 'Received/Paid :', "value": str(formatPercent(received_amount / paid_amount_underlying)),"inline": True},
            {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False},
            {"name": 'Debt Repayment Contract :',"value": str(f'[{address}](https://etherscan.io/address/{address})'), "inline": False}]

        self.color = colors.dark_orange

        self.send = True

        self.result = {"webhook": self.webhook,
                       "title": self.title,
                       "content": self.content,
                       "fields": self.fields,
                       "color": self.color,
                       "image": self.image,
                       "send": self.send}

        return self.result

