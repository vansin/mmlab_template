
export DNAME=10185

# python /project/mmlab_template/tools/dataset_converters/cvmarr_${DNAME}_to_coco.py
# # python /project/train/mmlab_template/tools/train.py /project/train/mmlab_template/configs/icdar2019_fire/faster_rcnn/faster_rcnn_r101_fpn_1x_coco.py --work-dir /project/train/models
# python /project/mmlab_template/tools/train.py /project/mmlab_template/configs/${DNAME}/yolo/yolov3_mobilenetv2_mstrain-416_300e_coco.py --work-dir /project/train/models/${DNAME} --auto-resume
# #bash /project/mmlab_template/cvmart/599/yolov3_mobilenetv2_mstrain-416_300e_coco.sh


export TENSORRT_DIR=/project/TensorRT-8.2.3.0
export LD_LIBRARY_PATH=$TENSORRT_DIR/lib:$TENSORRT_DIR
export CUDNN_DIR=/project/cuda
export LD_LIBRARY_PATH=${CUDNN_DIR}/lib64:${LD_LIBRARY_PATH}

export PATH=$PATH:/usr/local/cuda-11.1/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH://usr/local/cuda-11.1/lib64
python /project/mmlab_template/tools/dataset_converters/cvmarr_${DNAME}_to_coco.py
python /project/mmlab_template/mmdeploy/tools/deploy.py \
/project/mmlab_template/mmdeploy/configs/mmdet/detection/detection_tensorrt-int8_dynamic-160x160-608x608.py \
/project/mmlab_template/configs/${DNAME}/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py \
/project/train/models/${DNAME}/latest.pth \
/home/data/901/171.jpg \
--work-dir /project/train/models/${DNAME} \
--device cuda \
--dump-info



