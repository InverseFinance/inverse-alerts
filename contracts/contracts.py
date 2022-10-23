from utils.helpers  import *
from web3 import Web3
import logging
import random

class Contract:
    def __init__(self,address,chain_id):
        try:
            contracts = load_contracts()
            self.address = Web3.toChecksumAddress(address)
            self.chain_id = int(chain_id)
            self.ABI = getABI2(self.address,self.chain_id)
            self.web3 = getWeb3(chain_id)
            self.exists = False
            for c in contracts:
                if contracts[c]['address']==address:
                    self.name = c
                    self.exists = True

        except AttributeError as e:
            logging.error(e)
            logging.info(f"Contract is not registered in contracts.json file. Add it first before adding it to your alert.")
    def add_to_json(self):
        contracts = (load_contracts())
        create_contract = True
        add_chain = True

        while create_contract:
            for c in contracts.copy():
                if Web3.toChecksumAddress(contracts[c]["address"]) == self.address:
                    print(f"""Contract {contracts[c]["address"]} already exists with name {c} and chain_ids {contracts[c]["chain_ids"]}""")
                    if self.chain_id in contracts[c]["chain_ids"]:
                        add_chain = False
                    create_contract = False

            if create_contract:
                contracts[self.name] = {"address": self.address, "chain_ids": [self.chain_id]}
                print(f"Contract {self.address} created with name {self.name} and chain_id {self.chain_id}")
                create_contract = False
                add_chain  = False

        while add_chain:
            for c in (contracts.copy()):
                if Web3.toChecksumAddress(contracts[c]["address"]) == self.address:
                    while add_chain:
                        if self.chain_id in contracts[c]["chain_ids"]:
                            print(f"""Chain {self.chain_id} already exists on contract {self.address}""")
                            add_chain = False
                        else:
                            contracts[c]["chain_ids"].append(self.chain_id)
                            print(f"""Chain {self.chain_id} added on existing contract {self.address}""")
                            add_chain = False

        save_contracts(contracts)
    def remove_from_json(self):
        contracts = (load_contracts())
        remove_contract = True
        remove_chain = True

        print(f"Removing contract {self.address} from chain {self.chain_id}")

        while remove_chain:
            for c in (contracts.copy()):
                if Web3.toChecksumAddress(contracts[c]["address"]) == self.address:
                    if self.chain_id in contracts[c]["chain_ids"]:
                        contracts[c]["chain_ids"].remove(self.chain_id)
                        print(f"""Chain {self.chain_id} removed from contract {self.address}""")
                        remove_chain = False
                    else:
                        print(f"""Chain {self.chain_id} does not exist on contract {self.address}""")
                        remove_chain = False
            remove_chain = False

        while remove_contract:

            for c in (contracts.copy()):
                if Web3.toChecksumAddress(contracts[c]["address"]) == self.address and contracts[c][
                    "chain_ids"] == []:
                    del contracts[c]
                    print(f"Contract {self.address} removed")
                    remove_contract = False

                elif Web3.toChecksumAddress(contracts[c]["address"]) == self.address and contracts[c][
                    "chain_ids"] != []:
                    print(f"""Contract {self.address} has active chains : {contracts[c]["chain_ids"]}""")
                    remove_contract = False

            if remove_contract:
                print(f"Contract doesnt exist")
                remove_contract = False

        save_contracts(contracts)
    def get_entry_from_json(self):
        contracts = load_contracts()
        is_in_list = False

        for c in contracts:
            if contracts[c]['address']==self.address:
                is_in_list = True
                return contracts[c]
        if not is_in_list :
            print("Contract is not in contracts.json file. Please add your contract first")
            return None
    def list_events(self):
        events = []
        for item in self.ABI:
            if item["type"] == 'event':
                events.append(item['name'])
        return(events)
    def list_functions(self):
        events = []
        for item in self.ABI:
            if item["type"] == 'function':
                events.append(item['name'])
        return(events)
    def get(self):
        contract = self.web3.eth.contract(address=self.address, abi=self.ABI)
        return contract

