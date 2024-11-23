import socket
import struct
import json
import threading
from dataclasses import dataclass
from enum import IntEnum
import time

class MessageType(IntEnum):
    DISPLAY_TEXT = 10
    MOTOR_FORWARD = 30
    GET_ALL_SENSORS = 23
    SHUTDOWN = 42

class PiClient:
    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port
        self.sequence = 0
        self.socket = None
        self.running = False
        
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.running = True

        self.receive_thread = threading.Thread(target=self._receive_loop)
        self.receive_thread.start()
        
    def disconnect(self):
        self.running = False
        if self.socket:
            self.socket.close()
        self.receive_thread.join()
        
    def _receive_loop(self):
        while self.running:
            try:
                header = self.socket.recv(7)
                if not header:
                    break
                    
                msg_type, sequence, payload_size = struct.unpack('!BIH', header)
                payload = self.socket.recv(payload_size) if payload_size > 0 else b''
                
                if msg_type == MessageType.GET_ALL_SENSORS:
                    data = json.loads(payload.decode('utf-8'))
                    print(f"Sensor readings: {data}")
                    
            except ConnectionError:
                break
            except Exception as e:
                print(f"Erro ao receber dados: {e}")
                break
                
        self.running = False
        
    def display_text(self, text: str):
        payload = text.encode('utf-8')
        header = struct.pack('!BIH', MessageType.DISPLAY_TEXT, self.sequence, len(payload))
        self.socket.send(header + payload)
        self.sequence += 1
        
    def move_forward(self, speed: float, duration: float):
        payload = struct.pack('!ff', speed, duration)
        header = struct.pack('!BIH', MessageType.MOTOR_FORWARD, self.sequence, len(payload))
        self.socket.send(header + payload)
        self.sequence += 1
        
    def get_sensor_data(self):
        header = struct.pack('!BIH', MessageType.GET_ALL_SENSORS, self.sequence, 0)
        self.socket.send(header)
        self.sequence += 1
        
    def shutdown_server(self):
        header = struct.pack('!BIH', MessageType.SHUTDOWN, self.sequence, 0)
        self.socket.send(header)
        self.sequence += 1

if __name__ == '__main__':
    client = PiClient()
    try:
        client.connect()
        

        client.display_text("Teste do Display")
        time.sleep(1)
        
        client.move_forward(0.5, 2.0)  
        time.sleep(2)
        
        client.get_sensor_data()
        time.sleep(1)
        
        #client.shutdown_server()
        
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()
