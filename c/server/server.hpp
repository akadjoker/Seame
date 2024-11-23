#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <thread>
#include <queue>
#include <mutex>
#include <fstream>
#include <chrono>
#include <atomic>
#include <condition_variable>

enum class MessageType : uint8_t
{
    // Comandos de movimento
    MOVE_FORWARD = 1,
    MOVE_BACKWARD = 2,
    TURN_LEFT = 3,
    TURN_RIGHT = 4,
    STOP = 5,

    // Comandos de display
    DISPLAY_TEXT = 10,
    DISPLAY_IP = 11,
    CLEAR_DISPLAY = 12,

    // Comandos de sistema
    GET_SENSOR_DATA = 20,
    GET_POSITION = 21,
    SET_SPEED = 22,
    SAVE_POSITION = 23,
    LOAD_POSITION = 24,
    SHUTDOWN_SERVER = 25,
    PING = 26,
    PONG = 27,

    // Respostas
    ACK = 100,
    NACK = 101,
    DATA_RESPONSE = 102
};

#pragma pack(push, 1)
struct MessageHeader
{
    uint8_t startMarker = 0xFF;
    MessageType type;
    uint16_t payloadSize;
    uint32_t sequenceNumber;
    uint32_t timestamp;
};

struct DisplayMessage
{
    MessageHeader header;
    char text[64]; // Texto para mostrar no display
};

struct PositionData
{
    MessageHeader header;
    float x;
    float y;
    float heading;
    uint32_t timestamp;
};

struct SystemState
{
    float x = 0.0f;
    float y = 0.0f;
    float heading = 0.0f;
    float batteryLevel = 100.0f;
    float temperature = 25.0f;
    std::string lastDisplayMessage;
    std::chrono::system_clock::time_point lastUpdate;
};
#pragma pack(pop)

class NonBlockingRobotControl
{
private:
    int socket_;
    bool isServer_;
    struct sockaddr_in address_;
    static const int PORT = 8888;
    static const int BUFFER_SIZE = 1024;

    std::atomic<bool> running_{true};
    std::queue<std::vector<uint8_t>> messageQueue_;
    std::mutex queueMutex_;
    std::condition_variable queueCondition_;

    SystemState state_;
    std::string stateFile_ = "robot_state.txt";
    std::string logFile_ = "robot_log.txt";

    std::unique_ptr<std::thread> processThread_;
    std::unique_ptr<std::thread> displayThread_;

public:
    NonBlockingRobotControl(bool isServer) : isServer_(isServer)
    {
        socket_ = socket(AF_INET, SOCK_STREAM, 0);
        if (socket_ == -1)
        {
            throw std::runtime_error(" Failed to create socket");
        }

        // Configura socket como non-blocking
        int flags = fcntl(socket_, F_GETFL, 0);
        fcntl(socket_, F_SETFL, flags | O_NONBLOCK);

        address_.sin_family = AF_INET;
        address_.sin_port = htons(PORT);

        if (isServer_)
        {
            address_.sin_addr.s_addr = INADDR_ANY;
            initializeServer();
            loadState();
            startThreads();
        }
    }

