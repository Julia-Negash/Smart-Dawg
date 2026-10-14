#include <WiFi.h>

// WiFi name and password live in secrets.h
#include "secrets.h"
const char* ssid     = WIFI_SSID;
const char* password = WIFI_PASSWORD;
void setup() {
  // Initialize serial communication at 115200 baud rate
  Serial.begin(115200);
  delay(1000); 

  // Connect to the Wi-Fi network
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  // Wait until the ESP32 successfully connects
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Wi-Fi connected.");

  // 1. Retrieve and print the Local IP Address
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // 2. Retrieve and print the hardware MAC Address
  Serial.print("ESP32 MAC Address: ");
  Serial.println(WiFi.macAddress());
}

void loop() {
  // Your main code here
}
