# Preamble
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import calendar
from Processing import LaunchT0, LaunchOrbit, LaunchCountry, LocsName, LocsLaunchCount, LocsLat, LocsLon
from PIL import Image

Badge_DataLL2 = Image.open('assets/DataByLL2.png')
Badge_Nosu = Image.open('assets/Nosu.png')


# Functions for figures
def dark_figure():
    fig = plt.figure(facecolor='#0D1117', figsize=(7, 5))
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

# Plot of orbital launch attempts per country since 1957 stacked
F1_Countries = [['RUS', 'KAZ'], 'USA', 'CHN', ['FRA', 'GUF'], 'JPN', 'IND', 'NZL']
F1_Countries_Flatten = flatten(F1_Countries)
F1_Countries_Labels = ['Russia/USSR', 'USA', 'China', 'France', 'Japan', 'India', 'New Zealand', 'Others']
colors = {'red': '#e41a1c', 'orange': '#ff7f00', 'blue': '#377eb8', 'pink': '#f781bf', 'yellow': '#dede00',
          'green': '#4daf4a', 'grey': '#999999', 'purple': '#984ea3'}
F1_colors = ['blue', 'orange', 'red', 'green', 'pink', 'yellow', 'purple', 'grey']
F1_colors = [colors[i] for i in F1_colors]
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
         label=F1_Countries_Labels, color=F1_colors)
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
         label=F1_Countries_Labels, color=F1_colors, linewidth=2)
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
for year in range(1957, datetime.now(timezone.utc).year + 1):
    F1y_README.write('![Orbital attempts per country in ' + str(year) + '](' + str(year) + '.png)\n')
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
             linewidth=2, label=F1_Countries_Labels, color=F1_colors)
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
