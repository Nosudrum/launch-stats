import calendar

from Processing import PastT0s
from plotsCodes.PlotFunctions import dark_figure, flip_legend, finish_figure, colors, monthsLabels, \
    datetime, timezone, np


# Plot of orbital launch attempts by country for the last 8 years
def main(show=False):
    Past_T0s = PastT0s.copy()
    print('Starting plot of worldwide launch cadence over last 8 years (with linear prediction)')
    fig, axes = dark_figure()
    year_id = -1
    current_year = datetime.now(timezone.utc).year
    for year in range(current_year, current_year - 8, -1):
        year_id += 1
        Past_T0s_yearly = Past_T0s[Past_T0s["net"].dt.year == year]["net"].dt.dayofyear.to_list()
        days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
        if year == current_year:
            Past_bins = np.arange(days[0], datetime.now(timezone.utc).timetuple().tm_yday + 2)
        else:
            Past_bins = np.append(days, max(days) + 1)
        count_past, edges_past = np.histogram(Past_T0s_yearly, bins=Past_bins)
        axes[0].step(edges_past[:-1], count_past.cumsum(), linewidth=1.5, color=colors[year_id], label=year)
        if year == current_year:
            pred_minx = Past_bins[-1]
            pred_maxx = max(days) + 1
            pred_miny = len(Past_T0s_yearly)
            pred_maxy = np.round(pred_miny * pred_maxx / pred_minx)
            axes[0].plot([pred_minx, pred_maxx], [pred_miny, pred_maxy], linestyle='dotted',
                         linewidth=1, color=colors[year_id], label='_nolegend_')
    handles, labels = flip_legend(reverse=False)
    axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False,
                   labelcolor='white')
    axes[0].set_xticks(
        [datetime(current_year, i, 1).timetuple().tm_yday for i in range(1, 13)],
        monthsLabels)
    axes[0].set(ylabel='Cumulative number of launches', xlim=[1, 365],
                title='Orbital launch attempts worldwide over the last 8 years')
    finish_figure(fig, axes, 'launchCadence8yearsPredictionLinear', show=show)
    print('Done with plot of worldwide launch cadence over last 8 years (with linear prediction)')
