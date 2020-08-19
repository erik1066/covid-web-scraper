import requests, json, io, datetime, pathlib, sys, time, os, csv
from io import StringIO
import county_report, state_report
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

STATE_ABBR = 'SC'
STATE = 'South Carolina'

URL = 'https://www.arcgis.com/home/webmap/viewer.html?url=https://services2.arcgis.com/XZg2efAbaieYAXmu/ArcGIS/rest/services/COVID19_SharingView/FeatureServer/0&source=sd'

def get_row_data(table):
    for row in table:
        yield [td.text for td in row.find_elements_by_xpath(".//td")]
        
def scraper():
    counties = []

    # You will need a WebDriver for Edge. See https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

    try:
    
        browser = webdriver.Edge("msedgedriver.exe")
        browser.get(URL)

        time.sleep(1)
        
        show_table_link = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[3]/div/div/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div/div[2]/span')))
        show_table_link.click()

        time.sleep(1)

        county_div = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[5]/div[4]/div[1]/div/div/div/div[1]/div/div/div[2]/div/div[2]/div')))

        county_div_rows = county_div.find_elements_by_xpath('.//div[@role="row"]')
        
        # SC puts its county level data into lots of <div> elements, with one <div> per county. Each <div> has its own single-row <table> that contains the county data. Thus, we 
        # have some extra stuff to do to make this work right.
        for div_row in county_div_rows:
            county_table = div_row.find_element_by_xpath('.//table')
            htmlRows = county_table.find_elements_by_xpath(".//tr")  
            rows = get_row_data(htmlRows)

            for row in rows:
                county_name = row[0]

                if county_name == 'Unknown':
                    continue
                
                confirmed = int(row[3].replace(',', ''))
                deaths = int(row[4].replace(',', ''))
                county = county_report.CountyReport(STATE, county_name, confirmed, deaths, -1, -1, datetime.datetime.now())
                counties.append(county)

    except:
        print("Unexpected error:", sys.exc_info()[0])
    
    browser.quit()
            
    # print the number of counties we processed
    print(' ', STATE_ABBR, ':', len(counties), ' counties processed OK')

    # build the state-level report object that will include all of the counties
    stateReport = state_report.StateReport(STATE, STATE_ABBR, counties, datetime.datetime.now())
    
    # return the state-level report
    return stateReport        