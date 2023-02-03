import numpy as np
from matplotlib.ticker import MaxNLocator
from tqdm import tqdm

from Processing import PastFirstStageReuse, PastT0s, PastLSPs
from plotsCodes.PlotFunctions import prepare_legend, finish_figure, dark_figure, reusability_labels, \
    reusability_colors, datetime, timezone, LSPs_dict


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(show=True):
    LSPs = PastLSPs[PastT0s["net"] >= datetime(datetime.now(timezone.utc).year - 2, 1, 1, 0, 0, 0, 0, timezone.utc)][
        "id"].value_counts().index.tolist()
    print('Starting reusability plots by LSP')
    README = open('plots/byLSP/reusability/README.md', 'w')
    README.write('# First stages reusability per LSP since 1957\n')
    for LSP in tqdm(LSPs, desc='LSPs', ncols=80):
        years = PastT0s[PastLSPs["id"] == LSP].net.dt.year.unique().tolist()
        README.write(f"![First stages reusability by {LSPs_dict[LSP]}]({LSPs_dict[LSP].replace(' ', '_')}.png)\n")
        LSP_mask = PastLSPs["id"] == LSP
        new_not_recovered = []
        new_recovered = []
        not_new_not_recovered = []
        not_new_recovered = []
        for year in years:
            year_mask = PastT0s["net"].dt.year == year
            LSP_FirstStageReuseYear = PastFirstStageReuse[LSP_mask & year_mask]
            new_not_recovered.append(LSP_FirstStageReuseYear["NewLost"].sum())
            new_recovered.append(LSP_FirstStageReuseYear["NewRecovered"].sum())
            not_new_not_recovered.append(LSP_FirstStageReuseYear["ReusedLost"].sum())
            not_new_recovered.append(LSP_FirstStageReuseYear["ReusedRecovered"].sum())
        new_recovered = np.array(new_recovered)
        new_not_recovered = np.array(new_not_recovered)
        not_new_recovered = np.array(not_new_recovered)
        not_new_not_recovered = np.array(not_new_not_recovered)
        fig, axes = dark_figure()
        axes[0].bar(years, new_not_recovered, color=reusability_colors[0], label=reusability_labels[0], width=1,
                    align='edge')
        axes[0].bar(years, new_recovered, bottom=new_not_recovered, color=reusability_colors[1],
                    label=reusability_labels[1], width=1, align='edge')
        axes[0].bar(years, not_new_not_recovered, bottom=new_not_recovered + new_recovered, color=reusability_colors[2],
                    label=reusability_labels[2], width=1, align='edge')
        axes[0].bar(years, not_new_recovered, bottom=new_not_recovered + new_recovered + not_new_not_recovered,
                    color=reusability_colors[3], label=reusability_labels[3], width=1, align='edge')

        handles, labels = prepare_legend(reverse=False)
        axes[0].legend(handles, labels, loc='upper center', ncol=2, frameon=False, labelcolor='white')
        axes[0].set(ylabel='Total booster flights', xlim=[min(years), max(years) + 1],
                    title='Reuse of orbital-class boosters by ' + LSPs_dict[LSP] + ' since ' + str(
                        min(years)))
        axes[0].xaxis.set_major_locator(MaxNLocator(integer=True))
        finish_figure(fig, axes,
                      'byLSP/reusability/' + LSPs_dict[LSP].replace(" ", "_").replace("/", "_"),
                      show=show)
    README.close()
