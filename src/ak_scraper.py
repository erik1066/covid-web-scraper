import requests, json, io, datetime
import county_report, state_report

STATE_ABBR = 'AK'
STATE = 'Alaska'

def scraper():
    # make an HTTP web request to get the AK Json
    response = requests.get('https://services1.arcgis.com/WzFsmainVTuD5KML/arcgis/rest/services/Geographic_Distribution_of_Confirmed_Cases/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json')

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        jsonPayload = json.loads(response.text)
        features = jsonPayload['features']
        
        counties = []
        
        for feature in features:
            attribute = feature['attributes']
            
            county_name = attribute['Borough_Census_Area']
            confirmed = int(attribute['All_Cases'])
            hospitalizations = int(attribute['Hospitalizations'])
            deaths = int(attribute['Deaths'])

            county = findCounty(county_name, counties)

            if county == None:
                county = county_report.CountyReport(STATE, county_name, (int)(confirmed), (int)(deaths), -1, -1, datetime.datetime.now())
                counties.append(county)
            else:
                county.confirmed += confirmed
                county.hospitalizations += hospitalizations
                county.deaths += deaths

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
