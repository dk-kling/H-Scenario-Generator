# Installation Manual

## Setting up anaconda environment

Create conda environment for python 3.6.9
```shell
conda create -n hsg python=3.6.9
conda activate hsg
```

## Python packages

Install Python packages
```shell
pip install -r requirements.txt
```

## Build Carla PythonAPI

Ref. https://carla.readthedocs.io/en/0.9.10/build_linux/

Dependencies
```shell
sudo apt-get update &&
sudo apt-get install wget software-properties-common &&
sudo add-apt-repository ppa:ubuntu-toolchain-r/test &&
wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add - &&
sudo apt-add-repository "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-8 main" &&
sudo apt-get update
```

Ubuntu 18.04
```shell
sudo apt-get install build-essential clang-8 lld-8 g++-7 cmake ninja-build libvulkan1 python python-pip python-dev python3-dev python3-pip libpng-dev libtiff5-dev libjpeg-dev tzdata sed curl unzip autoconf libtool rsync libxml2-dev libxerces-c-dev &&
pip2 install --user setuptools &&
pip3 install --user -Iv setuptools==47.3.1 &&
pip2 install --user distro &&
pip3 install --user distro
sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/lib/llvm-8/bin/clang++ 180 &&
sudo update-alternatives --install /usr/bin/clang clang /usr/lib/llvm-8/bin/clang 180

```

Build using make
```shell
cd carla
make PythonAPI
```

Check if the file exists :: `H-Scenario-Generator/carla/PythonAPI/`  

## Setting up docker

Install docker-ce
```shell
sudo apt remove docker docker-engine docker.io
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce
```

Set up permissions
```shell
sudo groupadd docker
sudo usermod -aG docker ${USER}
sudo su - ${USER}
```

## (Optional) Setting up nvidia driver

Check recommended driver name such as `nvidia-driver-XXX`
```shell
sudo add-apt-repository ppa:graphics-drivers
sudo apt update
ubuntu-drivers devices
```

Install nvidia driver (Reboot is contained)
```shell
sudo apt install nvidia-driver-XXX
sudo reboot now
nvidia-smi
```

Install nvidia-docker2
```shell
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt update
sudo apt install nvidia-docker2
sudo systemctl restart docker
```

## Install Carla 0.9.10.1 docker

Pull docker image
```shell
docker pull carlasim/carla:0.9.10.1
```

