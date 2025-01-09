#include <iostream>
#include <cstring>
#include <cerrno>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <unistd.h>

int main() {
    int socket_fd;
    struct sockaddr_can addr;
    struct ifreq ifr;
    struct can_frame frame;

    // Cria um socket CAN RAW
    if ((socket_fd = socket(PF_CAN, SOCK_RAW, CAN_RAW)) < 0) {
        std::cerr << "Erro ao criar socket: " << strerror(errno) << std::endl;
        return 1;
    }

    // Define a interface CAN (can0)
    strcpy(ifr.ifr_name, "can0");
    if (ioctl(socket_fd, SIOCGIFINDEX, &ifr) < 0) {
        std::cerr << "Erro ao definir interface: " << strerror(errno) << std::endl;
        close(socket_fd);
        return 1;
    }

    // Configura o endereço do socket
    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    // Associa o socket à interface CAN
    if (bind(socket_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        std::cerr << "Erro ao associar socket: " << strerror(errno) << std::endl;
        close(socket_fd);
        return 1;
    }

    std::cout << "A ouvir mensagens CAN em can0..." << std::endl;

    // Loop para receber mensagens
    while (true) {
        int nbytes = read(socket_fd, &frame, sizeof(struct can_frame));
        if (nbytes < 0) {
            std::cerr << "Erro ao ler do socket: " << strerror(errno) << std::endl;
            break;
        }

        std::cout << "Recebido ID: 0x" << std::hex << frame.can_id << " DLC: " << std::dec << (int)frame.can_dlc << " Dados: ";
        for (int i = 0; i < frame.can_dlc; i++) {
            std::cout << "0x" << std::hex << (int)frame.data[i] << " ";
        }
        std::cout << std::dec << std::endl;
    }

    close(socket_fd);
    return 0;
}
