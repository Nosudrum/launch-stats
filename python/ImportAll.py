# Preamble
import json
import math
import os

import requests
from tqdm import tqdm

# Import parameters
API = 'll'  # ll or lldev
API_version = '2.2.0'
with open('APIkey.txt', 'r') as f:
    API_key = f.read()
    f.close()
header = {'Authorization': 'Token ' + API_key}

# create data directory if it doesnt exist
os.makedirs("../data", exist_ok=True)


def ll2_call(data_name, endpoint, call_headers, api, api_version, limit):
    count_url = f'https://{api}.thespacedevs.com/{api_version}/{endpoint}/?limit={limit}&mode=list'
    count_call = requests.get(count_url, headers=call_headers, timeout=1440).json()
    number_data = count_call['count']
    number_calls = math.ceil(number_data / limit)
    data = []
    next_url = f'https://{api}.thespacedevs.com/{api_version}/{endpoint}/?limit={limit}&mode=detailed'
    for _ in tqdm(range(number_calls), desc=data_name, ncols=80):
        call = requests.get(next_url, headers=call_headers, timeout=1440).json()
        data.extend(call['results'])
        next_url = call['next']
    return data


def export(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)


print('Importing LL2 data...')

# Import Launches
export('data/Launches.json', ll2_call('Launches', 'launch', header, API, API_version, 80))

# Import Orbits
export('data/Orbits.json', ll2_call('Orbits', 'config/orbit', header, API, API_version, 100))

# Import Statuses
export('data/Statuses.json', ll2_call('Statuses', 'config/launchstatus', header, API, API_version, 100))

# Import Agencies
export('data/Agencies.json', ll2_call('Agencies', 'agencies', header, API, API_version, 100))

# Import Locations
export('data/Locations.json', ll2_call('Locations', 'location', header, API, API_version, 100))

# Import Pads
export('data/Pads.json', ll2_call('Pads', 'pad', header, API, API_version, 100))

# Import Astronauts
export('data/Astronauts.json', ll2_call('Astronauts', 'astronaut', header, API, API_version, 20))

print('Successfully completed import.')
