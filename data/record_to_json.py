import time
import json
import sys
import serial
import numpy as np

data = []

communication_port = 'COM4'
baudRate = 921600
saved_data_name = 'imu_data_collection.csv'

# Open serial port for receiving data from Arduino
ser = serial.Serial(communication_port, baudRate, timeout=1)


def AsciiDecoder(b) -> str:
    """
    Decode key presses from the waitKey function in OpenCV.

    Parameters
    ----------
    b : int
        The keypress code received from the waitKey function.

    Returns
    -------
    str
        Returns the decoded character corresponding to the keypress.
        If the keypress code is '-1', returns "".
    """
    if b == '-1':
        return ""
    # bitmasks the last byte of b and returns decoded character
    return chr(b & 0xFF)


def exit_if_pressed(exit_key):
    if 'q' == AsciiDecoder(exit_key):
        with open("digits.json", "w") as json_file:
            json.dump(data, json_file)
        sys.exit()


def get_label(label_key, assigned_label):
    value = AsciiDecoder(label_key)
    if value == '0':
        return 'open_3_hand'
    elif value == '1':
        return 'open_2_hand'
    elif value == '2':
        return 'pinch_2_hand'
    elif value == '3':
        return 'pinch_3_hand'
    elif value == '4':
        return 'fist'
    elif value == '6':
        return 'point'


while True:
    dic = dict()

    sensor_data = ser.readline().decode().strip()