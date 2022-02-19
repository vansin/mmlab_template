# tabledet

## environment prepare


```shell

git clone https://github.com/open-mmlab/mmdetection.git

git submodule init
git submodule update
pip install -v -e .

cd mmdetection
pip install -v -e .

```

### install latest pytorch

```shell
conda create -n mmlab python=3.9 -y
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
```

cpu 版本

```shell
conda create -n mmlab_cpu python=3.9 -y
conda install pytorch torchvision torchaudio cpuonly -c pytorch
pip install mmcv-full=={mmcv_version} -f https://download.openmmlab.com/mmcv/dist/cpu/torch1.10.0/index.html

```

### install mmcv-full

```shell
pip install mmcv-full=={mmcv_version} -f https://download.openmmlab.com/mmcv/dist/cu113/torch1.10.0/index.html
pip install mmcv-full==1.4.4 -f https://download.openmmlab.com/mmcv/dist/cu113/torch1.10.0/index.html
```

### install mmdetection

```shell
pip install -r requirements/build.txt
```

## select gpu to run

```shell
CUDA_VISIBLE_DEVICES=1 python tools/test_batch.py
```