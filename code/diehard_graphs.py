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
    "pgf.rcfonts": False,
    "figure.figsize": (12, 6),
    "axes.spines.bottom": True,
    "axes.spines.left": True,
    "axes.spines.right": False,
    "axes.spines.top": False
})

def plot_test_requirements():
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

    fig, ax = plt.subplots()
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
    plot_test_requirements()
