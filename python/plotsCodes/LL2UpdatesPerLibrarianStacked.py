from Processing import Updates
from plotsCodes.PlotFunctions import (
    dark_figure,
    prepare_legend,
    finish_figure,
    colors,
    Librarians_dict,
    np,
)


# Plot of orbital launch attempts per LSP since 1957 stacked
def main(pbar, show=True):
    created_on = Updates["created_on"]
    years = created_on.dt.year.unique().tolist()
    years.sort()
    fig, axes = dark_figure()
    librarians = Updates["created_by"].copy()
    librarians_sorted = librarians.value_counts().index.tolist()
    librarians_selected = librarians_sorted[0:7]
    librarians[~librarians.isin(librarians_selected)] = 0
    librarians_selected.append(0)
    data = []
    for librarian in librarians_selected:
        data.append(created_on.loc[librarians == librarian].dt.year.values.tolist())
    librarians_labels = [Librarians_dict[ii] for ii in librarians_selected]
    axes[0].hist(
        data,
        bins=np.append(years, max(years) + 1),
        histtype="bar",
        stacked=True,
        label=librarians_labels,
        color=colors,
    )
    handles, labels = prepare_legend(reverse=False)
    axes[0].legend(
        handles, labels, loc="upper center", ncol=4, frameon=False, labelcolor="white"
    )
    axes[0].set(
        ylabel="Total updates per year",
        xlim=[min(years), max(years) + 1],
        title="LL2 updates per librarian since " + str(min(years)),
    )
    finish_figure(fig, axes, "LL2UpdatesPerLibrarianStacked", show=show)
    pbar.update()
