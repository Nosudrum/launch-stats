# Preamble
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import calendar
from Processing import LaunchT0, LaunchOrbit, LaunchCountry, LocsName, LocsLaunchCount, LocsLat, LocsLon, LaunchLSP, \
    Agencies
from PIL import Image

Badge_DataLL2 = Image.open('assets/DataByLL2.png')
Badge_Nosu = Image.open('assets/Nosu.png')


# Functions for figures
def dark_figure():
    fig = plt.figure(facecolor='#0D1117', figsize=(7, 5.2))
    f = plt.gca()
    for i in f.spines:
        f.spines[i].set_color('white')
    f.tick_params(axis='x', colors='white', which='both')
    f.tick_params(axis='y', colors='white', which='both')
    f.yaxis.label.set_color('white')
    f.xaxis.label.set_color('white')
    f.title.set_color('white')
    f.set_facecolor('#0D1117')
    return f, fig


def finish_figure(fig, path, show):
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.20)
    fig_axes1 = fig.add_axes([0.678, 0.02, 0.3, 0.3], anchor='SE', zorder=1)
    fig_axes1.imshow(Badge_DataLL2)
    fig_axes1.axis('off')
    fig_axes2 = fig.add_axes([0.014, 0.02, 0.3, 0.3], anchor='SW', zorder=1)
    fig_axes2.imshow(Badge_Nosu)
    fig_axes2.axis('off')
    plt.savefig('plots/' + path + '_transparent.png', transparent=True, dpi=500)
    plt.savefig('plots/' + path + '_background.png', transparent=False, dpi=500)
    if show:
        plt.show()
    plt.close()


def flip_legend(reverse):
    handles_, labels_ = plt.gca().get_legend_handles_labels()
    handles_ = [k for j in [handles_[i::4] for i in range(4)] for k in j]
    labels_ = [k for j in [labels_[i::4] for i in range(4)] for k in j]
    if reverse:
        return handles_[::-1], labels_[::-1]
    else:
        return handles_, labels_


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
plt.xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."), color='dimgray',
           labelpad=10)
# finish_figure(F0, 'plots/test1.png')

colors_dict = {'red': '#e41a1c', 'orange': '#ff7f00', 'blue': '#377eb8', 'pink': '#f781bf', 'yellow': '#dede00',
               'green': '#4daf4a', 'grey': '#999999', 'purple': '#984ea3'}
colors = ['blue', 'orange', 'red', 'green', 'pink', 'yellow', 'purple', 'grey']
colors = [colors_dict[i] for i in colors]
LSPs_dict = {66: 'Soviet Union', 161: 'USAF', 63: 'ROSCOSMOS', 88: 'CASC', 115: 'Arianespace',
             96: 'Khrunichev ', 121: 'SpaceX', 147: 'Rocket Lab', 124: 'ULA', 257: 'NGSS', 285: 'Astra',
             199: 'Virgin Orbit', 163: 'VVKO', 166: 'US Navy', 271: 'ABMA', 165: 'US Army', 44: 'NASA', 270: 'RVSN RF',
             1018: 'CNR IT', 1017: 'SERC UK', 46: 'CNES FR', 1009: 'ISAS JP', 1019: 'ESRO', 1015: 'ELDO',
             1005: 'RAE UK', 189: 'CASC', 82: 'Lockheed', 228: 'NASDA', 100: 'OSC', 1004: 'Convair', 102: 'Rockwell',
             192: 'Lockheed SOC', 98: 'Mitsubishi HI', 1014: 'Martin M.', 111: 'Progress RSC', 154: 'Polyot',
             197: 'LMSO', 191: 'USA', 122: 'Sea Launch', 37: 'JAXA', 118: 'ILS', 193: 'VKS', 31: 'ISRO', 194: 'ExPace'}

