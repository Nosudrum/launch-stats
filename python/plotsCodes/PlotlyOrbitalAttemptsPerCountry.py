import plotly.express as px

from Processing import PastT0s, PastCountries, PastPad, PastName, PastStatus, PastLSPs
from plotsCodes.PlotFunctions import Countries_dict, colors, subtitle_html, finish_plotly_figure, datetime, ceil


# Plot of orbital launch attempts per country since 1957 non-stacked
def main(pbar):
    Countries = PastCountries.copy().rename(columns={"location.country_code": "Country"}).replace(
        {"Country": Countries_dict})
    Pad = PastPad.copy().rename(columns={"name": "Pad"})["Pad"]
    Location = PastPad.rename(columns={"location.name": "Location"})["Location"]
    Outcome = PastStatus.rename(columns={"name": "Outcome"})["Outcome"]
    LSP = PastLSPs.rename(columns={"name": "LSP"})["LSP"]
    Date = PastT0s.copy().rename(columns={"net": "Date"})
    T0 = PastT0s.copy().rename(columns={"net": "T0"}).T0.dt.strftime("%B %d, %Y at %H:%M:%S %Z")
    data = Date.join(Countries).join(T0).join(Pad).join(Location).join(PastName).join(
        Outcome).join(LSP)

    nb_launches_country = data.Country.value_counts().to_dict()
    data['CountryVal'] = data['Country'].map(nb_launches_country)
    data = data.sort_values(by='CountryVal', ascending=False)

    number_of_bins = PastT0s.net.dt.year.max() - PastT0s.net.dt.year.min() + 1
    hover_data = ["T0", "LSP", "Location", "Pad", "Country", "Outcome"]
    fig = px.histogram(data, x="Date", color="Country", marginal="rug", hover_data=hover_data, hover_name="name",
                       template="plotly_dark", nbins=int(number_of_bins),
                       color_discrete_sequence=colors[:-1])
    fig.update_layout(yaxis_title="Total launches per year",
                      xaxis_range=[datetime(1957, 1, 1, 0, 0, 0), datetime(datetime.now().year, 12, 31, 23, 59, 59)],
                      yaxis_range=[0, ceil(data.Date.dt.year.value_counts().max() / 10) * 10 + 27],
                      title_text="Orbital launch attempts per country since " + str(
                          PastT0s.net.dt.year.min()) + subtitle_html,
                      legend_title="Launch Country")

    finish_plotly_figure(fig, 'OrbitalAttemptsPerCountry.html')
    pbar.update()
