import requests, json, io, datetime, pathlib, sys, time
import county_report, state_report
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

STATE_ABBR = 'UT'
STATE = 'Utah'

URL = 'https://coronavirus-dashboard.utah.gov/'

def get_row_data(table):
    for row in table:
        yield [td.text for td in row.find_elements_by_xpath(".//td")]

def scraper():
    counties = []

    # You will need a WebDriver for Edge. See https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

    browser = webdriver.Edge("msedgedriver.exe")
    browser.get(URL)

    counties_table = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0"]')))

    time.sleep(1)

    htmlRows = counties_table.find_elements_by_xpath(".//tbody/tr")
    rows = get_row_data(htmlRows)

    for row in rows:
        county_name = row[0]

        if county_name == 'State Total' or county_name == 'Unassigned' or len(row) < 4:
            continue

        confirmed = int(row[1].replace(',', ''))
        hospitalizations = int(row[2].replace(',', ''))
        deaths = int(row[3].replace(',', ''))
        county = county_report.CountyReport(STATE, county_name, confirmed, deaths, hospitalizations, -1, datetime.datetime.now())
        counties.append(county)
    
    browser.quit()
            
    # print the number of counties we processed
    print(' ', STATE_ABBR, ':', len(counties), ' counties processed OK')

    # build the state-level report object that will include all of the counties
    stateReport = state_report.StateReport(STATE, STATE_ABBR, counties, datetime.datetime.now())
    
    # return the state-level report
    return stateReport        