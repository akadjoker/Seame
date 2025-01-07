import network
import socket
from machine import Pin
import time

# Configuração do LED
led = Pin(2, Pin.OUT)

# Configurações do WiFi
ssid = 'NOS-BC36'  # Nome da rede que aparece na foto
password = 'VKCT2WYF'  # Senha que deve estar na etiqueta

# Conecta ao WiFi
def conecta_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print('Conectando ao WiFi...')
        wifi.connect(ssid, password)
        while not wifi.isconnected():
            time.sleep(1)
    print('Conectado!')
    print('IP:', wifi.ifconfig()[0])

# Página HTML
def pagina_web():
    html = """
    <html>
        <head>
            <title>ESP32 Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial; text-align: center; margin:0px auto; padding: 20px; }
                .button { background-color: #4CAF50; color: white; padding: 10px 20px;
                         border: none; border-radius: 4px; cursor: pointer; }
                .button:hover { background-color: #45a049; }
            </style>
        </head>
        <body>
            <h1>ESP32 Web Server</h1>
            <p>LED Status: <strong>%STATUS%</strong></p>
            <p><a href="/led/on"><button class="button">LED ON</button></a></p>
            <p><a href="/led/off"><button class="button">LED OFF</button></a></p>
        </body>
    </html>
    """
    return html

# Inicia o servidor
def inicia_servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    
    while True:
        try:
            conn, addr = s.accept()
            request = conn.recv(1024)
            request = str(request)
            
            # Controle do LED
            led_on = request.find('/led/on')
            led_off = request.find('/led/off')
            
            if led_on == 6:
                led.value(1)
            if led_off == 6:
                led.value(0)
                
            # Prepara resposta
            status = "ON" if led.value() else "OFF"
            response = pagina_web().replace('%STATUS%', status)
            
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
            
        except Exception as e:
            print('Erro:', e)
            conn.close()

# Executa o programa
conecta_wifi()
print('Iniciando servidor web...')
inicia_servidor()