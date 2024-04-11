#include <Wire.h>
#include "SparkFun_BMI270_Arduino_Library.h"

// Create a new sensor object
BMI270 imu;
BMI270 imu2;
BMI270 imu3;

// I2C address selection
uint8_t i2cAddress = BMI2_I2C_PRIM_ADDR;  // 0x68
uint8_t i2cAddress2 = BMI2_I2C_SEC_ADDR;  // 0x69

int interruptPin = 4;

// Flag to know when interrupts occur
volatile bool interruptOccurred = false;
int buttonState = 0;


void setup() {
  // Start serial
  Serial.begin(115200);
  Serial.println("BMI270 Example 1 - Basic Readings I2C");

  // Initialize the I2C library
  Wire.begin(12, 13);
  Wire.begin(11, 14);

  pinMode(interruptPin,INPUT);

  while (imu.beginI2C(i2cAddress) != BMI2_OK) {
    Serial.println(imu.beginI2C(i2cAddress));
    // Not connected, inform user
    Serial.println("Error: BMI270 not connected, check wiring and I2C address!");

    // Wait a bit to see if connection is established
    delay(1000);
  }
  Serial.println("BMI270 connected!");

  while (imu2.beginI2C(i2cAddress2) != BMI2_OK) {
    Serial.println(imu2.beginI2C(i2cAddress2));
    // Not connected, inform user
    Serial.println("Error: BMI270 not connected, check wiring and I2C address!");

    // Wait a bit to see if connection is established
    delay(1000);
  }
  Serial.println("BMI270 connected!");

  while (imu3.beginI2C(i2cAddress) != BMI2_OK) {
    Serial.println(imu3.beginI2C(i2cAddress));
    // Not connected, inform user
    Serial.println("Error: BMI270 not connected, check wiring and I2C address!");

    // Wait a bit to see if connection is established
    delay(1000);
  }
  Serial.println("BMI270 connected!");

  // Check if sensor is connected and initialize
  // Address is optional (defaults to 0x68)
}

void loop() {
  // Get measurements from the sensor. This must be called before accessing
  // the sensor data, otherwise it will never update

  buttonState = digitalRead(interruptPin);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
    // turn LED on:
    interruptOccurred = false;
  } else {
    // turn LED off:
    interruptOccurred = true;
  }

  if (interruptOccurred) {
    // Reset flag for next interrupt
    interruptOccurred = false;

    imu.getSensorData();
    Serial.print("IMU number: ");
    Serial.print(1);
    // Print acceleration data
    Serial.print(" Acceleration in g's");
    Serial.print("\t");
    Serial.print("X: ");
    Serial.print(imu.data.accelX, 3);
    Serial.print("\t");
    Serial.print("Y: ");
    Serial.print(imu.data.accelY, 3);
    Serial.print("\t");
    Serial.print("Z: ");
    Serial.print(imu.data.accelZ, 3);

    Serial.print("\t");

    // Print rotation data
    Serial.print("Rotation in deg/sec");
    Serial.print("\t");
    Serial.print("X: ");
    Serial.print(imu.data.gyroX, 3);
    Serial.print("\t");
    Serial.print("Y: ");
    Serial.print(imu.data.gyroY, 3);
    Serial.print("\t");
    Serial.print("Z: ");
    Serial.println(imu.data.gyroZ, 3);

    // Print 50x per second
    delay(20);

    imu2.getSensorData();
    Serial.print("IMU number: ");
    Serial.print(2);
    // Print acceleration data
    Serial.print(" Acceleration in g's");
    Serial.print("\t");
    Serial.print("X_1: ");
    Serial.print(imu2.data.accelX, 3);
    Serial.print("\t");
    Serial.print("Y_1: ");
    Serial.print(imu2.data.accelY, 3);
    Serial.print("\t");
    Serial.print("Z_1: ");
    Serial.print(imu2.data.accelZ, 3);

    Serial.print("\t");

    // Print rotation data
    Serial.print("Rotation in deg/sec");
    Serial.print("\t");
    Serial.print("X_2: ");
    Serial.print(imu2.data.gyroX, 3);
    Serial.print("\t");
    Serial.print("Y_2: ");
    Serial.print(imu2.data.gyroY, 3);
    Serial.print("\t");
    Serial.print("Z_2: ");
    Serial.println(imu2.data.gyroZ, 3);

    // Print 50x per second
    delay(20);

    imu3.getSensorData();
    Serial.print("IMU number: ");
    Serial.print(3);
    // Print acceleration data
    Serial.print(" Acceleration in g's");
    Serial.print("\t");
    Serial.print("X_1: ");
    Serial.print(imu3.data.accelX, 3);
    Serial.print("\t");
    Serial.print("Y_1: ");
    Serial.print(imu3.data.accelY, 3);
    Serial.print("\t");
    Serial.print("Z_1: ");
    Serial.print(imu3.data.accelZ, 3);

    Serial.print("\t");

    // Print rotation data
    Serial.print("Rotation in deg/sec");
    Serial.print("\t");
    Serial.print("X_2: ");
    Serial.print(imu3.data.gyroX, 3);
    Serial.print("\t");
    Serial.print("Y_2: ");
    Serial.print(imu3.data.gyroY, 3);
    Serial.print("\t");
    Serial.print("Z_2: ");
    Serial.println(imu3.data.gyroZ, 3);

    // Print 50x per second
    delay(20);
  }
}