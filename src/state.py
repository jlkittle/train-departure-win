import json
from trains import loadDeparturesForStation, loadDestinationsForDeparture

def loadConfig():
    with open('config.json', 'r') as jsonConfig:
        return json.load(jsonConfig)

config = loadConfig()
# print (config)

def loadStation(apiConfig, journeyConfig):
    departures, stationName = loadDeparturesForStation(
        journeyConfig, apiConfig["appId"], apiConfig["apiKey"])

    if len(departures) == 0:
        return False, False, stationName

    return departures, stationName

class Station():
    def __init__(self):
        self.code = config.get("journey").get("departureStation")
        departures, self.name = loadStation(config["transportApi"], config["journey"])
        self.departures = list()
        for departure in iter(departures):
            self.departures.append(Departure(departure,self.code))

class Departure():
    def __init__(self,departure,stationCode):
        self.platform = departure["platform"]
        if not(self.platform):
            self.platform = "?"

        service = departure["service"]
        serviceData = loadDestinationsForDeparture(
            departure["service_timetable"]["id"], service)
        self.stops = serviceData["stops"]

        self.aimed_time = departure["aimed_departure_time"]
        self.origin_name = departure["origin_name"]
        self.destination_name = departure["destination_name"]

