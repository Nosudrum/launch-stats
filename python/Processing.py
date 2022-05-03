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
# Astronauts.loc[:, 'time_in_space'] = timedelta(0)
# for astronaut in Astronauts["id"].to_list():
#     flights = pd.json_normalize(Astronauts[Astronauts["id"] == astronaut].flights.to_list()[0])
#     landings = pd.json_normalize(Astronauts[Astronauts["id"] == astronaut].landings.to_list()[0])
#     if flights.empty:
#         flights_ids = []
#     else:
#         flights_ids = flights["id"].to_list()
#     if landings.empty:
#         landings_ids = []
#         landings_launch_ids = []
#     else:
#         landings_ids = landings["id"].to_list()
#         landings_launch_ids = landings["launch.id"].to_list()
#
#     time_in_space = timedelta(0)
#
#     for launch_id in list(set(flights_ids) - set(landings_launch_ids)):
#         launch_id_net = datetime.fromisoformat(flights[flights["id"] == launch_id]["net"].item()[:-1]).replace(
#             tzinfo=timezone.utc)
#         if launch_id_net < datetime.now(timezone.utc):
#             time_in_space += datetime.now(timezone.utc) - launch_id_net
#
#     for landing_id in landings_ids:
#         landing_id_mission_end = landings[landings["id"] == landing_id]["mission_end"]
#         landing_id_launch_net = landings[landings["id"] == landing_id]["launch.net"]
#         landing_id_launch_net = datetime.fromisoformat(landing_id_launch_net.item()[:-1]).replace(tzinfo=timezone.utc)
#         if landing_id_mission_end.item() is not None:
#             landing_id_mission_end = datetime.fromisoformat(landing_id_mission_end.item()[:-1]).replace(
#                 tzinfo=timezone.utc)
#             if landing_id_mission_end < datetime.now(timezone.utc):
#                 time_in_space += landing_id_mission_end - landing_id_launch_net
#             else:
#                 time_in_space += datetime.now(timezone.utc) - landing_id_launch_net
#         else:
#             time_in_space += datetime.now(timezone.utc) - landing_id_launch_net
#
#     Astronauts.loc[Astronauts["id"] == astronaut, "time_in_space"] = time_in_space
