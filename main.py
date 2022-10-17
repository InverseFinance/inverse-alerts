# import the following dependencies
from helpers import *
from listeners import *
from contracts import *
from alerts import *
from dotenv import load_dotenv
from web3 import Web3
import logging,fetchers

# Load locals and web3 provider
load_dotenv()
LoggerParams()

try:
    n = 0

    for i in event_alerts:
        alert = event_alerts[i]['name']
        for j in contracts:
            if event_alerts[i]['name'] in contracts[j]['alerts']['events']:
                for l in contracts[j]['chain_ids']:

                    rpc = getRPC(l)
                    frequency = assignFrequency(l)
                    web3 = Web3(Web3.HTTPProvider(rpc))
                    contract_address = web3.toChecksumAddress(contracts[j]['address'])
                    contract_abi = getABI(contracts[j]['address'])

                    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

                    for k in event_alerts[i]['events']:
                        event_name = event_alerts[i]['events'][k]['name']
                        event_filters = event_alerts[i]['events'][k]['filters']
                        event_filters = fixFromToFilters(event_filters,contract_address)
                        EventListener(web3, alert, contract, event_name,event_filters, frequency).start()
                        n += 1
                        logging.info(alert + '-' +
                                     contract.address + '-' +
                                     event_name + '-' +
                                     str(n) + ' started listening at event ' +
                                     event_name + ' with filters ' +
                                     str(event_filters) + ' on contract ' +
                                     contract.address)

    for i in state_alerts:
        alert = state_alerts[i]['name']

        for j in contracts:
            if state_alerts[i]['name'] in contracts[j]['alerts']['state']:
                for l in contracts[j]['chain_ids']:

                    rpc = getRPC(l)
                    frequency = assignFrequency(l)
                    web3 = Web3(Web3.HTTPProvider(rpc))
                    contract_address = web3.toChecksumAddress(contracts[j]['address'])
                    contract_abi = getABI(contracts[j]['address'])

                    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

                    for k in state_alerts[i]['functions']:
                        state_function = state_alerts[i]['functions'][k]['name']
                        state_arguments = eval(str(state_alerts[i]['functions'][k]['arg']))

                        for argument in state_arguments:
                            StateChangeListener(web3, alert, contract, state_function, argument, frequency).start()

                        n += 1
                        logging.info(alert + '-' +
                                     contract.address + '-' +
                                     state_function + '-' +
                                     str(n) + ' started listening at state function ' +
                                     state_function + ' on contract ' +
                                     contract.address)

    for i in tx_alerts:
        alert = tx_alerts[i]['name']

        for j in contracts:
            if tx_alerts[i]['name'] in contracts[j]['alerts']['tx']:
                for l in contracts[j]['chain_ids']:
                    rpc = getRPC(l)
                    frequency = assignFrequency(l)
                    contract_name = contracts[j]["name"]
                    contract_address = web3.toChecksumAddress(contracts[j]["address"])
                    n += 1
                    TxListener(web3, alert, contract_address, contract_name, frequency).start()

                    # Log alerts-contract
                    logging.info(alert + '-' +
                                 str(contract_name) + '-' +
                                 str(n) + ' started listening at transactions on '
                                 + str(contract_name))

    for i in coingecko_alerts:
        id = coingecko_alerts[i]['id']
        if coingecko_alerts[i]['price']:
            n += 1
            CoinGeckoListener(id).start()
            logging.info("Started Coingecko price Listener " + str(id))
        if coingecko_alerts[i]['volume']:
            n += 1
            CoinGeckoVolumeListener(id).start()
            logging.info("Started Coingecko volume Listener " + str(id))

    logging.info(f'Total alerts running : {n}')

except Exception as e:
    logging.error(e)
    sendError(e)
    pass




