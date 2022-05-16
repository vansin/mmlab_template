# Copyright (c) OpenMMLab. All rights reserved.
import argparse
import os
import os.path as osp
# import time
import warnings
from xmlrpc.client import boolean

import mmcv
import torch
from mmcv import Config, DictAction
from mmcv.cnn import fuse_conv_bn
from mmcv.parallel import MMDataParallel, MMDistributedDataParallel
from mmcv.runner import (get_dist_info, init_dist, load_checkpoint,
                         wrap_fp16_model)

from mmdet.apis import multi_gpu_test, single_gpu_test
from mmdet.datasets import (build_dataloader, build_dataset,
                            replace_ImageToTensor)
from mmdet.models import build_detector
import custom


from common.aliyun_oss.test_eval_store import TestEvalStore
from common.model_op.deepl import addEval

def parse_args():
    parser = argparse.ArgumentParser(
        description='MMDet test (and eval) a model')
    # parser.add_argument('--config', default=config,
    #                     help='test config file path')
    # parser.add_argument('--checkpoint', default=checkpoint,
    #                     help='checkpoint file')
    parser.add_argument(
        '--work-dir',
        help='the directory to save the file containing evaluation metrics')
    parser.add_argument(
        '--work_dirs',
        default='work_dirs',
        help='special the directories to eval')
    # parser.add_argument('--out', default=out,
    #                     help='output result file in pickle format')
    parser.add_argument(
        '--fuse-conv-bn',
        action='store_true',
        help='Whether to fuse conv and bn, this will slightly increase'
        'the inference speed')
    parser.add_argument(
        '--format-only',
        action='store_true',
        help='Format the output results without perform evaluation. It is'
        'useful when you want to format the result to a specific format and '
        'submit it to the test server')
    parser.add_argument(
        '--eval',
        default='mAP',
        type=str,
        nargs='+',
        help='evaluation metrics, which depends on the dataset, e.g., "bbox",'
        ' "segm", "proposal" for COCO, and "mAP", "recall" for PASCAL VOC')
    parser.add_argument('--show', action='store_true', help='show results')
    parser.add_argument(
        '--show-dir', help='directory where painted images will be saved')
    parser.add_argument(
        '--show-score-thr',
        type=float,
        default=0.3,
        help='score threshold (default: 0.3)')

    parser.add_argument(
        '--eval_json',
        type=boolean,
        default=True,
        help='score threshold (default: 0.3)')

    parser.add_argument(
        '--gpu-collect',
        action='store_true',
        help='whether to use gpu to collect results.')
    parser.add_argument(
        '--tmpdir',
        help='tmp directory used for collecting results from multiple '
        'workers, available when gpu-collect is not specified')
    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. If the value to '
        'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
        'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
        'Note that the quotation marks are necessary and that no white space '
        'is allowed.')
    parser.add_argument(
        '--options',
        nargs='+',
        action=DictAction,
        help='custom options for evaluation, the key-value pair in xxx=yyy '
        'format will be kwargs for dataset.evaluate() function (deprecate), '
        'change to --eval-options instead.')
    parser.add_argument(
        '--eval-options',
        nargs='+',
        action=DictAction,
        help='custom options for evaluation, the key-value pair in xxx=yyy '
        'format will be kwargs for dataset.evaluate() function')
    parser.add_argument(
        '--launcher',
        choices=['none', 'pytorch', 'slurm', 'mpi'],
        default='none',
        help='job launcher')
    parser.add_argument('--local_rank', type=int, default=0)
    args = parser.parse_args()
    if 'LOCAL_RANK' not in os.environ:
        os.environ['LOCAL_RANK'] = str(args.local_rank)

    if args.options and args.eval_options:
        raise ValueError(
            '--options and --eval-options cannot be both '
            'specified, --options is deprecated in favor of --eval-options')
    if args.options:
        warnings.warn('--options is deprecated in favor of --eval-options')
        args.eval_options = args.options
    return args


