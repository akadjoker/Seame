import pygame
import time
import math

FONT_8X8 = {
    '0': [0x7C, 0xC6, 0xCE, 0xDE, 0xF6, 0xE6, 0x7C, 0x00],
    '1': [0x30, 0x70, 0x30, 0x30, 0x30, 0x30, 0xFC, 0x00],
    '2': [0x78, 0xCC, 0x0C, 0x38, 0x60, 0xCC, 0xFC, 0x00],
    '3': [0x78, 0xCC, 0x0C, 0x38, 0x0C, 0xCC, 0x78, 0x00],
    '4': [0x1C, 0x3C, 0x6C, 0xCC, 0xFE, 0x0C, 0x1E, 0x00],
    '5': [0xFC, 0xC0, 0xF8, 0x0C, 0x0C, 0xCC, 0x78, 0x00],
    '6': [0x38, 0x60, 0xC0, 0xF8, 0xCC, 0xCC, 0x78, 0x00],
    '7': [0xFC, 0xCC, 0x0C, 0x18, 0x30, 0x30, 0x30, 0x00],
    '8': [0x78, 0xCC, 0xCC, 0x78, 0xCC, 0xCC, 0x78, 0x00],
    '9': [0x78, 0xCC, 0xCC, 0x7C, 0x0C, 0x18, 0x70, 0x00],
    'A': [0x30, 0x78, 0xCC, 0xCC, 0xFC, 0xCC, 0xCC, 0x00],
    'B': [0xFC, 0x66, 0x66, 0x7C, 0x66, 0x66, 0xFC, 0x00],
    'C': [0x3C, 0x66, 0xC0, 0xC0, 0xC0, 0x66, 0x3C, 0x00],
    'D': [0xF8, 0x6C, 0x66, 0x66, 0x66, 0x6C, 0xF8, 0x00],
    'E': [0xFE, 0x62, 0x68, 0x78, 0x68, 0x62, 0xFE, 0x00],
    'F': [0xFE, 0x62, 0x68, 0x78, 0x68, 0x60, 0xF0, 0x00],
    'G': [0x3C, 0x66, 0xC0, 0xC0, 0xCE, 0x66, 0x3E, 0x00],
    'H': [0xCC, 0xCC, 0xCC, 0xFC, 0xCC, 0xCC, 0xCC, 0x00],
    'I': [0x78, 0x30, 0x30, 0x30, 0x30, 0x30, 0x78, 0x00],
    'J': [0x1E, 0x0C, 0x0C, 0x0C, 0xCC, 0xCC, 0x78, 0x00],
    'K': [0xE6, 0x66, 0x6C, 0x78, 0x6C, 0x66, 0xE6, 0x00],
    'L': [0xF0, 0x60, 0x60, 0x60, 0x62, 0x66, 0xFE, 0x00],
    'M': [0xC6, 0xEE, 0xFE, 0xD6, 0xC6, 0xC6, 0xC6, 0x00],
    'N': [0xC6, 0xE6, 0xF6, 0xDE, 0xCE, 0xC6, 0xC6, 0x00],
    'O': [0x38, 0x6C, 0xC6, 0xC6, 0xC6, 0x6C, 0x38, 0x00],
    'P': [0xFC, 0x66, 0x66, 0x7C, 0x60, 0x60, 0xF0, 0x00],
    'Q': [0x78, 0xCC, 0xCC, 0xCC, 0xDC, 0x78, 0x1C, 0x00],
    'R': [0xFC, 0x66, 0x66, 0x7C, 0x6C, 0x66, 0xE6, 0x00],
    'S': [0x78, 0xCC, 0x60, 0x30, 0x18, 0xCC, 0x78, 0x00],
    'T': [0xFC, 0xB4, 0x30, 0x30, 0x30, 0x30, 0x78, 0x00],
    'U': [0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0x78, 0x00],
    'V': [0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0x78, 0x30, 0x00],
    'W': [0xC6, 0xC6, 0xC6, 0xD6, 0xFE, 0xEE, 0xC6, 0x00],
    'X': [0xC6, 0xC6, 0x6C, 0x38, 0x6C, 0xC6, 0xC6, 0x00],
    'Y': [0xCC, 0xCC, 0xCC, 0x78, 0x30, 0x30, 0x78, 0x00],
    'Z': [0xFC, 0xCC, 0x98, 0x30, 0x64, 0xCC, 0xFC, 0x00],
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    '.': [0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x30, 0x00],
    ',': [0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x30, 0x20],
    '!': [0x30, 0x30, 0x30, 0x30, 0x30, 0x00, 0x30, 0x00],
    '?': [0x78, 0xCC, 0x0C, 0x18, 0x30, 0x00, 0x30, 0x00],
    ':': [0x00, 0x30, 0x30, 0x00, 0x00, 0x30, 0x30, 0x00],
    '-': [0x00, 0x00, 0x00, 0x7C, 0x00, 0x00, 0x00, 0x00],
}

