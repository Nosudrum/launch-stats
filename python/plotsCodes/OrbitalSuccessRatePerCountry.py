from matplotlib.cm import ScalarMappable
from tqdm import tqdm

from Processing import PastCountries, PastStatus, PastT0s
from plotsCodes.PlotFunctions import Countries_dict, finish_figure, np, dark_figure, plt


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(show=True):
    Countries_list = PastCountries["location.country_code"].unique().tolist()
    print('Starting launch & success rate plots by country since 1957')
    README = open('plots/byCountry/successRate/README.md', 'w')
    README.write('# Launches and success rate per country since 1957\n')
    Years_list = PastT0s.net.dt.year.unique().tolist()
    success_mask = PastStatus["id"] == 3
    failure_mask = (PastStatus["id"] == 4) | (PastStatus["id"] == 7)
    for Country in tqdm(Countries_list, desc='Countries', ncols=80):
        README.write('![Launches and success rate by ' + Countries_dict[Country] + ' since 1957](' + Countries_dict[
            Country].replace(" ", "_").replace("/", "_") + '.png)\n')
        country_mask = PastCountries["location.country_code"] == Country
        data = np.empty((len(Years_list), 2))
        for year in Years_list:
            successes = ((PastT0s["net"].dt.year == year) & success_mask & country_mask).sum()
            failures = ((PastT0s["net"].dt.year == year) & failure_mask & country_mask).sum()
            if successes + failures == 0:
                success_rate_country = np.NaN
            else:
                success_rate_country = 100.0 * successes / (successes + failures)
            data[year - Years_list[0], :] = [successes + failures, success_rate_country]
        data_color = data[:, 1] / 100
        colormap = plt.cm.get_cmap('RdYlGn')
        fig, axes = dark_figure()
        axes[0].bar(Years_list, data[:, 0], color=colormap(data_color), width=1)
        axes[0].set(ylabel='Launches per year', xlim=[min(Years_list) - 0.5, max(Years_list) + 0.5],
                    title='Orbital launch attempts by ' + Countries_dict[Country] + ' since 1957')
        sm = ScalarMappable(cmap=colormap, norm=plt.Normalize(vmin=0, vmax=100))
        sm.set_array([])
        cax = axes[0].inset_axes([0.05, 0.9, 0.9, 0.035])
        cbar = fig.colorbar(sm, orientation="horizontal", cax=cax)
        cbar.ax.set_title('Yearly success rate', color='white', fontsize=8)
        finish_figure(fig, axes, 'byCountry/successRate/' + Countries_dict[Country].replace(" ", "_").replace("/", "_"),
                      show=show, colorbar=cbar)
    README.close()
