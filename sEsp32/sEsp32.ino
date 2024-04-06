#include <WiFi.h>
#include <WebSocketsClient.h>
#include <SPI.h>  // Required for MFRC522 library
#include <MFRC522.h>  // RFID library
#include <ArduinoJson.h>

const char* ssid = "xxxxx";
const char* password = "xxx";
const char* webSocketHost = "xx.x.x.x";  // Replace with your server's domain name or IP address
const int webSocketPort = 8002;  // WebSocket port of your server
const char* webSocketPath = "/ws/rfid/";  // WebSocket path on your Django Channels server

WebSocketsClient webSocket;
char tokenBuffer[256];  // Buffer to store the token

// Define RFID module pins
#define RST_PIN   5  // Configurable, see typical pin layout above
#define SS_PIN    21  // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

bool isWebSocketConnected = false;  // Flag to track WebSocket connection

void setup() {
    Serial.begin(9600);
    delay(1000);
    Serial.println("Connecting to WiFi...");

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("WiFi connected");

    SPI.begin();  // Initialize SPI bus
    mfrc522.PCD_Init();  // Initialize MFRC522 RFID reader

    // Set up WebSocket client callbacks
    webSocket.begin(webSocketHost, webSocketPort, webSocketPath);
    webSocket.onEvent(webSocketEvent);

    Serial.println("Waiting for WebSocket connection...");
}

void loop() {
    if (!isWebSocketConnected) {
        // If WebSocket is not connected, handle WebSocket events
        webSocket.loop();
        return;
    }

    // Check for new RFID tags
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
        // Read NUID of the card
        String nuid = "";
        for (byte i = 0; i < mfrc522.uid.size; i++) {
            nuid.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
            nuid.concat(String(mfrc522.uid.uidByte[i], HEX));
        }

        // Print NUID to serial monitor
        Serial.print("NUID: ");
        Serial.println(nuid);

        // Send NUID along with the token to the server
        sendTokenAndNUID(nuid);
    }

    // Handle WebSocket events
    webSocket.loop();
}

void sendTokenAndNUID(String nuid) {
    // Parse JSON from tokenBuffer
    DynamicJsonDocument doc(256);
    DeserializationError error = deserializeJson(doc, tokenBuffer);
    if (!error) {
        const char* token = doc["token"];  // Extract token from JSON

        // Construct JSON data to send
        StaticJsonDocument<256> data;
        data["token"] = token;
        data["nuid"] = nuid;

        // Serialize JSON to string
        char dataString[256];
        serializeJson(data, dataString);

        // Send data over WebSocket
        webSocket.sendTXT(dataString);
    } else {
        Serial.print("Error parsing JSON: ");
        Serial.println(error.c_str());
    }
}

void webSocketEvent(WStype_t type, uint8_t* payload, size_t length) {
    switch (type) {
        case WStype_TEXT:
            Serial.print("Received data from server: ");

            if (strcmp((char*)payload, "ack") == 0) {
                Serial.println("Received acknowledgment from server");
                
            } else {
                Serial.print("Received token: ");
                Serial.println((char*)payload);
                strncpy(tokenBuffer, (char*)payload, sizeof(tokenBuffer) - 1);
                tokenBuffer[sizeof(tokenBuffer) - 1] = '\0';  // Ensure null-terminated string
            }
            break;
        case WStype_CONNECTED:
            Serial.println("WebSocket connected");
            isWebSocketConnected = true;
            break;
        case WStype_DISCONNECTED:
            Serial.println("WebSocket disconnected");
            isWebSocketConnected = false;
            break;
        default:
            break;
    }
}
