import smbus2
import time

class PCA9685:
    # Registradores do PCA9685
    MODE1              = 0x00
    MODE2              = 0x01
    SUBADR1           = 0x02
    SUBADR2           = 0x03
    SUBADR3           = 0x04
    PRESCALE          = 0xFE
    LED0_ON_L         = 0x06
    LED0_ON_H         = 0x07
    LED0_OFF_L        = 0x08
    LED0_OFF_H        = 0x09
    ALL_LED_ON_L      = 0xFA
    ALL_LED_ON_H      = 0xFB
    ALL_LED_OFF_L     = 0xFC
    ALL_LED_OFF_H     = 0xFD

    def __init__(self, address=0x40, bus_number=1):
        self.address = address
        self.bus = smbus2.SMBus(bus_number)
        
        # Inicializa o PCA9685
        self.bus.write_byte_data(self.address, self.MODE1, 0x00)
        time.sleep(0.005)  # Aguarda 5ms para estabilizar
        
        # Define frequência para 50Hz OBS: bom para servos
        self.set_pwm_freq(50)
        time.sleep(0.005)

    def set_pwm_freq(self, freq):
        """Define a frequência PWM"""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        prescale = int(prescaleval + 0.5)
        
        oldmode = self.bus.read_byte_data(self.address, self.MODE1)
        newmode = (oldmode & 0x7F) | 0x10    # sleep
        self.bus.write_byte_data(self.address, self.MODE1, newmode)  # vai para sleep
        self.bus.write_byte_data(self.address, self.PRESCALE, prescale)
        self.bus.write_byte_data(self.address, self.MODE1, oldmode)
        time.sleep(0.005)
        self.bus.write_byte_data(self.address, self.MODE1, oldmode | 0x80)

    def set_pwm(self, channel, on, off):
        """Define o PWM para um canal"""
        on = int(on)
        off = int(off)
        self.bus.write_byte_data(self.address, self.LED0_ON_L + 4 * channel, on & 0xFF)
        self.bus.write_byte_data(self.address, self.LED0_ON_H + 4 * channel, on >> 8)
        self.bus.write_byte_data(self.address, self.LED0_OFF_L + 4 * channel, off & 0xFF)
        self.bus.write_byte_data(self.address, self.LED0_OFF_H + 4 * channel, off >> 8)

    def set_duty_cycle(self, channel, duty_cycle):
        """Define duty cycle (0-100)"""
        value = int(duty_cycle * 4095 / 100)  # Converte para 12-bit
        self.set_pwm(channel, 0, value)

    def set_servo_angle(self, channel, angle):
        """Define ângulo do servo (0-180)"""
        # Converte ângulo para pulso (cerca de 150-600 para 0-180 graus)
        pulse = int(150 + (angle * 450 / 180))
        self.set_pwm(channel, 0, pulse)

class PiRacer:
    def __init__(self, pca_address=0x40):
        self.pca = PCA9685(address=pca_address)
        
        # Canais para motor DC (por saber)
        self.MOTOR1_IN1 = 0  # LED0
        self.MOTOR1_IN2 = 1  # LED1
        self.MOTOR1_VREF = 2  # LED2
        
        # Canal para servo freio
        self.SERVO_BRAKE = 15  # LED15
        
        # Inicializa tudo parado
        self.stop_motors()
        self.release_brake()

    def set_motor(self, speed):
        """
        Controla o motor DC
        speed: -100 a 100 (negativo para trás, positivo para frente)
        """
        if speed > 0:  # Frente
            self.pca.set_duty_cycle(self.MOTOR1_IN1, 100)  # HIGH
            self.pca.set_duty_cycle(self.MOTOR1_IN2, 0)    # LOW
            self.pca.set_duty_cycle(self.MOTOR1_VREF, abs(speed))
        elif speed < 0:  # Trás
            self.pca.set_duty_cycle(self.MOTOR1_IN1, 0)    # LOW
            self.pca.set_duty_cycle(self.MOTOR1_IN2, 100)  # HIGH
            self.pca.set_duty_cycle(self.MOTOR1_VREF, abs(speed))
        else:  # Parado
            self.stop_motors()

    def stop_motors(self):
        """Para os motores"""
        self.pca.set_duty_cycle(self.MOTOR1_IN1, 0)
        self.pca.set_duty_cycle(self.MOTOR1_IN2, 0)
        self.pca.set_duty_cycle(self.MOTOR1_VREF, 0)

    def set_brake(self, position):
        """
        Controla o servo do freio
        position: 0-180 graus
        """
        self.pca.set_servo_angle(self.SERVO_BRAKE, position)

    def apply_brake(self):
        """Aplica freio totalmente"""
        self.set_brake(180)

    def release_brake(self):
        """Solta o freio totalmente"""
        self.set_brake(0)


if __name__ == "__main__":
    try:
        car = PiRacer()
        
        print("Testando motor e freio...")
        

        print("Aplicando travao")
        car.apply_brake()
        time.sleep(1)
        
        print("Soltando travao")
        car.release_brake()
        time.sleep(1)
        

        print("Motor para frente")
        car.set_motor(50)  # 50% velocidade para frente
        time.sleep(2)
        
        print("Parando")
        car.stop_motors()
        time.sleep(1)
        
        print("Motor para trás")
        car.set_motor(-50)  # 50% velocidade para trás
        time.sleep(2)
        
        print("Parando")
        car.stop_motors()
        
    except KeyboardInterrupt:
        print("\nPrograma interrompido ")
        car.stop_motors()
        car.release_brake()