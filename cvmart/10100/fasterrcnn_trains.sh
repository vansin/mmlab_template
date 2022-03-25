# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/project/TensorRT-8.2.3.0
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/project/cuda
# export TENSORRT_DIR=/project/train/src_repo/TensorRT-8.2.3.0
# export CUDNN_DIR=/project/cuda

export TENSORRT_DIR=/project/TensorRT-8.2.3.0
export LD_LIBRARY_PATH=$TENSORRT_DIR/lib:$TENSORRT_DIR
export CUDNN_DIR=/project/cuda
export LD_LIBRARY_PATH=${CUDNN_DIR}/lib:${LD_LIBRARY_PATH}

python /project/mmlab_template/mmdeploy/tools/deploy.py \
/project/mmlab_template/mmdeploy/configs/mmdet/detection/detection_tensorrt_dynamic-320x320-1344x1344.py \
/project/train/models/faster_rcnn_r50_fpn_1x_coco.py \
/project/train/models/epoch_10.pth \
/home/data/599/fire_p_190.jpg \
--work-dir /project/train/models \
--device cuda \
--dump-info



