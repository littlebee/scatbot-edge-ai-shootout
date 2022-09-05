#!/usr/bin/env python3

import torchvision.transforms as T
import torchvision

from lib.camera_benchmark import CameraBenchmark
from lib.benchmark_args import parse_cmd_line


# Class labels from official PyTorch documentation for the pretrained model
# Note that there are some N/A's for complete list check out
# https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]


class PytorchCameraBenchmark(CameraBenchmark):

    def __init__(self, args):
        self.model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_320_fpn(
            pretrained=True)
        self.model.eval()
        self.transform = T.Compose([T.ToTensor()])

        super(PytorchCameraBenchmark, self).__init__(args)

    def get_prediction(self, img):
        img = self.transform(img)
        pred = self.model([img])
        pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i]
                      for i in list(pred[0]['labels'].numpy())]
        pred_boxes = [[(i[0], i[1]), (i[2], i[3])]
                      for i in list(pred[0]['boxes'].detach().numpy())]
        pred_scores = list(pred[0]['scores'].detach().numpy())
        results = []

        indexes = range(len(pred_scores))
        for i in indexes:
            score = float(pred_scores[i])
            if score > 0.5:
                results.append({
                    "bounding_box": [
                        int(pred_boxes[i][0][0]),
                        int(pred_boxes[i][0][1]),
                        int(pred_boxes[i][1][0]),
                        int(pred_boxes[i][1][1]),
                    ],
                    "classification": pred_class[i],
                    "confidence": score
                })

        return results

    def get_benchmark_name(self):
        # TODO - remove the model name when I figure out how to dynamically accept this from cl arg
        return "pytorch (fasterrcnn_mobilenet_v3_large_320_fpn)"


if __name__ == "__main__":
    args = parse_cmd_line()
    benchmark = PytorchCameraBenchmark(args)
    results = benchmark.run_benchmark()
    print("Benchmark complete")
    print(results)
