from matplotlib.ticker import MaxNLocator
from tqdm import tqdm

from Processing import PastStatus, PastT0s, PastLauncherFamily
from plotsCodes.PlotFunctions import (
    prepare_legend,
    finish_figure,
    np,
    dark_figure,
    SPF_colors,
    SPF_labels,
    flatten,
)


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(pbar, show=True):
    Families_list = PastLauncherFamily.unique().tolist()
    Families_list.sort()
    Families_list.remove("")
    README = open("plots/byLauncherFamily/successFailures/README.md", "w")
    README.write("# Launch successes and failures per launcher family since 1957\n")
    years = PastT0s.net.dt.year.unique().tolist()
    success_mask = PastStatus["id"] == 3
    partial_mask = PastStatus["id"] == 7
    failure_mask = PastStatus["id"] == 4
    for Family in tqdm(
        Families_list, desc="Launcher Families", ncols=80, position=1, leave=False
    ):
        family_mask = PastLauncherFamily == Family
        successes = PastT0s[success_mask & family_mask]
        partial = PastT0s[partial_mask & family_mask]
        failures = PastT0s[failure_mask & family_mask]
        data = [
            successes["net"].dt.year.values.tolist(),
            partial["net"].dt.year.values.tolist(),
            failures["net"].dt.year.values.tolist(),
        ]
        first_year = min(flatten(data))
        last_year = max(flatten(data))
        README.write(
            f"![Launch successes and failures of the {Family} family since {first_year}]("
            + Family.replace(" ", "_").replace("/", "_")
            + ".png)\n"
        )
        fig, axes = dark_figure()
        axes[0].hist(
            data,
            bins=np.append(years, max(years) + 1),
            histtype="bar",
            stacked=True,
            label=SPF_labels,
            color=SPF_colors,
        )
        handles, labels = prepare_legend(reverse=False)
        axes[0].legend(
            handles,
            labels,
            loc="upper center",
            ncol=4,
            frameon=False,
            labelcolor="white",
        )
        axes[0].set(
            ylabel="Total launches per year",
            xlim=[first_year, last_year + 1],
            title=f"Outcome of orbital launch attempts by the {Family} family since {first_year}",
        )
        axes[0].xaxis.set_major_locator(MaxNLocator(integer=True))
        finish_figure(
            fig,
            axes,
            "byLauncherFamily/successFailures/"
            + Family.replace(" ", "_").replace("/", "_"),
            show=show,
        )
    README.close()
    pbar.update()
