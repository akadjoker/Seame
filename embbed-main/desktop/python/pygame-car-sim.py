import pygame
import math
from pygame import gfxdraw  
from Jetcar import *

class CarSimulator:
    def __init__(self, width=1024, height=768):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("JetCar Simulator")
        
        # Relógio para controle de FPS
        self.clock = pygame.time.Clock()
        
        # Cria o carro
        self.car = JetCar()
        
        # Estado do carro
        self.car_pos = [width//2, height//2]  # [x, y]
        self.car_angle = 0  # Ângulo em graus
        
        # Cores
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        
    def draw_car(self):
        # Desenha o corpo do carro
        car_length = 40
        car_width = 20
        
        # Calcula os pontos do retângulo do carro
        angle_rad = math.radians(self.car_angle)
        cos_val = math.cos(angle_rad)
        sin_val = math.sin(angle_rad)
        
        half_length = car_length // 2
        half_width = car_width // 2
        
        points = [
            (-half_length, -half_width),
            (half_length, -half_width),
            (half_length, half_width),
            (-half_length, half_width)
        ]
        
        # Rotaciona e translada os pontos
        rotated_points = []
        for x, y in points:
            rotated_x = x * cos_val - y * sin_val + self.car_pos[0]
            rotated_y = x * sin_val + y * cos_val + self.car_pos[1]
            rotated_points.append((int(rotated_x), int(rotated_y)))
        
        # Desenha o carro
        pygame.gfxdraw.filled_polygon(self.screen, rotated_points, self.BLUE)
        pygame.gfxdraw.aapolygon(self.screen, rotated_points, self.WHITE)
        
        # Desenha uma linha indicando a direção
        front_x = self.car_pos[0] + half_length * 1.5 * cos_val
        front_y = self.car_pos[1] + half_length * 1.5 * sin_val
        pygame.draw.line(self.screen, self.RED, 
                        (self.car_pos[0], self.car_pos[1]),
                        (front_x, front_y), 2)

    def draw_hud(self):
        # Desenha informações do carro
        state = self.car.get_state()
        info_texts = [
            f"Speed: {state['speed']:.1f} km/h",
            f"Gear: {state['gear']}",
            f"Mode: {'Auto' if state['is_automatic'] else 'Manual'}",
            f"Steering: {state['steering_angle']}°"
        ]
        
        for i, text in enumerate(info_texts):
            surface = pygame.font.Font(None, 36).render(text, True, self.WHITE)
            self.screen.blit(surface, (10, 10 + i * 30))

    def update_car_position(self):
        state = self.car.get_state()
        speed = state['speed']
        
        # Atualiza o ângulo do carro baseado no ângulo do volante
        self.car_angle += state['steering_angle'] * 0.01 * speed
        
        # Converte velocidade e ângulo em movimento x,y
        angle_rad = math.radians(self.car_angle)
        self.car_pos[0] += math.cos(angle_rad) * speed * 0.1
        self.car_pos[1] += math.sin(angle_rad) * speed * 0.1
        
        # Mantém o carro dentro da tela
        self.car_pos[0] = self.car_pos[0] % self.width
        self.car_pos[1] = self.car_pos[1] % self.height

    def run(self):
        #controller = create_keyboard_controller()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            # Atualiza estado do carro
            #controller()
            self.update_car_position()
            
            # Limpa a tela
            self.screen.fill(self.BLACK)
            
            # Desenha
            self.draw_car()
            self.draw_hud()
            
            # Atualiza a tela
            pygame.display.flip()
            
            # Controle de FPS
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    simulator = CarSimulator()
    simulator.run()
