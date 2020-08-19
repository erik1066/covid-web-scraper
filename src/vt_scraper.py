import requests, json, io, datetime
import county_report, state_report

STATE_ABBR = 'VT'
STATE = 'Vermont'
URL = 'https://services1.arcgis.com/BkFxaEFNwHqX3tAw/arcgis/rest/services/VIEW_EPI_CountyDailyCount_GEO_PUBLIC/FeatureServer/0/query?where=1%3D1&outFields=CNTY,CNTYNAME,Label,C_Total,D_Total,date&outSR=4326&f=json'

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
            
            county_name = attribute['Label']

            if county_name == None or len(county_name) == 0 or county_name == '' or county_name == 'Vermont':
                continue

            confirmed = int(attribute['C_Total'])

            deaths = 0
            if attribute['D_Total'] != None:
                deaths = int(attribute['D_Total'])
            
            county = county_report.CountyReport(STATE, county_name, confirmed, deaths, -1, -1, datetime.datetime.now())

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
