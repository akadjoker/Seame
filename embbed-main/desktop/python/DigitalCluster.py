import pygame
import psutil
import math

class DigitalCluster:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 480
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Digital Cluster")
        
        # Cores
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        
        # Fontes
        self.big_font = pygame.font.Font(None, 74)
        self.medium_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        # Estado inicial
        self.speed = 0
        self.use_km = True
        self.battery = 100
        self.wheel_angle = 0
        self.running = True

    def draw_speed(self):
        speed_unit = "km/h" if self.use_km else "mph"
        speed_value = self.speed if self.use_km else self.speed * 0.621371
        speed_text = f"{speed_value:.1f} {speed_unit}"
        speed_surface = self.big_font.render(speed_text, True, self.WHITE)
        self.screen.blit(speed_surface, (self.width//2 - speed_surface.get_width()//2, 50))

    def draw_battery(self):
        battery_text = f"Bateria: {self.battery}%"
        bat_surface = self.medium_font.render(battery_text, True, self.WHITE)
        self.screen.blit(bat_surface, (50, 150))
        
        # Desenha barra de bateria
        pygame.draw.rect(self.screen, self.WHITE, (50, 200, 200, 30), 2)
        pygame.draw.rect(self.screen, self.BLUE, (52, 202, 196 * self.battery/100, 26))

    def draw_wheel_direction(self):
        # Desenha indicador de direção das rodas
        center_x = self.width - 150
        center_y = 200
        radius = 50
        
        pygame.draw.circle(self.screen, self.WHITE, (center_x, center_y), radius, 2)
        end_x = center_x + radius * math.sin(math.radians(self.wheel_angle))
        end_y = center_y - radius * math.cos(math.radians(self.wheel_angle))
        pygame.draw.line(self.screen, self.RED, (center_x, center_y), (end_x, end_y), 3)

    def draw_system_stats(self):
        cpu_text = f"CPU: {psutil.cpu_percent()}%"
        mem_text = f"MEM: {psutil.virtual_memory().percent}%"
        
        cpu_surface = self.small_font.render(cpu_text, True, self.WHITE)
        mem_surface = self.small_font.render(mem_text, True, self.WHITE)
        
        self.screen.blit(cpu_surface, (50, self.height - 80))
        self.screen.blit(mem_surface, (50, self.height - 40))

    def update(self, speed, battery, wheel_angle):
        self.speed = speed
        self.battery = battery
        self.wheel_angle = wheel_angle

    def toggle_units(self):
        self.use_km = not self.use_km

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u: 
                        self.toggle_units()


            self.screen.fill(self.BLACK)
            

            self.draw_speed()
            self.draw_battery()
            self.draw_wheel_direction()
            self.draw_system_stats()
            
            pygame.display.flip()
            pygame.time.wait(100)

        pygame.quit()

if __name__ == "__main__":
    cluster = DigitalCluster()

    cluster.update(speed=60, battery=80, wheel_angle=15)
    cluster.run()