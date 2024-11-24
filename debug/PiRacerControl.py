import smbus
import time
from enum import Enum

class MotorState(Enum):
    FORWARD = 1
    BACKWARD = 2
    BRAKE = 3
    COAST = 4

class PiRacerControl:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        # Endereços separados
        self.SERVO_ADDR = 0x40    # PCA9685 para servo
        self.MOTOR_ADDR = 0x41    # PCA9685 para motores DC
        
        # Canal do servo (geralmente 0 no PCA9685 do servo)
        self.SERVO_CHANNEL = 0
        
        # Canais dos motores DC no PCA9685 dos motores
        self.MOTOR1 = {'in1': 0, 'in2': 1}
        self.MOTOR2 = {'in1': 2, 'in2': 3}
        
        # Inicializa os PCA9685s
        self.setup_pca9685(self.SERVO_ADDR)
        self.setup_pca9685(self.MOTOR_ADDR)
    
    def setup_pca9685(self, address):
        """Configura um PCA9685"""
        try:
            # Reset
            self.bus.write_byte_data(address, 0x00, 0x00)
            time.sleep(0.1)
            # Configura PRE_SCALE para ~50Hz
            self.bus.write_byte_data(address, 0xFE, 0x1E)
            time.sleep(0.1)
            # Modo normal
            self.bus.write_byte_data(address, 0x00, 0x20)
            print(f"PCA9685 0x{address:02X} configurado")
        except Exception as e:
            print(f"Erro ao configurar PCA9685 0x{address:02X}: {e}")
    
    def set_servo(self, angle):
        """
        Controla o servo (ângulo de 0-180)
        """
        try:
            # Converte ângulo para pulso PWM (ajuste estes valores conforme seu servo)
            pulse_min = 150  # Pulso para 0 graus
            pulse_max = 600  # Pulso para 180 graus
            pulse = int(pulse_min + (pulse_max - pulse_min) * angle / 180)
            
            # Define PWM no canal do servo
            channel = self.SERVO_CHANNEL
            self.bus.write_word_data(self.SERVO_ADDR, 0x06 + 4 * channel, 0)
            self.bus.write_word_data(self.SERVO_ADDR, 0x08 + 4 * channel, pulse)
            print(f"Servo movido para {angle} graus")
        except Exception as e:
            print(f"Erro ao controlar servo: {e}")
    
    def set_motor(self, motor_num, state: MotorState, speed=100):
        """
        Controla um motor DC
        motor_num: 1 ou 2
        state: FORWARD, BACKWARD, BRAKE ou COAST
        speed: 0-100 (porcentagem)
        """
        try:
            # Seleciona os canais do motor
            channels = self.MOTOR1 if motor_num == 1 else self.MOTOR2
            
            # Converte velocidade para valor PWM
            pwm_value = int((speed * 4095) / 100)
            
            # Define os sinais IN1/IN2 baseado no estado
            if state == MotorState.FORWARD:
                # Frente: IN1=0, IN2=PWM
                self.bus.write_word_data(self.MOTOR_ADDR, 0x06 + 4 * channels['in1'], 0)
                self.bus.write_word_data(self.MOTOR_ADDR, 0x06 + 4 * channels['in2'], pwm_value)
                print(f"Motor {motor_num}: Frente {speed}%")
                
            elif state == MotorState.BACKWARD:
                # Trás: IN1=PWM, IN2=0
                self.bus.write_word_data(self.MOTOR_ADDR, 0x06 + 4 * channels['in1'], pwm_value)
                self.bus.write_word_data(self.MOTOR_ADDR, 0x06 + 4 * channels['in2'], 0)
                print(f"Motor {motor_num}: Trás {speed}%")
                
            elif state == MotorState.BRAKE:
                # Freio: IN1=HIGH, IN2=HIGH
                self.bus.write_word_data(self.MOTOR_ADDR, 0x06 + 4 * channels['in1'], 4095)
                self.bus.write_word_data(self.MOTOR_ADDR, 0x06 + 4 * channels['in2'], 4095)
                print(f"Motor {motor_num}: Freio ativo")
                
            elif state == MotorState.COAST:
                # Coast: IN1=LOW, IN2=LOW
                self.bus.write_word_data(self.MOTOR_ADDR, 0x06 + 4 * channels['in1'], 0)
                self.bus.write_word_data(self.MOTOR_ADDR, 0x06 + 4 * channels['in2'], 0)
                print(f"Motor {motor_num}: Coast (livre)")
                
        except Exception as e:
            print(f"Erro ao controlar motor {motor_num}: {e}")

    def test_all(self):
        """Testa todos os componentes"""
        try:
            print("\n=== Teste do Servo ===")
            angles = [0, 90, 180, 90, 0]
            for angle in angles:
                print(f"Movendo servo para {angle} graus")
                self.set_servo(angle)
                time.sleep(1)
            
            print("\n=== Teste dos Motores DC ===")
            for motor in [1, 2]:
                print(f"\nTestando Motor {motor}")
                
                # Teste frente
                print("Frente 50%")
                self.set_motor(motor, MotorState.FORWARD, 50)
                time.sleep(2)
                
                # Teste freio
                print("Freio")
                self.set_motor(motor, MotorState.BRAKE)
                time.sleep(1)
                
                # Teste trás
                print("Trás 50%")
                self.set_motor(motor, MotorState.BACKWARD, 50)
                time.sleep(2)
                
                # Teste coast
                print("Coast")
                self.set_motor(motor, MotorState.COAST)
                time.sleep(1)
            
        except Exception as e:
            print(f"Erro no teste: {e}")

    def interactive_control(self):
        """Controle interativo"""
        while True:
            print("\n=== Controle PiRacer ===")
            print("1. Controlar Servo")
            print("2. Controlar Motor 1")
            print("3. Controlar Motor 2")
            print("4. Testar Tudo")
            print("5. Sair")
            
            try:
                choice = int(input("\nEscolha uma opção: "))
                
                if choice == 1:
                    angle = int(input("Ângulo (0-180): "))
                    self.set_servo(angle)
                    
                elif choice in [2, 3]:
                    motor_num = choice - 1
                    print("\nEstados:")
                    print("1. Frente")
                    print("2. Trás")
                    print("3. Freio")
                    print("4. Coast")
                    
                    state = int(input("Escolha o estado: "))
                    speed = int(input("Velocidade (0-100): ")) if state in [1, 2] else 0
                    
                    self.set_motor(motor_num, MotorState(state), speed)
                    
                elif choice == 4:
                    self.test_all()
                    
                elif choice == 5:
                    break
                    
            except ValueError:
                print("Entrada inválida!")
                continue

if __name__ == "__main__":
    controller = PiRacerControl()
    controller.set_servo(90)                         # Servo para 90 graus
    controller.set_motor(1, MotorState.FORWARD, 50)  # Motor 1 para frente a 50%

    #controller.interactive_control()