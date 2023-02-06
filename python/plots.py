# Preamble
import plotsCodes
from tqdm import tqdm

pbar = tqdm(total=33, desc="Plots", ncols=80, position=0, leave=True)

# Main plots
plotsCodes.OrbitalAttemptsPerCountryStacked.main(pbar, show=True)
plotsCodes.OrbitalAttemptsPerCountry.main(pbar, show=True)
plotsCodes.OrbitalAttemptsPerLSPStacked.main(pbar, show=True)
plotsCodes.OrbitalAttemptsPerLSP.main(pbar, show=True)
plotsCodes.OrbitalAttemptsPerLSPStacked.main(pbar, show=True)
plotsCodes.OrbitalAttemptsPerLSPType.main(pbar, show=True)
plotsCodes.OrbitalAttemptsPerLSPTypeStacked.main(pbar, show=True)
plotsCodes.DailyOrbitalAttemptsPerCountry.main(pbar, show=True)
plotsCodes.DailyOrbitalFailuresPerCountry.main(pbar, show=True)
plotsCodes.DailyOrbitalSuccessRate.main(pbar, show=True)
plotsCodes.OrbitalFailuresPerCountry.main(pbar, show=True)
plotsCodes.LaunchCadenceWorldwide.main(pbar, show=True)
plotsCodes.LaunchCadenceWorldwidePrediction.main(pbar, show=True)
plotsCodes.LaunchCadenceWorldwidePredictionLinear.main(pbar, show=True)
plotsCodes.OrbitalFailuresPerCountryStacked.main(pbar, show=True)
plotsCodes.OrbitalSuccessFailures.main(pbar, show=True)
plotsCodes.DailyConsecutiveYears.main(pbar, show=True)
plotsCodes.MaidenFlights.main(pbar, show=True)
plotsCodes.TotalOrbitalAttemptsPerCountry.main(pbar, show=True)

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

# Yearly plots
plotsCodes.YearlyOrbitalAttemptsPerCountry.main(pbar, show=False)
plotsCodes.YearlyOrbitalAttemptsPerLSP.main(pbar, show=False)

# Plotly plots
plotsCodes.PlotlyOrbitalAttemptsPerCountry.main(pbar)
plotsCodes.PlotlyOrbitalAttemptsPerLSP.main(pbar)

pbar.close()

print("Successfully generated and exported all plots.")
