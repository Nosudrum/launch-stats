# Preamble
import json
import pandas as pd
from datetime import datetime, timezone


# Import json data
def read_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data


# Import Data
Agencies = pd.read_json('data/Agencies.json')
Launches = pd.read_json('data/Launches.json', convert_dates=["net", "window_start", "window_end"])
Locations = pd.read_json('data/Locations.json')
Orbits = pd.read_json('data/Orbits.json')
Pads = pd.read_json('data/Pads.json')
Statuses = pd.read_json('data/Statuses.json')

# Processing
LaunchName = Launches["name"].to_frame()
LaunchStatus = pd.json_normalize(Launches["status"])
LaunchT0 = Launches["net"].to_frame()
LaunchLSP = pd.json_normalize(Launches["launch_service_provider"])
LaunchMission = pd.json_normalize(Launches.mission)
LaunchOrbit = LaunchMission["orbit.id"].to_frame()
LaunchPad = pd.json_normalize(Launches["pad"])
LaunchCountry = LaunchPad["location.country_code"].to_frame()
LaunchCountry_mask = (LaunchPad["location.id"] == 20) | (LaunchPad["location.id"] == 144) | (
        LaunchPad["location.id"] == 3)
LaunchCountry["location.country_code"].loc[LaunchCountry_mask] = LaunchLSP.country_code[LaunchCountry_mask]
LaunchCountry[LaunchCountry == 'KAZ'] = 'RUS'
LaunchCountry[LaunchCountry == 'GUF'] = 'FRA'
LaunchProgram = pd.json_normalize(Launches["program"])

# Intermediate data
PastLSPs = LaunchLSP[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastT0s = LaunchT0[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastCountries = LaunchCountry[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastName = LaunchName[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
