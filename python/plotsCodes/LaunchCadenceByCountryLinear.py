import calendar

from Processing import PastT0s, PastCountries
from plotsCodes.PlotFunctions import dark_figure, prepare_legend, finish_figure, colors, Countries_dict, monthsLabels, \
    datetime, timezone, np


# Plot of orbital launch attempts by country for the last 8 years
def main(show=False):
    current_year = datetime.now(timezone.utc).year
    Countries = \
        PastCountries[PastT0s["net"] >= datetime(current_year - 7, 1, 1, 0, 0, 0, 0, timezone.utc)][
            "location.country_code"].value_counts().index.tolist()
    Countries_dict_tmp = Countries_dict.copy()
    Countries_dict_tmp['RUS'] = 'Russia'
    README = open('plots/byCountry/launchCadence8yearsPredictionLinear/README.md', 'w')
    README.write(f'# Orbital attempts per country for the last 8 years (with {current_year} linear prediction)\n')
    print('Starting launch plots by country over last 8 years (with linear prediction)')
    for Country in Countries:
        print(Countries_dict_tmp[Country])
        README.write(
            f'![Orbital attempts by {Countries_dict_tmp[Country]} in the last 8 years](' + Countries_dict_tmp[
                Country].replace(" ", "_") + '.png)\n')
        fig, axes = dark_figure()
        Country_Past_T0s = PastT0s[PastCountries["location.country_code"] == Country].copy()
        year_id = -1
        for year in range(current_year, current_year - 8, -1):
            year_id += 1
            Country_Past_T0s_yearly = Country_Past_T0s[Country_Past_T0s["net"].dt.year == year][
                "net"].dt.dayofyear.to_list()
            days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
            if year == current_year:
                Past_bins = np.arange(days[0], datetime.now(timezone.utc).timetuple().tm_yday + 2)
            else:
                Past_bins = np.append(days, max(days) + 1)
            if Country_Past_T0s_yearly:
                count_past, edges_past = np.histogram(Country_Past_T0s_yearly, bins=Past_bins)
                axes[0].step(edges_past[:-1], count_past.cumsum(), linewidth=1.5, color=colors[year_id], label=year)
                if year == current_year:
                    pred_minx = Past_bins[-1]
                    pred_maxx = max(days) + 1
                    pred_miny = len(Country_Past_T0s_yearly)
                    pred_maxy = np.round(pred_miny * pred_maxx / pred_minx)
                    axes[0].plot([pred_minx, pred_maxx], [pred_miny, pred_maxy], linestyle='dotted',
                                 linewidth=1, color=colors[year_id], label='_nolegend_')
        handles, labels = prepare_legend(reverse=False)
        axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False,
                       labelcolor='white')
        axes[0].set_xticks(
            [datetime(datetime.now(timezone.utc).year, i, 1).timetuple().tm_yday for i in range(1, 13)],
            monthsLabels)
        axes[0].set(ylabel='Cumulative number of launches', xlim=[1, 365],
                    title='Orbital launch attempts by ' + Countries_dict_tmp[Country] + ' over the last ' + str(
                        current_year - int(labels[-1]) + 1) + ' years')
        finish_figure(fig, axes, 'byCountry/launchCadence8yearsPredictionLinear/' +
                      Countries_dict_tmp[Country].replace(" ", "_"), show=show)
    README.close()
    print('Done with launch plots by country over last 8 years (with linear prediction)')
