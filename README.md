# Inverse Python Alerts

This repository is a Python Smart contract alerting system, allowing to send to discord events depending on certain conditions based on Ethereum Transactions or state variables.

This was originally implemented for Inverse Finance Market monitoring and Risk Management purposes.

### Ethereum Endpoint
This script is continuous. Hence we recommend listening to events by running a private node with geth. 

Filters are now supported on light nodes so you don't have to index a full archive node before being able to start. Just install Geth and start a light node using :

`geth --syncmode light --http --http.addr 0.0.0.0`

### Contract.xlsx
This file is used to update the contract, events and return result triggered by the alert. It is to be amended carefully since the smallest typo will generate errors.