def func1(args_config, args_checkpoint, args_out, eval_json, args):

    pkl_exist = TestEvalStore.is_exist(args_out)
    eval_json_exist = TestEvalStore.is_exist(eval_json)

    is_out_exist = osp.exists(args_out)
    is_eval_json_exist = osp.exists(eval_json)

    checkpoint_path = args_checkpoint

    assert args_out or args.eval or args.format_only or args.show \
        or args.show_dir, \
        ('Please specify at least one operation (save/eval/format/show the '
         'results / save the results) with the argument "--out", "--eval"'
         ', "--format-only", "--show" or "--show-dir"')

    if args.eval and args.format_only:
        raise ValueError('--eval and --format_only cannot be both specified')

    if args_out is not None and not args_out.endswith(('.pkl', '.pickle')):
        raise ValueError('The output file must be a pkl file.')

    cfg = Config.fromfile(args_config)

    if args.cfg_options is not None:
        cfg.merge_from_dict(args.cfg_options)
    # import modules from string list.
    if cfg.get('custom_imports', None):
        from mmcv.utils import import_modules_from_strings
        import_modules_from_strings(**cfg['custom_imports'])
    # set cudnn_benchmark
    if cfg.get('cudnn_benchmark', False):
        torch.backends.cudnn.benchmark = True

    cfg.model.pretrained = None
    if cfg.model.get('neck'):
        if isinstance(cfg.model.neck, list):
            for neck_cfg in cfg.model.neck:
                if neck_cfg.get('rfp_backbone'):
                    if neck_cfg.rfp_backbone.get('pretrained'):
                        neck_cfg.rfp_backbone.pretrained = None
        elif cfg.model.neck.get('rfp_backbone'):
            if cfg.model.neck.rfp_backbone.get('pretrained'):
                cfg.model.neck.rfp_backbone.pretrained = None

    # in case the test dataset is concatenated
    samples_per_gpu = 1
    if isinstance(cfg.data.test, dict):
        cfg.data.test.test_mode = True
        samples_per_gpu = cfg.data.test.pop('samples_per_gpu', 1)
        if samples_per_gpu > 1:
            # Replace 'ImageToTensor' to 'DefaultFormatBundle'
            cfg.data.test.pipeline = replace_ImageToTensor(
                cfg.data.test.pipeline)
    elif isinstance(cfg.data.test, list):
        for ds_cfg in cfg.data.test:
            ds_cfg.test_mode = True
        samples_per_gpu = max(
            [ds_cfg.pop('samples_per_gpu', 1) for ds_cfg in cfg.data.test])
        if samples_per_gpu > 1:
            for ds_cfg in cfg.data.test:
                ds_cfg.pipeline = replace_ImageToTensor(ds_cfg.pipeline)

    # init distributed env first, since logger depends on the dist info.
    if args.launcher == 'none':
        distributed = False
    else:
        distributed = True
        init_dist(args.launcher, **cfg.dist_params)

    rank, _ = get_dist_info()
    # allows not to create
    # if args.work_dir is not None and rank == 0:
    #     mmcv.mkdir_or_exist(osp.abspath(args.work_dir))
    #     timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    #     json_file = osp.join(args.work_dir, f'eval_{timestamp}.json')

    # build the dataloader
    dataset = build_dataset(cfg.data.test)
    data_loader = build_dataloader(
        dataset,
        samples_per_gpu=samples_per_gpu,
        workers_per_gpu=cfg.data.workers_per_gpu,
        dist=distributed,
        shuffle=False)

    # build the model and load checkpoint
    # if not is_out_exist:
    if not pkl_exist:

        cfg.model.train_cfg = None
        model = build_detector(cfg.model, test_cfg=cfg.get('test_cfg'))
        fp16_cfg = cfg.get('fp16', None)
        if fp16_cfg is not None:
            wrap_fp16_model(model)
        checkpoint = load_checkpoint(
            model, args_checkpoint, map_location='cpu')
        if args.fuse_conv_bn:
            model = fuse_conv_bn(model)
        # old versions did not save class info in checkpoints, this walkaround is
        # for backward compatibility
        if 'CLASSES' in checkpoint.get('meta', {}):
            model.CLASSES = checkpoint['meta']['CLASSES']
        else:
            model.CLASSES = dataset.CLASSES

        if not distributed:
            model = MMDataParallel(model, device_ids=[0])
            outputs = single_gpu_test(model, data_loader, args.show, args.show_dir, args.show_score_thr)
        else:
            model = MMDistributedDataParallel(
                model.cuda(),
                device_ids=[torch.cuda.current_device()],
                broadcast_buffers=False)
            outputs = multi_gpu_test(model, data_loader, args.tmpdir, args.gpu_collect)
    else:
        if not eval_json_exist:
            TestEvalStore.get(args_out, args_out)
            outputs = mmcv.load(args_out)

    # if args_out and not is_out_exist:
    if args_out and not pkl_exist:
        print(f'\nwriting results to {args_out}')
        mmcv.dump(outputs, args_out)
        # 同步到阿里云oss
        TestEvalStore.put_file(key=args_out, file_path=args_out)

    if args.eval_json == False:
        return

    rank, _ = get_dist_info()
    # if rank == 0 and not is_eval_json_exist:
    if rank == 0 and not eval_json_exist:
    # if rank == 0 and True:

        kwargs = {} if args.eval_options is None else args.eval_options
        if args.format_only:
            dataset.format_results(outputs, **kwargs)
        if args.eval:
            eval_kwargs = cfg.get('evaluation', {}).copy()
            # hard-code way to remove EvalHook args
            for key in [
                    'interval', 'tmpdir', 'start', 'gpu_collect', 'save_best',
                    'rule'
            ]:
                eval_kwargs.pop(key, None)
            eval_kwargs.update(dict(metric=args.eval, **kwargs))
            metric = dataset.evaluate(outputs, **eval_kwargs)
            # print(metric)
            print(checkpoint_path)
            metric_dict = dict(config=args_config, metric=metric, checkpoint_size=osp.getsize(
                checkpoint_path) / 1024 / 1024)

            mmcv.dump(metric_dict, eval_json)
            addEval(eval_json)
            TestEvalStore.put_file(key=eval_json, file_path=eval_json)


