# Preamble
import json
import math
import os
from threading import Thread
import requests
from tqdm.auto import tqdm

# Import parameters
API = 'll'  # ll or lldev
API_version = '2.2.0'
with open('APIkey.txt', 'r') as f:
    API_key = f.read()
    f.close()
header = {'Authorization': 'Token ' + API_key}

# create data directory if it doesnt exist
os.makedirs("../data", exist_ok=True)


def import_ll2(path, data_name, endpoint, call_headers, api, api_version, limit, pos):
    count_url = f'https://{api}.thespacedevs.com/{api_version}/{endpoint}/?limit={limit}&mode=list'
    count_call = requests.get(count_url, headers=call_headers, timeout=1440).json()
    number_data = count_call['count']
    number_calls = math.ceil(number_data / limit)
    data = []
    next_url = f'https://{api}.thespacedevs.com/{api_version}/{endpoint}/?limit={limit}&mode=detailed'
    for _ in tqdm(range(number_calls), desc=data_name, ncols=80, leave=False, position=pos):
        call = requests.get(next_url, headers=call_headers, timeout=1440).json()
        data.extend(call['results'])
        next_url = call['next']
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)


print('Importing LL2 data...')

# Define threads
t_launches = Thread(target=import_ll2,
                    args=('data/Launches.json', 'Launches', 'launch', header, API, API_version, 80, 0))
t_astronauts = Thread(target=import_ll2,
                      args=('data/Astronauts.json', 'Astronauts', 'astronaut', header, API, API_version, 20, 1))
t_agencies = Thread(target=import_ll2,
                    args=('data/Agencies.json', 'Agencies', 'agencies', header, API, API_version, 100, 2))
t_pads = Thread(target=import_ll2,
                args=('data/Pads.json', 'Pads', 'pad', header, API, API_version, 100, 3))
t_orbits = Thread(target=import_ll2,
                  args=('data/Orbits.json', 'Orbits', 'config/orbit', header, API, API_version, 100, 4))
t_statuses = Thread(target=import_ll2,
                    args=('data/Statuses.json', 'Statuses', 'config/launchstatus', header, API, API_version, 100, 5))
t_locations = Thread(target=import_ll2,
                     args=('data/Locations.json', 'Locations', 'location', header, API, API_version, 100, 6))

# Start threads
t_launches.start()
t_astronauts.start()
t_agencies.start()
t_pads.start()
t_orbits.start()
t_statuses.start()
t_locations.start()

# Wait for threads to finish
t_launches.join()
print('Successfully completed import.')
