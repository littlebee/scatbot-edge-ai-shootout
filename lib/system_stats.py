import os
import psutil


def get_cpu_temp():
    cpu_temp = 0
    if os.path.exists('/sys/devices/virtual/thermal'):
        (cpu_temp, *rest) = [
            int(i) / 1000 for i in
            os.popen(
                'cat /sys/devices/virtual/thermal/thermal_zone*/temp').read().split()
        ]

    return cpu_temp


def get_cpu_available():
    return 100 - psutil.cpu_percent()
