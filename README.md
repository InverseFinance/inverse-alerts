# Inverse Python Alerts

This repository is a Python Smart contract alerting system, allowing to send to discord events depending on certain conditions 
based on Ethereum Transactions or state variables. 
This was originally implemented for Inverse Finance Market monitoring and Risk Management purposes.

The version in prod is running on a Remote Server running a light node.

### Ethereum Endpoint
This script is continuous. Hence we recommend listening to events by running a private node with geth. 
Filters being now supported on light nodes, you don't have to index a full archive node before being able to start. 
Just install Geth and start a light node using :

`geth --syncmode light --http --http.addr 0.0.0.0`


### Getting Rid of Async functions and using thread
The use of async functions is generally recommended for Nodes were the user have to pay to access the data or were 
the query rate is strongly limited.
However it generates challenges in term of parrallel processing and CPU optimisation in the case you are running a high number of Listeners.

This python script is instead continuously monitoring the events, inside separate threads, allowing the CPU to 
jump from one thread to the other and maintaining a sustainable CPU load over all processes.


### Contract.xlsx
This file is used to update the contract, events and return result triggered by the alert. 
It is to be amended carefully since the smallest typo will generate errors.