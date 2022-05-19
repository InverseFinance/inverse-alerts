import json
import re
import pandas as pd
from web3 import Web3
from threading import Thread

# Define a Thread to listen separately on each contract/event in the contract file
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
        print(f'contract.functions.{i}.call()')
        state_result = eval(f'contract.functions.{i}.call()')
        results.append(state_result)

    # Build table
    state_results = pd.DataFrame([results])
    state_results = state_results.set_axis(state_functions, axis=1, inplace=False)

    # Print result table and go to trigger routine
    print(state_results)
    handle_trigger(alert, tx, function, state_results, webhook)


# Get an event and define if it sends a message or not to the appropriate webhook
def handle_trigger(alert, tx, function, state_results, webhook):
    send = True
    if (alert == 'dola3crv'):
        if (function =='RemoveLiquidity'):
            title = 'DOLA3CRV Pool ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected"
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Address : " + str(tx['address']) +
                    "\n" + "Sender : " + str(tx['args']['sender']) +
                    "\n" + "Receiver : " + str(tx['args']['receiver']) +
                    "\n" + "Value : " + str(tx['args']['value']) +
                    "\n" + "Total Supply : " + str(state_results.at[0, 'totalSupply']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'])
        elif (function == 'RemoveLiquidityOne'):
            title = 'DOLA3CRV Pool ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected"
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Address : " + str(tx['address']) +
                    "\n" + "Provider : " + str(tx['args']['provider']) +
                    "\n" + "Token Amount : " + str(tx['args']['token_amount']) +
                    "\n" + "Coin Amount : " + str(tx['args']['coin_amount']) +
                    "\n" + "Token Supply : " + str(tx['args']['token_supply']) +
                    "\n" + "Total Supply : " + str(state_results.at[0, 'totalSupply()']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'])
        elif (function == 'AddLiquidity'):
            title = 'DOLA3CRV Pool ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected"
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Address : " + str(tx['address']) +
                    "\n" + "Provider : " + str(tx['args']['provider']) +
                    "\n" + "Token 0 Amount : " + str(tx['args']['token_amounts'][0]) +
                    "\n" + "Token 1 Amount : " + str(tx['args']['token_amounts'][1]) +
                    "\n" + "Fees 0 Amount : " + str(tx['args']['fees'][0]) +
                    "\n" + "Fees 1 Amount : " + str(tx['args']['fees'][1]) +
                    "\n" + "Invariant : " + str(tx['args']['invariant']) +
                    "\n" + "Token Supply : " + str(tx['args']['token_supply']) +
                    "\n" + "Total Supply : " + str(state_results.at[0, 'totalSupply()']) +
                    "\n" + "Total Supply : " + str(state_results.at[0, 'balances(0)']) +
                    "\n" + "Total Supply : " + str(state_results.at[0, 'balances(1)']) +
                    "\n" + "Address : " + str(tx['address']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'])
    elif (alert == 'lending'):
        if (function == 'Mint'):
            title = 'Lending Market New : ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected for " + str(state_results.at[0,'name()'])
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" +"Minter : " + str(tx['args']['minter']) +
                    "\n" +"Address : " + str(tx['address']) +
                    "\n" +"Mint Amount : " + str(tx['args']['mintAmount']) +
                    "\n" +"Mint Tokens : " + str(tx['args']['mintTokens']) +
                    "\n" +"Total Supply : " + str(state_results.at[0,'totalSupply()']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'])
        elif (function == 'Redeem'):
            title = 'Lending Market New : ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected for " + str(state_results.at[0,'name()'])
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" +"Redeemer : " + str(tx['args']['redeemer']) +
                    "\n" +"Address : " + str(tx['address']) +
                    "\n" +"Redeem Amount : " + str(tx['args']['redeemAmount']) +
                    "\n" +"Redeem Tokens : " + str(tx['args']['redeemTokens']) +
                    "\n" +"Total Supply : " + str(state_results.at[0,'totalSupply()']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'])
        elif (function == 'Borrow'):
            title = 'Lending Market New : ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected for " + str(state_results.at[0,'name()'])
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" +"Borrower : " + str(tx['args']['borrower']) +
                    "\n" +"Address : " + str(tx['address']) +
                    "\n" +"Borrow Amount : " + str(tx['args']['borrowAmount']) +
                    "\n" +"Account Borrows : " + str(tx['args']['accountBorrows']) +
                    "\n" +"Total Borrows : " + str(tx['args']['totalBorrows']) +
                    "\n" +"Total Supply : " + str(state_results.at[0,'totalSupply()']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'])
        elif (function == 'RepayBorrow'):
            title = 'Lending Market New : ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected for " + str(state_results.at[0,'name()'])
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" +"Payer : " + str(tx['args']['payer']) +
                    "\n" +"Address : " + str(tx['address']) +
                    "\n" +"Repaid Amount : " + str(tx['args']['repayAmount']) +
                    "\n" +"Account Borrows : " + str(tx['args']['accountBorrows']) +
                    "\n" +"Total Borrows : " + str(tx['args']['totalBorrows']) +
                    "\n" +"Total Supply : " + str(state_results.at[0,'totalSupply()']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'])
        elif (function == 'LiquidateBorrow'):
            title = 'Lending Market New : ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event'])) + " event detected for " + str(state_results.at[0,'name()'])
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" +"Liquidator : " + str(tx['args']['liquidator']) +
                    "\n" +"Borrower : " + str(tx['args']['borrower']) +
                    "\n" +"Address : " + str(tx['address']) +
                    "\n" +"Seized Token Address: " + str(tx['args']['cTokenCollateral']) +
                    "\n" +"Repay Amount : " + str(tx['args']['repayAmount']) +
                    "\n" +"Seized Tokens Amount : " + str(tx['args']['seizeTokens']) +
                    "\n" +"Total Supply : " + str(state_results.at[0,'totalSupply()']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'])
    elif (alert == 'governance'):
        if (function == 'ProposalCreated'):
            title = 'Governor Mills : New ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event']))
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Targets : " + str(tx['args']['targets']) +
                    "\n" + "Values : " + str(tx['args']['values']) +
                    "\n" + "Signatures : " + str(tx['args']['signatures']) +
                    "\n" + "Call Data : " + str(tx['args']['calldatas']) +
                    "\n" + "Description : " + str(tx['args']['description']) +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'])
        elif (function in ['ProposalCanceled', 'ProposalQueued', 'ProposalExecuted']):
            title = 'Governor Mills : New ' + re.sub(r"(\w)([A-Z])", r"\1 \2", str(tx['event']))
            body = ("Block Number : " + str(tx['blockNumber']) +
                    "\n" + "Proposal Number : " + str(tx['args']['proposalId']) +
                    "\n" + "Proposal : https://www.inverse.finance/governance/proposals/mills/" + str(tx['args']['proposalId'])  +
                    "\n" + "Transaction : https://etherscan.io/tx/" + tx['transactionHash'])

    if (send ==True):
        message = title + "\n" + body
    # "\n" + "Tag Test <@578956365205209098>")

    webhook.send(message)
