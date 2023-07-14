# Preamble
import json
import math
import os
from threading import Thread
import requests
from tqdm.auto import tqdm

# Import parameters
API = "ll"  # ll or lldev
API_VERSION = "2.2.0"
if os.path.exists("APIkey.txt"):
    print("Using API key from APIkey.txt")
    with open("APIkey.txt", "r") as f:
        API_key = f.read()
        f.close()
elif "LL2_API_KEY" in os.environ:
    print("Using API key from environment variable")
    API_key = os.environ["LL2_API_KEY"]
else:
    raise Exception("No API key found")
header = {"Authorization": "Token " + API_key}

# create data directory if it doesnt exist
os.makedirs("../data", exist_ok=True)


def import_ll2(path, data_name, endpoint, call_headers, api, api_version, limit, pos):
    count_url = f"https://{api}.thespacedevs.com/{api_version}/{endpoint}/?limit={limit}&mode=list"
    count_call = requests.get(count_url, headers=call_headers, timeout=1440).json()
    number_data = count_call["count"]
    number_calls = math.ceil(number_data / limit)
    data = []
    next_url = f"https://{api}.thespacedevs.com/{api_version}/{endpoint}/?limit={limit}&mode=detailed"
    for _ in tqdm(
        range(number_calls), desc=data_name, ncols=80, leave=False, position=pos
    ):
        call = requests.get(next_url, headers=call_headers, timeout=1440).json()
        data.extend(call["results"])
        next_url = call["next"]
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def import_all_data():
    print("Importing LL2 data...")

    # Define threads
    t_launches = Thread(
        target=import_ll2,
        args=(
            "data/Launches.json",
            "Launches",
            "launch",
            header,
            API,
            API_VERSION,
            80,
            0,
        ),
    )
    t_astronauts = Thread(
        target=import_ll2,
        args=(
            "data/Astronauts.json",
            "Astronauts",
            "astronaut",
            header,
            API,
            API_VERSION,
            20,
            1,
        ),
    )
    t_agencies = Thread(
        target=import_ll2,
        args=(
            "data/Agencies.json",
            "Agencies",
            "agencies",
            header,
            API,
            API_VERSION,
            100,
            2,
        ),
    )
    t_pads = Thread(
        target=import_ll2,
        args=("data/Pads.json", "Pads", "pad", header, API, API_VERSION, 100, 3),
    )
    t_orbits = Thread(
        target=import_ll2,
        args=(
            "data/Orbits.json",
            "Orbits",
            "config/orbit",
            header,
            API,
            API_VERSION,
            100,
            4,
        ),
    )
    t_statuses = Thread(
        target=import_ll2,
        args=(
            "data/Statuses.json",
            "Statuses",
            "config/launchstatus",
            header,
            API,
            API_VERSION,
            100,
            5,
        ),
    )
    t_locations = Thread(
        target=import_ll2,
        args=(
            "data/Locations.json",
            "Locations",
            "location",
            header,
            API,
            API_VERSION,
            100,
            6,
        ),
    )

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
    print("Successfully completed import.")
