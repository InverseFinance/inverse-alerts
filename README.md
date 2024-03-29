# Inverse Python Alerts

This repository is a Python Smart contract alerting system, allowing to send to discord events depending on certain
conditions based on Ethereum Transactions or state variables.
This was originally implemented for Inverse Finance Market monitoring and Risk Management purposes.

The version in prod is running on a Remote Server ( previously running an Ethereum light node).

### Ethereum Endpoint

Running on a light node before the merge, this possibility is unfortunately not available anymore for the time being. 
Therefore we have switched our local node infrastructure to a provider and improved querying rates.

### Install requirements

Make sure you're running the latest release of Python (3.10) and that Python is allowed through your Firewall (necessary
to be able to send requests to webhook) :

`pip install -r requirements.txt`

### Configure your *.env

Fill in your node RPC, and webhooks for alerts and error deliveries. Make sure they are included in `handler.py`

```
LOCALHOST = "http://localhost:8545"

WEBHOOK_TESTING = "[enter a Discord webhook for testing]"
WEBHOOK_ERRORS = "[enter a Discord webhook for errors]"

WEBHOOK_DOLA3CRV = "[enter a Discord webhook dola3crv alerts] "
WEBHOOK_FED = "[enter a Discord webhook fed alerts]"
WEBHOOK_GOVERNANCE = "[enter a Discord webhook governance alerts]"
WEBHOOK_LENDING = "[enter a Discord webhook lending alerts]"
WEBHOOK_LIQUIDATIONS = "[enter a Discord webhook liquidations alerts]"
WEBHOOK_MARKETS = "[enter a Discord webhook markets alerts]"
WEBHOOK_SWAP = "[enter a Discord webhook swap alerts]"
WEBHOOK_UNITROLLER = "[enter a Discord webhook unitroller alerts]"
```

### Run with Python

Execute main.py in your Python env or venv :

`[Path to your project]/venv/Scripts/python.exe main.py`

Alternatively you can use the CMD batch files available. You can use `run` to run the script alone.
Make sure you are running Python in the proper environment.

### Listeners

This script is using 3 types of listeners `listeners.py` and can listening to 3 types of Ethereum mainnet occurences :

- Smart contract events : `EventListener`
- Smart contract View State functions variations : `StateChangeListener`
- Transactions emitted from an address : `TxListener`

Those listeners are using events handlers `handlers.py` to define the conditions for  sending a message format and 
dispatch this latter to the appropriate webhook.

### Adding an alert

To add an alert head to `contract.py` and `alert.py`. Those files are used to update the contract, events and return result triggered by
the different alerts.
It is to be amended carefully since the smallest typo will generate errors.

1. Enter the contract you want to listen to on sheet 'contracts', and paste its unformatted ABI, or the one you are
   going to use (might be different from the contract ABI in the case of proxies).
2. Enter an alert name in the appropriate column depending on the alert type.
3. Define the alert type you are going to use :
    - for Smart contract events go to `alerts_events` sheet and add the alert name and the events you want to listen
      to (case-sensitive).
    - for State functions variation go to `alerts_state`, add the alert name and the state functions you want to monitor
    - for Transactions go to `alerts_tx`, add the alert name (it is not necessary to add the addresses again since they
      should be filled on the sheet `contracts`)
4. If you are using State function alerts with arguments, carefully amend `main.py` to allow the script to loop
   correctly through the function arguments.
   In the case of this script we have two State functions alerts, one with parameters, the other not, so we switch the
   arguments with :

```
if alert == 'oracle':
   # Get an array of all markets to use in the Oracle calling
   state_arguments = fetchers.getAllMarkets('0x4dcf7407ae5c07f8681e1659f626e114a7667339')
elif alert == 'cash':
   state_arguments = None
```

5. Finally, we need to amend the file `handler.py` to send formatted messages with the corresponding information to our
   webhooks.
   This is using `fetchers.py` a small homemade library allowing to fetch directly view & state functions on Ethereum.
   Discord handlers are very sensitive to formatting so make sure you are passing the results of your calculations into
   your  message as strings and that you are defining a handler condition for every case you need to (Address and function) :

```
if (self.alert == 'cash'):
    webhook = os.getenv('WEBHOOK_MARKETS')
    if self.state_function == 'cash':
    ...and so on
```
   