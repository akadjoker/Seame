import network
import time

# Configurações do WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Dados do seu modem NOS
ssid = 'NOS-BC36'  # Nome da rede que aparece na foto
password = 'VKCT2WYF'  # Senha que deve estar na etiqueta

print('Conectando ao WiFi...')
wifi.connect(ssid, password)

# Espera a conexão
while not wifi.isconnected():
    print('Tentando conectar...')
    time.sleep(1)

print('Conectado!')
print('Endereço IP:', wifi.ifconfig()[0])