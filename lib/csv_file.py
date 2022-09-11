#!/usr/bin/env python3
import sys

CSV_DEFAULTS = {
    "name": "",
    "model": "",
    "num_threads": 0,
    "enable_coral": False,
    "frame_height": 0,
    "frame_width": 0,
    "duration": 0,
    "cpu_avail_start": 0,
    "max_cpu_temp": 0,
    "fps": 0,
}


def write_header(file_path):
    headers = list(CSV_DEFAULTS.keys())
    headerStr = ",".join(headers)

    f = open(file_path, "w")
    f.write(headerStr + "\n")
    f.close()


def append_results(file_path, results):
    keys = list(CSV_DEFAULTS.keys())
    values = []
    for key in keys:
        results_value = results.get(key)
        values.append(str(results_value or CSV_DEFAULTS[key]))

    valueStr = ",".join(values)

    f = open(file_path, "a")
    f.write(valueStr + "\n")
    f.close()


# benchmarks.sh calls us with a file name to create and add headers
if __name__ == "__main__":
    if len(sys.argv) > 1 and len(sys.argv[1]) > 0:
        write_header(sys.argv[1])
