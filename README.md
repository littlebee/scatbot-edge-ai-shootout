<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

**Table of Contents** _generated with [DocToc](https://github.com/thlorenz/doctoc)_

- [scatbot-edge-ai-shootout](#scatbot-edge-ai-shootout)
  - [Why?](#why)
  - [Why would you do it at the edge?](#why-would-you-do-it-at-the-edge)
  - [Testing ethos and methods](#testing-ethos-and-methods)
  - [Hardware Configurations Tested](#hardware-configurations-tested)
    - [Raspberry Pi 4b](#raspberry-pi-4b)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# scatbot-edge-ai-shootout

A place to chronicle performance of various hardware and software solutions for using computer vision and AI at the edge for object detection.

## Why?

I build bots to train and entertain my canine housemate. Robotics automation routines like tracking and following your pet around the house require that we be able detect when a dog or cat is in the field of view (FOV) and, even more important, where in the FOV - how many degrees off center - the detected object is.

## Why would you do it at the edge?

It's true that for most applications around the house you could probably just set up a base computer that was much more powerful. All the computer hardware on the bot would do is send sensor data and video back and receive motor commands in.

**But that's not cool!** you yell? I'm with you. I want it to be fully autonomous and self contained. It's not really an issue if you have a good mesh and some onboard cliff detection, but you don't want to send the bot accidentally careening down the basement stairs when the connection to the controller drops. This does not mean you're limited to just one single board computer (SBC) on the robot however. For some applications, like bots that fit under furniture, you'll have a difficult time fitting a second Pi 4 onto an already crowded chassis that is about as big as your 3D printer will allow you to print.

This means, at a minimum, that we need to have available some percentage of cpu for behavior logic, video streaming / recording and reading other sensors. Using the Intel Realsense D435i depth camera and librealvision in Python, for example, can take up to 35% of the Raspberry PI 4 overall CPU.

## The Benchmark

For the application at hand, it does us little good to know how fast we can read and do object detection on a mp4 video file. Likewise, it's also useless to include any sort of display or saving of augmented images for a headless robot.

What we really need for most robotics applications is to know many frames per second (FPS) we can acquire the image from the camera, convert it to whatever format is needed by the ML framework or model, and invoke the ML model to produce an array of bounding coordinates as numbers, the classification label as string, and the confidence as a float value. How much time it takes to convert the data and produce the required output are very relevant to the application and are part reflected in the results. The benchmarks measures and reports the _overall_ FPS including pre and post processing.

There is [a test provided](https://github.com/littlebee/scatbot-edge-ai-shootout/blob/main/debug/test-camera.py) to see how fast openCV is able to read from the camera without object detection. Spoiler: with almost every configuration and camera including USB, this test is going to report just under 30 frames per second.

It is also relevant to robotics applications to know how many FPS the object detection can produce while running on a single board computer with other software running. We want to know both, how the object detection works without anything else running, and how it performs when only 50% or 25% of the SBC CPU is available for object detection. If space and battery constraints allow, We want to know how much better it would perform if object detection had its own dedicated SBC.

### Shell Script & Individual Python Benchmark Scripts

Instead of using Python to run all of the benchmarks, we use a BASH script (benchmarks.sh in repo root) to run the individual, stand alone Python scripts. This is intended to isolate each benchmark by causing a new python process to instantiate. Any effects, memory leaks, GC, etc from one benchmark should not effect any other benchmark.

#### Run all benchmarks:

```
cd scatbot-edge-ai-shootout
./benchmarks.sh
```

### Run a benchmark for a single framework:

To run, for example, just TensorFlow Lite without tpu coprocessor:

```
cd scatbot-edge-ai-shootout
./benchmark-tflite.py
```

## Hardware Configurations Tested

### Raspberry Pi 4b

Performance data is provided for both the 4GB and 8GB versions of the Raspberry Pi 4b. All tests are run on the 64 bit version of the Raspian Linux distribution codename Bullseye.

See the [setup guide for Raspberry Pi4](https://github.com/littlebee/scatbot-edge-ai-shootout/blob/main/Setup%20Raspberry%20Pi4.md) for more information about how to setup all of the things.

### Coral USB Accelerator

Performance results are provided for Tensor Flow with and without the [Coral USB Accelerator](https://coral.ai/products/accelerator/).

## Software Configurations Tested

### TensorFlow Lite via tflite_support

This benchmark uses [TensorFlow Lite](https://www.tensorflow.org/lite/guide) via the [tflight_support module](https://www.tensorflow.org/lite/api_docs/python/tflite_support).

### PyTorch via torchvision

This benchmark uses [PyTorch](https://pytorch.org/) via the [torchvision](https://pytorch.org/vision/stable/index.html) library.

### YOLOv5 via PyTorch Hub

The YOLOv5 benchmark uses YOLO (you only look once) version 5 via PyTorch Hub. The time to download the yolo model and weights one time costs and are not included in the FPS measurement.
