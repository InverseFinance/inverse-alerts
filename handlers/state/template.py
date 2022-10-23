from utils.fetchers import *
from dotenv import load_dotenv

load_dotenv()

class handler():
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
        self.webhook = os.getenv('WEBHOOK_TESTING')
        if self.state_function == 'totalSupply':
            if abs(self.change) > 0.015:
                self.content = '<@&945071604642222110>'
                self.level = 3
                self.color = colors.red
                self.send = True
            elif abs(self.change) > 0.01:
                self.level = 2
                self.color = colors.dark_orange
                self.send = True
            elif abs(self.change) > 0.005:
                self.level = 1
                self.color = colors.orange
                self.send = True
            if self.send:
                logging.info(str(self.change) + '% change detected on ' + str(getName(self.web3, self.contract.address)) + ' total supply')
                self.title = str(formatPercent(self.change)) + ' change detected on ' + str(getSymbol(self.web3, getUnderlying(self.web3, self.state_argument))) + ' Supply'
                self.fields = [{"name": 'Alert Level :', "value": str(self.level), "inline": True},
                          {"name": 'Variation :', "value": str(formatPercent(self.change)), "inline": True},
                          {"name": 'Old Value :', "value": str(formatCurrency(self.old_value / getDecimals(self.web3,getUnderlying(self.web3,self.contract.address)))), "inline": True},
                          {"name": 'New Value :', "value": str(formatCurrency(self.value / getDecimals(self.web3, getUnderlying(self.web3, self.contract.address)))), "inline": True},
                          {"name": 'Link to Pool :',"value": 'https://etherscan.io/address/' + str(self.contract.address), "inline": False}]

        self.result = {"webhook":self.webhook,
                  "title":self.title,
                  "content":self.content,
                  "fields":self.fields,
                  "color":self.color,
                  "image":self.image,
                  "send":self.send}

        return self.result

