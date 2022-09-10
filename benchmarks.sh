#!/bin/bash


BENCHMARK_RUNS=10
BENCHMARK_CPU_AVAIL=(100 75 50 25)

BENCHMARK_COMMANDS=(
  # pytorch via torchvision w/torchvision.models.detection.fasterrcnn_mobilenet_v3_large_320_fpn
  "./benchmark-pytorch.py"
  # # pytorch via torchhub with yolov5 model
  "./benchmark-yolov5.py"
  # TensorFlow lite with models from the official tflite Raspberry pi example
  # (https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi)
  "./benchmark-tflite.py --model data/tflite/efficientdet_lite0.tflite"
  "./benchmark-tflite.py --model data/tflite/efficientdet_lite0_edgetpu.tflite --enable_coral"
  # TensorFlow lite with ssd_mobilenet_v1_coco_quant_postprocess.tflite
  "./benchmark-tflite.py"
  "./benchmark-tflite.py --enable_coral"
)

busy_work_pids=()

runAndRest () {
  cmd=$@

  echo "running '$cmd'"
  eval $cmd
  echo "resting"
  echo ""
  echo ""
  sleep 20
}

for cpu_avail in ${BENCHMARK_CPU_AVAIL[@]}; do
  # create csv file for results
  results_file="results-${cpu_avail}.csv"
  python3 lib/csv_file.py $results_file
  echo "created results file: $results_file"

  # run the iterations of benchmarks number of runs
  for i in $(seq 1 $BENCHMARK_RUNS); do
    echo ""
    echo "starting run $i with $cpu_avail% overall cpu"
    echo ""

    for benchmark_command in "${BENCHMARK_COMMANDS[@]}"; do
      runAndRest "$benchmark_command --csv_file $results_file" $@
    done
  done

  echo "increasing cpu load by 1 core (25% on 4 core cpu)"
  ./busy_work.py > /dev/null &
  busy_work_pids+=($!)
done

echo "Killing busy work processes"
for pid in ${busy_work_pids[@]}; do
  kill -9 $pid
done