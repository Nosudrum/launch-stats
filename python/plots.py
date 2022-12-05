# Preamble
import plotsCodes

# Main plots
plotsCodes.OrbitalAttemptsPerCountryStacked.main(show=True)
plotsCodes.OrbitalAttemptsPerCountry.main(show=True)
plotsCodes.OrbitalAttemptsPerLSPStacked.main(show=True)
plotsCodes.OrbitalAttemptsPerLSP.main(show=True)
plotsCodes.OrbitalAttemptsPerLSPStacked.main(show=True)
plotsCodes.OrbitalAttemptsPerLSPType.main(show=True)
plotsCodes.OrbitalAttemptsPerLSPTypeStacked.main(show=True)
plotsCodes.DailyOrbitalAttemptsPerCountry.main(show=True)
plotsCodes.DailyOrbitalFailuresPerCountry.main(show=True)
plotsCodes.DailyOrbitalSuccessRate.main(show=True)
plotsCodes.OrbitalFailuresPerCountry.main(show=True)
plotsCodes.LaunchCadenceWorldwide.main(show=True)
plotsCodes.LaunchCadenceWorldwidePrediction.main(show=True)
plotsCodes.LaunchCadenceWorldwidePredictionLinear.main(show=True)
plotsCodes.OrbitalFailuresPerCountryStacked.main(show=True)
plotsCodes.OrbitalSuccessFailures.main(show=True)
plotsCodes.DailyConsecutiveYears.main(show=True)
plotsCodes.MaidenFlights.main(show=True)
plotsCodes.TotalOrbitalAttemptsPerCountry.main(show=True)

# Plots per Country
plotsCodes.LaunchCadenceByCountry.main(show=False)
plotsCodes.OrbitalSuccessRatePerCountry.main(show=False)
plotsCodes.OrbitalSuccessFailuresPerCountry.main(show=False)
plotsCodes.LaunchCadenceByCountryPrediction.main(show=False)
plotsCodes.LaunchCadenceByCountryLinear.main(show=False)

# Plots per LSP
plotsCodes.LaunchCadenceByLSP.main(show=False)
plotsCodes.LaunchCadenceByLSPprediction.main(show=False)
plotsCodes.OrbitalSuccessFailuresPerLSP.main(show=False)
plotsCodes.LaunchCadenceByLSPpredictionLinear.main(show=False)
plotsCodes.OrbitalReusabilityPerLSP.main(show=False)

# Yearly plots
plotsCodes.YearlyOrbitalAttemptsPerCountry.main(show=False)
plotsCodes.YearlyOrbitalAttemptsPerLSP.main(show=False)

# Plotly plots
plotsCodes.PlotlyOrbitalAttemptsPerCountry.main()
plotsCodes.PlotlyOrbitalAttemptsPerLSP.main()

print('Successfully generated and exported all plots.')
