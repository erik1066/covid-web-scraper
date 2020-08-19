import requests, json, io, datetime, pathlib, sys, time, os, csv
from io import StringIO
import county_report, state_report
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

STATE_ABBR = 'NC'
STATE = 'North Carolina'

URL = 'https://public.tableau.com/views/NCDHHS_COVID-19_DataDownload/CountyCasesandDeaths?%3Aembed=y&amp%3B%3AshowVizHome=no&amp%3B%3Ahost_url=https%3A%2F%2Fpublic.tableau.com%2F&amp%3B%3Aembed_code_version=3&amp%3B%3Atabs=yes&amp%3B%3Atoolbar=no&amp%3B%3Aanimate_transition=yes&amp%3B%3Adisplay_static_image=no&amp%3B%3Adisplay_spinner=no&amp%3B%3Adisplay_overlay=yes&amp%3B%3Adisplay_count=no&amp%3Bpublish=yes&amp%3B%3AloadOrderID=0'

def scraper():
    counties = []

    # You will need a WebDriver for Edge. See https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

    try:
    
        browser = webdriver.Edge("msedgedriver.exe")
        browser.get(URL)

        file_path = pathlib.Path.home().joinpath('Downloads', 'TABLE_COUNTY.csv')

        if os.path.isfile(file_path):
            print("  FAILED on ", STATE, " : Please delete ", file_path, " and start the process over. This file must not exist prior to running the scrape operation.")
        
        download_link = browser.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/div[5]')
        download_link.click()

        crosstab_link = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div/div[2]/div/button[3]')))
        crosstab_link.click()

        csv_link = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div/div/div/div[2]/div/div[2]/div[2]/div/label[2]')))
        csv_link.click()

        download_button = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div/div/div/div[2]/div/div[3]/button')))
        download_button.click()
        time.sleep(2)

        with open(file_path, 'rt', encoding='utf-16-le') as file_contents:
            data = file_contents.read()
            infile = StringIO(data)

            with open(file_path) as csv_file:
                csv_reader = csv.reader(data.splitlines(), delimiter='\t', quotechar='"') 

                for row in csv_reader:
                    # print(row)
                    county_name = row[0]
                    if county_name == 'County' or row[1] == 'Cases' or row[2] == 'Deaths':
                        continue

                    confirmed = row[1].replace(',', '')
                    deaths = row[2].replace(',', '')

                    county = county_report.CountyReport(STATE, county_name, (int)(confirmed), (int)(deaths), -1, -1, datetime.datetime.now())
                    counties.append(county) 

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