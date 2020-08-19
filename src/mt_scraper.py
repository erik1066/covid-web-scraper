import requests, bs4, datetime
import county_report, state_report

STATE_ABBR = 'MT'
STATE = 'Montana'
URL = 'https://dphhs.mt.gov/publichealth/cdepi/diseases/coronavirusmt/demographics'

def scraper():
    # make an HTTP web request to get the source information
    response = requests.get(URL)

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        soup = bs4.BeautifulSoup(response.text, features="html.parser")

        table = soup.find_all("table", attrs={"summary" : "Cases by County"})
        
        counties = []

        for item in table[0].find_all('tr'):
            
            row = item.find_all('td')
            
            if len(row) == 0:
                continue

            county_name = row[0].text

            if county_name == 'Total':
                continue

            casesStr = row[1].text
            deathsStr = row[2].text

            if len(casesStr) == 0 or casesStr == '' or casesStr == '\xa0' or casesStr == '\xa0\n\t':
                casesStr = '0'
            
            if len(deathsStr) == 0 or casesStr == '' or deathsStr == '\xa0' or deathsStr == '\xa0\n\t':
                deathsStr = '0'

            confirmed = int(casesStr)
            deaths = int(deathsStr)
            
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
