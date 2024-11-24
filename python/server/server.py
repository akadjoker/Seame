import socket
import selectors
import threading
import json
import time
import logging
import queue
import random
from dataclasses import dataclass
from enum import IntEnum
from typing import Dict, Callable, Optional, Any
import struct

class MessageType(IntEnum):
    # Sistema
    HEARTBEAT = 0
    ACK = 1
    NACK = 2
    
    # Display
    DISPLAY_TEXT = 10
    DISPLAY_CLEAR = 11
    DISPLAY_IP = 12
    
    # Sensores
    GET_TEMPERATURE = 20
    GET_HUMIDITY = 21
    GET_DISTANCE = 22
    GET_ALL_SENSORS = 23
    
    # Motores
    MOTOR_FORWARD = 30
    MOTOR_BACKWARD = 31
    MOTOR_LEFT = 32
    MOTOR_RIGHT = 33
    MOTOR_STOP = 34
    SET_SPEED = 35
    
    # Sistema
    SAVE_STATE = 40
    LOAD_STATE = 41
    SHUTDOWN = 42

@dataclass
class Message:
    type: MessageType
    sequence: int
    payload: bytes
    
    @classmethod
    def pack(cls, msg_type: MessageType, sequence: int, payload: bytes) -> bytes:
        header = struct.pack('!BIH', msg_type, sequence, len(payload))
        return header + payload
    
    @classmethod
    def unpack(cls, data: bytes) -> 'Message':
        msg_type, sequence, payload_size = struct.unpack('!BIH', data[:7])
        payload = data[7:7+payload_size]
        return cls(MessageType(msg_type), sequence, payload)

class Display:
    def __init__(self):
        self.last_message = ""
        logging.info("Display inicializado")
        
    def show_text(self, text: str):
        self.last_message = text
        logging.info(f"Display: {text}")
        
    def clear(self):
        self.last_message = ""
        logging.info("Display limpo")
        
    def show_ip(self):
        import socket
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        self.show_text(f"IP: {ip}")

class MotorController:
    def __init__(self):
        self.current_speed = 0
        self.is_moving = False
        logging.info("Motor Controller inicializado")
        
    def move_forward(self, speed: float, duration: float):
        self.current_speed = speed
        self.is_moving = True
        logging.info(f"Move frente: velocidade={speed}, duração={duration}")
        if duration > 0:
            threading.Timer(duration, self.stop).start()
    
    def stop(self):
        self.current_speed = 0
        self.is_moving = False
        logging.info("Motor parado")

class SensorManager:
    def __init__(self):
        self.last_reading = {
            'temperature': 25.0,
            'humidity': 50.0,
            'distance': 100.0,
            'battery': 100.0
        }
        logging.info("Sensor Manager inicializado")
    
    def read_all(self) -> dict:
        # simulamos leitura de sensores
        self.last_reading['temperature'] += (random.random() - 0.5)
        self.last_reading['humidity'] += (random.random() - 0.5)
        self.last_reading['distance'] += (random.random() - 0.5) * 5
        self.last_reading['battery'] -= random.random() * 0.1
        return self.last_reading

class PiServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8888):
        self.host = host
        self.port = port
        self.running = False
        self.selector = selectors.DefaultSelector()
        self.message_queue = queue.Queue()
        self.clients = {}
        self.sequence = 0
        
        # Componentes
        self.display = Display()
        self.motors = MotorController()
        self.sensors = SensorManager()
        
        # Configuração de logging
        logging.basicConfig(
            filename='piserver.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Registra handlers de mensagens
        self.message_handlers = {
            MessageType.DISPLAY_TEXT: self._handle_display_text,
            MessageType.MOTOR_FORWARD: self._handle_motor_forward,
            MessageType.GET_ALL_SENSORS: self._handle_sensor_request,
            MessageType.SHUTDOWN: self._handle_shutdown
        }
        
    def start(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_socket.setblocking(False)
        
        self.selector.register(
            self.server_socket,
            selectors.EVENT_READ,
            self._accept_connection
        )
        
        # Inicia threads
        self.process_thread = threading.Thread(target=self._process_messages)
        self.monitor_thread = threading.Thread(target=self._monitor_system)
        
        self.process_thread.start()
        self.monitor_thread.start()
        
        logging.info(f"Servidor iniciado em {self.host}:{self.port}")
        self.display.show_ip()
        
        try:
            while self.running:
                events = self.selector.select(timeout=1)
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj)
        except KeyboardInterrupt:
            self.stop()
            
    def stop(self):
        self.running = False
        self.selector.close()
        self.server_socket.close()
        
        # Espera threads terminarem
        self.process_thread.join()
        self.monitor_thread.join()
        
        logging.info("Servidor finalizado")
        
    def _accept_connection(self, sock):
        client_socket, addr = sock.accept()
        client_socket.setblocking(False)
        self.selector.register(
            client_socket,
            selectors.EVENT_READ,
            self._handle_client_data
        )
        self.clients[client_socket] = addr
        logging.info(f"Nova conexão de {addr}")
        
    def _handle_client_data(self, sock):
        try:
            data = sock.recv(1024)
            if data:
                # Coloca mensagem na fila para processamento
                self.message_queue.put((sock, data))
            else:
                # cliente saiu
                self._remove_client(sock)
        except ConnectionError:
            self._remove_client(sock)
            
    def _remove_client(self, sock):
        self.selector.unregister(sock)
        sock.close()
        if sock in self.clients:
            addr = self.clients.pop(sock)
            logging.info(f"Cliente {addr} desconectado")
            
    def _process_messages(self):
        while self.running:
            try:
                sock, data = self.message_queue.get(timeout=1)
                try:
                    message = Message.unpack(data)
                    handler = self.message_handlers.get(message.type)
                    if handler:
                        response = handler(message)
                        if response:
                            sock.send(response)
                except Exception as e:
                    logging.error(f"Erro ao processar mensagem: {e}")
            except queue.Empty:
                continue
                
    def _monitor_system(self):
        while self.running:
            # Monitora temperatura do sistema ??? TESTAR
            try:
                with open('/sys/class/thermal/thermal_zone0/temp') as f:
                    temp = float(f.read()) / 1000.0
                if temp > 80.0:
                    logging.warning(f"Temperatura alta: {temp}°C")
                    self.display.show_text(f"Atenção! Temp: {temp:.1f}°C")
            except:
                pass
            
            # Monitora memória TESTAR
            try:
                with open('/proc/meminfo') as f:
                    mem_total = 0
                    mem_free = 0
                    for line in f:
                        if 'MemTotal' in line:
                            mem_total = int(line.split()[1])
                        elif 'MemFree' in line:
                            mem_free = int(line.split()[1])
                            break
                    
                    mem_usage = (mem_total - mem_free) / mem_total * 100
                    if mem_usage > 90:
                        logging.warning(f"Uso de memória alto: {mem_usage:.1f}%")
            except:
                pass
                
            time.sleep(5)
            
    def _handle_display_text(self, message: Message) -> Optional[bytes]:
        text = message.payload.decode('utf-8')
        self.display.show_text(text)
        return Message.pack(MessageType.ACK, message.sequence, b'')
        
    def _handle_motor_forward(self, message: Message) -> Optional[bytes]:
        speed, duration = struct.unpack('!ff', message.payload)
        self.motors.move_forward(speed, duration)
        return Message.pack(MessageType.ACK, message.sequence, b'')
        
    def _handle_sensor_request(self, message: Message) -> Optional[bytes]:
        readings = self.sensors.read_all()
        payload = json.dumps(readings).encode('utf-8')
        return Message.pack(MessageType.GET_ALL_SENSORS, message.sequence, payload)
        
    def _handle_shutdown(self, message: Message) -> Optional[bytes]:
        threading.Timer(1.0, self.stop).start()
        return Message.pack(MessageType.ACK, message.sequence, b'')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Pi Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=8888, help='Port number')
    args = parser.parse_args()
    
    server = PiServer(args.host, args.port)
    server.start()
