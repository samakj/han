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
#define TEMPERATURE_INTERVAL 2000
#define HUMIDITY_INTERVAL 2000
#define MOTION_INTERVAL 10
#define PING_INTERVAL 1000

DHT dht(DHT_SENSOR_PIN, DHT_TYPE);
WiFiClientSecure wifiClient;
PubSubClient mqttClient(wifiClient);

//Variables
byte MACAddressByteArray[6];
String MACAddress;

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

String HUMIDITY_TOPIC;
String TEMPERATURE_TOPIC;
String MOTION_TOPIC;
String PING_TOPIC;
int last_ping = -1;

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

    connectToWifi();
    connectToMqtt();
    mqttClient.loop();

    checkHumidityMeasurement();
    checkTemperatureMeasurement();
    checkMotionMeasurement();
    pingMqtt();
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

    millis_offset = -1;

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

    PING_TOPIC += V0_META_TOPIC_ROOT;
    PING_TOPIC += "/";
    PING_TOPIC += NODE_ID;
    PING_TOPIC += "/";
    PING_TOPIC += "ping";
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
            temperature_report += "|";
            temperature_report += temperature;

            Serial.print("Reporting to ");
            Serial.print(TEMPERATURE_TOPIC);
            Serial.print(" -> ");
            Serial.println(temperature_report);

            mqttClient.publish(TEMPERATURE_TOPIC.c_str(), temperature_report.c_str());
            mqttClient.loop();
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

            String humidity_report;
            humidity_report += getIsoTimestamp();
            humidity_report += "|";
            humidity_report += humidity;

            Serial.print("Reporting to ");
            Serial.print(HUMIDITY_TOPIC);
            Serial.print("    -> ");
            Serial.println(humidity_report);

            mqttClient.publish(HUMIDITY_TOPIC.c_str(), humidity_report.c_str());
            mqttClient.loop();
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
            motion_report += "|";
            motion_report += motion ? "TRUE" : "FALSE";

            Serial.print("Reporting to ");
            Serial.print(MOTION_TOPIC);
            Serial.print("      -> ");
            Serial.println(motion_report);

            mqttClient.publish(MOTION_TOPIC.c_str(), motion_report.c_str());
            mqttClient.loop();
        }

        motion_last_test = current_millis;
    }
}

void pingMqtt()
{
    int current_millis = millis();
    if (last_ping == -1 || current_millis - last_ping > PING_INTERVAL)
    {
        String motion_report;
        ping_report += getIsoTimestamp();
        ping_report += "|ping";

        mqttClient.publish(PING_TOPIC.c_str(), ping_report.c_str());
        mqttClient.loop();

        last_ping = current_millis;
    }
}
