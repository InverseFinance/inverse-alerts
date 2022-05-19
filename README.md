# inverse-alerts

This repository is a Python Smart contract alerting system, allowing to send to discord events depending on certain conditions based on Ethereum Transactions or state variables. This was originally implemented for Inverse Finance Market monitoring and Risk Management purposes.

### Ethereum Endpoint
This script is based on a very high API query rate. Therefore we recommend listening to events by running a private node with geth. Filters are now supported on light nodes so you don't have to index a full archive node before being able to start. Just install get and start your node using :

`geth --syncmode light --http --http.addr 0.0.0.0`

### Contract.xslx

