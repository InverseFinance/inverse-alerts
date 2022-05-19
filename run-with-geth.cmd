@echo off
:Start
start "" geth --syncmode light --http --http.addr 0.0.0.0
C:/Users/naoufel/inverse-alerts/venv/Scripts/python.exe main.py
:: Wait 5 seconds before restarting.
TIMEOUT /T 5
GOTO:Start