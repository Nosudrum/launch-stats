import calendar

from Processing import PastT0s, PastLSPs
from plotsCodes.PlotFunctions import LSPs_dict, colors, monthsLabels, dark_figure, finish_figure, flip_legend, \
    datetime, timezone, np


# Plot of orbital launch attempts by LSP for the last 8 years
def main(show=False):
    current_year = datetime.now(timezone.utc).year
    LSPs = PastLSPs[PastT0s["net"] >= datetime(current_year - 7, 1, 1, 0, 0, 0, 0, timezone.utc)][
        "id"].value_counts().index.tolist()
    README = open('plots/byLSP/launchCadence8yearsPredictionLinear/README.md', 'w')
    README.write(f'# Orbital attempts per LSP for the last 8 years (with {current_year} linear prediction)\n')
    print('Starting launch plots by LSP over last 8 years (with linear prediction)')
    for LSP in LSPs:
        print(LSPs_dict[LSP])
        README.write(
            '![Orbital attempts by ' + LSPs_dict[LSP] + ' in the last 8 years]('
            + LSPs_dict[LSP].replace(" ", "_") + '.png)\n')
        fig, axes = dark_figure()
        LSP_Past_T0s = PastT0s[PastLSPs["id"] == LSP].copy()
        year_id = -1
        for year in range(current_year, current_year - 8, -1):
            year_id += 1
            LSP_Past_T0s_yearly = LSP_Past_T0s[LSP_Past_T0s["net"].dt.year == year]["net"].dt.dayofyear.to_list()
            days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
            if year == current_year:
                Past_bins = np.arange(days[0], datetime.now(timezone.utc).timetuple().tm_yday + 2)
            else:
                Past_bins = np.append(days, max(days) + 1)
            if LSP_Past_T0s_yearly:
                count_past, edges_past = np.histogram(LSP_Past_T0s_yearly, bins=Past_bins)
                axes[0].step(edges_past[:-1], count_past.cumsum(), linewidth=1.5, color=colors[year_id], label=year)
                if year == current_year:
                    pred_minx = Past_bins[-1]
                    pred_maxx = max(days) + 1
                    pred_miny = len(LSP_Past_T0s_yearly)
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
                    title=f'Orbital launch attempts by {LSPs_dict[LSP]} over the' +
                          f' last {str(current_year - int(labels[-1]) + 1)} years')
        finish_figure(fig, axes, 'byLSP/launchCadence8yearsPredictionLinear/' + LSPs_dict[LSP].replace(" ", "_"),
                      show=show)
    README.close()
    print('Done with launch plots by LSP over last 8 years (with linear prediction)')
