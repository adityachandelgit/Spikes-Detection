from matplotlib.pyplot import plot, scatter, show
from numpy import array

from Utils import smooth, peakdet, load_eda_csv

"""
Requirements/Dependencies:
    1. Numpy
    2. Matplotlib
"""
if __name__ == "__main__":
    # Load the EDA csv file
    series = load_eda_csv('EDA.csv')

    # Smoothen the data
    # window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
    smooth_series = smooth(series, window_len=9, window='flat')

    # Detect peaks
    # Second param = alpha
    maxTab, minTab = peakdet(smooth_series, .07)

    plot(smooth_series)
    scatter(array(maxTab)[:, 0], array(maxTab)[:, 1], color='red')
    # scatter(array(minTab)[:, 0], array(minTab)[:, 1], color='green')
    show()
