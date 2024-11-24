import smbus
import time

class PiRacerPinMap:
    # Endereços I2C
    PCA9685_ADDR1 = 0x40  # Primeiro PCA9685 (PCA1)
    PCA9685_ADDR2 = 0x41  # Segundo PCA9685 (PCA2)
    
    # Mapeamento do primeiro DRV8870 (DRV1)
    MOTOR1_CONFIG = {
        'in1': 0,  # LED0 no PCA1
        'in2': 1,  # LED1 no PCA1
        'name': 'Motor 1 (DRV1)'
    }
    
    # Mapeamento do segundo DRV8870 (DRV2)
    MOTOR2_CONFIG = {
        'in1': 2,  # LED2 no PCA1
        'in2': 3,  # LED3 no PCA1
        'name': 'Motor 2 (DRV2)'
    }
    
    # Mapeamento do Servo
    SERVO_CONFIG = {
        'channel': 4,  # LED4 no PCA1
        'name': 'Steering Servo'
    }
    
    def __init__(self):
        self.bus = smbus.SMBus(1)
        
    def test_configuration(self):
        """
        Testa a configuração identificada
        """
        print("=== Configuração do PiRacer ===")
        print("\nEndereços I2C:")
        print(f"PCA9685 Principal: 0x{self.PCA9685_ADDR1:02X}")
        print(f"PCA9685 Secundário: 0x{self.PCA9685_ADDR2:02X}")
        
        print("\nMapeamento de Motores:")
        print(f"Motor 1 (DRV1):")
        print(f"  - IN1: Canal {self.MOTOR1_CONFIG['in1']}")
        print(f"  - IN2: Canal {self.MOTOR1_CONFIG['in2']}")
        
        print(f"\nMotor 2 (DRV2):")
        print(f"  - IN1: Canal {self.MOTOR2_CONFIG['in1']}")
        print(f"  - IN2: Canal {self.MOTOR2_CONFIG['in2']}")
        
        print(f"\nServo:")
        print(f"  - Canal: {self.SERVO_CONFIG['channel']}")
        
    def verify_connections(self):
        """
        Verifica as conexões físicas
        """
        print("\nVerificando conexões...")
        
        # Testa PCA9685 Principal
        try:
            self.bus.read_byte_data(self.PCA9685_ADDR1, 0x00)
            print(f"✓ PCA9685 Principal (0x{self.PCA9685_ADDR1:02X}) respondendo")
        except Exception as e:
            print(f"✗ PCA9685 Principal não encontrado: {e}")
            
        # Testa PCA9685 Secundário
        try:
            self.bus.read_byte_data(self.PCA9685_ADDR2, 0x00)
            print(f"✓ PCA9685 Secundário (0x{self.PCA9685_ADDR2:02X}) respondendo")
        except Exception as e:
            print(f"✗ PCA9685 Secundário não encontrado: {e}")

def main():
    pinmap = PiRacerPinMap()
    pinmap.test_configuration()
    pinmap.verify_connections()
    
    print("\nPara usar esta configuração no seu código:")
    print("""
    # 
    from piracer_pinmap import PiRacerPinMap
    
    # Configuração dos motores
    motor1_in1 = PiRacerPinMap.MOTOR1_CONFIG['in1']  # Canal 0
    motor1_in2 = PiRacerPinMap.MOTOR1_CONFIG['in2']  # Canal 1
    
    motor2_in1 = PiRacerPinMap.MOTOR2_CONFIG['in1']  # Canal 2
    motor2_in2 = PiRacerPinMap.MOTOR2_CONFIG['in2']  # Canal 3
    
    # Configuração do servo
    servo_channel = PiRacerPinMap.SERVO_CONFIG['channel']  # Canal 4
    """)

if __name__ == "__main__":
    main()