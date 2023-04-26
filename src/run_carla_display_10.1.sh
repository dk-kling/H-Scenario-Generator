#!/bin/bash

docker run --name="carla-10.1" -it \
  -d --rm --privileged \
  --gpus all --runtime=nvidia \
  -e DISPLAY=$DISPLAY \
  --net=host \
  carlasim/carla:0.9.10.1 \
  /bin/bash -c \
  'CUDA_DEVICE_ORDER=PCI_BUS_ID \
  CUDA_VISIBLE_DEVICES=1 ./CarlaUE4.sh \
  -nosound -windowed -opengl \
  -carla-rpc-port=2000 \
  -quality-level=Epic'
