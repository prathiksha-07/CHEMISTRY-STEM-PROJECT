
float voltage;
float phValue;
float tempC;
// float voltage;
float turbidityValue;
float tdsVoltage;
float tdsValue;

int num_samples = 2;

void setup()
{
  Serial.begin(9600);
  for (int i = 0; i < num_samples; i++)
  {
    Serial.print("Sample ");
    Serial.println(i + 1);
    voltage = random(50, 451) / 100.0; // 0.50V to 4.50V

    // Approximate pH calculation (same formula as before)
    phValue = 7 + ((2.5 - voltage) / 0.18);

    Serial.print(" PH Voltage: ");
    Serial.print(voltage);
    Serial.print("   pH Value: ");
    Serial.println(phValue);

    delay(2000);
    // temperature******************
    tempC = random(2000, 4001) / 100.0; // 20.00°C to 40.00°C

    Serial.print("Dummy Water Temperature: ");
    Serial.print(tempC);
    Serial.println(" °C");

    delay(2000);
    // turbidity***********************************
    // Generate a dummy voltage between 0.5V and 4.5V
    voltage = random(50, 451) / 100.0; // 0.50V to 4.50V

    // Convert dummy voltage to turbidity (NTU) using approximate formula
    turbidityValue = 3000 * voltage - 500; // approximate NTU
    if (turbidityValue < 0)
      turbidityValue = 0; // clamp negative values

    Serial.print("Dummy Turbidity Voltage: ");
    Serial.print(voltage);
    Serial.print(" V   Dummy Turbidity: ");
    Serial.print(turbidityValue);
    Serial.println(" NTU");

    delay(2000);
    // Generate a dummy voltage between 0.5V and 4.5V
    tdsVoltage = random(50, 451) / 100.0; // 0.50V to 4.50V

    // Convert dummy voltage to TDS (ppm) using the same formula
    tdsValue = (133.42 * tdsVoltage * tdsVoltage * tdsVoltage - 255.86 * tdsVoltage * tdsVoltage + 857.39 * tdsVoltage) * 0.5; // approximate

    // Print dummy results
    Serial.print("Dummy TDS Voltage: ");
    Serial.print(tdsVoltage);
    Serial.print(" V   Dummy TDS Value: ");
    Serial.print(tdsValue);
    Serial.println(" ppm");

    delay(2000); // wait 2 seconds before next reading
  }
}

void loop()
{
}