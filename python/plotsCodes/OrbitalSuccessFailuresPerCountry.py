from tqdm import tqdm

from Processing import PastCountries, PastStatus, PastT0s
from plotsCodes.PlotFunctions import prepare_legend, Countries_dict, finish_figure, np, dark_figure, SPF_colors, \
    SPF_labels


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(show=True):
    Countries_list = PastCountries["location.country_code"].unique().tolist()
    print('Starting launch successes & failures plots by country since 1957')
    README = open('plots/byCountry/successFailures/README.md', 'w')
    README.write('# Launch successes and failures per country since 1957\n')
    years = PastT0s.net.dt.year.unique().tolist()
    success_mask = PastStatus["id"] == 3
    partial_mask = PastStatus["id"] == 7
    failure_mask = PastStatus["id"] == 4
    for Country in tqdm(Countries_list, desc='Countries', ncols=80):
        README.write('![Launch successes and failures by ' + Countries_dict[Country] + ' since 1957](' + Countries_dict[
            Country].replace(" ", "_").replace("/", "_") + '.png)\n')
        country_mask = PastCountries["location.country_code"] == Country
        successes = PastT0s[success_mask & country_mask]
        partial = PastT0s[partial_mask & country_mask]
        failures = PastT0s[failure_mask & country_mask]
        data = [successes["net"].dt.year.values.tolist(), partial["net"].dt.year.values.tolist(),
                failures["net"].dt.year.values.tolist()]
        fig, axes = dark_figure()
        axes[0].hist(data, bins=np.append(years, max(years) + 1), histtype='bar', stacked=True,
                     label=SPF_labels, color=SPF_colors)
        handles, labels = prepare_legend(reverse=False)
        axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
        axes[0].set(ylabel='Total launches per year', xlim=[min(years), max(years) + 1],
                    title='Outcome of orbital launch attempts by ' + Countries_dict[Country] + ' since ' + str(
                        min(years)))
        finish_figure(fig, axes,
                      'byCountry/successFailures/' + Countries_dict[Country].replace(" ", "_").replace("/", "_"),
                      show=show)
    README.close()
