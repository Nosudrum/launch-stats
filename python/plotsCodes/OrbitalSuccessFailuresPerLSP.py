from matplotlib.ticker import MaxNLocator

from Processing import PastStatus, PastT0s, PastLSPs
from plotsCodes.PlotFunctions import prepare_legend, finish_figure, np, dark_figure, SPF_colors, \
    SPF_labels, datetime, timezone, LSPs_dict, flatten


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(show=True):
    LSPs = PastLSPs[PastT0s["net"] >= datetime(datetime.now(timezone.utc).year - 7, 1, 1, 0, 0, 0, 0, timezone.utc)][
        "id"].value_counts().index.tolist()
    print('Starting launch successes & failures plots by LSP since 1957')
    README = open('plots/byLSP/successFailures/README.md', 'w')
    README.write('# Launch successes and failures per LSP since 1957\n')
    years = PastT0s.net.dt.year.unique().tolist()
    success_mask = PastStatus["id"] == 3
    partial_mask = PastStatus["id"] == 7
    failure_mask = PastStatus["id"] == 4
    for LSP in LSPs:
        print(LSPs_dict[LSP])

        LSP_mask = PastLSPs["id"] == LSP
        successes = PastT0s[success_mask & LSP_mask]
        partial = PastT0s[partial_mask & LSP_mask]
        failures = PastT0s[failure_mask & LSP_mask]
        data = [successes["net"].dt.year.values.tolist(), partial["net"].dt.year.values.tolist(),
                failures["net"].dt.year.values.tolist()]
        first_year = min(flatten(data))
        last_year = max(flatten(data))
        fig, axes = dark_figure()
        README.write(f'![Launch successes and failures by {LSPs_dict[LSP]} since {first_year}]('
                     + LSPs_dict[LSP].replace(" ", "_") + '.png)\n')
        axes[0].hist(data, bins=np.append(years, max(years) + 1), histtype='bar', stacked=True,
                     label=SPF_labels, color=SPF_colors)
        handles, labels = prepare_legend(reverse=False)
        axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
        axes[0].set(ylabel='Total launches per year', xlim=[first_year, last_year + 1],
                    title=f'Outcome of orbital launch attempts by {LSPs_dict[LSP]} since {first_year}')
        axes[0].xaxis.set_major_locator(MaxNLocator(integer=True))
        finish_figure(fig, axes,
                      'byLSP/successFailures/' + LSPs_dict[LSP].replace(" ", "_").replace("/", "_"),
                      show=show)
    README.close()
    print('Done with launch successes & failures plots by LSP since 1957')
