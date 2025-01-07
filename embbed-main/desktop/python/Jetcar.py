class Steering:
    def __init__(self):
        self.angle = 0
        self.max_angle = 180
        self.steering_rate = 5  # Graus por atualização
        
    def turn_left(self):
        self.angle = max(-self.max_angle, self.angle - self.steering_rate)
        
    def turn_right(self):
        self.angle = min(self.max_angle, self.angle + self.steering_rate)
        
    def center(self):
        if self.angle > 0:
            self.angle = max(0, self.angle - self.steering_rate)
        else:
            self.angle = min(0, self.angle + self.steering_rate)

class Transmission:
    def __init__(self):
        self.is_automatic = False
        self.current_gear = 1
        self.speed = 0
        
        # Ranges para transmissão manual
        self.manual_ranges = {
            1: (0, 25),
            2: (26, 50),
            3: (51, 75),
            4: (76, 100)
        }
        
        # Pontos de mudança automática (velocidade onde muda de gear)
        self.auto_shift_points = {
            'up': {
                1: 20,    # Muda para 2ª aos 20 km/h
                2: 45,    # Muda para 3ª aos 45 km/h
                3: 70     # Muda para 4ª aos 70 km/h
            },
            'down': {
                4: 65,    # Volta para 3ª abaixo de 65 km/h
                3: 40,    # Volta para 2ª abaixo de 40 km/h
                2: 15     # Volta para 1ª abaixo de 15 km/h
            }
        }
        
        # Taxas de aceleração por andamento
        self.acceleration_rates = {
            1: 2.0,
            2: 1.5,
            3: 1.0,
            4: 0.5
        }

    def toggle_transmission_mode(self):
        """Alterna entre modo automático e manual"""
        self.is_automatic = not self.is_automatic
        return "Automatic" if self.is_automatic else "Manual"

    def update_automatic(self, speed):
        """Atualiza a gear no modo automático"""
        if speed > self.auto_shift_points['up'].get(self.current_gear, float('inf')):
            if self.current_gear < 4:
                self.current_gear += 1
        elif speed < self.auto_shift_points['down'].get(self.current_gear + 1, 0):
            if self.current_gear > 1:
                self.current_gear -= 1

    def get_acceleration_rate(self):
        """Retorna taxa de aceleração atual"""
        return self.acceleration_rates[self.current_gear]

    def get_current_range(self):
        """Retorna range de velocidade da gear atual"""
        return self.manual_ranges[self.current_gear]

class Motor:
    def __init__(self):
        self.transmission = Transmission()
        self.speed = 0
        self.throttle = 0
        
    def update(self, throttle):
        self.throttle = throttle
        
        # Calcula aceleração baseada na marcha atual
        acc = self.transmission.get_acceleration_rate() * throttle
        
        if self.transmission.is_automatic:
            # Modo automático - pode usar toda a faixa de velocidade
            self.speed = min(max(0, self.speed + acc), 100)
            self.transmission.update_automatic(self.speed)
        else:
            # Modo manual - limita à faixa da gear atual
            min_speed, max_speed = self.transmission.get_current_range()
            self.speed = min(max(min_speed, self.speed + acc), max_speed)
    
    def brake(self, brake_force):
        self.speed = max(0, self.speed - (brake_force * 2))
        if self.transmission.is_automatic:
            self.transmission.update_automatic(self.speed)

class JetCar:
    def __init__(self):
        self.motor = Motor()
        self.steering = Steering()  
        
    def toggle_transmission(self):
        mode = self.motor.transmission.toggle_transmission_mode()
        print(f"Transmission mode: {mode}")
    
    def get_state(self):
        return {
            'speed': self.motor.speed,
            'gear': self.motor.transmission.current_gear,
            'steering_angle': self.steering.angle,
            'throttle': self.motor.throttle,
            'is_automatic': self.motor.transmission.is_automatic
        }


# def create_keyboard_controller():
#     import keyboard
#     car = JetCar()
    
#     def update_loop():
#         if keyboard.is_pressed('t'):  # Toggle transmission mode
#             car.toggle_transmission()
            
#         if keyboard.is_pressed('up'):
#             car.motor.update(1.0)  # Acelerador
#         else:
#             car.motor.update(0)
            
#         if keyboard.is_pressed('down'):
#             car.motor.brake(1.0)
            
#         if keyboard.is_pressed('left'):
#             car.steering.turn_left()
#         elif keyboard.is_pressed('right'):
#             car.steering.turn_right()
#         else:
#             car.steering.center()
            
#         # Mudanças manuais só funcionam no modo manual
#         if not car.motor.transmission.is_automatic:
#             if keyboard.is_pressed('q'):  # Shift up
#                 car.motor.transmission.current_gear = min(4, car.motor.transmission.current_gear + 1)
#             if keyboard.is_pressed('a'):  # Shift down
#                 car.motor.transmission.current_gear = max(1, car.motor.transmission.current_gear - 1)
        
#         return car.get_state()
    
#     return update_loop

