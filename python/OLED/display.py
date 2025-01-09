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
    


    def blit(self, buffer, x=0, y=0):
            buffer_height = len(buffer)
            buffer_width = len(buffer[0])
            
            for by in range(buffer_height):
                for bx in range(buffer_width):
                    dx = x + bx
                    dy = y + by
                    if 0 <= dx < self.width and 0 <= dy < self.height:
                        self.buffer[dy][dx] = buffer[by][bx]

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
    

    def save_buffer(self, filename, scale=1):
        save_width = self.width * scale
        save_height = self.height * scale
        save_surface = pygame.Surface((save_width, save_height))
        for y in range(self.height):
            for x in range(self.width):
                color = self.WHITE if self.buffer[y][x] else self.BLACK
                pygame.draw.rect(
                    save_surface,
                    color,
                    (x * scale, y * scale, scale, scale)
                )
        pygame.image.save(save_surface, filename)

    def save_image_buffer(self,buffer,  filename, scale=1):
        height = len(buffer)
        width = len(buffer[0]) if height > 0 else 0
      
        save_width = width * scale
        save_height = height * scale
        save_surface = pygame.Surface((save_width, save_height))
        for y in range(height):
            for x in range(width):
                color = self.WHITE if buffer[y][x] else self.BLACK
                pygame.draw.rect(
                    save_surface,
                    color,
                    (x * scale, y * scale, scale, scale)
                )
        pygame.image.save(save_surface, filename)


    def load_image(self, image_path,width=None, height=None):
        image = pygame.image.load(image_path)
        
        if width and height:
            image = pygame.transform.scale(image, (width, height))
        else:
            width = image.get_width()
            height = image.get_height()

        #image = pygame.transform.scale(image, (self.width, self.height))
        
        
        # convertemos para cinza
        image = pygame.Surface.convert_alpha(image)
        buffer = [[0 for x in range(width)] for y in range(height)]
        
        # Convertemos pixels em (preto e branco)
        for y in range(height):
            for x in range(width):
                # media dos valores RGB
                pixel = image.get_at((x, y))
                brightness = (pixel[0] + pixel[1] + pixel[2]) // 3
                #  usamos o 128 para threshold OBS podemos passar por variavel
                buffer[y][x] = 1 if brightness > 128 else 0
                
        return buffer
    def load_image_colorkey(self, image_path, colorkey=(255,255,0), threshold=30):
        """
        ignorando uma cor específica (com tolerância)
        colorkey: cor RGB a ser ignorada (default é mangenta A VERIFICAR)
        threshold: tolerância para a cor (variações)
        """
        image = pygame.image.load(image_path)

        width = image.get_width()
        height = image.get_height() 
       
        #image = pygame.transform.scale(image, (self.width, self.height))
        image = pygame.Surface.convert_alpha(image)
        
        buffer = [[0 for x in range(width)] for y in range(height)]
        
        for y in range(height):
            for x in range(width):
                pixel = image.get_at((x, y))
                
                if self._color_range(pixel, colorkey, threshold):
                    buffer[y][x] = 0  # Transparente"NADA"
                else:
                    brightness = (pixel[0] + pixel[1] + pixel[2]) // 3
                    buffer[y][x] = 1 if brightness > 128 else 0
                
        return buffer
    
    def _color_range(self, color1, color2, threshold):
        r1, g1, b1 = color1[:3]
        r2, g2, b2 = color2
        
        return (abs(r1 - r2) <= threshold and 
                abs(g1 - g2) <= threshold and 
                abs(b1 - b2) <= threshold)    


    def generate_doom_face(self, expression='normal', direction='front'):
        """
        Gera um buffer com uma face estilo Doom
        
        Args:
            expression: 'normal', 'angry', 'smile', 'hurt'
            direction: 'front', 'left', 'right'
        """
        # Tamanho da face (32x32 pixels)
        face_size = 32
        buffer = [[0 for x in range(face_size)] for y in range(face_size)]
        
        # Função auxiliar para desenhar pixels
        def draw_pixels(pixels):
            for x, y in pixels:
                if 0 <= x < face_size and 0 <= y < face_size:
                    buffer[y][x] = 1

        # Desenha o contorno da cabeça
        head_contour = [(x, 0) for x in range(8, 24)] + \
                      [(x, 31) for x in range(8, 24)] + \
                      [(8, y) for y in range(32)] + \
                      [(23, y) for y in range(32)]
        draw_pixels(head_contour)

        # Desenha os olhos baseado na direção
        left_eye_x = 12 if direction == 'left' else (14 if direction == 'right' else 13)
        right_eye_x = 18 if direction == 'left' else (20 if direction == 'right' else 19)
        
        # Olhos normais
        if expression != 'hurt':
            # Olho esquerdo
            for y in range(10, 14):
                for x in range(left_eye_x, left_eye_x + 3):
                    buffer[y][x] = 1
                    
            # Olho direito
            for y in range(10, 14):
                for x in range(right_eye_x, right_eye_x + 3):
                    buffer[y][x] = 1

        # Olhos machucados
        if expression == 'hurt':
            # Olhos em X
            for i in range(3):
                buffer[10+i][left_eye_x+i] = 1
                buffer[10+i][left_eye_x+2-i] = 1
                buffer[10+i][right_eye_x+i] = 1
                buffer[10+i][right_eye_x+2-i] = 1

        # Boca 
        if expression == 'normal':
            for x in range(12, 20):
                buffer[22][x] = 1
        elif expression == 'angry':
            for i in range(4):
                buffer[20+i][12+i] = 1
                buffer[20+i][19-i] = 1
        elif expression == 'smile':
            for i in range(4):
                buffer[22-i][12+i] = 1
                buffer[22-i][19-i] = 1
        elif expression == 'hurt':
            for i in range(5):
                buffer[24][13+i] = 1

        if expression == 'angry':
            for i in range(3):
                buffer[8][11+i] = 1
                buffer[8][18+i] = 1
                buffer[9][12+i] = 1
                buffer[9][19+i] = 1

        return buffer

    def draw_doom_face(self, x, y, expression='normal', direction='front'):
        face_buffer = self.generate_doom_face(expression, direction)
        self.blit(face_buffer, x, y)

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
    

