#pragma once
#include <mutex>
#include <cstdint>

class CarState
{
public:
    struct State
    {
        int16_t speed;
        int16_t angle;
        int8_t direction; // -1: tas 0: parado, 1: frente
        uint8_t power;// 0-100%

        State() : speed(0), angle(0),   direction(0), power(0) {}
    };

    void updateSpeed(int16_t new_speed)
    {
        std::lock_guard<std::mutex> lock(mutex_);
        state_.speed = new_speed;
    }

    void updateWheels(int16_t turn)
    {
        std::lock_guard<std::mutex> lock(mutex_);
        state_.angle = turn;
    }


    void updateMotor(int8_t dir, uint8_t pwr)
    {
        std::lock_guard<std::mutex> lock(mutex_);
        state_.direction = dir;
        state_.power = pwr;
    }

    State getState()
    {
        std::lock_guard<std::mutex> lock(mutex_);
        return state_;
    }

private:
    mutable std::mutex mutex_;
    State state_;
};
