from utils.fetchers import *
from dotenv import load_dotenv

load_dotenv()

class message():
    def __init__(self,web3,contract,state_function,state_argument,change,value,old_value):
        self.web3 = web3
        self.webhook = ''
        self.title = ''
        self.content = ''
        self.fields = ''
        self.color = colors.blurple
        self.image = ''
        self.level = 0
        self.contract = contract
        self.state_function = state_function
        self.state_argument = state_argument
        self.change = change
        self.value = value
        self.old_value = old_value
        self.send = False

    def compose(self):
        logging.info(str(self.change) + '% change detected on ' +str(getName(self.web3, self.contract.address)) + ' Liquidation incentive')

        self.webhook = os.getenv('WEBHOOK_MARKETS')
        self.title = str(formatPercent(self.change)) + ' change detected on ' + str(getSymbol(self.web3, getUnderlying(self.web3, self.state_argument))) + ' Liquidation incentive'

        self.fields = [{"name": 'Alert Level :', "value": str(self.level), "inline": True},
                  {"name": 'Variation :', "value": str(formatPercent(self.change)), "inline": True},
                  {"name": 'Old Value :', "value": str(formatCurrency(self.old_value / 1e18)), "inline": True},
                  {"name": 'New Value :', "value": str(formatCurrency(self.value / 1e18)), "inline": True},
                  {"name": 'Link to Pool :', "value": 'https://etherscan.io/address/' + str(self.contract.address),
                   "inline": False}]

        self.content = '<@&945071604642222110>'
        self.level = 3
        self.color = colors.red
        self.send = True

        self.result = {"webhook":self.webhook,
                  "title":self.title,
                  "content":self.content,
                  "fields":self.fields,
                  "color":self.color,
                  "image":self.image,
                  "send":self.send}

        return self.result

