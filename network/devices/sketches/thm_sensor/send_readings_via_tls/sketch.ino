//Libraries
#include <DHT.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <time.h>
#include <WiFiClientSecure.h>

#include "config.h"
#include "certificates.h"

//Constants
#define DHT_TYPE DHT22
#define MQTT_SOCKET_TIMEOUT 60
#define MEASUREMENT_INTERVAL 2000

DHT dht(DHT_SENSOR_PIN, DHT_TYPE);
WiFiClientSecure wifiClient;
PubSubClient mqttClient(wifiClient);

//Variables
byte MACAddressByteArray[6];
String MACAddress;
float humidity;
float temperature;
bool motion;

String HUMIDITY_TOPIC;
String TEMPERATURE_TOPIC;
String MOTION_TOPIC;

void setup()
{
    Serial.begin(115200);
    Serial.println("");
    Serial.println("");
    Serial.println("***********************************************************");
    Serial.println("* ~ Starting thm_sensor establish tls connection sketch ~ *");
    Serial.println("***********************************************************");

    createReportTopics();

    connectToWifi();
    connectToNtpTime();
    connectToMqtt();
}

void loop()
{
    connectToWifi();
    connectToMqtt();
    mqttClient.loop();

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
        temperature_report += ":";
        temperature_report += temperature;

        Serial.print("Reporting to ");
        Serial.print(TEMPERATURE_TOPIC);
        Serial.print(" -> ");
        Serial.println(temperature_report);

        mqttClient.publish(TEMPERATURE_TOPIC.c_str(), temperature_report.c_str());
    }
    if (!isnan(h) && h != humidity)
    {
        humidity = h;

        String humidity_report;
        humidity_report += now;
        humidity_report += ":";
        humidity_report += humidity;

        Serial.print("Reporting to ");
        Serial.print(HUMIDITY_TOPIC);
        Serial.print(" -> ");
        Serial.println(humidity_report);

        mqttClient.publish(HUMIDITY_TOPIC.c_str(), humidity_report.c_str());
    }
    if (!isnan(m) && m != motion)
    {
        motion = m;

        String motion_report;
        motion_report += now;
        motion_report += ":";
        motion_report += motion ? "TRUE" : "FALSE";

        Serial.print("Reporting to ");
        Serial.print(MOTION_TOPIC);
        Serial.print(" -> ");
        Serial.println(motion_report);

        mqttClient.publish(MOTION_TOPIC.c_str(), motion_report.c_str());
    }

    delay(MEASUREMENT_INTERVAL);
}

void connectToWifi()
{
    if (WiFi.status() != WL_CONNECTED)
    {
        int start = millis();

        int i = 0;
        while (WiFi.status() != WL_CONNECTED)
        {
            if (!(i % 32))
            {
                Serial.println("");
                Serial.print("Connecting to ");
                Serial.print(WIFI_SSID);
                WiFi.mode(WIFI_STA);
                WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
            }

            Serial.print(".");
            i++;
            delay(250);
        }

        Serial.println("");
        Serial.print("Connected WiFi after ");
        Serial.print((millis() - start) / 1000.0);
        Serial.println("s.");

        WiFi.macAddress(MACAddressByteArray);
        MACAddress = MACAddressByteArrayToString(MACAddressByteArray);

        Serial.print("IP Address: ");
        Serial.println(WiFi.localIP());
        Serial.print("MAC Address: ");
        Serial.println(MACAddress);
    }
}

String MACAddressByteArrayToString(byte MACAddressByteArray[6])
{
    String s;
    for (byte i = 0; i < 6; ++i)
    {
        char buf[3];
        sprintf(buf, "%02x", MACAddressByteArray[i]);
        s += buf;
        if (i < 5) s += ':';
    }
    return s;
}

void connectToNtpTime()
{
    int start = millis();

    int i = 0;
    while (time(nullptr) < 1577836800)
    {
        if(!(i % 32))
        {
            Serial.println("");
            Serial.print("Connnecting to time server @ ");
            Serial.print(NTP_SERVER);
            configTime(TIMEZONE * 3600, DST * 3600, NTP_SERVER);
        }
        Serial.print(".");
        i++;
        delay(250);
    }

    Serial.println("");
    Serial.print("Connected to NTP Server after ");
    Serial.print((millis() - start) / 1000.0);
    Serial.println("s.");
    Serial.print("Time synchronised to: ");

    time_t now = time(nullptr);
    Serial.print(ctime(&now));
}

void connectToMqtt()
{
    if (!mqttClient.connected())
    {
        int start = millis();

        wifiClient.setInsecure();

        int i = 0;
        while (!mqttClient.connected())
        {
            if (!(i % 32))
            {
                Serial.println("");
                Serial.print("Connecting to MQTT @ ");
                Serial.print(MQTT_HOST);
                Serial.print(":");
                Serial.print(MQTT_PORT);

                mqttClient.setServer(MQTT_HOST, MQTT_PORT);
                mqttClient.connect(MACAddress.c_str(), (char*)NODE_ID, (char*)MQTT_PASSWORD);
            }
            Serial.print(".");
            mqttClient.loop();
            i++;
            delay(250);
        }

        Serial.println("");
        Serial.print("Connected to MQTT after ");
        Serial.print((millis() - start) / 1000.0);
        Serial.println("s.");

        if (wifiClient.verify(CA_CERT, MQTT_HOST))
        {
            Serial.println("Connection security verified.");
        }
    }
}

void createReportTopics()
{
    HUMIDITY_TOPIC += V0_REPORT_TOPIC_ROOT;
    HUMIDITY_TOPIC += "/";
    HUMIDITY_TOPIC += NODE_ID;
    HUMIDITY_TOPIC += "/";
    HUMIDITY_TOPIC += "humidity";

    TEMPERATURE_TOPIC += V0_REPORT_TOPIC_ROOT;
    TEMPERATURE_TOPIC += "/";
    TEMPERATURE_TOPIC += NODE_ID;
    TEMPERATURE_TOPIC += "/";
    TEMPERATURE_TOPIC += "temperature";

    MOTION_TOPIC += V0_REPORT_TOPIC_ROOT;
    MOTION_TOPIC += "/";
    MOTION_TOPIC += NODE_ID;
    MOTION_TOPIC += "/";
    MOTION_TOPIC += "motion";
}
