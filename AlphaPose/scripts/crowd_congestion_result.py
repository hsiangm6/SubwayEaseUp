import os
import subprocess

from .act_recog_result import action_recognition
from ..head_count.final import head_count, head_count_in_multi


# hc_output_dir: "examples/res/vis_head_count"
# ar_output_dir: "examples/res/"


# evaluate final crowd congestion result
def comprehensive_evaluation(head_count_level, action_recognition_level):
    levels_count = head_count_level * 0.8 + action_recognition_level * 0.2
    if 0 < levels_count <= 1:
        return 'low', levels_count
    elif 1 < levels_count <= 2:
        return 'medium', levels_count
    elif 2 < levels_count <= 3.5:
        return 'high', levels_count
    else:
        return 'error', levels_count


def crowd_congestion_result(input_img="", hc_save_img=False, ar_save_img=False):
    # input directory: multi img
    if os.path.isdir(input_img):

        input_dir = input_img
        head_count_finish_code, head_count_dict = head_count_in_multi(input_dir=input_dir, hc_save_img=hc_save_img)
        if head_count_finish_code != 0:

            if ar_save_img is True:
                command = (r'python scripts/demo_inference.py --cfg configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml '
                           r'--checkpoint pretrained_models/fast_res50_256x192.pth --indir ') + input_img + (
                              ' --outdir '
                              'examples/res '
                              '--save_img '
                              ' --showbox '
                              '--vis_fast')
            else:
                command = (r'python scripts/demo_inference.py --cfg configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml '
                           r'--checkpoint pretrained_models/fast_res50_256x192.pth --indir ') + input_img + (
                              ' --outdir '
                              'examples/res ')
            process = subprocess.Popen(command, shell=True)
            process.wait()  # 等待指令執行完成

            act_recog_dict = action_recognition()
            final_result = {}
            for img_name in head_count_dict:
                head_count_info = head_count_dict[img_name]
                # 使用get()避免img_name不存在於act_recog_dict中時出錯
                act_recog_info = act_recog_dict.get(img_name, {})
                final_level, levels_count = comprehensive_evaluation(head_count_info["hc_congestion_level"],
                                                       act_recog_info["ar_congestion_level"])
                final_result[img_name] = {
                    **head_count_info,
                    **act_recog_info,
                    'final_level': final_level,
                    'levels_count': levels_count
                }

            return final_result
            # print(json.dumps(final_result, indent=4))
        else:
            return head_count_dict

# input single img path
    elif os.path.isfile(input_img):

        head_count_finish_code, head_count_dict = head_count(img_path=input_img, hc_save_img=hc_save_img)

        if head_count_finish_code != 0:
            if ar_save_img is True:
                command = (r'python scripts/demo_inference.py --cfg configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml '
                           r'--checkpoint pretrained_models/fast_res50_256x192.pth --image ') + input_img + (
                              ' --outdir '
                              'examples/res '
                              '--save_img '
                              '--showbox '
                              '--vis_fast')
            else:
                command = (r'python scripts/demo_inference.py --cfg configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml '
                           r'--checkpoint pretrained_models/fast_res50_256x192.pth --image ') + input_img + (
                              ' --outdir '
                              'examples/res '
                              '--showbox')
            process = subprocess.Popen(command, shell=True)
            process.wait()  # 等待指令執行完成
            act_recog_dict = action_recognition()

            # return act_recog_dict
            final_result = {}
            for img_name in head_count_dict:
                head_count_info = head_count_dict[img_name]
                # 使用get()避免img_name不存在於act_recog_dict中時出錯
                act_recog_info = act_recog_dict.get(img_name, {})
                final_level = comprehensive_evaluation(head_count_info["hc_congestion_level"],
                                                       act_recog_info["ar_congestion_level"])
                final_result[img_name] = {
                    **head_count_info,
                    **act_recog_info,
                    'final_level': final_level
                }

            return final_result

        else:
            return head_count_dict
            # print(head_count_dict)
    else:
        return "You don't input img_path"
        # print("You don't input img_path")
