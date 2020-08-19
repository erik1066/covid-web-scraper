import requests, json, io, datetime
import county_report, state_report

STATE_ABBR = 'FL'
STATE = 'Florida'
URL = 'https://opendata.arcgis.com/datasets/a7887f1940b34bf5a02c6f7f27a5cb2c_0.geojson'

def scraper():
    # make an HTTP web request to get the FL Json file
    response = requests.get(URL)

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        jsonPayload = json.loads(response.text)
        items = jsonPayload['features']

        counties = []
        
        for item in items:
            attributes = item['properties']
            county_name = attributes['County_1']

            if county_name == 'State': # this is FL's total, so skip
                continue
            
            confirmedStr = attributes['CasesAll']
            confirmed = int(confirmedStr)
            
            deathsStr = attributes['Deaths']
            deaths = int(deathsStr)

            hospitalizationsResStr = attributes['C_HospYes_Res'] # hospitalizations - Florida residents
            hospitalizationsRes = int(hospitalizationsResStr)

            hospitalizationsNonResStr = attributes['C_HospYes_NonRes'] # hospitalizations - Florida residents
            hospitalizationsNonRes = int(hospitalizationsNonResStr)

            county = county_report.CountyReport(STATE, county_name, confirmed, deaths, hospitalizationsRes + hospitalizationsNonRes, -1, datetime.datetime.now())
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
