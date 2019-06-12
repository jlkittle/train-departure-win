import os
import sys
import time
import json
import clr

from trains import loadDeparturesForStation, loadDestinationsForDeparture

SWF = clr.AddReference("System.Windows.Forms")
#print (SWF.Location)
import System.Windows.Forms as WinForms
from System.Drawing import Size, Point

def loadConfig():
    with open('config.json', 'r') as jsonConfig:
        data = json.load(jsonConfig)
        return data

config = loadConfig()
# print (config)

def loadData(apiConfig, journeyConfig):
    departures, stationName = loadDeparturesForStation(
        journeyConfig, apiConfig["appId"], apiConfig["apiKey"])

    if len(departures) == 0:
        return False, False, stationName

    firstDepartureDestinations = loadDestinationsForDeparture(
        departures[0]["service_timetable"]["id"])

    #print (departures);
    #print (firstDepartureDestinations);

    return departures, firstDepartureDestinations, stationName

class HelloApp(WinForms.Form):
    """A simple hello world app that demonstrates the essentials of
       winforms programming and event-based programming in Python."""

    def __init__(self):
        self.Text = "UK Trains Win @ "
        self.AutoScaleBaseSize = Size(5, 13)
        self.ClientSize = Size(392, 117)
        h = WinForms.SystemInformation.CaptionHeight
        self.MinimumSize = Size(500, (117 + h))

        # Create the button
        self.button = WinForms.Button()
        self.button.Location = Point(16, 64)
        self.button.Size = Size(100, 20)
        self.button.TabIndex = 2
        self.button.Text = "Refresh"

        # Register the event handler
        self.button.Click += self.button_Click

        # Create the text box
        self.textbox = WinForms.TextBox()
        self.textbox.Text = "train details should be here"
        self.textbox.TabIndex = 1
        self.textbox.Size = Size(400, 40)
        self.textbox.Location = Point(16, 24)

        # Add the controls to the form
        self.AcceptButton = self.button
        self.Controls.Add(self.button)
        self.Controls.Add(self.textbox)

    def button_Click(self, sender, args):
        print ("Click")
        refresh(self, config)
        #WinForms.MessageBox.Show("Need to Refresh from Server Here.")

    def run(self):
        WinForms.Application.Run(self)

def refresh(form, config):
    departureStationCode = config.get("journey").get("departureStation")
    data = loadData(config["transportApi"], config["journey"])
    #print (data)
    departures, firstDepartureDestinations, departureStation = data
    form.Text = "UK Trains Win @ " + departureStation + " (" + departureStationCode + ")"
    #print (departures)

    try:
        nextDeparture = departures[0]
        #print (firstDepartureDestinations)
        #print (departureStation)
        form.textbox.Text =  "Platform " + nextDeparture.get("platform") + " @ " + nextDeparture.get("aimed_departure_time") + " from " + nextDeparture.get("origin_name") + " to " + nextDeparture.get("destination_name")
    except:
        form.textbox.Text = "No current trains"

def main():
    form = HelloApp()
    print ("form created")
    app = WinForms.Application
    print ("app referenced")
    refresh(form,config)
    app.Run(form)

if __name__ == '__main__':
    main()
