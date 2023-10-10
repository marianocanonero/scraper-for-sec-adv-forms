@echo off
type README.md
IF NOT EXIST src\main\venv (
    ECHO Setting up the Virtual Enviroment...
    CALL src\main\Setup.bat
    ECHO Virtual Enviroment set up completed
)
CALL src\main\venv\Scripts\activate.bat
ECHO Activated Virtual Enviroment
python src\main\SecAdvScraperUI.py
CALL src\main\venv\Scripts\deactivate.bat
ECHO Deactivated Virtual Enviroment
ECHO Exiting...
