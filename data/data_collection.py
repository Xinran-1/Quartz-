import serial
import csv
from datetime import datetime
import keyboard

# Open serial port for receiving data from Arduino
# ser = serial.Serial('COM6', 921600, timeout=1)
ser = serial.Serial('COM6', 921600, timeout=1)

# Create a CSV file
csv_file_path = 'data1.csv'

# Open file for data logging+
file = open(csv_file_path, "w", newline='')
csv_writer = csv.writer(file)

try:
    # Write CSV header with Timestamp, sensor data, label and sep columns
    csv_header = ["Timestamp", "mid_Acceleration_X", "mid_Acceleration_Y", "mid_Acceleration_Z",
                  "mid_Rotation_X", "mid_Rotation_Y", "mid_Rotation_Z",
                  "ind_Acceleration_X", "ind_Acceleration_Y", "ind_Acceleration_Z",
                  "ind_Rotation_X", "ind_Rotation_Y", "ind_Rotation_Z",
                  "thb_Acceleration_X", "thb_Acceleration_Y", "thb_Acceleration_Z",
                  "thb_Rotation_X", "thb_Rotation_Y", "thb_Rotation_Z",
                  "Label", "Sep"]
    csv_writer.writerow(csv_header)

    # Initialize label and previous sign
    labels = ["pinch2finger", "release2finger", "pinch3finger", "release3finger", "fists"]  # List of possible labels
    label_index = 0  # Index for cycling through labels
    current_label = labels[label_index]
    sep = False  # Initial sep value


    def clean_and_join_numbers(data_str):
        # 将字符串中的连字符 '-' 替换为空格，然后使用空格连接所有数字
        cleaned_numbers = ''.join(data_str.replace('-', ''))
        return cleaned_numbers

    while True:
        data_row = []
        # Read data from Arduino
        for _ in range(3):
            line = ser.readline().decode().strip()
            data = line.strip("'").split("\t\t")
            data = [clean_and_join_numbers(data_str) for data_str in data]
            print(len(data))
            if len(data) == 6:
                data_row.extend(data)
            print(data)

        if len(data_row) == 18:  # Ensure we have exactly 6 sensor values
            # Get current timestamp1
            current_timestamp = datetime.now().strftime('%H:%M:%S.%f')

            # Check keyboard input to set sep and current_label
            if keyboard.is_pressed('1'):
                current_label = labels[0]
                sep = True
            elif keyboard.is_pressed('2'):
                current_label = labels[1]
                sep = True
            elif keyboard.is_pressed('3'):
                current_label = labels[2]
                sep = True
            elif keyboard.is_pressed('4'):
                current_label = labels[3]
                sep = True
            elif keyboard.is_pressed('5'):
                current_label = labels[4]
                sep = True
            else:
                sep = False

            # Write data to CSV file along with label and sep
            # print(data_row)
            csv_writer.writerow([current_timestamp] + data_row + [current_label, sep])


except serial.SerialException as e:
    print(f"Serial communication error: {e}")

finally:
    # Close serial port
    ser.close()

    # Close file and save data to CSV
    file.close()
    print("Data saved to", csv_file_path)