def main():

    args = parse_args()



    algorithm_list = []
    for root, dirs, files in os.walk(args.work_dirs):
        print("root", root)  # 当前目录路径
        # print("dirs", dirs)  # 当前路径下所有子目录
        print("files", files)  # 当前路径下所有非目录子文件

        if files.__len__() > 0 and 'tf_logs' not in root:
            algorithm_list.append([root, files])  
            
    for i, element in enumerate(algorithm_list):
        root, work_dir_files = element
        pth_files = []
        config_file = None
        for file_name in work_dir_files:
            if file_name.endswith('.pth'):
                pth_files.append(root + '/' + file_name)
            if file_name.endswith('.py'):
                config_file = root + '/' + file_name


        config_file_key = config_file.replace('work_dirs', 'work_dirs_no_pth')
        if not TestEvalStore.is_exist(config_file_key):
            TestEvalStore.put_file(config_file_key, config_file)


        for j, pth_file in enumerate(pth_files):
            print('===========', i, algorithm_list.__len__(),
                  j, pth_files.__len__(), '=============')

            print(config_file, ' ', pth_file)
            out = pth_file
            out = out.replace('.pth', '.pkl')
            out = out.replace('work_dirs', 'work_dirs_no_pth')

            eval_json = pth_file.replace('.pth', '_eval.json')
            eval_json = eval_json.replace('work_dirs', 'work_dirs_no_pth')
            # main(config_file, pth_file, out, eval_json)

            if 'latest.pth' in pth_file:
                continue

            func1(config_file, pth_file, out, eval_json, args)


if __name__ == '__main__':
    
    
    main()

    from common.notify.notify_robot import NotifyRobot
    # NotifyRobot('开始训练', '开始训练', '开始训练')

    try:
        main()
        NotifyRobot('测试成功', '测试成功', '测试成功')
    except Exception as e:
        NotifyRobot('测试失败', '测试失败', '测试失败')
        NotifyRobot('测试失败', '测试失败', str(e))
