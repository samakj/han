//Libraries
#include <DHT.h>

#include "config.h"

//Constants
#define ONBOARD_LED_PIN 13
#define DHT_TYPE DHT22
#define TEMPERATURE_INTERVAL 2000
#define HUMIDITY_INTERVAL 2000
#define MOTION_INTERVAL 10

DHT dht(DHT_SENSOR_PIN, DHT_TYPE);


//Variables
int millis_offset = -1;
time_t tm_initial = time(nullptr);
int ts_initial = mktime(gmtime(&tm_initial));
bool millis_offset_message_sent = false;

float humidity;
float temperature;
bool motion;
int humidity_last_test = -1;
int temperature_last_test = -1;
int motion_last_test = -1;

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
    if (millis_offset == -1)
    {
        if (!millis_offset_message_sent) {
            Serial.println("Getting millis offset...");
            millis_offset_message_sent = true;
        }
        setTimestampMillisOffset();
        return;
    }

    checkHumidityMeasurement();
    checkTemperatureMeasurement();
    checkMotionMeasurement();
}

void setTimestampMillisOffset()
{
    time_t tm_loop = time(nullptr);
    int ts_loop = mktime(gmtime(&tm_loop));
    int current_millis = millis();

    if (ts_loop != ts_initial)
    {
        millis_offset = current_millis % 1000;
        Serial.print("Offset found to be ");
        Serial.print(millis_offset);
        Serial.println("ms.");
    }
}

String getIsoTimestamp()
{
    String isoTimestamp;

    char datetime_buffer[23];
    time_t tm = time(nullptr);
    strftime(datetime_buffer, 23, "%FT%T", gmtime(&tm));
    isoTimestamp += datetime_buffer;

    char milliseconds_buffer[5];
    sprintf(milliseconds_buffer, ".%03d", (millis() - millis_offset) % 1000);
    isoTimestamp += milliseconds_buffer;

    return isoTimestamp;
}

void checkTemperatureMeasurement()
{
    int current_millis = millis();
    if (temperature_last_test == -1 || current_millis - temperature_last_test > TEMPERATURE_INTERVAL)
    {
        float t = dht.readTemperature();

        if (!isnan(t) && t != temperature)
        {
            temperature = t;

            String temperature_report;
            temperature_report += getIsoTimestamp();
            temperature_report += "| Temperature changed to: ";
            temperature_report += temperature;
            temperature_report += "°c";

            Serial.println(temperature_report);
        }

        temperature_last_test = current_millis;
    }
}

void checkHumidityMeasurement()
{
    int current_millis = millis();
    if (humidity_last_test == -1 || current_millis - humidity_last_test > HUMIDITY_INTERVAL)
    {
        float h = dht.readHumidity();

        if (!isnan(h) && h != humidity)
        {
            humidity = h;

            time_t tm = time(nullptr);
            char isoTimestamp[29];
            strftime(isoTimestamp, 29, "%FT%T+00:00", gmtime(&tm));

            String humidity_report;
            humidity_report += getIsoTimestamp();
            humidity_report += "| Humidity changed to: ";
            humidity_report += humidity;
            humidity_report += "%";

            Serial.println(humidity_report);
        }

        humidity_last_test = current_millis;
    }
}

void checkMotionMeasurement()
{
    int current_millis = millis();
    if (motion_last_test == -1 || current_millis - motion_last_test > MOTION_INTERVAL)
    {
        bool m = digitalRead(MOTION_SENSOR_PIN);

        if (!isnan(m) && m != motion)
        {
            motion = m;

            String motion_report;
            motion_report += getIsoTimestamp();
            motion_report += "| Motion changed to: ";
            motion_report += motion ? "TRUE" : "FALSE";

            Serial.println(motion_report);
        }

        motion_last_test = current_millis;
    }
}

