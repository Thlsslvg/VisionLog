@echo off
cd /d "%~dp0"

start "VLog Watchdog" cmd /k "..\.venv\Scripts\python.exe main.py"

timeout /t 3 > nul

start "VLog Dashboard" cmd /k "..\.venv\Scripts\streamlit.exe run dashboard\App.py"

timeout /t 5 > nul

start http://localhost:8501 