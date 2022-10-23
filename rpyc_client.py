# import the following dependencies
from utils.listeners import *
from utils.helpers import *
from contracts.contracts import Contract
from dotenv import load_dotenv
import rpyc
from contracts.contracts import Contract
from utils.helpers import *

try:
    web3 = getWeb3(1)
    alert = 'curve_liquidity'
    contract_obj = Contract('0xAA5A67c256e27A5d80712c51971408db3370927D', 1).get_web3_object()
    event = 'AddLiquidity'
    filters = {}
    frequency = 5

    conn = rpyc.connect("localhost", 8080,
                        config={'allow_public_attrs': True,
                                "allow_all_attrs": True,
                                "sync_request_timeout": None})
    c = conn.root
    # c.add_event_listener(web3, alert, contract_obj, event, filters, frequency)
    c.stop()
except Exception as e:
    if e.args[0]==10061:
        logging.info("Server is not running. Please start server.")
    else:
        logging.error(e)
        logging.error(e.args)