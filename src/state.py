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

    service = departures[0]["service"]
    firstDepartureDestinations = loadDestinationsForDeparture(
        departures[0]["service_timetable"]["id"],service)

    #print (departures);
    print (firstDepartureDestinations);

    return departures, firstDepartureDestinations, stationName

class Station():
    def __init__(self):
        self.code = config.get("journey").get("departureStation")
        self.departures, self.firstDepartureDestinations, self.name = loadStation(config["transportApi"], config["journey"])

class Departure():
    def __init__(self):
        self.time = "0:0"

class Service():
    def __init__(self):
        self.time = "0:0"



