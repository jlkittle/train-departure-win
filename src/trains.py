import os
import json
import requests

def loadDeparturesForStation(journeyConfig, appId, apiKey):
    if journeyConfig["departureStation"] == "":
        raise ValueError(
            "Please set the journey.departureStation property in config.json")

    if appId == "" or apiKey == "":
        raise ValueError(
            "Please complete the transportApi section of your config.json file")

    departureStation = journeyConfig["departureStation"]

    localStation = ".\\data\\station\\" + departureStation + ".json"

    if os.path.exists(localStation):
        print ("using cached station for " + departureStation)
        with open(localStation, 'r') as f:
            data = json.load(f)
    else:
        URL = f"http://transportapi.com/v3/uk/train/station/{departureStation}/live.json"

        PARAMS = {'app_id': appId,
                  'app_key': apiKey,
                  'calling_at': journeyConfig["destinationStation"]}

        r = requests.get(url=URL, params=PARAMS)
        data = r.json()

        if "error" in data:
           raise ValueError(data["error"])
        else:
            with open(localStation, "a") as f:
                json.dump(data,f)

    return data["departures"]["all"], data["station_name"]

def loadDestinationsForDeparture(timetableUrl,service):
    localService = ".\\data\\service\\" + service + ".json"

    if os.path.exists(localService):
        print ("using cached service for " + service)
        with open(localService, 'r') as f:
            data = json.load(f)
    else:
        r = requests.get(url=timetableUrl)
        data = r.json()
        if "error" in data:
            raise ValueError(data["error"])
        else:
            with open(localService, "a") as f:
                json.dump(data,f)

    return data #list(map(lambda x: x["station_name"], data["stops"]))[1:]
