#!/usr/bin/env python3

import torchvision.transforms as T
import torchvision
import torch

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


def load_torchvision_model(model_name):
    # how to dynamically specify the model name as a string eludes me
    if model_name == "fasterrcnn_resnet50_fpn":
        print(f"INFO: using model: {model_name}")
        return torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=torchvision.models.detection.FasterRCNN_ResNet50_FPN_Weights.COCO_V1)
    if model_name == "fasterrcnn_resnet50_fpn_v2":
        print(f"INFO: using model: {model_name}")
        return torchvision.models.detection .fasterrcnn_resnet50_fpn_v2(weights=torchvision.models.detection.FasterRCNN_ResNet50_FPN_V2_Weights.COCO_V1)
    if model_name == "maskrcnn_resnet50_fpn":
        print(f"INFO: using model: {model_name}")
        return torchvision.models.detection.maskrcnn_resnet50_fpn(weights=torchvision.models.detection.MaskRCNN_ResNet50_FPN_Weights.COCO_V1)
    if model_name == "maskrcnn_resnet50_fpn_v2":
        print(f"INFO: using model: {model_name}")
        return torchvision.models.detection.maskrcnn_resnet50_fpn_v2(weights=torchvision.models.detection.MaskRCNN_ResNet50_FPN_V2_Weights.COCO_V1)

    # default model is the fastest I could find in TorchVision
    print("INFO: using default model: fasterrcnn_mobilenet_v3_large_320_fpn")
    return torchvision.models.detection.fasterrcnn_mobilenet_v3_large_320_fpn(weights=torchvision.models.detection.FasterRCNN_MobileNet_V3_Large_320_FPN_Weights.COCO_V1)

    return null


class PytorchCameraBenchmark(CameraBenchmark):

    def __init__(self, args):
        self.model = load_torchvision_model(args.model)
        self.model.eval()
        self.transform = T.Compose([T.ToTensor()])
        torch.set_num_threads(args.num_threads)

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
        return "PyTorch via torchvision"

    def get_model_name(self):
        return "fasterrcnn_mobilenet_v3_large_320_fpn"


if __name__ == "__main__":
    args = parse_cmd_line()
    benchmark = PytorchCameraBenchmark(args)
    results = benchmark.run_benchmark()
    print("Benchmark complete")
    print(results)
