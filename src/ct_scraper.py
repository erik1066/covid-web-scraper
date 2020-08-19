import requests, json, io, datetime
import county_report, state_report

STATE_ABBR = 'CT'
STATE = 'Connecticut'
URL = 'https://data.ct.gov/resource/bfnu-rgqt.json'

def scraper():
    # make an HTTP web request to get the CT Json file
    response = requests.get(URL)

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        jsonPayload = json.loads(response.text)
        
        counties = []
        
        for item in jsonPayload:
            county_name = item['county']
            
            confirmed = 0
            if 'confirmedcases' in item:
                confirmed = int(item['confirmedcases'])

            hospitalizations = 0
            if 'hospitalization' in item:
                hospitalizations = int(item['hospitalization'])

            deaths = 0
            if 'confirmeddeaths' in item:
                deaths = int(item['confirmeddeaths'])

            county = findCounty(county_name, counties)

            if county == None:
                county = county_report.CountyReport(STATE, county_name, (int)(confirmed), (int)(deaths), -1, -1, datetime.datetime.now())
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
