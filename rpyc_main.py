# import the following dependencies
from utils.listeners import *
from utils.helpers import *
from contracts.contracts import Contract
from dotenv import load_dotenv
from rpyc.utils.server import ThreadedServer
import threading
from threading import Thread
import rpyc,platform,signal,ctypes

# Load locals and web3 provider
load_dotenv()
LoggerParams()

class Launchers():
    def start_all(self):
        alerts = load_alerts()
        for alert in alerts:
            if alert != 'test':
                if alerts[alert]['type'] == 'event':
                    for contract in alerts[alert]['contracts']:
                        for chain_id in alerts[alert]['contracts'][contract]['chain_ids']:
                            for event in alerts[alert]['events']:
                                web3 = getWeb3(chain_id)
                                contract_address = web3.toChecksumAddress(alerts[alert]['contracts'][contract]['address'])
                                contract_obj = web3.eth.contract(address=contract_address, abi=getABI(contract_address))
                                filters = fixFromToFilters(alerts[alert]['events'][event]['filters'], contract_address)
                                frequency = assignFrequency(chain_id)
                                EventListener(web3, alert, contract_obj, event, filters, frequency).start()

                if alerts[alert]['type'] == 'state':
                    for contract in alerts[alert]['contracts']:
                        for chain_id in alerts[alert]['contracts'][contract]['chain_ids']:
                            for function in alerts[alert]['functions']:
                                web3 = getWeb3(chain_id)
                                arguments = eval(alerts[alert]['functions'][function]['arg'])

                                for argument in arguments or []:
                                    contract_address = web3.toChecksumAddress(alerts[alert]['contracts'][contract]['address'])
                                    contract_obj = web3.eth.contract(address=contract_address, abi=getABI(contract_address))
                                    frequency = assignFrequency(chain_id)
                                    StateChangeListener(web3, alert, contract_obj, function, argument, frequency).start()

                if alerts[alert]['type'] == 'transaction':
                    for contract in alerts[alert]['contracts']:
                        for chain_id in alerts[alert]['contracts'][contract]['chain_ids']:
                            web3 = getWeb3(chain_id)
                            contract_address = web3.toChecksumAddress(alerts[alert]['contracts'][contract]['address'])
                            contract_obj = web3.eth.contract(address=contract_address, abi=getABI(contract_address))
                            frequency = assignFrequency(chain_id)
                            TxListener(web3, alert, contract_obj, contract, frequency).start()

                if alerts[alert]['type'] == 'coingecko':
                    for id in alerts[alert]['ids']:
                        if alerts[alert]['ids'][id]['price'] == True:
                            CoinGeckoListener(id).start()
                        if alerts[alert]['ids'][id]['volume'] == True:
                            CoinGeckoVolumeListener(id).start()
        return
    def add_event_listener(self,web3, alert, contract_obj, event, filters, frequency):
        EventListener(web3, alert, contract_obj, event, filters, frequency).start()
        return
    def add_state_listener(self,web3, alert, contract_obj, function, argument, frequency):
        StateChangeListener(web3, alert, contract_obj, function, argument, frequency).start()
        return
    def add_tx_listener(self,web3, alert, contract_obj, contract, frequency):
        TxListener(web3, alert, contract_obj, contract, frequency).start()
        return

class MyService(rpyc.Service):
    """
    def on_connect(self, conn):
        print('Connected')
        pass

    def on_disconnect(self, conn):
        print('Disconnected')
        pass
    """
    def start(self):
        return main.start_all()

    def exposed_add_event_listener(self,web3, alert, contract_obj, event, filters, frequency):
        return main.add_event_listener(web3, alert, contract_obj, event, filters, frequency)

    def exposed_add_state_listener(self,web3, alert, contract_obj, function, argument, frequency):
        return main.add_state_listener(web3, alert, contract_obj, function, argument, frequency)

    def exposed_add_tx_listener(self,web3, alert, contract_obj, contract, frequency):
        return main.add_tx_listener(web3, alert, contract_obj, contract, frequency)

    def exposed_stop(self):
        pid = os.getpid()

        if platform.system() == 'Windows':
            PROCESS_TERMINATE = 1
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
            logging.info("Closing server and all listeners.")
            ctypes.windll.kernel32.TerminateProcess(handle, -1)
            ctypes.windll.kernel32.CloseHandle(handle)
        else:
            os.kill(pid, signal.SIGTERM)

if __name__ == '__main__':
    server = ThreadedServer(MyService,
                            port = 8080,
                            protocol_config={'allow_public_attrs': True,
                                             "allow_all_attrs": True,
                                             "sync_request_timeout":None})

    threaded_server = Thread(target = server.start)
    threaded_server.daemon = True
    threaded_server.start()

    main = Launchers()
    main.start_all()
"""
    for thread in threading.enumerate():
        print(thread.name)
"""


