import json
import cv2



import os
os.system('export TENSORRT_DIR=/project/TensorRT-8.2.3.0')
os.system('export LD_LIBRARY_PATH=$TENSORRT_DIR/lib:$TENSORRT_DIR')
os.system('export CUDNN_DIR=/project/cuda')
os.system('export LD_LIBRARY_PATH=${CUDNN_DIR}/lib:${LD_LIBRARY_PATH}')

import sys
sys.path.append('/project/mmlab_template/mmdeploy/build/lib/')
import mmdeploy_python


def init():
    
    detector = mmdeploy_python.Detector('/project/train/models', 'cuda', 0)
    return detector

def process_image(handle=None, input_image=None, args=None, **kwargs):
    
    # result = inference_detector(handle, input_image)]

    print(input_image)

    result = handle([input_image])
    # Process image here
    objects = []
    fires = result[0][0]
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

