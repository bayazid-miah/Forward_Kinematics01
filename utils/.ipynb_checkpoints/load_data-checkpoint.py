import pandas as pd
import warnings
import numpy as np

def load_marker_data(file_path="data/Trial1_marker.trc"):
    
    import pandas as pd, re, warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", pd.errors.DtypeWarning)

        # --- find the data start ---
        with open(file_path, "r") as f:
            lines = f.readlines()

        data_start = None
        for i, line in enumerate(lines):
            if re.search(r"Frame#", line):
                data_start = i
                break

        if data_start is None:
            raise ValueError("Could not find 'Frame#' in TRC file header")

        # --- read the data ---
        df = pd.read_csv(file_path, sep="\t", skiprows=data_start)

    # --- clean header ---
    cols = df.columns.tolist()
    cols = [c.strip() for c in cols]

    # replace common naming errors
    if "Frame#" in cols[0] or "Frame" in cols[0]:
        cols[0] = "Frame"
    if "Time" in cols[1]:
        cols[1] = "Time"

    # fill unnamed columns properly
    new_cols = []
    coord_labels = ["_X", "_Y", "_Z"]
    coord_idx = 0
    current_marker = None

    for c in cols:
        if "Unnamed" in c:
            # continue last marker
            if current_marker:
                new_cols.append(current_marker + coord_labels[coord_idx])
                coord_idx = (coord_idx + 1) % 3
            else:
                new_cols.append(c)
        elif c not in ("Frame", "Time"):
            current_marker = c
            coord_idx = 0
            new_cols.append(current_marker + coord_labels[coord_idx])
            coord_idx = 1
        else:
            new_cols.append(c)

    df.columns = new_cols
    df = df.apply(pd.to_numeric, errors="coerce")

    print(f" Loaded marker data with {len(df.columns)} columns starting from line {data_start}")
    print("First 15 columns:", new_cols[:15])
    return df


def load_grf_data(file_path="data/Trial1_GRF.mot"):
    """Load ground reaction force data from a .mot file."""
    grf_data = pd.read_csv(file_path, sep='\t', skiprows=5)
    return grf_data


def load_kinematics_data(file_path="data/Trial1_kinematics.mot"):
    """Load kinematics data from a .mot file."""
    kinematics_data = pd.read_csv(file_path, sep='\t', skiprows=10)
    return kinematics_data