import argparse


def parse_cmd_line():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--camera_channel',
        help='Id of camera device to use.',
        required=False,
        type=int,
        default=0
    )
    parser.add_argument(
        '--csv_file',
        help='file and path to append csv result data',
        required=False,
        default=None
    )
    parser.add_argument(
        '--duration',
        help='Length of time in seconds to run benchmark.',
        required=False,
        type=int,
        default=30
    )
    parser.add_argument(
        '--enable_coral',
        help='Whether to run the model on Coral Edge TPU.  (tflite only)',
        required=False,
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--frame_height',
        help='Height of frame to capture from camera.',
        required=False,
        type=int,
        default=480
    )
    parser.add_argument(
        '--frame_width',
        help='Width of frame to capture from camera.',
        required=False,
        type=int,
        default=640
    )
    parser.add_argument(
        '--model',
        help='Path of the object detection model. (tflite only)',
        required=False,
        default=None
    )
    parser.add_argument(
        '--num_threads',
        help='Number of CPU threads to run the model.',
        required=False,
        type=int,
        default=4
    )
    parser.add_argument(
        '--verbose',
        help='Show detections and debugging info',
        required=False,
        default=False,
        action='store_true'
    )

    return parser.parse_args()
