from Processing import PastT0s, PastLSPs
from plotsCodes.PlotFunctions import (
    dark_figure,
    prepare_legend,
    finish_figure,
    colors,
    LSPs_dict,
    np,
)


# Plot of orbital launch attempts per LSP since 1957 stacked
def main(pbar, show=True):
    F3_Years = PastT0s["net"].dt.year.unique().tolist()
    F3, F3_axes = dark_figure()
    F3_LSPs = PastLSPs.copy()
    F3_LSPs_sorted = F3_LSPs["id"].value_counts().index.tolist()
    F3_LSPs_selected = F3_LSPs_sorted[0:7]
    F3_LSPs[~F3_LSPs["id"].isin(F3_LSPs_selected)] = 0
    F3_LSPs_selected.append(0)
    F3_data = []
    for LSP in F3_LSPs_selected:
        F3_data.append(PastT0s[F3_LSPs["id"] == LSP]["net"].dt.year.values.tolist())
    F3_LSPs_Labels = [LSPs_dict[ii] for ii in F3_LSPs_selected]
    F3_axes[0].hist(
        F3_data,
        bins=np.append(F3_Years, max(F3_Years) + 1),
        histtype="bar",
        stacked=True,
        label=F3_LSPs_Labels,
        color=colors,
    )
    handles, labels = prepare_legend(reverse=False)
    F3_axes[0].legend(
        handles, labels, loc="upper center", ncol=4, frameon=False, labelcolor="white"
    )
    F3_axes[0].set(
        ylabel="Total launches per year",
        xlim=[min(F3_Years), max(F3_Years) + 1],
        title="Orbital launch attempts per LSP since " + str(min(F3_Years)),
    )
    finish_figure(F3, F3_axes, "OrbitalAttemptsPerLSPStacked", show=show)
    pbar.update()
