import requests, json, io, datetime, pathlib, sys, time, os, csv
from io import StringIO
import county_report, state_report
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

STATE_ABBR = 'DE'
STATE = 'Delaware'

URL = 'https://myhealthycommunity.dhss.delaware.gov/embed/covid19/bg/white'

def scraper():
    counties = []

    # You will need a WebDriver for Edge. See https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

    try:
    
        browser = webdriver.Edge("msedgedriver.exe")
        browser.get(URL)

        county1 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/section/div/article/div/div[1]/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/a/div[2]/span')))
        county2 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/section/div/article/div/div[1]/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/a/div[2]/span')))
        county3 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/section/div/article/div/div[1]/div[2]/div[2]/div[2]/div/div/div[2]/div/div[3]/a/div[2]/span')))

        county1_cases = county1.text.replace(',', '')
        county2_cases = county2.text.replace(',', '')
        county3_cases = county3.text.replace(',', '')

        county = county_report.CountyReport(STATE, 'New Castle', int(county1_cases), -1, -1, -1, datetime.datetime.now())
        counties.append(county) 

        county = county_report.CountyReport(STATE, 'Kent', int(county2_cases), -1, -1, -1, datetime.datetime.now())
        counties.append(county) 

        county = county_report.CountyReport(STATE, 'Sussex', int(county3_cases), -1, -1, -1, datetime.datetime.now())
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