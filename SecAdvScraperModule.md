# SEC ADV Scraper Module

----
## Description
The underlying module used to parse the *SEC ADV Form* is the *SecAdvScraper class* inside [src/main/SecAdvScraper.py](src/main/SecAdvScraper.py). This module provides multiple functions for scraping and interacting with *SEC ADV Form* data. To incorporate it into your Python workflow the below instructions can be followed. Module will scrape the following datasets from a *SEC ADV Form*:
- Item 5D
- Direct Owners
- Indirect Owners

----
## Instructions
To execute using Python through the command line, follow the below instructions:

#### 1. Open a Command Prompt window.

#### 2. Change directory to the SecAdvScraper folder:
```bash
cd path\to\SecAdvScraper
```
#### 3. Set up the Virtual Enviroment (ONLY required on initial setup):
```bash
python -m venv src\main\venv
src\main\venv\Scripts\activate.bat
pip install --require-virtualenv -r src/main/requirements.txt
src\main\venv\Scripts\deactivate.bat
```
\*\* *Note: If Virtual Enviroments are not a necessity for your usecase, you can directly install the required dependencies with the below command and skip Steps 4 and 12 (activation/deactivation of virtual enviroment):*
```bash
pip install -r src\main\requirements.txt
```
#### 4. Activate the Virtual Enviroment:
```bash
src\main\Scripts\activate.bat
```
#### 5. Execute Python:
```bash
python
```
#### 6. Import the module:
```python
from src.main.SecAdvScraper import SecAdvScraper as SAS
```
\*\* *Note: src.main indicates the path to the SecAdvScraper.py file relative to your current working directory*
#### 7. Initialize an instance for the URL
```python
URL = "https://files.adviserinfo.sec.gov/IAPD/content/viewform/adv/sections/iapd_AdvIdentifyingInfoSection.aspx?ORG_PK=324312&FLNG_PK=008F69B6000801D40525238104B483B1056C8CC0"
scraper= SAS(URL)
```
\*\* *Expected URL Pattern: "https://files.adviserinfo.sec.gov/IAPD/content/viewform/adv/sections/\*\*\*\*\*\*.aspx?ORG_PK=\*\*\*\*\*\*&FLNG_PK=\*\*\*\*\*\*"*
#### 8. You can now access the extracted Pandas DataFrames as follows:
```python
scraper.DirectOwners
scraper.IndirectOwners
scraper.Item5D
```
#### 9. To export the above Pandas DataFrames to Excel use the below function:
```python
scraper.WriteToExcel(outputPath)
```
#### 10. The following functions are also available for further interaction with scraped data:
```python
scraper.getFilteredDirectOwners() # Returns Direct Owners with Owner Codes C, D or E
scraper.getFilteredIndirectOwners() # Returns Indirect Owners with Owner Codes B, C, D or E
scraper.getFilteredItem5D(assetsCutoff) # Returns only assets above the assetsCutoff value (for greater than 0 you can use 0.1)
```
#### 11. Exit Python:
```python
exit()
```
#### 12. Deactivate the Virtual Enviroment:
```bash
src\main\Scripts\deactivate.bat
```
----