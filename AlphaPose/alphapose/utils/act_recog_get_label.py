import numpy as np
import json


# Get sitting or standing label
def get_label(keypoints, angle):
    left_thigh = [keypoints[11][0] - keypoints[13][0], keypoints[11][1] - keypoints[13][1]]
    right_thigh = [keypoints[12][0] - keypoints[14][0], keypoints[12][1] - keypoints[14][1]]
    left_calf = [keypoints[15][0] - keypoints[13][0], keypoints[15][1] - keypoints[13][1]]
    right_calf = [keypoints[16][0] - keypoints[14][0], keypoints[16][1] - keypoints[14][1]]
    left_leg_angle = calculate_angle(left_thigh, left_calf)
    right_leg_angle = calculate_angle(right_thigh, right_calf)
    if left_leg_angle > angle and right_leg_angle > angle:
        return "standing", left_leg_angle, right_leg_angle
    else:
        return "sitting", left_leg_angle, right_leg_angle


# Calculate knee bend angle
def calculate_angle(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)
    # 避免除数为零或接近零的情况
    if magnitude1 < 1e-6 or magnitude2 < 1e-6 or magnitude1 * magnitude2 == 0:
        # 设置一个默认角度值，或者采取其他处理方式
        angle = np.pi
    else:
        cos_int = dot_product / (magnitude1 * magnitude2)
        # 将值限制在 [-1, 1] 范围内
        cos_int = np.clip(cos_int, -1, 1)
        angle = np.arccos(cos_int)

    return np.degrees(angle)
