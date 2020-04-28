//Libraries
#include <ArduinoJson.h>
#include <ArduinoJWT.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include "config.h"

//Constants
#define LOOP_DELAY 2000
#define ONBOARD_LED_PIN 13

ArduinoJWT jwt = ArduinoJWT(MQTT_JWT_KEY);
WiFiClient espClient;
PubSubClient client(espClient);

char SALT_CHARS[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-";

//Variables
byte mac[6];
String attachJsonString;
String attachPayload;

void setup()
{
    Serial.begin(115200);
    Serial.println("Starting thm_sensor log json sketch...");

    connectToWifi();

    connectToMqtt();
    attachJsonString = createAttachJsonString();
    attachPayload = jwt.encodeJWT(attachJsonString);
    Serial.println("Sending attach message.");
    client.publish_P("/v0/report/attach", attachPayload.c_str(), false);
}

void loop()
{
    client.loop();
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
    if (!client.connected()) {
        Serial.print("Connecting to MQTT");

        client.setServer(MQTT_HOST, MQTT_PORT);

        while (!client.connected()) {
            Serial.print(".");
            if (client.connect(NODE_ID)) {
                Serial.println(" MQTT connected.");
            } else {
                delay(250);
            }
        }
    }
}

String createAttachJsonString()
{
    const size_t capacity = JSON_OBJECT_SIZE(1) + JSON_OBJECT_SIZE(2);
    DynamicJsonDocument doc(capacity);

    JsonObject meta = doc.createNestedObject("meta");
    meta["id"] = NODE_ID;
    meta["s"] = salt(8);

    String json_string;
    serializeJson(doc, json_string);

    return json_string;
}
