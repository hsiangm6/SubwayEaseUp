#include "ACCSensor.cpp"
#include "AirSensor.cpp"
#include "Sound.cpp"
#include "Wifi.cpp"

/*loop COUNT*/
int count = 0;

/*value*/
int sound;
float ppm;
float acc_all;
String ppm_s, sound_s, acc_all_s;

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
    acc_all = acceleration_loop(count);
    ppm = air_loop();
    sound = sound_loop();
    // delay(1000);
    count++;
    /*to string*/
    ppm_s = String(ppm);
    sound_s = String(sound);
    acc_all_s = String(acc_all);

    Serial.println(acc_all_s);


    sendToServer(
            "",
            "",
            "/transfer_data?ppm=" + ppm_s + "&sound=" + sound_s + "&acc=" + acc_all_s,
            true);

}
