import calendar

from Processing import PastT0s, FutureT0s
from plotsCodes.PlotFunctions import (
    dark_figure,
    prepare_legend,
    finish_figure,
    colors,
    monthsLabels,
    datetime,
    timezone,
    np,
)


# Plot of orbital launch attempts by country for the last 8 years
def main(pbar, show=False):
    Past_T0s = PastT0s.copy()
    Future_T0s = FutureT0s.copy()
    fig, axes = dark_figure()
    year_id = -1
    current_year = datetime.now(timezone.utc).year
    for year in range(current_year, current_year - 8, -1):
        year_id += 1
        Past_T0s_yearly = Past_T0s[Past_T0s["net"].dt.year == year][
            "net"
        ].dt.dayofyear.to_list()
        days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
        if year == current_year:
            Past_bins = np.arange(
                days[0], datetime.now(timezone.utc).timetuple().tm_yday + 2
            )
            Future_bins = np.arange(
                datetime.now(timezone.utc).timetuple().tm_yday + 2, days[-1] + 2
            )
            Future_T0s_yearly = Future_T0s[Future_T0s["net"].dt.year == year][
                "net"
            ].dt.dayofyear.to_list()
        else:
            Past_bins = np.append(days, max(days) + 1)
            Future_T0s_yearly = None
            Future_bins = None
        count_past, edges_past = np.histogram(Past_T0s_yearly, bins=Past_bins)
        axes[0].step(
            edges_past[:-1],
            count_past.cumsum(),
            linewidth=1.5,
            color=colors[year_id],
            label=year,
        )
        if Future_T0s_yearly:
            count_future, edges_future = np.histogram(
                Future_T0s_yearly, bins=Future_bins
            )
            axes[0].step(
                edges_future[:-1],
                count_future.cumsum() + count_past.sum(),
                linestyle="dotted",
                linewidth=1,
                color=colors[year_id],
                label="_nolegend_",
            )
    handles, labels = prepare_legend(reverse=False)
    axes[0].legend(
        handles, labels, loc="upper center", ncol=4, frameon=False, labelcolor="white"
    )
    axes[0].set_xticks(
        [datetime(current_year, i, 1).timetuple().tm_yday for i in range(1, 13)],
        monthsLabels,
    )
    axes[0].set(
        ylabel="Cumulative number of launches",
        xlim=[1, 365],
        title="Orbital launch attempts worldwide over the last 8 years",
    )
    finish_figure(fig, axes, "launchCadence8yearsPrediction", show=show)
    pbar.update()
