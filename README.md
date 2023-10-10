# SecAdvScraper UI
This application will parse the following data from a SEC ADV url and generate an excel with one sheet per dataset:
- Item 5D
- Direct Owners
- Indirect Owners

----

## Requirements
python

----

## Instructions
1. Execute SecAdvScraperUI.bat (command prompt and pop-up will open)
2. Paste the URL in the corresponding field
3. Select Output Path
4. Click on Extract Data
5. Excel Workbook (.xlsx) will be generated
6. To exit simply exit the pop-up (command prompt will close automatically)

Important: The application uses a Virtual Enviroment for execution. On first execution the enviroment will be automatically generated and all required dependencies (as defined in src/main/requirements.txt) will be installed.

----

## Advanced User
The underlying module used to parse the SEC ADV url is the SecAdvScraper class inside src/main/SecAdvScraper.py

To execute using Python through the command line, follow the below instructions:
1. Open a Command Prompt window
2. Change directory to the SecAdvScraper folder:
```bash
cd path\to\SecAdvScraper
```
3. Execute Python:
```bash
python
```
4. Import the Module
```python
from src.main.SecAdvScraper import SecAdvScraper as SAS
```
5. Initialize an instance for the URL:
```python
URL = "https://files.adviserinfo.sec.gov/IAPD/content/viewform/adv/sections/iapd_AdvIdentifyingInfoSection.aspx?ORG_PK=324312&FLNG_PK=008F69B6000801D40525238104B483B1056C8CC0"
scraper= SAS(URL)
```
6. You can now access the Pandas DataFrames as follows:
```python
scraper.DirectOwners
scraper.IndirectOwners
scraper.Item5D
```
8. To export the above Pandas DataFrames to Excel:
```python
scraper.WriteToExcel(outputPath)
```
7. The following functions are also available:
```python
scraper.getFilteredDirectOwners() # Returns Direct Owners with Owner Codes C, D or E
scraper.getFilteredIndirectOwners() # Returns Indirect Owners with Owner Codes B, C, D or E
scraper.getFilteredItem5D(assetsCutoff) # Returns only assets above the assetsCutoff value (for greater than 0 you can use 0.1)
```
----
