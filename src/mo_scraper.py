import requests, json, io, datetime
import county_report, state_report

STATE_ABBR = 'MO'
STATE = 'Missouri'
URL = 'https://services6.arcgis.com/Bd4MACzvEukoZ9mR/arcgis/rest/services/county_MOHSIS_map/FeatureServer/0/query?where=1%3D1&outFields=OBJECTID,NAME,NAME2,CASES,DEATHS&returnGeometry=false&outSR=4326&f=json'

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
            confirmed = int(attribute['CASES'])
            deaths = int(attribute['DEATHS'])
            
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
