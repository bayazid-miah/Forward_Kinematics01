import torch
from fk.rotation import rotate_by_axis

def forward_kinematics(q, key, kintree):
    """
    Compute global joint and marker positions for a nested dict-based OpenSim kinematic tree.
    Compatible with match_markers_but_ignore_physics.osim.
    """
    q_map = {name: torch.tensor(val, dtype=torch.float32) for name, val in zip(key, q)}
    joint_positions, marker_positions = {}, {}

    # --- root pelvis transform (translation + 3 rotations) ---
    T_root = torch.eye(4, dtype=torch.float32)
    pelvis = kintree["pelvis"]

    # Translation
    tx = q_map.get("pelvis_tx", torch.tensor(0.0))
    ty = q_map.get("pelvis_ty", torch.tensor(0.0))
    tz = q_map.get("pelvis_tz", torch.tensor(0.0))
    T_root[:3, 3] = torch.tensor([tx, ty, tz])

    # Rotation order: tilt → list → rotation
    for jname in ["pelvis_tilt", "pelvis_list", "pelvis_rotation"]:
        if jname in pelvis["joints"]:
            axis = torch.tensor(pelvis["joints"][jname]["axis"], dtype=torch.float32)
            angle = q_map.get(jname, torch.tensor(0.0))
            _, R = rotate_by_axis(torch.zeros(3), axis, angle)
            T_rot = torch.eye(4)
            T_rot[:3, :3] = R
            T_root = T_root @ T_rot

    # --- recursive FK ---
    def recurse(seg_name, seg_data, T_parent):
        offset = torch.tensor(seg_data.get("offset", [0, 0, 0]), dtype=torch.float32)
        T_local = torch.eye(4, dtype=torch.float32)
        T_local[:3, 3] = offset

        # Apply local joints
        for jname, jinfo in seg_data.get("joints", {}).items():
            if jname in ["pelvis_tilt", "pelvis_list", "pelvis_rotation", "pelvis_tx", "pelvis_ty", "pelvis_tz"]:
                continue  # already handled above
            q_val = q_map.get(jname, torch.tensor(0.0))
            axis = torch.tensor(jinfo["axis"], dtype=torch.float32)
            if jinfo["type"] == "hinge":
                _, R = rotate_by_axis(torch.zeros(3), axis, q_val)
                T_joint = torch.eye(4)
                T_joint[:3, :3] = R
            elif jinfo["type"] == "slider":
                T_joint = torch.eye(4)
                T_joint[:3, 3] = axis * q_val
            else:
                continue
            T_local = T_local @ T_joint

        # Global transform
        T_global = T_parent @ T_local
        joint_positions[seg_name] = T_global[:3, 3]

        # Attached markers
        for mname, mpos in seg_data.get("markers", {}).items():
            m_local = torch.cat([torch.tensor(mpos, dtype=torch.float32), torch.tensor([1.0])])
            m_world = T_global @ m_local
            marker_positions[mname] = m_world[:3]

        # Children
        for child_name, child_data in seg_data.get("children", {}).items():
            recurse(child_name, child_data, T_global)

    # start recursion
    recurse("pelvis", pelvis, T_root)
    return joint_positions, marker_positions

# NEW FUNCTION

def get_connections(kintree, joint_positions):
    
    connections = []

    def recurse(parent_name, parent_data):
        for child_name, child_data in parent_data.get("children", {}).items():
            # add only if both joints exist
            if parent_name in joint_positions and child_name in joint_positions:
                connections.append((parent_name, child_name))
            recurse(child_name, child_data)

    recurse("pelvis", kintree["pelvis"])
    return connections