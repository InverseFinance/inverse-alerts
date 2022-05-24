import fetchers
import json
from utils import formatCurrency,formatPercent
import requests #dependency
from utils import sendWebhook,makeFields

test = fetchers.getUnderlyingPrice(0)

print(test)