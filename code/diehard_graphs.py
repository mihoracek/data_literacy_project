import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({
    "backend": "TKAgg",
    "xtick.labelsize": "large",
    "ytick.labelsize": "large",
    "axes.labelsize":  "large",
    "legend.fontsize": "large",
    "xtick.major.width": 1,
    "ytick.major.width": 1,
    "xtick.minor.width": 0,
    "ytick.minor.width": 0,
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "text.usetex": True,
    "pgf.rcfonts": False
})

def plot_dataset_composition():
    matplotlib.rcParams.update({
        "axes.spines.bottom": False,
        "axes.spines.left": False,
        "axes.spines.right": False,
        "axes.spines.top": False
    })

    dataset_size = {
        "Italy": 324.6,
        "Poland": 230.4,
        "USA": 229.5,
        "Australia": 45.4,
        "Czech Republic": 28.3,
        "Germany": 17.5,
        "Israel": 15.2,
        "United Kingdom": 13.5,
        "Canada": 12.9,
        "Eurojackpot": 1.3
    }

    labels = list(dataset_size.keys())
    data = np.array(list(dataset_size.values()))
    cummulative_data = np.cumsum(data)    
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.85, 0.15, len(data))
    )

    fig, ax = plt.subplots(figsize=(12, 1.5))
    fig.subplots_adjust(top=1, bottom=0.33)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, cummulative_data[-1])
    axbox = ax.get_position()

    for i, (colname, color) in enumerate(zip(labels, category_colors)):
        widths = data[i]
        starts = cummulative_data[i] - widths
        rects = ax.barh(
            0,
            widths,
            left=starts,
            height=1,
            label=colname,
            color=color
        )

    ax.legend(
        ncol=(len(labels) + 1)//2,
        bbox_to_anchor=(0, axbox.y0-0.33, 1, 1),
        bbox_transform=fig.transFigure,
        loc='lower center',
        fontsize='medium'
    )
    
    plt.show()

def plot_test_requirements():
    matplotlib.rcParams.update({
        "axes.spines.bottom": True,
        "axes.spines.left": True,
        "axes.spines.right": False,
        "axes.spines.top": False
    })

    requirements = {
        "Birthday":                     2048000,
        "Overlapping 5-Perms":          8011776,
        "Binary rank 31x31":            4964352,
        "Binary rank 32x32":            5128192,
        "Binary rank 6x8":              2408448,
        "Bitstream":                    5259264,
        "Monkey OPSO":                  8404992,
        "Monkey OQSO":                  8404992,
        "Monkey DNA":                   8404992,
        "Count 1s":                     1032192,
        "Parking":                       966656,
        "Mindist":                      6406144,
        "3D spheres":                    966656,
        "Squeeze":                      8306688,
        "Overlapping sums":              802816,
        "Runs":                          802816,
        "Craps":                        5832704
    }

    available = 477

    bar_properties_below = {
        "width": 1,
        "color": "0.8",
        "edgecolor": "black",
        "linewidth": 1,
        "fill": True
    }

    bar_properties_above = {
        "bottom": available,
        "width": 1,
        "color": "white",
        "edgecolor": "black",
        "linewidth": 1,
        "fill": False
    }

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.autofmt_xdate(bottom=0.22, rotation=45, ha='right')

    ax.bar(
        np.arange(len(requirements)) * 1.25 - 0.5,
        available,
        **bar_properties_below
    )
    above_bars = ax.bar(
        np.arange(len(requirements)) * 1.25 - 0.5,
        [(int(v)//1024) - available for v in requirements.values()],
        **bar_properties_above
    )
    ax.bar_label(above_bars, labels=[int(v)//1024 for v in requirements.values()], padding=3)

    ax.set_xticks(np.arange(len(requirements)) * 1.25 - 0.5, requirements.keys())
    ax.set_yticks([512, 1024, 2048, 4096, 8192], [512, 1024, 2048, 4096, 8192])
    ax.axhline(available, color="black")
    ax.set_ylabel("KiB required")

    plt.show()

if __name__ == "__main__":
    plot_dataset_composition()
    # plot_test_requirements()
