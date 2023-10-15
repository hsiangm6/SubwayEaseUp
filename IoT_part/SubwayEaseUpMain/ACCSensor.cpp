#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <HardwareSerial.h>

/*PING DEFINE*/
static Adafruit_MPU6050 mpu;  //acceleration define
/*PING DEFINE _END*/

static float prex = 0, prey = 0, prez = 0, acc_sum = 0;
static int status;// 0->heading toward next station, 1->close to next station, 2-> between two station

static void acceleration_setup() {
    if (!mpu.begin()) {
        Serial.println("[ERROR] Failed to find MPU6050 chip");
        while (1) {
            delay(10);
        }
    }
    mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
    mpu.setGyroRange(MPU6050_RANGE_250_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
    Serial.println("[INFO] MPU6050 initialized.");
}

static float acceleration_loop(int count) {
    /* Get new sensor events with the readings */
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    if (count == 0) {
        prex = a.acceleration.x;
        prey = a.acceleration.y;
        prez = a.acceleration.z;

        /* Print out the accelerometer and gyro values */
        Serial.print("Accelerometer (m/s^2): ");
        Serial.print(0);
        Serial.print(", ");
        Serial.print(0);
        Serial.print(", ");
        Serial.print(0);
    } else {
        /* Print out the accelerometer and gyro values */
        Serial.print("Accelerometer (m/s^2): ");
        Serial.print(a.acceleration.x - prex);
        Serial.print(", ");
        Serial.print(a.acceleration.y - prey);
        Serial.print(", ");
        Serial.print(a.acceleration.z - prez);

        acc_sum = abs(a.acceleration.x - prex) + abs(a.acceleration.y - prey) + abs(a.acceleration.z - prez);

        prex = a.acceleration.x;
        prey = a.acceleration.y;
        prez = a.acceleration.z;
    }
    if (acc_sum > 3) {
        digitalWrite(8, HIGH);
        status = ~status;
    } else {
        digitalWrite(8, LOW);
        status = 2;
    }

    return status;
}
