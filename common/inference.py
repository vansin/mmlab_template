from mmdet.apis import init_detector, inference_detector

config_file = 'work_dirs/icdar2019_fire/detectors/cascade_rcnn_r50_rfp_1x_coco/cascade_rcnn_r50_rfp_1x_coco.py'
checkpoint_file = 'work_dirs/icdar2019_fire/detectors/cascade_rcnn_r50_rfp_1x_coco/epoch_12.pth'


model = init_detector(config_file, checkpoint_file)

img = '/home/data/599/2119a7.jpg'  # or img = mmcv.imread(img), which will only load it once
result = inference_detector(model, img)
objects = []
fires = result[0]
for fire in fires:
    obj = dict(
        xmin=fire[0],
        ymin=fire[1],
        xmax=fire[2],
        ymax=fire[3],
        confidence=fire[4],
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


print(r_json)

