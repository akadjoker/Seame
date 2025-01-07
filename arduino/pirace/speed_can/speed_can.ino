#include <SPI.h>
#include "mcp2515_can.h"


struct VehicleData 
{
    uint16_t speed;          // Velocidade atual (km/h ou mph)
    uint32_t totalPulses;    // Total de pulsos desde o início
    uint16_t rpm;            // RPM atual
    uint32_t timestamp;      // Timestamp da medição
     // float temperature;    // Temperatura
    // float voltage;        // Tensão da bateria
    // uint32_t distance;    // Distância percorrida
    // etc...
};

const int sensorPin = 3;// Pin onde o sensor está conectado
unsigned long pulseCount = 0;
unsigned long previousMillis = 0;
const long interval = 500; // Intervalo em millisegundos

// Parâmetros da roda e sensor
const float wheelDiameter = 0.067;  // Diâmetro em metros
const int pulsesPerRevolution = 36; // Pulsos por revolução
bool isReady = false;
// Configuração CAN Bus
const int SPI_CS_PIN = 9;
mcp2515_can CAN(SPI_CS_PIN);

// Seleção de unidades
const bool METRIC = true;  // false para mph

// Estrutura global para armazenar dados
VehicleData vehicleData = {0};

// ISR para contar pulsos
void countPulse() 
{
    pulseCount++;
    vehicleData.totalPulses++;
}

void setup() 
{
    Serial.begin(9600);
    
    // Inicializa CAN Bus
    while (CAN.begin(CAN_500KBPS) != CAN_OK) 
    {
        Serial.println("CAN init failed, retrying...");
        isReady = false;
        delay(100);
    }
    
    CAN.setMode(MODE_NORMAL);
    
    // Configura sensor
    pinMode(sensorPin, INPUT);
    attachInterrupt(digitalPinToInterrupt(sensorPin), countPulse, FALLING);
    isReady = true;
}

// Função para calcular e atualizar dados do veículo
void updateVehicleData() 
{
    // Calcula RPM
    vehicleData.rpm = (pulseCount / (float)pulsesPerRevolution) * (60.0 * (1000.0 / interval));
    
    // Calcula velocidade linear
    float circumference = PI * wheelDiameter;
    float units = (METRIC) ? 1000.000 : 1609.344;
    vehicleData.speed = round((vehicleData.rpm * circumference * 60.0) / units);
    
    // Atualiza timestamp
    vehicleData.timestamp = millis();
}

// Função para enviar dados via CAN
void sendCANData() 
{
    byte canData[8] = {0}; // Buffer para 8 bytes de dados
    
    // Empacota os dados
    canData[0] = vehicleData.speed & 0xFF;         // Byte baixo da velocidade
    canData[1] = (vehicleData.speed >> 8) & 0xFF;  // Byte alto da velocidade
    canData[2] = vehicleData.rpm & 0xFF;           // Byte baixo do RPM
    canData[3] = (vehicleData.rpm >> 8) & 0xFF;    // Byte alto do RPM
    // canData[4] a [7] disponíveis para futuros dados
    
    // Envia mensagem CAN (ID 0x100, formato standard, 8 bytes de dados)
    if (CAN.sendMsgBuf(0x100, 0, 8, canData) == CAN_OK)
    {
        Serial.println("Dados enviados via CAN");
    } else {
        Serial.println("Erro no envio CAN");
    }
}

void loop() 
{
    unsigned long currentMillis = millis();
    
    if (currentMillis - previousMillis >= interval) 
    {
        previousMillis = currentMillis;
        
        // Atualiza dados
        updateVehicleData();
        
        sendCANData();
        
        Serial.print("Velocidade: ");
        Serial.print(vehicleData.speed);
        Serial.print(METRIC ? " km/h" : " mph");
        Serial.print(" RPM: ");
        Serial.println(vehicleData.rpm);
        
        // Resetamos contador de pulsos
        pulseCount = 0;
    }
}