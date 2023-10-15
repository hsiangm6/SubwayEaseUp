#include <MQ135.h>
#include <HardwareSerial.h>

/*PING DEFINE*/
#define ANALOGPIN A0  // 空氣船趕氣腳位
/*PING DEFINE _END*/

static MQ135 gasSensor = MQ135(ANALOGPIN);  // AIR SENSOR PING

static void air_setup() {
    float rzero = gasSensor.getRZero();
    delay(3000);
    Serial.print("[INFO] MQ135 initialized. RZERO Calibration Value : ");
    Serial.println(rzero);
}

static float air_loop() {
    Serial.print("\tCO2 ppm value: ");
    float ppm = gasSensor.getPPM();
    Serial.print(ppm);
    return ppm;
}
