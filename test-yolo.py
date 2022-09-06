#!/usr/bin/env python3
import os
from pathlib import Path


from yolov5.models.common import DetectMultiBackend
from yolov5.utils.dataloaders import LoadStreams
from yolov5.utils.general import (LOGGER, check_img_size, check_requirements,
                                  non_max_suppression, scale_coords)
from yolov5.utils.plots import Annotator, colors, save_one_box
from yolov5.utils.torch_utils import select_device, time_sync

import torch
import torch.backends.cudnn as cudnn

YOLO_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), './yolov5'))

WEIGHTS_FILE = YOLO_ROOT + '/yolov5s.pt'
DATA_FILE = YOLO_ROOT + '/data/coco128.yaml'


@torch.no_grad()
def run(
        imgsz=(240, 320),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        line_thickness=3,  # bounding box thickness (pixels)
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
):

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(
        WEIGHTS_FILE, device=device, dnn=dnn, data=DATA_FILE, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader
    cudnn.benchmark = True  # set True to speed up constant image size inference
    dataset = LoadStreams(str(0),
                          img_size=imgsz, stride=stride, auto=pt)
    bs = len(dataset)  # batch_size

    # Run inference
    model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], [0.0, 0.0, 0.0]
    for path, im, im0s, vid_cap, s in dataset:
        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        pred = model(im, augment=augment, visualize=visualize)
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        # pred = non_max_suppression(
        #     pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        # dt[2] += time_sync() - t3

        print(pred)

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        # for i, det in enumerate(pred):  # per image
        #     seen += 1
        #     p, im0, frame = path[i], im0s[i].copy(), dataset.count
        #     s += f'{i}: '

        #     p = Path(p)  # to Path
        #     s += '%gx%g ' % im.shape[2:]  # print string

        #     # annotator = Annotator(
        #     #     im0, line_width=line_thickness, example=str(names))
        #     if len(det):
        #         # Rescale boxes from img_size to im0 size
        #         det[:, :4] = scale_coords(
        #             im.shape[2:], det[:, :4], im0.shape).round()

        #         # Print results
        #         for c in det[:, -1].unique():
        #             n = (det[:, -1] == c).sum()  # detections per class
        #             # add to string
        #             s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "

        # Save results (image with detections)
        # Print time (inference-only)
        LOGGER.info(f'{s}Done. ({t3 - t2:.3f}s)')

    # Print results
    t = tuple(x / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(
        f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)


if __name__ == "__main__":
    check_requirements(exclude=('tensorboard', 'thop'))
    run()
