import smbus2
import time

class PCA9685:
    def __init__(self, i2c_bus=1, address=0x40):
        self.address = address
        self.bus = smbus2.SMBus(i2c_bus)
        self.set_pwm_freq(50)

    def set_pwm_freq(self, freq_hz):
        prescale_val = int(round(25000000.0 / (4096.0 * freq_hz)) - 1)
        old_mode = self.bus.read_byte_data(self.address, 0x00)
        new_mode = (old_mode & 0x7F) | 0x10  # sleep
        self.bus.write_byte_data(self.address, 0x00, new_mode)
        self.bus.write_byte_data(self.address, 0xFE, prescale_val)
        self.bus.write_byte_data(self.address, 0x00, old_mode)
        time.sleep(0.005)
        self.bus.write_byte_data(self.address, 0x00, old_mode | 0x80)  # restart

    def set_pwm(self, channel, on, off):
        reg_base = 0x06 + 4 * channel
        data = [
            on & 0xFF,
            (on >> 8) & 0xFF,
            off & 0xFF,
            (off >> 8) & 0xFF,
        ]
        self.bus.write_i2c_block_data(self.address, reg_base, data)

