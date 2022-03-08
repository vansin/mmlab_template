from distutils.command.config import config
from operator import index
from common.app import app, db
from common.models.train_info import TrainInfo
from common.models.eval_info import EvalInfo

import pandas as pd


import getpass
user_name = getpass.getuser()

train_df = '/project/nutstore/ubuntu/paper/data/trained_origin.csv'
eval_df = '/nutstore/ubuntu/paper/data/csv/latest.csv'

train_data_list = train_df.to_dict('records')


for i, train_data in enumerate(train_data_list):
    if i % 100 == 0:
        print(i, train_data_list.__len__())
    
    q_TrainInfo = TrainInfo.query.filter(
        TrainInfo.algorithm == train_data['algorithm'],
        TrainInfo.config == train_data['config'],
        TrainInfo.dataset == train_data['dataset']).first()

    if q_TrainInfo:

        q_TrainInfo.config = train_data['config']
        q_TrainInfo.algorithm = train_data['algorithm']
        q_TrainInfo.dataset = train_data['dataset']

        q_TrainInfo.cmd = train_data['cmd']
        q_TrainInfo.eval_epoch = train_data['eval_epoch']
        q_TrainInfo.epoch = train_data['epoch']
        # db.session.commit()

    else:

        new = TrainInfo()
        new.config = train_data['config']
        new.algorithm = train_data['algorithm']
        new.cmd= train_data['cmd']
        new.dataset = train_data['dataset']
        new.eval_epoch = train_data['eval_epoch']
        new.epoch = train_data['epoch']

        db.session.add(new)
    
db.session.commit()


train_data_list = eval_df.to_dict('records')


for i, train_data in enumerate(train_data_list):

    if i % 100 == 0:
        print(i, train_data_list.__len__())

    epoch = train_data['epoch']
    dataset = train_data['dataset']
    config = train_data['config']
    algorithm = train_data['algorithm']
    checkpoint_size = train_data['checkpoint_size']
    iou = train_data['iou']
    detail = train_data['detail']
    ap = train_data['ap']
    num_gts = train_data['num_gts']
    num_dets = train_data['num_dets']
    recall = train_data['recall']
    precision = train_data['precision']
    f1_score = train_data['f1_score']
    recall_in_max_f1_score = train_data['recall_in_max_f1_score']
    precision_in_max_f1_score = train_data['precision_in_max_f1_score']
    max_f1_score = train_data['max_f1_score']



    q_TrainInfo = EvalInfo.query.filter(
        EvalInfo.epoch == epoch,
        EvalInfo.dataset == dataset,
        EvalInfo.algorithm == algorithm,
        EvalInfo.config == config,
        EvalInfo.iou == iou
        ).first()

    if q_TrainInfo:

        EvalInfo.epoch = train_data['epoch']
        EvalInfo.dataset = train_data['dataset']
        EvalInfo.config = train_data['config']
        EvalInfo.algorithm = train_data['algorithm']
        EvalInfo.checkpoint_size = train_data['checkpoint_size']
        EvalInfo.iou = train_data['iou']
        # EvalInfo.detail = train_data['detail']
        EvalInfo.ap = train_data['ap']
        EvalInfo.num_gts = train_data['num_gts']
        EvalInfo.num_dets = train_data['num_dets']
        EvalInfo.recall = train_data['recall']
        EvalInfo.precision = train_data['precision']
        # EvalInfo.f1_score = train_data['f1_score']
        EvalInfo.recall_in_max_f1_score = train_data['recall_in_max_f1_score']
        EvalInfo.precision_in_max_f1_score = train_data['precision_in_max_f1_score']
        EvalInfo.max_f1_score = train_data['max_f1_score']

        # db.session.commit()

    else:
        
        new = EvalInfo()

        new.epoch = train_data['epoch']
        new.dataset = train_data['dataset']
        new.config = train_data['config']
        new.algorithm = train_data['algorithm']
        new.checkpoint_size = train_data['checkpoint_size']
        new.iou = train_data['iou']
        # new.detail = train_data['detail']
        new.ap = train_data['ap']
        new.num_gts = train_data['num_gts']
        new.num_dets = train_data['num_dets']
        new.recall = train_data['recall']
        new.precision = train_data['precision']
        # new.f1_score = train_data['f1_score']
        new.recall_in_max_f1_score = train_data['recall_in_max_f1_score']
        new.precision_in_max_f1_score = train_data['precision_in_max_f1_score']
        new.max_f1_score = train_data['max_f1_score']

        db.session.add(new)
    
db.session.commit()

# for row in train_df.itertuples():



#     print(row)

# train_data = pd.pivot_table(train_df, index=['cmd'], values=[
#                       'epoch', 'eval_epoch'], )

# eval_data = pd.pivot_table(eval_df, index=['cmd'], values=[
#     'epoch', 'eval_epoch'], )

