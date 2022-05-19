@echo off
:Start
C:/Users/naoufel/inverse-alerts/venv/Scripts/python.exe main.py
:: Wait 5 seconds before restarting.
TIMEOUT /T 5
GOTO:Start