import smbus2
import time

#Raspberry Pi -> I2C -> PCA9685 -> PWM -> DRV8870 -> Motor DC

class PCA9685ChannelScanner:
    def __init__(self, address=0x40):
        self.bus = smbus2.SMBus(1)
        self.address = address

    def set_pwm(self, channel, value):
        """Define PWM para um canal (0-4095)"""
        try:
            # Registradores para cada canal
            led_on_l = 0x06 + 4 * channel
            led_on_h = 0x07 + 4 * channel
            led_off_l = 0x08 + 4 * channel
            led_off_h = 0x09 + 4 * channel
            
            self.bus.write_byte_data(self.address, led_on_l, 0)
            self.bus.write_byte_data(self.address, led_on_h, 0)
            self.bus.write_byte_data(self.address, led_off_l, value & 0xFF)
            self.bus.write_byte_data(self.address, led_off_h, value >> 8)
            
        except Exception as e:
            print(f"Erro no canal {channel}")

    def scan_channels(self):
        try:
            while True:
                print("\nIniciando scan de canais...")
                
                for channel in range(16):
                    print(f"\nTestando canal {channel}")
                    
                    # Teste HIGH
                    print(f"Canal {channel} -> HIGH")
                    self.set_pwm(channel, 4095)
                    time.sleep(1)
                    
                    # Teste LOW
                    print(f"Canal {channel} -> LOW")
                    self.set_pwm(channel, 0)
                    time.sleep(0.5)
                    
                    # Teste PWM gradual
                    print(f"Canal {channel} -> PWM Gradual")
                    for pwm in range(0, 4096, 500):
                        self.set_pwm(channel, pwm)
                        time.sleep(0.1)
                    self.set_pwm(channel, 0)
                    time.sleep(0.5)
                    
                print("\nScan completo. Reiniciando...")
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nScan interrompido!")
            # limpamos todos os canais
            for ch in range(16):
                self.set_pwm(ch, 0)

if __name__ == "__main__":
    print("Scanner  de canais PCA9685")
    print("Ctrl+C para parar")
    scanner = PCA9685ChannelScanner()
    scanner.scan_channels()