# Preamble
import json
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import calendar


# Import json data
def import_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data


# Import Data
Agencies = import_json('data/Agencies.json')
Launches = import_json('data/Launches.json')
Locations = import_json('data/Locations.json')
Orbits = import_json('data/Orbits.json')
Pads = import_json('data/Pads.json')
Statuses = import_json('data/Statuses.json')

# Process Launch Data
NumberOfLaunches = len(Launches)
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


# Functions for figures
def dark_figure():
    fig = plt.figure(facecolor='black', figsize=(7, 5))
    f = plt.gca()
    for i in f.spines:
        f.spines[i].set_color('white')
    f.tick_params(axis='x', colors='white', which='both')
    f.tick_params(axis='y', colors='white', which='both')
    f.yaxis.label.set_color('white')
    f.xaxis.label.set_color('white')
    f.title.set_color('white')
    f.set_facecolor('black')
    return f, fig


def flatten(list_of_lists):
    flattened_list = []
    for i in list_of_lists:
        if isinstance(i, list):
            flattened_list += i
        else:
            flattened_list.append(i)
    return flattened_list


# Figures

# Plot of launch sites
dark_figure()

F0 = plt.axes(projection=ccrs.EckertIII())
F0.set_global()
for Location in enumerate(LocsName):
    if LocsLaunchCount[Location[0]] != 0:
        F0.plot(float(LocsLon[Location[0]]), float(LocsLat[Location[0]]), marker='o', color='red',
                markersize=max(LocsLaunchCount[Location[0]] / max(LocsLaunchCount) * 20, 1), transform=ccrs.Geodetic())
F0.stock_img()
plt.savefig('plots/test1.png', transparent=True, dpi=300)
plt.savefig('plots/test1.pdf', transparent=True, dpi=300)
plt.show()

# Plot of orbital launch attempts per country since 1957 stacked
F1_Countries = [['RUS', 'KAZ'], 'USA', 'CHN', ['FRA', 'GUF'], 'JPN', 'IND', 'NZL']
F1_Countries_Flatten = flatten(F1_Countries)
F1_Countries_Labels = ['Russia/USSR', 'USA', 'China', 'France', 'Japan', 'India', 'New Zealand', 'Others']
colors = {'red': '#e41a1c', 'orange': '#ff7f00', 'blue': '#377eb8', 'pink': '#f781bf', 'yellow': '#dede00',
          'green': '#4daf4a', 'grey': '#999999', 'purple': '#984ea3'}
F1_colors = ['blue', 'orange', 'red', 'green', 'pink', 'yellow', 'purple', 'grey']
F1_colors = [colors[i] for i in F1_colors]
F1_Years = [i.year for i in LaunchT0 if i < datetime.now(timezone.utc).replace(tzinfo=None)]
dark_figure()
F1_data = []
for ii in F1_Countries:
    if isinstance(ii, list):
        tmp = []
        for jj in ii:
            tmp += [i[1].year for i in enumerate(LaunchT0) if
                    i[1] < datetime.now(timezone.utc).replace(tzinfo=None) and LaunchOrbit[i[0]] != 15 and
                    LaunchCountry[
                        i[0]] == jj]
        F1_data.append(tmp)
    else:
        F1_data.append([i[1].year for i in enumerate(LaunchT0) if
                        i[1] < datetime.now(timezone.utc).replace(tzinfo=None) and LaunchOrbit[i[0]] != 15 and
                        LaunchCountry[
                            i[0]] == ii])
F1_data.append([i[1].year for i in enumerate(LaunchT0) if
                i[1] < datetime.now(timezone.utc).replace(tzinfo=None) and LaunchOrbit[i[0]] != 15 and
                LaunchCountry[
                    i[0]] not in F1_Countries_Flatten])
plt.hist(F1_data, bins=np.append(np.unique(F1_Years), max(F1_Years) + 1), histtype='bar', stacked=True,
         label=F1_Countries_Labels, color=F1_colors)
