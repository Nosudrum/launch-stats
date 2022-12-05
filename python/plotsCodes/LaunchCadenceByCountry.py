import calendar

from Processing import PastT0s, PastCountries
from plotsCodes.PlotFunctions import dark_figure, prepare_legend, finish_figure, colors, Countries_dict, monthsLabels, \
    datetime, timezone, np


# Plot of orbital launch attempts by country for the last 8 years
def main(show=False):
    F5_Countries = \
        PastCountries[PastT0s["net"] >= datetime(datetime.now(timezone.utc).year - 7, 1, 1, 0, 0, 0, 0, timezone.utc)][
            "location.country_code"].value_counts().index.tolist()
    F5_Countries_dict = Countries_dict.copy()
    F5_Countries_dict['RUS'] = 'Russia'
    F5_README = open('plots/byCountry/launchCadence8years/README.md', 'w')
    F5_README.write('# Orbital attempts per country for the last 8 years\n')
    print('Starting launch plots by country over last 8 years')
    for Country in F5_Countries:
        print(F5_Countries_dict[Country])
        F5_README.write(
            '![Orbital attempts by ' + F5_Countries_dict[Country] + ' in the last 8 years](' + F5_Countries_dict[
                Country].replace(" ", "_") + '.png)\n')
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
                F5_axes[0].step(edges[:-1], count.cumsum(), linewidth=1.5, color=colors[year_id], label=year)
        handles, labels = prepare_legend(reverse=False)
        F5_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False,
                          labelcolor='white')
        F5_axes[0].set_xticks(
            [datetime(datetime.now(timezone.utc).year, i, 1).timetuple().tm_yday for i in range(1, 13)],
            monthsLabels)
        F5_axes[0].set(ylabel='Cumulative number of launches', xlim=[1, 365],
                       title='Orbital launch attempts by ' + F5_Countries_dict[Country] + ' over the last ' + str(
                           datetime.now(timezone.utc).year - int(labels[-1]) + 1) + ' years')
        finish_figure(F5, F5_axes, 'byCountry/launchCadence8years/' + F5_Countries_dict[Country].replace(" ", "_"),
                      show=show)
    F5_README.close()
    print('Done with launch plots by country over last 8 years')
