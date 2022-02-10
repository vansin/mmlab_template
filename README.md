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


## select gpu to run

```shell
CUDA_VISIBLE_DEVICES=1 python tools/test_batch.py
```