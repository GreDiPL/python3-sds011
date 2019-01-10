#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" SDS011 POC in python3 """

import sds011
import time
import sys
import signal

__author__ = "Grzegorz Deneka"
__license__ = "GPL3"
__status__ = "PoC"
__version__ = "0.01"

serial_device = "/dev/ttyUSB0"  # REQ Read and Write access
sleep_time = 300  # 5 min
sleep_warm_up = 30

if __name__ == "__main__":
    try:
        sensor = sds011.SDS011(serial_device, use_query_mode=True)
    except OSError as e:
        print(e.strerror)
        sys.exit(1)

    def signal_heandler(signum, frame):
        sensor.sleep()
        print("Sensor Off. Good Bye! ", signum)
        sys.exit(signum)

    signal.signal(signal.SIGINT, signal_heandler)
    signal.signal(signal.SIGTERM, signal_heandler)

    print("(pm2.5, pm10)")

    while True:
        print("Warming up sensor! StandBy for " + str(sleep_warm_up) + "secs")
        sensor.sleep(sleep=False)
        time.sleep(sleep_warm_up)
        for i in range(0, 5):
            print(sensor.query())
            time.sleep(1)

        print("Sleeping for next reading. " + str(sleep_time) + "sec")
        sensor.sleep()
        time.sleep(sleep_time)
