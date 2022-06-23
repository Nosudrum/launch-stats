from datetime import datetime, timezone

import plotly.express as px

from Processing import PastT0s, PastCountries, PastPad, PastName, PastStatus, PastLSPs
from plotsCodes.PlotFunctions import *


# Plot of orbital launch attempts per country since 1957 non-stacked
def main():
    Countries = PastCountries.copy().rename(columns={"location.country_code": "Country"}).replace(
        {"Country": Countries_dict})
    Pad = PastPad.copy().rename(columns={"name": "Pad"})["Pad"]
    Location = PastPad.rename(columns={"location.name": "Location"})["Location"]
    Status = PastStatus.rename(columns={"name": "Status"})["Status"]
    LSP = PastLSPs.rename(columns={"name": "LSP"})["LSP"]
    Date = PastT0s.copy().rename(columns={"net": "Date"})
    T0 = PastT0s.copy().rename(columns={"net": "T0"}).T0.dt.strftime("%B %d, %Y at %H:%M:%S %Z")
    data = Date.join(Countries).join(T0).join(Pad).join(Location).join(PastName).join(
        Status).join(LSP)

    nb_launches_country = data.Country.value_counts().to_dict()
    data['CountryVal'] = data['Country'].map(nb_launches_country)
    data = data.sort_values(by='CountryVal', ascending=False)

    number_of_bins = PastT0s.net.dt.year.max() - PastT0s.net.dt.year.min() + 1
    hover_data = ["T0", "LSP", "Location", "Pad", "Country", "Status"]
    fig = px.histogram(data, x="Date", color="Country", marginal="rug", hover_data=hover_data, hover_name="name",
                       template="plotly_dark", nbins=number_of_bins,
                       color_discrete_sequence=colors[:-1])

    subtitle_html = r'<br><br><sup>Double-click on legend entries to isolate, again to reset.' \
                    r'<br>Click and drag to zoom in, double-click to reset.</sup>'
    fig.update_layout(yaxis_title="Launches",
                      title_text="Orbital launch attempts per country since " + str(
                          PastT0s.net.dt.year.min()) + subtitle_html,
                      xaxis=dict(
                          title=datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."),
                          titlefont=dict(color='dimgray')),
                      legend_title="Launch Country")
    fig.update_layout(legend=dict(font=dict(size=18)), title=dict(font=dict(size=18)))
    fig.update_annotations()
    fig.write_html("plots/OrbitalAttemptsPerCountry.html")
    remove_html_margins("plots/OrbitalAttemptsPerCountry.html")
    # labels = dict(
    #     Country="Launch Country",
    #     net=,
    #     count="Launches per year"
    # )
