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
        "Joint lotteries",
        "DC Keno",
        "NY Quick Draw",
        "/dev/urandom 4M",
        "/dev/urandom 19M"
    ]

    p_values = [
        np.array(   # Joint lotteries
            [0.] * 30   # Collective number of zero p-values collected across all tests
            + [0.999998, 0.659449, 0.980051]    # Parking
            + [0.759803, 0.787090, 0.354090, 0.468001, 0.323930, 0.260593, 0.130447, 0.312485, 0.572716, 0.666767,
               0.221748, 0.590500, 0.382056, 0.075568, 0.660695, 0.147636, 0.067845, 0.144823, 0.066163, 0.073271]  # 3D Spheres
            + [0.001028, 0.000247, 0.087383, 0.289471, 0.005908, 0.049645]  # Overlapping sums
            + [0.882938, 0.651151, 0.709057, 0.003857]  # Runs
            + [1.] * 7
        ),
        np.array(   # DC Keno
            [0.] * 36   # All Rank 6x8, Count 1s and Overlapping sums
            + [0.000218, 0.150191, 0.000098, 0.054794, 0.030341, 0.028518, 0.000001, 0.002070, 0.053682]    # Birthday
            + [0.999999, 0.999989, 0.999957, 0.999984, 0.999910, 0.999989, 0.999999, 0.999998, 0.999964]    # Parking
            + [0.606197, 0.600990, 0.254748, 0.818353, 0.553510, 0.050146, 0.621395, 0.177995, 0.112369, 0.470621,
               0.686696, 0.269411, 0.707174, 0.077131, 0.163620, 0.779918, 0.015540, 0.241430, 0.525674, 0.522292]  # 3D Spheres
            + [0.972813, 0.632246, 0.154379, 0.205730]  # Runs
            + [1.] * 1
        ),
        np.array(   # NY Quick Draw
            [0.] * (9 + 19 + 20 + 23 + 28 + 31 + 1 + 3 + 1 + 3)    # All Birthdays, 19 in Rank 6x8, all Bitstream, all Monkey, Count 1s, 3 Mindist, Squeeze, 3 Runs, 1 Craps
            + [0.260]   # Rank 31x31
            + [0.497]   # Rank 32x32
            + [0.368556, 0.578047, 0.000590, 0.089127, 0.005209, 0.008229]  # Rank 6x8
            + [0.000057, 0.000001, 0.000007, 0.000075, 0.000010, 0.000023, 0.000082, 0.000090, 0.000007,
               0.000001, 0.000002, 0.000001, 0.000022, 0.000004, 0.000010, 0.000059, 0.000094]  # Mindist
            + [0.000621, 0.028158, 0.000867, 0.001495, 0.001675, 0.013686, 0.000012, 0.001535, 0.024313, 0.000072,
               0.009340, 0.000796, 0.004837, 0.000008, 0.061759, 0.002863, 0.003876, 0.000001, 0.005999, 0.004096]  # 3D Spheres
            + [0.028141, 0.929069, 0.003666, 0.000272, 0.027896, 0.675658, 0.000187, 0.001770, 0.000737, 0.190722]  # Overlapping sums
            + [0.000001]
            + [1.] * (10 + 1) # All Parking, 1 Craps
        ),
        np.array(   # /dev/urandom 4M
            [0.884536, 0.157790, 0.088269, 0.588527, 0.147874, 0.162086, 0.278437, 0.047255, 0.275698]    # Birthdays
            + [0.116222, 0.110622, 0.067516, 0.102171, 0.889268, 0.834450, 0.599883, 0.182923, 0.071072, 0.788530,
               0.213510, 0.995235, 0.601520, 0.293541, 0.795319, 0.733503, 0.626226, 0.348218, 0.296589, 0.606103,
               0.313583, 0.916213, 0.094863, 0.789837, 0.278014]    # Rank 6x8
            + [0.301102]    # Count 1s
            + [0.819442, 0.232514, 0.921543, 0.781201, 0.723613, 0.781201, 0.518210, 0.033889, 0.136563, 0.907282]  # Parking
            + [0.675655, 0.392010, 0.301688, 0.718797, 0.952913, 0.605903, 0.342845, 0.342082, 0.238561, 0.122485,
               0.097779, 0.601061, 0.566267, 0.378517, 0.892834, 0.847895, 0.953650, 0.050435, 0.119014, 0.395133]  # 3D Spheres
            + [0.985346, 0.081629, 0.474857, 0.412810, 0.949648, 0.537400, 0.757278, 0.667565, 0.014511, 0.300779]  # Overlapping Sums
            + [0.064537, 0.119692, 0.153507, 0.322232]  # Runs
        ),
        np.array(   # /dev/urandom 19M
              [0.210609, 0.050252, 0.851880, 0.061027, 0.635811, 0.633647, 0.075573, 0.095146, 0.583107]  # Birthdays
            + [0.647]   # Rank 31x31
            + [0.193]   # Rank 32x32
            + [0.054407, 0.663004, 0.900643, 0.093392, 0.194942, 0.746340, 0.231718, 0.201123, 0.491421, 0.387082,
               0.010384, 0.016644, 0.378448, 0.469790, 0.756303, 0.880610, 0.880192, 0.836727, 0.272827, 0.996791,
               0.425038, 0.943160, 0.242289, 0.895491, 0.959416]    # Rank 6x8
            + [0.318752, 0.470507, 0.864604, 0.306345, 0.676781, 0.855773, 0.185637, 0.685125, 0.141937, 0.303072,
               0.829969, 0.625843, 0.602613, 0.319587, 0.791466, 0.125810, 0.798765, 0.092752, 0.154914, 0.242643]  # Bitstream
            + [0.326144, 0.060500, 0.599813, 0.536171, 0.174432, 0.644347, 0.703890, 0.296897, 0.147518, 0.805039, 0.518331, 0.851414,
               0.466103, 0.585089, 0.831412, 0.444235, 0.467474, 0.866820, 0.847383, 0.925907, 0.630120, 0.523826, 0.429294]    # Monkey OPSO
            + [0.383162, 0.522072, 0.516670, 0.136280, 0.298855, 0.997480, 0.806625, 0.137022, 0.390949, 0.825547,
               0.522072, 0.018752, 0.206330, 0.892844, 0.198682, 0.859725, 0.867142, 0.229270, 0.009964, 0.353773,
               0.900162, 0.920419, 0.786501, 0.104466, 0.550349, 0.538253, 0.123390, 0.352514]  # Monkey OQSO
            + [0.324104, 0.320929, 0.535645, 0.702619, 0.118619, 0.639793, 0.360936, 0.207211, 0.335854, 0.773444, 0.072255,
               0.368696, 0.602784, 0.046436, 0.602784, 0.663780, 0.923030, 0.311483, 0.050285, 0.263287, 0.758984,
               0.344502, 0.516859, 0.595944, 0.605058, 0.752504, 0.854749, 0.159606, 0.011414, 0.902505, 0.156757]  # Monkey DNA
            + [0.057863]    # Count 1s
            + [0.400606, 0.331343, 0.701195, 0.504165, 0.182099, 0.679394, 0.395408, 0.515019, 0.950648,
               0.250897, 0.829212, 0.247030, 0.582150, 0.041598, 0.857790, 0.033347, 0.927146, 0.344586,
               0.770537, 0.775454, 0.259879, 0.580461, 0.833601, 0.350841, 0.268921]    # Count 1s stream
            + [0.445521, 0.518210, 0.873180, 0.708135, 0.409702, 0.011212, 0.607947, 0.205562, 0.374623, 0.708135]  # Parking
            + [0.576194, 0.770316, 0.376306, 0.626960, 0.019487, 0.013951, 0.027964, 0.702668, 0.353784, 0.020645,
               0.825332, 0.038885, 0.679258, 0.841900, 0.347541, 0.527896, 0.617503, 0.171829, 0.579731, 0.364154]  # Mindist
            + [0.359037, 0.214722, 0.896004, 0.083124, 0.476312, 0.926604, 0.871952, 0.263104, 0.040303, 0.835403,
               0.751040, 0.178352, 0.804897, 0.823770, 0.746802, 0.221453, 0.936524, 0.179005, 0.984374, 0.771952]  # 3D Spheres
            + [0.105024]    # Squeeze
            + [0.743782, 0.455722, 0.595618, 0.008413, 0.008448, 0.324101, 0.027188, 0.007986, 0.119995, 0.197483]  # Overlapping sums
            + [0.452345, 0.937476, 0.907917, 0.572022]  # Runs
            + [0.180611, 0.836299]  # Craps
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
    plot_dataset_composition()
    # plot_test_requirements()
    # plot_performance()
    # plot_pvalue_distributions()