# Plot of orbital launch attempts per country since 1957 stacked
F1_Countries = [['RUS', 'KAZ'], 'USA', 'CHN', ['FRA', 'GUF'], 'JPN', 'IND', 'NZL']
F1_Countries_Flatten = flatten(F1_Countries)
F1_Countries_Labels = ['Russia/USSR', 'USA', 'China', 'France', 'Japan', 'India', 'New Zealand', 'Others']
F1_Years = [i.year for i in LaunchT0 if i < datetime.now(timezone.utc).replace(tzinfo=None)]
_, F1 = dark_figure()
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
         label=F1_Countries_Labels, color=colors)
handles, labels = flip_legend(reverse=False)
plt.legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
plt.ylabel('Total launches per year')
plt.ylim([0, 180])
plt.xlim([min(F1_Years), max(F1_Years) + 1])
plt.title('Orbital launch attempts per country since ' + str(min(F1_Years)))
plt.xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."), color='dimgray',
           labelpad=10)
finish_figure(F1, 'OrbitalAttemptsPerCountryStacked', show=True)

# Plot of orbital launch attempts per country since 1957 non-stacked
_, F2 = dark_figure()
plt.hist(F1_data, bins=np.append(np.unique(F1_Years), max(F1_Years) + 1), histtype='step', stacked=False,
         label=F1_Countries_Labels, color=colors, linewidth=2)
handles, labels = flip_legend(reverse=True)
plt.legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
plt.ylabel('Launches per year')
plt.ylim([0, 130])
plt.xlim([min(F1_Years), max(F1_Years) + 1])
plt.xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."), color='dimgray',
           labelpad=10)
plt.title('Orbital launch attempts per country since ' + str(min(F1_Years)))
finish_figure(F2, 'OrbitalAttemptsPerCountry', show=True)

# Plot of orbital launch attempts per country per year since 1957
F1y_README = open('plots/yearly/orbitalAttemptsPerCountry/README.md', 'w')
F1y_README.write('# Orbital attempts per country for every year since 1957\n')
monthsLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
print('Starting yearly launch plots by country')
for year in range(1957, datetime.now(timezone.utc).year + 1):
    print(year)
    if year <= 1991:
        F1_Countries_Labels[0] = 'USSR'
    else:
        F1_Countries_Labels[0] = 'Russia'
    F1y_README.write('![Orbital attempts per country in ' + str(year) + '](' + str(year) + '_transparent.png)\n')
    days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
    if year > 1957:
        del F3
    _, F3 = dark_figure()
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
             linewidth=2, label=F1_Countries_Labels, color=colors)
    handles, labels = flip_legend(reverse=True)
    plt.legend(handles, labels, loc='upper center', ncol=4, frameon=False,
               labelcolor='white')
    plt.xticks([datetime(year, i, 1).timetuple().tm_yday for i in range(1, 13)], monthsLabels)
    plt.ylabel('Cumulative number of launches')
    plt.ylim([0, max([len(x) for x in F1y_data]) * 1.2])
    plt.xlim([1, max(days)])
    plt.xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."), color='dimgray',
               labelpad=10)
    plt.title('Orbital launch attempts per country in ' + str(year))
    finish_figure(F3, 'yearly/orbitalAttemptsPerCountry/' + str(year), show=False)
F1y_README.close()
print('Done with yearly launch plots by country')

# Plot of orbital launch attempts per LSP since 1957 stacked
F3_LSPs_Labels = ['SpaceX', 'ULA', 'CASC', 'Rocket Lab', 'ROSCOSMOS', 'Arianespace', 'Northrop Grumman', 'Others']
F3_Years = [i.year for i in LaunchT0 if i < datetime.now(timezone.utc).replace(tzinfo=None)]
_, F3 = dark_figure()
F3_data = []
F3_LSPs_ID = []
for LSP in Agencies:
    F3_LSP_ID = LSP['id']
    F3_data_tmp = [i[1].year for i in enumerate(LaunchT0) if
                   i[1] < datetime.now(timezone.utc).replace(tzinfo=None) and LaunchOrbit[i[0]] != 15 and
                   LaunchLSP[i[0]] == F3_LSP_ID]
    if F3_data_tmp:
        F3_data.append(F3_data_tmp)
        F3_LSPs_ID.append(LSP['id'])
