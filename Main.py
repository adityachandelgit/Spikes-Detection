import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from numpy import array, genfromtxt, std
from datetime import datetime
from matplotlib.dates import MINUTELY
import os

from Utils import smooth, peakdet
import csv

"""
Requirements/Dependencies:
    1. Numpy
    2. Matplotlib
"""


def spike_detection_and_plotting(input_file, plot_path):
    print

    # Load data from csv file
    data = genfromtxt(input_file, delimiter=',')
    eda = data[:, 1]

    # Calculate standard deviation
    std_dev = std(eda)

    # Extract timestamps and artifacts
    timestamp = []
    artifact = []
    ts_art_dict = {}
    with open(input_file, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            ts_art_dict[datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')] = row[2]
            artifact.append(row[2])
            timestamp.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))

    # Smoothen the data
    # window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
    # smooth_series = smooth(series, window_len=20, window='flat')

    # Detect peaks
    maxTab, minTab = peakdet(eda, 0.3)

    # Setup graph
    plt.figure(figsize=(25, 15))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    adl = mdates.AutoDateLocator()
    adl.intervald[MINUTELY] = [5]
    plt.gca().xaxis.set_major_locator(adl)

    # Plot eda
    plt.plot(timestamp, eda)

    # Set plot labels
    plt.title(plot_path[-7:-1] + ' - ' + timestamp[0].strftime("%d/%b/%Y"), fontsize=30)
    plt.xlabel('Time', fontsize=20)
    plt.ylabel('eda (uS)', fontsize=20)
    plt.gcf().autofmt_xdate()

    # Plot noise bars
    arts = []
    for idx, val in enumerate(artifact):
        if val == '-1.0':
            arts.append(timestamp[idx])
    [plt.axvline(_x, linewidth=1, color='red') for _x in arts]

    # Plot peak points
    if len(maxTab) > 0:
        scatter_ts = []
        for ts in array(maxTab)[:, 0]:
            scatter_ts.append(timestamp[int(ts.item())])
        plt.scatter(scatter_ts, array(maxTab)[:, 1], color='limegreen', s=40)

        # Annotate peak points
        ar = array(maxTab)[:, 1]
        for i, dt in enumerate(scatter_ts):
            if ts_art_dict[dt] == '-1.0':
                color = 'red'
            if ts_art_dict[dt] == '1.0':
                color = 'yellow'
            time_label = dt.strftime('%H:%M:%S')
            plt.annotate(
                time_label,
                xy=(scatter_ts[i], ar[i]), xytext=(-20, 20),
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc=color, alpha=0.5),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    # scatter(array(minTab)[:, 0], array(minTab)[:, 1], color='green')

    plt.savefig(plot_path + '\Plot.jpg')


for subdir, dirs, files in os.walk('C:\My-Files\SnD\USU\EMW-Research\Empatica Data\Cache Rocket\By Date'):
    for f in files:
        if f == 'Merged-EDA.csv':
            spike_detection_and_plotting(os.path.join(subdir, f), subdir)

# spike_detection_and_plotting('C:/My-Files/SnD/USU/EMW-Research/Empatica Data/Cache Rocket/By Date/15-Nov-2016/1479251403_A009D3/Merged-EDA.csv',
#                              'C:/My-Files/SnD/USU/EMW-Research/Empatica Data/Cache Rocket/By Date/15-Nov-2016/1479251403_A009D3/')
