export DNAME=9985
export img_paht=/home/data/918/ZDScrowddensity20220402_V1_train_60927.jpg
export algorthm_path=yolox/yolox_s_8x8_300e_coco

# python /project/mmlab_template/tools/dataset_converters/cvmarr_${DNAME}_to_coco.py
# # python /project/train/mmlab_template/tools/train.py /project/train/mmlab_template/configs/icdar2019_fire/faster_rcnn/faster_rcnn_r101_fpn_1x_coco.py --work-dir /project/train/models
# python /project/mmlab_template/tools/train.py /project/mmlab_template/configs/${DNAME}/yolo/yolov3_mobilenetv2_mstrain-416_300e_coco.py --work-dir /project/train/models/${DNAME} --auto-resume
# #bash /project/mmlab_template/cvmart/599/yolov3_mobilenetv2_mstrain-416_300e_coco.sh


export TENSORRT_DIR=/project/TensorRT-8.2.3.0
export LD_LIBRARY_PATH=$TENSORRT_DIR/lib:$TENSORRT_DIR
export CUDNN_DIR=/project/cuda
export LD_LIBRARY_PATH=${CUDNN_DIR}/lib64:${LD_LIBRARY_PATH}

python /project/mmlab_template/mmdeploy/tools/test.py \
/project/mmlab_template/mmdeploy/configs/mmdet/detection/detection_tensorrt-fp16_dynamic-320x320-1344x1344.py \
/project/mmlab_template/configs/${DNAME}/${algorthm_path}.py \
--model /project/train/models/${DNAME}/${algorthm_path}/end2end.engine \
--out /project/train/models/${DNAME}/${algorthm_path}/out.pkl \
--speed-test \
--device cuda

