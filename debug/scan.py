import smbus2
import time

def scan_i2c_devices():
    """Scan para encontrar endereços I2C ativos"""
    print("Scanning I2C bus...")
    bus = smbus2.SMBus(1)  # 1 indica /dev/i2c-1
    
    devices = []
    for address in range(0x00, 0x7F):
        try:
            bus.read_byte(address)
            hex_address = hex(address)
            print(f"Dispositivo encontrado no endereço: {hex_address}")
            devices.append(hex_address)
        except Exception as e:
            pass
    
    bus.close()
    return devices


def identify_device(address):
    """Tenta identificar o tipo de dispositivo baseado no endereço"""
    if address in range(0x40, 0x48):
        return "PCA9685 (LED/Servo Controller)"
    elif address == 0x41:
        return "INA219 (Current Sensor)"
    elif address in [0x3C, 0x3D]:
        return "SSD1306 (OLED Display)"
    else:
        return "Dispositivo Desconhecido"

def scan_all_devices():
    """Scan completo de dispositivos I2C"""
    print("Scanning todos dispositivos I2C...")
    bus = smbus2.SMBus(1)
    
    for address in range(0x00, 0x7F):
        try:
            bus.read_byte(address)
            hex_address = hex(address)
            device_type = identify_device(address)
            print(f"Endereço: {hex_address} - {device_type}")
        except Exception as e:
            pass
    
    bus.close()




def detect_pca9685():
    """Detecta especificamente dispositivos PCA9685"""
    print("Procurando por dispositivos PCA9685...")
    bus = smbus2.SMBus(1)
    
    # Range de endereços possíveis para PCA9685
    pca9685_addresses = range(0x40, 0x48)  # 0x40 a 0x47
    
    found_devices = []
    for address in pca9685_addresses:
        try:
            # Tentamos ler o registrador MODE1 (0x00) do PCA9685
            bus.read_byte_data(address, 0x00)
            hex_address = hex(address)
            print(f"PCA9685 encontrado no endereço: {hex_address}")
            found_devices.append(hex_address)
        except Exception as e:
            pass
    
    bus.close()
    return found_devices


#    
found_devices = scan_i2c_devices()
if found_devices:
    print("\nDispositivos encontrados:")
    for device in found_devices:
        print(f"Endereço: {device}")
else:
    print("Nenhum dispositivo I2C encontrado")



found_pca9685s = detect_pca9685()

if found_pca9685s:
    print("\nPCA9685s encontrados:")
    for addr in found_pca9685s:
        print(f"Endereço: {addr}")
else:
    print("Nenhum PCA9685 encontrado")





scan_all_devices()