_base_ = './tablebank_cvpr2020_both:fcos_r50_caffe_fpn_gn-head_1x.py'
model = dict(
    backbone=dict(
        depth=101,
        init_cfg=dict(
            type='Pretrained',
            checkpoint='open-mmlab://detectron/resnet101_caffe')))