def teste_text():
    display = SSD1306_Simulator()
    
    display.draw_text(10, 0, "Team06!", 2)
    display.draw_text(0, 20, "SEA:ME", 1)
    display.draw_text(60, 20, "42Porto", 1)
    custom_buffer = [
        [1,1,1,1,0,0,0,1],
        [1,0,0,1,0,0,0,1],
        [1,0,0,1,0,0,0,1],
        [1,1,1,1,0,0,1,0],
    ]

    display.save_image_buffer(custom_buffer,"custom_buffer.bmp", scale=1)
    
    display.blit(custom_buffer,5,5)

    running = True
    while running:
        display.update()
        if display.check_quit():
            running = False
        time.sleep(0.1)

    pygame.quit()

def teste_faces():
    display = SSD1306_Simulator()
    
  
    expressions = [
        ('normal', 'front'),
        ('normal', 'left'),
        ('normal', 'right'),
        ('angry', 'front'),
        ('smile', 'front'),
        ('hurt', 'front')
    ]
    
    running = True
    frame = 0
    while running:
        display.clear()

        FPS = 60 # lento , 30 normal
        
        # expressão atual
        expression, direction = expressions[frame // FPS]
        

        display.draw_doom_face(0, 0, expression, direction)
        
        # Atualiza o frame
        frame = (frame + 1) % (len(expressions) * FPS)
        #frame = 5 * FPS
        
        display.update()
        if display.check_quit():
            running = False
        time.sleep(0.033)  # Aproximadamente 30 FPS    
    pygame.quit()

def teste_buffer():
    display = SSD1306_Simulator()
    
    custom_buffer = [
        [1,1,1,1,0,0,0,1],
        [1,0,0,1,0,0,0,1],
        [1,0,0,1,0,0,0,1],
        [1,1,1,1,0,0,1,0],
    ]

    display.save_image_buffer(custom_buffer,"custom_buffer.bmp", scale=1)
    
    display.blit(custom_buffer,5,5)

    running = True
    while running:
        display.update()
        if display.check_quit():
            running = False
        time.sleep(0.1)

    pygame.quit()


RETRO_FACES = {
    'face1': [  # Normal face (top left)
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,1,0,0,1,1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,0,0,0,0,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
    ],
    'face2': [  # Serious face (top middle)
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,1,0,0,1,1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,0,0,0,0,0,0,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
    ],
    'face3': [  # Concerned face (top right)
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,1,0,0,1,1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,0,0,0,0,1,1,1,1,1],
        [1,1,1,1,0,0,1,1,0,0,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
    ],
    'face4': [  # Angry face (bottom left)
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,0,0,1,1,1,1,1,1,0,0,1,1],
        [1,1,1,0,0,1,1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,0,0,0,0,1,1,1,1,1],
        [1,1,1,1,0,0,1,1,0,0,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
    ],
    'face5': [  # Shouting face (bottom middle)
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,0,0,1,1,1,1,1,1,0,0,1,1],
        [1,1,1,0,0,1,1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,0,0,0,0,1,1,1,1,1],
        [1,1,1,0,0,0,1,1,0,0,0,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
    ],
    'face6': [  # Intense face (bottom right)
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,0,0,1,1,1,1,1,1,0,0,1,1],
        [1,1,1,0,0,1,1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,0,0,0,0,0,0,1,1,1,1],
        [1,1,1,0,0,1,1,1,1,0,0,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
    ]
}

class RetroFaceDemo:
    def __init__(self, display):
        self.display = display
    def draw_face(self, face_name, x, y):
        if face_name in RETRO_FACES:
            self.display.blit(RETRO_FACES[face_name], x, y)
            
    def demo_all_faces(self):
        # grid 2x3
        positions = [
            (0, 0), (20, 0), (40, 0),    # Top row
            (0, 15), (20, 15), (40, 15)  # Bottom row
        ]
        
        self.display.clear()
        
        for face_name, pos in zip(RETRO_FACES.keys(), positions):
            self.draw_face(face_name, pos[0], pos[1])
            
        self.display.update()
            
    def animate_faces(self):
        faces = list(RETRO_FACES.keys())
        frame = 0
        
        while True:
            self.display.clear()
            face_name = faces[frame % len(faces)]
            self.draw_face(face_name, 10, 10)
            self.display.update()
            
            frame += 1
            time.sleep(0.5)  # Meio segundo de pausa
            
            if self.display.check_quit():
                break

def teste_doom_face():
    display = SSD1306_Simulator()
    demo = RetroFaceDemo(display)
    demo.demo_all_faces()
    time.sleep(2)
    demo.animate_faces()
    pygame.quit()

def test_real_image():
    display = SSD1306_Simulator()
    
    buffer = display.load_image("../../assets/face.bmp",30,30)
    print(buffer)
    display.save_image_buffer(buffer,"custom_buffer.bmp", scale=1)
    
    display.blit(buffer,40,1)

    running = True
    while running:
        display.update()
        if display.check_quit():
            running = False
        time.sleep(0.1)

    pygame.quit()


if __name__ == "__main__":
    #teste_text()
    #teste_faces()
    #teste_buffer()
    #teste_doom_face()
    test_real_image()
