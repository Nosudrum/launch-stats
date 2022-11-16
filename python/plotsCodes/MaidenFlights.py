from Processing import PastRocket, PastT0s
from plotsCodes.PlotFunctions import flip_legend, finish_figure, np, dark_figure, colors, datetime, timezone


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(show=True):
    print('Starting maiden flights plot since 1957')
    data = PastRocket[
        ["configuration.name", "configuration.family", "configuration.id"]].copy().rename(
        columns={"configuration.name": "name", "configuration.family": "family",
                 "configuration.id": "id"}).drop_duplicates()
    current_year = datetime.now(timezone.utc).year
    families_found = []
    maiden_flights_newFamily = []
    maiden_flights_oldFamily = []
    for _, row in data.iterrows():
        mf_year = PastT0s[PastRocket["configuration.id"] == row["id"]]["net"].min().year
        if row["family"] in families_found:
            maiden_flights_oldFamily.append(mf_year)
        else:
            maiden_flights_newFamily.append(mf_year)
            families_found.append(row["family"])
    fig, axes = dark_figure()
    axes[0].hist([maiden_flights_newFamily, maiden_flights_oldFamily], bins=np.arange(1957, current_year + 2),
                 histtype='bar', stacked=True, label=["New rocket family", "Existing rocket family"],
                 color=colors[0:2])
    handles, labels = flip_legend(reverse=False)
    axes[0].legend(handles, labels, loc='upper center', ncol=4, frameon=False, labelcolor='white')
    axes[0].set(ylabel='Maiden flights per year', xlim=[1957, current_year + 1],
                title='Maiden flights of new launch vehicles per year since 1957')
    finish_figure(fig, axes, "maidenFlights", show=show)
