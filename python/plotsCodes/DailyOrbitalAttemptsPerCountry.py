from Processing import PastDayOfYear, PastCountries
from plotsCodes.PlotFunctions import *


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(pbar, show=True):
    F2, F2_axes = dark_figure()
    # F2_Years = PastT0s["net"].dt.year.unique().tolist()
    F2_Countries = PastCountries.copy()
    F2_Countries_sorted = F2_Countries["location.country_code"].value_counts().index.tolist()
    F2_Countries_selected = F2_Countries_sorted[0:7]
    F2_Countries[~F2_Countries["location.country_code"].isin(F2_Countries_selected)] = 'OTH'
    F2_Countries_selected.append('OTH')
    F2_data = []
    for Country in F2_Countries_selected:
        F2_data.append(PastDayOfYear[F2_Countries["location.country_code"] == Country]["net"].values.tolist())
    F2_Countries_Labels = [Countries_dict[ii] for ii in F2_Countries_selected]
    F2_axes[0].hist(F2_data, bins=np.arange(1, 368), histtype='bar', stacked=True,
                    label=F2_Countries_Labels, color=colors, linewidth=1.5)
    handles, labels = prepare_legend(reverse=False)
    F2_axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
    F2_axes[0].set_xticks(monthsTicks, monthsLabels)
    F2_axes[0].set(ylabel='Launches per day of year', xlim=[1, 367],
                   title='Orbital launch attempts per country per day of year since 1957')
    finish_figure(F2, F2_axes, 'DailyOrbitalAttemptsPerCountry', show=show)
    pbar.update()
