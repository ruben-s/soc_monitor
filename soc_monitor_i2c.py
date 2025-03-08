#!/usr/bin/env python3
import logging
from ina226 import INA226
from time import sleep

R_LOAD_OHM = 1.53
total_agm_capacity_Ah = 85
file_name = "soc_monitor_agm.csv"
MEASURING_PERIOD_SEC = 300 # 5min

def calculate_current(given_voltage, load_resistance_ohm):
    calculated_current = given_voltage / load_resistance_ohm
    return calculated_current

def calculate_drained_capacity(period, current):
    capacity_mAperiod = (current/3600)*period
    return capacity_mAperiod

def calculate_remaining_capacity(total_capacity_Ah, drained_capacity_Ah):
    remaining_capacity_Ah = total_capacity_Ah - drained_capacity_Ah
    return remaining_capacity_Ah

def read_bus_voltage():
    return ina.voltage()

def read():
    print("Bus Voltage    : %.3f V" % ina.voltage())
    print("Bus Current    : %.3f mA" % ina.current())
    print("Supply Voltage : %.3f V" % ina.supply_voltage())
    print("Shunt voltage  : %.3f mV" % ina.shunt_voltage())
    print("Power          : %.3f mW" % ina.power())

def create_write_str(itteration,
                     elapsed_period_sec,
                     measured_voltage_V,
                     R_LOAD_OHM,
                     calculated_current_A,
                     total_drained_capacity_Ah,
                     calculated_remaining_capacity_Ah
                     ):
    str_to_write = f"{itteration}"
    str_to_write = str_to_write + f",{elapsed_period_sec}"
    str_to_write = str_to_write + f",{measured_voltage_V}"
    str_to_write = str_to_write + f",{R_LOAD_OHM}"
    str_to_write = str_to_write + f",{calculated_current_A}"
    str_to_write = str_to_write + f",{total_drained_capacity_Ah}"
    str_to_write = str_to_write + f",{calculated_remaining_capacity_Ah}"
    return str_to_write

if __name__ == "__main__":
    # ina = INA226(busnum=1, max_expected_amps=25, log_level=logging.DEBUG)
    ina = INA226(busnum=1, max_expected_amps=0.1, shunt_ohms=0.1, log_level=logging.WARNING)
    ina.configure()
    ina.set_low_battery(5)
    csv_file = open(file_name, "w")
    str_to_write = "Itteration, Elapsed_period_Sec, Measured_voltage_V, Load_Ohm, Calculated_current_A, Total_drained_capacity, Remaining_capacity"
    print(str_to_write)
    csv_file.write(str_to_write)

    itt = 0
    elapsed_period_sec = 0
    calculated_current_A = 0
    measured_voltage_V = 0
    total_drained_capacity_Ah = 0
    calculated_remaining_capacity_Ah = total_agm_capacity_Ah
    measured_voltage_V = read_bus_voltage()
    str_to_write = create_write_str(itt,
                                    elapsed_period_sec,
                                    measured_voltage_V,
                                    R_LOAD_OHM,
                                    calculated_current_A,
                                    total_drained_capacity_Ah,
                                    calculated_remaining_capacity_Ah
    )
    print(str_to_write)
    csv_file.write(str_to_write)
    while itt < 5:
        itt = itt+1
        sleep(0.25)
        print(f"itteration: {itt},======Begin to read")
        measured_voltage_V_begin = read_bus_voltage()
        sleep(MEASURING_PERIOD_SEC)
        measured_voltage_V_end = read_bus_voltage()
        measured_voltage_V_avg = (measured_voltage_V_begin + measured_voltage_V_end)/2
        calculated_current = calculate_current(
                                given_voltage=measured_voltage_V_avg,
                                load_resistance_ohm=R_LOAD_OHM
        )
        calculated_drained_capacity_period = calculate_drained_capacity(
                                period=MEASURING_PERIOD_SEC,
                                current=calculate_current
        )
        total_drained_capacity_Ah = total_drained_capacity_Ah + calculated_drained_capacity_period
        calculated_remaining_capacity_Ah = calculate_remaining_capacity(
                                total_capacity_Ah=total_agm_capacity_Ah,
                                drained_capacity_Ah=total_drained_capacity_Ah
        )
        str_to_write = create_write_str(itt,
                                        elapsed_period_sec,
                                        measured_voltage_V,
                                        R_LOAD_OHM,
                                        calculated_current_A,
                                        total_drained_capacity_Ah,
                                        calculated_remaining_capacity_Ah
        )
        print(str_to_write)
        csv_file.write(str_to_write)

csv_file.close()
