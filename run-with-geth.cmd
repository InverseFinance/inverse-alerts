@echo off
:Start
start "" geth --syncmode light --http --http.addr 0.0.0.0
:: Wait 120 seconds for geth to connect and launch sync
TIMEOUT /T 120
C:/Users/naoufel/inverse-alerts/venv/Scripts/python.exe main.py
:: Wait 5 seconds before restarting.
TIMEOUT /T 5
GOTO:Start