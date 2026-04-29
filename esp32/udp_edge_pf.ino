#include <WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <MPU6050.h>

const char* ssid = "OPPO";
const char* password = "12345678";
const char* host = "10.83.216.165";
const int port = 5000;

WiFiUDP udp;
MPU6050 imu;

#define N 200

float particles[N];
float weights[N];

float randn() {
  return random(-1000,1000)/1000.0;
}

void init_particles(){
  for(int i=0;i<N;i++){
    particles[i] = randn()*100;
    weights[i] = 1.0/N;
  }
}

float pf(float z){
  // Predict
  for(int i=0;i<N;i++){
    particles[i] += randn()*20;
  }

  // Update
  float sum_w=0;
  for(int i=0;i<N;i++){
    float diff = particles[i]-z;
    weights[i] = exp(-(diff*diff)/(2*5000));
    sum_w += weights[i];
  }

  if(sum_w < 1e-6){
    for(int i=0;i<N;i++) weights[i]=1.0/N;
    sum_w=1;
  }

  for(int i=0;i<N;i++) weights[i]/=sum_w;

  // Resample
  float newp[N];
  for(int i=0;i<N;i++){
    float r = random(0,1000)/1000.0;
    float cum=0;
    for(int j=0;j<N;j++){
      cum+=weights[j];
      if(r<=cum){
        newp[i]=particles[j];
        break;
      }
    }
  }

  for(int i=0;i<N;i++){
    particles[i]=newp[i];
    weights[i]=1.0/N;
  }

  float mean=0;
  for(int i=0;i<N;i++) mean+=particles[i];

  return mean/N;
}

void setup(){
  Serial.begin(115200);
  Wire.begin(21,22);
  imu.initialize();

  randomSeed(analogRead(0));
  init_particles();

  WiFi.begin(ssid,password);
  while(WiFi.status()!=WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
}

void loop(){
  int16_t ax,ay,az;
  imu.getAcceleration(&ax,&ay,&az);

  float f = pf(ax);

  if(isnan(f)||isinf(f)) f=0;

  // 🔥 kirim RAW + FILTERED
  String data = String(ax)+","+String(f);

  udp.beginPacket(host,port);
  udp.print(data);
  udp.endPacket();

  Serial.print("RAW=");
  Serial.print(ax);
  Serial.print(" FILT=");
  Serial.println(f);

  delay(200);
}