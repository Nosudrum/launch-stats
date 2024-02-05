import matplotlib.pyplot as plt

from Processing import PastT0s, PastLSPs
from plotsCodes.PlotFunctions import np, datetime, xkcd_font


# Plot of orbital launch attempts per LSP per year since 1957
def main(pbar, show=False):
    SpX_mask = PastLSPs["id"] == 121
    T0s = PastT0s[SpX_mask]["net"]
    count = np.arange(1, T0s.count() + 1, 1)

    plt.xkcd()

    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    ax.annotate(
        "START OF DEDICATED\nSTARLINK LAUNCHES",
        xy=(datetime(2019, 8, 20), 85),
        arrowprops=dict(arrowstyle="->"),
        xytext=(datetime(2007, 1, 1), 82),
        font=xkcd_font,
    )

    ax.annotate(
        "START OF HIGH-INCLINATION\nSTARLINK LAUNCHES",
        xy=(datetime(2021, 9, 20), 133),
        arrowprops=dict(arrowstyle="->"),
        xytext=(datetime(2007, 1, 1), 230),
        font=xkcd_font,
    )

    ax.plot(T0s, count)
    ax.set_xlabel("time", font=xkcd_font)
    ax.set_ylabel("orbital launches", font=xkcd_font)

    ax.set_title("SpaceX launch cadence", font=xkcd_font)

    fig.text(0.05, 0.05, "launch-stats.com", ha="left", font=xkcd_font)

    fig.text(0.95, 0.05, "data from the LL2 API", ha="right", font=xkcd_font)

    plt.savefig("plots/xkcd/SpaceXStarlink.png", transparent=False, dpi=500)
    if show:
        plt.show()
    pbar.update()
