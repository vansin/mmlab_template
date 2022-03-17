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

```shell
cmake .. -DCMAKE_CXX_COMPILER=g++-7 -DMMDEPLOY_BUILD_SDK=ON -DMMDEPLOY_TARGET_DEVICES="cpu;cuda" -DMMDEPLOY_TARGET_BACKENDS="trt" \
-DMMDEPLOY_CODEBASES=all \
-DMMDEPLOY_BUILD_SDK_PYTHON_API=ON \
-Dpplcv_DIR=/tmp/ppl.cv/cuda-build/install/lib/cmake/ppl \
-DOpenCV_DIR=/tmp/opencv-4.5.3/install/lib/cmake/opencv4 \
-DTENSORRT_DIR=/tmp/TensorRT-8.4.0.6 \
-DCUDNN_DIR=/tmp/cudnn-8.2.1

cmake .. -DCMAKE_CXX_COMPILER=g++-7 -DMMDEPLOY_BUILD_SDK=ON -DMMDEPLOY_TARGET_DEVICES="cpu;cuda" -DMMDEPLOY_TARGET_BACKENDS="trt" \
-DMMDEPLOY_CODEBASES=all \
-DMMDEPLOY_BUILD_SDK_PYTHON_API=ON \
-Dpplcv_DIR=/project/train/ppl.cv/cuda-build/install/lib/cmake/ppl \
-DOpenCV_DIR=/usr/local/lib/cmake/opencv4 \
-DTENSORRT_DIR=/project/train/TensorRT-8.4.0.6 \
-DCUDNN_DIR=/project/train/cudnn-linux-x86_64-8.3.2.44_cuda11.5-archive


cmake .. -DCMAKE_CXX_COMPILER=g++-7 -DMMDEPLOY_BUILD_SDK=ON -DMMDEPLOY_TARGET_DEVICES="cpu;cuda" -DMMDEPLOY_TARGET_BACKENDS="trt" \
-DMMDEPLOY_CODEBASES=all \
-DMMDEPLOY_BUILD_SDK_PYTHON_API=ON \
-DTENSORRT_DIR=/project/TensorRT-8.4.0.6 \
-DCUDNN_DIR=/project/cuda


export LD_LIBRARY_PATH=/project/train/TensorRT-8.4.0.6/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/project/train/cudnn-linux-x86_64-8.3.2.44_cuda11.5-archive/lib:$LD_LIBRARY_PATH

```