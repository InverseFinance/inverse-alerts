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

        self.webhook = os.getenv('WEBHOOK_FED')

        self.tx = fixFromToValue(self.tx)
        from_address = self.tx["args"]["from"]
        to_address = self.tx["args"]["to"]
        value = self.tx["args"]["value"]

        feds = ["0xcc180262347F84544c3a4854b87C34117ACADf94",
                "0x7eC0D931AFFBa01b77711C2cD07c76B970795CDd",  # stabilizer
                "0xC564EE9f21Ed8A2d8E7e76c085740d5e4c5FaFbE",  # fantom bridge
                "0x7765996dAe0Cf3eCb0E74c016fcdFf3F055A5Ad8",
                "0x5Fa92501106d7E4e8b4eF3c4d08112b6f306194C",
                "0xe3277f1102C1ca248aD859407Ca0cBF128DB0664",
                "0x5E075E40D01c82B6Bf0B0ecdb4Eb1D6984357EF7",
                "0x9060A61994F700632D16D6d2938CA3C7a1D344Cb",
                "0xCBF33D02f4990BaBcba1974F1A5A8Aea21080E36",
                "0x4d7928e993125A9Cefe7ffa9aB637653654222E2",
                "0x57D59a73CDC15fe717D2f1D433290197732659E2"]

        if (self.event_name in ["Transfer"] and (
                from_address in feds and to_address == '0x926dF14a23BE491164dCF93f4c468A50ef659D5B')):
            self.title = "Profit Taking detected"
            self.fields = [
                {"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline": False},
                {"name": 'Profit :', "value": str(formatCurrency(value / getDecimals(self.web3, address))) + ' ' + str(getSymbol(self.web3, address)), "inline": False},
                {"name": 'From :', "value": str(f'[{from_address}](https://etherscan.io/address/{from_address})'),"inline": False},
                {"name": 'To :', "value": str(f'[{to_address}](https://etherscan.io/address/{to_address})'),"inline": False},
                {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]
            self.content = '<@&945071604642222110>'
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

