import sys
sys.path.append('/project/mmlab_template/mmdeploy/build/lib/')
import mmdeploy_python

import cv2

detector = mmdeploy_python.Detector('/project/mmlab_template/work_dirs/icdar2019_tracka_modern/faster_rcnn/faster_rcnn_r101_fpn_1x_coco', 'cuda', 0)

img = cv2.imread('/project/mmlab_template/data/icdar2019/test/TRACKA/cTDaR_t10184.jpg')

result = detector([img])

print(result)