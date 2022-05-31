@echo off
:Start
start "" geth --syncmode light --http --http.addr 0.0.0.0
:: Wait 120 seconds for geth to connect and launch sync
TIMEOUT /T 60
setlocal
cd /d %~dp0
venv\Scripts\python.exe main.py
:: Wait 5 seconds before restarting in case of timeout
TIMEOUT /T 5
GOTO:Start