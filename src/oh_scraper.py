import requests, io, csv, datetime
import county_report, state_report

STATE_ABBR = 'OH'
STATE = 'Ohio'
URL = 'https://coronavirus.ohio.gov/static/COVIDSummaryData.csv'

def scraper():
    # make an HTTP web request to get the CA CSV file
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
            confirmedStr = row[6]
            
            # skip the header row
            if county_name == 'County' or len(county_name) == 0 or confirmedStr == 'Case Count' or county_name == 'Grand Total':
                continue

            confirmed = int(confirmedStr.replace(',', ''))

            deathsStr = row[7]
            deaths = int(deathsStr.replace(',', ''))

            hospitalizationsStr = row[8]
            hospitalizations = int(hospitalizationsStr.replace(',', ''))

            county = findCounty(county_name, counties)

            if county == None:
                county = county_report.CountyReport(STATE, county_name, confirmed, deaths, hospitalizations, -1, datetime.datetime.now())
                counties.append(county) # append the countyReport to our list of counties
            else:
                county.confirmed += confirmed
                county.deaths += deaths
                county.hospitalizations += hospitalizations
                
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