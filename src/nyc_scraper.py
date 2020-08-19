import requests, io, csv, datetime
import county_report, state_report

STATE_ABBR = 'NYC'
STATE = 'New York City'

def scraper():
    # make an HTTP web request to get the data
    response = requests.get('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/by-boro.csv')

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        csvData = response.text

        # read the in-memory string using the 'csv' module so we can iterate over each row
        csvReader = csv.reader(csvData.splitlines(), delimiter=',', quotechar='"')
        
        # create a list that will contain our county data
        counties = []

        # iterate over every row in the CSV
        for row in csvReader:
            # skip the header row
            if row[0] == 'BOROUGH_GROUP':
                continue
            
            county_name = row[0]
            confirmed = int(row[4])
            deaths = int(row[6])
            hospitalizations = int(row[5])

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
        print(' ', STATE_ABBR, ': ERROR : Download failed - HTTP status code ', response.status_code)