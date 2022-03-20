import numpy as np
import matplotlib.ticker as ticker
from datetime import datetime, timezone
from plotsCodes.PlotFunctions import dark_figure, flip_legend, finish_figure, colors
from Processing import PastT0s, PastLSPs


# Plot of orbital launch attempts per LSP type since 1957 stacked
def main(show=True):
    print('Creating of orbital launch attempts per LSP type since 1957 stacked')
    F3_Years = PastT0s["net"].dt.year.unique().tolist()
    F3, F3_axes = dark_figure()
    F3_LSPs = PastLSPs.copy()
    F3_LSPs.loc[F3_LSPs["type"] == 'Multinational', "type"] = 'Government'
    F3_LSPs_types = F3_LSPs["type"].unique().tolist()
    F3_data = []
    for LSP_type in F3_LSPs_types:
        F3_data.append(PastT0s[F3_LSPs["type"] == LSP_type]["net"].dt.year.values.tolist())
    F3_axes[0].hist(F3_data, bins=np.append(F3_Years, max(F3_Years) + 1), histtype='bar', stacked=True,
                    label=F3_LSPs_types, color=colors[0:len(F3_LSPs_types)])
    handles, labels = flip_legend(reverse=False)
    F3_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
    F3_axes[0].set(ylabel='Total launches per year', ylim=[0, 160], xlim=[min(F3_Years), max(F3_Years) + 1],
                   title='Orbital launch attempts per LSP type since ' + str(min(F3_Years)))
    F3_axes[0].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    F3_axes[0].set_xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."),
                          color='dimgray', labelpad=10)
    finish_figure(F3, 'OrbitalAttemptsPerLSPTypeStacked', show=show)
