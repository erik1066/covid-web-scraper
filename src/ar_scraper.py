import requests, bs4, datetime
import county_report, state_report

STATE_ABBR = 'AR'
STATE = 'Arkansas'

def scraper():
    # make an HTTP web request to get the AR data
    response = requests.get('https://www.healthy.arkansas.gov/programs-services/topics/covid-19-county-data')

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        table = bs4.BeautifulSoup(response.text, features="html.parser").select('table tr')
        
        counties = []
        
        for i in range (1, 75):
            row = table[i].find_all('td')
            county_name = row[0].find('p').getText()
            confirmed = int(row[1].find('p').getText())
            deaths = int(row[3].find('p').getText())
            
            county = county_report.CountyReport(STATE, county_name, confirmed, deaths, -1, -1, datetime.datetime.now())
            counties.append(county)

        # print the number of counties we processed
        print(' ', STATE_ABBR, ':', len(counties), ' counties processed OK')

        # build the state-level report object that will include all of the counties
        stateReport = state_report.StateReport(STATE, STATE_ABBR, counties, datetime.datetime.now())
        
        # return the state-level report
        return stateReport
        
    else:
        # Fail
        print(' ', STATE_ABBR, ': ERROR : Web download failed - HTTP status code ', response.status_code)

def findCounty(county_name, counties):
    for county in counties:
        if county.county == county_name:
            return county
