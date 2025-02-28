#!/usr/bin/env python3
import logging
from ina226 import INA226
from time import sleep

v_measured = 0.0
i_measured = 0.0
r_load_ohm = 1.8
i_fan_a = 0.250


def read():
    print("Bus Voltage    : %.3f V" % ina.voltage())
    print("Bus Current    : %.3f mA" % ina.current())
    print("Supply Voltage : %.3f V" % ina.supply_voltage())
    print("Shunt voltage  : %.3f mV" % ina.shunt_voltage())
    print("Power          : %.3f mW" % ina.power())


if __name__ == "__main__":
    # ina = INA226(busnum=1, max_expected_amps=25, log_level=logging.DEBUG)
    ina = INA226(busnum=1, max_expected_amps=0.1, shunt_ohms=0.1, log_level=logging.WARNING)
    ina.configure()
    ina.set_low_battery(5)

    itt = 0
    while itt < 5:
        itt = itt+1
        sleep(0.25)
        print(itt, "===================================================Begin to read")
        read()
        sleep(1)