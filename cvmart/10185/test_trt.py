# import json
# from mmdet.apis import init_detector, inference_detector
# import mmcv

# def init():

#     config_file = '/project/train/models/599/yolov3_mobilenetv2_mstrain-416_300e_coco.py'
#     checkpoint_file = '/project/train/models/599/latest.pth'
#     # build the model from a config file and a checkpoint file
#     model = init_detector(config_file, checkpoint_file)
#     return model

# def process_image(handle=None, input_image=None, args=None, **kwargs):
    
#     result = inference_detector(handle, input_image)
#     # Process image here
#     objects = []
#     fires = result[0]
#     for fire in fires:
#         obj = dict(
#             xmin = int(fire[0].item()),
#             ymin= int(fire[1].item()),
#             xmax=int(fire[2].item()),
#             ymax=int(fire[3].item()),
#             confidence=fire[4].item(),
#             name = "fire"
#         )

#         if obj['confidence']>0.5:
#             objects.append(obj)

#     # model.show_result(img, result)
#     # model.show_result(img, result, out_file='result.jpg', score_thr = 0.3)

#     r_json = dict()
#     r_json['algorithm_data'] = dict(target_info=objects, is_alert=False, target_count=0)
#     r_json['model_data'] = dict(objects=objects)

#     if objects.__len__()>0:
#         r_json['algorithm_data']['is_alert'] = True
#         r_json['algorithm_data']['target_count'] = objects.__len__()

#     # return json.dumps(objects, indent=4)

#     return json.dumps(r_json, indent=4)


import json
from mmdet_custom.datasets import D10185Dataset as NormalDataset
import os
os.system('export TENSORRT_DIR=/project/TensorRT-8.2.3.0')
os.system('export LD_LIBRARY_PATH=$TENSORRT_DIR/lib:$TENSORRT_DIR')
os.system('export CUDNN_DIR=/project/cuda')
os.system('export LD_LIBRARY_PATH=${CUDNN_DIR}/lib64:${LD_LIBRARY_PATH}')




import sys
sys.path.append('/project/mmlab_template/mmdeploy/build/lib/')
import mmdeploy_python

os.system('echo $LD_LIBRARY_PATH')



def init():
    
    detector = mmdeploy_python.Detector('/project/train/models/10185/yolox/yolox_s_8x8_300e_coco', 'cuda', 0)
    return detector

def process_image(handle=None, input_image=None, args=None, **kwargs):
    
    # result = inference_detector(handle, input_image)]
    # args = json.loads(args)

    result = handle([input_image])
    objects = []
    v1, v2, v3 = result[0][0], result[0][1], result[0][2]
    target_count = 0

    for i,j,k in zip(v1, v2, v3):

        print(i,j,k)
        obj = dict(
            xmin=int(i[0].item()),
            ymin=int(i[1].item()),
            xmax=int(i[2].item()),
            ymax=int(i[3].item()),
            confidence=i[4].item(),
            name=NormalDataset.CLASSES[j.item()]
        )
        if obj['confidence']>0.5:
            objects.append(obj)
            if obj['name']==NormalDataset.CLASSES[0]:
                target_count+=1

    r_json = dict()

    r_json['algorithm_data'] = dict(target_info=objects, is_alert=False, target_count=0)
    r_json['algorithm_data']['target_count'] = target_count

    r_json['model_data'] = dict(objects=objects)
    if target_count> 21:
        r_json['algorithm_data']['is_alert'] = True
        r_json['algorithm_data']['target_count'] = target_count

    a = json.dumps(r_json, indent=4)

    return a
