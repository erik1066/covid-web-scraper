import requests, json, io, datetime, pathlib, sys, time, os, csv
from io import StringIO
import county_report, state_report
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

STATE_ABBR = 'ID'
STATE = 'Idaho'

URL = 'https://public.tableau.com/views/DPHIdahoCOVID-19Dashboard_V2/Story1?%3Aembed=y&%3AshowVizHome=no&%3Adisplay_count=y&%3Adisplay_static_image=y&%3AbootstrapWhenNotified=true&%3Alanguage=en&:embed=y&:showVizHome=n&:apiID=host0#navType=0&navSrc=Parse'

def scraper():
    counties = []

    # You will need a WebDriver for Edge. See https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

    try:
    
        browser = webdriver.Edge("msedgedriver.exe")
        browser.get(URL)

        file_path = pathlib.Path.home().joinpath('Downloads', 'County Table.csv')

        if os.path.isfile(file_path):
            print("  FAILED on ", STATE, " : Please delete ", file_path, " and start the process over. This file must not exist prior to running the scrape operation.")
        
        tab_link = browser.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div/div[2]/div[4]/div/div/div/span[2]/div/span/span/span[3]/div[2]/div/div[1]/span/div')
        tab_link.click()

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
                    if county_name == 'County' or row[1] == 'Public Health District' or row[2] == 'Confirmed Cases':
                        continue

                    confirmed = row[2].replace(',', '')
                    deaths = row[7].replace(',', '')
                    if len(deaths) == 0:
                        deaths = '0'

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