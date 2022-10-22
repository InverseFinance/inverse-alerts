# import the following dependencies
from utils.listeners import *
from utils.helpers import *
from dotenv import load_dotenv
from brownie import Contract

# Load locals and web3 provider
load_dotenv()
LoggerParams()

def main():
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
                            EventListener2(web3, alert, contract_obj, event, filters, frequency).start()
"""
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
                        TxListener(web3, alert, contract_obj, contract, frequency)

            if alerts[alert]['type'] == 'coingecko':
                for id in alerts[alert]['ids']:
                    if alerts[alert]['ids'][id]['price'] == True:
                        CoinGeckoListener(id)
                    if alerts[alert]['ids'][id]['volume'] == True:
                        CoinGeckoVolumeListener(id)
"""
if __name__ == "__main__":
    alerts = load_alerts()
    main()