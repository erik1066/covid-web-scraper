import requests, json, io, datetime
import county_report, state_report

STATE_ABBR = 'CO'
STATE = 'Colorado'
URL = 'https://services3.arcgis.com/66aUo8zsujfVXRIT/arcgis/rest/services/colorado_covid19_county_statistics_cumulative/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'

def scraper():
    # make an HTTP web request to get the CO Json
    response = requests.get(URL)

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        jsonPayload = json.loads(response.text)
        features = jsonPayload['features']
        
        counties = []
        
        for feature in features:
            attribute = feature['attributes']
            
            county_name = attribute['LABEL']

            county = findCounty(county_name, counties)

            if county == None:
                county = county_report.CountyReport(STATE, county_name, 0, 0, -1, -1, datetime.datetime.now())
                counties.append(county)

            metric = attribute['Metric']
            
            if metric == 'Cases':
                confirmed = int(attribute['Value'])
                county.confirmed = confirmed
            
            if metric == 'Deaths':
                deaths = int(attribute['Value'])
                county.deaths = deaths

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
