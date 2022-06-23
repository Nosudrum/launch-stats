import plotly.express as px
import plotly.figure_factory as ff
from datetime import datetime, timezone
from plotsCodes.PlotFunctions import *
from Processing import PastT0s, PastCountries, PastPad, PastName, PastStatus, PastLSPs


# Plot of orbital launch attempts per country since 1957 non-stacked
def main():
    Countries = PastCountries.copy().rename(columns={"location.country_code": "Country"})
    Countries = Countries.replace({"Country": Countries_dict})
    data = PastT0s.copy().join(Countries).join(PastPad.rename(columns={"name": "pad"})["pad"]).join(
        PastPad["location.name"]).join(PastName).join(
        PastStatus.rename(columns={"name": "status"})["status"]).join(PastLSPs.rename(columns={"name": "LSP"})["LSP"])
    number_of_bins = PastT0s.net.dt.year.max() - PastT0s.net.dt.year.min() + 1
    hover_data = ["name", "net", "LSP", "location.name", "pad", "Country", "status"]
    fig = px.histogram(data, x="net", color="Country", marginal="rug", hover_data=hover_data, hover_name="name",
                       template="plotly_dark", nbins=number_of_bins)
    # fig.update_layout(
    #     margin=dict(l=0, r=0, b=0, t=0),
    #     paper_bgcolor="Black"
    # )
    # template = "test"
    # fig.update_traces(hovertemplate=template)
    fig.update_layout(yaxis_title="Launches",
                      title_text='Orbital launch attempts per country since ' + str(PastT0s.net.dt.year.min()),
                      xaxis_title=datetime.now(timezone.utc).strftime("Plot generated on %Y/%m/%d at %H:%M:%S UTC."))
    fig.write_html("plots/OrbitalAttemptsPerCountry.html")
    # labels = dict(
    #     Country="Launch Country",
    #     net=,
    #     count="Launches per year"
    # )
