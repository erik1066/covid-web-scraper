import requests, json, io, datetime
import county_report, state_report

STATE_ABBR = 'VA'
STATE = 'Virginia'
URL = 'https://data.virginia.gov/resource/bre9-aqqr.json'

def scraper():
    # make an HTTP web request to get the VA Json file
    response = requests.get(URL)

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        counties = []
        jsonPayload = json.loads(response.text)
        
        for item in jsonPayload:
            
            county_name = item['locality']
            
            if findCounty(county_name, counties) == None:
                confirmedStr = item['total_cases']
                confirmed = int(confirmedStr)
                
                deathsStr = item['deaths']
                deaths = int(deathsStr)

                hospitalizationsStr = item['hospitalizations']
                hospitalizations = int(hospitalizationsStr)

                county = county_report.CountyReport(STATE, county_name, confirmed, deaths, hospitalizations, -1, datetime.datetime.now())
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
