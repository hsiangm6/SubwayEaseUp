#include <SoftwareSerial.h>
#include "WiFiEsp.h"

#define LED 13
SoftwareSerial ESP8266(6, 7);  // Arduino 的 RX, TX

String ssid = "";  // Wifi 名稱
String pwd = "";   // Wifi 密碼
String ip = "";    // 連接伺服器地址
String port = "";  // 連接伺服器端口

unsigned long realtime = 0;
bool FAIL_8266 = false;

// 下方參考
// http://andrewpythonarduino.blogspot.com/2018/05/python27esp8266-and-iot.html
void setup() {
    pinMode(LED, OUTPUT);
    digitalWrite(LED, LOW);
    Serial.begin(9600);
    ESP8266.begin(9600);

    // 閃爍三次，嘗試連接開始
    for (int i = 0; i < 3; i++) {
        digitalWrite(LED, HIGH);
        delay(200);
        digitalWrite(LED, LOW);
        delay(200);
    }

    // 重複直到連接上 Wifi
    do {
        sendESP8266cmd("AT+RST", 2000);
        Serial.println("reset 8266...");
        if (ESP8266.find("OK")) {
            Serial.println("OK");

            // 連線AP
            if (connectWiFi(10)) {
                // 連接 Wifi 成功
                FAIL_8266 = false;
                Serial.println("connect success");
            } else {
                // 連接 Wifi 失敗
                FAIL_8266 = true;
                Serial.println("connect fail");
            }
        } else {
            // 連接 ESP8266 失敗
            delay(500);
            FAIL_8266 = true;
            Serial.println("no response");
        }
    } while (FAIL_8266);

    // 常亮顯示正常連接
    digitalWrite(LED, HIGH);
}

void loop() {
    if ((millis() - realtime) >= 10000)  // 10秒 Update 一次
    {
        realtime = millis();
        if (!FAIL_8266) {
            sendToServer("Test%20message:%20" + String(realtime));
        }
    }
}

// 發送到伺服器
void sendToServer(String msg) {
    // 連線伺服器指令
    String cmd = "AT+CIPSTART=\"TCP\",\"" + ip + "\"," + port;
    sendESP8266cmd(cmd, 2000);

    // 檢查是否連線成功
    if (ESP8266.find("OK")) {
        // TCP 成功
        Serial.println("TCP OK");

        // 發送 Request (GET)
        cmd = "GET /test?test=" + msg;

        ESP8266.print("AT+CIPSEND=");
        ESP8266.println(cmd.length());

        if (ESP8266.find(">")) {
            // 把命令顯示出來
            ESP8266.print(cmd);
            Serial.println(cmd);

            // 檢查是否成功執行 Request
            if (ESP8266.find("OK")) {
                Serial.println("update OK");
            } else {
                Serial.println("update error");
            }
        }
    } else {
        // TCP 失敗
        Serial.println("TCP error");
        sendESP8266cmd("AT+CIPCLOSE", 1000);
    }
}

// 連線到 WiFi
boolean connectWiFi(int timeout) {
    // 設置成 station MODE
    sendESP8266cmd("AT+CWMODE=1", 2000);
    Serial.println("WiFi mode:STA");

    // 重複重連直到 timeout 次數
    do {
        String cmd = "AT+CWJAP=\"";
        cmd += ssid;
        cmd += "\",\"";
        cmd += pwd;
        cmd += "\"";
        sendESP8266cmd(cmd, 1000);
        Serial.println("join AP...");
        if (ESP8266.find("OK")) {
            Serial.println("OK");
            sendESP8266cmd("AT+CIPMUX=0", 1000);
            return true;
        }
    } while ((timeout--) > 0);
    return false;
}

// 發送命令給 ESP8266 並顯示在 Serial
void sendESP8266cmd(String cmd, int waitTime) {
    Serial.println(cmd);
    ESP8266.println(cmd);
    delay(waitTime);
}