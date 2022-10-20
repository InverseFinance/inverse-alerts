import os,random,requests,logging,sys,json,time
from dotenv import load_dotenv
from web3 import Web3
load_dotenv()


def load_alerts():
    a_file = open("alerts.json", "r")
    alerts = json.load(a_file)
    return alerts
def fixFromToValue(string):
    """
    format the different version of 'from'/'to'/'value to one comprehensive output with from and to
    """
    string = str(string)

    string = string.replace("_from","from")
    string = string.replace("_to","to")
    string = string.replace("_value","value")
    string = string.replace("src","from")
    string = string.replace("dst","to")
    string = string.replace("wad","value")
    string = string.replace("src","from")
    string = string.replace("dst","to")
    string = string.replace("wad","value")

    string = json.loads(string)
    return string

def fixFromToFilters(string,token_address):
    """
    Amend the from/to filter depending on the token to produce valid filters
    """

    if token_address in["0xD533a949740bb3306d119CC777fa900bA034cd52"]:
        string = str(string)
        string = string.replace("from","_from")
        string = string.replace("to","_to")

    elif token_address == "0x6B175474E89094C44Da98b954EedeAC495271d0F":
        string = str(string)
        string = string.replace("from","src")
        string = string.replace("to","dst")

    if isinstance(string, str): string  = eval(string)

    return string

def getWeb3(chainid):
    """
    Return an RPC based on the ChainId provided
    """
    if chainid==1:
        rpc = os.getenv('QUICKNODE_ETH')
        web3 = Web3(Web3.HTTPProvider(rpc))
    elif chainid==10:
        rpc = os.getenv('QUICKNODE_OPT')
        web3 = Web3(Web3.HTTPProvider(rpc))
    elif chainid==250:
        rpc = os.getenv('QUICKNODE_FTM')
        web3 = Web3(Web3.HTTPProvider(rpc))
    return web3

def getRPC(chainid):
    """
    Return an RPC based on the ChainId provided
    """
    if chainid==1:
        rpc = os.getenv('QUICKNODE_ETH')
    elif chainid==10:
        rpc = os.getenv('QUICKNODE_OPT')
    elif chainid==250:
        rpc = os.getenv('QUICKNODE_FTM')
    return rpc

def assignFrequency(chainid):
    if chainid==1:
        frequency = random.uniform(60,120)
    elif chainid==10:
        frequency = random.uniform(10,15)
    elif chainid==250:
        frequency = random.uniform(10,15)
    return frequency

def sendWebhook(webhook, title, fields, content, imageurl, color):
    """
    Send a webhook with embed (title,fields,image,url,color)
    content is used for the body of the message and tagging roles
    :param webhook: string webhook link to send the message to
    :param title: self-explanatory, string
    :param fields: a json string of fields with names, values, and inLine paramter filled (use the function makefields)
    :param content: the text body of the message, can be used for tagging roles
    :param imageurl: string link to an embedded image url
    :param color: color of the embed message in discord
    :return:
    """
    error = True
    while error:
        try:
            data = {"content": content,
                    "embeds":[{"fields": fields,
                               "title": title,
                               "color": color,
                               "image": {"url": imageurl}}]}
            result = requests.post(webhook, json=data)
            result.raise_for_status()
            time.sleep(random.uniform(2, 5))
        except requests.exceptions.HTTPError as err:
            logging.error(err)
            sendError("Error in sending message to webhook. Waiting 5 seconds to retry...")
            time.sleep(5)
            error = True
        except Exception as e:
            logging.error("Unknown error in sending message to webhook. Please inspect the logs.")
            logging.error(e)
            sendError('<@578956365205209098>')
            sendError("Unknown error in sending message to webhook. Please inspect the logs.")
            sendError(e)
        else:
            logging.info("Embed delivered successfully to webhook "+str(webhook)+" code {}.".format(result.status_code))
            error = False
            break

def sendError(content):
    """
    Send a message to a discord channel exclusively used for reporting errors
    :param content: string
    :return:
    """
    load_dotenv()
    webhook = os.getenv('WEBHOOK_ERRORS')
    error = True
    replacers = {'{': '(', '}': ')',']': ')','[': ')',':': '='}  # etc....
    i = 0
    while error and i<5 :
        try:
            i = i+ 1
            for a, b in replacers.items():
                content = str(content).replace(a,b)
            data = {"content": content}
            result = requests.post(webhook, json=data)
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(err)
            logging.info("Error in sending message to webhook. Waiting 10 seconds to retry... code {}.".format(result.status_code))
            # time sleep is used to avoid throttling the error webhook w/ too many attempts

            time.sleep(10)
            error = True
        else:
            error = False

# Format to 0,000.00
def formatCurrency(value):
    value = "{:,.2f}".format(value)
    return value

# Format to 00.00 %
def formatPercent(value):
    value = "{:.2%}".format(value)
    return value

# Logger settings
def LoggerParams():
    """
    Configure our logger to write in debug.log
    """
    # Logger config
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    # Mute warning when pool is full
    logging.getLogger("urllib3").setLevel(logging.ERROR)

# Define easiy colors for discord
class colors:
    """
    This color class allows to pass readable arguments to theDiscord Embed
    """
    default = 0
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da
    greyple = 0x99aab5

def hex_and_pad(i):
    unpadded_hex_value = hex(i).rstrip("L")
    return "0x" + unpadded_hex_value[2:].zfill(64)


# Check if contract ABI is present in the working folder otherwise download from etherscan and stores it
def getABI(address):
    try:
        # First try to get the ABI from the ABI folder
        #logging.info('Loading ABI from file')
        contract_abi = json.load(open(f'ABI/{address}.json'))
        #logging.info(contract_abi)
        #logging.info('ABI loaded from file')
        return contract_abi
    except:
        # Else get the ABI from Etherscan, be warry of the query rate to etherscan API (5/sec)
        logging.info(f"Can't find ABI locally. Fetching ABI from Etherscan for contract{address}")
        contract_abi = requests.get('https://api.etherscan.io/api?module=contract&action=getabi&address=' + address + '&apikey=' + os.getenv('ETHERSCAN')).json()['result']
        #logging.info(f'ABI Found : {contract_abi}')
        # Then save it to the ABI folder
        #logging.info('Saving ABI...')
        with open(f'ABI/{address}.json', 'w') as outfile:
            outfile.write(str(contract_abi))
        logging.info(f'ABI Saved to ABI/{address}.json')
        #and return object
        return contract_abi

# A simple Contract Class with name, address and ABI
class Contract(object):
    def __init__(self,address):
        self.address = Web3.toChecksumAddress(address)
        self.ABI = getABI(self.address)

    def get_address(self):
        return self.address

    def get_ABI(self):
        return self.ABI