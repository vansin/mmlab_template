export DNAME=10185
export algorthm_path=yolox/yolox_nano_8x8_300e_coco

cd /project/mmlab_template
python /project/mmlab_template/tools/dataset_converters/cvmarr_${DNAME}_to_coco.py
# python /project/train/mmlab_template/tools/train.py /project/train/mmlab_template/configs/icdar2019_fire/faster_rcnn/faster_rcnn_r101_fpn_1x_coco.py --work-dir /project/train/models
python /project/mmlab_template/tools/train_new.py /project/mmlab_template/configs/${DNAME}/${algorthm_path}.py --work-dir /project/train/models --auto-resume


#bash /project/mmlab_template/cvmart/599/yolov3_mobilenetv2_mstrain-416_300e_coco.sh