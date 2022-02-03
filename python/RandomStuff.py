# Preamble
import json
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs


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

for Launch in Launches:
    if Launch['mission'] is not None and Launch['mission']['orbit'] is not None and Launch['mission']['orbit'][
        'id'] == 15:
        continue
    elif datetime.fromisoformat(Launch['net'][:-1]) > datetime.now(timezone.utc).replace(tzinfo=None):
        continue
    elif Launch['mission'] is None or Launch['mission']['orbit'] is None:
        LaunchOrbit.append(-1)
    else:
        LaunchOrbit.append(Launch['mission']['orbit']['id'])
    LaunchName.append(Launch['name'])
    LaunchStatus.append(Launch['status']['id'])
    LaunchT0.append(datetime.fromisoformat(Launch['net'][:-1]))
    LaunchLSP.append(Launch['launch_service_provider']['id'])
    LaunchCountry.append(Launch['pad']['location']['country_code'])
    LaunchPad.append(Launch['pad']['id'])

# Process Locations Data
LocsName = []
LocsLat = []
LocsLon = []
LocsLaunchCount = []

for Location in Locations:
    if Location['id'] == 20 or Location['id'] == 144 or Location['id'] == 3:
        # Air launch to orbit, air launch to suborbital flight, sea launch
        for pad in Location['pads']:
            LocsName.append(pad['name'])
            LocsLat.append(pad['latitude'])
            LocsLon.append(pad['longitude'])
            LocsLaunchCount.append(pad['total_launch_count'])
    elif Location['id'] == 22:  # Unknown location
        break
    else:
        if Location['pads']:
            LocsLat.append(Location['pads'][0]['latitude'])
            LocsLon.append(Location['pads'][0]['longitude'])
            LocsName.append(Location['name'])
            LocsLaunchCount.append(Location['total_launch_count'])

# What the following code does :
# - Find how many times there was more than 3 launches in 48 hours
# - Find the record for most launches in 48 hours
# - Count how many times it happened
# - Return the latest occurrence
counter_allLSP = 0
nblaunches_next48 = []
maxlaunches_next48 = []
maxlaunches_next48_Name = []
maxlaunches_next48_T0 = []
counter = 0
for ii in range(0, len(LaunchT0) - 2):
    if LaunchT0[ii + 2] - LaunchT0[ii] <= timedelta(hours=48):
        counter_allLSP += 1
    LaunchName_48hours = []
    LaunchT0_48hours = []
    jj = 0
    while ii + jj < len(LaunchT0) and LaunchT0[ii + jj] - LaunchT0[ii] <= timedelta(hours=48):
        LaunchName_48hours.append(LaunchName[ii + jj])
        LaunchT0_48hours.append(LaunchT0[ii + jj])
        jj += 1
    temp = len(LaunchName_48hours) - 1
    nblaunches_next48.append(temp)
    if temp >= max(nblaunches_next48):
        maxlaunches_next48_Name = LaunchName_48hours
        maxlaunches_next48_T0 = LaunchT0_48hours
    if temp == 4:
        counter += 1
max_timedelta = maxlaunches_next48_T0[-1] - maxlaunches_next48_T0[0]

print(str(counter_allLSP))
print(str(max(nblaunches_next48) + 1))
print(str(counter))
print(maxlaunches_next48_Name)
print(maxlaunches_next48_T0)
print(max_timedelta.total_seconds() / 3600)
