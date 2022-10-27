# import the following dependencies
from utils.listeners import *
from utils.helpers import *
from contracts.contracts import Contract
from dotenv import load_dotenv
import logging
import asyncio

# Load locals and web3 provider
load_dotenv()
LoggerParams()

def main():
    for alert in alerts:

            if alerts[alert]['type'] == 'transaction':
                for contract in alerts[alert]['contracts']:
                    for chain_id in alerts[alert]['contracts'][contract]['chain_ids']:
                        web3 = getWeb3(chain_id)
                        contract_address = web3.toChecksumAddress(alerts[alert]['contracts'][contract]['address'])
                        contract_obj = web3.eth.contract(address=contract_address, abi=getABI(contract_address))
                        frequency = assignFrequency(chain_id)
                        TxListener(web3, alert, contract_obj, contract, frequency).start()


if __name__ == "__main__":
    alerts = load_alerts()
    main()