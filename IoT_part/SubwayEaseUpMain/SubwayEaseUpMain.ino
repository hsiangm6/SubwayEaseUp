#include "ACCSensor.cpp"
#include "AirSensor.cpp"
#include "Sound.cpp"
#include "Wifi.cpp"

/*loop COUNT*/
int count = 0;

/*value*/
int sound;
float ppm;
float acc[3];
String ppm_s, sound_s, accx_s, accy_s, accz_s;




void setup() {

  wifiSetUp("OPPO A9 2020", "c8d4c408aaff");

  Serial.begin(9600);
  while (!Serial) {
    delay(10);  // will pause Zero, Leonardo, etc until serial console opens
  }
  /*PING SET*/
  acceleration_setup();
  air_setup();
}

void loop() {
  acceleration_loop(count, acc);
  ppm = air_loop();
  sound = sound_loop();
  delay(1000);
  count++;
  /*to string*/
  ppm_s = String(ppm);
  sound_s = String(sound);
  accx_s=String(acc[0]);
  accy_s=String(acc[1]);
  accz_s=String(acc[2]);

  sendToServer(
    "",
    "",
    "/transfer_data?ppm=" + ppm_s + "&sound=" + sound_s + "&accX=" + accx_s + "&accY=" + accy_s + "&accZ=" + accz_s,
    true);
}
