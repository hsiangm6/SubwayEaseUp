// nRF24L01_Sender.ino
// 參考 http://pizgchen.blogspot.com/2020/01/nrf24l01-1100.html
#include <SPI.h>
#include "RF24.h"
#include "nRF24L01.h"

RF24 radio(9, 8);  // 指定 Arduino Nano 腳位對應 nRF24L01 之 (CE, CSN)
const byte address[6] = "00001";  // 節點位址為 5 bytes + \0=6 bytes

int counter = 0;  // Hello 計數器

void setup() {
    Serial.begin(9600);
    radio.begin();                   // 初始化 nRF24L01 模組
    radio.setDataRate(RF24_2MBPS);   // 開啟 2 MBPS 速度
    radio.openWritingPipe(address);  // 開啟寫入管線
    radio.setPALevel(RF24_PA_MIN);   // 設為低功率, 預設為 RF24_PA_MAX
    radio.stopListening();           // 傳送端不需接收, 停止傾聽
}

void loop() {
    const char text[32];  // 宣告用來儲存欲傳送之字串
    sprintf(text, "Hello World %d", counter);  // 將整數嵌入字串中
    Serial.println(text);
    radio.write(&text, sizeof(text));  // 將字串寫入傳送緩衝器
    ++counter;
    // delay(1000);
}