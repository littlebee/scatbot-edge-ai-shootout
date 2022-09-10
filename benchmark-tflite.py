#!/usr/bin/env python3
from lib.benchmark_args import parse_cmd_line
from lib.camera_benchmark import CameraBenchmark
import os

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

TF_DATA_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), './data/tflite'))

# Loosely based on Raspberry Pi object detection example
# See, https://github.com/tensorflow/examples/blob/5d3579cb1057d31c260be4289a32ebc0a91782e0/lite/examples/object_detection/raspberry_pi/detect.py


class TfliteCameraBenchmark(CameraBenchmark):

    def __init__(self, args):
        model = args.model
        if model == None:
            if args.enable_coral:
                model = f"{TF_DATA_DIR}/ssd_mobilenet_v1_coco_quant_postprocess_edgetpu.tflite"
            else:
                model = f"{TF_DATA_DIR}/ssd_mobilenet_v1_coco_quant_postprocess.tflite"

        print(f"INFO: tflite using model {model}")

        base_options = core.BaseOptions(
            file_name=model, use_coral=args.enable_coral, num_threads=args.num_threads)
        detection_options = processor.DetectionOptions(
            max_results=3, score_threshold=0.5)
        options = vision.ObjectDetectorOptions(
            base_options=base_options, detection_options=detection_options)

        self.detector = vision.ObjectDetector.create_from_options(options)

        super(TfliteCameraBenchmark, self).__init__(args)

    def get_prediction(self, img):
        input_tensor = vision.TensorImage.create_from_array(img)
        detection_result = self.detector.detect(input_tensor)
        results = []
        if detection_result.detections:
            for detection in detection_result.detections:
                bestClassification = max(
                    detection.classes, key=lambda x: x.score)
                results.append({
                    "boundingBox": [
                        detection.bounding_box.origin_x,
                        detection.bounding_box.origin_y,
                        detection.bounding_box.origin_x + detection.bounding_box.width,
                        detection.bounding_box.origin_y + detection.bounding_box.height,
                    ],
                    "classification": bestClassification.class_name,
                    "confidence": bestClassification.score
                })

        return results

    def get_benchmark_name(self):
        name = "TensorFlow Lite via tflite_support"
        if self.args.enable_coral:
            name += " w/Coral TPU"
        return name

    def get_model_name(self):
        return self.args.model or ("ssd_mobilenet_v1_coco_quant_postprocess_edgetpu.tflite" if self.args.enable_coral else "ssd_mobilenet_v1_coco_quant_postprocess.tflite")


if __name__ == "__main__":
    args = parse_cmd_line()
    benchmark = TfliteCameraBenchmark(args)
    results = benchmark.run_benchmark()
    print("Benchmark complete")
    print(results)
