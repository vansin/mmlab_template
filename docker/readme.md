docker build docker/GPU/ -t mmdeploy:1 --network=host --cpu-shares 16
docker build docker/GPU/ -t mmdeploy:GPU