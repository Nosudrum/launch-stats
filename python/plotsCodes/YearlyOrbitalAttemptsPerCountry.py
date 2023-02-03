import calendar

from tqdm import tqdm

from Processing import PastT0s, PastCountries
from plotsCodes.PlotFunctions import Countries_dict, dark_figure, finish_figure, prepare_legend, colors, monthsLabels, \
    datetime, timezone, np


# Plot of orbital launch attempts per country per year since 1957
def main(pbar, show=False):
    F1y_README = open('plots/yearly/orbitalAttemptsPerCountry/README.md', 'w')
    F1y_README.write('# Orbital attempts per country for every year since 1957\n')
    F1y_Countries_dict = Countries_dict.copy()
    F1_Countries = PastCountries.copy()
    F1_Countries_sorted = F1_Countries["location.country_code"].value_counts().index.tolist()
    F1_Countries_selected = F1_Countries_sorted[0:7]
    F1_Countries[~F1_Countries["location.country_code"].isin(F1_Countries_selected)] = 'OTH'
    F1_Countries_selected.append('OTH')
    for year in tqdm(range(1957, datetime.now(timezone.utc).year + 1), desc='Years', ncols=80, position=1, leave=False):
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
                F1y_axes[0].step(edges[:-1], count.cumsum(), linewidth=1.5, color=colors[ii[0]],
                                 label=F1y_Countries_dict[ii[1]])
        handles, labels = prepare_legend(reverse=False)
        F1y_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False,
                           labelcolor='white')
        F1y_axes[0].set_xticks([datetime(year, i, 1).timetuple().tm_yday for i in range(1, 13)], monthsLabels)
        F1y_axes[0].set(ylabel='Cumulative number of launches', xlim=[1, max(days)],
                        title='Orbital launch attempts per country in ' + str(year))
        finish_figure(F1y, F1y_axes, 'yearly/orbitalAttemptsPerCountry/' + str(year), show=show)
    F1y_README.close()
    pbar.update()
