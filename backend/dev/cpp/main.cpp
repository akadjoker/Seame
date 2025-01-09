#include "mcp2515.h"
#include <iostream>
#include <iomanip>
#include <signal.h>

volatile bool running = true;

void signalHandler(int signum)
{
    running = false;
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

    std::cout << "Sending initial data..." << std::endl;
    uint16_t id = 0x100; // ID exemplo
    uint8_t data[] = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
    uint8_t dlc = 8;

    if (!can.Send(id, data, dlc))
    {
        std::cerr << "Initial send failed!" << std::endl;
        return 1;
    }

    std::cout << "Waiting for messages..." << std::endl;

    uint8_t readbuf[8];
    uint8_t length;

    while (running)
    {
        if (can.Receive(readbuf, length))
        {
            std::cout << "Received: ";
            for (int i = 0; i < length; i++)
            {
                std::cout << "0x" << std::hex << std::setw(2) << std::setfill('0')
                          << static_cast<int>(readbuf[i]) << " ";
            }
            std::cout << std::dec << std::endl;
        }

        static uint32_t lastSend = 0;
        uint32_t now = time(NULL);
        if (now - lastSend >= 1)
        {
            data[0]++;
            can.Send(id, data, dlc);
            lastSend = now;
        }

        usleep(10000); // 10ms delay
    }

    std::cout << "\n--------------------------------------------------------" << std::endl;
    return 0;
}