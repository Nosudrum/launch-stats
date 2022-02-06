# Preamble
from datetime import datetime, timezone, timedelta
from Processing import LaunchT0, LaunchName, LaunchOrbit

# What the following code does :
# - Find how many times there was more than 3 launches in 48 hours
# - Find the record for most launches in 48 hours
# - Count how many times it happened
# - Return the latest occurrence
counter_allLSP = 0
nb_launches_next48 = []
max_launches_next48 = []
max_launches_next48_Name = []
max_launches_next48_T0 = []
counter = 0

# Get indices of past orbital launches and use them to filter LaunchT0 and LaunchName
Launch_indices = [i for i in range(0, len(LaunchT0)) if
                  LaunchT0[i] <= datetime.now(timezone.utc).replace(tzinfo=None) and LaunchOrbit[i] != 15]
LaunchT0 = [LaunchT0[i] for i in Launch_indices]
LaunchName = [LaunchName[i] for i in Launch_indices]

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
    nb_launches_next48.append(temp)
    if temp >= max(nb_launches_next48):
        max_launches_next48_Name = LaunchName_48hours
        max_launches_next48_T0 = LaunchT0_48hours
    if temp == 4:
        counter += 1
max_timedelta = max_launches_next48_T0[-1] - max_launches_next48_T0[0]

print(str(counter_allLSP))
print(str(max(nb_launches_next48) + 1))
print(str(counter))
print(max_launches_next48_Name)
print(max_launches_next48_T0)
print(max_timedelta.total_seconds() / 3600)
