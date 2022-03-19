# Preamble
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import calendar
from math import ceil, prod
from Processing import LaunchT0, LaunchOrbit, LaunchLSP, LaunchCountry
from PIL import Image

Badge_DataLL2 = Image.open('assets/DataByLL2.png')
Badge_Nosu = Image.open('assets/Nosu.png')


# Functions for figures
def dark_figure(subplots=(1, 1), figsize=(7, 5.2)):
    fig = plt.figure(facecolor='#0D1117', figsize=figsize)
    axes = []
    for ii in range(0, prod(subplots)):
        axes.append(fig.add_subplot(subplots[0], subplots[1], ii + 1, facecolor='#0D1117'))
        axes[ii].tick_params(axis='x', colors='white', which='both')
        axes[ii].tick_params(axis='y', colors='white', which='both')
        axes[ii].yaxis.label.set_color('white')
        axes[ii].xaxis.label.set_color('white')
        axes[ii].title.set_color('white')
        for i in axes[ii].spines:
            axes[ii].spines[i].set_color('white')
    return fig, axes


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


# Colors
colors_dict = {'red': '#e41a1c', 'orange': '#ff7f00', 'blue': '#377eb8', 'pink': '#f781bf', 'yellow': '#dede00',
               'green': '#4daf4a', 'grey': '#999999', 'purple': '#984ea3'}
colors = ['blue', 'orange', 'red', 'green', 'pink', 'yellow', 'purple', 'grey']
colors = [colors_dict[i] for i in colors]

# LSPs custom names
LSPs_dict = {0: 'Others', 66: 'Soviet Union', 161: 'USAF', 63: 'ROSCOSMOS', 88: 'CASC', 115: 'Arianespace',
             96: 'Khrunichev ', 121: 'SpaceX', 147: 'Rocket Lab', 124: 'ULA', 257: 'NGSS', 285: 'Astra',
             199: 'Virgin Orbit', 163: 'VVKO', 166: 'US Navy', 271: 'ABMA', 165: 'US Army', 44: 'NASA', 270: 'RVSN RF',
             1018: 'CNR IT', 1017: 'SERC UK', 46: 'CNES FR', 1009: 'ISAS JP', 1019: 'ESRO', 1015: 'ELDO',
             1005: 'RAE UK', 189: 'CASC', 82: 'Lockheed', 228: 'NASDA', 100: 'OSC', 1004: 'Convair', 102: 'Rockwell',
             192: 'Lockheed SOC', 98: 'Mitsubishi HI', 1014: 'Martin M.', 111: 'Progress RSC', 154: 'Polyot',
             197: 'LMSO', 191: 'USA', 122: 'Sea Launch', 37: 'JAXA', 118: 'ILS', 193: 'VKS', 31: 'ISRO', 194: 'ExPace',
             1016: 'Aus. WRE', 29: 'DLR DE', 106: 'Gen. Dynamics', 1032: 'IRGCAF', 36: 'ASI IT', 119: 'ISCK', 34: 'IRN'}

Countries_dict = {'OTH': 'Others', 'RUS': 'Russia/USSR', 'USA': 'USA', 'CHN': 'China', 'FRA': 'France', 'JPN': 'Japan',
                  'IND': 'India', 'NZL': 'New Zealand'}

