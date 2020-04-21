//Libraries
#include <ArduinoJson.h>
#include <DHT.h>

//Constants
#define DHT_SENSOR_PIN 2
#define DHT_TYPE DHT22
#define LOOP_DELAY 2000
#define MOTION_SENSOR_PIN 4
#define NODE_ID "fa75e1"
#define ONBOARD_LED_PIN 13

DHT dht(DHT_SENSOR_PIN, DHT_TYPE);


//Variables
float humidity;
float temperature;
bool motion;

void setup()
{
    Serial.begin(9600);
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

    Serial.println(createReportJsonString(temperature, humidity, motion));

    delay(LOOP_DELAY);
}

String createReportJsonString(float temperature, float humidity, bool motion)
{
    const size_t capacity = JSON_ARRAY_SIZE(3) + JSON_OBJECT_SIZE(1) + JSON_OBJECT_SIZE(2) + 3 * JSON_OBJECT_SIZE(3);
    DynamicJsonDocument doc(capacity);

    JsonObject meta = doc.createNestedObject("meta");
    meta["node_id"] = NODE_ID;

    JsonArray reports = doc.createNestedArray("reports");

    JsonObject temp = reports.createNestedObject();
    temp["metric"] = "temperature";
    temp["value"] = temperature;
    temp["rate"] = LOOP_DELAY;

    JsonObject hum = reports.createNestedObject();
    hum["metric"] = "humidity";
    hum["value"] = humidity;
    hum["rate"] = LOOP_DELAY;

    JsonObject mot = reports.createNestedObject();
    mot["metric"] = "motion";
    mot["value"] = motion;
    mot["rate"] = LOOP_DELAY;

    String report;
    serializeJson(doc, report);

    return report;
}
