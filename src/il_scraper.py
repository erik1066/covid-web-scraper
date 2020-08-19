import requests, json, io, datetime, pathlib, sys, time, os, csv
from io import StringIO
import county_report, state_report
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

STATE_ABBR = 'IL'
STATE = 'Illinois'

URL = 'https://www.dph.illinois.gov/covid19/covid19-statistics'

def get_row_data(table):
    for row in table:
        yield [td.text for td in row.find_elements_by_xpath(".//td")]

def scraper():
    counties = []

    # You will need a WebDriver for Edge. See https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

    try:
    
        browser = webdriver.Edge("msedgedriver.exe")
        browser.get(URL)

        time.sleep(4)
        
        county_link = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/article/div/div/div/ul[1]/li[1]/a')))
        county_link.click()

        time.sleep(4)

        all_link = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pagin"]/li[12]/a')))
        all_link.click()

        time.sleep(2)

        county_table = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/article/div/div/div/table/tbody')))
        
        time.sleep(2)
        # print(county_table)

        htmlRows = county_table.find_elements_by_xpath(".//tr")

        # print(htmlRows)
        rows = get_row_data(htmlRows)
        # print(rows)

        for row in rows:
            # print(row)
            county_name = row[0]

            if county_name == 'Illinois':
                continue
            
            confirmed = int(row[2])
            deaths = int(row[3])
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