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

    fig, ax = plt.subplots(figsize=(12, 1.5))
    fig.subplots_adjust(top=1, bottom=0.50)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    axbox = ax.get_position()

    # plot_barh(dataset_size, 0)
    plot_barh(other_size, 0)

    # ax.axvline(x=1, ymin=0.4, ymax=0.6)
    # ax.axline(xy1=(0, 0.4), slope=0.55, transform=ax.transAxes)   #xy1=(0, 0.4)

    ax.legend(
        ncol=(len(other_size) + 1) // 2,
        bbox_to_anchor=(0, axbox.y0-0.4, 1, 1),
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

# Mask tests where dataset lacks enough bytes 
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

def plot_pvalue_distributions():
    matplotlib.rcParams.update({
        "axes.spines.bottom": True,
        "axes.spines.left": True,
        "axes.spines.right": False,
        "axes.spines.top": False
    })

    bit_sources = [
        "Joint Lotteries",
        "DC Keno",
        "NY Quick Draw",
        "/dev/urandom 3M",
        "/dev/urandom 15M"
    ]

    p_values = [
        np.array(   # Joint lotteries
            [0.] * 1   # Collective number of zero p-values collected across all tests
            + [0.899470, 0.205562, 0.781201, 0.999989, 1.000000, 0.999997, 1.000000, 1.000000, 1.000000, 1.000000]    # Parking
            + [0.166952, 0.533278, 0.018036, 0.124910, 0.724003, 0.483606, 0.111519, 0.206068, 0.000068, 0.000008,
               0.000155, 0.813621, 0.033500, 0.000468, 0.000606, 0.000003, 0.018697, 0.001056, 0.000710, 0.000195]  # 3D Spheres
            + [0.000249, 0.151731, 0.392932, 0.007543, 0.417294, 0.772924, 0.008993, 0.125059, 0.000000, 0.000000]  # Overlapping sums
            + [0.981149, 0.904974, 0.000000, 0.000000]  # Runs
        ),
        np.array(   # DC Keno
            [0.] * 27   # All Rank 6x8, Count 1s
            + [0.541271, 0.068902, 0.530540, 0.946908, 0.825604, 0.562559, 0.104863, 0.899733, 0.197744]    # Birthday
            + [0.882429, 0.958644, 0.831196, 0.642555, 0.863437, 0.944998, 0.676028, 0.374623, 0.767486, 0.999186]    # Parking
            + [0.614374, 0.587119, 0.095097, 0.190983, 0.649011, 0.398152, 0.816170, 0.008576, 0.319404, 0.076079,
               0.769168, 0.057085, 0.516542, 0.537590, 0.148601, 0.314576, 0.370156, 0.933385, 0.394321, 0.436331]  # 3D Spheres
            + [0.000000, 0.000000, 0.000000, 0.000001, 0.000220, 0.000000, 0.000000, 0.000000, 0.002348, 0.000108]  # Overlapping RUns
            + [0.274252, 0.697789, 0.319506, 0.442761]  # Runs
            + [1.] * 1
        ),
        np.array(   # NY Quick Draw
            [0.] * (9 + 19 + 25 + 23 + 28 + 31 + 1 + 3 + 1 + 3)    # All Birthdays, All Rank 6x8, all Bitstream, all Monkey, Count 1s, 3 Mindist, Squeeze, 3 Runs, 1 Craps
            + [0.864]   # Rank 31x31
            + [0.954]   # Rank 32x32
            + [0.000000, 0.000172, 0.000002, 0.000202, 0.000005, 0.000033, 0.000050, 0.000054, 0.000383, 0.000000,
               0.000031, 0.000120, 0.000840, 0.000464, 0.000024, 0.000047, 0.000060, 0.000000, 0.000003, 0.000008]  # Mindist
            + [0.000423, 0.001766, 0.001634, 0.000031, 0.000034, 0.010907, 0.000119, 0.000587, 0.000614, 0.000002,
               0.000022, 0.000537, 0.000367, 0.000566, 0.000032, 0.000880, 0.000547, 0.000879, 0.000548, 0.000070]  # 3D Spheres
            + [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]  # Overlapping sums
            + [0.000001]
            + [1.] * (10 + 1) # All Parking, 1 Craps
        ),
        np.array(   # /dev/urandom 3M
            [0.348718, 0.111287, 0.184292, 0.620304, 0.550322, 0.941748, 0.311596, 0.859726, 0.443114]    # Birthdays
            + [0.043581, 0.390324, 0.716402, 0.057192, 0.015145, 0.921085, 0.607242, 0.580108, 0.062324, 0.148309,
               0.925389, 0.551145, 0.640269, 0.807229, 0.406862, 0.407707, 0.727363, 0.720685, 0.092005, 0.580141,
               0.250703, 0.986889, 0.627056, 0.261831, 0.218085]    # Rank 6x8
            + [0.686100]    # Count 1s
            + [0.118983, 0.835505, 0.463574, 0.659615, 0.988854, 0.403083, 0.131870, 0.561444, 0.917328, 0.760479,
               0.458941, 0.841077, 0.884443, 0.586755, 0.280323, 0.587651, 0.959726, 0.927346, 0.657893, 0.502601,
               0.303784, 0.501667, 0.168551, 0.227245, 0.517251]    # Count 1s Stream
            + [0.676028, 0.357445, 0.980051, 0.590298, 0.291865, 0.842447, 0.192812, 0.831196, 0.427537, 0.392053]  # Parking
            + [0.450357, 0.982956, 0.154505, 0.693506, 0.938720, 0.484377, 0.412830, 0.697878, 0.276081, 0.475469,
               0.950946, 0.711610, 0.837260, 0.727367, 0.762694, 0.884349, 0.965807, 0.238359, 0.415582, 0.530474]  # 3D Spheres
            + [0.469496, 0.213569, 0.792062, 0.908212, 0.940481, 0.811764, 0.918508, 0.296839, 0.593965, 0.401768]  # Overlapping Sums
            + [0.496771, 0.187828, 0.576015, 0.846748]  # Runs
        ),
        np.array(   # /dev/urandom 15M
              [0.403685, 0.082346, 0.724733, 0.145476, 0.207411, 0.659017, 0.579853, 0.313638, 0.669233]  # Birthdays
            + [0.654]   # Rank 31x31
            + [0.524]   # Rank 32x32
            + [0.057827, 0.007909, 0.471677, 0.921250, 0.589605, 0.865652, 0.176497, 0.637568,
               0.020626, 0.203003, 0.758697, 0.571092, 0.078719, 0.568228, 0.508636, 0.571082,
               0.277021, 0.291555, 0.048458, 0.491945, 0.249113, 0.050382, 0.634230, 0.811666, 0.737854]    # Rank 6x8
            + [0.863073, 0.677619, 0.218501, 0.411562, 0.060215, 0.847665, 0.045884, 0.021922, 0.672574, 0.583576,
               0.929589, 0.972655, 0.743006, 0.358908, 0.632024, 0.515218, 0.092752, 0.882061, 0.652949, 0.494715]  # Bitstream
            + [0.411768, 0.889764, 0.386475, 0.029710, 0.337406, 0.597145, 0.453785, 0.477080, 0.072017, 0.342460, 0.429294, 0.842452,
               0.434716, 0.739731, 0.108082, 0.587776, 0.233782, 0.575656, 0.658376, 0.782436, 0.034152, 0.459255, 0.049060]    # Monkey OPSO
            + [0.326453, 0.703095, 0.666994, 0.575717, 0.441158, 0.666994, 0.603391, 0.609910, 0.199628, 0.784523,
               0.347491, 0.925320, 0.602084, 0.052336, 0.563733, 0.253573, 0.821152, 0.407966, 0.358828, 0.034439,
               0.673131, 0.634386, 0.449195, 0.044831, 0.032176, 0.935715, 0.607306, 0.701920]  # Monkey OQSO
            + [0.427824, 0.013101, 0.927200, 0.577563, 0.999669, 0.431299, 0.725678, 0.728619, 0.420890, 0.125181, 0.862026,
               0.399105, 0.552020, 0.741181, 0.681875, 0.521561, 0.305253, 0.945829, 0.614114, 0.391154, 0.356527,
               0.411684, 0.425510, 0.237957, 0.475690, 0.150469, 0.425510, 0.439428, 0.386630, 0.976496, 0.084774]  # Monkey DNA
            + [0.752158]    # Count 1s
            + [0.343080, 0.337851, 0.872838, 0.486210, 0.900146, 0.981836, 0.860178, 0.953276, 0.357450,
               0.980800, 0.993092, 0.620926, 0.313547, 0.951391, 0.525591, 0.055784, 0.191794, 0.045231,
               0.578388, 0.956640, 0.171971, 0.767922, 0.462354, 0.096067, 0.560090]    # Count 1s stream
            + [0.807188, 0.307734, 0.392053, 0.590298, 0.168804, 0.723613, 0.767486, 0.157553, 0.984068, 0.126820]  # Parking
            + [0.483051, 0.449288, 0.795696, 0.066104, 0.701655, 0.564695, 0.980632, 0.535848, 0.201702, 0.922340,
               0.024349, 0.555208, 0.064886, 0.098087, 0.601509, 0.983688, 0.908297, 0.788827, 0.541362, 0.412745]  # Mindist
            + [0.390534, 0.015193, 0.749144, 0.358539, 0.050641, 0.916139, 0.875968, 0.316776, 0.674583, 0.069724,
               0.117909, 0.310243, 0.350934, 0.751197, 0.895716, 0.105824, 0.268205, 0.937833, 0.641028, 0.533467]  # 3D Spheres
            + [0.867679]    # Squeeze
            + [0.976108, 0.082778, 0.827780, 0.308613, 0.063533, 0.090693, 0.131835, 0.138024, 0.311349, 0.065625]  # Overlapping sums
            + [0.818870, 0.263975, 0.034056, 0.935695]  # Runs
            + [0.172496, 0.561812]  # Craps
        )
    ]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")

    epsilon = 0.05
    ax.set_xlim((0, 1+epsilon))
    ax.set_ylim((0, 1+epsilon))
    ax.spines['left'].set_bounds(low=0, high=1)
    ax.spines['bottom'].set_bounds(low=0, high=1)
    
    ax.plot([0, 1], [0, 1], color="gray")
    for source, name in zip(p_values, bit_sources):
        source.sort()
        xaxis = np.linspace(0, 1, num=len(source), endpoint=True)
        ax.plot(xaxis, source, label=name, zorder=6)
    
    ax.legend(
        ncol=1,
        bbox_to_anchor=(0.125, 0.24, 1, 1),
        bbox_transform=fig.transFigure,
        loc='center left'
    )

    plt.show()


if __name__ == "__main__":
    # plot_dataset_composition()
    # plot_test_requirements()
    # plot_performance()
    plot_pvalue_distributions()
