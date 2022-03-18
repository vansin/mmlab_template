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
-Dpplcv_DIR=/project/train/ppl.cv/cuda-build/install/lib/cmake/ppl \
-DOpenCV_DIR=/usr/local/lib/cmake/opencv4 \
-DTENSORRT_DIR=/project/TensorRT-8.4.0.6 \
-DCUDNN_DIR=/project/cudnn-linux-x86_64-8.3.2.44_cuda11.5-archive
cmake --build . -- -j$(nproc) && cmake --install .

export PATH=/usr/local/cuda-11.0:$PATH
export LD_LIBRARY_PATH=/project/TensorRT-8.4.0.6/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/project/cudnn-linux-x86_64-8.3.2.44_cuda11.5-archive/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.0/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/project/mmlab_template/mmdeploy/build/lib

```



python tools/deploy.py \
/project/mmlab_template/mmdeploy/configs/mmdet/detection/detection_tensorrt_dynamic-320x320-1344x1344.py  \
/project/train/models/retinanet_r50_fpn_1x_coco.py \
/project/train/models/epoch_10.pth \
/home/data/816/street_garbage_public_roads_avenue_CID_train_p_day_20220127_1009.jpg \
--device cuda \
--work-dir /project/train/models --dump-info
```

```shell
Driver:   Not Selected
Toolkit:  Installed in /usr/local/cuda-11.3/
Samples:  Installed in /root/, but missing recommended libraries

Please make sure that
 -   PATH includes /usr/local/cuda-11.3/bin
 -   LD_LIBRARY_PATH includes /usr/local/cuda-11.3/lib64, or, add /usr/local/cuda-11.3/lib64 to /etc/ld.so.conf and run ldconfig as root

To uninstall the CUDA Toolkit, run cuda-uninstaller in /usr/local/cuda-11.3/bin
***WARNING: Incomplete installation! This installation did not install the CUDA Driver. A driver of version at least 465.00 is required for CUDA 11.3 functionality to work.
To install the driver using this installer, run the following command, replacing <CudaInstaller> with the name of this run file:
    sudo <CudaInstaller>.run --silent --driver
```

```shell
export PYTHONPATH=/project/mmlab_template/mmdeploy/build/lib

```