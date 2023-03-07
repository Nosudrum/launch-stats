import calendar

from tqdm import tqdm
from Processing import PastT0s, PastCountries, PastStatus
from plotsCodes.PlotFunctions import (
    Countries_dict,
    dark_figure,
    finish_figure,
    prepare_legend,
    colors,
    monthsLabels,
    datetime,
    timezone,
    np,
    github_dark,
)


# Plot of orbital launch attempts per country per year since 1957
def main(pbar, show=False):
    README = open("plots/yearly/orbitalAttemptsPerCountry/README.md", "w")
    README.write("# Orbital attempts per country for every year since 1957\n")
    Countries_dict_tmp = Countries_dict.copy()
    Countries = PastCountries.copy()
    Countries_sorted = Countries["location.country_code"].value_counts().index.tolist()
    Countries_selected = Countries_sorted[0:7]
    Countries[~Countries["location.country_code"].isin(Countries_selected)] = "OTH"
    Countries_selected.append("OTH")
    for year in tqdm(
        range(1957, datetime.now(timezone.utc).year + 1),
        desc="Years",
        ncols=80,
        position=1,
        leave=False,
    ):
        README.write(
            "![Orbital attempts per country in "
            + str(year)
            + "]("
            + str(year)
            + ".png)\n"
        )
        days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
        if year > 1991:
            Countries_dict_tmp["RUS"] = "Russia"
        else:
            Countries_dict_tmp["RUS"] = "USSR"
        if year > 1957:
            del fig
        fig, axes = dark_figure()
        T0s = PastT0s[PastT0s["net"].dt.year == year].copy()
        Countries_yearly = (
            PastCountries[PastT0s["net"].dt.year == year]["location.country_code"]
            .to_frame()
            .copy()
        )
        Countries_yearly[
            ~Countries_yearly["location.country_code"].isin(Countries_selected)
        ] = "OTH"
        if year == datetime.now(timezone.utc).year:
            bins = np.arange(
                days[0], datetime.now(timezone.utc).timetuple().tm_yday + 2
            )
        else:
            bins = np.append(days, max(days) + 1)
        legend_failure = False
        legend_partial = False
        for ii in enumerate(Countries_selected):
            yearly_country_dayofyear = T0s[
                Countries_yearly["location.country_code"] == ii[1]
            ]["net"].dt.dayofyear.to_list()
            yearly_country_failure = T0s.loc[
                (Countries_yearly["location.country_code"] == ii[1])
                & (PastStatus["id"] == 4)
            ]["net"].dt.dayofyear.to_list()
            yearly_country_partial = T0s.loc[
                (Countries_yearly["location.country_code"] == ii[1])
                & (PastStatus["id"] == 7)
            ]["net"].dt.dayofyear.to_list()
            if yearly_country_dayofyear:
                count, edges = np.histogram(yearly_country_dayofyear, bins=bins)
                cumulative_count = count.cumsum()

                axes[0].step(
                    edges[:-1],
                    cumulative_count,
                    linewidth=1.2,
                    color=colors[ii[0]],
                    label=Countries_dict_tmp[ii[1]],
                    zorder=1,
                )

                index_failure = [
                    np.where(edges == item)[0][0] for item in yearly_country_failure
                ]
                # [edges.index(item) for item in yearly_country_failure]
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
                    np.where(edges == item)[0][0] for item in yearly_country_partial
                ]
                # [edges.index(item) for item in yearly_country_partial]
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
                label="Partial Failure",
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
            title="Orbital launch attempts per country in " + str(year),
        )
        finish_figure(
            fig, axes, "yearly/orbitalAttemptsPerCountry/" + str(year), show=show
        )
    README.close()
    pbar.update()
