# COVID-19 County-level Web Scraper Project

I created this project because we seem absent a way to transparently determine county-level counts of confirmed cases, deaths, and hospitalizations. Publicly-available data from the U.S. state health departments is used as input.

## States/territories supported as of 8/18/2020

- [x] Alabama
- [x] Alaska
- [ ] Arizona
- [x] Arkansas
- [x] California
- [x] Colorado
- [x] Connecticut
- [x] Delaware
- [x] Florida
- [x] Georgia
- [ ] Hawaii
- [x] Idaho
- [x] Illinois
- [x] Indiana
- [ ] Iowa
- [ ] Kansas
- [ ] Kentucky
- [x] Louisiana
- [ ] Maine
- [ ] Maryland
- [ ] Massachusetts
- [x] Michigan
- [x] Minnesota
- [x] Mississippi
- [x] Missouri
- [x] Montana
- [x] Nebraska
- [x] Nevada
- [ ] New Hampshire
- [ ] New Jersey
- [x] New Mexico
- [x] New York City
- [ ] New York (excluding NYC)
- [x] North Carolina
- [ ] North Dakota
- [x] Ohio
- [x] Oklahoma
- [ ] Oregon
- [ ] Pennsylvania
- [ ] Rhode Island
- [x] South Carolina
- [ ] South Dakota
- [x] Tennessee
- [x] Texas
- [ ] Utah
- [x] Vermont
- [x] Virginia
- [ ] Washington
- [ ] West Virginia
- [x] Wisconsin
- [ ] Wyoming
- [ ] American Samoa
- [ ] District of Columbia
- [ ] Guam
- [ ] Northern Mariana Islands
- [ ] U.S. Virgin Islands
- [ ] Puerto Rico
- [ ] Palau
- [ ] Federated States of Micronesia
- [ ] Republic of Marshall Islands 
- [ ] Navajo Nation

## Breakages

In the roughly 16 hours of development time that it took me to write and test these algorithms, three feeds from U.S. state health departments changed slightly. Even these slight changes caused those states to not generate output. Rework of their respective scraping algorithms was required.

It is likely that continuous development work will be required to keep the scraper project up-to-date for use in daily reporting.

## Missing data

Some states will never be represented in this project because county-level data is either not published by those states or it is too difficult to obtain with even advanced web scraping techniques.

## Running the code yourself

Install Python 3 and then use `pip` to install the following packages:

```bash
pip install openpyxl
pip install bs4
pip install selenium
```

Some states' data is only accessible by using web browser automation. As such, you will need to install a web driver for the scraping operation before you can run the Python code. You first need to install the new Microsoft Edge browser for Windows 10: https://www.microsoft.com/en-us/edge. Note that Edge may already be installed.

Once installed, you will then need to find the version number of Edge. You can do this by opening Edge and clicking the ellipsis button at the top right of the screen. Select **Help and Feedback** > **About Microsoft Edge**. Note the version number in the **About** page that appears.

Next, modify the Edge webdriver URL found in the `installEdgeDriver` function of `main.py`. You'll want to modify this URL to match the version you just saw in the Edge **About** page. Visit https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ to find a valid URL that matches your version of Edge. Copy and paste the URL from that page into the Python code. Generally, as long as the major version number is the same between the **About** page and what's listed on the [Microsoft webdriver website](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/), it'll probably work.

> Edge is updated every few weeks, so changing the Python URL to match your Edge version is likely going to be required on a periodic basis.

Finally, navigate to the `src` folder and run `main.py`:

```bash
cd src
python main.py
```
Output should start to generate after a few seconds. Web browser windows will appear on occasion; please do not close the browser windows that appear or the scaping operation will fail.

Once the operation completes, please open the `src/output` folder to view a timestamped CSV file representing all county-level data for all states that were included in the scraping operation.

> On Ubuntu or other Linux-based OS distributions, you may need to use the `pip3` command instead of `pip` and `python3` instead of `python`.

> Because this scraping project relies on web drivers to deal with JavaScript-intense pages for a small subset of states, you will need to be running Windows and MS Edge to obtain a full CSV output. A long-term TODO is to use headless Firefox or Chromium so this will run on *nix-based distributions or on Windows Subsystem for Linux (WSL).

## Excluding states from the scraping operation

You can exclude states from the scraper by commenting them out in `main.py`. Any state scraper not included in the `scrapers` array will not be run.

## License
The repository utilizes code licensed under the terms of the Apache Software License and therefore is licensed under ASL v2 or later.

This source code in this repository is free: you can redistribute it and/or modify it under
the terms of the Apache Software License version 2, or (at your option) any later version.

This source code in this repository is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the Apache Software License for more details.

You should have received a copy of the Apache Software License along with this program. If not, see https://www.apache.org/licenses/LICENSE-2.0.html

The source code forked from other open source projects will inherit its license.