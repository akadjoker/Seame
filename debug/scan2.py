import smbus
import time
from typing import Dict, List, Optional

class PiRacerScanner:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        # Lista de possíveis chips e seus endereços conhecidos
        self.KNOWN_DEVICES = {
            'PCA9685': [0x40, 0x41, 0x42, 0x43],
            'SSD1306': [0x3C, 0x3D],
            'INA219': [0x40, 0x41, 0x42, 0x43, 0x44, 0x45]
        }
        
        # Registradores importantes
        self.PCA9685_MODE1 = 0x00
        self.PCA9685_PRESCALE = 0xFE
        self.INA219_CONFIG = 0x00
        self.SSD1306_COMMAND = 0x00
        
    def identify_device(self, address: int) -> Optional[str]:
        """
        Tenta identificar qual chip está em um determinado endereço
        """
        try:
            # Tenta identificar PCA9685
            try:
                self.bus.write_byte_data(address, self.PCA9685_MODE1, 0x00)
                mode1 = self.bus.read_byte_data(address, self.PCA9685_MODE1)
                if mode1 in [0x00, 0x20, 0x30]:  # Valores típicos do PCA9685
                    return 'PCA9685'
            except:
                pass

            # Tenta identificar INA219
            try:
                config = self.bus.read_word_data(address, self.INA219_CONFIG)
                if config & 0x399F:  # Máscara para configuração típica do INA219
                    return 'INA219'
            except:
                pass

            # Tenta identificar SSD1306
            try:
                self.bus.write_byte_data(address, self.SSD1306_COMMAND, 0xAE)
                return 'SSD1306'
            except:
                pass

            return 'Unknown'
        except:
            return None

    def scan_i2c_bus(self) -> Dict[int, str]:
        """
        Varre o barramento I2C e identifica todos os dispositivos
        """
        print("\n=== Iniciando varredura do barramento I2C ===")
        found_devices = {}
        
        for addr in range(0x00, 0x7F):
            try:
                self.bus.read_byte(addr)
                device_type = self.identify_device(addr)
                found_devices[addr] = device_type
                print(f"Endereço 0x{addr:02X}: {device_type or 'Desconhecido'}")
            except:
                continue
                
        return found_devices

    def test_pca9685_channels(self, address: int) -> List[bool]:
        """
        Testa todos os canais de um PCA9685 para identificar quais estão conectados a motores
        """
        print(f"\n=== Testando canais do PCA9685 no endereço 0x{address:02X} ===")
        active_channels = []
        
        try:
            # Configura o PCA9685
            self.bus.write_byte_data(address, 0x00, 0x00)  # Reset
            time.sleep(0.1)
            self.bus.write_byte_data(address, 0xFE, 0x1E)  # ~50Hz
            time.sleep(0.1)
            self.bus.write_byte_data(address, 0x00, 0x20)  # Auto-increment on
            
            # Testa cada canal
            for channel in range(16):
                print(f"\nTestando canal {channel}:")
                base_reg = 0x06 + (channel * 4)
                
                # Teste 1: PWM baixo
                print(f"- Teste LOW")
                self.bus.write_word_data(address, base_reg, 0x0000)
                time.sleep(0.2)
                
                # Teste 2: PWM médio
                print(f"- Teste 50% PWM")
                self.bus.write_word_data(address, base_reg, 0x0800)
                time.sleep(0.5)
                
                # Teste 3: PWM alto
                print(f"- Teste HIGH")
                self.bus.write_word_data(address, base_reg, 0x0FFF)
                time.sleep(0.2)
                
                # Reset canal
                self.bus.write_word_data(address, base_reg, 0x0000)
                
                resposta = input(f"Canal {channel} mostrou atividade? (s/n): ")
                if resposta.lower() == 's':
                    active_channels.append(channel)
                
        except Exception as e:
            print(f"Erro ao testar canais: {e}")
        
        return active_channels

    def find_motor_channels(self):
        """
        Procura e identifica os canais dos motores DC
        """
        print("\n=== Procurando canais dos motores DC ===")
        
        # Primeiro encontra todos os dispositivos
        devices = self.scan_i2c_bus()
        
        # Procura por PCA9685s
        pca9685_addrs = [addr for addr, dev_type in devices.items() if dev_type == 'PCA9685']
        
        motor_channels = {}
        for addr in pca9685_addrs:
            print(f"\nTestando PCA9685 no endereço 0x{addr:02X}")
            print("Vamos testar cada canal para identificar os motores.")
            print("Observe o comportamento dos motores durante o teste.")
            
            active_channels = self.test_pca9685_channels(addr)
            if active_channels:
                motor_channels[addr] = active_channels
                print(f"\nCanais ativos encontrados no PCA9685 0x{addr:02X}: {active_channels}")
        
        return motor_channels

    def interactive_test(self):
        """
        Interface interativa para teste
        """
        while True:
            print("\n=== Menu de Teste PiRacer ===")
            print("1. Varrer barramento I2C")
            print("2. Procurar canais dos motores")
            print("3. Testar endereço específico")
            print("4. Sair")
            
            choice = input("\nEscolha uma opção: ")
            
            if choice == '1':
                self.scan_i2c_bus()
            
            elif choice == '2':
                channels = self.find_motor_channels()
                print("\nResumo dos canais encontrados:")
                for addr, chans in channels.items():
                    print(f"PCA9685 0x{addr:02X}: {chans}")
            
            elif choice == '3':
                try:
                    addr = int(input("Digite o endereço (ex: 64 para 0x40): "), 16)
                    self.test_pca9685_channels(addr)
                except ValueError:
                    print("Endereço inválido!")
            
            elif choice == '4':
                break

if __name__ == "__main__":
    scanner = PiRacerScanner()
    scanner.interactive_test()