# Preamble
import json
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np


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
NumberOfLaunches = len(Locations)
LocsName = []
LocsLat = []
LocsLong = []
LocsLaunchCount = []

for Location in Locations:
    LocsName.append(Location['name'])
    LocsLaunchCount.append(Location['total_launch_count'])
    if Location['pads']:
        LocsLat.append(Location['pads'][0]['latitude'])
        LocsLong.append(Location['pads'][0]['longitude'])
    else:
        LocsLat.append(None)
        LocsLong.append(None)


# Figures
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
    return f


# figure
# geobubble(LocsLat,LocsLong,LocsLaunchCount,'BubbleColorList',[1 0 0])
# geobasemap('satellite')


plt.figure()
F1_Years = [i.year for i in LaunchT0 if i < datetime.now(timezone.utc).replace(tzinfo=None)]

plt.hist(F1_Years, bins=np.unique(F1_Years))
plt.xlabel('Year')
plt.ylabel('# of launches')
plt.ylim([0, 170])
plt.title('All launches attempts')
plt.savefig('plots/test1.png', transparent=True, dpi=300)
plt.savefig('plots/test1.pdf', transparent=True, dpi=300)
plt.show()

plt.figure()
F2_Years = [i[1].year for i in enumerate(LaunchT0) if
            i[1] < datetime.now(timezone.utc).replace(tzinfo=None) and LaunchOrbit[i[0]] != 15]
plt.hist(F2_Years, bins=np.unique(F2_Years), alpha=0.5)
plt.xlabel('Year')
plt.ylabel('# of launches')
plt.ylim([0, 170])
plt.title('Orbital attempts')
plt.savefig('plots/test2.png', transparent=True, dpi=300)
plt.savefig('plots/test2.pdf', transparent=True, dpi=300)
plt.show()

F4_Countries = ['USA', ['RUS', 'KAZ'], ['FRA', 'GUF'], 'CHN', 'JPN', 'IND', 'NZL']
F4_Countries_Flatten = []
for i in F4_Countries:
    if isinstance(i, list):
        F4_Countries_Flatten += i
    else:
        F4_Countries_Flatten.append(i)
F4_Countries_Labels = ['USA', 'Russia/USSR', 'France', 'China', 'Japan', 'India', 'New Zealand', 'Others']
F4_Years = [i.year for i in LaunchT0 if i < datetime.now(timezone.utc).replace(tzinfo=None)]
F4 = dark_figure()
F4_data = []
for ii in F4_Countries:
    if isinstance(ii, list):
        tmp = []
        for jj in ii:
            tmp += [i[1].year for i in enumerate(LaunchT0) if
                    i[1] < datetime.now(timezone.utc).replace(tzinfo=None) and LaunchOrbit[i[0]] != 15 and
                    LaunchCountry[
                        i[0]] == jj]
        F4_data.append(tmp)
    else:
        F4_data.append([i[1].year for i in enumerate(LaunchT0) if
                        i[1] < datetime.now(timezone.utc).replace(tzinfo=None) and LaunchOrbit[i[0]] != 15 and
                        LaunchCountry[
                            i[0]] == ii])
F4_data.append([i[1].year for i in enumerate(LaunchT0) if
                i[1] < datetime.now(timezone.utc).replace(tzinfo=None) and LaunchOrbit[i[0]] != 15 and
                LaunchCountry[
                    i[0]] not in F4_Countries_Flatten])
plt.hist(F4_data, bins=np.unique(F4_Years), histtype='bar', stacked=True)

plt.legend(F4_Countries_Labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
# legend = plt.legend(frameon=1)
# frame = legend.get_frame()
# frame.set_facecolor('black')
# frame.set_edgecolor('white')
plt.xlabel('Year')
plt.ylabel('# of launches')
plt.ylim([0, 180])
plt.xlim([min(F4_Years), max(F4_Years)])
plt.title('Orbital launch attempts per country since ' + str(min(F4_Years)))
plt.savefig('plots/OrbitalAttemptsPerCountryStacked.png', transparent=True, dpi=300)
plt.savefig('plots/OrbitalAttemptsPerCountryStacked.pdf', transparent=True, dpi=300)
plt.show()

# plt.figure()
# plt.show()
# [N1,edges] = histcounts(year(LaunchT0((LaunchT0<datetime('now')).*(LaunchOrbit~=15).*(LaunchCountry=='RUS' | LaunchCountry=='KAZ')>=1)),min(year(LaunchT0(LaunchT0<datetime('now')))):(year(datetime('now'))+1));
# [N2,edges] = histcounts(year(LaunchT0((LaunchT0<datetime('now')).*(LaunchOrbit~=15).*(LaunchCountry=='USA')>=1)),min(year(LaunchT0(LaunchT0<datetime('now')))):(year(datetime('now'))+1));
# [N3,edges] = histcounts(year(LaunchT0((LaunchT0<datetime('now')).*(LaunchOrbit~=15).*(LaunchCountry=='CHN')>=1)),min(year(LaunchT0(LaunchT0<datetime('now')))):(year(datetime('now'))+1));
# [N4,edges] = histcounts(year(LaunchT0((LaunchT0<datetime('now')).*(LaunchOrbit~=15).*(LaunchCountry~='USA' & LaunchCountry~='RUS' & LaunchCountry~='KAZ' & LaunchCountry~='CHN')>=1)),min(year(LaunchT0(LaunchT0<datetime('now')))):(year(datetime('now'))+1));
# bar(edges(1:(end-1)),[N1',N2',N3',N4'],'stacked','EdgeColor','black','LineWidth',0.001)
# legend("USSR/Russia","USA","China","Others",'Location','southoutside','Orientation','horizontal')
# title('Orbital launch attempts per launch country since 1957')
# ylim([0 150])
# exportgraphics(gcf,'plots/OrbitalAttemptsPerCountry.pdf')
# exportgraphics(gcf,'plots/OrbitalAttemptsPerCountry.png','Resolution',300)
