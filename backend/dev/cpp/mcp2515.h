// mcp2515.h
#ifndef MCP2515_H
#define MCP2515_H

#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <string.h>



#define CANSTAT      0x0E
#define CANCTRL      0x0F
#define BFPCTRL      0x0C
#define TEC          0x1C
#define REC          0x1D
#define CNF3         0x28
#define CNF2         0x29
#define CNF1         0x2A
#define CANINTE      0x2B
#define CANINTF      0x2C
#define EFLG         0x2D
#define TXRTSCTRL    0x0D

// Receive Registers
#define RXB0CTRL     0x60
#define RXB0SIDH     0x61
#define RXB0SIDL     0x62
#define RXB0DLC      0x65
#define RXB0D0       0x66

// Receive Filters
#define RXF0SIDH     0x00
#define RXF0SIDL     0x01
#define RXF1SIDH     0x04
#define RXF1SIDL     0x05

// Receive Masks
#define RXM0SIDH     0x20
#define RXM0SIDL     0x21
#define RXM1SIDH     0x24
#define RXM1SIDL     0x25

// CAN Speed configurations
#define CAN_10Kbps   0x31
#define CAN_25Kbps   0x13
#define CAN_50Kbps   0x09
#define CAN_100Kbps  0x04
#define CAN_125Kbps  0x03
#define CAN_250Kbps  0x01
#define CAN_500Kbps  0x00

// SPI Commands
#define CAN_RESET    0xC0
#define CAN_READ     0x03
#define CAN_WRITE    0x02
#define CAN_RTS      0x80
#define CAN_RTS_TXB0 0x81
#define CAN_RD_STATUS 0xA0
#define CAN_BIT_MODIFY 0x05

class MCP2515 {
public:
    MCP2515();
    ~MCP2515();
    
    bool Init();
    bool Send(uint16_t canId, uint8_t* data, uint8_t length);
    bool Receive(uint8_t* buffer, uint8_t& length);

private:
    int spi_fd;
    bool debug;

    uint8_t ReadByte(uint8_t addr);
    void WriteByte(uint8_t addr, uint8_t data);
    void Reset();
    bool InitSPI();
};
#endif