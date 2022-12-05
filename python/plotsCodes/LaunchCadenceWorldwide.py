import calendar

from Processing import PastT0s
from plotsCodes.PlotFunctions import dark_figure, prepare_legend, finish_figure, colors, monthsLabels, \
    datetime, timezone, np


# Plot of orbital launch attempts by country for the last 8 years
def main(show=False):
    T0s = PastT0s.copy()
    print('Starting plot of worldwide launch cadence over last 8 years')
    fig, axes = dark_figure()
    year_id = -1
    for year in range(datetime.now(timezone.utc).year, datetime.now(timezone.utc).year - 8, -1):
        year_id += 1
        T0s_yearly = T0s[T0s["net"].dt.year == year]["net"].dt.dayofyear.to_list()
        days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
        if year == datetime.now(timezone.utc).year:
            bins = np.arange(days[0], datetime.now(timezone.utc).timetuple().tm_yday + 2)
        else:
            bins = np.append(days, max(days) + 1)
        count, edges = np.histogram(T0s_yearly, bins=bins)
        axes[0].step(edges[:-1], count.cumsum(), linewidth=1.5, color=colors[year_id], label=year)
    handles, labels = prepare_legend(reverse=False)
    axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False,
                   labelcolor='white')
    axes[0].set_xticks(
        [datetime(datetime.now(timezone.utc).year, i, 1).timetuple().tm_yday for i in range(1, 13)],
        monthsLabels)
    axes[0].set(ylabel='Cumulative number of launches', xlim=[1, 365],
                title='Orbital launch attempts worldwide over the last 8 years')
    finish_figure(fig, axes, 'launchCadence8years', show=show)
    print('Done with plot of worldwide launch cadence over last 8 years')
