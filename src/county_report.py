class CountyReport:
    state = ''
    county = ''
    confirmed = -1
    deaths = -1
    hospitalizations = -1
    caserate = -1
    timestamp = ''
    
    def __init__(self, state, county, confirmed, deaths, hospitalizations, caserate, timestamp):
        self.state = state
        self.county = county
        self.confirmed = confirmed
        self.deaths = deaths
        self.hospitalizations = hospitalizations
        self.caserate = caserate
        self.timestamp = timestamp