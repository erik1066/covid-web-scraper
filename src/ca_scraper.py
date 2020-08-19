import requests, io, csv, datetime
import county_report, state_report

STATE_ABBR = 'CA'
STATE = 'California'

def scraper():
    # make an HTTP web request to get the CA CSV file
    response = requests.get('https://data.ca.gov/dataset/590188d5-8545-4c93-a9a0-e230f0db7290/resource/926fd08f-cc91-4828-af38-bd45de97f8c3/download/statewide_cases.csv')

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
            if row[0] == 'county':
                continue    
            
            county_name = row[0]
            confirmedStr = row[1]
            confirmed = 0
            if '.' in confirmedStr:
                confirmed = int(float(confirmedStr))
            elif len(confirmedStr) > 0:
                confirmed = int(confirmedStr)

            deathsStr = row[2]
            deaths = 0
            if '.' in deathsStr:
                deaths = int(float(deathsStr))
            elif len(deathsStr) > 0:
                deaths = int(deathsStr)

            county = findCounty(county_name, counties)

            if county == None:
                county = county_report.CountyReport(STATE, county_name, confirmed, deaths, -1, -1, datetime.datetime.now())
                counties.append(county) # append the countyReport to our list of counties
            else:
                county.confirmed = confirmed
                county.deaths = deaths
                
        # print the number of counties we processed
        print(' ', STATE_ABBR, ':', len(counties), ' counties processed OK')

        # build the state-level report object that will include all of the counties
        stateReport = state_report.StateReport(STATE, STATE_ABBR, counties, datetime.datetime.now())
        
        # return the state-level report
        return stateReport

    else:
        # Fail
        print(' ', STATE_ABBR, ': ERROR : Download failed - HTTP status code ', response.status_code)


def findCounty(county_name, counties):
    for county in counties:
        if county.county == county_name:
            return county