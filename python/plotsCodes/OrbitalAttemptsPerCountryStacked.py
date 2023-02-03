from Processing import PastT0s, PastCountries
from plotsCodes.PlotFunctions import dark_figure, prepare_legend, finish_figure, colors, Countries_dict, np


# Plot of orbital launch attempts per country since 1957 stacked
def main(pbar, show=True):
    F1, F1_axes = dark_figure()
    F1_Years = PastT0s["net"].dt.year.unique().tolist()
    F1_Countries = PastCountries.copy()
    F1_Countries_sorted = F1_Countries["location.country_code"].value_counts().index.tolist()
    F1_Countries_selected = F1_Countries_sorted[0:7]
    F1_Countries[~F1_Countries["location.country_code"].isin(F1_Countries_selected)] = 'OTH'
    F1_Countries_selected.append('OTH')
    F1_data = []
    for Country in F1_Countries_selected:
        F1_data.append(PastT0s[F1_Countries["location.country_code"] == Country]["net"].dt.year.values.tolist())
    F1_Countries_Labels = [Countries_dict[ii] for ii in F1_Countries_selected]
    F1_axes[0].hist(F1_data, bins=np.append(np.unique(F1_Years), max(F1_Years) + 1), histtype='bar', stacked=True,
                    label=F1_Countries_Labels, color=colors)
    handles, labels = prepare_legend(reverse=False)
    F1_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
    F1_axes[0].set(ylabel='Total launches per year', xlim=[min(F1_Years), max(F1_Years) + 1],
                   title='Orbital launch attempts per country since ' + str(min(F1_Years)))
    finish_figure(F1, F1_axes, 'OrbitalAttemptsPerCountryStacked', show=show)
    pbar.update()