    void initializeServer()
    {
        int opt = 1;
        setsockopt(socket_, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

        if (bind(socket_, (struct sockaddr *)&address_, sizeof(address_)) < 0)
        {
            throw std::runtime_error("Falha no bind");
        }

        if (listen(socket_, 5) < 0)
        {
            throw std::runtime_error("Falha no listen");
        }

        displayIpAddress();
        logMessage("Server Initialized");
    }

    void startThreads()
    {
        processThread_ = std::make_unique<std::thread>(&NonBlockingRobotControl::processLoop, this);
        displayThread_ = std::make_unique<std::thread>(&NonBlockingRobotControl::displayLoop, this);
    }

    void displayLoop()
    {
        while (running_)
        {
            updateDisplay();
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }

    void updateDisplay()
    {
        // Simula 
        std::cout << "\033[2J\033[1;1H"; 
        std::cout << "=== Robot Display ===\n";
        std::cout << "Position: (" << state_.x << ", " << state_.y << ")\n";
        std::cout << "Heading: " << state_.heading << "°\n";
        std::cout << "Battery: " << state_.batteryLevel << "%\n";
        std::cout << "Last Message: " << state_.lastDisplayMessage << "\n";
    }

    void displayIpAddress()
    {
        char hostname[256];
        gethostname(hostname, sizeof(hostname));

        struct ifaddrs *ifaddr, *ifa;
        if (getifaddrs(&ifaddr) == -1)
        {
            logMessage("Fail to get network interfaces");
            return;
        }

        std::string ipAddress = "IPs: ";
        for (ifa = ifaddr; ifa != nullptr; ifa = ifa->ifa_next)
        {
            if (ifa->ifa_addr && ifa->ifa_addr->sa_family == AF_INET)
            {
                void *tmpAddrPtr = &((struct sockaddr_in *)ifa->ifa_addr)->sin_addr;
                char addressBuffer[INET_ADDRSTRLEN];
                inet_ntop(AF_INET, tmpAddrPtr, addressBuffer, INET_ADDRSTRLEN);
                ipAddress += std::string(addressBuffer) + " ";
            }
        }

        freeifaddrs(ifaddr);
        state_.lastDisplayMessage = ipAddress;
        logMessage("IPs mostrados no display: " + ipAddress);
    }

    void saveState()
    {
        // Json::Value root;
        // root["x"] = state_.x;
        // root["y"] = state_.y;
        // root["heading"] = state_.heading;
        // root["battery"] = state_.batteryLevel;

        // std::ofstream file(stateFile_);
        // if (file.is_open())
        // {
        //     file << root;
        //     file.close();
        //     logMessage("Estado salvo em " + stateFile_);
        // }
    }

    void loadState()
    {
        // std::ifstream file(stateFile_);
        // if (file.is_open())
        // {
        //     Json::Value root;
        //     file >> root;

        //     state_.x = root.get("x", 0.0f).asFloat();
        //     state_.y = root.get("y", 0.0f).asFloat();
        //     state_.heading = root.get("heading", 0.0f).asFloat();
        //     state_.batteryLevel = root.get("battery", 100.0f).asFloat();

        //     logMessage("Estado carregado de " + stateFile_);
        //     file.close();
        // }
    }

    void logMessage(const std::string &message)
    {
        std::ofstream log(logFile_, std::ios::app);
        if (log.is_open())
        {
            auto now = std::chrono::system_clock::now();
            auto nowTime = std::chrono::system_clock::to_time_t(now);
            log << std::ctime(&nowTime) << ": " << message << std::endl;
            log.close();
        }
    }

    void processMessage(const std::vector<uint8_t> &buffer)
    {
        if (buffer.size() < sizeof(MessageHeader))
            return;

        const MessageHeader *header = reinterpret_cast<const MessageHeader *>(buffer.data());

        if (header->startMarker != 0xFF)
        {
            logMessage("Invalid message start marker");
            return;
        }

        switch (header->type)
        {
        case MessageType::DISPLAY_TEXT:
        {
            const DisplayMessage *msg = reinterpret_cast<const DisplayMessage *>(buffer.data());
            state_.lastDisplayMessage = std::string(msg->text);
            logMessage("Display: " + state_.lastDisplayMessage);
            break;
        }
        case MessageType::DISPLAY_IP:
        {
            displayIpAddress();
            break;
        }
        case MessageType::SAVE_POSITION:
        {
            saveState();
            break;
        }
        case MessageType::LOAD_POSITION:
        {
            loadState();
            break;
        }
        case MessageType::SHUTDOWN_SERVER:
        {
            logMessage("Turn off server");
            running_ = false;
            saveState();
            break;
        }
            
        }
    }

    void processLoop()
    {
        std::vector<uint8_t> buffer(BUFFER_SIZE);
        while (running_)
        {
            std::unique_lock<std::mutex> lock(queueMutex_);
            queueCondition_.wait_for(lock, std::chrono::milliseconds(100),
                                     [this]
                                     { return !messageQueue_.empty(); });

            while (!messageQueue_.empty())
            {
                auto msg = std::move(messageQueue_.front());
                messageQueue_.pop();
                lock.unlock();

                processMessage(msg);

                lock.lock();
            }
        }
    }

    void enqueueMessage(const std::vector<uint8_t> &message)
    {
        {
            std::lock_guard<std::mutex> lock(queueMutex_);
            messageQueue_.push(message);
        }
        queueCondition_.notify_one();
    }

    void displayText(const std::string &text)
    {
        DisplayMessage msg;
        msg.header.type = MessageType::DISPLAY_TEXT;
        msg.header.payloadSize = sizeof(DisplayMessage) - sizeof(MessageHeader);
        msg.header.timestamp = std::chrono::system_clock::now().time_since_epoch().count();
        strncpy(msg.text, text.c_str(), sizeof(msg.text) - 1);

        std::vector<uint8_t> buffer(sizeof(DisplayMessage));
        memcpy(buffer.data(), &msg, sizeof(DisplayMessage));
        enqueueMessage(buffer);
    }

    void shutdown()
    {
        MessageHeader header;
        header.type = MessageType::SHUTDOWN_SERVER;
        header.payloadSize = 0;
        header.timestamp = std::chrono::system_clock::now().time_since_epoch().count();

        std::vector<uint8_t> buffer(sizeof(MessageHeader));
        memcpy(buffer.data(), &header, sizeof(MessageHeader));
        enqueueMessage(buffer);
    }

    ~NonBlockingRobotControl()
    {
        running_ = false;
        if (processThread_ && processThread_->joinable())
        {
            processThread_->join();
        }
        if (displayThread_ && displayThread_->joinable())
        {
            displayThread_->join();
        }
        close(socket_);
    }
};
