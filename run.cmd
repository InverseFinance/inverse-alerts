@echo off
:Start
setlocal
cd /d %~dp0
venv\Scripts\python.exe main.py
:: Wait 5 seconds before restarting.
TIMEOUT /T 5
GOTO:Start