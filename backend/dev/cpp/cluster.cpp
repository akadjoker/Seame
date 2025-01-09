#include "mcp2515.h"
#include <iostream>
#include <iomanip>
#include <signal.h>

volatile bool running = true;

void signalHandler(int signum)
{
    running = false;
}

struct CarData
{
    uint16_t speed; // Velocidade em km/h
    uint16_t rpm;   // RPM
};

void displayCluster(const CarData &carData)
{
    std::cout << "----- CLUSTER -----" << std::endl;
    std::cout << "Velocidade: " << (int)carData.speed << " km/h" << std::endl;
    std::cout << "RPM: " << (int)carData.rpm << std::endl;
    std::cout << "-------------------" << std::endl;
}
int main()
{
    signal(SIGINT, signalHandler);
    std::cout << "--------------------------------------------------------" << std::endl;

    MCP2515 can;

    std::cout << "Initializing..." << std::endl;
    if (!can.Init())
    {
        std::cerr << "Initialization failed!" << std::endl;
        return 1;
    }

    std::cout << "Waiting for messages..." << std::endl;

    uint8_t readBuf[8];
    uint8_t length;
    CarData carData;

    while (running)
    {
        if (can.Receive(readBuf, length))
        {
            if (length == sizeof(CarData))
            {
                memcpy(&carData, readBuf, sizeof(CarData));
                displayCluster(carData);
            }
            else
            {
                std::cerr << "Invalid data length received: " << (int)length << std::endl;
            }
        }

        usleep(10000); 
    }

    std::cout << "\n--------------------------------------------------------" << std::endl;
    return 0;
}