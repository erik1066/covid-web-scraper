import requests, json, io, datetime
import county_report, state_report

STATE_ABBR = 'WI'
STATE = 'Wisconsin'
URL = 'https://dhsgis.wi.gov/server/rest/services/DHS_COVID19/COVID19_WI/FeatureServer/10/query?where=1%3D1&outFields=OBJECTID,NAME,POSITIVE,HOSP_YES,DEATHS,DATE&outSR=4326&f=json'

def scraper():
    # make an HTTP web request to get the data
    response = requests.get(URL)

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        jsonPayload = json.loads(response.text)
        features = jsonPayload['features']
        
        counties = []
        
        for feature in features:
            attribute = feature['attributes']
            
            county_name = attribute['NAME']

            if county_name == None or len(county_name) == 0 or county_name == '' or county_name == 'WI':
                continue

            confirmed = int(attribute['POSITIVE'])

            hospitalizations = 0
            if attribute['HOSP_YES'] != None:
                hospitalizations = int(attribute['HOSP_YES'])

            deaths = 0
            if attribute['DEATHS'] != None:
                deaths = int(attribute['DEATHS'])
            
            county = county_report.CountyReport(STATE, county_name, confirmed, deaths, hospitalizations, -1, datetime.datetime.now())

            existing_county = findCounty(county_name, counties)
            if existing_county == None:
                counties.append(county)
            elif existing_county.confirmed < county.confirmed or existing_county.deaths < county.deaths or existing_county.hospitalizations < county.hospitalizations:
                existing_county.confirmed = county.confirmed
                existing_county.deaths = county.deaths
                existing_county.hospitalizations = county.hospitalizations
            
            
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
