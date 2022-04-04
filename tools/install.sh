
# conda create -n cvmart python=3.9 -y
# conda activate cvmart
# pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
# pip install mmcv-full==1.4.7 -f https://download.openmmlab.com/mmcv/dist/cu111/torch1.9.0/index.html


# wget https://cdn.vansin.top/cudnn-11.3-linux-x64-v8.2.1.32.tgz
# wget https://cdn.vansin.top/cuda_11.1.0_455.23.05_linux.run
# wget https://cdn.vansin.top/TensorRT-8.2.3.0.Linux.x86_64-gnu.cuda-11.4.cudnn8.2.tar.gz


# download the cudnn 
tar -zxvf TensorRT-8.2.3.0.Linux.x86_64-gnu.cuda-11.4.cudnn8.2.tar.gz*
tar -zxvf cudnn-11.3-linux-x64-v8.2.1.32.tgz*

cp /project/cuda/lib64/* /usr/local/cuda/lib64/
cp /project/cuda/include/* /usr/local/cuda/include

cp /project/ 

sudo apt-get update
sudo apt-get install libspdlog-dev -y

# 安装ppl.cv
cd /project/
git clone https://github.com/openppl-public/ppl.cv.git
cd /project/ppl.cv
export PPLCV_DIR=$(pwd)
./build.sh cuda


# 安装onnxruntime
pip install onnxruntime==1.8.1
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
cd /project
wget https://github.com/microsoft/onnxruntime/releases/download/v1.8.1/onnxruntime-linux-x64-1.8.1.tgz
tar -zxvf onnxruntime-linux-x64-1.8.1.tgz
cd onnxruntime-linux-x64-1.8.1
export ONNXRUNTIME_DIR=$(pwd)
export LD_LIBRARY_PATH=$ONNXRUNTIME_DIR/lib:$LD_LIBRARY_PATH


cd /project
pip install TensorRT-8.2.3.0/python/tensorrt-8.2.3.0-cp39-none-linux_x86_64.whl
export TENSORRT_DIR=$(pwd)/TensorRT-8.2.3.0
export LD_LIBRARY_PATH=$TENSORRT_DIR/lib:$LD_LIBRARY_PATH

export CUDNN_DIR=$(pwd)/cuda
export LD_LIBRARY_PATH=$CUDNN_DIR/lib64:$LD_LIBRARY_PATH

export MMDEPLOY_DIR=/project/mmlab_template/mmdeploy


cd ${MMDEPLOY_DIR}
mkdir -p build && cd build
cmake -DCMAKE_CXX_COMPILER=g++-7 -DMMDEPLOY_TARGET_BACKENDS=ort -DONNXRUNTIME_DIR=${ONNXRUNTIME_DIR} ..
make -j$(nproc)

cd ${MMDEPLOY_DIR}
mkdir -p build && cd build
cmake -DCMAKE_CXX_COMPILER=g++-7 -DMMDEPLOY_TARGET_BACKENDS=trt -DTENSORRT_DIR=${TENSORRT_DIR} -DCUDNN_DIR=${CUDNN_DIR} ..
make -j$(nproc)

cd ${MMDEPLOY_DIR}
pip install -e .

cd ${MMDEPLOY_DIR}
mkdir -p build && cd build
cmake .. \
    -DCMAKE_CXX_COMPILER=g++-7 \
    -DMMDEPLOY_BUILD_SDK=ON \
    -DMMDEPLOY_BUILD_SDK_PYTHON_API=ON \
    -DMMDEPLOY_TARGET_DEVICES=cpu \
    -DMMDEPLOY_TARGET_BACKENDS=ort \
    -DMMDEPLOY_CODEBASES=all \
    -DONNXRUNTIME_DIR=${ONNXRUNTIME_DIR}

make -j$(nproc) && make install


cd ${MMDEPLOY_DIR}
mkdir -p build && cd build
cmake .. \
    -DCMAKE_CXX_COMPILER=g++-7 \
    -DMMDEPLOY_BUILD_SDK=ON \
    -DMMDEPLOY_BUILD_SDK_PYTHON_API=ON \
    -DMMDEPLOY_TARGET_DEVICES="cuda;cpu" \
    -DMMDEPLOY_TARGET_BACKENDS=trt \
    -DMMDEPLOY_CODEBASES=all \
    -Dpplcv_DIR=${PPLCV_DIR}/cuda-build/install/lib/cmake/ppl \
    -DTENSORRT_DIR=${TENSORRT_DIR} \
    -DCUDNN_DIR=${CUDNN_DIR}

make -j$(nproc) && make install


cd ${MMDEPLOY_DIR}/build/install/example
mkdir -p build && cd build
cmake .. -DMMDeploy_DIR=${MMDEPLOY_DIR}/build/install/lib/cmake/MMDeploy
make -j$(nproc)