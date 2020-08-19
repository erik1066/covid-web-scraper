import requests, openpyxl, io, os, datetime, pathlib
import county_report, state_report

STATE_ABBR = 'LA'
STATE = 'Louisiana'
URL = 'https://ldh.la.gov/assets/oph/Coronavirus/data/LA_COVID_TESTBYDAY_PARISH_PUBLICUSE.xlsx'

def scraper():
    # make an HTTP web request to get the file
    response = requests.get(URL)

    if response.status_code == requests.codes.ok:
        # Success - print to the console that the HTTP request succeeeded
        print(' ', STATE_ABBR, ': Downloaded succeeded')

        # Writing the XLSX to disk makes the loop below orders of magnitude faster 
        # versus keeping the XLSX doc in-memory, so we create a temp folder and download
        # the file there.
        temppath = 'temp' 
        if not os.path.exists(temppath):
            os.makedirs(temppath)
        
        tempfilename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + '_temp_' + STATE_ABBR + '.xlsx'
        tempfilepath = pathlib.Path.cwd().joinpath('temp', tempfilename)

        with open(tempfilepath, "wb") as file:
            file.write(response.content)

        wb = openpyxl.load_workbook(filename=tempfilepath)
        
        sheet = wb.worksheets[0]

        parishes = []
        parishesDictionary = {}

        max_rows = sheet.max_row

        for i in range(2, max_rows):
            rowCount = str(i)
            # print(rowCount)
            parish_name = sheet['B' + rowCount].value
            confirmed = sheet['F' + rowCount].value

            parish = findParish(parish_name, parishesDictionary)

            if parish == None:
                parish = county_report.CountyReport(STATE, parish_name, (int)(confirmed), -1, -1, -1, datetime.datetime.now())
                parishes.append(parish)
                parishesDictionary[parish_name] = parish
            else:
                parish.confirmed += int(confirmed)

        # print the number of counties we processed
        print(' ', STATE_ABBR, ':', len(parishes), ' counties processed OK')

        # build the state-level report object that will include all of the counties
        stateReport = state_report.StateReport(STATE, STATE_ABBR, parishes, datetime.datetime.now())
        
        # return the state-level report
        return stateReport        

    else:
        # Fail
        print(' ', STATE_ABBR, ': ERROR : Web download failed - HTTP status code ', response.status_code)

def findParish(parish_name, parishesDictionary):
    if parish_name in parishesDictionary:
        return parishesDictionary[parish_name]
    else:
        return None