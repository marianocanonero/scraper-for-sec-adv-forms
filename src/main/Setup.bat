@echo off
python -m venv src\main\venv
CALL src\main\venv\Scripts\activate.bat
ECHO Installing required dependencies...
pip install --require-virtualenv -r src/main/requirements.txt
ECHO Required dependencies installed 
CALL src\main\venv\Scripts\deactivate.bat
