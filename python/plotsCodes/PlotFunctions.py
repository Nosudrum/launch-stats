import matplotlib.pyplot as plt
from math import prod, ceil, floor
import numpy as np
from PIL import Image

Badge_DataLL2 = Image.open('assets/DataByLL2.png')
Badge_Nosu = Image.open('assets/Nosu.png')

# Colors
colors_dict = {'red': '#e41a1c', 'orange': '#ff7f00', 'blue': '#377eb8', 'pink': '#f781bf', 'yellow': '#dede00',
               'green': '#4daf4a', 'grey': '#999999', 'purple': '#984ea3'}
colors = ['blue', 'orange', 'red', 'green', 'pink', 'yellow', 'purple', 'grey']
colors = [colors_dict[i] for i in colors]

# LSPs custom names
LSPs_dict = {0: 'Others', 66: 'Soviet Union', 161: 'USAF', 63: 'ROSCOSMOS', 88: 'CASC', 115: 'Arianespace',
             96: 'Khrunichev', 121: 'SpaceX', 147: 'Rocket Lab', 124: 'ULA', 257: 'NGSS', 285: 'Astra',
             199: 'Virgin Orbit', 163: 'VVKO', 166: 'US Navy', 271: 'ABMA', 165: 'US Army', 44: 'NASA', 270: 'RVSN RF',
             1018: 'CNR IT', 1017: 'SERC UK', 46: 'CNES FR', 1009: 'ISAS JP', 1019: 'ESRO', 1015: 'ELDO',
             1005: 'RAE UK', 189: 'CASC', 82: 'Lockheed', 228: 'NASDA', 100: 'OSC', 1004: 'Convair', 102: 'Rockwell',
             192: 'Lockheed SOC', 98: 'Mitsubishi HI', 1014: 'Martin M.', 111: 'Progress RSC', 154: 'Polyot',
             197: 'LMSO', 191: 'USA', 122: 'Sea Launch', 37: 'JAXA', 118: 'ILS', 193: 'VKS', 31: 'ISRO', 194: 'ExPace',
             1016: 'Aus. WRE', 29: 'DLR DE', 106: 'Gen. Dynamics', 1032: 'IRGCAF', 36: 'ASI IT', 119: 'ISCK', 34: 'IRN',
             190: 'Antrix', 195: 'Sandia Nat. Labs', 40: 'KCST', 117: 'Eurockot LS', 95: 'Israel AI',
             179: 'Orbital ATK', 259: 'LandSpace', 263: 'OneSpace', 274: 'iSpace', 272: 'Chinarocket',
             1021: 'Galactic Energy', 187: 'GK Launch Services', 265: 'Firefly', 41: 'KARI'}

Countries_dict = {'OTH': 'Others', 'RUS': 'Russia/USSR', 'USA': 'USA', 'CHN': 'China', 'FRA': 'France', 'JPN': 'Japan',
                  'IND': 'India', 'NZL': 'New Zealand', 'IRN': 'Iran', 'PRK': 'North Korea', 'ISR': 'Israel',
                  'KOR': 'South Korea'}

monthsLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# Functions for figures
def dark_figure(subplots=(1, 1), figsize=(7, 5.2)):
    fig = plt.figure(facecolor='#0D1117', figsize=figsize)
    axes = []
    for ii in range(0, prod(subplots)):
        axes.append(fig.add_subplot(subplots[0], subplots[1], ii + 1, facecolor='#0D1117'))
        axes[ii].tick_params(axis='x', colors='white', which='both')
        axes[ii].tick_params(axis='y', colors='white', which='both')
        axes[ii].yaxis.label.set_color('white')
        axes[ii].xaxis.label.set_color('white')
        axes[ii].title.set_color('white')
        for i in axes[ii].spines:
            axes[ii].spines[i].set_color('white')
    return fig, axes


def finish_figure(fig, axes, path, show, save_transparent=False):
    plt.tight_layout()
    ticks = axes_ticks(axes[0].get_ylim()[1])
    axes[0].set_yticks(ticks)
    axes[0].set_ylim([0, ticks[-1] * 1.2])
    fig.subplots_adjust(bottom=0.20)
    fig_axes1 = fig.add_axes([0.678, 0.02, 0.3, 0.3], anchor='SE', zorder=1)
    fig_axes1.imshow(Badge_DataLL2)
    fig_axes1.axis('off')
    fig_axes2 = fig.add_axes([0.014, 0.02, 0.3, 0.3], anchor='SW', zorder=1)
    fig_axes2.imshow(Badge_Nosu)
    fig_axes2.axis('off')
    if save_transparent:
        plt.savefig('plots/' + path + '_transparent.png', transparent=True, dpi=500)
    plt.savefig('plots/' + path + '.png', transparent=False, dpi=500)
    if show:
        plt.show()
    plt.close()


def flip_legend(reverse):
    handles_, labels_ = plt.gca().get_legend_handles_labels()
    handles_ = [k for j in [handles_[i::4] for i in range(4)] for k in j]
    labels_ = [k for j in [labels_[i::4] for i in range(4)] for k in j]
    if reverse:
        return handles_[::-1], labels_[::-1]
    else:
        return handles_, labels_


def flatten(list_of_lists):
    flattened_list = []
    for i in list_of_lists:
        if isinstance(i, list):
            flattened_list += i
        else:
            flattened_list.append(i)
    return flattened_list


def axes_ticks(value):
    value = floor(value)
    if value < 5:
        interval = 1
    elif value < 14:
        interval = 2
    elif value < 30:
        interval = 5
    elif value < 100:
        interval = 10
    elif value < 200:
        interval = 25
    elif value < 500:
        interval = 50
    else:
        interval = 1
    upper_bound = interval * (ceil(value / interval) + 1)
    return np.arange(0, upper_bound, interval)
