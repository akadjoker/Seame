import smbus
import time
from enum import Enum

class MotorDirection(Enum):
    FORWARD = 1
    BACKWARD = 2
    BRAKE = 3
    RELEASE = 4

class PiRacerMotorControl:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.MOTOR_ADDR = 0x41  # Endereço do PCA9685 dos motores ??? a ver
        
        # Mapeamento dos canais para cada motor
        self.MOTOR1_CHANNELS = {'in1': 0, 'in2': 1}  # Motor 1: IN1=Canal 0, IN2=Canal 1
        self.MOTOR2_CHANNELS = {'in1': 2, 'in2': 3}  # Motor 2: IN1=Canal 2, IN2=Canal 3
        
        self.setup_pca9685()
    
    def setup_pca9685(self):
        """Configura o PCA9685"""
        try:
            # Reset
            self.bus.write_byte_data(self.MOTOR_ADDR, 0x00, 0x00)
            time.sleep(0.1)
            # Configura frequência (~50Hz) a ver
            self.bus.write_byte_data(self.MOTOR_ADDR, 0xFE, 0x1E)
            time.sleep(0.1)
            # Modo normal
            self.bus.write_byte_data(self.MOTOR_ADDR, 0x00, 0x20)
            print("PCA9685 configurado com sucesso")
        except Exception as e:
            print(f"Erro na configuração do PCA9685: {e}")

    def set_pwm(self, channel, value):
        """Define o valor PWM para um canal"""
        try:
            reg_offset = 4 * channel
            self.bus.write_word_data(self.MOTOR_ADDR, 0x06 + reg_offset, 0)
            self.bus.write_word_data(self.MOTOR_ADDR, 0x08 + reg_offset, value)
        except Exception as e:
            print(f"Erro ao definir PWM no canal {channel}: {e}")

    def control_motor(self, motor_num, direction, speed=100):
        """
        Controla um motor específico
        motor_num: 1 ou 2
        direction: MotorDirection.FORWARD, BACKWARD, BRAKE, ou RELEASE
        speed: 0-100 (porcentagem da velocidade máxima)
        """
        #  canais corretos para o motor
        channels = self.MOTOR1_CHANNELS if motor_num == 1 else self.MOTOR2_CHANNELS
        
        # Converte velocidade de porcentagem (0-100) para valor PWM (0-4095)
        pwm_value = int((speed * 4095) / 100)
        
        # Configura os sinais IN1 e IN2 baseado na direção
        if direction == MotorDirection.FORWARD:
            self.set_pwm(channels['in1'], 0)        # IN1 = LOW
            self.set_pwm(channels['in2'], pwm_value) # IN2 = PWM
            print(f"Motor {motor_num}: Frente {speed}%")
            
        elif direction == MotorDirection.BACKWARD:
            self.set_pwm(channels['in1'], pwm_value) # IN1 = PWM
            self.set_pwm(channels['in2'], 0)         # IN2 = LOW
            print(f"Motor {motor_num}: Trás {speed}%")
            
        elif direction == MotorDirection.BRAKE:
            self.set_pwm(channels['in1'], 4095)      # IN1 = HIGH
            self.set_pwm(channels['in2'], 4095)      # IN2 = HIGH
            print(f"Motor {motor_num}: Freio")
            
        elif direction == MotorDirection.RELEASE:
            self.set_pwm(channels['in1'], 0)         # IN1 = LOW
            self.set_pwm(channels['in2'], 0)         # IN2 = LOW
            print(f"Motor {motor_num}: Parado")

    def test_sequence(self):
        """Executa uma sequência de teste em ambos os motores"""
        try:
            print("\nIniciando sequência de teste...")
            
            # Testa cada motor individualmente
            for motor in [1, 2]:
                print(f"\nTestando Motor {motor}")
                
                print("1. Teste movimento para frente")
                self.control_motor(motor, MotorDirection.FORWARD, 50)
                time.sleep(2)
                
                print("2. Teste breake (RELEASE)")
                self.control_motor(motor, MotorDirection.RELEASE)
                time.sleep(1)
                
                print("3. Teste movimento para trás")
                self.control_motor(motor, MotorDirection.BACKWARD, 50)
                time.sleep(2)
                
            
                print("4. Teste stop")
                self.control_motor(motor, MotorDirection.BRAKE)
                time.sleep(1)
                
                print("5. Teste release (release) ")
                self.control_motor(motor, MotorDirection.RELEASE)
                
            print("\nSequência de teste concluída")
            
        except Exception as e:
            print(f"Erro durante o teste: {e}")

    def interactive_control(self):
        """Controle interativo dos motores"""
        print("\n=== Controle Interativo dos Motores ===")
        print("Comandos disponíveis:")
        print("1. Controlar Motor 1")
        print("2. Controlar Motor 2")
        print("3. Testar sequência")
        print("4. Sair")
        
        while True:
            try:
                choice = int(input("\nEscolha uma opção: "))
                
                if choice in [1, 2]:
                    print("1. Frente")
                    print("2. Trás")
                    print("3. Stop")
                    print("4. Livre")
                    
                    dir_choice = int(input("Escolhe a direção: "))
                    
                    if dir_choice in [1, 2]:
                        speed = int(input("Velocidade (0-100%): "))
                    else:
                        speed = 0
                    
                    direction = {
                        1: MotorDirection.FORWARD,
                        2: MotorDirection.BACKWARD,
                        3: MotorDirection.BRAKE,
                        4: MotorDirection.RELEASE
                    }.get(dir_choice)
                    
                    if direction:
                        self.control_motor(choice, direction, speed)
                
                elif choice == 3:
                    self.test_sequence()
                
                elif choice == 4:
                    break
                    
            except ValueError:
                print("Entrada inválida!")
                continue
    def simpes():
        controller = PiRacerMotorControl()
        # controle direto
        controller.control_motor(1, MotorDirection.FORWARD, 50)  # Motor 1, frente, 50% velocidade
        time.sleep(5)
        controller.control_motor(2, MotorDirection.BACKWARD, 75) # Motor 2, trás, 75% velocidade
        time.sleep(5)


if __name__ == "__main__":
    controller = PiRacerMotorControl()
    controller.interactive_control()