#include <SPI.h>
#include "mcp2515_can.h"

// Pin where the sensor is connected
const int sensorPin = 3;  
unsigned long pulseCount = 0;  // Pulse count
unsigned long previousMillis = 0;  // Stores the last time speed was updated
const long interval = 500;        // Interval to display speed (in milliseconds)

// Wheel and sensor parameters
const float wheelDiameter = 0.067;  // Diameter in meters
const int pulsesPerRevolution = 36; // Pulses per wheel revolution

// CAN Bus setup
const int SPI_CS_PIN = 9;   // Chip select pin for CAN module

mcp2515_can CAN(SPI_CS_PIN);  // Create an instance of the MCP_CAN class

// SELECT UNITS
const bool METRIC = true;  // Set to false for mph

// Interrupt Service Routine to count pulses
void countPulse() {
  pulseCount++;
}

void setup() {
  // Start serial communication for debugging
  Serial.begin(9600);

  // Initialize CAN Bus
  if (CAN.begin(CAN_500KBPS) == CAN_OK) {
    //Serial.println("CAN initialized successfully!");
  } else {
    //Serial.println("CAN initialization failed!");
    while (1);  // Stop the program if CAN initialization fails
  }

  // Set CAN mode to loopback for testing
  CAN.setMode(MODE_NORMAL);
  //Serial.println("CAN in NORMAL");

  // Set up the speed sensor
  pinMode(sensorPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(sensorPin), countPulse, FALLING);  // Trigger on falling edge
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Calculate rotational speed (RPM)
    float rpm = (pulseCount / (float)pulsesPerRevolution) * 60.0;
    
    // Calculate linear speed
    // Circumference = π * diameter
    float circumference = PI * wheelDiameter;
    
    // Convert to km/h or mph
    float units = (METRIC) ? 1000.000 : 1609.344;  // 1 km/h = 1000 m/h, 1 mph = 1609 m/h
    int speed = round((rpm * circumference * 60.0) / units);

    // Print the speed to Serial Monitor
    //Serial.print("\nSpeed (km/h): ");
    Serial.println(speed);
    pulseCount = 0;

    byte canMessage[1];  // Message data payload
    canMessage[0] = speed & 0xFF;  // Example: speed value in 1 byte

    // Send the CAN message with ID 0x100, standard frame, 1 byte of data
    if (CAN.sendMsgBuf(0x100, 0, 1, canMessage) == CAN_OK) {
      //Serial.println("CAN MESSAGE SENT!");
    } else {
      //Serial.println("CAN MESSAGE ERROR!");
    }
  }
}