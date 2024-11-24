import smbus
import time
import RPi.GPIO as GPIO
from subprocess import getoutput

class PiRacerScanner:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        
    def scan_i2c_devices(self):
        print("Iniciando varredura de dispositivos I2C...\n")
        
        # Dicionário de dispositivos I2C comuns no PiRacer
        known_devices = {
            0x40: "PCA9685 (PWM Controller 1)",
            0x41: "PCA9685 (PWM Controller 2)",
            0x3C: "SSD1306 (OLED Display)",
            0x41: "INA219 (Current Sensor)"
        }
        
        found_devices = []
        
        for addr in range(0x00, 0x7F):
            try:
                self.bus.read_byte(addr)
                device_name = known_devices.get(addr, "Dispositivo Desconhecido")
                found_devices.append((addr, device_name))
                print(f"Dispositivo encontrado: 0x{addr:02X} - {device_name}")
            except Exception:
                pass
                
        return found_devices
    
    def test_i2c_device(self, address):
        try:
            self.bus.read_byte(address)
            print(f"Comunicação bem sucedida com dispositivo 0x{address:02X}")
            return True
        except Exception as e:
            print(f"Erro ao comunicar com dispositivo 0x{address:02X}: {e}")
            return False
    
    def scan_gpio_pins(self):
        print("\nVerificando pinos GPIO...\n")
        
        # Configura modo de numeração dos pinos
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Lista de pinos GPIO válidos no Raspberry Pi
        valid_pins = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
        
        pin_status = {}
        
        for pin in valid_pins:
            try:
                # Testa como entrada
                GPIO.setup(pin, GPIO.IN)
                value = GPIO.input(pin)
                status = "Pull-Down" if value == 0 else "Pull-Up"
                
                # Testa como saída
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)
                time.sleep(0.1)
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(0.1)
                
                pin_status[pin] = {
                    "mode": "OK - Entrada/Saída",
                    "status": status
                }
                
            except Exception as e:
                pin_status[pin] = {
                    "mode": "ERRO ou Em Uso",
                    "status": str(e)
                }
            
            finally:
                GPIO.setup(pin, GPIO.IN)
        
        # Limpa configuração GPIO
        GPIO.cleanup()
        
        return pin_status
    
    def check_system_info(self):
        print("\nInformações do Sistema:\n")
        
        # Verifica versão do Raspberry Pi
        model = getoutput('cat /proc/device-tree/model')
        print(f"Modelo: {model}")
        
        # Verifica temperatura
        temp = getoutput('vcgencmd measure_temp')
        print(f"Temperatura: {temp}")
        
        # Verifica tensão
        volts = getoutput('vcgencmd measure_volts')
        print(f"Tensão: {volts}")
        
        # Lista módulos I2C carregados
        i2c_modules = getoutput('lsmod | grep i2c')
        print("\nMódulos I2C carregados:")
        print(i2c_modules)

def main():
    scanner = PiRacerScanner()
    
    print("=== Scanner de Hardware PiRacer ===\n")
    
    # Verifica informações do sistema
    scanner.check_system_info()
    
    # Varre dispositivos I2C
    print("\n=== Dispositivos I2C Encontrados ===")
    devices = scanner.scan_i2c_devices()
    
    # Verifica pinos GPIO
    print("\n=== Status dos Pinos GPIO ===")
    gpio_status = scanner.scan_gpio_pins()
    for pin, status in gpio_status.items():
        print(f"GPIO {pin}: {status['mode']} - {status['status']}")

if __name__ == "__main__":
    main()