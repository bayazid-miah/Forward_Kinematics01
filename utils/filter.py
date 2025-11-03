import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt


def butterworth_lowpass_filter(data, cutoff, fs, order=2):

    # Make a copy so we don’t modify the original data
    filtered_data = data.copy()

    # Compute normalized cutoff frequency (Nyquist frequency = fs/2)
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist

    # Design Butterworth filter
    b, a = butter(order, normal_cutoff, btype='low', analog=False)

    # Apply filter to all numeric columns except time/frame
    for col in filtered_data.columns:
        if col.lower() in ['time', 'frame']:
            continue
        if np.issubdtype(filtered_data[col].dtype, np.number):
            filtered_data[col] = filtfilt(b, a, filtered_data[col])

    return filtered_data
