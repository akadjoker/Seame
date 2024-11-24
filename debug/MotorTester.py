import smbus
import time
from typing import Dict, List

class MotorTester:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        # Lista de possíveis endereços do PCA9685 para testar , script para procurar
        self.possible_pca_addresses = [0x40, 0x41, 0x42, 0x43, 0x44, 0x45]
        
    def find_pca9685(self) -> List[int]:
        """
        Encontra todos os PCA9685 conectados
        """
        found_addresses = []
        for addr in self.possible_pca_addresses:
            try:
                # Tenta ler o registrador MODE1
                self.bus.read_byte_data(addr, 0x00)
                found_addresses.append(addr)
                print(f"PCA9685 encontrado no endereço 0x{addr:02X}")
            except Exception as e:
                pass
        return found_addresses

    def setup_pca9685(self, address: int):
        """
        Configura o PCA9685 com configurações detalhadas
        """
        try:
            # Reset
            self.bus.write_byte_data(address, 0x00, 0x00)
            time.sleep(0.1)
            
            # Modo Sleep para configurar PRE_SCALE
            self.bus.write_byte_data(address, 0x00, 0x10)
            time.sleep(0.1)
            
            # Set PRE_SCALE para ~50Hz (valor 0x1E)
            self.bus.write_byte_data(address, 0xFE, 0x1E)
            time.sleep(0.1)
            
            # Modo normal com auto-increment
            self.bus.write_byte_data(address, 0x00, 0x20)
            time.sleep(0.1)
            
            print(f"PCA9685 0x{address:02X} configurado com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao configurar PCA9685 0x{address:02X}: {e}")
            return False

    def test_single_motor_channel(self, address: int, channel: int, duty_cycle: int):
        """
        Testa um único canal do motor com duty cycle específico
        """
        try:
            # Registradores LED0_ON_L até LED15_ON_L são 4 bytes cada, começando em 0x06
            base_reg = 0x06 + (channel * 4)
            
            # Define quando o PWM liga (0) e desliga (duty_cycle)
            self.bus.write_byte_data(address, base_reg, 0x00)     # ON_L
            self.bus.write_byte_data(address, base_reg + 1, 0x00) # ON_H
            self.bus.write_byte_data(address, base_reg + 2, duty_cycle & 0xFF)        # OFF_L
            self.bus.write_byte_data(address, base_reg + 3, (duty_cycle >> 8) & 0xFF) # OFF_H
            
            return True
        except Exception as e:
            print(f"Erro no canal {channel}: {e}")
            return False

    def test_drv8870_detailed(self, pca_address: int):
        """
        Teste detalhado do DRV8870 com diferentes configurações
        """
        # Configurações dos motores (??? in1 e in2 no driver)
        motor_configs = {
            'motor1': {'in1': 0, 'in2': 1},  # Canais para o primeiro motor
            'motor2': {'in1': 2, 'in2': 3}   # Canais para o segundo motor
        }
        
        print(f"\nIniciando teste detalhado do DRV8870 usando PCA9685 em 0x{pca_address:02X}")
        
        for motor_name, pins in motor_configs.items():
            print(f"\nTestando {motor_name}:")
            
            # Teste de movimento para frente
            print("1. Teste movimento para frente")
            # IN1 = 0, IN2 = PWM
            self.test_single_motor_channel(pca_address, pins['in1'], 0)
            self.test_single_motor_channel(pca_address, pins['in2'], 2048)
            time.sleep(2)
            

            print("2. Teste parada")
            self.test_single_motor_channel(pca_address, pins['in1'], 0)
            self.test_single_motor_channel(pca_address, pins['in2'], 0)
            time.sleep(1)
            
            # Teste de movimento para trás
            print("3. Teste movimento para trás")
            # IN1 = PWM, IN2 = 0
            self.test_single_motor_channel(pca_address, pins['in1'], 2048)
            self.test_single_motor_channel(pca_address, pins['in2'], 0)
            time.sleep(2)
            
            # Parada
            self.test_single_motor_channel(pca_address, pins['in1'], 0)
            self.test_single_motor_channel(pca_address, pins['in2'], 0)
            
            # Teste de diferentes velocidades
            print("4. Teste de velocidades variadas")
            speeds = [1024, 2048, 3072, 4095]  # 25%, 50%, 75%, 100% duty cycle
            for speed in speeds:
                print(f"Testando velocidade {speed//40.95:.0f}%")
                self.test_single_motor_channel(pca_address, pins['in1'], 0)
                self.test_single_motor_channel(pca_address, pins['in2'], speed)
                time.sleep(1)
            

            self.test_single_motor_channel(pca_address, pins['in1'], 0)
            self.test_single_motor_channel(pca_address, pins['in2'], 0)

    def debug_mode(self):
        print("\n=== Modo de Debug dos Motores ===")
        
        # Encontra PCA9685s
        pca_addresses = self.find_pca9685()
        if not pca_addresses:
            print("Nenhum PCA9685 encontrado!")
            return
        
        # Configuração inicial
        for addr in pca_addresses:
            self.setup_pca9685(addr)
        
        while True:
            print("\nOpções de teste:")
            print("1. Testar canal específico")
            print("2. Teste completo do motor")
            print("3. Variar velocidade")
            print("4. Sair")
            
            try:
                choice = int(input("Escolha uma opção: "))
                
                if choice == 1:
                    addr = int(input("Endereço PCA9685 (ex: 64 para 0x40): "), 16)
                    channel = int(input("Número do canal (0-15): "))
                    duty = int(input("Duty cycle (0-4095): "))
                    self.test_single_motor_channel(addr, channel, duty)
                
                elif choice == 2:
                    addr = int(input("Endereço PCA9685 (ex: 64 para 0x40): "), 16)
                    self.test_drv8870_detailed(addr)
                
                elif choice == 3:
                    addr = int(input("Endereço PCA9685 (ex: 64 para 0x40): "), 16)
                    channel = int(input("Número do canal (0-15): "))
                    for duty in range(0, 4096, 512):
                        print(f"Testando duty cycle: {duty}")
                        self.test_single_motor_channel(addr, channel, duty)
                        time.sleep(1)
                
                elif choice == 4:
                    break
                
            except ValueError as e:
                print(f"Entrada inválida: {e}")
                continue

if __name__ == "__main__":
    tester = MotorTester()
    tester.debug_mode()