import requests, io, csv, datetime
import county_report, state_report

STATE_ABBR = 'OK'
STATE = 'Oklahoma'
URL = 'https://storage.googleapis.com/ok-covid-gcs-public-download/oklahoma_cases_county.csv'

def scraper():
    # make an HTTP web request to get the OK CSV file
    response = requests.get(URL)

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
            
            county_name = row[0]

            # skip the header row
            if row[0] == 'County':
                continue   

            if county_name == '' or len(county_name) == 0:
                continue

            confirmedStr = row[1]
            confirmed = int(confirmedStr)

            deathsStr = row[2]
            deaths = int(deathsStr)

            county = county_report.CountyReport(STATE, county_name, confirmed, deaths, -1, -1, datetime.datetime.now())
            counties.append(county) # append the countyReport to our list of counties
                
        # print the number of counties we processed
        print(' ', STATE_ABBR, ':', len(counties), ' counties processed OK')

        # build the state-level report object that will include all of the counties
        stateReport = state_report.StateReport(STATE, STATE_ABBR, counties, datetime.datetime.now())
        
        # return the state-level report
        return stateReport

    else:
        # Fail
        print(' ', STATE_ABBR, ': ERROR : Download failed - HTTP status code ', response.status_code)
