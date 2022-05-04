# Preamble
import json
import pandas as pd
from datetime import datetime, timezone, timedelta


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
Astronauts = pd.read_json('data/Astronauts.json')

# Remove unwanted data
# Apollo 1
Launches = Launches[Launches.id != 'a49d791b-3c7f-4ee9-8917-14596a2a1a25'].reset_index()

# Processing launch data
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

# Intermediate launch data
PastLSPs = LaunchLSP[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastT0s = LaunchT0[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastCountries = LaunchCountry[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastName = LaunchName[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()

# Processing astronaut data
AstronautsAgency = pd.json_normalize(Astronauts["agency"])
AstronautsType = pd.json_normalize(Astronauts["type"])

Astronauts.loc[:, 'time_in_space'] = timedelta(0)
for astronaut in Astronauts["id"].to_list():
    if AstronautsAgency[Astronauts["id"] == astronaut]["id"].item() == 1024:  # Virgin Galactic
        continue
    if AstronautsType[Astronauts["id"] == astronaut]["id"].item() == 6:  # Non-Human
        continue
    flights = pd.json_normalize(Astronauts[Astronauts["id"] == astronaut].flights.to_list()[0])
    landings = pd.json_normalize(Astronauts[Astronauts["id"] == astronaut].landings.to_list()[0])

    if flights.empty:
        # flights_ids = []
        start_times = []
    else:
        # Remove Apollo 1
        flights = flights[flights.id != 'a49d791b-3c7f-4ee9-8917-14596a2a1a25'].reset_index()
        # flights_ids = flights["id"].to_list()
        start_times = flights["net"].to_list()

    if landings.empty:
        # landings_ids = []
        # landings_launch_ids = []
        end_times = []
    else:
        # Remove Apollo 1
        landings = landings[landings.id != '598'].reset_index()
        # landings_ids = landings["id"].to_list()
        # landings_launch_ids = landings["launch.id"].to_list()
        end_times = landings["mission_end"].to_list()

    time_delta = timedelta(0)
    for start in enumerate(start_times):

        start_time = datetime.fromisoformat(start[1][:-1]).replace(tzinfo=timezone.utc)
        if start_time > datetime.now(timezone.utc):
            continue
        if start[0] >= len(end_times):
            time_delta += datetime.now(timezone.utc) - start_time
            continue
        if end_times[start[0]]:
            end_time = datetime.fromisoformat(end_times[start[0]][:-1]).replace(tzinfo=timezone.utc)
            if end_time > datetime.now(timezone.utc):
                time_delta += datetime.now(timezone.utc) - start_time
                continue
            else:
                time_delta += end_time - start_time
    Astronauts.loc[Astronauts["id"] == astronaut, "time_in_space"] = time_delta
