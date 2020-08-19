class StateReport:
    state = ''
    stateAbbreviation = ''
    counties = []
    confirmed = -1
    deaths = -1
    hospitalizations = -1
    timestamp = ''
    
    def __init__(self, state, stateAbbreviation, counties, timestamp):
        self.state = state
        self.stateAbbreviation = stateAbbreviation
        self.counties = counties
        self.timestamp = timestamp

        self.confirmed = 0
        self.deaths = 0
        self.hospitalizations = 0

        for county in counties:
            self.confirmed += county.confirmed
            self.deaths += county.deaths
            self.hospitalizations += county.hospitalizations