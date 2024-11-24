from dataclasses import dataclass
from typing import Dict, List

@dataclass
class DeviceConfig:
    name: str
    address: int
    channels: Dict[str, int]
    description: str

class PiRacerMap:
    def __init__(self):
        # Mapeamento dos dispositivos I2C
        self.i2c_devices = {
            'servo_controller': DeviceConfig(
                name="PCA9685 (Servo)",
                address=0x40,
                channels={
                    'servo': 0,  # LED0
                },
                description="Controlador PWM para servo"
            ),
            
            'motor_controller': DeviceConfig(
                name="PCA9685 (Motores)",
                address=0x41,
                channels={
                    'motor1_in1': 0,  # LED0
                    'motor1_in2': 1,  # LED1
                    'motor2_in1': 2,  # LED2
                    'motor2_in2': 3,  # LED3
                },
                description="Controlador PWM para motores DC"
            ),
            
            'oled': DeviceConfig(
                name="SSD1306",
                address=0x3C,
                channels={},
                description="Display OLED 128x32"
            ),
            
            'current_sensor': DeviceConfig(
                name="INA219",
                address=0x41,
                channels={},
                description="Sensor de corrente"
            )
        }
        
        # Mapeamento dos motores para DRV8870
        self.motor_mapping = {
            'motor1': {
                'driver': 'DRV8870_1',
                'in1_channel': self.i2c_devices['motor_controller'].channels['motor1_in1'],
                'in2_channel': self.i2c_devices['motor_controller'].channels['motor1_in2']
            },
            'motor2': {
                'driver': 'DRV8870_2',
                'in1_channel': self.i2c_devices['motor_controller'].channels['motor2_in1'],
                'in2_channel': self.i2c_devices['motor_controller'].channels['motor2_in2']
            }
        }
        
        # Mapeamento dos pinos de conexão
        self.connection_pins = {
            '1': '3V3',
            '2': '5V',
            '3': 'SDA',
            '4': '5V',
            '5': 'SCL',
            '6': 'GND'
        }

    def print_device_map(self):
        """Imprime o mapa completo dos dispositivos"""
        print("=== Mapa de Dispositivos do PiRacer ===\n")
        
        print("Conexões do Header:")
        print("-" * 30)
        for pin, signal in self.connection_pins.items():
            print(f"Pin {pin}: {signal}")
        
        print("\nDispositivos I2C:")
        print("-" * 30)
        for device in self.i2c_devices.values():
            print(f"\n{device.name}:")
            print(f"  Endereço: 0x{device.address:02X}")
            print(f"  Descrição: {device.description}")
            if device.channels:
                print("  Canais:")
                for name, channel in device.channels.items():
                    print(f"    - {name}: {channel}")
        
        print("\nMapeamento dos Motores:")
        print("-" * 30)
        for motor, config in self.motor_mapping.items():
            print(f"\n{motor}:")
            print(f"  Driver: {config['driver']}")
            print(f"  IN1: Canal {config['in1_channel']}")
            print(f"  IN2: Canal {config['in2_channel']}")

    def verify_addresses(self) -> List[str]:
        """
        Verifica possíveis conflitos de endereço
        """
        used_addresses = {}
        conflicts = []
        
        for dev_name, device in self.i2c_devices.items():
            if device.address in used_addresses:
                conflicts.append(f"Conflito de endereço 0x{device.address:02X} entre {dev_name} e {used_addresses[device.address]}")
            used_addresses[device.address] = dev_name
        
        return conflicts

if __name__ == "__main__":
    piracer_map = PiRacerMap()
    
    print("=== Análise do Hardware PiRacer ===\n")
    

    conflicts = piracer_map.verify_addresses()
    if conflicts:
        print("⚠️ Conflitos detectados:")
        for conflict in conflicts:
            print(f"- {conflict}")
        print("\nPode ser necessário ajustar os endereços!\n")
 
    piracer_map.print_device_map()