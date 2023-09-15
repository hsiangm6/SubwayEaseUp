#include <SoftwareSerial.h>
#include "WiFiEsp.h"

SoftwareSerial ESP8266(11, 12);  // Arduino 的 RX, TX

unsigned long realtime = 0;
bool FAIL_8266 = false;

// 下方參考
// http://andrewpythonarduino.blogspot.com/2018/05/python27esp8266-and-iot.html
void setup() {
    wifiSetUp("", "");
}

void loop() {
    if ((millis() - realtime) >= 10000)  // 10秒 Update 一次
    {
        realtime = millis();
        if (!FAIL_8266) {
            sendToServer("", "", "/test?test=test", true);
        }
    }
}

void wifiSetUp(String wifi_name, String password) {
    Serial.begin(9600);
    ESP8266.begin(9600);

    // 重複直到連接上 Wifi
    do {
        sendESP8266cmd("AT+RST", 2000);
        Serial.println("[INFO] Reset ESP8266...");
        // 重設
        if (!ESP8266.find("OK")) {
            // 連接 ESP8266 失敗
            delay(500);
            FAIL_8266 = true;
            Serial.println("[ERROR] ESP8266 No Response");
            continue;
        }

        Serial.println("> OK");

        // 連線AP
        if (!connectWiFi(wifi_name, password, 10)) {
            // 連接 Wifi 失敗
            FAIL_8266 = true;
            Serial.println("[ERROR] Connect Fail");
            continue;
        }

        // 連接 Wifi 成功
        FAIL_8266 = false;
        Serial.println("[INFO] Connect Success");
    } while (FAIL_8266);
}

// 連線到 WiFi
boolean connectWiFi(String wifi_name, String password, int timeout) {
    // 設置成 station MODE
    sendESP8266cmd("AT+CWMODE=1", 2000);
    Serial.println("[INFO] WiFi Mode:STA");

    // 重複重連直到 timeout 次數
    do {
        String cmd = "AT+CWJAP=\"" + wifi_name + "\",\"" + password + "\"";

        sendESP8266cmd(cmd, 1000);
        Serial.println("[INFO] Join AP...");

        if (ESP8266.find("OK")) {
            Serial.println("> OK");
            sendESP8266cmd("AT+CIPMUX=0", 1000);
            return true;
        }
    } while ((timeout--) > 0);
    return false;
}

// 發送到伺服器
void sendToServer(String ip, String port, String msg, short use_get) {
    // 連線伺服器指令
    String cmd = "AT+CIPSTART=\"TCP\",\"" + ip + "\"," + port;
    sendESP8266cmd(cmd, 2000);

    // 檢查是否連線成功
    if (!ESP8266.find("OK")) {
        // TCP 失敗
        Serial.println("[ERROR] TCP Error");
        sendESP8266cmd("AT+CIPCLOSE", 1000);
        return;
    }

    // TCP 成功
    Serial.println("[INFO] TCP OK");

    if (use_get)
        // 發送 Request (GET)
        cmd = "GET " + msg;
    else
        cmd = "POST " + msg;

    ESP8266.print("AT+CIPSEND=");
    ESP8266.println(cmd.length());

    if (!ESP8266.find(">")) return;

    // 把命令顯示出來
    ESP8266.print(cmd);
    Serial.println("> " + cmd);

    // 檢查是否成功執行 Request
    if (ESP8266.find("OK")) {
        Serial.println("[INFO] Update OK");
    } else {
        Serial.println("[ERROR] Update Error");
    }

}

// 發送命令給 ESP8266 並顯示在 Serial
void sendESP8266cmd(String cmd, int waitTime) {
    Serial.println("> " + cmd);
    ESP8266.println(cmd);
    delay(waitTime);
}