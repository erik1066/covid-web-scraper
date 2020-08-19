# See https://app.powerbigov.us/view?r=eyJrIjoiMjA2ZThiOWUtM2FlNS00MGY5LWFmYjUtNmQwNTQ3Nzg5N2I2IiwidCI6ImU0YTM0MGU2LWI4OWUtNGU2OC04ZWFhLTE1NDRkMjcwMzk4MCJ9. 
# This is a weird format of Json and it might be better to use a browser-based scrape instead of a Json download...

import requests, json, io, datetime, pathlib
import county_report, state_report

STATE_ABBR = 'NV'
STATE = 'Nevada'

def scraper():

    payload = ''

    filepath = pathlib.Path.cwd().joinpath('config', 'nv_post_body.json')
    with open(filepath, 'r') as file:
        payload = file.read().replace('\n', '')

    # make an HTTP web request to get the data
    response = requests.post('https://wabi-us-gov-iowa-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true', 
    data=payload)

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        jsonPayload = json.loads(response.text)
        features = jsonPayload['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']

        counties = []
        
        for feature in features:

            if 'S' in feature:
                continue
            
            county_object = feature['C']
            has_R = 'R' in feature
            
            deaths = 0

            cases_index = 3
            if has_R:
                cases_index = 2
            else:
                deaths = int(county_object[1])

            county_name = county_object[0]
            confirmed = int(county_object[cases_index])
            
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
