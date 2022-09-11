import time
import os

import cv2

from .system_stats import *
from .csv_file import append_results

cpu_avail_start = get_cpu_available()


class CameraBenchmark(object):

    # see lib/benchmark_args.py for args and defaults that come from command line
    def __init__(self, args):
        self.args = args

        camera_channel = args.camera_channel
        frame_height = args.frame_height
        frame_width = args.frame_width

        print(
            f"INFO: initializing OpenCV on camera_channel {camera_channel} @ {frame_width}X{frame_height}")
        self.camera = cv2.VideoCapture(camera_channel)

        # We need to check if camera is opened previously or not
        if (self.camera.isOpened() == False):
            self.raise_error('Error initializing opencv cameraCapture')

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    def __del__(self):
        if hasattr(self, "camera"):
            self.camera.release()

    def raise_error(self, msg):
        raise RuntimeError(
            "{msg}. Set env var OPENCV_VIDEOIO_DEBUG=1 for more information")

    def run_benchmark(self):
        global cpu_avail_start
        duration = self.args.duration
        printDetections = self.args.verbose

        name = self.get_benchmark_name()
        model = self.get_model_name()
        peak_cpu_temp = 0

        print(f"INFO: running {name} benchmark for {duration}secs...")

        num_frames = 0
        start = time.time()
        while((time.time() - start) < duration):
            if num_frames % 5 == 0:
                cpu_temp = get_cpu_temp()
                if cpu_temp > peak_cpu_temp:
                    peak_cpu_temp = cpu_temp

            ret, frame = self.camera.read()
            if ret != True:
                self.raise_error('opencv camera.read returned false')
            num_frames += 1
            detections = self.get_prediction(frame)
            if printDetections:
                print(
                    f"INFO: detected {len(detections)} objects. {detections}")

        # the loop above stops after duration + length of time for last prediction
        actual_duration = time.time() - start
        fps = num_frames / actual_duration
        results = {
            "name": name,
            "args": self.args,
            "actual_duration": actual_duration,
            "peak_cpu_temp": peak_cpu_temp,
            "fps": fps,
        }
        print(f"INFO: {name} complete.  FPS={fps}")

        if self.args.csv_file:
            append_results(self.args.csv_file, {
                "name": name,
                "model": model,
                "num_threads": self.args.num_threads,
                "enable_coral": self.args.enable_coral,
                "frame_height": self.args.frame_height,
                "frame_width": self.args.frame_width,
                "duration": actual_duration,
                "cpu_avail_start": cpu_avail_start,
                "max_cpu_temp": peak_cpu_temp,
                "fps": fps,
            })

        return results

    @staticmethod
    def get_prediction(frame):
        raise RuntimeError('get_prediction must be implemented by subclass.')

    @staticmethod
    def get_benchmark_name():
        raise RuntimeError(
            'get_benchmark_name must be implemented by subclass.')

    @staticmethod
    def get_model_name():
        raise RuntimeError(
            'get_model_name must be implemented by subclass.')
