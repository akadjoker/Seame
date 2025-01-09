import spidev
import time

# Configuração do SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI0, CS0
spi.max_speed_hz = 1000000

# Função para enviar e receber dados SPI
def spi_transfer(data):
    return spi.xfer2(data)

# Inicializar o MCP2515
def init_mcp2515():
    # Reset do MCP2515
    spi_transfer([0xC0])  # Comando RESET
    time.sleep(0.1)

    # Configurar o modo loopback
    spi_transfer([0x02, 0x0F, 0x40])  # Escreve no registro CANCTRL para entrar no modo loopback
    print("MCP2515 configurado no modo loopback")

# Enviar mensagem CAN
def send_can_message():
    # Configurar ID e dados da mensagem
    spi_transfer([0x40, 0x31, 0x00, 0x00, 0x00, 0x00])  # Configura o ID
    spi_transfer([0x40, 0x36, 0x08, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])  # Configura os dados
    spi_transfer([0x81])  # Solicita transmissão
    print("Mensagem CAN enviada")

# Receber mensagem CAN
def receive_can_message():
    # Verifica se há mensagens recebidas
    status = spi_transfer([0xA0, 0x00])[1]
    if status & 0x01:
        # Lê a mensagem recebida
        message = spi_transfer([0x90, 0x00] + [0x00] * 13)
        print("Mensagem CAN recebida: ", message)
    else:
        print("Sem mensagens CAN")

# Inicializar o MCP2515
init_mcp2515()

# Loop principal
while True:
    send_can_message()
    time.sleep(1)
    receive_can_message()
    time.sleep(1)
