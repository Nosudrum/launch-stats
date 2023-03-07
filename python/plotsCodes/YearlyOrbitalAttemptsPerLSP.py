import calendar

from tqdm import tqdm

from Processing import PastT0s, PastLSPs, PastStatus
from plotsCodes.PlotFunctions import (
    dark_figure,
    prepare_legend,
    colors,
    finish_figure,
    LSPs_dict,
    monthsLabels,
    np,
    datetime,
    timezone,
    github_dark,
)


# Plot of orbital launch attempts per LSP per year since 1957
def main(pbar, show=False):
    README = open("plots/yearly/orbitalAttemptsPerLSP/README.md", "w")
    README.write("# Orbital attempts per LSP for every year since 1957\n")
    Years = PastT0s["net"].dt.year.unique().tolist()
    for year in tqdm(Years, desc="Years", ncols=80, position=1, leave=False):
        README.write(
            "![Orbital attempts per LSP in " + str(year) + "](" + str(year) + ".png)\n"
        )
        days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
        if year > 1957:
            del fig
        fig, axes = dark_figure()
        T0s = PastT0s[PastT0s["net"].dt.year == year].copy()
        LSPs = PastLSPs[PastT0s["net"].dt.year == year]["id"].to_frame().copy()
        LSPs_sorted = LSPs["id"].value_counts().index.tolist()
        if len(LSPs_sorted) > 7:
            LSPs_selected = LSPs_sorted[0:7]
            LSPs[~LSPs["id"].isin(LSPs_selected)] = 0
            LSPs_selected.append(0)
        else:
            LSPs_selected = LSPs_sorted
        if year == datetime.now(timezone.utc).year:
            bins = np.arange(
                days[0], datetime.now(timezone.utc).timetuple().tm_yday + 2
            )
        else:
            bins = np.append(days, max(days) + 1)
        legend_failure = False
        legend_partial = False
        for ii in enumerate(LSPs_selected):
            LSP_mask = LSPs["id"] == ii[1]
            yearly_LSP_dayofyear = T0s[LSP_mask]["net"].dt.dayofyear.to_list()
            yearly_LSP_failure = T0s.loc[LSP_mask & (PastStatus["id"] == 4)][
                "net"
            ].dt.dayofyear.to_list()
            yearly_LSP_partial = T0s.loc[LSP_mask & (PastStatus["id"] == 7)][
                "net"
            ].dt.dayofyear.to_list()

            count, edges = np.histogram(yearly_LSP_dayofyear, bins=bins)
            cumulative_count = count.cumsum()

            axes[0].step(
                edges[:-1],
                cumulative_count,
                linewidth=1.2,
                color=colors[ii[0]],
                label=LSPs_dict[ii[1]],
                zorder=1,
            )

            index_failure = [
                np.where(edges == item)[0][0] for item in yearly_LSP_failure
            ]
            if index_failure:
                legend_failure = True
                edges_failure = edges[index_failure]
                count_failure = cumulative_count[index_failure]
                axes[0].scatter(
                    edges_failure - 1,
                    count_failure,
                    marker="*",
                    c=colors[ii[0]],
                    s=70,
                    edgecolors=github_dark,
                    linewidths=0.8,
                    zorder=2,
                )
            index_partial = [
                np.where(edges == item)[0][0] for item in yearly_LSP_partial
            ]
            if index_partial:
                legend_partial = True
                edges_partial = edges[index_partial]
                count_partial = cumulative_count[index_partial]
                axes[0].scatter(
                    edges_partial - 1,
                    count_partial,
                    marker="^",
                    c=colors[ii[0]],
                    s=25,
                    edgecolors=github_dark,
                    linewidths=0.8,
                    zorder=2,
                )

        if legend_failure:
            axes[0].scatter(
                [],
                [],
                marker="*",
                c="white",
                label="Failure",
                edgecolors="none",
            )
        if legend_partial:
            axes[0].scatter(
                [],
                [],
                marker="^",
                c="white",
                label="Partial",
                edgecolors="none",
            )

        handles, labels = prepare_legend(reverse=False)
        axes[0].legend(
            handles,
            labels,
            loc="upper center",
            ncol=4,
            frameon=False,
            labelcolor="white",
            markerscale=1.4,
        )
        axes[0].set_xticks(
            [datetime(year, i, 1).timetuple().tm_yday for i in range(1, 13)],
            monthsLabels,
        )
        axes[0].set(
            ylabel="Cumulative number of launches",
            xlim=[1, max(days)],
            title="Orbital launch attempts per LSP in " + str(year),
        )
        finish_figure(fig, axes, "yearly/orbitalAttemptsPerLSP/" + str(year), show=show)
    README.close()
    pbar.update()
