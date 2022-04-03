import json
from torch import R
from mmdet_custom.datasets import FireDataset as NormalDataset




import os
os.system('export TENSORRT_DIR=/project/TensorRT-8.2.3.0')
os.system('export LD_LIBRARY_PATH=$TENSORRT_DIR/lib:$TENSORRT_DIR')
os.system('export CUDNN_DIR=/project/cuda')
os.system('export LD_LIBRARY_PATH=${CUDNN_DIR}/lib64:${LD_LIBRARY_PATH}')

import sys
sys.path.append('/project/mmlab_template/mmdeploy/build/lib/')
import mmdeploy_python


def init():
    
    detector = mmdeploy_python.Detector('/project/train/599/models', 'cuda', 0)
    return detector

def process_image(handle=None, input_image=None, args=None, **kwargs):
    
    # result = inference_detector(handle, input_image)]


    result = handle([input_image])
    objects = []
    v1, v2, v3 = result[0][0], result[0][1], result[0][2]
    target_count = 0

    for i,j,k in zip(v1, v2, v3):

        print(i,j,k)
        obj = dict(
            xmin=i[0].item(),
            ymin=i[1].item(),
            xmax=i[2].item(),
            ymax=i[3].item(),
            confidence=i[4].item(),
            name=NormalDataset.CLASSES[j.item()]
        )
        if obj['confidence']>0.5:
            objects.append(obj)
            if obj['name']==NormalDataset.CLASSES[0]:
                target_count+=1

    r_json = dict()
    r_json['algorithm_data'] = dict(target_info=objects, is_alert=False, target_count=0)
    r_json['model_data'] = dict(objects=objects)

        
    if target_count>0:
        r_json['algorithm_data']['is_alert'] = True
        r_json['algorithm_data']['target_count'] = target_count

    a = json.dumps(r_json, indent=4)

    return a
