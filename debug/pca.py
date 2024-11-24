from smbus2 import SMBus
import time


PCA9685_ADDR = 0x40  # Endereço padrão do PCA9685, quantos PCA9685 tem no sistema

# Registradores do PCA9685
MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06
LED0_ON_H = 0x07
LED0_OFF_L = 0x08
LED0_OFF_H = 0x09

class MotorDriver:
    def __init__(self, bus_number=1):
        self.bus = SMBus(bus_number)
        self.setup_pca9685()

    def setup_pca9685(self):
        self.bus.write_byte_data(PCA9685_ADDR, MODE1, 0x00)
        # Configura frequência PWM
        self.set_pwm_freq(1000)

    def set_pwm_freq(self, freq):
        """Define a frequência PWM"""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        prescale = int(prescaleval + 0.5)
        
        oldmode = self.bus.read_byte_data(PCA9685_ADDR, MODE1)
        newmode = (oldmode & 0x7F) | 0x10
        self.bus.write_byte_data(PCA9685_ADDR, MODE1, newmode)
        self.bus.write_byte_data(PCA9685_ADDR, PRESCALE, prescale)
        self.bus.write_byte_data(PCA9685_ADDR, MODE1, oldmode)
        time.sleep(0.005)
        self.bus.write_byte_data(PCA9685_ADDR, MODE1, oldmode | 0x80)

    def set_pwm(self, channel, value):
        """Define o valor PWM para um canal"""
        value = min(4095, max(0, value))  # 12-bit (0-4095)
        self.bus.write_byte_data(PCA9685_ADDR, LED0_ON_L + 4 * channel, 0)
        self.bus.write_byte_data(PCA9685_ADDR, LED0_ON_H + 4 * channel, 0)
        self.bus.write_byte_data(PCA9685_ADDR, LED0_OFF_L + 4 * channel, value & 0xFF)
        self.bus.write_byte_data(PCA9685_ADDR, LED0_OFF_H + 4 * channel, value >> 8)

    def set_motor(self, motor_num, speed):
        """
        Controla um motor DC
        motor_num: 1 ou 2 para selecionar o motor
        speed: -100 a 100 (negativo para trás, positivo para frente)
        """
        # Mapeia -100 a 100 para 0 a 4095
        pwm_value = abs(speed) * 40.95  # 4095/100
        
        if motor_num == 1:
            if speed >= 0:
                # Frente
                self.set_pwm(0, pwm_value)  # IN1
                self.set_pwm(1, 0)          # IN2
            else:
                # Trás
                self.set_pwm(0, 0)          # IN1
                self.set_pwm(1, pwm_value)  # IN2
        elif motor_num == 2:
            if speed >= 0:
                # Frente
                self.set_pwm(2, pwm_value)  # IN1
                self.set_pwm(3, 0)          # IN2
            else:
                # Trás
                self.set_pwm(2, 0)          # IN1
                self.set_pwm(3, pwm_value)  # IN2


if __name__ == "__main__":
    motor = MotorDriver()
    
    try:
        print("Motor 1 frente")
        motor.set_motor(1, 50)  # Motor 1 a 50% para frente
        time.sleep(2)
        
        print("Motor 1 trás")
        motor.set_motor(1, -50)  # Motor 1 a 50% para trás
        time.sleep(2)
        
        print("Parando")
        motor.set_motor(1, 0)   # Para o motor
        
    except KeyboardInterrupt:
        print("Programa interrompido")
        motor.set_motor(1, 0)
        motor.set_motor(2, 0)