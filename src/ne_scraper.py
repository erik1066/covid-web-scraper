import requests, json, io, datetime
import county_report, state_report

STATE_ABBR = 'NE'
STATE = 'Nebraska'

def scraper():
    # make an HTTP web request to get the data
    response = requests.get('https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases_US/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json')

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        jsonPayload = json.loads(response.text)
        features = jsonPayload['features']
        
        counties = []
        
        for feature in features:
            attribute = feature['attributes']
            
            state_name = attribute['Province_State']

            if state_name != 'Nebraska':
                continue

            county_name = attribute['Admin2']
            confirmed = int(attribute['Confirmed'])
            deaths = int(attribute['Deaths'])
            
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
