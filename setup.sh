#!/bin/bash

log() {
  set +x
  echo "#"
  echo "# $1"
  echo "#"
  set -x
}

# echo on
set -x

# stop on errors
set -e

# Start with Raspian Bullseye 64bit OS Lite image
#

DATA_DIR="./data"
TFLITE_DATA_DIR="$DATA_DIR/tflite"

#sudo apt-get update
#sudo apt-get -y upgrade

log 'Installing OS prerequisites'
sudo apt install -y python3-pip git

log 'Installing opencv & deps (https://singleboardblog.com/install-python-opencv-on-raspberry-pi/)'
sudo apt-get install -y libhdf5-dev libhdf5-serial-dev python3-pyqt5 libatlas-base-dev
sudo pip3 install --upgrade pip setuptools wheel
# see (https://www.piwheels.org/project/opencv-contrib-python/)
sudo pip3 install opencv-contrib-python-headless==4.5.5.62

log 'Installing pytorch'
sudo pip3 install torch torchvision torchaudio
sudo pip3 install numpy --upgrade
sudo pip3 install matplotlib
sudo pip3 install werkzeug==2.0.3

log 'Installing tensor flow lite (https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi)'
sudo apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo pip3 install tflite-support==0.4.0
sudo pip3 install "protobuf>=3.18.0,<4"

# Download TF Lite models

mkdir -p $TFLITE_DATA_DIR
FILE=${TFLITE_DATA_DIR}/efficientdet_lite0.tflite
if [ ! -f "$FILE" ]; then
  log 'downloading tflight model'
  curl \
    -L 'https://tfhub.dev/tensorflow/lite-model/efficientdet/lite0/detection/metadata/1?lite-format=tflite' \
    -o ${FILE}
fi

FILE=${TFLITE_DATA_DIR}/efficientdet_lite0_edgetpu.tflite
if [ ! -f "$FILE" ]; then
  log 'downloading tflight model'
  curl \
    -L 'https://storage.googleapis.com/download.tensorflow.org/models/tflite/edgetpu/efficientdet_lite0_edgetpu_metadata.tflite' \
    -o ${FILE}
fi


log 'Installing coral edge usb tpu (https://coral.ai/docs/accelerator/get-started)'
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y libedgetpu1-std
sudo apt-get install -y python3-pycoral


if [ ! -d "yolov5" ]; then
  log "Installing yolo v5 (https://github.com/ultralytics/yolov5)"
  git clone https://github.com/ultralytics/yolov5
  cd yolov5
  sudo pip3 install -r requirements.txt
  cd ..
fi

log 'Done'
set +x
echo "Be sure to run "
echo "  sudo raspi-config "
echo "and ENABLE 'Legacy Camera Support' under 'Interfaces'"
