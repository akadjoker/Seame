#pragma once
#include <vector>
#include <thread>
#include <atomic>
#include <memory>
#include <algorithm>
#include "CarState.hpp"
#include "Messages.hpp"
#include "Buffer.hpp"

class Server
{
public:
    Server(uint16_t port = 4206);
    ~Server();

    void start();
    void stop();
    std::string getLocalIP() const;

    bool Send(int socket, const Buffer &buffer);
    bool Recv(int socket, Buffer *buffer);

private:
    void acceptConnections();
    bool handleClient(int client_socket);
    void processMessage(uint8_t type, int sender_socket);

    void broadcast(const Buffer &data, int socket);

    int server_socket_;
    std::vector<int> client_sockets_;
    std::mutex clients_mutex_;
    std::atomic<bool> running_;
    std::shared_ptr<CarState> car_state_;
    uint16_t port_;
};
