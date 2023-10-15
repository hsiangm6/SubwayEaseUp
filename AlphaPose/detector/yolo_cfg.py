import os

from easydict import EasyDict as edict
# Get the directory containing the script (yolox_api.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative paths
config_path = os.path.join(script_dir, 'yolo', 'cfg', 'yolov3-spp.cfg')
weights_path = os.path.join(script_dir, 'yolo', 'data', 'yolov3-spp.weights')

cfg = edict()
cfg.CONFIG = config_path
cfg.WEIGHTS = weights_path
cfg.INP_DIM =  608
cfg.NMS_THRES =  0.6
cfg.CONFIDENCE = 0.1
cfg.NUM_CLASSES = 80
