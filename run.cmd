@echo off
:Start
setlocal
cd /d %~dp0
python main.py
:: Wait 5 seconds before restarting.
TIMEOUT /T 5
GOTO:Start