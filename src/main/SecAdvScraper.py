import requests
import pandas as pd
import logging
import os
import re

#------------------------------------------------------------------------------
# CONFIG
#------------------------------------------------------------------------------

FORMAT = '[%(asctime)s][%(levelname)s] %(module)s - %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S',)
pd.options.display.float_format = '{:,.2f}'.format

#------------------------------------------------------------------------------
# MODULE
#------------------------------------------------------------------------------

class SecAdvScraper:

    def __init__(self, URL):
        self.ERRORS = {}
        if not self.__validURL(URL):
            logging.warn('Invalid URL')
            self.ERRORS['URL'] = 'Invalid URL'
            return
        self.BASE = "https://files.adviserinfo.sec.gov/IAPD/content/viewform/adv/Sections/"    
        self.PARAMS = self.__getParams(URL)
        self.ORG_PK = self.__getOrgPK()
        self.FLNG_PK = self.__getFlngPK()
        self.ERRORS = {}
        self.__scrapeAdvForm()

    # ----------------------
    # PARSE URL
    #-----------------------

    def __validURL(self, URL):
        url = re.findall(r"https://files.adviserinfo.sec.gov/IAPD/content/viewform/adv/sections/iapd_.*Section\.aspx\?ORG_PK=[0-9]+\&FLNG_PK=[0-9A-Z]{40}", URL)
        if len(url) == 1:
            return True
        else:
            return False
        
    def __getParams (self, URL):
        PARAMS = URL.split('?')[1].split('&')
        return PARAMS

    def __getOrgPK (self):
        ORG_PK = self.PARAMS[0].split('=')[1]
        return ORG_PK

    def __getFlngPK (self):
        FLNG_PK = self.PARAMS[1].split('=')[1]
        return FLNG_PK

    # ----------------------
    # GET ITEM DATA
    #----------------------- 
    #
    # Item5D 
    # Direct Owners
    # Indirect Owners
    #
    #----------------------- 

    def __getData (self, section):
        url = self.BASE + section + "ORG_PK=" + self.ORG_PK + "&" + "FLNG_PK=" + self.FLNG_PK
        response = requests.get(url)
        html_doc = response.content
        dfs = pd.read_html(html_doc)
        return dfs

    def __getItem5D(self):
        section = "iapd_AdvAdvisoryBusinessSection.aspx?"
        dfs = self.__getData(section)
        for df in dfs: 
            if df[0][0] == 'Type of Client':
                headers = df.iloc[0]
                Item5D  = pd.DataFrame(df.values[1:], columns=headers)
        Item5D.columns = [self.__cleanColumns(column) for column in Item5D.columns]
        Item5D['Amount_of_Regulatory_Assets_under_Management'] = [self.__cleanData(value) for value in Item5D['Amount_of_Regulatory_Assets_under_Management']]
        return Item5D

    def __getDirectOwners(self):
        section = "iapd_AdvScheduleASection.aspx?"
        dfs = self.__getData(section)
        for df in dfs: 
            if df.columns[0] == 'FULL LEGAL NAME (Individuals: Last Name, First Name, Middle Name)': 
                DirectOwners = df
        DirectOwners.columns = [self.__cleanColumns(column) for column in DirectOwners.columns]
        return DirectOwners

    def __getIndirectOwners(self):
        section = "iapd_AdvScheduleBSection.aspx?"
        dfs = self.__getData(section)
        for df in dfs: 
            if df.columns[0] == 'FULL LEGAL NAME (Individuals: Last Name, First Name, Middle Name)': 
                IndirectOwners = df
        IndirectOwners.columns = [self.__cleanColumns(column) for column in IndirectOwners.columns]
        return IndirectOwners

    def __scrapeAdvForm (self):
        try:
            self.Item5D = self.__getItem5D()
        except Exception as e:
            logging.error('Unable to extract Item5D data. Verify URL.')
            logging.error("Error: "+ str(e))
            self.ERRORS['Item5F'] = str(e)
        try:
            self.DirectOwners = self.__getDirectOwners()
        except Exception as e:
            logging.error('Unable to extract DirectOwners data. Verify URL.')
            logging.error("Error: "+ str(e))
            self.ERRORS['DirectOwners'] = str(e)
        try:
            self.IndirectOwners = self.__getIndirectOwners()
        except Exception as e:
            logging.error('Unable to extract IndirectOwners data. Verify URL.')
            logging.error("Error: "+ str(e))
            self.ERRORS['IndirectOwners'] = str(e)


    #----------------------
    # OUTPUT
    #-----------------------

    def WriteToExcel (self, output_path):
        """
        Method to generate excel with one tab per Item

        @params string output_path
        @returns {ORG_PK}.xlsx
        """
        self.fileName = self.ORG_PK + '.xlsx'
        filePath = os.path.join(output_path, self.fileName)
        writer = pd.ExcelWriter(filePath)
        self.Item5D.to_excel(writer, sheet_name='Item5D', index=False)
        self.DirectOwners.to_excel(writer, sheet_name='DirectOwners', index=False)
        self.IndirectOwners.to_excel(writer, sheet_name='IndirectOwners', index=False)
        writer.close() 

    # ----------------------
    # CLEANING/FORMATTING FUNCTIONS
    #-----------------------

    def __cleanColumns (self, column):
        column = re.sub(r'(\(\d\))*', '', column).strip().replace(' ','_')
        return column

    def __cleanData (self, item):
        item = item.replace('$','').replace(",","").strip()
        item = float(item or 0)
        return item

    # ----------------------
    # FILTERING FUNCTIONS
    #-----------------------

    def getFilteredDirectOwners (self):
        """
        Method to get Item5 items where assets are equal or greater than {min}

        @params float min
        @returns df filteredItem5D
        """
        DirectOwners = self.DirectOwners
        expCodes = ["C","D","E"]
        filteredDirectOwners = DirectOwners[DirectOwners.Ownership_Code.isin(expCodes)]
        return filteredDirectOwners

    def getFilteredIndirectOwners (self):
        """
        Method to get Item5 items where assets are equal or greater than {min}

        @params float min
        @returns df filteredItem5D
        """
        IndirectOwners = self.IndirectOwners
        expCodes = ["B","C","D","E"]
        filteredIndirectOwners = IndirectOwners[IndirectOwners.Ownership_Code.isin(expCodes)]
        return filteredIndirectOwners

    def getFilteredItem5D (self, min = 0):
        """
        Method to get Item5 items where assets are equal or greater than {min}

        @params optional float min default=0
         @returns df filteredItem5D
        """
        Item5D = self.Item5D
        filteredItem5D  = Item5D[Item5D['Amount_of_Regulatory_Assets_under_Management'] >= min]
        return filteredItem5D

