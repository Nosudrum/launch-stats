from Processing import PastDayOfYear, PastT0s
from plotsCodes.PlotFunctions import *
from calendar import isleap
from tqdm import tqdm


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(pbar, show=True):
    fig, axes = dark_figure()

    PastYears = PastT0s.net.dt.year.copy().to_frame().rename(columns={"net": "year"})
    PastDays = PastDayOfYear.copy().rename(columns={"net": "dayOfYear"})

    currentYear = datetime.now(timezone.utc).year
    currentDayOfYear = datetime.now(tz=timezone.utc).timetuple().tm_yday
    if not isleap(currentYear) and currentDayOfYear >= 60:
        currentDayOfYear += 1

    def find_previous_leap_year(year, current_valid):
        if isleap(year):
            if current_valid:
                return year
            else:
                year -= 1
        else:
            while not isleap(year):
                year -= 1
            return year

    daysVector = np.arange(1, 367, 1).tolist()
    consecutiveYearsVector = []
    for dayOfYear in tqdm(daysVector, desc="Day of year", position=1, leave=False):
        if dayOfYear == 60:  # February 29th
            if (
                dayOfYear > currentDayOfYear
            ):  # Last time this day happened was in the previous **leap** year
                startYear = find_previous_leap_year(currentYear, current_valid=False)
            else:  # Last time this day happened was in the previous OR current **leap** year
                startYear = find_previous_leap_year(currentYear, current_valid=True)
        else:  # All other days
            if (
                dayOfYear > currentDayOfYear
            ):  # Last time this day happened was in the previous year
                startYear = currentYear - 1
            else:  # Last time this day happened was in the current year
                startYear = currentYear
        consecutiveYears = 0
        consecutive = True
        evaluatedYear = startYear
        while consecutive:
            if evaluatedYear in PastYears[PastDays.dayOfYear == dayOfYear].year.values:
                consecutiveYears += 1
                if dayOfYear == 60:
                    evaluatedYear = find_previous_leap_year(
                        evaluatedYear, current_valid=False
                    )
                else:
                    evaluatedYear -= 1
            else:
                consecutive = False
        consecutiveYearsVector.append(consecutiveYears)

    axes[0].bar(
        daysVector, consecutiveYearsVector, color=colors[0], linewidth=0, width=1
    )

    axes[0].set_xticks(monthsTicks, monthsLabels)
    axes[0].set(
        ylabel="Consecutive years",
        xlim=[1, 367],
        title="Consecutive years with an orbital launch attempts per day of year",
    )
    finish_figure(fig, axes, "DailyConsecutiveYears", show=show)
    pbar.update()
