import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import CubicHermiteSpline

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
        "NY Quick Draw": 19247.32,
        "DC Keno": 3881.082,
        "Other": 1198.68
    }

    other_size = {
        "Italy": 324.6,
        "USA": 231.57,
        "Poland": 230.4,
        "Slovakia": 149.5,
        "Belgium": 123.64,
        "Australia": 45.4,
        "Czech Republic": 28.3,
        "Germany": 17.5,
        "Israel": 15.2,
        "United Kingdom": 13.5,
        "Canada": 12.9,
        "Europe": 6.31
    }

    def plot_barh(dataset, y_position):
        labels = list(dataset.keys())
        data = np.array(list(dataset.values()))
        cummulative_data = np.cumsum(data)
        colors = plt.colormaps['RdYlGn'](
            np.linspace(0.85, 0.15, len(data))
        )

        # Normalize to fit on the same xaxis
        data /= cummulative_data[-1]
        cummulative_data /= cummulative_data[-1]
        for i, (colname, color) in enumerate(zip(labels, colors)):
            widths = data[i]
            starts = cummulative_data[i] - widths
            rects = ax.barh(
                y_position,
                widths,
                left=starts,
                height=1,
                label=colname,
                color=color
            )

    fig, ax = plt.subplots(figsize=(12, 3))
    fig.subplots_adjust(top=1, bottom=0.33)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    axbox = ax.get_position()

    plot_barh(dataset_size, 1.5)
    plot_barh(other_size, 0)

    ax.axvline(x=1, ymin=0.4, ymax=0.6)
    ax.axline(xy1=(0, 0.4), slope=0.55, transform=ax.transAxes)   #xy1=(0, 0.4)

    ax.legend(
        ncol=(len(dataset_size) + len(other_size) + 1)//2,
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

    bar_properties_below = {
        "width": 1,
        "color": "0.8",
        "edgecolor": "black",
        "linewidth": 1,
        "fill": True
    }

    bar_properties_above = {
        "width": 1,
        "color": "white",
        "edgecolor": "black",
        "linewidth": 1,
        "fill": False
    }

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.autofmt_xdate(bottom=0.22, rotation=45, ha='right')

    # ax.bar(
    #     np.arange(len(requirements)) * 1.25 - 0.5,
    #     available,
    #     **bar_properties_below
    # )
    above_bars = ax.bar(
        np.arange(len(requirements)) * 1.25 - 0.5,
        [(int(v)//1000) for v in requirements.values()],
        **bar_properties_above
    )
    ax.bar_label(above_bars, labels=[int(v)//1024 for v in requirements.values()], padding=3)

    ax.set_xticks(np.arange(len(requirements)) * 1.25 - 0.5, requirements.keys())
    ax.set_yticks([512, 1024, 2048, 4096, 8192], [512, 1024, 2048, 4096, 8192])
    ax.set_ylabel("kB required")

    plt.show()

def plot_performance():
    matplotlib.rcParams.update({
        "axes.spines.bottom": False,
        "axes.spines.left": False,
        "axes.spines.right": False,
        "axes.spines.top": False
    })

    bit_sources = [
        "/dev/urandom 4M",
        "/dev/urandom 19M",
        "Joint lotteries",
        "DC Keno",
        "NY Quick Draw"
    ]

    performance = np.array([
        #    Bday,    31x31,    32x32,      6x8, Count 1s,  Parking,  Mindist,  3DSphrs,  Squeeze, OverSums
        [0.033248,    0.329,    0.001, 0.554153, 0.301102,       0.,       0., 0.944090,       0., 0.840705], # /dev/urandom 4M
        [0.100870,    0.647,    0.193, 0.428252, 0.057863,       0., 0.375738, 0.196550, 0.105024, 0.000958], # /dev/urandom 19M
        [      0.,       0.,       0.,       0.,       0.,       1.,       0., 0.032128,       0.,       0.], # Joint lotteries
        [      0.,    0.241,       0.,       0.,       0.,       1.,       0., 0.231590,       0.,       0.], # DC Keno
        [      0.,    0.260,    0.497,       0.,       0.,       0.,       0.,       0.,       0.,       0.]  # NY Quick Draw
    ])

    tests = [
        "Birthday", "Rank 31x31", "Rank 32x32", "Rank 6x8", "Count 1s",
        "Parking", "Mindist", "3D spheres", "Squeeze", "OverSums"
    ]

    def modify_axis(ax, test, x_position):
        epsilon = 0.05
        ax.set_xlim((0, len(tests)-1))
        ax.set_ylim((-epsilon, 1+epsilon))

        # Eliminate upper and right axes
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(False)
        
        ax.spines['right'].set_color("gray")
        ax.spines['right'].set_position(('axes', x_position/(len(tests)-1)))
        ax.spines['right'].set_bounds(low=0, high=1)

        ax.yaxis.set_ticks_position('right')
        ax.tick_params(
            axis="y", which="both", direction="out", colors="gray",
            top=False, left=False, right=True, bottom=False,
            labeltop=False, labelleft=False, labelright=True, labelbottom=False
        )
        ax.tick_params(
            axis="x", which="both", top=False, left=False, right=False, bottom=False,
            labeltop=False, labelleft=False, labelright=False, labelbottom=False
        )

        ax.set_title(test, x=x_position/(len(tests)-1), pad=12)
    
    def plot_spline(nodes, source, i):
        t = np.linspace(0, len(tests), nodes.shape[0]*100)
        curve = CubicHermiteSpline(
            x = np.arange(nodes.shape[0]),
            y = nodes,
            dydx = np.zeros_like(nodes)
        )
        plot_points = curve(t)
        artist, = plt.plot(t, plot_points, label=source, linewidth=2, zorder=2.1 + i/10)    # fit into default zorder scale
        return artist

    fig = plt.figure(figsize=(12, 6))
    fig.subplots_adjust(top=0.833, bottom=0.166)

    ax1 = fig.add_subplot(1, 1, 1)
    axes = [ax1] + [ax1.twinx() for i in range(1, len(tests))]

    for i, (t, ax) in enumerate(zip(tests, axes)):
        modify_axis(ax, t, i)

    artists = []    # For reordering labels in the legend
    for i, (source, nodes) in enumerate(zip(bit_sources, performance)):
        artists.append(plot_spline(nodes, source, i))
    
    fig.legend(
        ncol=len(tests),
        handles=[artists[2], artists[3], artists[4], artists[0], artists[1]],   # Bleh but who cares
        bbox_to_anchor=(0.0125, ax1.get_position().y0-0.1, 1, 1),
        bbox_transform=fig.transFigure,
        loc='lower center'
    )

    plt.show()


if __name__ == "__main__":
    # plot_dataset_composition()
    # plot_test_requirements()
    plot_performance()
