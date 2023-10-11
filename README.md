# SecAdvScraper UI

---
## Description
This application provides a User Interface (UI) for the [SecAdvScraper](src/main/SecAdvScraper.py) module by providing a simple interface for SEC ADV Form data extraction.
The application will parse a SEC ADV Form for the below indicated datasets and write them to an Excel (with on sheet per dataset):
- Item 5D
- Direct Owners
- Indirect Owners

*To use the underlying SecAdvScraper module from within Python refer to [SecAdvScraperModule.md](SecAdvScraperModule.md)*

----
## Requirements
- Python

----
## Instructions
1. Execute SecAdvScraperUI.bat (command prompt and pop-up will open)
2. Paste the URL in the corresponding field
3. Select Output Path
4. Click on Extract Data
5. Excel Workbook (.xlsx) will be generated
6. To exit simply exit the pop-up (command prompt will close automatically)

**Important**: *The application uses a Virtual Enviroment for execution. On first execution the enviroment will be automatically generated and all required dependencies (as defined in src/main/requirements.txt) will be installed.*

----
