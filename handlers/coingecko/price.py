from utils.fetchers import *
from dotenv import load_dotenv

load_dotenv()


class message():
    def __init__(self, id, value, old_value, change):
        self.id = id
        self.change = change
        self.value = value
        self.old_value = old_value
        self.webhook = ''
        self.title = ''
        self.content = ''
        self.fields = ''
        self.color = colors.blurple
        self.image = ''
        self.level = 0
        self.send = False

    def compose(self):
        if abs(self.change) > 0.2:
            self.content = '<@&945071604642222110>'
            self.level = 3
            self.color = colors.red
            self.send = True
        elif abs(self.change) > 0.1:
            self.level = 2
            self.color = colors.dark_orange
            self.send = True
        elif abs(self.change) > 0.05:
            self.level = 1
            self.color = colors.orange
            self.send = True

        if self.send:
            logging.info(str(formatPercent(self.change)) + ' change detected on Coingecko ' + str(self.id) + ' Price')

            self.webhook = os.getenv('WEBHOOK_MARKETS')
            self.title = str(formatPercent(self.change)) + ' change detected on Coingecko ' + str(self.id) + ' Price'
            self.fields = [{"name": 'Alert Level :', "value": str(self.level), "inline": False},
                           {"name": 'Variation :', "value": str(formatPercent(self.change)), "inline": True},
                           {"name": 'Old Value :', "value": str(formatCurrency(self.old_value)), "inline": True},
                           {"name": 'New Value :', "value": str(formatCurrency(self.value)), "inline": True},
                           {"name": 'Link to Market :', "value": 'https://www.coingecko.com/en/coins/' + self.id,
                            "inline": False}]

        self.result = {"webhook": self.webhook,
                       "title": self.title,
                       "content": self.content,
                       "fields": self.fields,
                       "color": self.color,
                       "image": self.image,
                       "send": self.send}

        return self.result

