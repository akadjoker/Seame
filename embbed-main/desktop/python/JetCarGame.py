import pygame
import math
import sys
from pygame import gfxdraw
from Jetcar import *

class JetCarGame:
    def __init__(self):
        pygame.init()
        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("JetCar Simulator")
        
        self.car = JetCar() 
        self.car_pos = [self.width // 2, self.height // 2]
        self.car_rotation = 0
        self.clock = pygame.time.Clock()
        
        # Cores
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)

    # def handle_input(self):
    #     keys = pygame.key.get_pressed()
        
    #     # Aceleração e travao
    #     if keys[pygame.K_UP]:
    #         self.car.motor.update(1.0)
    #     else:
    #         self.car.motor.update(0)
            
    #     if keys[pygame.K_DOWN]:
    #         self.car.motor.brake(1.0)
        
    #     # Direção
    #     if keys[pygame.K_LEFT]:
    #         self.car.steering.turn_left()
    #     elif keys[pygame.K_RIGHT]:
    #         self.car.steering.turn_right()
    #     else:
    #         self.car.steering.center()
        
    #     # Troca de gear manual (apenas no modo manual)
    #     if not self.car.motor.transmission.is_automatic:
    #         if keys[pygame.K_q]:  # gear up
    #             self.car.motor.transmission.current_gear = min(4, self.car.motor.transmission.current_gear + 1)
    #         if keys[pygame.K_a]:  # gear down
    #             self.car.motor.transmission.current_gear = max(1, self.car.motor.transmission.current_gear - 1)
        
    #     # Alternar modo de transmissão
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             return False
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_t:
    #                 self.car.toggle_transmission()
                    
    #     return True
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Aceleração e direção (contínuos)
        if keys[pygame.K_UP]:
            self.car.motor.update(1.0)
        else:
            self.car.motor.update(0)
            
        if keys[pygame.K_DOWN]:
            self.car.motor.brake(1.0)
        
        if keys[pygame.K_LEFT]:
            self.car.steering.turn_left()
        elif keys[pygame.K_RIGHT]:
            self.car.steering.turn_right()
        else:
            self.car.steering.center()
        
        # Eventos únicos (keydown)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if not self.car.motor.transmission.is_automatic:
                    if event.key == pygame.K_q:  # Marcha acima
                        current_gear = self.car.motor.transmission.current_gear
                        if current_gear < 4:
                            self.car.motor.transmission.current_gear = current_gear + 1
                            self.show_gear_change_message("Gear Up", current_gear + 1)
                            
                    elif event.key == pygame.K_a:  # Marcha abaixo
                        current_gear = self.car.motor.transmission.current_gear
                        if current_gear > 1:
                            self.car.motor.transmission.current_gear = current_gear - 1
                            self.show_gear_change_message("Gear Down", current_gear - 1)
                
                # Alternar modo de transmissão
                if event.key == pygame.K_t:
                    mode = self.car.toggle_transmission()
                    self.show_transmission_message(mode)
                    
        return True
    
    def show_gear_change_message(self, action, new_gear):
        print(f"{action}: {new_gear}")  

    def show_transmission_message(self, mode):
        print(f"Transmission mode: {mode}") 


    def update_car_position(self):

        speed_factor = self.car.motor.speed / 50.0
        angle_rad = math.radians(self.car_rotation)
        
        self.car_pos[0] += math.cos(angle_rad) * speed_factor
        self.car_pos[1] += math.sin(angle_rad) * speed_factor
        

        self.car_pos[0] = self.car_pos[0] % self.width
        self.car_pos[1] = self.car_pos[1] % self.height
        
    
        self.car_rotation += self.car.steering.angle / 30 * speed_factor

    def draw_speedometer(self, x, y, radius):

        pygame.draw.arc(self.screen, self.WHITE, (x-radius, y-radius, radius*2, radius*2), math.pi, 2*math.pi, 2)
        

        for i in range(11):
            angle = math.pi + (math.pi * i / 10)
            start_x = x + (radius - 10) * math.cos(angle)
            start_y = y + (radius - 10) * math.sin(angle)
            end_x = x + radius * math.cos(angle)
            end_y = y + radius * math.sin(angle)
            pygame.draw.line(self.screen, self.WHITE, (start_x, start_y), (end_x, end_y), 2)
            
            if i % 2 == 0:
                speed = i * 10
                font = pygame.font.Font(None, 24)
                text = font.render(str(speed), True, self.WHITE)
                text_x = x + (radius - 30) * math.cos(angle) - text.get_width()/2
                text_y = y + (radius - 30) * math.sin(angle) - text.get_height()/2
                self.screen.blit(text, (text_x, text_y))
        
        # Ponteiro do velocímetro
        speed = self.car.motor.speed
        speed_angle = math.pi + (math.pi * speed / 100)
        pointer_x = x + (radius - 20) * math.cos(speed_angle)
        pointer_y = y + (radius - 20) * math.sin(speed_angle)
        pygame.draw.line(self.screen, self.RED, (x, y), (pointer_x, pointer_y), 3)
        
        # Velocidade atual em texto
        font = pygame.font.Font(None, 36)
        speed_text = font.render(f"{int(speed)} km/h", True, self.WHITE)
        self.screen.blit(speed_text, (x - speed_text.get_width()/2, y + radius - 80))

    def draw_gear_indicator(self, x, y):
        font = pygame.font.Font(None, 36)
        # GEAR atual
        gear_text = font.render(f"Gear: {self.car.motor.transmission.current_gear}", True, self.WHITE)
        self.screen.blit(gear_text, (x, y))
        
        # Modo de transmissão
        mode = "Auto" if self.car.motor.transmission.is_automatic else "Manual"
        mode_text = font.render(f"Mode: {mode}", True, self.GREEN if mode == "Auto" else self.BLUE)
        self.screen.blit(mode_text, (x, y + 30))

    def draw_steering_indicator(self, x, y, width, height):
        # Barra de direção
        pygame.draw.rect(self.screen, self.GRAY, (x, y, width, height))
        
        # Indicador de posição
        center = width // 2
        pos = center + (self.car.steering.angle / self.car.steering.max_angle * center)
        pygame.draw.rect(self.screen, self.RED, (x + pos - 5, y, 10, height))
        
        # angulo em texto
        font = pygame.font.Font(None, 36)
        angle_text = font.render(f"Steering: {int(self.car.steering.angle)}°", True, self.WHITE)
        self.screen.blit(angle_text, (x, y - 30))

    def draw_car(self):

        car_length = 40
        car_width = 20
        
        # Pontos do carro
        car_points = [
            (-car_length/2, -car_width/2),
            (car_length/2, -car_width/2),
            (car_length/2, car_width/2),
            (-car_length/2, car_width/2)
        ]
        

        angle_rad = math.radians(self.car_rotation)
        rotated_points = []
        for x, y in car_points:
            rot_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            rot_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            rotated_points.append((rot_x + self.car_pos[0], rot_y + self.car_pos[1]))
        
        #  corpo do carro
        pygame.draw.polygon(self.screen, self.BLUE, rotated_points)
        
        # direction do carro
        front_x = self.car_pos[0] + car_length * math.cos(angle_rad)
        front_y = self.car_pos[1] + car_length * math.sin(angle_rad)
        pygame.draw.line(self.screen, self.RED, self.car_pos, (front_x, front_y), 2)

    def draw_controls_help(self):
        font = pygame.font.Font(None, 24)
        controls = [
            "Controls:",
            "↑ - Accelerate",
            "↓ - Brake",
            "← → - Steering",
            "T - Toggle transmission",
            "Q/A - Shift up/down (manual)",
        ]
        
        y = 10
        for text in controls:
            surface = font.render(text, True, self.WHITE)
            self.screen.blit(surface, (10, y))
            y += 25

    def run(self):
        running = True
        while running:
       
            running = self.handle_input()
            
     
            self.update_car_position()
            
 
            self.screen.fill(self.BLACK)
 
            self.draw_car()
            self.draw_speedometer(150, 650, 100)
            self.draw_gear_indicator(300, 600)
            self.draw_steering_indicator(500, 650, 200, 20)
            self.draw_controls_help()
            
     
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = JetCarGame()
    game.run()