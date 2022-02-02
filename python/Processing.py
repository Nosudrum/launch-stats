# Preamble
import json
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np


# Import json data
def import_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data


# Import Data
Agencies = import_json('data/Agencies.json')
Launches = import_json('data/Launches.json')
Locations = import_json('data/Locations.json')
Orbits = import_json('data/Orbits.json')
Pads = import_json('data/Pads.json')
Statuses = import_json('data/Statuses.json')

# Process Launch Data
NumberOfLaunches = len(Launches)
LaunchName = []
LaunchStatus = []
LaunchT0 = []
LaunchLSP = []
LaunchCountry = []
LaunchOrbit = []
LaunchPad = []
LaunchProgram = []

for Launch in Launches:
    LaunchName.append(Launch['name'])
    LaunchStatus.append(Launch['status']['id'])
    LaunchT0.append(datetime.fromisoformat(Launch['net'][:-1]))
    LaunchLSP.append(Launch['launch_service_provider']['id'])
    LaunchCountry.append(Launch['pad']['location']['country_code'])
    LaunchPad.append(Launch['pad']['id'])
    if Launch['mission'] is not None and Launch['mission']['orbit'] is not None:
        LaunchOrbit.append(Launch['mission']['orbit']['id'])
    else:
        LaunchOrbit.append(-1)
    if Launch['program']:
        LaunchProgram.append([i['id'] for i in Launch['program']])
    else:
        LaunchProgram.append(-1)

# Process Locations Data
NumberOfLaunches = len(Locations)
LocsName = []
LocsLat = []
LocsLong = []
LocsLaunchCount = []

for Location in Locations:
    LocsName.append(Location['name'])
    LocsLaunchCount.append(Location['total_launch_count'])
    if Location['pads']:
        LocsLat.append(Location['pads'][0]['latitude'])
        LocsLong.append(Location['pads'][0]['longitude'])
    else:
        LocsLat.append(None)
        LocsLong.append(None)


# Figures
def dark_figure():
    plt.figure(facecolor='black', figsize=(7, 5))
    f = plt.gca()
    for i in f.spines:
        f.spines[i].set_color('white')
    f.tick_params(axis='x', colors='white', which='both')
    f.tick_params(axis='y', colors='white', which='both')
    f.yaxis.label.set_color('white')
    f.xaxis.label.set_color('white')
    f.title.set_color('white')
    f.set_facecolor('black')
    return f


# figure
# geobubble(LocsLat,LocsLong,LocsLaunchCount,'BubbleColorList',[1 0 0])
# geobasemap('satellite')

F1_Countries = [['RUS', 'KAZ'], 'USA', 'CHN', ['FRA', 'GUF'], 'JPN', 'IND', 'NZL']
F1_Countries_Flatten = []
for i in F1_Countries:
    if isinstance(i, list):
        F1_Countries_Flatten += i
    else:
        F1_Countries_Flatten.append(i)
F1_Countries_Labels = ['Russia/USSR', 'USA', 'China', 'France', 'Japan', 'India', 'New Zealand', 'Others']
F1_Years = [i.year for i in LaunchT0 if i < datetime.now(timezone.utc).replace(tzinfo=None)]
F1 = dark_figure()
F1_data = []
for ii in F1_Countries:
    if isinstance(ii, list):
        tmp = []
        for jj in ii:
            tmp += [i[1].year for i in enumerate(LaunchT0) if
                    i[1] < datetime.now(timezone.utc).replace(tzinfo=None) and LaunchOrbit[i[0]] != 15 and
                    LaunchCountry[
                        i[0]] == jj]
        F1_data.append(tmp)
    else:
        F1_data.append([i[1].year for i in enumerate(LaunchT0) if
                        i[1] < datetime.now(timezone.utc).replace(tzinfo=None) and LaunchOrbit[i[0]] != 15 and
                        LaunchCountry[
                            i[0]] == ii])
F1_data.append([i[1].year for i in enumerate(LaunchT0) if
                i[1] < datetime.now(timezone.utc).replace(tzinfo=None) and LaunchOrbit[i[0]] != 15 and
                LaunchCountry[
                    i[0]] not in F1_Countries_Flatten])
plt.hist(F1_data, bins=np.append(np.unique(F1_Years), max(F1_Years) + 1), histtype='bar', stacked=True)
plt.legend(F1_Countries_Labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
plt.xlabel('Year')
plt.ylabel('# of launches')
plt.ylim([0, 180])
plt.xlim([min(F1_Years), max(F1_Years) + 1])
plt.title('Orbital launch attempts per country since ' + str(min(F1_Years)))
plt.savefig('plots/OrbitalAttemptsPerCountryStacked.png', transparent=True, dpi=300)
plt.savefig('plots/OrbitalAttemptsPerCountryStacked.pdf', transparent=True, dpi=300)
plt.show()
