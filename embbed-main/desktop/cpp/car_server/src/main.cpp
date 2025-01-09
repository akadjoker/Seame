#include "Server.hpp"
#include <iostream>
#include <csignal>

std::atomic<bool> running(true);

void signal_handler(int)
{
    running = false;
    std::cout<<"Aborted"<< std::endl;
}

int main()
{
    signal(SIGINT, signal_handler);

    try
    {
        Server server;
        server.start();

        std::cout << "Servidor enable.  Ctrl+C para terminar." << std::endl;

        while (running)
        {
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }

        server.stop();
    }
    catch (const std::exception &e)
    {
        std::cerr << "Erro: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
