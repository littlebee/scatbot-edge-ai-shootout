<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [scatbot-edge-ai-shootout](#scatbot-edge-ai-shootout)
  - [Disclaimer](#disclaimer)
  - [The Results](#the-results)
  - [Why?](#why)
  - [Why would you do it at the edge?](#why-would-you-do-it-at-the-edge)
  - [The Benchmark](#the-benchmark)
    - [Shell Script & Individual Python Benchmark Scripts](#shell-script--individual-python-benchmark-scripts)
      - [Run all benchmarks:](#run-all-benchmarks)
    - [Run a benchmark for a single framework:](#run-a-benchmark-for-a-single-framework)
  - [Hardware Configurations Tested](#hardware-configurations-tested)
    - [Raspberry Pi 4b](#raspberry-pi-4b)
    - [Coral USB Accelerator](#coral-usb-accelerator)
  - [Software Configurations Tested](#software-configurations-tested)
    - [TensorFlow Lite via tflite_support](#tensorflow-lite-via-tflite_support)
    - [PyTorch via torchvision](#pytorch-via-torchvision)
    - [YOLOv5 via PyTorch Hub](#yolov5-via-pytorch-hub)
  - [Hardware and Software Setup](#hardware-and-software-setup)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# scatbot-edge-ai-shootout

A place to chronicle performance of various hardware and software solutions for using computer vision and AI at the edge for object detection.

## Disclaimer

I have, to date, received exactly $0.00 in compensation from any company for this work, nor am I seeking any. I overpaid for all of the hardware used herein.

## The Results

That's why you came here right? Let's cut to the chase.

<img src="https://github.com/littlebee/scatbot-edge-ai-shootout/blob/main/docs/images/pi4b4gb_results/pi4b4gb_chart.png"
     alt="Raspberry Pi 4 4GB Results Chart"
     style="margin: 30px;" />

### The model matters

The chart above is grouped by model first because, as it turns out, the **model almost matters more** than the framework for performance!

Look, for example, at the left two clusters which represent the throughput of the two models that are included with the official [TensorFlow Lite Example for Raspbery Pi 4](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi). The first cluster is the model compiled for use with the Coral USB coprocessor; the second is the model without TPU support. Looking at those first two clusters you might conclude that the Coral coprocessor is worthless until there is downward CPU pressure. With the right model from the [Coral object detection models web page](https://coral.ai/models/object-detection/), the Coral TPU is definitely worth the money if you are looking for greater than 15 FPS and is also the only option I've found so far capable of that on an Pi 4b.

<img src="https://github.com/littlebee/scatbot-edge-ai-shootout/blob/main/docs/images/pi4b4gb_results/pi4b4gb_rollup.png"
     alt="Raspberry Pi 4 4GB Results Rollup"
     style="margin: 30px;" />

You can also see a nice resistance to downward CPU pressure provided by the Coral TPU.

### The raw data

The [Google Sheet for the Pi 4b w/GB](https://docs.google.com/spreadsheets/d/1LXBu7aTxJHfXpfTashEkwpSy_eArMZYGN5jX-iU5H9I/edit?usp=sharing) has the individual run data including a few details, like peak CPU temperature. It also turns out that a [fan is kinda necessary](https://docs.google.com/spreadsheets/d/1OunzVdvjCsR7pb2HZ-KAyl6a1l6dVf1urdRFchbyeJE/edit?usp=sharing) when stressing the Pi's CPU for long periods. 😂

### What about the Pi 4 w/8GB

In case you are wondering if upgrading to a Pi 4b w/8GB will improve your performance, [the answer is no](https://docs.google.com/spreadsheets/d/1Hg6KqjM1XklWzadYWLZX_fj89gi2aZGdOFT6RKGLaas/edit?usp=sharing). Put that money towards a Coral TPU.

## Why?

I build bots to train and entertain my canine housemate. Robotics automation routines like tracking and following your pet around the house require that we be able detect when a dog or cat is in the field of view (FOV) and, even more important, where in the FOV - how many degrees off center - the detected object is.

The higher the performance of object detection correlates to a higher chance of successfully tracking and following an object.

## Why would you do it at the edge?

It's true that for most applications around the house you could probably just set up a base computer that was much more powerful. All the computer hardware on the bot would do is send sensor data and video back and receive motor commands in.

**But that's not cool!** you yell? I'm with you. I want it to be fully autonomous and self contained. If I needed a second computer, I would rather just put the second computer on board the bot, but sometimes [space and battery constraints](https://github.com/littlebee/scatbot) make a second onboard SBC impossible. This means, at a minimum, that we need to have available some percentage of CPU for behavior logic, video streaming / recording and reading sensors. Using the Intel Realsense D435i depth camera and librealvision in Python, for example, can take up to 35% of the Raspberry PI 4 overall CPU.

## The Benchmark

For the application at hand, it does us little good to know how fast we can read and do object detection on a mp4 video file. Likewise, it's also useless to include any sort of display or saving of augmented images for a headless robot.

What we really need for most robotics applications is to know many frames per second (FPS) we can acquire the image from the camera, convert it to whatever format is needed by the ML framework or model, and invoke the ML model to produce an array of bounding coordinates as numbers, the classification label as string, and the confidence as a float value. How much time it takes to convert the data and produce the required output are very relevant to the application and are reflected in the results. The benchmarks measure and report the _overall_ FPS including pre and post processing.

For the capturing video, all of the benchmarks use [OpenCV](https://opencv.org/) to acquire the image from the camera. For the results above, all results were measured using the official Raspberry Pi 4 Camera Module and ribbon cable connection. This means that **the upper limit FPS for any object detection is 30 FPS**. Additionally, all benchmarks are **using a 640x480 captured image**. No scaling is done for any of the benchmarks. Past experience with performance of this tells me there is overhead with downscaling the image that rarely gets recovered by using a smaller image.

There is [a test provided](https://github.com/littlebee/scatbot-edge-ai-shootout/blob/main/debug/test-camera.py) to see how fast openCV is able to read from the camera without object detection. Spoiler: with almost every configuration and camera, including USB, this test is going to report just under 30 frames per second.

It is also relevant to robotics applications to know how many FPS the object detection can produce while running on a single board computer with other software running. We want to know both, how fast the object detection works without anything else running, and how it performs when only 50% or 25% of the SBC CPU cores are available for object detection.

### Shell Script & Individual Python Benchmark Scripts

Instead of using Python to run all of the benchmarks, we use a BASH script (benchmarks.sh in repo root) to run the individual, stand alone Python scripts. This is intended to isolate each benchmark by causing a new python process to instantiate. Any effects, memory leaks, GC, etc from one benchmark should not effect any other benchmark.

Each benchmark (framework + model) is run 10 times for 30 seconds with a 20 second rest between each benchmark. After every 10 runs of each, a background process is spawned that consumes 100% of one core or 25% of the overall CPU availability on a 4 core processor such as the Raspberry Pi 4.

See the [benchmarks.sh script](https://github.com/littlebee/scatbot-edge-ai-shootout/blob/main/benchmarks.sh) for more information.

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

Performance data is provided for both the 4GB and 8GB versions of the Raspberry Pi 4b. All tests are run on the 64 bit "lite" version of the Raspian Linux distribution codename Bullseye.

See the [setup guide for Raspberry Pi4](https://github.com/littlebee/scatbot-edge-ai-shootout/blob/main/Setup%20Raspberry%20Pi4.md) for more information about how to setup all of the things.

### Coral USB Accelerator

Performance results are provided for Tensor Flow with and without the [Coral USB Accelerator](https://coral.ai/products/accelerator/).

## Software Configurations Tested

### TensorFlow Lite via tflite_support

This benchmark uses [TensorFlow Lite](https://www.tensorflow.org/lite/guide) via the [tflight_support module](https://www.tensorflow.org/lite/api_docs/python/tflite_support).

The code for init and detecting objects based on the [TensorFlow Lite example for Raspberry PI](https://github.com/tensorflow/examples/blob/5d3579cb1057d31c260be4289a32ebc0a91782e0/lite/examples/object_detection/raspberry_pi/detect.py).

Results are provided for both the models used in the above TensorFlow Lite example and for the best performing models I've found with Coral support from the from https://coral.ai/models/object-detection/. MobileNet V1 quantized model from Coral is one of two from that list of models that actually works on the Pi 4 via tflite_support. The models listed as "New" on the Coral models web page were not compiled with metadata and will not load via tflite_support without modification, but the the ones I was able to test, have the same relative performance to [Coral's published performance](https://coral.ai/docs/edgetpu/benchmarks/). MobileNet V1 and V2 are closer in performance and it was V1 that had the better average over 10 runs.

### PyTorch via torchvision

This benchmark uses [PyTorch](https://pytorch.org/) via the [torchvision](https://pytorch.org/vision/stable/index.html) library. I tried [several different models](https://github.com/littlebee/scatbot-edge-ai-shootout/blob/1715caa4220fce76a436aedef3a6942357299da2/benchmark-pytorch.py#L30) from `torchvision.models.detection`. By far the fastest and also the most accurate was `fasterrcnn_mobilenet_v3_large_320_fpn`. You can manually run one of the other models using, for example `./benchmark-pytorch --model fasterrcnn_resnet50_fpn`.

### YOLOv5 via PyTorch Hub

The YOLOv5 benchmark uses [YOLO (you only look once) version 5](https://github.com/ultralytics/yolov5) via PyTorch Hub. The time to download the yolo model and weights are one time costs and are not included in the FPS measurement.

## Hardware and Software Setup

Consult the [setup.sh script](https://github.com/littlebee/scatbot-edge-ai-shootout/blob/main/setup.sh) in the root of the project directory for information on how the various software was installed.

You can also use the setup.sh script to setup a freshly flashed Bullseye 64bit OS Lite. See [the setup doc](https://github.com/littlebee/scatbot-edge-ai-shootout/blob/main/Setup%20Raspberry%20Pi4.md) for more details and alternate install methods.
