# Preamble
import plotsCodes
from tqdm import tqdm


def generate_plots(show):
    pbar = tqdm(total=33, desc="Plots", ncols=80, position=0, leave=True)

    # Main plots
    plotsCodes.OrbitalAttemptsPerCountryStacked.main(pbar, show=show)
    plotsCodes.OrbitalAttemptsPerCountry.main(pbar, show=show)
    plotsCodes.OrbitalAttemptsPerLSPStacked.main(pbar, show=show)
    plotsCodes.OrbitalAttemptsPerLSP.main(pbar, show=show)
    plotsCodes.OrbitalAttemptsPerLSPStacked.main(pbar, show=show)
    plotsCodes.OrbitalAttemptsPerLSPType.main(pbar, show=show)
    plotsCodes.OrbitalAttemptsPerLSPTypeStacked.main(pbar, show=show)
    plotsCodes.DailyOrbitalAttemptsPerCountry.main(pbar, show=show)
    plotsCodes.DailyOrbitalFailuresPerCountry.main(pbar, show=show)
    plotsCodes.DailyOrbitalSuccessRate.main(pbar, show=show)
    plotsCodes.OrbitalFailuresPerCountry.main(pbar, show=show)
    plotsCodes.LaunchCadenceWorldwide.main(pbar, show=show)
    plotsCodes.LaunchCadenceWorldwidePrediction.main(pbar, show=show)
    plotsCodes.LaunchCadenceWorldwidePredictionLinear.main(pbar, show=show)
    plotsCodes.OrbitalFailuresPerCountryStacked.main(pbar, show=show)
    plotsCodes.OrbitalSuccessFailures.main(pbar, show=show)
    plotsCodes.DailyConsecutiveYears.main(pbar, show=show)
    plotsCodes.MaidenFlights.main(pbar, show=show)
    plotsCodes.TotalOrbitalAttemptsPerCountry.main(pbar, show=show)

    # Plots per Country
    plotsCodes.LaunchCadenceByCountry.main(pbar, show=False)
    plotsCodes.OrbitalSuccessRatePerCountry.main(pbar, show=False)
    plotsCodes.OrbitalSuccessFailuresPerCountry.main(pbar, show=False)
    plotsCodes.LaunchCadenceByCountryPrediction.main(pbar, show=False)
    plotsCodes.LaunchCadenceByCountryLinear.main(pbar, show=False)

    # Plots per LSP
    plotsCodes.LaunchCadenceByLSP.main(pbar, show=False)
    plotsCodes.LaunchCadenceByLSPprediction.main(pbar, show=False)
    plotsCodes.OrbitalSuccessFailuresPerLSP.main(pbar, show=False)
    plotsCodes.LaunchCadenceByLSPpredictionLinear.main(pbar, show=False)
    plotsCodes.OrbitalReusabilityPerLSP.main(pbar, show=False)

    # Plots per Launcher Family
    plotsCodes.OrbitalSuccessFailuresPerLauncherFamily.main(pbar, show=False)

    # Yearly plots
    plotsCodes.YearlyOrbitalAttemptsPerCountry.main(pbar, show=False)
    plotsCodes.YearlyOrbitalAttemptsPerLSP.main(pbar, show=False)

    # Plotly plots
    plotsCodes.PlotlyOrbitalAttemptsPerCountry.main(pbar)
    plotsCodes.PlotlyOrbitalAttemptsPerLSP.main(pbar)

    pbar.close()

    print("Successfully generated and exported all plots.")


if __name__ == "__main__":
    generate_plots(True)
