#include "Server.hpp"
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <iostream>

Server::Server(uint16_t port)
    : port_(port), running_(false), car_state_(std::make_shared<CarState>())
{

    server_socket_ = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket_ < 0)
    {
        throw std::runtime_error(" Fail to create socket");
    }

    int opt = 1;
    setsockopt(server_socket_, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    sockaddr_in server_addr{};
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port_);

    car_state_->updateSpeed(60);
    car_state_->updateWheels(-180);
    car_state_->updateMotor(1, 75);

    if (bind(server_socket_, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0)
    {
        throw std::runtime_error("Fail to bind");
    }

    if (listen(server_socket_, 5) < 0)
    {
        throw std::runtime_error("Fail to listen");
    }
}

void Server::start()
{
    running_ = true;
    std::cout << " Server started on " << getLocalIP() << ":" << port_ << std::endl;

    std::thread accept_thread([this]()
                              { acceptConnections(); });
    accept_thread.detach();
}

void Server::acceptConnections()
{
    while (running_)
    {
        sockaddr_in client_addr{};
        socklen_t client_len = sizeof(client_addr);
        int client_socket = accept(server_socket_,
                                   (struct sockaddr *)&client_addr,
                                   &client_len);

        if (client_socket >= 0)
        {
            std::cout << "New connection from "
                      << inet_ntoa(client_addr.sin_addr) << std::endl;

            // Adicionar cliente à lista
            {
                std::lock_guard<std::mutex> lock(clients_mutex_);
                client_sockets_.push_back(client_socket);
            }

            std::thread client_thread([this, client_socket]()
                                      { handleClient(client_socket); });
            client_thread.detach();
        }
    }
}
bool Server::Recv(int socket, Buffer *buffer)
{
    //  (primeiro byte) que indica o tipo
    //std::cout << "Reading header..." << std::endl;
    uint8_t type;
    ssize_t received = recv(socket, &type, sizeof(uint8_t), MSG_WAITALL);
    if (received <= 0)
    {
        std::cout << " Connection closed" << std::endl;
        return false;
    }
    // Lê o tamanho (2 bytes)
    uint16_t size;
    received = recv(socket, &size, sizeof(uint16_t), MSG_WAITALL);
    if (received <= 0)
    {
        std::cout << " Connection closed" << std::endl;
        return false;
    }

    buffer->setPosition(0);

    buffer->writeByte(type);
    buffer->writeUShort(size);

    if (size > 0)
    {

        std::vector<uint8_t> tempBuffer(size);
        received = recv(socket, tempBuffer.data(), size, MSG_WAITALL);
        if (received <= 0)
        {
            std::cout << " Connection closed" << std::endl;
            return false;
        }

        buffer->writeBytes(tempBuffer.data(), size);
    }
    buffer->setPosition(0);
 //   std::cout << "Read " << buffer->size() << " bytes" << std::endl;

    return true;
}

bool Server::Send(int socket, const Buffer &buffer)
{
    if (buffer.size() > 0)
    {
        return send(socket, buffer.getData(), buffer.size(), 0) > 0;
    }
    else
    {
        return true;
    }
}

bool Server::handleClient(int client_socket)
{

    while (running_)
    {
        Buffer requestBuffer;
        if (!Recv(client_socket, &requestBuffer))
        {
            break; // Sai do loop se houver erro
        }

       

        uint8_t type = requestBuffer.readByte();
        uint16_t size = requestBuffer.readUShort();

       //std::cout << "Process message " << requestBuffer.size() << " " << requestBuffer.getPosition() << std::endl;

        processMessage(type, client_socket);
     //   Send(client_socket, requestBuffer);
    }

    // Remove cliente da lista ao desconectar
    {
        std::lock_guard<std::mutex> lock(clients_mutex_);
        client_sockets_.erase(
            std::remove(client_sockets_.begin(), client_sockets_.end(), client_socket),
            client_sockets_.end());
    }
    close(client_socket);

    return true;
}

void Server::processMessage(uint8_t type, int sender_socket)
{

    switch (static_cast<MessageType>(type))
    {
    case MessageType::SPEED:
    {
        SpeedMessage msg;
        auto state = car_state_->getState();
        msg.speed = state.speed;
        Buffer responseBuffer;
        responseBuffer.writeByte(msg.speed);
        Send(sender_socket, responseBuffer);

        break;
    }
    case MessageType::WHEELS:
    {
        WheelMessage msg;
        auto state = car_state_->getState();
        msg.angle = state.angle;
        Buffer responseBuffer;
        responseBuffer.writeShort(msg.angle);
        Send(sender_socket, responseBuffer);

        break;
    }
    case MessageType::MOTOR:
    {
        MotorMessage msg;

        auto state = car_state_->getState();
        msg.direction = state.direction;
        msg.power = state.power;

        Buffer responseBuffer;
        responseBuffer.writeByte(msg.direction);
        responseBuffer.writeByte(msg.power);
        Send(sender_socket, responseBuffer);

        break;
    }

    default:
        std::cout << "Unknown message type: " << type << std::endl;
        Buffer responseBuffer;
        responseBuffer.writeByte(128);
        Send(sender_socket, responseBuffer);
        break;
    }
}

void Server::broadcast(const Buffer &data, int socket)
{
    ///podeos eviar para todos para 1 cliente ??? a ver depois
    std::lock_guard<std::mutex> lock(clients_mutex_);
    for (int client : client_sockets_)
    {
        if (client == socket)
        {
            Send(client, data);
        }
    }
}

std::string Server::getLocalIP() const
{
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1)
        return "unknown";

    struct sockaddr_in serv
    {
    };
    serv.sin_family = AF_INET;
    serv.sin_addr.s_addr = inet_addr("8.8.8.8");
    serv.sin_port = htons(53);

    if (connect(sock, (const struct sockaddr *)&serv, sizeof(serv)) == -1)
    {
        close(sock);
        return "unknown";
    }

    struct sockaddr_in name
    {
    };
    socklen_t namelen = sizeof(name);
    getsockname(sock, (struct sockaddr *)&name, &namelen);

    close(sock);
    return inet_ntoa(name.sin_addr);
}

void Server::stop()
{
    running_ = false;
    std::lock_guard<std::mutex> lock(clients_mutex_);
    for (int client : client_sockets_)
    {
        close(client);
    }
    close(server_socket_);
}

Server::~Server()
{
    stop();
}
