from datetime import datetime, timezone
from plotsCodes.PlotFunctions import *
from Processing import PastDayOfYear, PastStatus
from matplotlib.cm import ScalarMappable


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(show=True):
    print('Creating plot of daily orbital success rate since 1957')
    F2, F2_axes = dark_figure()
    F2_data = np.empty((366, 4))
    for day in np.arange(1, 367):
        successes = ((PastStatus.id == 3) & (PastDayOfYear.net == day)).sum()
        failures = (((PastStatus.id == 4) | (PastStatus.id == 7)) & (PastDayOfYear.net == day)).sum()
        success_rate = 100 * successes / (successes + failures)
        F2_data[day - 1, :] = [day, successes, failures, success_rate]
    attempts = F2_data[:, 1] + F2_data[:, 2]
    data_color = attempts / max(attempts)
    my_cmap = plt.cm.get_cmap('YlGnBu')
    F2_axes[0].bar(F2_data[:, 0], F2_data[:, 3], color=my_cmap(data_color), width=1)
    F2_axes[0].set_xticks(monthsTicks, monthsLabels)
    F2_axes[0].set(ylabel='Success rate per day of year [%]', xlim=[1, 367],
                   title='Orbital success rate per day of year since 1957')
    F2_axes[0].set_xlabel(datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."),
                          color='dimgray',
                          labelpad=10)
    sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(vmin=0, vmax=10 * ceil(max(attempts) / 10)))
    sm.set_array([])
    cax = F2_axes[0].inset_axes([0.05, 0.9, 0.9, 0.035])
    cbar = F2.colorbar(sm, orientation="horizontal", cax=cax)
    cbar.ax.set_title('Total attempts per day of year since 1957', color='white', fontsize=8)
    finish_figure(F2, F2_axes, 'DailyOrbitalSuccessRate', show=show, override_ylim=[0, 120],
                  override_yticks=[0, 25, 50, 75, 100], colorbar=cbar)
