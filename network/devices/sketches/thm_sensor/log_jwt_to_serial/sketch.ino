//Libraries
#include <ArduinoJson.h>
#include <ArduinoJWT.h>
#include <DHT.h>

#include "config.h"

//Constants
#define DHT_TYPE DHT22
#define LOOP_DELAY 2000
#define ONBOARD_LED_PIN 13

DHT dht(DHT_SENSOR_PIN, DHT_TYPE);
ArduinoJWT jwt_encoder = ArduinoJWT(MQTT_JWT_KEY);

char SALT_CHARS[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-";

//Variables
float humidity;
float temperature;
bool motion;
String report;
String payload;

void setup()
{
    Serial.begin(115200);
    Serial.println("Starting thm_sensor log json sketch...");

    pinMode(ONBOARD_LED_PIN, OUTPUT);
    digitalWrite(ONBOARD_LED_PIN, LOW);

    pinMode(MOTION_SENSOR_PIN, INPUT);

    dht.begin();
}

void loop()
{
    temperature = dht.readTemperature();
    humidity = dht.readHumidity();
    motion = digitalRead(MOTION_SENSOR_PIN);
    report = createReportJsonString(temperature, humidity, motion);
    payload = jwt_encoder.encodeJWT(report);

    Serial.println(payload);

    delay(LOOP_DELAY);
}

String salt (int length)
{
    String s;

    int i;
    for(i = 0; i < length; i++)
    {
        s += SALT_CHARS[rand() % 16];
    }

    return s;
}

String createReportJsonString(float temperature, float humidity, bool motion)
{
    const size_t capacity = JSON_ARRAY_SIZE(3) + JSON_OBJECT_SIZE(1) + JSON_OBJECT_SIZE(2) + 3 * JSON_OBJECT_SIZE(3);
    DynamicJsonDocument doc(capacity);

    JsonObject meta = doc.createNestedObject("meta");
    meta["id"] = NODE_ID;
    meta["t"] = millis() / 1000;
    meta["s"] = salt(8);

    doc["t"] = temperature;
    doc["h"] = humidity;
    doc["m"] = motion;

    String json_string;
    serializeJson(doc, json_string);

    return json_string;
}
