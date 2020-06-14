//Libraries
#include <DHT.h>

#include "config.h"

//Constants
#define ONBOARD_LED_PIN 13
#define DHT_TYPE DHT22
#define MEASUREMENT_INTERVAL 2000

DHT dht(DHT_SENSOR_PIN, DHT_TYPE);


//Variables
float humidity;
float temperature;
bool motion;

void setup()
{
    Serial.begin(115200);
    Serial.println("Starting thm_sensor log string sketch...");

    pinMode(ONBOARD_LED_PIN, OUTPUT);
    digitalWrite(ONBOARD_LED_PIN, LOW);

    pinMode(MOTION_SENSOR_PIN, INPUT);

	dht.begin();
}

void loop()
{
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    bool m = digitalRead(MOTION_SENSOR_PIN);

    time_t tm = time(nullptr);
    char now[29];
    strftime(now, 29, "%FT%T+00:00", gmtime(&tm));

    if (!isnan(t) && t != temperature)
    {
        temperature = t;

        String temperature_report;
        temperature_report += now;
        temperature_report += "| Temperature changed to: ";
        temperature_report += temperature;
        temperature_report += "°c";

        Serial.println(temperature_report);
    }
    if (!isnan(h) && h != humidity)
    {
        humidity = h;

        String humidity_report;
        humidity_report += now;
        humidity_report += "| Humidity changed to: ";
        humidity_report += humidity;
        humidity_report += "%";

        Serial.println(humidity_report);
    }
    if (!isnan(m) && m != motion)
    {
        motion = m;

        String motion_report;
        motion_report += now;
        motion_report += "| Motion changed to: ";
        motion_report += motion ? "TRUE" : "FALSE";

        Serial.println(motion_report);
    }

    delay(MEASUREMENT_INTERVAL);
}

