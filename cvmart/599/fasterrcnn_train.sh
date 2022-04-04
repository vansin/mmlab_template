export DNAME=599

python /project/mmlab_template/tools/dataset_converters/cvmarr_${DNAME}_to_coco.py
# python /project/train/mmlab_template/tools/train.py /project/train/mmlab_template/configs/icdar2019_fire/faster_rcnn/faster_rcnn_r101_fpn_1x_coco.py --work-dir /project/train/models
python /project/mmlab_template/tools/train.py /project/mmlab_template/configs/599/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py --work-dir /project/train/models/${DNAME} --auto-resume