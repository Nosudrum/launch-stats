import matplotlib.pyplot as plt

from Processing import PastT0s, PastCountries
from plotsCodes.PlotFunctions import dark_figure, prepare_legend, finish_figure, colors, Countries_dict
from calendar import isleap


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(pbar, show=True):
    fig, axes = dark_figure(grid=True)

    countries = PastCountries.copy()
    countries_sorted = countries["location.country_code"].value_counts().index.tolist()
    countries_selected = countries_sorted[0:7]
    countries[~countries["location.country_code"].isin(countries_selected)] = 'OTH'
    countries_selected.append('OTH')
    countries_labels = [Countries_dict[ii] for ii in countries_selected]
    for Country in enumerate(countries_selected):
        y_data = PastT0s[countries["location.country_code"] == Country[1]]["net"].copy().reset_index(
            drop=True).index.values.tolist()
        years = PastT0s[countries["location.country_code"] == Country[1]]["net"].dt.year.values
        fractional_years = None
        for year in years:
            if isleap(year):
                fractional_years = PastT0s[countries["location.country_code"] == Country[1]][
                                       "net"].dt.dayofyear.values / 366
            else:
                fractional_years = PastT0s[countries["location.country_code"] == Country[1]][
                                       "net"].dt.dayofyear.values / 365
        x_data = (years + fractional_years).tolist()
        axes[0].step(x_data, y_data, label=countries_labels[Country[0]], color=colors[Country[0]], linewidth=1.5)

    handles, labels = prepare_legend(reverse=False)
    axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
    axes[0].set(ylabel='Total attempts', xlim=[1957, max(PastT0s.net.dt.year) + 1],
                title='Total orbital launch attempts per country since 1957')
    finish_figure(fig, axes, 'TotalOrbitalAttemptsPerCountry', show=show)
    pbar.update()