F3_data_len = [len(x) for x in F3_data]
F3_data = [element for _, element in sorted(zip(F3_data_len, F3_data))]
F3_data = F3_data[-7::][::-1] + [flatten(F3_data[0:-7])]
F3_LSPs_ID = [element for _, element in sorted(zip(F3_data_len, F3_LSPs_ID))]
F3_LSPs_ID = F3_LSPs_ID[-7::][::-1]
F3_LSPs_Labels = [LSPs_dict[ii] for ii in F3_LSPs_ID] + ['Others']
plt.hist(F3_data, bins=np.append(np.unique(F3_Years), max(F3_Years) + 1), histtype='bar', stacked=True,
         label=F3_LSPs_Labels, color=colors)
handles, labels = flip_legend(reverse=False)
plt.legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
plt.ylabel('Total launches per year')
plt.ylim([0, 180])
plt.xlim([min(F3_Years), max(F3_Years) + 1])
plt.title('Orbital launch attempts per LSP since ' + str(min(F3_Years)))
plt.xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."), color='dimgray',
           labelpad=10)
finish_figure(F3, 'OrbitalAttemptsPerLSPStacked', show=True)

# Plot of orbital launch attempts per LSP per year since 1957
F3y_README = open('plots/yearly/orbitalAttemptsPerLSP/README.md', 'w')
F3y_README.write('# Orbital attempts per LSP for every year since 1957\n')
monthsLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
print('Starting yearly launch plots by LSP')
for year in range(1957, datetime.now(timezone.utc).year + 1):
    print(year)
    F3y_README.write('![Orbital attempts per LSP in ' + str(year) + '](' + str(year) + '_transparent.png)\n')
    days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
    if year > 1957:
        del F3
    _, F3 = dark_figure()
    F3y_data = []
    F3y_LSPs_ID = []
    for LSP in Agencies:
        F3y_LSP_ID = LSP['id']
        F3y_data_tmp = [i[1].timetuple().tm_yday for i in enumerate(LaunchT0) if
                        i[1].year == year and LaunchOrbit[i[0]] != 15 and LaunchLSP[i[0]] == F3y_LSP_ID and i[
                            1] < datetime.now(timezone.utc).replace(tzinfo=None)]
        if F3y_data_tmp:
            F3y_data.append(F3y_data_tmp)
            F3y_LSPs_ID.append(LSP['id'])
    F3y_data_len = [len(x) for x in F3y_data]
    F3y_data = [element for _, element in sorted(zip(F3y_data_len, F3y_data))]
    F3y_data = F3y_data[-7::][::-1] + [flatten(F3y_data[0:-7])]
    F3y_LSPs_ID = [element for _, element in sorted(zip(F3y_data_len, F3y_LSPs_ID))]
    F3y_LSPs_ID = F3y_LSPs_ID[-7::][::-1]
    F3y_LSPs_Labels = [LSPs_dict[ii] for ii in F3y_LSPs_ID] + ['Others']
    plt.hist(F3y_data, bins=np.append(days, max(days) + 1), histtype='step', cumulative=True, stacked=False,
             linewidth=2, label=F3y_LSPs_Labels, color=colors[0:len(F3y_data)])
    handles, labels = flip_legend(reverse=True)
    plt.legend(handles, labels, loc='upper center', ncol=4, frameon=False,
               labelcolor='white')
    plt.xticks([datetime(year, i, 1).timetuple().tm_yday for i in range(1, 13)], monthsLabels)
    plt.ylabel('Cumulative number of launches')
    plt.ylim([0, max([len(x) for x in F3y_data]) * 1.2])
    plt.xlim([1, max(days)])
    plt.xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."), color='dimgray',
               labelpad=10)
    plt.title('Orbital launch attempts per LSP in ' + str(year))
    finish_figure(F3, 'yearly/orbitalAttemptsPerLSP/' + str(year), show=False)
print('Done with yearly launch plots by LSP')
F3y_README.close()

print('Successfully generated and exported all plots.')
