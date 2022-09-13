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
LaunchCountry[LaunchCountry == 'MHL'] = 'USA'
LaunchProgram = pd.json_normalize(Launches["program"])

# Intermediate launch data
PastLSPs = LaunchLSP[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastT0s = LaunchT0[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastCountries = LaunchCountry[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastName = LaunchName[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastStatus = LaunchStatus[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastPad = LaunchPad[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()

PastDayOfYear = PastT0s.copy()
PastDayOfYear.loc[~PastT0s.net.dt.is_leap_year & (
        PastT0s.net.dt.dayofyear >= 60), "net"] = PastT0s.net.dt.dayofyear + 1
PastDayOfYear.loc[PastT0s.net.dt.is_leap_year | (
        PastT0s.net.dt.dayofyear < 60), "net"] = PastT0s.net.dt.dayofyear

FutureLSPs = LaunchLSP[(LaunchT0["net"] > datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
FutureT0s = LaunchT0[(LaunchT0["net"] > datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
FutureCountries = LaunchCountry[(LaunchT0["net"] > datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
FutureName = LaunchName[(LaunchT0["net"] > datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
FutureStatus = LaunchStatus[(LaunchT0["net"] > datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
FuturePad = LaunchPad[(LaunchT0["net"] > datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()

# Processing astronaut data
AstronautsAgency = pd.json_normalize(Astronauts["agency"])
AstronautsType = pd.json_normalize(Astronauts["type"])

Astronauts.loc[:, 'time_in_space'] = timedelta(0)
Astronauts.loc[:, 'total_flights'] = 0
Astronauts.loc[:, 'total_landings'] = 0
Astronauts.loc[:, 'first_landing_mission_end'] = None
Astronauts.loc[:, 'last_landing_mission_end'] = None
Astronauts.loc[:, 'is_in_space'] = False
for astronaut in Astronauts["id"].to_list():
    flights = pd.json_normalize(Astronauts[Astronauts["id"] == astronaut].flights.to_list()[0])
    landings = pd.json_normalize(Astronauts[Astronauts["id"] == astronaut].landings.to_list()[0])

    if flights.empty:
        start_times = []
    else:
        # Remove Apollo 1
        flights = flights[flights.id != 'a49d791b-3c7f-4ee9-8917-14596a2a1a25'].reset_index()
        flights['net'] = pd.to_datetime(flights['net'], utc=True)
        flights = flights[flights.net < datetime.now(timezone.utc)]
        start_times = flights.net.to_list()
        start_times.sort()
    if landings.empty or landings.mission_end.count() == 0:
        end_times = []
    else:
        # Remove Apollo 1
        landings = landings[landings.id != '598'].reset_index()
        landings['mission_end'] = pd.to_datetime(landings['mission_end'], utc=True)
        landings = landings[landings.mission_end < datetime.now(timezone.utc)]
        end_times = landings.mission_end.to_list()
        end_times.sort()

    time_delta = timedelta(0)
    if (AstronautsAgency[Astronauts["id"] == astronaut]["id"].head(1).item() != 1024) and (
            AstronautsType[Astronauts["id"] == astronaut]["id"].head(1).item() != 6):  # Virgin Galactic & Non-Human
        for start in enumerate(start_times):
            start_time = start[1]
            if start_time > datetime.now(timezone.utc):
                continue
            if start[0] >= len(end_times):
                time_delta += datetime.now(timezone.utc) - start_time
                continue
            if end_times[start[0]]:
                end_time = end_times[start[0]]
                if end_time > datetime.now(timezone.utc):
                    time_delta += datetime.now(timezone.utc) - start_time
                    continue
                else:
                    time_delta += end_time - start_time
        Astronauts.loc[Astronauts["id"] == astronaut, "time_in_space"] = time_delta

    if len(flights) > 0:
        Astronauts.loc[Astronauts["id"] == astronaut, "total_flights"] = len(flights)
        Astronauts.loc[Astronauts["id"] == astronaut, "first_flight_net"] = flights.iloc[0].net
        Astronauts.loc[Astronauts["id"] == astronaut, "last_flight_net"] = flights.iloc[-1].net

    if len(landings) > 0:
        Astronauts.loc[Astronauts["id"] == astronaut, "total_landings"] = len(landings)
        if landings.iloc[0].mission_end:
            Astronauts.loc[Astronauts["id"] == astronaut, "first_landing_mission_end"] = landings.iloc[0].mission_end
        if landings.iloc[-1].mission_end:
            Astronauts.loc[Astronauts["id"] == astronaut, "last_landing_mission_end"] = landings.iloc[-1].mission_end

    if len(start_times) > 0:
        if (len(end_times) == 0) or (end_times[-1] < start_times[-1]):
            Astronauts.loc[Astronauts["id"] == astronaut, "is_in_space"] = True
