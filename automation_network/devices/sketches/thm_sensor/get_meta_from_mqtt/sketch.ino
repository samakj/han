//Libraries
#include <ArduinoJson.h>
#include <ArduinoJWT.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include "config.h"

//Constants
#define MEASUREMENT_INTERVAL 2000
#define ONBOARD_LED_PIN 13

ArduinoJWT jwt = ArduinoJWT(MQTT_JWT_KEY);
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

char SALT_CHARS[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-";

//Variables
byte mac[6];
String metaRequestJsonString;
String metaRequestPayload;
long initialTimestamp = -1;
long lastMeasurementMillis = -MEASUREMENT_INTERVAL;

void setup()
{
    Serial.begin(115200);
    Serial.println("Starting thm_sensor log json sketch...");

    connectToWifi();

    connectToMqtt();
    metaRequestJsonString = createMetaRequestJsonString();
    metaRequestPayload = jwt.encodeJWT(metaRequestJsonString);
    Serial.println("Sending meta request message...");
    mqttClient.subscribe(META_TOPIC);
    mqttClient.publish_P(META_TOPIC, metaRequestPayload.c_str(), false);
}

void loop()
{
    mqttClient.loop();

    if (initialTimestamp != -1) {
        if (millis() - lastMeasurementMillis > MEASUREMENT_INTERVAL) {
            // DO MEASUREMENTS
            Serial.println(millis());

            lastMeasurementMillis = millis();
        }
    }
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

void connectToWifi()
{
    if (WiFi.status() != WL_CONNECTED) {
        Serial.print("Connecting to ");
        Serial.print(WIFI_SSID);

        WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

        while (WiFi.status() != WL_CONNECTED) {
            delay(250);
            Serial.print(".");
        }

        Serial.println(" WiFi connected.");

        Serial.print("IP Address:");
        Serial.print(WiFi.localIP());
        WiFi.macAddress(mac);
        Serial.print(" | MAC Address: ");
        Serial.print(mac[5], HEX);
        Serial.print(":");
        Serial.print(mac[4], HEX);
        Serial.print(":");
        Serial.print(mac[3], HEX);
        Serial.print(":");
        Serial.print(mac[2], HEX);
        Serial.print(":");
        Serial.print(mac[1], HEX);
        Serial.print(":");
        Serial.println(mac[0], HEX);
    }
}

void connectToMqtt()
{
    if (!mqttClient.connected()) {
        Serial.print("Connecting to MQTT");

        mqttClient.setServer(MQTT_HOST, MQTT_PORT);
        mqttClient.setCallback(subscriptionCallback);

        while (!mqttClient.connected()) {
            Serial.print(".");
            if (mqttClient.connect(NODE_ID)) {
                Serial.println(" MQTT connected.");
            } else {
                delay(250);
            }
        }
    }
}

String createMetaRequestJsonString()
{
    const size_t capacity = JSON_ARRAY_SIZE(1) + 2 * JSON_OBJECT_SIZE(2) + 64;
    DynamicJsonDocument doc(capacity);

    JsonObject meta = doc.createNestedObject("meta");
    meta["id"] = NODE_ID;
    meta["s"] = salt(8);

    JsonArray keys = doc.createNestedArray("k");
    keys.add("t");

    String jsonString;
    serializeJson(doc, jsonString);

    return jsonString;
}

void handleMetaResponse(char* payload)
{
    char* payloadString;
    bool decodeError = jwt.decodeJWT(payloadString, payload, strlen(payload));

    if (decodeError) {
        Serial.print("Invalid jwt received.");
        return;
    }

    const size_t capacity = JSON_OBJECT_SIZE(1) + JSON_OBJECT_SIZE(2) + 64;
    DynamicJsonDocument data(capacity);
    DeserializationError deserialisationError = deserializeJson(data, payloadString);

    if (deserialisationError) {
        Serial.print("Invalid json recieved: ");
        Serial.println(deserialisationError.c_str());
        return;
    }

    long timestamp = data["t"];

    if (data["meta"]["id"] == NODE_ID) {
        initialTimestamp = timestamp - (millis() / 1000);
        Serial.println("Meta data handled, unsubscribing.");
        mqttClient.unsubscribe(META_TOPIC);
    } else {
        Serial.println("Incorrect meta data.");
    }
}

void subscriptionCallback(char* topic, byte* payload, unsigned int length)
{
    if (strcmp(META_TOPIC, topic) == 0) {
        Serial.println("Meta response received.");
        handleMetaResponse((char*)payload);
    }
}
