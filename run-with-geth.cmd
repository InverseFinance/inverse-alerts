@echo off
:Start
start "" geth --syncmode light --http --http.addr 0.0.0.0
:: Wait 60 seconds for geth to connect and launch sync before initiating alert to avoid timeout error
TIMEOUT /T 60
setlocal
:: Set local folder
cd /d %~dp0
python main.py
:: Wait 5 seconds before restarting in case of timeout
TIMEOUT /T 5
GOTO:Start