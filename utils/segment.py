import numpy as np
import pandas as pd
# Segment gait cycles
def segment_gait_cycles(grf_y_column, data, threshold=60, fs=100):
    gait_cycles = []
    force = np.array(grf_y_column)
    time = np.array(data["time"])

    # Heel strike detection (threshold crossings)
    raw_strikes = np.where((force[:-1] < threshold) & (force[1:] >= threshold))[0]

    # Enforce 0.5 s minimum gap to prevent duplicates
    min_interval = int(0.5 * fs)
    heel_strikes = [raw_strikes[0]]
    for hs in raw_strikes[1:]:
        if hs - heel_strikes[-1] > min_interval:
            heel_strikes.append(hs)
    heel_strikes = np.array(heel_strikes)

    if len(heel_strikes) < 2:
        print("No valid heel strikes found.")
        return gait_cycles

    # Remove outlier durations (±2 SD)
    durations = np.diff(time[heel_strikes])
    mean_dur, std_dur = np.mean(durations), np.std(durations)

    for i in range(len(heel_strikes) - 1):
        start_idx, end_idx = heel_strikes[i], heel_strikes[i + 1]
        duration = time[end_idx] - time[start_idx]
        if not (mean_dur - 2 * std_dur <= duration <= mean_dur + 2 * std_dur):
            continue

        segment = data.iloc[start_idx:end_idx].copy()
        if segment["ground_force_vy"].max() < 300:
            continue

        segment["time"] -= segment["time"].iloc[0]
        gait_cycles.append(segment)
    return gait_cycles
    
# Ensemble average of gait cycles
def ensemble_average(gait_cycles, n_points=100):
    """
    Compute ensemble average and standard deviation of any variable
    (e.g. ground reaction force or joint angle) across all gait cycles.
    """
    if not gait_cycles:
        raise ValueError("No gait cycles provided.")

    # detect which data column (besides 'time') to use
    sample = gait_cycles[0]
    data_cols = [c for c in sample.columns if c != "time"]
    if len(data_cols) != 1:
        raise ValueError(f"Expected one data column besides 'time', got {data_cols}")
    data_col = data_cols[0]

    # normalize all cycles to common 0–1 time and interpolate
    common_time = np.linspace(0, 1, n_points)
    resampled = []

    for cycle in gait_cycles:
        t = cycle["time"].to_numpy()
        y = cycle[data_col].to_numpy()
        if len(t) < 2:
            continue
        t_norm = (t - t[0]) / (t[-1] - t[0])
        y_interp = np.interp(common_time, t_norm, y)
        resampled.append(y_interp)

    resampled = np.array(resampled)
    mean_y = np.mean(resampled, axis=0)
    std_y = np.std(resampled, axis=0)

    ensemble_avg = pd.DataFrame({"time": common_time, data_col: mean_y})
    ensemble_std = pd.DataFrame({"time": common_time, data_col: std_y})
    return ensemble_avg, ensemble_std