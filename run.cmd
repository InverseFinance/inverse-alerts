@echo off
:Start
setlocal
cd /d %~dp0
python.exe main.py
:: Wait 5 seconds before restarting.
TIMEOUT /T 5
GOTO:Start