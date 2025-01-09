#pragma once
#include <cstdint>
enum class MessageType : uint8_t
{
    SPEED    = 1,
    WHEELS = 2,
    MOTOR    = 3
};

#pragma pack(push, 1) 

struct MessageHeader
{
    uint8_t  type;
    uint16_t size;
    char     *buffer;
};

struct SpeedMessage
{
    int16_t speed;
};

struct WheelMessage
{
    int16_t angle;
};

struct MotorMessage
{
  
    int8_t direction; // -1: tas 0: parado, 1: frente
    uint8_t power;    // 0-100%
};
#pragma pack(pop)