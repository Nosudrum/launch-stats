from datetime import datetime, timezone
from plotsCodes.PlotFunctions import *
from Processing import PastT0s, PastCountries


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(show=True):
    print('Creating of orbital launch attempts per country since 1957 non-stacked')
    F2, F2_axes = dark_figure()
    F2_Years = PastT0s["net"].dt.year.unique().tolist()
    F2_Countries = PastCountries.copy()
    F2_Countries_sorted = F2_Countries["location.country_code"].value_counts().index.tolist()
    F2_Countries_selected = F2_Countries_sorted[0:7]
    F2_Countries[~F2_Countries["location.country_code"].isin(F2_Countries_selected)] = 'OTH'
    F2_Countries_selected.append('OTH')
    F2_data = []
    for Country in F2_Countries_selected:
        F2_data.append(PastT0s[F2_Countries["location.country_code"] == Country]["net"].dt.year.values.tolist())
    F2_Countries_Labels = [Countries_dict[ii] for ii in F2_Countries_selected]
    F2_axes[0].hist(F2_data, bins=np.append(np.unique(F2_Years), max(F2_Years) + 1), histtype='step', stacked=False,
                    label=F2_Countries_Labels, color=colors, linewidth=1.5)
    handles, labels = flip_legend(reverse=True)
    F2_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
    F2_axes[0].set(ylabel='Launches per year', xlim=[min(F2_Years), max(F2_Years) + 1],
                   title='Orbital launch attempts per country since ' + str(min(F2_Years)))
    F2_axes[0].set_xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."),
                          color='dimgray',
                          labelpad=10)
    finish_figure(F2, F2_axes, 'OrbitalAttemptsPerCountry', show=show)
