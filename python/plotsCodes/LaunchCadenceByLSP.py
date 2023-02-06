import calendar

from tqdm import tqdm

from Processing import PastT0s, PastLSPs
from plotsCodes.PlotFunctions import (
    LSPs_dict,
    colors,
    monthsLabels,
    dark_figure,
    finish_figure,
    prepare_legend,
    datetime,
    timezone,
    np,
)


# Plot of orbital launch attempts by LSP for the last 8 years
def main(pbar, show=False):
    F4_LSPs = (
        PastLSPs[
            PastT0s["net"]
            >= datetime(
                datetime.now(timezone.utc).year - 7, 1, 1, 0, 0, 0, 0, timezone.utc
            )
        ]["id"]
        .value_counts()
        .index.tolist()
    )

    F4_README = open("plots/byLSP/launchCadence8years/README.md", "w")
    F4_README.write("# Orbital attempts per LSP for the last 8 years\n")
    for LSP in tqdm(F4_LSPs, desc="LSPs", ncols=80, position=1, leave=False):
        F4_README.write(
            "![Orbital attempts by "
            + LSPs_dict[LSP]
            + " in the last 8 years]("
            + LSPs_dict[LSP].replace(" ", "_")
            + ".png)\n"
        )
        F4, F4_axes = dark_figure()
        F4_LSP_T0s = PastT0s[PastLSPs["id"] == LSP].copy()
        year_id = -1
        for year in range(
            datetime.now(timezone.utc).year, datetime.now(timezone.utc).year - 8, -1
        ):
            year_id += 1
            F4_LSP_T0s_yearly = F4_LSP_T0s[F4_LSP_T0s["net"].dt.year == year][
                "net"
            ].dt.dayofyear.to_list()
            days = list(range(1, 1 + (366 if calendar.isleap(year) else 365)))
            if year == datetime.now(timezone.utc).year:
                F4_bins = np.arange(
                    days[0], datetime.now(timezone.utc).timetuple().tm_yday + 2
                )
            else:
                F4_bins = np.append(days, max(days) + 1)
            if F4_LSP_T0s_yearly:
                count, edges = np.histogram(F4_LSP_T0s_yearly, bins=F4_bins)
                F4_axes[0].step(
                    edges[:-1],
                    count.cumsum(),
                    linewidth=1.5,
                    color=colors[year_id],
                    label=year,
                )
        handles, labels = prepare_legend(reverse=False)
        F4_axes[0].legend(
            handles,
            labels,
            loc="upper center",
            ncol=4,
            frameon=False,
            labelcolor="white",
        )
        F4_axes[0].set_xticks(
            [
                datetime(datetime.now(timezone.utc).year, i, 1).timetuple().tm_yday
                for i in range(1, 13)
            ],
            monthsLabels,
        )
        F4_axes[0].set(
            ylabel="Cumulative number of launches",
            xlim=[1, 365],
            title="Orbital launch attempts by "
            + LSPs_dict[LSP]
            + " over the last "
            + str(datetime.now(timezone.utc).year - int(labels[-1]) + 1)
            + " years",
        )
        finish_figure(
            F4,
            F4_axes,
            "byLSP/launchCadence8years/" + LSPs_dict[LSP].replace(" ", "_"),
            show=show,
        )
    F4_README.close()
    pbar.update()
