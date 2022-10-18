# import the following dependencies
import os,json,re,fetchers,logging,requests,sys,time
import pandas as pd
from helpers import *
from threading import Thread
from web3 import Web3



# Define event to handle and logs to the console/send to discord
class HandleEvent(Thread):
    def __init__(self, web3,event, alert,contract, event_name, **kwargs):
        super(HandleEvent, self).__init__(**kwargs)
        self.web3 = web3
        self.event = event
        self.alert = alert
        self.event_name = event_name
        self.contract=contract

    def run(self):
        while True:
            try:
                self.tx = json.loads(Web3.toJSON(self.event))
                send = False
                webhook = ''
                title = ''
                content= ''
                fields = []
                image = ''
                color = colors.blurple
                
                address=self.tx["address"]
                blockNumber=self.tx["blockNumber"]
                transactionHash=self.tx["transactionHash"]

                if (self.alert == "curve_liquidity"):
                    # logs result table and start writing message
                    pool_address = address

                    if pool_address=="0xAA5A67c256e27A5d80712c51971408db3370927D":
                        webhook = os.getenv('WEBHOOK_DOLA3CRV')
                        token_0 = 'DOLA'
                        token_1 = '3CRV'
                        token_0_address = '0x865377367054516e17014CcdED1e7d814EDC9ce4'
                        token_1_address = '0x6c3f90f043a72fa612cbac8115ee7e52bde6e490'
                        token_0_total = fetchers.getBalance(self.web3,pool_address,token_0_address)
                        token_1_total = fetchers.getBalance(self.web3, pool_address, token_1_address)
                        image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/833844/1457892/c8141b30-aa8c-4588-8d42-877ce649abee.jpg"
                    elif pool_address=="0xE57180685E3348589E9521aa53Af0BCD497E884d":
                        webhook = os.getenv('WEBHOOK_DOLAFRAXBP')
                        token_0 = 'DOLA'
                        token_1 = 'crvFRAX'
                        token_0_address = '0x865377367054516e17014CcdED1e7d814EDC9ce4'
                        token_1_address = '0x3175Df0976dFA876431C2E9eE6Bc45b65d3473CC'
                        token_0_total = fetchers.getBalance(self.web3,pool_address,token_0_address)
                        token_1_total = fetchers.getBalance(self.web3, pool_address, token_1_address)
                        image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/1300762/2228671/f10870d8-4e95-474d-a47a-d75b05cd2a99.jpg"


                    if (self.event_name == "RemoveLiquidity"):
                        if (self.tx["args"]["token_amounts"][0] + self.tx["args"]["token_amounts"][1]) / 1e18 > 500000:
                            content = '<@&945071604642222110>'
                        color = colors.red
                        send = True
                        title = token_0 + token_1+ " Pool Liquidity Removal event detected"
                        fields = [{"name":'Block :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'Provider :',"value":str(f'[{self.tx["args"]["provider"]}](https://etherscan.io/address/{self.tx["args"]["provider"]})'),"inline":False},
                        {"name": token_0+' Amount :',"value":str(formatCurrency(self.tx["args"]["token_amounts"][0] / 1e18)),"inline":True},
                        {"name":token_1+' Amount :',"value":str(formatCurrency(self.tx["args"]["token_amounts"][1] / 1e18)),"inline":True},
                        {"name":token_0+' in Pool :',"value":str(formatCurrency(token_0_total)),"inline":True},
                        {"name":token_1+' in Pool :',"value":str(formatCurrency(token_1_total)),"inline":True},
                        {"name":token_0+'+'+token_1+' in Pool',"value":str(formatCurrency(token_0_total + token_1_total)),"inline":False},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]
                        if (self.tx["args"]["token_amounts"][0] + self.tx["args"]["token_amounts"][1]) / 1e18 > 50000:
                            send = True
                    elif (self.event_name == "RemoveLiquidityOne" ):
                        if self.tx["args"]["coin_amount"] / 1e18 > 500000:
                            content = '<@&945071604642222110>'
                        color = colors.red
                        send = True
                        title = token_0+token_1+" Pool Liquidity Removal event detected"
                        fields = [
                        {"name":'Block :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'Provider :',"value":str(f'[{self.tx["args"]["provider"]}](https://etherscan.io/address/{self.tx["args"]["provider"]})'),"inline":False},
                        {"name":'Token Amount :',"value":str(formatCurrency(self.tx["args"]["coin_amount"] / 1e18)),"inline":True},
                        {"name":'Token Symbol :',"value":str(fetchers.getRemovedTokenSymbol(self.web3,transactionHash,address)),"inline":True},
                        {"name":token_0+' in Pool :',"value":str(formatCurrency(token_0_total)),"inline":True},
                        {"name":token_1+' in Pool :',"value":str(formatCurrency(token_1_total)),"inline":True},
                        {"name":token_0+'+'+token_1+' in Pool',"value":str(formatCurrency(token_0_total + token_1_total)),"inline":False},
                        {"name": 'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        if (self.tx["args"]["coin_amount"] / 1e18) > 50000:
                            send = True
                    elif (self.event_name == "AddLiquidity"):
                        if (self.tx["args"]["token_amounts"][0] + self.tx["args"]["token_amounts"][1]) / 1e18 > 500000:
                            content = '<@&945071604642222110>'

                        title = token_0+token_1+" Pool Liquidity Add event detected"
                        fields = [{"name":'Block :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'Provider :',"value":str(f'[{self.tx["args"]["provider"]}](https://etherscan.io/address/{self.tx["args"]["provider"]})'),"inline":False},
                        {"name":token_0+' Amount :',"value":str(formatCurrency(self.tx["args"]["token_amounts"][0] / 1e18)),"inline":True},
                        {"name":token_1+' Amount :',"value":str(formatCurrency(self.tx["args"]["token_amounts"][1] / 1e18)),"inline":True},
                        {"name":token_0+' in Pool :',"value":str(formatCurrency(token_0_total)),"inline":True},
                        {"name":token_1+' in Pool :',"value":str(formatCurrency(token_1_total)),"inline":True},
                        {"name":token_0+'+'+token_1+' in Pool',"value":str(formatCurrency(token_0_total + token_1_total)),"inline":False},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        color = colors.dark_green
                        if (self.tx["args"]["token_amounts"][0] + self.tx["args"]["token_amounts"][1]) / 1e18 > 50000:
                            send = True

                    concave = ["0x6fF51547f69d05d83a7732429cfe4ea1E3299E10","0x226e7AF139a0F34c6771DeB252F9988876ac1Ced"]

                    if self.tx["args"]["provider"] in concave:
                        webhook = os.getenv('WEBHOOK_CONCAVE')
                        title = 'Concave Activity : ' + title
                        content = '<@&945071604642222110>'

                elif (self.alert == "gauge_controller"):
                    gauges = ["0xBE266d68Ce3dDFAb366Bb866F4353B6FC42BA43c","0x8Fa728F393588E8D8dD1ca397E9a710E53fA553a"]
                    gauge_address = str(self.tx["args"]["gauge_addr"])
                    
                    if gauge_address  in gauges:
                        vecrv_address = "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2"
                        vecrv_supply = fetchers.getSupply(self.web3,vecrv_address)
                        user = self.tx["args"]["user"]
                        user_vecrv_balance = fetchers.getBalance(self.web3,user,vecrv_address)
                        weight = self.tx["args"]["weight"]
                    else: break
                    
                    if gauge_address=="0xBE266d68Ce3dDFAb366Bb866F4353B6FC42BA43c":
                        webhook = os.getenv('WEBHOOK_DOLAFRAXBP')
                        pool_address="0xE57180685E3348589E9521aa53Af0BCD497E884d"
                        token_0 = "DOLA"
                        token_1 = "crvFRAX"
                        image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/1349566/2302403/6731fd1b-9cb1-4ca8-a321-1025b786a010.jpg"
                        content = '<@&945071604642222110>'
                        color = colors.dark_green
                        send = True
                    elif gauge_address=="0x8Fa728F393588E8D8dD1ca397E9a710E53fA553a":
                        webhook = os.getenv('WEBHOOK_DOLA3CRV')
                        pool_address = "0xAA5A67c256e27A5d80712c51971408db3370927D"
                        token_0 = "DOLA"
                        token_1 = "3CRV"
                        image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/1348784/2301280/9afceee3-e958-441a-b77a-5558a7a08595.jpg"
                        content = '<@&945071604642222110>'
                        color = colors.dark_green
                        send = True
                        
                    
                    if (self.event_name == "NewGaugeWeight" and (gauge_address in gauges)):
                        title = token_0 + token_1 +" New Gauge Weight detected"
                        fields = [{"name":'Block :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Gauge Address :',"value":str(f'[{gauge_address}](https://etherscan.io/address/{gauge_address})'),"inline":False},
                        {"name":'Pool Address :',"value":str(f'[{pool_address}](https://etherscan.io/address/{pool_address})'),"inline":False},
                        {"name":'% Weight :',"value":str(formatPercent(weight/1000)),"inline":True},
                        {"name":'veCRV Weight :',"value":str(formatCurrency(user_vecrv_balance  * weight/10000)),"inline":True},
                        {"name":'veCRV Balance :',"value":str(formatPercent(user_vecrv_balance )),"inline":True},
                        {"name":'Balance / veCRV Supply :',"value":str(formatPercent(user_vecrv_balance  / vecrv_supply)),"inline":True},
                        {"name": 'Total Weight :',"value":str(self.tx["args"]["total_weight"]),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]
                    elif (self.event_name == "VoteForGauge" and (gauge_address in gauges)):
                        title = token_0 + token_1 + " Pool Vote For Gauge detected"
                        fields = [{"name":'Block :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'User :',"value":str(f'[{user}](https://etherscan.io/address/{user})'),"inline":False},
                        {"name":'Gauge Address :',"value":str(f'[{gauge_address}](https://etherscan.io/address/{gauge_address})'),"inline":False},
                        {"name":'Pool Address :',"value":str(f'[{pool_address}](https://etherscan.io/address/{pool_address})'),"inline":False},
                        {"name":'Weight :',"value":str(formatPercent(weight/10000)),"inline":True},
                        {"name":'veCRV Weight :',"value":str(formatCurrency(user_vecrv_balance  * weight/10000)),"inline":True},
                        {"name":'veCRV Balance :',"value":str(formatPercent(user_vecrv_balance )),"inline":True},
                        {"name":'Balance / veCRV Supply :',"value":str(formatPercent(user_vecrv_balance / vecrv_supply)),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                elif (self.alert in ["lending1", "lending2"]):
                    market_symbol = fetchers.getSymbol(self.web3,address)
                    market_decimals = fetchers.getDecimals(self.web3,address)
                    underlying_address = fetchers.getUnderlying(self.web3,address)
                    underlying_decimals = fetchers.getDecimals(self.web3,underlying_address)
                    underlying_price = fetchers.getUnderlyingPrice(self.web3,address)
                    market_supply = fetchers.getSupply(self.web3,address)
                    market_cash = fetchers.getCash(self.web3,address)
                    
                    if (self.event_name == "Mint"):
                        webhook = os.getenv('WEBHOOK_SUPPLY')
                        title = "Lending Market : New Deposit event detected for " + str(market_symbol)
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Minter :',"value":str(f'[{self.tx["args"]["minter"]}](https://etherscan.io/address/{self.tx["args"]["minter"]})'),"inline":True},
                        {"name":'Market Symbol :',"value":str(market_symbol),"inline":True},
                        {"name":'USD Value',"value":str(formatCurrency(self.tx["args"]["mintAmount"] / underlying_decimals * underlying_price)),"inline":True},
                        {"name":'Mint Amount :',"value":str(formatCurrency(self.tx["args"]["mintAmount"] / underlying_decimals)),"inline":True},
                        {"name":'Mint Tokens :',"value":str(formatCurrency(self.tx["args"]["mintTokens"] / market_decimals)),"inline":True},
                        {"name":'Total Supply',"value":str(formatCurrency(market_supply)),"inline":True},
                        {"name":'Total Cash :',"value":str(formatCurrency(market_cash)),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        if ((self.tx["args"]["mintAmount"] / underlying_decimals * underlying_price)>100000):
                            content = '<@&945071604642222110>'

                        color = colors.blurple
                        send = True

                    elif (self.event_name == "Redeem"):
                        webhook = os.getenv('WEBHOOK_SUPPLY')
                        title = "Lending Market : New Withdrawal event detected for " + str(market_symbol)
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Redeemer :',"value":str(f'[{self.tx["args"]["redeemer"]}](https://etherscan.io/address/{self.tx["args"]["redeemer"]})'),"inline":True},
                        {"name":'Market Symbol :',"value":str(market_symbol),"inline":True},
                        {"name":'Market Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'USD Value',"value":str(formatCurrency(self.tx["args"]["redeemAmount"] / underlying_decimals * underlying_price)),"inline":True},
                        {"name":'Redeem Amount :',"value":str(formatCurrency(self.tx["args"]["redeemAmount"] / underlying_decimals)),"inline":True},
                        {"name":'Redeem Tokens :',"value":str(formatCurrency(self.tx["args"]["redeemTokens"] / market_decimals)),"inline":True},
                        {"name":'Total Supply',"value":str(formatCurrency(market_supply)),"inline":True},
                        {"name":'Total Cash :',"value":str(formatCurrency(market_cash)),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        if ((self.tx["args"]["redeemAmount"] / underlying_decimals * underlying_price)>100000):
                            content = '<@&945071604642222110>'

                        color = colors.blurple
                        send = True
                    elif (self.event_name == "Borrow"):
                        webhook = os.getenv('WEBHOOK_BORROW')
                        title = "Lending Market : New Borrow event detected for " + str(market_symbol)
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Borrower :',"value":str(f'[{self.tx["args"]["borrower"]}](https://etherscan.io/address/{self.tx["args"]["borrower"]})'),"inline":True},
                        {"name":'Market Symbol :',"value":str(market_symbol),"inline":False},
                        {"name":'Market Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":True},
                        {"name":'USD Value :',"value":str(formatCurrency(self.tx["args"]["borrowAmount"] / underlying_decimals * underlying_price)),"inline":True},
                        {"name":'Borrow Amount :',"value":str(formatCurrency(self.tx["args"]["borrowAmount"] / underlying_decimals)),"inline":True},
                        {"name":'Account Borrows :',"value":str(formatCurrency(self.tx["args"]["accountBorrows"] / underlying_decimals)),"inline":True},
                        {"name":'Total Borrows :',"value":str(formatCurrency(self.tx["args"]["totalBorrows"] / underlying_decimals)),"inline":True},
                        {"name":'Total Supply :',"value":str(formatCurrency(market_supply)),"inline":True},
                        {"name":'Total Cash :',"value":str(formatCurrency(market_cash)),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]


                        if ((self.tx["args"]["borrowAmount"] / underlying_decimals * underlying_price)>100000):
                            content = '<@&945071604642222110>'

                        color = colors.blurple
                        send = True
                    elif (self.event_name == "RepayBorrow"):
                        webhook = os.getenv('WEBHOOK_BORROW')
                        title = "Lending Market : New Repayment event detected for " + str(market_symbol)
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Borrower :',"value":str(f'[{self.tx["args"]["borrower"]}](https://etherscan.io/address/{self.tx["args"]["borrower"]})'),"inline":True},
                        {"name":'Market Symbol :',"value":str(market_symbol),"inline":False},
                        {"name":'Market Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":True},
                        {"name":'USD Value :',"value":str(formatCurrency(self.tx["args"]["repayAmount"] / underlying_decimals * underlying_price)),"inline":True},
                        {"name": 'Borrow Amount :',"value":str(formatCurrency(self.tx["args"]["repayAmount"] / underlying_decimals)),"inline":True},
                        {"name":'Account Borrows :',"value":str(formatCurrency(self.tx["args"]["accountBorrows"] / underlying_decimals)),"inline":True},
                        {"name":'Total Borrows :',"value":str(formatCurrency(self.tx["args"]["totalBorrows"] / underlying_decimals)),"inline":True},
                        {"name":'Total Supply :',"value":str(formatCurrency(market_supply)),"inline":True},
                        {"name":'Total Cash :',"value":str(formatCurrency(market_cash)),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        if ((self.tx["args"]["repayAmount"] / underlying_decimals * underlying_price)>100000):
                            content = '<@&945071604642222110>'

                        color = colors.blurple
                        send = True
                    elif (self.event_name == "LiquidateBorrow"):
                        title = "Lending Market New Liquidation event detected for " + str(market_symbol)
                        webhook = os.getenv('WEBHOOK_LIQUIDATIONS')
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Liquidator :',"value":str(f'[{self.tx["args"]["liquidator"]}](https://etherscan.io/address/{self.tx["args"]["liquidator"]})'),"inline":False},
                        {"name":'Borrower :',"value":str(f'[{self.tx["args"]["borrower"]}](https://etherscan.io/address/{self.tx["args"]["borrower"]})'),"inline":False},
                        {"name":'Market Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'Seized Amount :',"value":str(formatCurrency(self.tx["args"]["seizeTokens"]/ fetchers.getDecimals(self.web3,self.tx["args"]["cTokenCollateral"]))),"inline":True},
                        {"name":'Seized Token  :',"value":str(fetchers.getSymbol(self.web3,self.tx["args"]["cTokenCollateral"])),"inline":True},
                        {"name":'Repay Amount :',"value":str(formatCurrency(self.tx["args"]["repayAmount"]/ underlying_decimals)),"inline":False},
                        {"name":'Repay Amount USD:',"value":str(formatCurrency(self.tx["args"]["repayAmount"]* underlying_price/ underlying_decimals)),"inline":True},
                        {"name":'Repay Token  :',"value":str(market_symbol),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        if ((self.tx["args"]["repayAmount"]/ underlying_decimals)>100000):
                            content = '<@&945071604642222110>'

                        color = colors.blurple
                        send = True

                elif (self.alert in ["lendingfuse127"]):
                    market_symbol = fetchers.getSymbol(self.web3,address)
                    market_decimals = fetchers.getDecimals(self.web3,address)
                    underlying_address = fetchers.getUnderlyingFuse(self.web3,address)
                    underlying_decimals = fetchers.getDecimals(self.web3,underlying_address)
                    underlying_price = fetchers.getUnderlyingPriceFuse(self.web3,address)
                    market_supply = fetchers.getSupply(self.web3,address)
                    market_cash = fetchers.getCash(self.web3,address)
                    if (self.event_name == "Mint"):
                        webhook = os.getenv('WEBHOOK_127')
                        title = "Lending Market : New Deposit event detected for " + str(market_symbol)
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Minter :',"value":str(f'[{self.tx["args"]["minter"]}](https://etherscan.io/address/{self.tx["args"]["minter"]})'),"inline":True},
                        {"name":'Market Symbol :',"value":str(market_symbol),"inline":True},
                        {"name":'Market Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'ETH Value',"value":str(formatCurrency(self.tx["args"]["mintAmount"] / underlying_decimals * underlying_price)),"inline":True},
                        {"name":'Mint Amount :',"value":str(formatCurrency(self.tx["args"]["mintAmount"] / underlying_decimals)),"inline":True},
                        {"name":'Mint Tokens :',"value":str(formatCurrency(self.tx["args"]["mintTokens"] / market_decimals)),"inline":True},
                        {"name":'Total Supply',"value":str(formatCurrency(market_supply)),"inline":True},
                        {"name":'Total Cash :',"value":str(formatCurrency(market_cash)),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        if ((self.tx["args"]["mintAmount"] / underlying_decimals * underlying_price)>100000):
                            content = '<@&945071604642222110>'
                        color = colors.blurple
                        send = True
                    elif (self.event_name == "Redeem"):
                        webhook = os.getenv('WEBHOOK_127')
                        title = "Lending Market : New Withdrawal event detected for " + str(market_symbol)
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Redeemer :',"value":str(f'[{self.tx["args"]["redeemer"]}](https://etherscan.io/address/{self.tx["args"]["redeemer"]})'),"inline":True},
                        {"name":'Market Symbol :',"value":str(market_symbol),"inline":True},
                        {"name":'Market Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'ETH Value',"value":str(formatCurrency(self.tx["args"]["redeemAmount"] / underlying_decimals * underlying_price)),"inline":True},
                        {"name":'Redeem Amount :',"value":str(formatCurrency(self.tx["args"]["redeemAmount"] / underlying_decimals)),"inline":True},
                        {"name":'Redeem Tokens :',"value":str(formatCurrency(self.tx["args"]["redeemTokens"] / market_decimals)),"inline":True},
                        {"name":'Total Supply',"value":str(formatCurrency(market_supply)),"inline":True},
                        {"name":'Total Cash :',"value":str(formatCurrency(market_cash)),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        if ((self.tx["args"]["redeemAmount"] / underlying_decimals * underlying_price)>100000):
                            content = '<@&945071604642222110>'

                        color = colors.blurple
                        send = True
                    elif (self.event_name == "Borrow"):
                        webhook = os.getenv('WEBHOOK_127')
                        title = "Lending Market : New Borrow event detected for " + str(market_symbol)
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Borrower :',"value":str(f'[{self.tx["args"]["borrower"]}](https://etherscan.io/address/{self.tx["args"]["borrower"]})'),"inline":True},
                        {"name":'Market Symbol :',"value":str(market_symbol),"inline":False},
                        {"name":'Market Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":True},
                        {"name":'ETH Value :',"value":str(formatCurrency(self.tx["args"]["borrowAmount"] / underlying_decimals * underlying_price)),"inline":True},
                        {"name":'Borrow Amount :',"value":str(formatCurrency(self.tx["args"]["borrowAmount"] / underlying_decimals)),"inline":True},
                        {"name":'Account Borrows :',"value":str(formatCurrency(self.tx["args"]["accountBorrows"] / underlying_decimals)),"inline":True},
                        {"name":'Total Borrows :',"value":str(formatCurrency(self.tx["args"]["totalBorrows"] / underlying_decimals)),"inline":True},
                        {"name":'Total Supply :',"value":str(formatCurrency(market_supply)),"inline":True},
                        {"name":'Total Cash :',"value":str(formatCurrency(market_cash)),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]


                        if ((self.tx["args"]["borrowAmount"] / underlying_decimals * underlying_price)>100000):
                            content = '<@&945071604642222110>'

                        color = colors.blurple
                        send = True
                    elif (self.event_name == "RepayBorrow"):
                        webhook = os.getenv('WEBHOOK_127')
                        title = "Lending Market : New Repayment event detected for " + str(market_symbol)
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Borrower :',"value":str(f'[{self.tx["args"]["borrower"]}](https://etherscan.io/address/{self.tx["args"]["borrower"]})'),"inline":True},
                        {"name":'Market Symbol :',"value":str(market_symbol),"inline":False},
                        {"name":'Market Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":True},
                        {"name":'ETH Value :',"value":str(formatCurrency(self.tx["args"]["repayAmount"] / underlying_decimals * underlying_price)),"inline":True},
                        {"name":'Borrow Amount :',"value":str(formatCurrency(self.tx["args"]["repayAmount"] / underlying_decimals)),"inline":True},
                        {"name":'Account Borrows :',"value":str(formatCurrency(self.tx["args"]["accountBorrows"] / underlying_decimals)),"inline":True},
                        {"name":'Total Borrows :',"value":str(formatCurrency(self.tx["args"]["totalBorrows"] / underlying_decimals)),"inline":True},
                        {"name":'Total Supply :',"value":str(formatCurrency(market_supply)),"inline":True},
                        {"name":'Total Cash :',"value":str(formatCurrency(market_cash)),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        if ((self.tx["args"]["repayAmount"] / underlying_decimals * underlying_price)>100000):
                            content = '<@&945071604642222110>'

                        color = colors.blurple
                        send = True
                    elif (self.event_name == "LiquidateBorrow"):
                        title = "Lending Market New Liquidation event detected for " + str(market_symbol)
                        webhook = os.getenv('WEBHOOK_127')
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Liquidator :',"value":str(f'[{self.tx["args"]["liquidator"]}](https://etherscan.io/address/{self.tx["args"]["liquidator"]})'),"inline":False},
                        {"name":'Borrower :',"value":str(f'[{self.tx["args"]["borrower"]}](https://etherscan.io/address/{self.tx["args"]["borrower"]})'),"inline":False},
                        {"name":'Market Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'Seized Amount :',"value":str(formatCurrency(self.tx["args"]["seizeTokens"]/ fetchers.getDecimals(self.web3,self.tx["args"]["cTokenCollateral"]))),"inline":True},
                        {"name":'Seized Token  :',"value":str(fetchers.getSymbol(self.web3,self.tx["args"]["cTokenCollateral"])),"inline":True},
                        {"name":'Repay Amount :',"value":str(formatCurrency(self.tx["args"]["repayAmount"]/ underlying_decimals)),"inline":False},
                        {"name":'Repay Amount ETH:',"value":str(formatCurrency(self.tx["args"]["repayAmount"]* underlying_price/ underlying_decimals)),"inline":True},
                        {"name":'Repay Token  :',"value":str(market_symbol),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        if ((self.tx["args"]["repayAmount"]/ underlying_decimals)>100000):
                            content = '<@&945071604642222110>'

                        color = colors.blurple
                        send = True

                elif (self.alert == "governance"):
                    content = "<@&899302193608409178>"
                    webhook = os.getenv('WEBHOOK_GOVERNANCE')

                    if (self.event_name == "ProposalCreated"):
                        title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(self.tx["event"]))

                        fields = [{"name":'Block Number :', "value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'), "inline": True},
                                {"name": 'Start Block :',"value": str(f'[{self.tx["args"]["startBlock"]}](https://etherscan.io/block/{self.tx["args"]["startBlock"]})'),"inline": True},
                                {"name": 'End Block :',"value": str(f'[{self.tx["args"]["endBlock"]}](https://etherscan.io/block/{self.tx["args"]["endBlock"]})'),"inline": True},
                                {"name":'Proposal :', "value":"https://www.inverse.finance/governance/proposals/mills/" + str(fetchers.getProposalCount(self.web3)), "inline": False},
                                {"name":'Proposer :', "value":str(f'[{self.tx["args"]["proposer"]}](https://etherscan.io/address/{self.tx["args"]["proposer"]})'), "inline": False},
                                #{"name":'Targets :', "value":str({self.tx["args"]["targets"]}), "inline": False},
                                #{"name":'Values :', "value":str({self.tx["args"]["values"]}), "inline": False},
                                {"name":'Description :', "value":str(f'{self.tx["args"]["description"][0:400]}...'), "inline": False},
                                {"name":'Transaction :', "value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]

                        color = colors.dark_green
                        send = True

                    elif (self.event_name in ["ProposalCanceled"]):
                        title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(self.tx["event"]))
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Proposal :',"value":"https://www.inverse.finance/governance/proposals/mills/" + str(self.tx["args"]["id"]),"inline":False},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        color = colors.dark_red
                        send = True

                    elif (self.event_name in ["ProposalQueued"]):
                        title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",str(self.tx["event"]))
                        fields = [{"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'), "inline": False},
                                  {"name": 'Proposal :',"value": "https://www.inverse.finance/governance/proposals/mills/" + str(self.tx["args"]["id"]), "inline": False},
                                  {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]

                        color = colors.blurple
                        send = True

                    elif (self.event_name in ["ProposalExecuted"]):
                        title = "Governor Mills : New " + re.sub(r"(\w)([A-Z])", r"\1 \2",str(self.tx["event"]))
                        fields = [{"name": 'Block Number :', "value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'), "inline": False},
                                  {"name": 'Proposal :',"value": "https://www.inverse.finance/governance/proposals/mills/" + str( self.tx["args"]["id"]), "inline": False},
                                  {"name": 'Transaction :',"value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'), "inline": False}]
                        color = colors.dark_green
                        send = True

                elif (self.alert == "fed"):
                    webhook = os.getenv('WEBHOOK_FED')
                    image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/22517/1128427/3084f915-b906-4fdf-ac8c-ad5c0ce57e2b.jpg"

                    if (self.event_name in ["Expansion"]):
                        title = "Fed " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(self.tx["event"])) + " event detected"
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Fed Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'Amount :',"value": str(formatCurrency(self.tx["args"]["amount"] / 1e18)),"inline":True},
                        {"name":'Total Supply :',"value":str(formatCurrency(fetchers.getSupply(self.web3,'0x865377367054516e17014ccded1e7d814edc9ce4') / 1e18)),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        color = colors.dark_red
                        send = True
                    if (self.event_name in ["Contraction"]):
                        title = "Fed " + re.sub(r"(\w)([A-Z])", r"\1 \2", str(self.tx["event"])) + " event detected"
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Fed Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'Amount :',"value": str(formatCurrency(self.tx["args"]["amount"] / 1e18)),"inline":True},
                        {"name":'Total Supply :',"value":str(formatCurrency(fetchers.getSupply(self.web3,'0x865377367054516e17014ccded1e7d814edc9ce4') / 1e18)),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                        color = colors.dark_green
                        send = True

                elif (self.alert == "swap"):
                    webhook = os.getenv('WEBHOOK_SWAP')
                    if (self.event_name == "Swap"):
                        image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/838610/1466237/8e64e858-5db5-4692-922d-5f9fe6b7a8c6.jpg"
                        if self.tx["args"]['amount0In'] == 0:
                            operation = 'Buy ' + str(formatCurrency(self.tx["args"]['amount0Out'] / fetchers.getDecimals(self.web3,
                                fetchers.getSushiTokens(self.web3,address)[0]))) + " " + str(
                                fetchers.getSushiTokensSymbol(self.web3,address)[0])
                            color = colors.dark_green
                            title = "Sushiswap New Buy event detected"
                            send = True
                        else:
                            operation = 'Sell ' + str(formatCurrency(self.tx["args"]['amount0In'] / fetchers.getDecimals(self.web3,
                                fetchers.getSushiTokens(self.web3,address)[0]))) + " " + str(
                                fetchers.getSushiTokensSymbol(self.web3,address)[0])
                            color = colors.dark_red
                            title = "Sushiswap New Sell event detected"
                            send = True

                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":True},
                        {"name":'Name :',"value":str(fetchers.getName(self.web3,address)),"inline":True},
                        {"name":'Symbol :',"value":str(fetchers.getSymbol(self.web3,address)),"inline":True},
                        {"name":'Operation :',"value":str(operation),"inline":True},
                        {"name":'USD value :',"value":str(formatCurrency(((self.tx["args"]["amount0Out"] + self.tx["args"]["amount0In"]) / fetchers.getDecimals(self.web3,fetchers.getSushiTokens(self.web3,address)[0])) * fetchers.getUnderlyingPrice(self.web3,'0x1637e4e9941d55703a7a5e7807d6ada3f7dcd61b'))),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]
                    elif (self.event_name in ["Mint"]):
                        title = "Sushi New Liquidity Add event detected"
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'Name :',"value":str(fetchers.getName(self.web3,address)),"inline":True},
                        {"name":'Symbol :',"value":str(fetchers.getSymbol(self.web3,address)),"inline":True},
                        {"name":'amountAMin :',"value":str(self.tx["args"]["amount0"] / 1e18),"inline":False},
                        {"name":'amountBMin :',"value":str(self.tx["args"]["amount1"] / 1e18),"inline":True},
                        {"name":'Token 0 :',"value":str(fetchers.getBalance(self.web3,address, fetchers.getSushiTokens(self.web3,address[0]))),"inline":False},
                        {"name":'Token 1 :',"value":str(fetchers.getBalance(self.web3,address, fetchers.getSushiTokens(self.web3,address[1]))),"inline":True},
                        {"name":'Total Supply :',"value":str(fetchers.getSupply(self.web3,address)),"inline":False},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]


                        color = colors.dark_green
                        send = True
                    elif (self.event_name in ["Burn"]):
                        title = "Sushi New Liquidity Removal detected"

                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":True},
                        {"name":'Name :',"value":str(fetchers.getName(self.web3,address)) ,"inline":True},
                        {"name":'Symbol :',"value":str(fetchers.getSymbol(self.web3,address)),"inline":False},
                        {"name":'Amount 0 :',"value":str(self.tx["args"]["amount0"] / 1e18),"inline":True},
                        {"name":'Amount 1 :',"value":str(self.tx["args"]["amount1"] / 1e18),"inline":True},
                        {"name":'Total Reserves 0 :',"value":str(fetchers.getBalance(self.web3,address, fetchers.getSushiTokens(self.web3,address[0]))),"inline":True},
                        {"name":'Total Reserves 1 :',"value":str(fetchers.getBalance(self.web3,address, fetchers.getSushiTokens(self.web3,address[1]))),"inline":True},
                        {"name":'Total Supply :',"value":str(fetchers.getSupply(self.web3,address)),"inline":True},
                        {"name": 'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]
                        color = colors.dark_red
                        send = True

                elif (self.alert == "unitroller"):

                    webhook = os.getenv('WEBHOOK_UNITROLLER')
                    if (self.event_name in ["NewBorrowCap",
                                            "NewSupplyCap",
                                            "NewCollateralFactor",
                                            "NewPriceOracle",
                                            "MarketListed",
                                            "MarketUnlisted"]):
                        title = "Comptroller Markets " + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                                str(self.tx["event"])) + " event detected"
                        content = '<@&945071604642222110>'
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Address :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]

                    color = colors.dark_orange
                    send = True

                elif (self.alert == "concave"):

                    webhook = os.getenv('WEBHOOK_CONCAVE')
                    watch_addresses = ["0x6fF51547f69d05d83a7732429cfe4ea1E3299E10","0x226e7AF139a0F34c6771DeB252F9988876ac1Ced"]

                    self.tx = fixFromToValue(self.tx)

                    from_address = self.tx["args"]["from"]
                    to_address = self.tx["args"]["to"]
                    value = self.tx["args"]["value"]

                    if self.event_name in ["Transfer"]:

                        title = "Concave DOLA/3CRV activity detected"
                        #content = '<@&945071604642222110>'
                        fields = [{"name": 'Block Number :',"value": str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline": False},
                                  {"name": 'Transfer :', "value": str(formatCurrency(value / fetchers.getDecimals(self.web3, address))) + ' ' + str(fetchers.getSymbol(self.web3, address)), "inline": False},
                                  {"name": 'From :',"value": str(f'[{from_address}](https://etherscan.io/address/{from_address})'),"inline": False},
                                  {"name": 'To :',"value": str(f'[{to_address}](https://etherscan.io/address/{to_address})'),"inline": False},
                                  {"name": 'Transaction :', "value": str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline": False}]
                        color = colors.dark_orange
                        send = True

                elif (self.alert == "transf_usdc"):
                    webhook = os.getenv('WEBHOOK_FRAXUSDC')
                    from_address = self.tx["args"]["from"]
                    to_address = self.tx["args"]["to"]
                    value = self.tx["args"]["value"]/1e6

                    usdc_balance = fetchers.getBalance(self.web3,"0xDcEF968d416a41Cdac0ED8702fAC8128A64241A2","0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
                    ratio = float(value) / float(usdc_balance)
                    print('Ratio is '+str(ratio))
                    if ratio > 0.005 :
                        title = "fraxUSDC High activity detected"
                        content = '<@&945071604642222110>'
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'From :',"value":str(f'[{from_address}](https://etherscan.io/address/{from_address})'),"inline":False},
                        {"name":'To :',"value":str(f'[{to_address}](https://etherscan.io/address/{to_address})'),"inline":False},
                        {"name":'Value :',"value":str(formatCurrency(value)),"inline":False},
                        {"name":'USDC Balance :',"value":str(formatCurrency(usdc_balance)),"inline":False},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]
                        color = colors.dark_orange
                        send = True

                elif (self.alert == "profits"):
                    webhook = os.getenv('WEBHOOK_DOLA3CRV')

                    self.tx = fixFromToValue(self.tx)
                    from_address = self.tx["args"]["from"]
                    to_address = self.tx["args"]["to"]
                    value = self.tx["args"]["value"]

                    feds = ["0xcc180262347F84544c3a4854b87C34117ACADf94",
                            "0x7eC0D931AFFBa01b77711C2cD07c76B970795CDd",  # stabilizer
                            "0xC564EE9f21Ed8A2d8E7e76c085740d5e4c5FaFbE",  # fantom bridge
                            "0x7765996dAe0Cf3eCb0E74c016fcdFf3F055A5Ad8",
                            "0x5Fa92501106d7E4e8b4eF3c4d08112b6f306194C",
                            "0xe3277f1102C1ca248aD859407Ca0cBF128DB0664",
                            "0x5E075E40D01c82B6Bf0B0ecdb4Eb1D6984357EF7",
                            "0x9060A61994F700632D16D6d2938CA3C7a1D344Cb",
                            "0xCBF33D02f4990BaBcba1974F1A5A8Aea21080E36",
                            "0x4d7928e993125A9Cefe7ffa9aB637653654222E2",
                            "0x57D59a73CDC15fe717D2f1D433290197732659E2"]


                    if (self.event_name in ["Transfer"] and (from_address in feds and to_address=='0x926dF14a23BE491164dCF93f4c468A50ef659D5B')):
                        title = "Profit Taking detected"
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Profit :',"value":str(formatCurrency(value/fetchers.getDecimals(self.web3,address)))+' '+str(fetchers.getSymbol(self.web3,address)),"inline":False},
                        {"name":'From :',"value":str(f'[{from_address}](https://etherscan.io/address/{from_address})'),"inline":False},
                        {"name":'To :',"value":str(f'[{to_address}](https://etherscan.io/address/{to_address})'),"inline":False},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]
                        content = '<@&945071604642222110>'
                        color = colors.dark_orange
                        send = True

                elif (self.alert == "harvest"):
                    webhook = os.getenv('WEBHOOK_DOLA3CRV')
                    pool_address = "0xAA5A67c256e27A5d80712c51971408db3370927D"
                    token_0 = 'DOLA'
                    token_1 = '3CRV'
                    token_0_address = '0x865377367054516e17014CcdED1e7d814EDC9ce4'
                    token_1_address = '0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490'
                    token_0_total = fetchers.getBalance(self.web3, pool_address, token_0_address)
                    token_1_total = fetchers.getBalance(self.web3, pool_address, token_1_address)

                    if (self.event_name in ["Harvested"]):
                        title = "Yearn Harvest detected"
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name": 'Pool Address :', "value": str(f'[{pool_address}](https://etherscan.io/address/{pool_address})'), "inline": False},
                        {"name": 'Strategy Address :', "value": str(f'[{address}](https://etherscan.io/address/{address})'), "inline": False},
                        {"name":'Total Profit :',"value": str(formatCurrency(self.tx["args"]["profit"]/1e18)) ,"inline":True},
                        {"name":'Inverse Profit :',"value": str(formatCurrency(self.tx["args"]["profit"]*0.2/1e18)) ,"inline":True},
                        {"name":'Yearn Profit :',"value": str(formatCurrency(self.tx["args"]["profit"]*0.8/1e18)) ,"inline":True},
                        {"name":'Loss :',"value": str(formatCurrency(self.tx["args"]["loss"]/1e18)) ,"inline":True},
                        {"name":'Debt Payment :',"value": str(formatCurrency(self.tx["args"]["debtPayment"]/1e18)) ,"inline":True},
                        {"name":'Debt Outstanding :',"value": str(formatCurrency(self.tx["args"]["debtOutstanding"]/1e18)) ,"inline":True},
                        {"name":token_0+' in Pool :',"value":str(formatCurrency(token_0_total)),"inline":True},
                        {"name":token_1+' in Pool :',"value":str(formatCurrency(token_1_total)),"inline":True},
                        {"name":token_0+'+'+token_1+' in Pool',"value":str(formatCurrency(token_0_total + token_1_total)),"inline":False},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]
                        content = '<@&945071604642222110>'
                        image = 'https://dune.com/api/screenshot?url=https://dune.com/embeds/1382819/2351787/0e47fbff-397e-43b5-94f3-a4e40067dffa.jpg'
                        color = colors.dark_green
                        send = True

                elif (self.alert == "debt_repayment"):
                    webhook = os.getenv('WEBHOOK_DEBTREPAYMENT')
                    image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/1291754/2213835/4c5b629f-a6b0-4575-98a1-9d5fae4fab33"
                    if (self.event_name in ["debtRepayment"]):
                        title = "Debt Repayment detected"

                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Token Repaid :',"value":str(fetchers.getSymbol(self.web3,self.tx["args"]["underlying"])),"inline":True},
                        {"name":'Amount Received :',"value":str(formatCurrency(self.tx["args"]["receiveAmount"]/fetchers.getDecimals(self.web3,self.tx["args"]["underlying"]))),"inline":True},
                        {"name":'Amount Paid :',"value":str(formatCurrency(self.tx["args"]["paidAmount"]/fetchers.getDecimals(self.web3,self.tx["args"]["underlying"]))),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False},
                        {"name":'Debt Repayment Contract :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False}]
                        color = colors.dark_orange

                        send = True

                elif (self.alert == "debt_conversion"):
                    webhook = os.getenv('WEBHOOK_DEBTREPAYMENT')
                    image = "https://dune.com/api/screenshot?url=https://dune.com/embeds/1291809/2213790/9e5c3845-66c0-496f-b42a-49a2fbd20df9.jpg"



                    if (self.event_name in ["Conversion"]):
                        title = "Debt Conversion  detected"
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'User :',"value":str(f'[{self.tx["args"]["user"]}](https://etherscan.io/address/{self.tx["args"]["user"]})'),"inline":True},
                        {"name":'Token Repaid :',"value":str(fetchers.getSymbol(self.web3,self.tx["args"]["anToken"])),"inline":True},
                        {"name": 'DOLA Amount :',"value":str(formatCurrency(self.tx["args"]["dolaAmount"] / 1e18)),"inline":True},
                        {"name":'Underlying Amount :',"value":str(formatCurrency(self.tx["args"]["underlyingAmount"] / fetchers.getDecimals(self.web3,self.tx["args"]["anToken"]))),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False},
                        {"name":'Debt Conversion Contract :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False}]
                        color = colors.dark_orange
                        send = True
                    elif (self.event_name in ["Redemption"]):
                        title = "Debt Conversion  detected - Redemption"
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'User :',"value":str(f'[{self.tx["args"]["user"]}](https://etherscan.io/address/{self.tx["args"]["user"]})'),"inline":True},
                        {"name": 'DOLA Amount :',"value":str(formatCurrency(self.tx["args"]["dolaAmount"] / 1e18)),"inline":True},
                        {"name":'Debt Conversion Contract :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]
                        color = colors.dark_orange
                        send = True
                    elif (self.event_name in ["Repayment"]):
                        title = "Debt Conversion  detected - Repayment"
                        fields = [{"name":'Block Number :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":False},
                        {"name":'Debt Conversion Contract :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":False},
                        {"name": 'DOLA Amount :',"value":str(formatCurrency(self.tx["args"]["dolaAmount"] / 1e18)),"inline":True},
                        {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":False}]
                        color = colors.dark_orange
                        send = True

                if send:
                    sendWebhook(webhook, title, fields, content, image, color)

            except Exception as e:
                logging.warning(f'Error in event handler {str(self.alert)}-{str(self.contract.address)}-{str(self.event_name)}')
                logging.error(e)
                sendError(f'Error in event handler {str(self.alert)}-{str(self.contract.address)}-{str(self.event_name)}')
                sendError(e)
                continue
            break

# Define state change to handle and logs to the console/send to discord
class HandleStateVariation(Thread):
    def __init__(self, web3,old_value,value, change, alert, contract, state_function, state_argument, **kwargs):
        super(HandleStateVariation, self).__init__(**kwargs)
        self.web3 = web3
        self.value = value
        self.change = change
        self.contract = contract
        self.alert = alert
        self.state_function = state_function
        self.state_argument = state_argument
        self.old_value = old_value

    def run(self):
        try:

            send = False
            image = ''
            content = ''
            webhook = ''
            title = ''
            fields = []
            color = colors.blurple
            level = 0

            if (self.alert == 'oracle'):
                webhook = os.getenv('WEBHOOK_MARKETS')
                if self.state_function == 'getUnderlyingPrice':
                    logging.info(str(self.change) + '% change detected on ' + str(
                        fetchers.getSymbol(self.web3,fetchers.getUnderlying(self.web3,self.state_argument))))
                    title = str(formatPercent(self.change)) + ' change detected on ' + str(
                        fetchers.getSymbol(self.web3,fetchers.getUnderlying(self.web3,self.state_argument))) + ' Oracle'

                    if abs(self.change) > 0.2:
                        content = '<@&945071604642222110>'
                        level = 3
                        color = colors.red
                        send = True
                    elif abs(self.change) > 0.1:
                        level = 2
                        color = colors.dark_orange
                        send = True
                    elif abs(self.change) > 0.05:
                        level = 1
                        color = colors.orange
                        send = True
                    if send:
                        fields = [{"name": 'Alert Level :',"value": str(level),"inline": True},
                                  {"name": 'Variation :', "value": str(formatPercent(self.change)),"inline": True},
                                  {"name": 'Old Value :', "value": str(formatCurrency(self.old_value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.state_argument)))), "inline": True},
                                  {"name": 'New Value :', "value": str(formatCurrency(self.value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.state_argument)))), "inline": True},
                                  {"name": 'Link to Market :', "value": 'https://etherscan.io/address/' + str(self.state_argument), "inline": False}]

            if (self.alert == 'cash'):
                webhook = os.getenv('WEBHOOK_MARKETS')
                if self.state_function == 'getCash':
                    logging.info(str(self.change) + '% change detected on ' + str(
                        fetchers.getName(self.web3,self.contract.address)) + ' balance')
                    title = str(formatPercent(self.change)) + ' change detected on ' + str(
                        fetchers.getSymbol(self.web3,fetchers.getUnderlying(self.web3,self.contract.address))) + ' Cash balance'

                    if abs(self.change) > 0.2:
                        content = '<@&945071604642222110>'
                        level = 3
                        color = colors.red
                        send = True
                    elif abs(self.change) > 0.1:
                        level = 2
                        color = colors.dark_orange
                        send = True
                    elif abs(self.change) > 0.05:
                        level = 1
                        color = colors.orange
                        send = True

                    if send:
                        fields = [{"name": 'Alert Level :',"value": str(level),"inline": True},
                                  {"name": 'Variation :',"value": str(formatPercent(self.change)), "inline" : True},
                                  {"name": 'Old Value :',"value": str(formatCurrency(self.old_value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.contract.address)))), "inline" : True},
                                  {"name": 'New Value :',"value": str(formatCurrency(self.value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.contract.address)))), "inline" : True},
                                  {"name": 'Link to Market :',"value":'https://etherscan.io/address/' + str(self.contract.address), "inline" : False}]

            if (self.alert == 'supply'):
                webhook = os.getenv('WEBHOOK_DOLA3CRV')
                if self.state_function == 'totalSupply':
                    logging.info(str(self.change) + '% change detected on ' + str(
                        fetchers.getName(self.web3,self.contract.address))+ ' total supply')
                    title = str(formatPercent(self.change)) + ' change detected on ' + str(
                        fetchers.getSymbol(self.web3,fetchers.getUnderlying(self.web3,self.state_argument))) + ' Supply'

                    if abs(self.change) > 0.015:
                        content = '<@&945071604642222110>'
                        level = 3
                        color = colors.red
                        send = True
                    elif abs(self.change) > 0.01:
                        level = 2
                        color = colors.dark_orange
                        send = True
                    elif abs(self.change) > 0.005:
                        level = 1
                        color = colors.orange
                        send = True
                    if send:
                        fields = [{"name":'Alert Level :',"value":str(level),"inline": True},
                        {"name":'Variation :', "value":str(formatPercent(self.change)), "inline": True},
                        {"name":'Old Value :', "value":str(formatCurrency(self.old_value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.contract.address)))), "inline": True},
                        {"name":'New Value :', "value":str(formatCurrency(self.value / fetchers.getDecimals(self.web3,fetchers.getUnderlying(self.web3,self.contract.address)))), "inline": True},
                        {"name":'Link to Pool :', "value":'https://etherscan.io/address/' + str(self.contract.address), "inline": False}]

            if (self.alert == 'liquidation_incentive'):
                webhook = os.getenv('WEBHOOK_MARKETS')
                if self.state_function == 'liquidationIncentiveMantissa':
                    logging.info(str(self.change) + '% change detected on ' +
                                 str(fetchers.getName(self.web3,self.contract.address))+ ' Liquidation incentive')
                    title = str(formatPercent(self.change)) + ' change detected on ' +\
                            str(fetchers.getSymbol(self.web3,fetchers.getUnderlying(self.web3,self.state_argument))) + ' Liquidation incentive'

                    fields = [{"name": 'Alert Level :',"value": str(level),"inline": True},
                    {"name": 'Variation :',"value": str(formatPercent(self.change)),"inline": True},
                    {"name": 'Old Value :',"value": str(formatCurrency(self.old_value / 1e18)),"inline": True},
                    {"name": 'New Value :',"value":str(formatCurrency(self.value / 1e18)),"inline": True},
                    {"name": 'Link to Pool :',"value":'https://etherscan.io/address/' + str(self.contract.address),"inline": False}]

                    content = '<@&945071604642222110>'
                    level = 3
                    color = colors.red
                    send = True

            if send:
                sendWebhook(webhook, title, fields, content, image, color)


        except Exception as e:
            logging.warning(f'Error in state variation handler {str(self.alert)}-{str(self.contract.address)}-{str(self.state_function)}-{str(self.state_argument)}')
            logging.error(e)
            sendError(f'Error in state variation handler {str(self.alert)}-{str(self.contract.address)}-{str(self.state_function)}-{str(self.state_argument)}')
            sendError(e)
            pass

# Define state change to handle and logs to the console/send to discord
class HandleTx(Thread):
    def __init__(self,web3, tx, alert, contract, name, **kwargs):
        super(HandleTx, self).__init__(**kwargs)
        self.web3 = web3
        self.contract = contract
        self.alert = alert
        self.name = name
        self.tx = tx

    def run(self):
        try:
            self.tx = json.loads(Web3.toJSON(self.tx))
            # logs result table and start writing message
            logging.info(str(self.tx))

            send = False
            image = ''
            content = ''
            webhook = ''
            title = ''
            fields = []
            color = colors.blurple

            address = self.tx["address"]
            blockNumber = self.tx["blockNumber"]
            transactionHash = self.tx["transactionHash"]
            
            if (self.alert == 'multisig' and self.web3.eth.chainId==1):
                webhook = os.getenv('WEBHOOK_GOVERNANCE')

                logging.info(str('Tx detected on ' + str(address)))
                title = str('Tx detected on ' + str(self.name))
                
                send = True
                fields = [{"name":'Multisig :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":True},
                {"name":'Transaction :',"value":str(f'[{transactionHash}](https://etherscan.io/tx/{transactionHash})'),"inline":True},
                {"name":'Block :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":True},
                {"name":'Transaction Log :',"value":str(self.tx),"inline":False}]
            if (self.alert == 'multisig' and self.web3.eth.chainId==10):
                webhook = os.getenv('WEBHOOK_GOVERNANCE')

                logging.info(str('Tx detected on ' + str(address)))
                title = str('Tx detected on ' + str(self.name))

                send = True
                fields = [{"name":'Multisig :',"value":str(f'[{address}](https://etherscan.io/address/{address})'),"inline":True},
                {"name":'Transaction :',"value":str(f'[{transactionHash}](https://optimistic.etherscan.io/tx/{transactionHash})'),"inline":True},
                {"name":'Block :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":True},
                {"name":'Transaction Log :',"value":str(self.tx),"inline":False}]
            if (self.alert == 'multisig' and self.web3.eth.chainId==250):
                webhook = os.getenv('WEBHOOK_GOVERNANCE')

                logging.info(str('Tx detected on ' + str(address)))
                title = str('Tx detected on ' + str(self.name))

                send = True
                fields = [{"name":'Multisig :',"value":str(f'[{address}](https://ftmscan.io/address/{address})'),"inline":True},
                {"name":'Transaction :',"value":str(f'[{transactionHash}](https://ftmscan.io/tx/{transactionHash})'),"inline":True},
                {"name":'Block :',"value":str(f'[{blockNumber}](https://etherscan.io/block/{blockNumber})'),"inline":True},
                {"name":'Transaction Log :',"value":str(self.tx),"inline":False}]

            if send:
                sendWebhook(webhook, title, fields, content, image, color)
        except Exception as e:
            logging.warning(f'Error in tx handler {str(self.alert)}-{str(self.contract.address)}-{str(self.name)}')
            logging.error(e)
            sendError(f'Error in tx handler {str(self.alert)}-{str(self.contract.address)}-{str(self.name)}')
            sendError(e)
            pass

# Listen to coingecko  price changes every 60 seconds
class HandleCoingecko(Thread):
    def __init__(self, id, old_value,value, change,  **kwargs):
        super(HandleCoingecko, self).__init__(**kwargs)
        self.value = value
        self.id = id
        self.old_value = old_value
        self.change = change


    def run(self):
        try:
            if abs(self.change) > 0:
                send = False
                image = ''
                content=''
                title = ''
                fields = []
                color = colors.blurple
                webhook = os.getenv('WEBHOOK_MARKETS')
                logging.info(str(formatPercent(self.change)) + ' change detected on Coingecko '+str(self.id)+' Price')
                title = str(formatPercent(self.change)) + ' change detected on Coingecko '+str(self.id)+' Price'

                if abs(self.change) > 0.2:
                    content = '<@&945071604642222110>'
                    level = 3
                    color = colors.red
                    send = True
                elif abs(self.change) > 0.1:
                    level = 2
                    color = colors.dark_orange
                    send = True
                elif abs(self.change) > 0.05:
                    level = 1
                    color = colors.orange
                    send = True

                if send:
                    fields = [{"name":'Alert Level :',"value":str(level),"inline":False},
                    {"name":'Variation :',"value":str(formatPercent(self.change)),"inline":True},
                    {"name":'Old Value :',"value":str(formatCurrency(self.old_value)),"inline":True},
                    {"name":'New Value :',"value":str(formatCurrency(self.value)),"inline":True},
                    {"name":'Link to Market :',"value": 'https://www.coingecko.com/en/coins/'+self.id,"inline":False}]
                    sendWebhook(webhook, title, fields, content, image, color)

        except Exception as e:
            logging.warning(f'Error in coingecko variation handler')
            logging.error(e)
            sendError(f'Error in coingecko variation handler')
            sendError(e)
            pass

# Listen to coingecko  price changes every 60 seconds
class HandleCoingeckoVolume(Thread):
    def __init__(self, id, old_value,value, change,  **kwargs):
        super(HandleCoingeckoVolume, self).__init__(**kwargs)
        self.value = value
        self.id = id
        self.old_value = old_value
        self.change = change
        self.diff = abs(value - old_value)


    def run(self):
        try:
            if abs(self.change) > 0:
                send = False
                image = ''
                content=''
                title = ''
                fields = []
                color = colors.blurple
                webhook = os.getenv('WEBHOOK_MARKETS')
                logging.info(str(formatPercent(self.change)) + ' change detected on Coingecko '+str(self.id)+' 24H volume')
                title = str(formatPercent(self.change)) + ' change detected on Coingecko '+str(self.id)+'  24H volume'

                if abs(self.change) > 0.9:
                    #content = '<@&945071604642222110>'
                    level = 3
                    color = colors.red
                    send = True
                elif abs(self.change) > 0.8:
                    level = 2
                    color = colors.dark_orange
                    send = True
                elif abs(self.change) > 0.7:
                    level = 1
                    color = colors.orange
                    send = True

                if send and (self.diff > 500000):
                    fields = [{"name": 'Alert Level :', "value": str(level), "inline": False},
                              {"name": 'Variation :', "value": str(formatPercent(self.change)), "inline": True},
                              {"name": 'Old Value :', "value": str(formatCurrency(self.old_value)), "inline": True},
                              {"name": 'New Value :', "value": str(formatCurrency(self.value)), "inline": True},
                              {"name": 'Link to Market :',"value": 'https://www.coingecko.com/en/coins/'+self.id, "inline": False}]

                    sendWebhook(webhook, title, fields, content, image, color)

        except Exception as e:
            logging.warning(f'Error in coingecko volume variation handler')
            logging.error(e)
            sendError(f'Error in coingecko volume variation handler')
            sendError(e)
            pass
