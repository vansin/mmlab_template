import sys
sys.path.append('/project/mmlab_template/mmdeploy/build/lib/')
import mmdeploy_python

import cv2

detector = mmdeploy_python.Detector('/project/train/models', 'cuda', 0)

img = cv2.imread('/home/data/599/fire_8556.jpg')

result = detector([img])

print(result)