import requests, io, datetime, pathlib, sys, time, os, openpyxl
import county_report, state_report
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

STATE_ABBR = 'AL'
STATE = 'Alabama'

URL = 'https://dph1.adph.state.al.us/covid-19/'

FILE_NAME = 'COVID-19 in Alabama.xlsx'

def scraper():
    counties = []

    # You will need a WebDriver for Edge. See https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

    try:
    
        browser = webdriver.Edge("msedgedriver.exe")
        browser.get(URL)

        file_path = pathlib.Path.home().joinpath('Downloads', FILE_NAME)

        if os.path.isfile(file_path):
            print("  FAILED on ", STATE, " : Please delete ", file_path, " and start the process over. This file must not exist prior to running the scrape operation.")
        
        download_link = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div/div[1]/a[2]')))
        download_link.click()

        time.sleep(4)

        wb = openpyxl.load_workbook(filename=file_path)
        
        sheet = wb.worksheets[0]

        counties = []

        max_rows = sheet.max_row

        for i in range(2, max_rows):
            rowCount = str(i)
            #     print(rowCount)
            county_name = sheet['A' + rowCount].value
                

            if county_name == None or len(county_name) == 0:
                continue

            confirmed = sheet['B' + rowCount].value
            deaths = sheet['D' + rowCount].value
        
            county = county_report.CountyReport(STATE, county_name, (int)(confirmed), (int)(deaths), -1, -1, datetime.datetime.now())
            counties.append(county) # append the countyReport to our list of counties

        wb.close()

    except:
        print("Unexpected error:", sys.exc_info()[0])
    
    browser.quit()

    os.remove(file_path)
            
    # print the number of counties we processed
    print(' ', STATE_ABBR, ':', len(counties), ' counties processed OK')

    # build the state-level report object that will include all of the counties
    stateReport = state_report.StateReport(STATE, STATE_ABBR, counties, datetime.datetime.now())
    
    # return the state-level report
    return stateReport        