#include "ACCSensor.cpp"
#include "AirSensor.cpp"
#include "Sound.cpp"
#include "Wifi.cpp"

/*loop COUNT*/
int count = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    delay(10);  // will pause Zero, Leonardo, etc until serial console opens
  }
  /*PING SET*/
  acceleration_setup();
  air_setup();
}

void loop() {
  acceleration_loop(count);
  air_loop();
  sound_loop();
  delay(1000);
  count++;
}
