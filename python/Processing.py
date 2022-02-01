# Preamble
import json
from datetime import datetime
import matplotlib.pyplot as plt

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
# figure
# geobubble(LocsLat,LocsLong,LocsLaunchCount,'BubbleColorList',[1 0 0])
# geobasemap('satellite')

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