# Intermediate data
PastLSPs = LaunchLSP[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastT0s = LaunchT0[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastCountries = LaunchCountry[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()

# Figures

# Plot of orbital launch attempts per country since 1957 stacked
F1_Years = PastT0s["net"].dt.year.unique().tolist()
F1, F1_axes = dark_figure()
F1_Countries = PastCountries.copy()
F1_Countries_sorted = F1_Countries["location.country_code"].value_counts().index.tolist()
F1_Countries_selected = F1_Countries_sorted[0:7]
F1_Countries[~F1_Countries["location.country_code"].isin(F1_Countries_selected)] = 'OTH'
F1_Countries_selected.append('OTH')
F1_data = []
for Country in F1_Countries_selected:
    F1_data.append(PastT0s[F1_Countries["location.country_code"] == Country]["net"].dt.year.values.tolist())
F1_Countries_Labels = [Countries_dict[ii] for ii in F1_Countries_selected]
F1_axes[0].hist(F1_data, bins=np.append(np.unique(F1_Years), max(F1_Years) + 1), histtype='bar', stacked=True,
                label=F1_Countries_Labels, color=colors)
handles, labels = flip_legend(reverse=False)
F1_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
F1_axes[0].set(ylabel='Total launches per year', ylim=[0, 180], xlim=[min(F1_Years), max(F1_Years) + 1],
               title='Orbital launch attempts per country since ' + str(min(F1_Years)))
F1_axes[0].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
F1_axes[0].set_xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."),
                      color='dimgray',
                      labelpad=10)
finish_figure(F1, 'OrbitalAttemptsPerCountryStacked', show=True)

# Plot of orbital launch attempts per country since 1957 non-stacked
F2, F2_axes = dark_figure()
F2_axes[0].hist(F1_data, bins=np.append(np.unique(F1_Years), max(F1_Years) + 1), histtype='step', stacked=False,
                label=F1_Countries_Labels, color=colors, linewidth=2)
handles, labels = flip_legend(reverse=True)
F2_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
F2_axes[0].set(ylabel='Launches per year', ylim=[0, 130], xlim=[min(F1_Years), max(F1_Years) + 1],
               title='Orbital launch attempts per country since ' + str(min(F1_Years)))
F1_axes[0].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
F2_axes[0].set_xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."),
                      color='dimgray',
                      labelpad=10)
finish_figure(F2, 'OrbitalAttemptsPerCountry', show=True)

# Plot of orbital launch attempts per country per year since 1957
F1y_README = open('plots/yearly/orbitalAttemptsPerCountry/README.md', 'w')
F1y_README.write('# Orbital attempts per country for every year since 1957\n')
monthsLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
print('Starting yearly launch plots by country')
F1y_Countries_dict = Countries_dict
for year in range(1957, datetime.now(timezone.utc).year + 1):
    print(year)
    F1y_README.write('![Orbital attempts per country in ' + str(year) + '](' + str(year) + '_transparent.png)\n')
    days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
    if year > 1991:
        F1y_Countries_dict['RUS'] = 'Russia'
    else:
        F1y_Countries_dict['RUS'] = 'USSR'
    if year > 1957:
        del F1y
    F1y, F1y_axes = dark_figure()
    F1y_T0s = PastT0s[PastT0s["net"].dt.year == year].copy()
    F1y_Countries = PastCountries[PastT0s["net"].dt.year == year]["location.country_code"].to_frame().copy()
    F1y_Countries[~F1y_Countries["location.country_code"].isin(F1_Countries_selected)] = 'OTH'
    if year == datetime.now(timezone.utc).year:
        F1y_bins = np.arange(days[0], datetime.now(timezone.utc).timetuple().tm_yday + 2)
    else:
        F1y_bins = np.append(days, max(days) + 1)
    for ii in enumerate(F1_Countries_selected):
        F1y_data_tmp = F1y_T0s[F1y_Countries["location.country_code"] == ii[1]]["net"].dt.dayofyear.to_list()
        if F1y_data_tmp:
            count, edges = np.histogram(F1y_data_tmp, bins=F1y_bins)
            F1y_axes[0].step(edges[:-1], count.cumsum(), linewidth=2, color=colors[ii[0]],
                             label=F1y_Countries_dict[ii[1]])
    handles, labels = flip_legend(reverse=False)
    F1y_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False,
                       labelcolor='white')
    F1y_axes[0].set_xticks([datetime(year, i, 1).timetuple().tm_yday for i in range(1, 13)], monthsLabels)
    F1y_axes[0].set(ylabel='Cumulative number of launches', xlim=[1, max(days)],
                    title='Orbital launch attempts per country in ' + str(year),
                    ylim=[0, ceil(F1y_Countries["location.country_code"].value_counts().to_list()[0] * 1.2)])
    F1y_axes[0].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    F1y_axes[0].set_xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."),
                           color='dimgray', labelpad=10)
    finish_figure(F1y, 'yearly/orbitalAttemptsPerCountry/' + str(year), show=False)
F1y_README.close()
print('Done with yearly launch plots by country')

