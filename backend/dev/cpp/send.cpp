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

    // Prepara a mensagem CAN
    frame.can_id = 0x100; // ID da mensagem
    frame.can_dlc = 8;    // Número de bytes (DLC)
    frame.data[0] = 0x01;
    frame.data[1] = 0x02;
    frame.data[2] = 0x03;
    frame.data[3] = 0x04;
    frame.data[4] = 0x05;
    frame.data[5] = 0x06;
    frame.data[6] = 0x07;
    frame.data[7] = 0x08;

    // Envia a mensagem
    if (write(socket_fd, &frame, sizeof(struct can_frame)) != sizeof(struct can_frame)) {
        std::cerr << "Erro ao enviar mensagem: " << strerror(errno) << std::endl;
    } else {
        std::cout << "Mensagem CAN enviada com sucesso!" << std::endl;
    }

    close(socket_fd);
    return 0;
}
