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

        gauges = ["0xBE266d68Ce3dDFAb366Bb866F4353B6FC42BA43c", "0x8Fa728F393588E8D8dD1ca397E9a710E53fA553a"]
        gauge_address = str(self.tx["args"]["gauge_addr"])

        if gauge_address in gauges:
            vecrv_address = "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2"
            vecrv_supply = getSupply(self.web3, vecrv_address)
            user = self.tx["args"]["user"]
            user_vecrv_balance = getBalance(self.web3, user, vecrv_address)
            weight = self.tx["args"]["weight"]

            if gauge_address == "0xBE266d68Ce3dDFAb366Bb866F4353B6FC42BA43c":
                self.webhook = os.getenv('WEBHOOK_DOLAFRAXBP')
                pool_address = "0xE57180685E3348589E9521aa53Af0BCD497E884d"
                token_0 = "DOLA"
                token_1 = "crvFRAX"
                self.image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/1349566/2302403/6731fd1b-9cb1-4ca8-a321-1025b786a010.jpg"
                self.content = ''#'<@&945071604642222110>'
                self.color = colors.dark_green
                self.send = True
            elif gauge_address == "0x8Fa728F393588E8D8dD1ca397E9a710E53fA553a":
                self.webhook = os.getenv('WEBHOOK_DOLA3CRV')
                pool_address = "0xAA5A67c256e27A5d80712c51971408db3370927D"
                token_0 = "DOLA"
                token_1 = "3CRV"
                self.image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/1348784/2301280/9afceee3-e958-441a-b77a-5558a7a08595.jpg"
                self.content = ''#'<@&945071604642222110>'
                self.color = colors.dark_green
                self.send = True


            self.title = token_0 + token_1 + " Pool Vote For Gauge detected"
            self.fields = [
                {"name": 'Block :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline": False},
                {"name": 'User :', "value": str(f'[{user}](https://etherscan.io/address/{user})'), "inline": False},
                {"name": 'Gauge Address :',"value": str(f'[{gauge_address}](https://etherscan.io/address/{gauge_address})'), "inline": False},
                {"name": 'Pool Address :',"value": str(f'[{pool_address}](https://etherscan.io/address/{pool_address})'), "inline": False},
                {"name": 'Weight :', "value": str(formatPercent(weight / 10000)), "inline": True},
                {"name": 'veCRV Weight :', "value": str(formatCurrency(user_vecrv_balance * weight / 10000)),"inline": True},
                {"name": 'veCRV Balance :', "value": str(formatCurrency(user_vecrv_balance)), "inline": True},
                {"name": 'Balance / veCRV Supply :', "value": str(formatPercent(user_vecrv_balance / vecrv_supply)),"inline": True},
                {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]

        self.result = {"webhook": self.webhook,
                       "title": self.title,
                       "content": self.content,
                       "fields": self.fields,
                       "color": self.color,
                       "image": self.image,
                       "send": self.send}

        return self.result


