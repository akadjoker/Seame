import smbus2
import time

class MotorFinder:
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        self.pca_addresses = []
        self.found_motors = {}
        
    def find_pca9685(self):
        """Encontra todos PCA9685 no bus I2C"""
        for addr in range(0x40, 0x48):
            try:
                self.bus.read_byte_data(addr, 0x00)
                self.pca_addresses.append(addr)
                print(f"PCA9685 encontrado: {hex(addr)}")
            except:
                pass

    def test_channel(self, addr, channel, value):
        """Testa um canal específico"""
        try:
            # Registradores para o canal
            led_on_l = 0x06 + 4 * channel
            led_on_h = 0x07 + 4 * channel
            led_off_l = 0x08 + 4 * channel
            led_off_h = 0x09 + 4 * channel
            
            # Define PWM
            self.bus.write_byte_data(addr, led_on_l, 0)
            self.bus.write_byte_data(addr, led_on_h, 0)
            self.bus.write_byte_data(addr, led_off_l, value & 0xFF)
            self.bus.write_byte_data(addr, led_off_h, value >> 8)
        except Exception as e:
            print(f"Erro no canal {channel}: {e}")

    def test_for_motors(self):
        for addr in self.pca_addresses:
            print(f"\nTestando PCA9685 em {hex(addr)}")
            
            # Testa cada canal
            for channel in range(16):
                # Reset do canal
                self.test_channel(addr, channel, 0)
                time.sleep(0.1)
                
                # Teste Forward
                print(f"Testando canal {channel} -> Forward")
                self.test_channel(addr, channel, 4095)  # Full ON
                time.sleep(0.5)  # Tempo para observar movimento
                self.test_channel(addr, channel, 0)     # OFF
                time.sleep(0.5)  # Pequena pausa entre testes

    def run(self):
        """Executa o processo de encontrar os motores"""
        print("Iniciando busca por motores DC...")
        
        # Primeiro encontra os PCA9685
        self.find_pca9685()
        
        if not self.pca_addresses:
            print("Nenhum PCA9685 encontrado!")
            return
            
        try:
            while True:
                self.test_for_motors()
                print("\nReiniciando testes...")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nTeste interrompido!")
            # Desliga todos os canais
            for addr in self.pca_addresses:
                for channel in range(16):
                    self.test_channel(addr, channel, 0)

if __name__ == "__main__":
    finder = MotorFinder()
    print(" Ctrl+C para sair")
    finder.run()