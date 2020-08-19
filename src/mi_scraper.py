import requests, openpyxl, io, csv, datetime
import county_report, state_report

STATE_ABBR = 'MI'
STATE = 'Michigan'
URL = 'https://www.michigan.gov/documents/coronavirus/Cases_and_Deaths_by_County_2020-07-24_697248_7.xlsx'

def scraper():
    # make an HTTP web request to get the MI XLSX file
    response = requests.get(URL)

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        data = io.BytesIO(response.content)

        wb = openpyxl.load_workbook(filename=data, read_only=True, data_only=True)
        
        sheet = wb.worksheets[0]

        counties = []

        for i in range(2, 169):
            rowCount = str(i)
            status = sheet['B' + rowCount].value  
            if status == 'Confirmed':
                county = sheet['A' + rowCount].value
                confirmed = sheet['C' + rowCount].value
                deaths = sheet['D' + rowCount].value
            
                county = county_report.CountyReport(STATE, county, (int)(confirmed), (int)(deaths), -1, -1, datetime.datetime.now())
                counties.append(county) # append the countyReport to our list of counties

        # print the number of counties we processed
        print(' ', STATE_ABBR, ':', len(counties), ' counties processed OK')

        # build the state-level report object that will include all of the counties
        stateReport = state_report.StateReport(STATE, STATE_ABBR, counties, datetime.datetime.now())
        
        # return the state-level report
        return stateReport
        

    else:
        # Fail
        print(' ', STATE_ABBR, ': ERROR : Web download failed - HTTP status code ', response.status_code)