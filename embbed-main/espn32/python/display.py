import machine
import time
import st7735
import framebuf

# Definindo os pinos
CS_PIN = 5    # Chip Select
DC_PIN = 19   # Data/Command
RST_PIN = 18  # Reset
SCK_PIN = 18  # SPI Clock
SDI_PIN = 23  # SPI Data In

# Configurando o barramento SPI
spi = machine.SPI(1, baudrate=10000000, polarity=0, phase=0, sck=machine.Pin(SCK_PIN), mosi=machine.Pin(SDI_PIN))

# Inicializando o display ST7735
lcd = st7735.ST7735(spi, cs=machine.Pin(CS_PIN), dc=machine.Pin(DC_PIN), rst=machine.Pin(RST_PIN))

# Inicializando o display
lcd.init()

# Limpando a tela com cor preta
lcd.fill(0)

# Exibindo texto
lcd.text('Hello, ESP32!', 10, 10, st7735.color565(255, 255, 255))  # Texto branco

while True:
    time.sleep(1)  # Manter a tela atualizada
