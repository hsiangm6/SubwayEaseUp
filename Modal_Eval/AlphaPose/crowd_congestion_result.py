import os
import subprocess

from AlphaPose.head_count.final import head_count, head_count_in_multi
from AlphaPose.scripts.act_recog_result import action_recognition


def comprehensive_evaluation(head_count_level: int, action_recognition_level: int):
    """
    Calculate a comprehensive evaluation score based on head count and action recognition levels.

    Parameters:
    - head_count_level (int): A value representing the level of head count detection.
    - action_recognition_level (int): A value representing the level of action recognition performance.

    Returns:
    - Tuple (str, float): A tuple containing two elements:
        - The first element is a string indicating the evaluation category ('low', 'medium', 'high', or 'error').
        - The second element is a float representing the calculated comprehensive evaluation score.
    """

    # Calculate the weighted sum of head count and action recognition levels
    levels_count = head_count_level * 0.8 + action_recognition_level * 0.2

    # Determine the evaluation category based on the comprehensive score
    if 0 < levels_count <= 1:
        return '不壅擠', levels_count
    elif 1 < levels_count <= 2:
        return '尚可', levels_count
    elif 2 < levels_count <= 3.5:
        return '壅擠', levels_count
    else:
        return 'unknown', levels_count


def crowd_congestion_result(input_img: str='', work_dir: str='', output_dir: str='',hc_save_img: bool=False, ar_save_img: bool=False):
    """
    Process crowd congestion results for multi or single images.

    Parameters:
    - input_img (str): Path to the input image or directory containing multiple images.
    - work_dir (str): Path to the working directory.
    - hc_save_img (bool): Flag to indicate whether to save head count images.
    - ar_save_img (bool): Flag to indicate whether to save action recognition images.

    Returns:
    - dict: A dictionary containing the final results for each processed image.
    """

    # Create directories
    res_dir = os.path.join(output_dir, 'res')
    vis_dir = os.path.join(res_dir, 'vis')
    vis_head_count_dir = os.path.join(res_dir, 'vis_head_count')

    # Check if directories exist and create them if not
    for directory in [res_dir, vis_dir, vis_head_count_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # input directory: multi img
    if os.path.isdir(input_img):
        input_dir = input_img

        head_count_finish_code, head_count_dict = head_count_in_multi(input_dir=input_dir, output_path=output_dir, hc_save_img=hc_save_img)

        if head_count_finish_code != 0:

            if ar_save_img is True:
                command = (f'python {work_dir}/scripts/demo_inference.py '
                           f'--cfg {work_dir}/configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml '
                           f'--checkpoint {work_dir}/pretrained_models/fast_res50_256x192.pth '
                           f'--indir {input_img} '
                           f'--outdir {output_dir}/res '
                           f'--save_img '
                           f' --showbox '
                           f'--vis_fast')
            else:
                command = (f'python {work_dir}/scripts/demo_inference.py '
                           f'--cfg {work_dir}/configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml '
                           f'--checkpoint {work_dir}/pretrained_models/fast_res50_256x192.pth '
                           f'--indir {input_img} '
                           f'--outdir {output_dir}/res ')

            process = subprocess.Popen(command, shell=True)

            # Wait for the command to complete
            process.wait()

            act_recog_dict = action_recognition(output_dir)
            final_result = {}
            for img_name in head_count_dict:
                head_count_info = head_count_dict[img_name]
                # Use get() to avoid errors if img_name is not in act_recog_dict
                act_recog_info = act_recog_dict.get(img_name, {})

                try:
                    final_level, levels_count = comprehensive_evaluation(head_count_info["hc_congestion_level"],
                                                                     act_recog_info["ar_congestion_level"])
                except KeyError:
                    final_level, levels_count = '不壅擠', 1

                final_result[img_name] = {
                    **head_count_info,
                    **act_recog_info,
                    'final_level': final_level,
                    'levels_count': levels_count
                }

            return final_result
        else:
            return head_count_dict

    # input single img path
    elif os.path.isfile(input_img):

        head_count_finish_code, head_count_dict = head_count(img_path=input_img, hc_save_img=hc_save_img)

        if head_count_finish_code != 0:
            if ar_save_img is True:
                command = (f'python {work_dir}/scripts/demo_inference.py '
                           f'--cfg {work_dir}/configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml '
                           f'--checkpoint {work_dir}/pretrained_models/fast_res50_256x192.pth '
                           f'--image {input_img} '
                           f'--outdir {output_dir}/res '
                           f'--save_img '
                           f'--showbox '
                           f'--vis_fast')
            else:
                command = (f'python {work_dir}/scripts/demo_inference.py '
                           f'--cfg {work_dir}/configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml '
                           f'--checkpoint {work_dir}/pretrained_models/fast_res50_256x192.pth '
                           f'--image {input_img} '
                           f'--outdir {output_dir}/res '
                           f'--showbox')

            process = subprocess.Popen(command, shell=True)

            # Wait for the command to complete
            process.wait()
            act_recog_dict = action_recognition(output_dir)

            # return act_recog_dict
            final_result = {}
            for img_name in head_count_dict:
                head_count_info = head_count_dict[img_name]
                # Use get() to avoid errors if img_name is not in act_recog_dict
                act_recog_info = act_recog_dict.get(img_name, {})

                try:
                    final_level = comprehensive_evaluation(head_count_info["hc_congestion_level"],
                                                           act_recog_info["ar_congestion_level"])
                except KeyError:
                    final_level = '不壅擠'

                final_result[img_name] = {
                    **head_count_info,
                    **act_recog_info,
                    'final_level': final_level
                }

            return final_result

        else:
            return head_count_dict
    else:
        return "You don't input img_path"
