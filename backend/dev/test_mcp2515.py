import spidev

def read_register(spi, register):
    # Envia o comando READ e o endereço do registro
    tx = [0x03, register, 0x00]  # 0x03 é o comando READ
    rx = spi.xfer2(tx)  # Transfere dados SPI
    return rx[2]  # Retorna o valor lido

# Testar /dev/spidev0.0
spi0 = spidev.SpiDev()
spi0.open(0, 0)  # SPI0, CS0
spi0.max_speed_hz = 1000000

# Testar /dev/spidev0.1
spi1 = spidev.SpiDev()
spi1.open(0, 1)  # SPI0, CS1
spi1.max_speed_hz = 1000000

print("Testando /dev/spidev0.0...")
value0 = read_register(spi0, 0x0E)  # Lê o registro CANSTAT
print(f"Registro CANSTAT: 0x{value0:02X}")

print("Testando /dev/spidev0.1...")
value1 = read_register(spi1, 0x0E)  # Lê o registro CANSTAT
print(f"Registro CANSTAT: 0x{value1:02X}")

spi0.close()
spi1.close()
