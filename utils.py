import json
from web3 import Web3
from threading import Thread


class Listener(Thread):
    def __init__(self, web3, alert, contract, function, state_functions, webhook, **kwargs):
        super(Listener, self).__init__(**kwargs)
        self.web3 = web3
        self.alert = alert
        self.contract = contract
        self.function = function
        self.state_functions = state_functions
        self.webhook = webhook
        self.event_filter = []

    def run(self):
        self.event_filter = eval(f"self.contract.events.{self.function}.createFilter(fromBlock='latest')")
        while True:
            for event in self.event_filter.get_new_entries():
                handle_event(event, self.web3, self.alert, self.contract, self.state_functions, self.webhook)


# Define function to handle events and print to the console/send to discord
def handle_event(event, web3, alert, contract, state_functions, webhook):
    tx = json.loads(Web3.toJSON(event))
    print(tx)
    results = []

    # Collect state function results

    for i in state_functions:
        state_result = eval(f'contract.functions.{i}().call()')
        results.append(state_result)
    # Build table
    state_results = [state_functions, results]

    # Print result table and send discord message
    print(state_results)

    webhook.send(alert + ' :' + tx['event'] + "Event Detected" +
                 "\n" + "Block Number : " + str(tx['blockNumber']) +
                 "\n" + "Transaction Hash : " + tx['transactionHash'] +
                 "\n" + "Etherscan : https://etherscan.io/tx/" + tx['transactionHash'] +
                 "\n" + "Full tx" + str(tx) +
                 "\n" + "State Results" + str(state_results))

    # "\n" + "Tag Test <@578956365205209098>")



