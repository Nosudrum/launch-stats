# Preamble
from datetime import datetime, timezone
import matplotlib.ticker as ticker
import numpy as np
import calendar
from math import ceil
from Processing import LaunchT0, LaunchOrbit, LaunchLSP, LaunchCountry
from PlotFunctions import dark_figure, finish_figure, flip_legend, LSPs_dict, colors, monthsLabels

# Intermediate data
PastLSPs = LaunchLSP[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastT0s = LaunchT0[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()
PastCountries = LaunchCountry[(LaunchT0["net"] <= datetime.now(timezone.utc)) & (LaunchOrbit["orbit.id"] != 15)].copy()

# Plot of orbital launch attempts by LSP for the last 8 years
F4_LSPs_selected = [121, 115, 63, 88, 96, 147, 124, 285, 199, 37, 31]

F4_README = open('plots/byLSP/README.md', 'w')
F4_README.write('# Orbital attempts per LSP for the last 8 years\n')
print('Starting launch plots by LSP over last 8 years')
for LSP in F4_LSPs_selected:
    F4_README.write(
        '![Orbital attempts by ' + LSPs_dict[LSP] + ' in the last 8 years](' + LSPs_dict[LSP] + '_transparent.png)\n')
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
                       timezone.utc).year - int(labels[-1])+1) + ' years',
                   ylim=[0, ceil(F4_axes[0].get_ylim()[1] * 1.2)])
    F4_axes[0].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    F4_axes[0].set_xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."),
                          color='dimgray', labelpad=10)
    finish_figure(F4, 'byLSP/' + LSPs_dict[LSP], show=True)
F4_README.close()
