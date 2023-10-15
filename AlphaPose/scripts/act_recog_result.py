# pose estimation
# import os
# os.chdir('C:/Users/hsian/AlphaPose')
# python scripts/demo_inference.py --cfg
# configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml --checkpoint pretrained_models/fast_res50_256x192.pth --image
# C:/Users/hsian/Documents/GitHub/Advanced_Learning/yolo_openpose/people_detection/examples/demo/real_carriage_9.jpg
# --outdir C:/Users/hsian/Documents/GitHub/Advanced_Learning/yolo_openpose/people_detection/examples/res

# action recognition
# python scripts/act_recog_result.py
import json
import numpy as np


# get result of action recognition for each img
def action_recognition():
    # 读取 JSON 文件
    with open('examples/res/alphapose-results.json', 'r') as json_file:  # 替换成你的 JSON 文件路径
        whole_data = json.load(json_file)

    # 使用字典将数据按照 image_id 分组
    grouped_data = {}
    for item in whole_data:
        image_id = item["image_id"]
        if image_id not in grouped_data:
            grouped_data[image_id] = []
        grouped_data[image_id].append(item)

    # action recognition for each person
    action = {}
    for img_data in grouped_data:
        for data in grouped_data[img_data]:
            kp_scores = []
            kp_preds = []
            for i in range(0, len(data["keypoints"]), 3):
                kp_preds.append([data["keypoints"][i], data["keypoints"][i + 1]])
                kp_scores.append(data["keypoints"][i + 2])
            action_flag, left_leg_angle, right_leg_angle = get_label(kp_preds, 145)
            if img_data not in action:
                action[img_data] = []  # 添加这行以确保字典中有对应的键
            # action label, left leg angle, right leg angle, left-up box point x, left-up box point y
            action[img_data].append(
                [action_flag, left_leg_angle, right_leg_angle, data["box"]])

    # group the result for each image
    # group_action = {}
    congestion_level_dict = {}
    for image_id, labels in action.items():
        sitting_count = 0
        standing_count = 0
        for label in labels:
            area = int(label[3][2])*int(label[3][3])
            if area > 23000 and int(label[3][1]) != 0:
                if label[0] == 'sitting':
                    sitting_count += 1
                elif label[0] == 'standing':
                    standing_count += 1

        # group_action[image_id] = {'sitting': sitting_count, 'standing': standing_count}
        congestion_level = judge_level(sitting_count, standing_count)
        congestion_level_dict[image_id] = {
            'ar_congestion_level': congestion_level,
            'sitting': sitting_count,
            'standing': standing_count
        }

    # print(json.dumps(group_action, indent=4))

    return congestion_level_dict
    # print(action)
    # print(json.dumps(action, indent=4))


# 壅擠程度判斷式
def judge_level(sitting_count, standing_count):
    if sitting_count + standing_count < 12:
        return 1
    elif standing_count < 3:
        return 2
    else:
        return 3


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
