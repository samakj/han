//Libraries
#include <DHT.h>

#include "config.h"

//Constants
#define ONBOARD_LED_PIN 13
#define DHT_TYPE DHT22

DHT dht(DHT_SENSOR_PIN, DHT_TYPE);


//Variables
float humidity;
float temperature;
bool motion;

void setup()
{
    Serial.begin(9600);
    Serial.println("Starting thm_sensor log string sketch...");

    pinMode(ONBOARD_LED_PIN, OUTPUT);
    digitalWrite(ONBOARD_LED_PIN, LOW);

    pinMode(MOTION_SENSOR_PIN, INPUT);

	dht.begin();
}

void loop()
{
    humidity = dht.readHumidity();
    temperature = dht.readTemperature();
    motion = digitalRead(MOTION_SENSOR_PIN);

    String log;
    char buffer[10];

    log += "Temperature: ";
    log += dtostrf(temperature, 2, 2, buffer);
    log += "°c | Humidity: ";
    log += dtostrf(humidity, 2, 2, buffer);
    log += "% | Motion: ";
    log += motion ? "TRUE" : "FALSE";

    Serial.println(log);
    delay(2000);
}

