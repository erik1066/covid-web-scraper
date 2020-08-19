import requests, zipfile, io, csv, datetime
import county_report, state_report

STATE_ABBR = 'GA'
STATE = 'Georgia'
URL = 'https://ga-covid19.ondemand.sas.com/docs/ga_covid_data.zip'

def scraper():
    # make an HTTP web request to get the GA ZIP file
    response = requests.get(URL)

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': ZIP downloaded succeeded')

        # read ZIP into memory
        z = zipfile.ZipFile(io.BytesIO(response.content))

        # extract the CSV file from the ZIP file into an in-memory byte array
        csvDataBytes = z.read('countycases.csv')

        # convert the byte array into a string so we can read it as a CSV file
        csvData = csvDataBytes.decode(encoding='UTF-8')

        # read the in-memory string using the 'csv' module so we can iterate over each row
        csvReader = csv.reader(csvData.splitlines(), delimiter=',', quotechar='"')
        
        # create a list that will contain our county data
        counties = []

        # iterate over every row in the CSV
        for row in csvReader:
            # skip the header row
            if row[0] == 'county_resident':
                continue
            
            # take the row we're iterating over and build a countyReport object out of it - this has the confirmed cases, deaths, etc that we're interested in
            county = county_report.CountyReport(STATE, row[0], (int)(row[1]), (int)(row[2]), (int)(row[3]), (float)(row[4]), datetime.datetime.now())
            counties.append(county) # append the countyReport to our list of counties

        # print the number of counties we processed
        print(' ', STATE_ABBR, ':', len(counties), ' counties processed OK')

        # build the state-level report object that will include all of the counties
        stateReport = state_report.StateReport(STATE, STATE_ABBR, counties, datetime.datetime.now())
        
        # return the state-level report
        return stateReport

    else:
        # Fail
        print(' ', STATE_ABBR, ': ERROR : ZIP download failed - HTTP status code ', response.status_code)
