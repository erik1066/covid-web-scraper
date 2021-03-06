import csv, datetime, requests, zipfile, pathlib, os, logging, sys
import ak_scraper
import al_scraper
import ar_scraper
import ca_scraper
import co_scraper
import ct_scraper
import de_scraper
import fl_scraper
import ga_scraper
import id_scraper
import in_scraper
import il_scraper
import la_scraper
import mi_scraper
import mn_scraper
import ms_scraper
import mo_scraper
import mt_scraper
import ne_scraper
import nv_scraper
import nm_scraper
import nyc_scraper
import nc_scraper
import ok_scraper
import oh_scraper
import or_scraper
import sc_scraper
import tn_scraper
import tx_scraper
import ut_scraper
import va_scraper
import vt_scraper
import wa_scraper
import wi_scraper


def main():

    # Get current date/time and store it in a variable
    now = datetime.datetime.now()

    # First, create an /output folder that will store the final .csv containing all the counties
    outputpath = 'output' 
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    # Let's deterime what to call our logfile
    logfilename = now.strftime("%Y-%m-%d_%H%M%S") + '_logfile.txt'
    logfilepath = pathlib.Path.cwd().joinpath('output', logfilename)

    # Set up logging
    logging.basicConfig(level=logging.DEBUG, filename=logfilepath, filemode="a+",
        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info("Initialized")

    installEdgeDriver()
    installGeckoDriver()

    reports = []

    scrapers = addScrapers()

    for scraper in scrapers:
        try:
            logging.info(scraper.STATE_ABBR + " : Starting scrape operation")
            logging.info(scraper.STATE_ABBR + " : Source data: " + scraper.URL)
            print('Starting scrape for' , scraper.STATE, '...')
            report = scraper.scraper()
            print(scraper.STATE, ' report generated at ', report.timestamp)
            logging.info(scraper.STATE_ABBR + " : " + str(len(report.counties)) + " counties read")
            logging.info(scraper.STATE_ABBR + " : Completed scrape operation")
            reports.append(report)
        except Exception as e:
            logging.error(e)

    counties = []
    for report in reports:
        for county in report.counties:
            counties.append(county)

    # The following section writes the final CSV output containing all counties for all states

    # Determine the filename to use - we'll include a timestamp in the filename itself that explains when the file was generated by our Python 3 code
    filename = now.strftime("%Y-%m-%d_%H%M%S") + '.csv'
    filepath = pathlib.Path.cwd().joinpath('output', filename)

    # Write the state reports to a CSV file
    with open(filepath, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        for county in counties:
            writer.writerow([ county.state, county.county, county.confirmed, county.deaths, county.hospitalizations, county.timestamp ])

    logging.info("Wrote " + str(len(counties)) + " counties to " + filename)

def installEdgeDriver():
    driver_path = pathlib.Path("msedgedriver.exe")
    if driver_path.is_file():
        logging.info("Edge webdriver was already installed - skipping Edge webdriver download and extraction")
        pass
    else:
        try:
            response = requests.get('https://msedgedriver.azureedge.net/84.0.524.0/edgedriver_win64.zip', stream=True)

            save_path = pathlib.Path.cwd().joinpath('temp', 'edgedriver_win64.zip')
            with open(save_path, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=128):
                    fd.write(chunk)

            with zipfile.ZipFile(save_path, 'r') as zipObj:
                zipObj.extract('msedgedriver.exe', path=None, pwd=None)
        except Exception as e:
            logging.error(e)

def installGeckoDriver():
    # Note - I've experienced too many problems with Firefox (Gecko) webdriver to use it, but
    # I've kept the webdriver install steps documented in the event others wish to solve the
    # problems and have a Firefox-friendly way of going about the scraping jobs.
    driver_path = pathlib.Path("geckodriver.exe")
    if driver_path.is_file():
        logging.info("Gecko (Firefox) webdriver was already installed - skipping Gecko webdriver download and extraction")
        pass
    else:
        try:
            response = requests.get('https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-win64.zip', stream=True)

            save_path = pathlib.Path.cwd().joinpath('temp', 'geckodriver-v0.27.0-win64.zip')
            with open(save_path, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=128):
                    fd.write(chunk)

            with zipfile.ZipFile(save_path, 'r') as zipObj:
                zipObj.extract('geckodriver.exe', path=None, pwd=None)
        except Exception as e:
            logging.error(e)

def addScrapers():
    scrapers = []
    scrapers.append(ak_scraper)
    scrapers.append(al_scraper)
    scrapers.append(ar_scraper)
    scrapers.append(ca_scraper)
    scrapers.append(co_scraper)
    scrapers.append(ct_scraper)
    scrapers.append(de_scraper)
    scrapers.append(fl_scraper)
    scrapers.append(ga_scraper)
    scrapers.append(id_scraper)
    scrapers.append(in_scraper)
    scrapers.append(il_scraper)
    scrapers.append(la_scraper)
    scrapers.append(mi_scraper)
    scrapers.append(mn_scraper)
    scrapers.append(ms_scraper)
    scrapers.append(mo_scraper)
    scrapers.append(mt_scraper)
    scrapers.append(ne_scraper)
    scrapers.append(nv_scraper)
    scrapers.append(nm_scraper)
    scrapers.append(nyc_scraper)
    scrapers.append(nc_scraper)
    scrapers.append(oh_scraper)
    scrapers.append(ok_scraper)
    scrapers.append(or_scraper)
    scrapers.append(sc_scraper)
    scrapers.append(tn_scraper)
    scrapers.append(tx_scraper)
    scrapers.append(ut_scraper)
    scrapers.append(va_scraper)
    scrapers.append(vt_scraper)
    scrapers.append(wi_scraper)
    scrapers.append(wa_scraper)
    return scrapers



main()