import smbus2

class INA219:
    def __init__(self, i2c_bus=1, address=0x42):
        self.bus = smbus2.SMBus(i2c_bus)
        self.address = address
        self._calibrate()

    def _calibrate(self):
        self.bus.write_word_data(self.address, 0x05, 0x2000)  # Calibration

    def _read_word(self, reg):
        value = self.bus.read_word_data(self.address, reg)
        return ((value << 8) & 0xFF00) + (value >> 8)

    @property
    def bus_voltage(self):
        return (self._read_word(0x02) >> 3) * 4.0 / 1000.0

    @property
    def shunt_voltage(self):
        return self._read_word(0x01) * 0.01  # mV

    @property
    def current(self):
        return self._read_word(0x04) * 0.1  # mA

    @property
    def power(self):
        return self._read_word(0x03) * 0.02  # W

