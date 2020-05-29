//Libraries
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <time.h>
#include <WiFiClientSecure.h>

#include "config.h"
#include "certificates.h"

//Constants
#define MQTT_SOCKET_TIMEOUT 60
#define MEASUREMENT_INTERVAL 2000
#define ONBOARD_LED_PIN 13

WiFiClientSecure wifiClient;
PubSubClient mqttClient(wifiClient);

//Variables
byte MACAddressByteArray[6];
String MACAddress;

void setup()
{
    Serial.begin(115200);
    Serial.println("");
    Serial.println("");
    Serial.println("***********************************************************");
    Serial.println("* ~ Starting thm_sensor establish tls connection sketch ~ *");
    Serial.println("***********************************************************");
    Serial.println("");

    connectToWifi();
    connectToNtpTime();
    connectToMqtt();
}

void loop()
{
    connectToWifi();
    connectToMqtt();
    mqttClient.loop();

    Serial.println(millis());

    delay(MEASUREMENT_INTERVAL);
}

void connectToWifi()
{
    if (WiFi.status() != WL_CONNECTED)
    {
        int start = millis();
        Serial.print("Connecting to ");
        Serial.print(WIFI_SSID);

        WiFi.mode(WIFI_STA);
        WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

        int i = 0;
        while (WiFi.status() != WL_CONNECTED)
        {
            !(i % 32) ? Serial.println(".") : Serial.print(".");
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
        sprintf(buf, "%02X", MACAddressByteArray[i]);
        s += buf;
        if (i < 5) s += ':';
    }
    return s;
}

void connectToNtpTime()
{
    int start = millis();
    Serial.print("Connnecting to time server @ ");
    Serial.print(NTP_SERVER);

    int i = 0;

    while (time(nullptr) < 1577836800) {
        if (!(i % 4)) configTime(TIMEZONE * 3600, DST * 3600, NTP_SERVER);
        !(i % 32) ? Serial.println(".") : Serial.print(".");
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
//        wifiClient.setTrustAnchors(new BearSSL::X509List(CA_CERT));

        Serial.print("Connecting to MQTT @ ");
        Serial.print(MQTT_HOST);
        Serial.print(":");
        Serial.print(MQTT_PORT);

        mqttClient.setServer(MQTT_HOST, MQTT_PORT);
        mqttClient.connect(MACAddress.c_str(), (char*)NODE_ID, (char*)"test");

        int i = 0;
        while (!mqttClient.connected()) {
            !(i % 32) ? Serial.println(".") : Serial.print(".");
            mqttClient.loop();
            i++;
            delay(250);
        }

        Serial.println("");
        Serial.print("Connected to MQTT after ");
        Serial.print((millis() - start) / 1000.0);
        Serial.println("s.");

        if (wifiClient.verify(CA_CERT, MQTT_HOST)) {
            Serial.println("Connection security verified.");
        }
    }
}
