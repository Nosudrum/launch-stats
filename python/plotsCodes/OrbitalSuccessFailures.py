from Processing import PastStatus, PastT0s
from plotsCodes.PlotFunctions import prepare_legend, finish_figure, np, dark_figure, SPF_colors, \
    SPF_labels


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(show=True):
    print('Starting launch successes & failures plot since 1957')
    years = PastT0s.net.dt.year.unique().tolist()
    success_mask = PastStatus["id"] == 3
    partial_mask = PastStatus["id"] == 7
    failure_mask = PastStatus["id"] == 4
    successes = PastT0s[success_mask]
    partial = PastT0s[partial_mask]
    failures = PastT0s[failure_mask]
    data = [successes["net"].dt.year.values.tolist(), partial["net"].dt.year.values.tolist(),
            failures["net"].dt.year.values.tolist()]
    fig, axes = dark_figure()
    axes[0].hist(data, bins=np.append(years, max(years) + 1), histtype='bar', stacked=True,
                 label=SPF_labels, color=SPF_colors)
    handles, labels = prepare_legend(reverse=False)
    axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
    axes[0].set(ylabel='Total launches per year', xlim=[min(years), max(years) + 1],
                title='Outcome of orbital launch attempts since ' + str(min(years)))
    finish_figure(fig, axes, "successFailures", show=show)
