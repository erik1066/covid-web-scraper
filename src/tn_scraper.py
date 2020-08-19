import requests, openpyxl, io, csv, datetime, os, pathlib
import county_report, state_report

STATE_ABBR = 'TN'
STATE = 'Tennessee'
URL = 'https://www.tn.gov/content/dam/tn/health/documents/cedep/novel-coronavirus/datasets/Public-Dataset-County-New.XLSX'

def scraper():
    # make an HTTP web request to get the MI XLSX file
    response = requests.get(URL)

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        temppath = 'temp' 
        if not os.path.exists(temppath):
            os.makedirs(temppath)
        
        tempfilename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + '_temp_' + STATE_ABBR + '.xlsx'
        tempfilepath = pathlib.Path.cwd().joinpath('temp', tempfilename)

        with open(tempfilepath, "wb") as file:
            file.write(response.content)

        wb = openpyxl.load_workbook(filename=tempfilepath)
        
        sheet = wb.worksheets[0]
        max_rows = sheet.max_row

        counties = []
        countyDictionary = {}

        i = max_rows

        while i > 2:
            rowCount = str(i)
            county_name = sheet['B' + rowCount].value

            county = findCounty(county_name, countyDictionary)

            if county == None:
                
                confirmed = int(sheet['E' + rowCount].value)
                deaths = int(sheet['P' + rowCount].value)
            
                county = county_report.CountyReport(STATE, county_name, confirmed, deaths, -1, -1, datetime.datetime.now())
                counties.append(county) # append the countyReport to our list of counties
                countyDictionary[county_name] = county

            i = i - 1

        # since the above algorithm outputs the counties in reverse-ABC order, let's reverse that so they're in ABC order...
        counties = list(reversed(counties))

        # print the number of counties we processed
        print(' ', STATE_ABBR, ':', len(counties), ' counties processed OK')

        # build the state-level report object that will include all of the counties
        stateReport = state_report.StateReport(STATE, STATE_ABBR, counties, datetime.datetime.now())
        
        # return the state-level report
        return stateReport
        

    else:
        # Fail
        print(' ', STATE_ABBR, ': ERROR : Web download failed - HTTP status code ', response.status_code)


def findCounty(county_name, countyDictionary):
    if county_name in countyDictionary:
        return countyDictionary[county_name]
    else:
        return None