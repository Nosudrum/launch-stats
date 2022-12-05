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
Rocket = pd.json_normalize(Launches["rocket"])
FirstStage = pd.json_normalize(Rocket["launcher_stage"])
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

FirstStageReuse = pd.DataFrame(columns=['NewLost', 'NewRecovered', 'ReusedLost', 'ReusedRecovered'],
                               index=Launches.index)
for i in range(len(FirstStage)):
    new_not_recovered = 0
    new_recovered = 0
    not_new_not_recovered = 0
    not_new_recovered = 0
    has_first_stage = False
    for j in range(len(FirstStage.iloc[i])):
        if FirstStage.iloc[i][j] is not None:
            has_first_stage = True
            if FirstStage.iloc[i][j]['reused'] is True:
                reused = True
            elif FirstStage.iloc[i][j]['reused'] is False:
                reused = False
            else:
                continue
            if "landing.attempt" in FirstStage.iloc[i][j]:
                if FirstStage.iloc[i][j]['landing.attempt'] is True:
                    if 'landing.type.id' in FirstStage.iloc[i][j] and FirstStage.iloc[i][j]['landing.type.id'] == 3:
                        # Ocean
                        recovered = False
                    elif FirstStage.iloc[i][j]['landing.success'] is True:
                        recovered = True
                    elif FirstStage.iloc[i][j]['landing.success'] is False:
                        recovered = False
                    else:
                        if LaunchT0.iloc[i][0] <= datetime.now(timezone.utc):
                            print(f"WARNING : Missing landing outcome for launch {LaunchName.iloc[i][0]}")
                        continue
                else:
                    recovered = False
            else:
                if LaunchT0.iloc[i][0] <= datetime.now(timezone.utc):
                    print(f"WARNING : Missing landing data for launch {LaunchName.iloc[i][0]}")
                continue
            if not reused and not recovered:
                new_not_recovered += 1
            elif not reused and recovered:
                new_recovered += 1
            elif reused and not recovered:
                not_new_not_recovered += 1
            elif reused and recovered:
                not_new_recovered += 1
    if not has_first_stage:
        new_not_recovered = 1
    FirstStageReuse.iloc[i] = [new_not_recovered, new_recovered, not_new_not_recovered, not_new_recovered]

# Intermediate launch data
past_filter = (LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)

PastLSPs = LaunchLSP[past_filter].copy()
PastT0s = LaunchT0[past_filter].copy()
PastCountries = LaunchCountry[past_filter].copy()
PastName = LaunchName[past_filter].copy()
PastStatus = LaunchStatus[past_filter].copy()
PastPad = LaunchPad[past_filter].copy()
PastRocket = Rocket[past_filter].copy()
PastFirstStage = FirstStage[past_filter].copy()
PastFirstStageReuse = FirstStageReuse[past_filter].copy()

PastDayOfYear = PastT0s.copy()
PastDayOfYear.loc[~PastT0s.net.dt.is_leap_year & (
        PastT0s.net.dt.dayofyear >= 60), "net"] = PastT0s.net.dt.dayofyear + 1
PastDayOfYear.loc[PastT0s.net.dt.is_leap_year | (
        PastT0s.net.dt.dayofyear < 60), "net"] = PastT0s.net.dt.dayofyear

future_filter = (LaunchT0["net"] > datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)
FutureLSPs = LaunchLSP[future_filter].copy()
FutureT0s = LaunchT0[future_filter].copy()
FutureCountries = LaunchCountry[future_filter].copy()
FutureName = LaunchName[future_filter].copy()
FutureStatus = LaunchStatus[future_filter].copy()
FuturePad = LaunchPad[future_filter].copy()
FutureRocket = Rocket[future_filter].copy()

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
