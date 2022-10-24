from contracts.contracts import Contract
from utils.helpers import *
import rpyc

def stop_server():
    try:
        conn = rpyc.connect("localhost", 8080,
                            config={'allow_public_attrs': True,
                                    "allow_all_attrs": True,
                                    "sync_request_timeout": None})
        c = conn.root
        c.stop()
    except Exception as e:
        if str(10061) in str(e.args[0]):
            logging.info("Server is not running. Please start server.")
        elif str(10054) in str(e.args[0]):
            logging.info("Server was closed successfully.")
        else:
            logging.error(e)

def add_event_listener(web3, alert, contract_obj, event, filters, frequency):
    try:
        conn = rpyc.connect("localhost", 8080,
                            config={'allow_public_attrs': True,
                                    "allow_all_attrs": True,
                                    "sync_request_timeout": None})
        c = conn.root
        c.add_event_listener(web3, alert, contract_obj, event, filters, frequency)
    except Exception as e:
            logging.error(e)

def add_state_listener(web3, alert, contract_obj, function, argument, frequency):

    conn = rpyc.connect("localhost", 8080,
                        config={'allow_public_attrs': True,
                                "allow_all_attrs": True,
                                "sync_request_timeout": None})
    c = conn.root
    c.add_state_listener(web3, alert, contract_obj, event, function, argument, frequency)

def add_tx_listener(self,web3, alert, contract_obj, contract, frequency):

    conn = rpyc.connect("localhost", 8080,
                        config={'allow_public_attrs': True,
                                "allow_all_attrs": True,
                                "sync_request_timeout": None})
    c = conn.root
    c.add_tx_listener(web3, alert, contract_obj, contract, frequency)

web3 = getWeb3(1)
alert = 'curve_liquidity'
contract_obj = Contract('0xAA5A67c256e27A5d80712c51971408db3370927D', 1).get_web3_object()
event = 'AddLiquidity'
filters = {}
frequency = 5

add_event_listener(web3, alert, contract_obj, event, filters, frequency)
stop_server()