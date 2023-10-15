#include <Wire.h>
#include <Arduino.h>
#include <HardwareSerial.h>

/*PING DEFINE*/
#define SoundSensorPin A1    // SOUND SENSOR PING
static int sound_value = 0;  // sound define
/*PING DEFINE _END*/

static int sound_loop() {
    sound_value = analogRead(SoundSensorPin);  //set the value as the value read from A2
    Serial.print("\tSound: ");
    Serial.println(sound_value, DEC);  //print the value and line wrap
    return sound_value;
}