# Plot of orbital launch attempts per LSP since 1957 stacked
F3_Years = PastT0s["net"].dt.year.unique().tolist()
F3, F3_axes = dark_figure()
F3_LSPs = PastLSPs.copy()
F3_LSPs_sorted = F3_LSPs["id"].value_counts().index.tolist()
F3_LSPs_selected = F3_LSPs_sorted[0:7]
F3_LSPs[~F3_LSPs["id"].isin(F3_LSPs_selected)] = 0
F3_LSPs_selected.append(0)
F3_data = []
for LSP in F3_LSPs_selected:
    F3_data.append(PastT0s[F3_LSPs["id"] == LSP]["net"].dt.year.values.tolist())
F3_LSPs_Labels = [LSPs_dict[ii] for ii in F3_LSPs_selected]
F3_axes[0].hist(F3_data, bins=np.append(F3_Years, max(F3_Years) + 1), histtype='bar', stacked=True,
                label=F3_LSPs_Labels, color=colors)
handles, labels = flip_legend(reverse=False)
F3_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
F3_axes[0].set(ylabel='Total launches per year', ylim=[0, 180], xlim=[min(F3_Years), max(F3_Years) + 1],
               title='Orbital launch attempts per LSP since ' + str(min(F3_Years)))
F3_axes[0].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
F3_axes[0].set_xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."),
                      color='dimgray', labelpad=10)
finish_figure(F3, 'OrbitalAttemptsPerLSPStacked', show=True)

# Plot of orbital launch attempts per LSP per year since 1957
F3y_README = open('plots/yearly/orbitalAttemptsPerLSP/README.md', 'w')
F3y_README.write('# Orbital attempts per LSP for every year since 1957\n')
monthsLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
print('Starting yearly launch plots by LSP')
for year in F3_Years:
    print(year)
    F3y_README.write('![Orbital attempts per LSP in ' + str(year) + '](' + str(year) + '_transparent.png)\n')
    days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
    if year > 1957:
        del F3y
    F3y, F3y_axes = dark_figure()
    F3y_T0s = PastT0s[PastT0s["net"].dt.year == year].copy()
    F3y_LSPs = PastLSPs[PastT0s["net"].dt.year == year]["id"].to_frame().copy()
    F3y_LSPs_sorted = F3y_LSPs["id"].value_counts().index.tolist()
    if len(F3y_LSPs_sorted) > 7:
        F3y_LSPs_selected = F3y_LSPs_sorted[0:7]
        F3y_LSPs[~F3y_LSPs["id"].isin(F3y_LSPs_selected)] = 0
        F3y_LSPs_selected.append(0)
    else:
        F3y_LSPs_selected = F3y_LSPs_sorted
    if year == datetime.now(timezone.utc).year:
        F3y_bins = np.arange(days[0], datetime.now(timezone.utc).timetuple().tm_yday + 2)
    else:
        F3y_bins = np.append(days, max(days) + 1)
    for ii in enumerate(F3y_LSPs_selected):
        F3y_data_tmp = F3y_T0s[F3y_LSPs["id"] == ii[1]]["net"].dt.dayofyear.to_list()
        count, edges = np.histogram(F3y_data_tmp, bins=F3y_bins)
        F3y_axes[0].step(edges[:-1], count.cumsum(), linewidth=2, color=colors[ii[0]], label=LSPs_dict[ii[1]])
    handles, labels = flip_legend(reverse=False)
    F3y_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False,
                       labelcolor='white')
    F3y_axes[0].set_xticks([datetime(year, i, 1).timetuple().tm_yday for i in range(1, 13)], monthsLabels)
    F3y_axes[0].set(ylabel='Cumulative number of launches', xlim=[1, max(days)],
                    title='Orbital launch attempts per LSP in ' + str(year),
                    ylim=[0, ceil(F3y_LSPs["id"].value_counts().to_list()[0] * 1.2)])
    F3y_axes[0].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    F3y_axes[0].set_xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."),
                           color='dimgray', labelpad=10)
    finish_figure(F3y, 'yearly/orbitalAttemptsPerLSP/' + str(year), show=False)
print('Done with yearly launch plots by LSP')
F3y_README.close()

print('Successfully generated and exported all plots.')
