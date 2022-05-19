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
                handle_event(event, self.web3, self.alert, self.contract, self.function, self.state_functions,
                             self.webhook)


# Define function to handle events and print to the console/send to discord
def handle_event(event, web3, alert, contract, function, state_functions, webhook):
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
    message = write_message(alert, tx, function, state_results)
    webhook.send(message)


def write_message(alert, tx, function, state_results):
    if (alert == 'dola3crv'):
        if (function in ['AddLiquidity', 'RemoveLiquidity', 'RemoveLiquidityOne']):
            title = 'DOLA3CRV Pool ' + tx['event'] + "event detected"
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'] +
                    "\n" + "Full tx :" + str(tx) +
                    "\n" + "State Results :" + str(state_results))

    elif (alert == 'lending'):
        if (function == 'Mint'):
            title = 'Lending Market ' + tx['event'] + " event detected for " + state_results[1]
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "Minter : " + str(tx['minter']) +
                    "Mint Amount : " + str(tx['mintAmount']) +
                    "Mint Tokens : " + str(tx['mintTokens']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'] +
                    "\n" + "Full tx :" + str(tx) +
                    "\n" + "State Results :" + str(state_results))
        elif (function == 'Redeem'):
            title = 'Lending Market ' + tx['event'] + " event detected for " + state_results[1]
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "Redeemer : " + str(tx['redeemer']) +
                    "Redeem Amount : " + str(tx['redeemAmount']) +
                    "Redeem Tokens : " + str(tx['redeemTokens']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'] +
                    "\n" + "Full tx :" + str(tx) +
                    "\n" + "State Results :" + str(state_results))
        elif (function == 'Borrow'):
            title = 'Lending Market ' + tx['event'] + " event detected for " + state_results[1]
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "Borrower : " + str(tx['borrower']) +
                    "Borrow Amount : " + str(tx['borrowAmount']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'] +
                    "\n" + "Full tx :" + str(tx) +
                    "\n" + "State Results :" + str(state_results))
        elif (function == 'RepayBorrow'):
            title = 'Lending Market ' + tx['event'] + " event detected for " + state_results[1]
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "Payer : " + str(tx['payer']) +
                    "Repaid Amount : " + str(tx['repayAmount']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'] +
                    "\n" + "Full tx :" + str(tx) +
                    "\n" + "State Results :" + str(state_results))
        elif (function == 'LiquidateBorrow'):
            title = 'Lending Market ' + tx['event'] + " event detected for " + state_results[1]
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "Liquidator : " + str(tx['liquidator']) +
                    "Borrower : " + str(tx['borrower']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'] +
                    "\n" + "Full tx :" + str(tx) +
                    "\n" + "State Results :" + str(state_results))

    elif (alert == 'governance'):
        print('nothing')

    message = title + "\n" + body
    # "\n" + "Tag Test <@578956365205209098>")

    return message
