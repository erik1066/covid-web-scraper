import requests, json, io, datetime, pathlib, sys
import county_report, state_report
from selenium import webdriver

STATE_ABBR = 'NM'
STATE = 'New Mexico'

URL = 'https://cvprovider.nmhealth.org/public-dashboard.html'

def get_row_data(table):
    for row in table:
        yield [td.text for td in row.find_elements_by_xpath(".//td")]

def scraper():
    counties = []

    # You will need a WebDriver for Edge. See https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

    browser = webdriver.Edge("msedgedriver.exe")
    browser.get(URL)

    try:
        counties_link = browser.find_element_by_id('open-counties-table-modal')
        counties_link.click()

        rootCountyDiv = browser.find_elements_by_class_name('counties-table')
        htmlRows = rootCountyDiv[0].find_elements_by_xpath(".//tbody/tr")

        rows = get_row_data(htmlRows)

        for row in rows:
            county_name = row[0]
            confirmed = int(row[1])
            deaths = int(row[2])
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