class SSD1306_Simulator:
    def __init__(self, scale=4):
        self.width = 128
        self.height = 32
        self.scale = scale
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.width * scale, self.height * scale))
        pygame.display.set_caption('SSD1306 OLED Simulator Team06 SEA:ME')
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
        self.buffer = [[0 for x in range(self.width)] for y in range(self.height)]
        self.screen.fill(self.BLACK)
        pygame.display.flip()
    
    def draw_rect(self, x, y, width, height, fill=False):
            if width < 0:
                x += width
                width = abs(width)
            if height < 0:
                y += height
                height = abs(height)
                
            if fill:
                for i in range(x, x + width):
                    for j in range(y, y + height):
                        self.draw_pixel(i, j)
            else:
                for i in range(x, x + width):
                    self.draw_pixel(i, y)
                    self.draw_pixel(i, y + height - 1)
                for i in range(y, y + height):
                    self.draw_pixel(x, i)
                    self.draw_pixel(x + width - 1, i)

    def draw_circle(self, x_center, y_center, radius, fill=False):
            x = radius
            y = 0
            error = -radius
            
            while x >= y:
                if fill:
                    for i in range(-x, x + 1):
                        self.draw_pixel(x_center + i, y_center + y)
                        self.draw_pixel(x_center + i, y_center - y)
                    for i in range(-y, y + 1):
                        self.draw_pixel(x_center + i, y_center + x)
                        self.draw_pixel(x_center + i, y_center - x)
                else:
                    self.draw_pixel(x_center + x, y_center + y)
                    self.draw_pixel(x_center + y, y_center + x)
                    self.draw_pixel(x_center - y, y_center + x)
                    self.draw_pixel(x_center - x, y_center + y)
                    self.draw_pixel(x_center - x, y_center - y)
                    self.draw_pixel(x_center - y, y_center - x)
                    self.draw_pixel(x_center + y, y_center - x)
                    self.draw_pixel(x_center + x, y_center - y)
                
                error += 2 * y + 1
                y += 1
                if error >= 0:
                    error += 2 * (1 - x)
                    x -= 1

    def draw_oval(self, x, y, width, height, fill=False):
            a = width // 2  # Raio horizontal
            b = height // 2  # Raio vertical
            x_center = x + a
            y_center = y + b
            for angle in range(360):
                rad = math.radians(angle)
                x1 = int(x_center + a * math.cos(rad))
                y1 = int(y_center + b * math.sin(rad))
                
                if fill:
                    self.draw_line(x_center, y_center, x1, y1)
                else:
                    self.draw_pixel(x1, y1)

    def clear(self):
        self.buffer = [[0 for x in range(self.width)] for y in range(self.height)]
    
    def draw_pixel(self, x, y, color=1):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = color
    
    def draw_char(self, x, y, char, scale=1):
        if char in FONT_8X8:
            char_data = FONT_8X8[char]
            for row in range(8):
                for col in range(8):
                    # ordem dos bits invertida
                    # (7-col) para ler os bits da direita para a esquerda
                    if char_data[row] & (1 << (7-col)):
                        for sx in range(scale):
                            for sy in range(scale):
                                self.draw_pixel(x + col * scale + sx, y + row * scale + sy)
    
    def draw_text(self, x, y, text, scale=1, space = 8):
        cursor_x = x
        char_spacing = space * scale  # podmeos mover para uma variavel para alterar no init
        
        for char in text.upper():
            if cursor_x + 8 * scale > self.width:
                cursor_x = x
                y += 8 * scale
            if y + 8 * scale > self.height:
                break
            self.draw_char(cursor_x, y, char, scale)
            cursor_x += char_spacing
    
    def update(self):
        for y in range(self.height):
            for x in range(self.width):
                color = self.WHITE if self.buffer[y][x] else self.BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x * self.scale, y * self.scale, self.scale, self.scale)
                )
        pygame.display.flip()
    
    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

if __name__ == "__main__":
    display = SSD1306_Simulator()
    
    display.draw_text(0, 0, "Team06!", 2)
    display.draw_text(0, 20, "SEA:ME", 1)
    
    running = True
    while running:
        display.update()
        if display.check_quit():
            running = False
        time.sleep(0.1)
    
    pygame.quit()