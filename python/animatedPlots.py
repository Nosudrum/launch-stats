# Preamble
import numpy as np
from datetime import datetime, timezone, timedelta
from Processing import LaunchT0, LaunchName, LaunchOrbit, LaunchCountry
import pycountry

country_names = {'years': 'years', 'AUS': 'Australia', 'BRA': 'Brazil', 'CHN': 'China', 'FRA': 'France',
                 'GUF': 'French Guiana',
                 'IND': 'India', 'IRN': 'Iran', 'ISR': 'Israel', 'ITA': 'Italy', 'JPN': 'Japan', 'KAZ': 'Kazakhstan',
                 'KOR': 'South Korea', 'MHL': 'Marshall Islands', 'NZL': 'New Zealand', 'PRK': 'North Korea',
                 'RUS': 'Russia', 'UNK': 'Unknown', 'USA': 'United States'}

years = np.unique([i.year for i in LaunchT0 if i < datetime.now(timezone.utc).replace(tzinfo=None)])
data = {'years': years.tolist()}
for country in np.unique(LaunchCountry):
    print(country)
    data[country] = []
    nb = 0
    for year in years:
        nb += len([i[0] for i in enumerate(LaunchT0) if
                   LaunchT0[i[0]].year == year and LaunchCountry[i[0]] == country and LaunchOrbit[i[0]] != 15 and
                   LaunchT0[i[0]] < datetime.now(timezone.utc).replace(tzinfo=None)])
        data[country].append(nb)

data['RUS'] = np.add(data['RUS'], data['KAZ']).tolist()
del data['KAZ']
data['USA'] = np.add(data['USA'], data['MHL']).tolist()
del data['MHL']
data['FRA'] = np.add(data['FRA'], data['GUF']).tolist()
del data['GUF']
del data['UNK']

with open('data/animated.csv', 'w') as file:
    for key in data.keys():
        file.write("%s,%s\n" % (country_names[key], data[key]))
