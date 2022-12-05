from Processing import PastStatus, PastT0s, PastLSPs
from plotsCodes.PlotFunctions import prepare_legend, finish_figure, np, dark_figure, SPF_colors, \
    SPF_labels, datetime, timezone, LSPs_dict


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
        README.write('![Launch successes and failures by ' + LSPs_dict[LSP] + ' since 1957]('
                     + LSPs_dict[LSP].replace(" ", "_") + '.png)\n')
        LSP_mask = PastLSPs["id"] == LSP
        successes = PastT0s[success_mask & LSP_mask]
        partial = PastT0s[partial_mask & LSP_mask]
        failures = PastT0s[failure_mask & LSP_mask]
        data = [successes["net"].dt.year.values.tolist(), partial["net"].dt.year.values.tolist(),
                failures["net"].dt.year.values.tolist()]
        fig, axes = dark_figure()
        axes[0].hist(data, bins=np.append(years, max(years) + 1), histtype='bar', stacked=True,
                     label=SPF_labels, color=SPF_colors)
        handles, labels = prepare_legend(reverse=False)
        axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
        axes[0].set(ylabel='Total launches per year', xlim=[min(years), max(years) + 1],
                    title='Outcome of orbital launch attempts by ' + LSPs_dict[LSP] + ' since ' + str(
                        min(years)))
        finish_figure(fig, axes,
                      'byLSP/successFailures/' + LSPs_dict[LSP].replace(" ", "_").replace("/", "_"),
                      show=show)
    README.close()
    print('Done with launch successes & failures plots by LSP since 1957')
