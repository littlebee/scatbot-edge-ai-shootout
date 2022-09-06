#!/usr/bin/env python3
import os

from lib.benchmark_args import parse_cmd_line
from lib.camera_benchmark import CameraBenchmark

import torch


class Yolov5CameraBenchmark(CameraBenchmark):

    def __init__(self, args):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        super(Yolov5CameraBenchmark, self).__init__(args)

    def get_prediction(self, img):
        results = []
        detections = self.model(img)

        for i, (detections.im, detections.pred) in enumerate(zip(detections.ims, detections.pred)):
            if detections.pred.shape[0]:
                for c in detections.pred[:, -1].unique():
                    # xyxy, confidence, class
                    for *box, conf, cls in reversed(detections.pred):
                        if conf < 0.5:
                            continue

                        label = f'{detections.names[int(cls)]} {conf:.2f}'
                        results.append({
                            'boundingBox': [box[0].item(), box[1].item(), box[2].item(), box[3].item()],
                            'classification': label,
                            'confidence': conf,
                        })
        return results

    def get_benchmark_name(self):
        # TODO - remove the model name when I figure out how to dynamically accept this from cl arg
        return "Yolo V5"


if __name__ == "__main__":
    args = parse_cmd_line()
    benchmark = Yolov5CameraBenchmark(args)
    results = benchmark.run_benchmark()
    print("Benchmark complete")
    print(results)
