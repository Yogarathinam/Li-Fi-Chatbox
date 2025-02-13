#define SOLAR_PIN 34
#define SAMPLE_TIME 100  // Sampling interval in ms
#define START_SIGNAL "11110000"
#define STOP_SIGNAL "00001111"

int roomLight = 0;
int threshold = 0;
bool listening = false;
String receivedData = "";

void setup() {
    Serial.begin(115200);
    Serial.println("ESP32 LiFi Receiver Ready...");
    Serial.println("Calibrating Room Light...");
    
    // Measure room light for 2 seconds
    long total = 0;
    int samples = 20;
    for (int i = 0; i < samples; i++) {
        total += analogRead(SOLAR_PIN);
        delay(100);
    }
    roomLight = total / samples;
    threshold = roomLight + 1500; // Adaptive threshold
    Serial.print("Fixed Room Light Level: ");
    Serial.println(roomLight);
    Serial.print("Adaptive Threshold Set At: ");
    Serial.println(threshold);
}

bool checkPattern(String pattern) {
    return receivedData.endsWith(pattern);
}

void loop() {
    int lightValue = analogRead(SOLAR_PIN);
    bool bitValue = (lightValue > threshold); // High if above threshold
    
    // Append bit
    receivedData += (bitValue ? "1" : "0");

    // Detect Start Signal "11110000"
    if (!listening && checkPattern(START_SIGNAL)) {
        Serial.println("Start Signal Detected! Listening...");
        receivedData = ""; // Reset to start recording
        listening = true;
    }
    
    // Record data only after start signal
    if (listening) {
        if (checkPattern(STOP_SIGNAL)) {
            Serial.println("Stop Signal Detected! Data Received:");
            
            // **Remove the STOP signal from data**
            receivedData = receivedData.substring(0, receivedData.length() - 8);
            
            // Trim excess bits if not a multiple of 8
            while (receivedData.length() % 8 != 0) {
                receivedData.remove(receivedData.length() - 1);
            }
            
            Serial.println(receivedData);
            Serial.print("Decoded Text: ");
            Serial.println(binaryToText(receivedData));
            listening = false;
            receivedData = "";
        }
    }

    delay(SAMPLE_TIME); // 100ms per bit
}

String binaryToText(String binary) {
    String text = "";
    for (int i = 0; i < binary.length(); i += 8) {
        String byteString = binary.substring(i, i + 8);
        char c = strtol(byteString.c_str(), NULL, 2);
        text += c;
    }
    return text;
}
