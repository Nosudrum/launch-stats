# Preamble
from datetime import datetime
import json


# Import json data
def read_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data


# Import Data
Agencies = read_json('data/Agencies.json')
Launches = read_json('data/Launches.json')
Locations = read_json('data/Locations.json')
Orbits = read_json('data/Orbits.json')
Pads = read_json('data/Pads.json')
Statuses = read_json('data/Statuses.json')

# Process Launch Data
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
    loc_id = Launch['pad']['location']['id']
    if loc_id == 20 or loc_id == 144 or loc_id == 3:
        # Air launch to orbit, air launch to suborbital flight, sea launch
        LaunchCountry.append(Launch['launch_service_provider']['country_code'])
    else:
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
