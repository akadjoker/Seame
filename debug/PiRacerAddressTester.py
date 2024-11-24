import smbus
import time

class PiRacerAddressTester:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        # Possíveis configurações
        self.SERVO_ADDR = 0x40
        self.MOTOR_ADDR = 0x41
        
    def test_servo_addr(self):
        """
        Testa o PCA9685 no endereço 0x40 com o servo
        """
        print("\n=== Testando Servo no endereço 0x40 ===")
        try:
            # Reset e configuração do PCA9685
            self.bus.write_byte_data(self.SERVO_ADDR, 0x00, 0x00)  # Reset
            time.sleep(0.1)
            self.bus.write_byte_data(self.SERVO_ADDR, 0xFE, 0x1E)  # Frequência ~50Hz
            time.sleep(0.1)
            self.bus.write_byte_data(self.SERVO_ADDR, 0x00, 0x20)  # Modo normal
            
            # Teste do servo (canal 0)
            print("Movendo servo...")
            positions = [150, 300, 450, 300, 150]  # Diferentes posições
            for pos in positions:
                # Definir PWM
                self.bus.write_word_data(self.SERVO_ADDR, 0x06, 0)
                self.bus.write_word_data(self.SERVO_ADDR, 0x08, pos)
                time.sleep(0.5)
            
            print("✓ Servo respondendo no endereço 0x40")
            return True
        except Exception as e:
            print(f"✗ Erro no teste do servo: {e}")
            return False
            
    def test_motor_addr(self):
        """
        Testa o PCA9685 no endereço 0x41 com os motores
        """
        print("\n=== Testando Motores no endereço 0x41 ===")
        try:
            # Reset e configuração do PCA9685
            self.bus.write_byte_data(self.MOTOR_ADDR, 0x00, 0x00)  # Reset
            time.sleep(0.1)
            self.bus.write_byte_data(self.MOTOR_ADDR, 0xFE, 0x1E)  # Frequência ~50Hz
            time.sleep(0.1)
            self.bus.write_byte_data(self.MOTOR_ADDR, 0x00, 0x20)  # Modo normal
            
            # Teste do Motor 1
            print("\nTestando Motor 1...")
            # Movimento para frente
            self.bus.write_word_data(self.MOTOR_ADDR, 0x06, 0)      # Canal 0 (IN1)
            self.bus.write_word_data(self.MOTOR_ADDR, 0x0A, 2048)   # Canal 1 (IN2)
            time.sleep(1)
            # Parar
            self.bus.write_word_data(self.MOTOR_ADDR, 0x06, 0)
            self.bus.write_word_data(self.MOTOR_ADDR, 0x0A, 0)
            
            # Teste do Motor 2
            print("\nTestando Motor 2...")
            # Movimento para frente
            self.bus.write_word_data(self.MOTOR_ADDR, 0x0E, 0)      # Canal 2 (IN1)
            self.bus.write_word_data(self.MOTOR_ADDR, 0x12, 2048)   # Canal 3 (IN2)
            time.sleep(1)
            # Parar
            self.bus.write_word_data(self.MOTOR_ADDR, 0x0E, 0)
            self.bus.write_word_data(self.MOTOR_ADDR, 0x12, 0)
            
            print("✓ Motores respondendo no endereço 0x41")
            return True
        except Exception as e:
            print(f"✗ Erro no teste dos motores: {e}")
            return False
    
    def scan_i2c(self):
        """
        Varre todos os endereços I2C possíveis
        """
        print("\n=== Varredura de endereços I2C ===")
        for addr in range(0x00, 0x7F):
            try:
                self.bus.read_byte(addr)
                print(f"Dispositivo encontrado no endereço 0x{addr:02X}")
            except:
                pass
    
    def interactive_test(self):
        """
        Modo de teste interativo
        """
        while True:
            print("\n=== Menu de Teste ===")
            print("1. Varrer endereços I2C")
            print("2. Testar servo (0x40)")
            print("3. Testar motores (0x41)")
            print("4. Testar canal específico")
            print("5. Sair")
            
            try:
                choice = int(input("opção: "))
                
                if choice == 1:
                    self.scan_i2c()
                
                elif choice == 2:
                    self.test_servo_addr()
                
                elif choice == 3:
                    self.test_motor_addr()
                
                elif choice == 4:
                    addr = int(input(" endereço (ex: 64 para 0x40): "), 16)
                    channel = int(input("canal (0-15): "))
                    value = int(input(" valor PWM (0-4095): "))
                    
                    try:
                        print(f"Test endereço 0x{addr:02X}, canal {channel}, valor {value}")
                        self.bus.write_word_data(addr, 0x06 + (channel * 4), 0)
                        self.bus.write_word_data(addr, 0x08 + (channel * 4), value)
                        print("sucesso")
                    except Exception as e:
                        print(f"Erro: {e}")
                
                elif choice == 5:
                    break
                    
            except ValueError:
                print("Entrada inválida!")
                continue

if __name__ == "__main__":
    tester = PiRacerAddressTester()
    tester.interactive_test()