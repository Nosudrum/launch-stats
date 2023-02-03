import calendar

from tqdm import tqdm

from Processing import PastT0s, PastLSPs
from plotsCodes.PlotFunctions import dark_figure, prepare_legend, colors, finish_figure, LSPs_dict, monthsLabels, np, \
    datetime, timezone


# Plot of orbital launch attempts per LSP per year since 1957
def main(show=False):
    F3y_README = open('plots/yearly/orbitalAttemptsPerLSP/README.md', 'w')
    F3y_README.write('# Orbital attempts per LSP for every year since 1957\n')
    print('Starting yearly launch plots by LSP')
    F3_Years = PastT0s["net"].dt.year.unique().tolist()
    for year in tqdm(F3_Years, desc='Years', ncols=80):
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
            F3y_axes[0].step(edges[:-1], count.cumsum(), linewidth=1.5, color=colors[ii[0]], label=LSPs_dict[ii[1]])
        handles, labels = prepare_legend(reverse=False)
        F3y_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False,
                           labelcolor='white')
        F3y_axes[0].set_xticks([datetime(year, i, 1).timetuple().tm_yday for i in range(1, 13)], monthsLabels)
        F3y_axes[0].set(ylabel='Cumulative number of launches', xlim=[1, max(days)],
                        title='Orbital launch attempts per LSP in ' + str(year))
        finish_figure(F3y, F3y_axes, 'yearly/orbitalAttemptsPerLSP/' + str(year), show=show)
    F3y_README.close()
