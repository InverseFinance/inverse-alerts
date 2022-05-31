@echo off
:Start
geth --syncmode light --http --http.addr 0.0.0.0
:: Wait 30 seconds before restarting.
TIMEOUT /T 30
GOTO:Start