import clr
SWF = clr.AddReference("System.Windows.Forms")
#print (SWF.Location)
import System.Windows.Forms as WinForms
from System.Drawing import Size, Point

import state
myStation = state.Station()

class App(WinForms.Form):
    """A simple hello world app that demonstrates the essentials of
       winforms programming and event-based programming in Python."""

    def __init__(self):
        self.Text = "UK Trains Win"
        self.AutoScaleBaseSize = Size(5, 13)
        self.ClientSize = Size(1600, 117)
        h = WinForms.SystemInformation.CaptionHeight
        self.MinimumSize = Size(500, (600 + h))

        # Create the button
        self.button = WinForms.Button()
        self.button.Location = Point(32, 540)
        self.button.Size = Size(100, 20)
        self.button.TabIndex = 2
        self.button.Text = "Refresh"

        # Register the event handler
        self.button.Click += self.button_Click

        self.departCount = WinForms.Label()
        self.departCount.Text = "departure count"
        self.departCount.Size = Size(400, 40)
        self.departCount.Location = Point(8, 12)

        # Create the text box
        self.textbox = WinForms.Label()
        self.textbox.Text = "train details should be here"
        self.textbox.TabIndex = 1
        self.textbox.Size = Size(1600, 400)
        self.textbox.Location = Point(16, 32)

        # Add the controls to the form
        self.AcceptButton = self.button
        self.Controls.Add(self.button)
        self.Controls.Add(self.textbox)
        self.Controls.Add(self.departCount)

    def button_Click(self, sender, args):
        print ("Click")
        refresh(self)
        #WinForms.MessageBox.Show("Need to Refresh from Server Here.")

    def run(self):
        WinForms.Application.Run(self)

def refresh(form):
    form.Text = "UK Trains Win @ " + myStation.name + " (" + myStation.code + ")"
    #print (departures)
    departures = myStation.departures

    if departures:
        departureCount = len(departures)
        form.departCount.Text = str(departureCount)
        form.textbox.Text = ""
        for nextDeparture in iter(departures):
                form.textbox.Text =  form.textbox.Text +"\nPlatform " + nextDeparture.platform + " @ " + nextDeparture.aimed_time + " from " + nextDeparture.origin_name + " to " + nextDeparture.destination_name
                fromStops = "   from "
                toStops = "       to "
                for stop in iter(nextDeparture.stops):
                    aimed_time = stop["aimed_departure_time"]
                    if not aimed_time:
                        aimed_time = stop["aimed_arrival_time"]
                    if aimed_time < nextDeparture.aimed_time:
                        fromStops = fromStops + " " + stop["station_code"] + "(" + aimed_time + ") "
                    else:
                        try:
                            if aimed_time > nextDeparture.aimed_time:
                               toStops = toStops + " " + stop["station_code"] + "(" + aimed_time + ") "
                        except:
                            print(nextDeparture.aimed_time + nextDeparture.platform + nextDeparture.origin_name)
                if fromStops.__contains__("("):
                    form.textbox.Text = form.textbox.Text + "\n" + fromStops
                if toStops.__contains__("("):
                    form.textbox.Text = form.textbox.Text + "\n" + toStops
    else:
        form.departCount.Text = "0"
        form.textbox.Text = "No current trains"

def main():
    form = App()
    print ("form created")
    app = WinForms.Application
    print ("app referenced")
    refresh(form)
    app.Run(form)

if __name__ == '__main__':
    main()