handles, labels = plt.gca().get_legend_handles_labels()
handles = [k for j in [handles[i::4] for i in range(4)] for k in j]
labels = [k for j in [labels[i::4] for i in range(4)] for k in j]
plt.legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
plt.ylabel('Total launches per year')
plt.ylim([0, 180])
plt.xlim([min(F1_Years), max(F1_Years) + 1])
plt.title('Orbital launch attempts per country since ' + str(min(F1_Years)))
plt.savefig('plots/OrbitalAttemptsPerCountryStacked.png', transparent=True, dpi=300)
plt.savefig('plots/OrbitalAttemptsPerCountryStacked.pdf', transparent=True, dpi=300)
plt.show()

# Plot of orbital launch attempts per country since 1957 non stacked
dark_figure()
plt.hist(F1_data, bins=np.append(np.unique(F1_Years), max(F1_Years) + 1), histtype='step', stacked=False,
         label=F1_Countries_Labels, color=F1_colors, linewidth=2)
handles, labels = plt.gca().get_legend_handles_labels()
handles = [k for j in [handles[i::4] for i in range(4)] for k in j]
labels = [k for j in [labels[i::4] for i in range(4)] for k in j]
plt.legend(handles[::-1], labels[::-1], loc='upper center', ncol=4, frameon=False, labelcolor='white')
plt.ylabel('Launches per year')
plt.ylim([0, 130])
plt.xlim([min(F1_Years), max(F1_Years) + 1])
plt.title('Orbital launch attempts per country since ' + str(min(F1_Years)))
plt.savefig('plots/OrbitalAttemptsPerCountry.png', transparent=True, dpi=300)
plt.savefig('plots/OrbitalAttemptsPerCountry.pdf', transparent=True, dpi=300)
plt.show()

# Plot of orbital launch attempts per country per year since 1957
monthsLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
for year in range(1957, datetime.now(timezone.utc).year + 1):
    days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
    dark_figure()
    F1y_data = []
    for ii in F1_Countries:
        if isinstance(ii, list):
            tmp = []
            for jj in ii:
                tmp += [i[1].timetuple().tm_yday for i in enumerate(LaunchT0) if
                        i[1].year == year and LaunchOrbit[i[0]] != 15 and LaunchCountry[i[0]] == jj and i[
                            1] < datetime.now(timezone.utc).replace(tzinfo=None)]
            F1y_data.append(tmp)
        else:
            F1y_data.append([i[1].timetuple().tm_yday for i in enumerate(LaunchT0) if
                             i[1].year == year and LaunchOrbit[i[0]] != 15 and LaunchCountry[i[0]] == ii and i[
                                 1] < datetime.now(timezone.utc).replace(tzinfo=None)])
    F1y_data.append([i[1].timetuple().tm_yday for i in enumerate(LaunchT0) if
                     i[1].year == year and LaunchOrbit[i[0]] != 15 and LaunchCountry[
                         i[0]] not in F1_Countries_Flatten and i[1] < datetime.now(timezone.utc).replace(tzinfo=None)])
    plt.hist(F1y_data, bins=np.append(days, max(days) + 1), histtype='step', cumulative=True, stacked=False,
             linewidth=2, label=F1_Countries_Labels, color=F1_colors)
    handles, labels = plt.gca().get_legend_handles_labels()
    handles = [k for j in [handles[i::4] for i in range(4)] for k in j]
    labels = [k for j in [labels[i::4] for i in range(4)] for k in j]
    plt.legend(handles[::-1], labels[::-1], loc='upper center', ncol=4, frameon=False,
               labelcolor='white')
    plt.xticks([datetime(year, i, 1).timetuple().tm_yday for i in range(1, 13)], monthsLabels)
    plt.ylabel('Cumulative number of launches')
    plt.ylim([0, max([len(x) for x in F1y_data]) * 1.2])
    plt.xlim([1, max(days)])
    plt.title('Orbital launch attempts per country in ' + str(year))
    plt.savefig('plots/yearly/orbitalAttemptsPerCountryStacked/' + str(year) + '.png', transparent=True, dpi=300)
    plt.savefig('plots/yearly/orbitalAttemptsPerCountryStacked/' + str(year) + '.svg', transparent=True, dpi=300)
    plt.close()
