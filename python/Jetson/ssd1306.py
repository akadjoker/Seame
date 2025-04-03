import smbus2
from PIL import Image, ImageDraw, ImageFont
import time

class SSD1306:
    def __init__(self, i2c_bus=1, address=0x3C, width=128, height=32):
        self.bus = smbus2.SMBus(i2c_bus)
        self.address = address
        self.width = width
        self.height = height
        self.image = Image.new("1", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        self._init_display()

    def _command(self, cmd):
        self.bus.write_byte_data(self.address, 0x00, cmd)

    def _init_display(self):
        cmds = [0xAE, 0x20, 0x00, 0xB0, 0xC8, 0x00, 0x10, 0x40,
                0x81, 0x7F, 0xA1, 0xA6, 0xA8, 0x1F, 0xD3, 0x00,
                0xD5, 0xF0, 0xD9, 0x22, 0xDA, 0x02, 0xDB, 0x20,
                0x8D, 0x14, 0xAF]
        for cmd in cmds:
            self._command(cmd)

    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def text(self, msg, x=0, y=0):
        self.draw.text((x, y), msg, font=self.font, fill=255)

    def show(self):
        buffer = list(self.image.tobytes())
        for page in range(0, self.height // 8):
            self._command(0xB0 + page)
            self._command(0x00)
            self._command(0x10)
            start = self.width * page
            self.bus.write_i2c_block_data(self.address, 0x40, buffer[start:start + self.width])

