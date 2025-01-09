
    

import socket
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# Configuração do I2C
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 32, i2c)

# Limpa o display
oled.fill(0)
oled.show()

# Função para obter o IP
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "Sem Conexão"
    finally:
        s.close()
    return ip

# Criar a imagem para o OLED
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Escrever o IP
ip = get_ip()
draw.text((0, 0), f"IP: {ip}", font=font, fill=255)
oled.image(image)
oled.show()
