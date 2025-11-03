import matplotlib.pyplot as plt
import numpy as np

def visualize_markers(marker_positions_FK, marker_positions_exp):
    """
    Visualize markers from Forward Kinematics (red) and experimental data (green).
    Works with both dict inputs.
    """
    fig = plt.figure(figsize=(10, 4))

    # Three anatomical planes
    for i in range(3):
        ax = fig.add_subplot(131 + i)
        idx = [0, 1] if i == 0 else [2, 1] if i == 1 else [0, 2]
        plane = "Sagittal" if i == 0 else "Frontal" if i == 1 else "Transverse"

        # Plot FK (model) markers — red
        for marker_name, marker_pos in marker_positions_FK.items():
            ax.plot(marker_pos[idx[0]], marker_pos[idx[1]], 'rx')
            ax.text(marker_pos[idx[0]], marker_pos[idx[1]], marker_name, color='red', fontsize=6)

        # Plot experimental markers — green
        for marker_name, marker_pos in marker_positions_exp.items():
            ax.plot(marker_pos[idx[0]], marker_pos[idx[1]], 'gx')
            ax.text(marker_pos[idx[0]], marker_pos[idx[1]], marker_name, color='green', fontsize=6)

        ax.set_title(f"{plane} Plane")
        ax.axis('equal')

    plt.tight_layout()
    plt.show()


def evaluate_marker_error(marker_positions_FK, marker_positions_exp):
    """
    Compute RMSE error between FK and experimental markers.
    Both must be dicts of {marker_name: np.array([x, y, z])}.
    """
    errors = []
    for name in marker_positions_FK.keys():
        if name in marker_positions_exp:
            err = np.linalg.norm(marker_positions_FK[name] - marker_positions_exp[name])
            errors.append(err ** 2)
    if len(errors) == 0:
        return np.nan
    return np.sqrt(np.mean(errors))