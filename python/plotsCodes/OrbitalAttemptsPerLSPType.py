from Processing import PastT0s, PastLSPs
from plotsCodes.PlotFunctions import (
    dark_figure,
    prepare_legend,
    finish_figure,
    colors,
    np,
)


# Plot of orbital launch attempts per LSP type since 1957 non-stacked
def main(pbar, show=True):
    F3_Years = PastT0s["net"].dt.year.unique().tolist()
    F3, F3_axes = dark_figure()
    F3_LSPs = PastLSPs.copy()
    F3_LSPs.loc[F3_LSPs["type"] == "Multinational", "type"] = "Government"
    F3_LSPs_types = F3_LSPs["type"].unique().tolist()
    F3_data = []
    for LSP_type in F3_LSPs_types:
        F3_data.append(
            PastT0s[F3_LSPs["type"] == LSP_type]["net"].dt.year.values.tolist()
        )
    F3_axes[0].hist(
        F3_data,
        bins=np.append(F3_Years, max(F3_Years) + 1),
        histtype="step",
        stacked=False,
        label=F3_LSPs_types,
        color=colors[0 : len(F3_LSPs_types)],
        linewidth=1.5,
    )
    handles, labels = prepare_legend(reverse=True)
    F3_axes[0].legend(
        handles, labels, loc="upper center", ncol=4, frameon=False, labelcolor="white"
    )
    F3_axes[0].set(
        ylabel="Launches per year",
        xlim=[min(F3_Years), max(F3_Years) + 1],
        title="Orbital launch attempts per LSP type since " + str(min(F3_Years)),
    )
    finish_figure(F3, F3_axes, "OrbitalAttemptsPerLSPType", show=show)
    pbar.update()
