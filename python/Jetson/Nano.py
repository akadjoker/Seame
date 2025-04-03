import math
import time
from abc import abstractmethod
from smbus2 import SMBus
from pca9685 import PCA9685   
from ina219 import INA219
from ssd1306 import SSD1306


class NanoBase:
    PWM_RESOLUTION = 12
    PWM_MAX_RAW_VALUE = int(math.pow(2, PWM_RESOLUTION)) - 1

    PWM_FREQ_50HZ = 50.0
    PWM_WAVELENGTH_50HZ = 1.0 / PWM_FREQ_50HZ

    @classmethod
    def _set_channel_active_time(cls, time_s: float, pwm_controller: PCA9685, channel: int) -> None:
        raw_value = int(cls.PWM_MAX_RAW_VALUE * (time_s / cls.PWM_WAVELENGTH_50HZ))
        pwm_controller.set_pwm(channel, 0, raw_value)

    @classmethod
    def _get_50hz_duty_cycle_from_percent(cls, value: float) -> float:
        return 0.0015 + (value * 0.0005)  # ±0.5ms em torno dos 1.5ms

    def __init__(self) -> None:
        self.bus = SMBus(1)

    def _warmup(self) -> None:
        self.set_steering_percent(0.0)
        self.set_throttle_percent(0.0)
        time.sleep(2.0)

    @abstractmethod
    def set_steering_percent(self, value: float) -> None:
        pass

    @abstractmethod
    def set_throttle_percent(self, value: float) -> None:
        pass


class Nano(NanoBase):
    PWM_STEERING_CHANNEL = 0
    PWM_LEFT_IN1 = 5
    PWM_LEFT_IN2 = 6
    PWM_LEFT_PWM = 7
    PWM_RIGHT_IN1 = 1
    PWM_RIGHT_IN2 = 2
    PWM_RIGHT_PWM = 0

    def __init__(self):
        super().__init__()

        # Controlador da direção
        self.steering_pwm = PCA9685(i2c_bus=self.i2c_bus, address=0x40)
        self.steering_pwm.set_pwm_freq(self.PWM_FREQ_50HZ)

        # Controlador dos motores (ponte H)
        self.motor_pwm = PCA9685(i2c_bus=self.i2c_bus, address=0x60)
        self.motor_pwm.set_pwm_freq(self.PWM_FREQ_50HZ)

        # Monitor ecrã e bateria
        self.battery = INA219(i2c_bus=self.i2c_bus, address=0x41)
        self.display = SSD1306(i2c_bus=self.i2c_bus, address=0x3C)

        self._warmup()

    def set_steering_percent(self, value: float):
        pulse = self._get_50hz_duty_cycle_from_percent(-value)
        self._set_channel_active_time(pulse, self.steering_pwm, self.PWM_STEERING_CHANNEL)

    def set_throttle_percent(self, value: float):
        raw = int(self.PWM_MAX_RAW_VALUE * abs(value))

        if value > 0:
            # Frente
            self.motor_pwm.set_pwm(self.PWM_LEFT_IN1, 0, self.PWM_MAX_RAW_VALUE)
            self.motor_pwm.set_pwm(self.PWM_LEFT_IN2, 0, 0)
            self.motor_pwm.set_pwm(self.PWM_RIGHT_IN1, 0, 0)
            self.motor_pwm.set_pwm(self.PWM_RIGHT_IN2, 0, self.PWM_MAX_RAW_VALUE)
        else:
            # Trás
            self.motor_pwm.set_pwm(self.PWM_LEFT_IN1, 0, 0)
            self.motor_pwm.set_pwm(self.PWM_LEFT_IN2, 0, self.PWM_MAX_RAW_VALUE)
            self.motor_pwm.set_pwm(self.PWM_RIGHT_IN1, 0, self.PWM_MAX_RAW_VALUE)
            self.motor_pwm.set_pwm(self.PWM_RIGHT_IN2, 0, 0)

        # PWM para os motores (intensidade da velocidade)
        self.motor_pwm.set_pwm(self.PWM_LEFT_PWM, 0, raw)
        self.motor_pwm.set_pwm(self.PWM_RIGHT_PWM, 0, raw)

    def get_battery_voltage(self):
        return self.battery.bus_voltage + self.battery.shunt_voltage

    def get_battery_current(self):
        return self.battery.current

    def get_power_consumption(self):
        return self.battery.power

    def get_display(self):
        return self.display



def main():
    nano = NanoStandard()

    display = nano.get_display()

    try:
        while True:
            # Medições
            voltage = nano.get_battery_voltage()
            current = nano.get_battery_current()
            power = nano.get_power_consumption()

            # Atualiza display OLED
            display.clear()
            display.text(f"V: {voltage:.2f} V", 0, 0)
            display.text(f"I: {current:.0f} mA", 0, 10)
            display.text(f"P: {power:.2f} W", 0, 20)
            display.show()

            # Movimento de direção (esq → dir)
            for angle in [-1.0, -0.5, 0.0, 0.5, 1.0]:
                nano.set_steering_percent(angle)
                time.sleep(0.3)

 
            nano.set_throttle_percent(0.3)
            time.sleep(1.5)

      
            nano.set_throttle_percent(0.0)
            time.sleep(0.5)

 
            nano.set_throttle_percent(-0.3)
            time.sleep(1.5)

 
            nano.set_throttle_percent(0.0)
            time.sleep(2.0)

    except KeyboardInterrupt:
        nano.set_throttle_percent(0.0)
        nano.set_steering_percent(0.0)
        print("Parado com CTRL+C")

if __name__ == "__main__":
    main()

