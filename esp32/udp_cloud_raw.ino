#include <WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <MPU6050.h>

const char* ssid = "OPPO";
const char* password = "12345678";

const char* host = "10.83.216.165"; // IP Raspberry
const int port = 5000;

WiFiUDP udp;
MPU6050 imu;

void setup() {
  Serial.begin(115200);

  Wire.begin(21, 22);
  imu.initialize();

  if (!imu.testConnection()) {
    Serial.println("MPU6050 ERROR");
    while (1);
  }

  Serial.println("MPU6050 OK");

  WiFi.begin(ssid, password);

  Serial.print("Connecting WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected");
}

void loop() {
  int16_t ax, ay, az;
  imu.getAcceleration(&ax, &ay, &az);

  // kirim RAW saja
  String data = String(ax);

  udp.beginPacket(host, port);
  udp.print(data);
  udp.endPacket();

  Serial.print("RAW SEND: ");
  Serial.println(ax);

  delay(200);
}