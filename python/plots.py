# Preamble
from datetime import datetime, timezone
import matplotlib.ticker as ticker
import numpy as np
import calendar
from math import ceil
from Processing import LaunchT0, LaunchOrbit, LaunchLSP, LaunchCountry
from PlotFunctions import dark_figure, finish_figure, flip_legend, Countries_dict, LSPs_dict, colors, monthsLabels

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
print('Starting yearly launch plots by country')
F1y_Countries_dict = Countries_dict
for year in range(1957, datetime.now(timezone.utc).year + 1):
    print(year)
    F1y_README.write('![Orbital attempts per country in ' + str(year) + '](' + str(year) + '.png)\n')
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
print('Starting yearly launch plots by LSP')
for year in F3_Years:
    print(year)
    F3y_README.write('![Orbital attempts per LSP in ' + str(year) + '](' + str(year) + '.png)\n')
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

# Plot of orbital launch attempts by LSP for the last 8 years
F4_LSPs = PastLSPs[PastT0s["net"] >= datetime(datetime.now(timezone.utc).year - 7, 1, 1, 0, 0, 0, 0, timezone.utc)][
    "id"].value_counts().index.tolist()

F4_README = open('plots/byLSP/README.md', 'w')
F4_README.write('# Orbital attempts per LSP for the last 8 years\n')
print('Starting launch plots by LSP over last 8 years')
for LSP in F4_LSPs:
    print(LSPs_dict[LSP])
    F4_README.write(
        '![Orbital attempts by ' + LSPs_dict[LSP] + ' in the last 8 years](' + LSPs_dict[LSP] + '.png)\n')
    F4, F4_axes = dark_figure()
    F4_LSP_T0s = PastT0s[PastLSPs["id"] == LSP].copy()
    year_id = -1
    for year in range(datetime.now(timezone.utc).year, datetime.now(timezone.utc).year - 8, -1):
        year_id += 1
        F4_LSP_T0s_yearly = F4_LSP_T0s[F4_LSP_T0s["net"].dt.year == year]["net"].dt.dayofyear.to_list()
        days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
        if year == datetime.now(timezone.utc).year:
            F4_bins = np.arange(days[0], datetime.now(timezone.utc).timetuple().tm_yday + 2)
        else:
            F4_bins = np.append(days, max(days) + 1)
        if F4_LSP_T0s_yearly:
            count, edges = np.histogram(F4_LSP_T0s_yearly, bins=F4_bins)
            F4_axes[0].step(edges[:-1], count.cumsum(), linewidth=2, color=colors[year_id], label=year)
    handles, labels = flip_legend(reverse=False)
    F4_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False,
                      labelcolor='white')
    F4_axes[0].set_xticks([datetime(datetime.now(timezone.utc).year, i, 1).timetuple().tm_yday for i in range(1, 13)],
                          monthsLabels)
    F4_axes[0].set(ylabel='Cumulative number of launches', xlim=[1, 365],
                   title='Orbital launch attempts by ' + LSPs_dict[LSP] + ' over the last ' + str(datetime.now(
                       timezone.utc).year - int(labels[-1]) + 1) + ' years',
                   ylim=[0, ceil(F4_axes[0].get_ylim()[1] * 1.2)])
    F4_axes[0].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    F4_axes[0].set_xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."),
                          color='dimgray', labelpad=10)
    finish_figure(F4, 'byLSP/' + LSPs_dict[LSP], show=True)
F4_README.close()

# Plot of orbital launch attempts by country for the last 8 years
F5_Countries = \
    PastCountries[PastT0s["net"] >= datetime(datetime.now(timezone.utc).year - 7, 1, 1, 0, 0, 0, 0, timezone.utc)][
        "location.country_code"].value_counts().index.tolist()
F5_Countries_dict = Countries_dict
F5_Countries_dict['RUS'] = 'Russia'
F5_README = open('plots/byCountry/README.md', 'w')
F5_README.write('# Orbital attempts per country for the last 8 years\n')
print('Starting launch plots by country over last 8 years')
for Country in F5_Countries:
    print(F5_Countries_dict[Country])
    F5_README.write(
        '![Orbital attempts by ' + F5_Countries_dict[Country] + ' in the last 8 years](' + F5_Countries_dict[
            Country] + '.png)\n')
    F5, F5_axes = dark_figure()
    F5_Country_T0s = PastT0s[PastCountries["location.country_code"] == Country].copy()
    year_id = -1
    for year in range(datetime.now(timezone.utc).year, datetime.now(timezone.utc).year - 8, -1):
        year_id += 1
        F5_Country_T0s_yearly = F5_Country_T0s[F5_Country_T0s["net"].dt.year == year]["net"].dt.dayofyear.to_list()
        days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
        if year == datetime.now(timezone.utc).year:
            F5_bins = np.arange(days[0], datetime.now(timezone.utc).timetuple().tm_yday + 2)
        else:
            F5_bins = np.append(days, max(days) + 1)
        if F5_Country_T0s_yearly:
            count, edges = np.histogram(F5_Country_T0s_yearly, bins=F5_bins)
            F5_axes[0].step(edges[:-1], count.cumsum(), linewidth=2, color=colors[year_id], label=year)
    handles, labels = flip_legend(reverse=False)
    F5_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False,
                      labelcolor='white')
    F5_axes[0].set_xticks([datetime(datetime.now(timezone.utc).year, i, 1).timetuple().tm_yday for i in range(1, 13)],
                          monthsLabels)
    F5_axes[0].set(ylabel='Cumulative number of launches', xlim=[1, 365],
                   title='Orbital launch attempts by ' + F5_Countries_dict[Country] + ' over the last ' + str(
                       datetime.now(timezone.utc).year - int(labels[-1]) + 1) + ' years',
                   ylim=[0, ceil(F5_axes[0].get_ylim()[1] * 1.2)])
    F5_axes[0].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    F5_axes[0].set_xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."),
                          color='dimgray', labelpad=10)
    finish_figure(F5, 'byCountry/' + F5_Countries_dict[Country], show=True)
F5_README.close()

print('Successfully generated and exported all plots.')
