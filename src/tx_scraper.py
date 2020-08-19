import requests, openpyxl, io, csv, datetime, os, pathlib
import county_report, state_report

STATE_ABBR = 'TX'
STATE = 'Texas'
URL = 'https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyFatalityCountData.xlsx'

def scraper():
    # make an HTTP web request to get the MI XLSX file
    response = requests.get(URL)

    counties = []

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
        max_cols = sheet.max_column

        for i in range(4, max_rows):
            rowCount = str(i)

            county_name = sheet['A' + rowCount].value

            if county_name == 'Unknown' or county_name == 'Total' or len(county_name) == 0:
                break

            confirmed = sheet.cell(row=i, column=max_cols).value

            county = county_report.CountyReport(STATE, county_name, (int)(confirmed), -1, -1, -1, datetime.datetime.now())
            counties.append(county)

        # print the number of counties we processed
        print(' ', STATE_ABBR, ':', len(counties), ' counties processed OK')

        # build the state-level report object that will include all of the counties
        stateReport = state_report.StateReport(STATE, STATE_ABBR, counties, datetime.datetime.now())
        
        # return the state-level report
        return stateReport
        

    else:
        # Fail
        print(' ', STATE_ABBR, ': ERROR : Web download failed - HTTP status code ', response.status_code)