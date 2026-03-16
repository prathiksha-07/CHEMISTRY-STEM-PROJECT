#include <OneWire.h>
#include <DallasTemperature.h>

#define PH_PIN 1
#define TURB_PIN 2
#define TDS_PIN 3
#define ONE_WIRE_BUS 4

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

float averageAnalog(int pin) {
  long sum = 0;
  for (int i = 0; i < 20; i++) {
    sum += analogRead(pin);
    delay(10);
  }
  return sum / 20.0;
}

void setup() {
  Serial.begin(115200);
  sensors.begin();
}

void loop() {

  float phRaw = averageAnalog(PH_PIN);
  float turbRaw = averageAnalog(TURB_PIN);
  float tdsRaw = averageAnalog(TDS_PIN);

  sensors.requestTemperatures();
  float temperature = sensors.getTempCByIndex(0);

  float voltagePH = phRaw * (3.3 / 4095.0);
  float pH = 7 + ((2.5 - voltagePH) / 0.18);

  float turbidity = turbRaw;
  float tds = (tdsRaw * 3.3 / 4095.0) * 500;

  // Send JSON format to Python
  Serial.print("{");
  Serial.print("\"ph\":"); Serial.print(pH,2); Serial.print(",");
  Serial.print("\"turbidity\":"); Serial.print(turbidity,2); Serial.print(",");
  Serial.print("\"tds\":"); Serial.print(tds,2); Serial.print(",");
  Serial.print("\"temperature\":"); Serial.print(temperature,2);
  Serial.println("}");

  delay(3000);
}