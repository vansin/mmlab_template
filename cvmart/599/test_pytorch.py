import json
from mmdet.apis import init_detector, inference_detector
import mmcv

def init():

    config_file = '/project/train/models/yolov3_mobilenetv2_mstrain-416_300e_coco.py'
    checkpoint_file = '/project/train/models/latest.pth'
    # build the model from a config file and a checkpoint file
    model = init_detector(config_file, checkpoint_file)
    return model

def process_image(handle=None, input_image=None, args=None, **kwargs):
    
    result = inference_detector(handle, input_image)
    # Process image here
    objects = []
    fires = result[0]
    for fire in fires:
        obj = dict(
            xmin = int(fire[0].item()),
            ymin= int(fire[1].item()),
            xmax=int(fire[2].item()),
            ymax=int(fire[3].item()),
            confidence=fire[4].item(),
            name = "fire"
        )

        if obj['confidence']>0.5:
            objects.append(obj)

    # model.show_result(img, result)
    # model.show_result(img, result, out_file='result.jpg', score_thr = 0.3)

    r_json = dict()
    r_json['algorithm_data'] = dict(target_info=objects, is_alert=False, target_count=0)
    r_json['model_data'] = dict(objects=objects)

    if objects.__len__()>0:
        r_json['algorithm_data']['is_alert'] = True
        r_json['algorithm_data']['target_count'] = objects.__len__()

    # return json.dumps(objects, indent=4)

    return json.dumps(r_json, indent=4)
