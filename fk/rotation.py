import torch

def rotate_by_axis(point, axis, angle):
    """Rotate a 3D point around x, y, or z axis by given angle (radians)."""
    axis = axis.float()
    angle = angle.float()

    if torch.allclose(axis, torch.tensor([1, 0, 0], dtype=torch.float32)):  # X-axis
        R = torch.tensor([
            [1, 0, 0],
            [0, torch.cos(angle), -torch.sin(angle)],
            [0, torch.sin(angle),  torch.cos(angle)]
        ])
    elif torch.allclose(axis, torch.tensor([0, 1, 0], dtype=torch.float32)):  # Y-axis
        R = torch.tensor([
            [torch.cos(angle), 0, torch.sin(angle)],
            [0, 1, 0],
            [-torch.sin(angle), 0, torch.cos(angle)]
        ])
    elif torch.allclose(axis, torch.tensor([0, 0, 1], dtype=torch.float32)):  # Z-axis
        R = torch.tensor([
            [torch.cos(angle), -torch.sin(angle), 0],
            [torch.sin(angle),  torch.cos(angle), 0],
            [0, 0, 1]
        ])
    else:
        # Rodrigues' rotation formula (arbitrary axis)
        axis = axis / torch.norm(axis)
        x, y, z = axis
        c, s = torch.cos(angle), torch.sin(angle)
        R = torch.stack([
            torch.stack([c + x*x*(1-c),     x*y*(1-c) - z*s, x*z*(1-c) + y*s]),
            torch.stack([y*x*(1-c) + z*s,   c + y*y*(1-c),   y*z*(1-c) - x*s]),
            torch.stack([z*x*(1-c) - y*s,   z*y*(1-c) + x*s, c + z*z*(1-c)])
        ])

    rotated_point = R @ point
    rotated_point = torch.round(rotated_point, decimals=6)
    rotated_point = torch.where(torch.abs(rotated_point) < 1e-6,
                                torch.tensor(0.0, dtype=rotated_point.dtype),
                                rotated_point)
    return rotated_point, R


def rotate_multi_axis(point, order, angles):
    """Sequential rotations (extrinsic, x→y→z)."""
    if isinstance(order, list):
        order = order[0]

    axis_map = {
        'x': torch.tensor([1., 0., 0.], dtype=torch.float32),
        'y': torch.tensor([0., 1., 0.], dtype=torch.float32),
        'z': torch.tensor([0., 0., 1.], dtype=torch.float32)
    }

    R_total = torch.eye(3, dtype=torch.float32)
    for ax, ang in zip(order, angles):
        _, R_axis = rotate_by_axis(torch.zeros(3), axis_map[ax], ang)
        R_total = R_axis @ R_total

    p_rotated = R_total @ point
    p_rotated = torch.where(torch.abs(p_rotated) < 1e-6,
                            torch.tensor(0.0, dtype=p_rotated.dtype),
                            p_rotated)
    return p_rotated, R_total