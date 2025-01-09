import socket
import threading
from enum import IntEnum

class BinaryStream:
    def __init__(self, data=None):
        self.buffer = bytearray() if data is None else bytearray(data)
        self.position = 0
        
    def write_byte(self, value):
        self.buffer.extend(value.to_bytes(1, 'little'))
        
    def write_short(self, value):
        self.buffer.extend(value.to_bytes(2, 'little', signed=True))
    
    def write_ushort(self, value):
        self.buffer.extend(value.to_bytes(2, 'little'))
        
    def write_int(self, value):
        self.buffer.extend(value.to_bytes(4, 'little', signed=True))
        
    def write_string(self, value):
        encoded = value.encode('utf-8')
        self.write_short(len(encoded))
        self.buffer.extend(encoded)
        
    def read_byte(self):
        value = self.buffer[self.position]
        self.position += 1
        return value
        
    def read_short(self):
        value = int.from_bytes(self.buffer[self.position:self.position + 2], 'little', signed=True)
        self.position += 2
        return value

    def read_ushort(self):
        value = int.from_bytes(self.buffer[self.position:self.position + 2], 'little')
        self.position += 2
        return value
        
    def read_int(self):
        value = int.from_bytes(self.buffer[self.position:self.position + 4], 'little', signed=True)
        self.position += 4
        return value
        
    def read_string(self):
        length = self.read_short()
        value = self.buffer[self.position:self.position + length].decode('utf-8')
        self.position += length
        return value
        
    def get_buffer(self):
        return self.buffer
    def get_size(self):
        return len(self.buffer)
    

class RequestType(IntEnum):
    GET_SPEED = 1
    GET_WHEELS = 2
    GET_MOTOR = 3
    GET_ALL_STATE = 4

class CarStateClient:
    def __init__(self, host='localhost', port=4206):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        print(f"Connected to server at {host}:{port}")

    def request_speed(self):
        stream = BinaryStream()
        stream.write_byte(RequestType.GET_SPEED)
        stream.write_ushort(0)
        self.sock.send(stream.get_buffer())
        
        response = BinaryStream(self.sock.recv(1024))
        speed = response.read_byte()
        return speed

    def request_wheels(self):
        stream = BinaryStream()
        stream.write_byte(RequestType.GET_WHEELS)
        stream.write_ushort(0)
        self.sock.send(stream.get_buffer())
        
        response = BinaryStream(self.sock.recv(1024))
        angle = response.read_short()
        return angle

    def request_motor(self):
        stream = BinaryStream()
        stream.write_byte(RequestType.GET_MOTOR)
        stream.write_ushort(0)
        self.sock.send(stream.get_buffer())
        
        response = BinaryStream(self.sock.recv(1024))
        direction = response.read_byte()
        power = response.read_byte()
        return direction, power



    def close(self):
        self.sock.close()

if __name__ == "__main__":
    client = CarStateClient()
    
    try:
        while True:
            print("\nRequest Menu:")
            print("1. Get Speed")
            print("2. Get Wheels State")
            print("3. Get Motor State")
            #print("4. Get Complete State")
            print("0. Exit")
            
            choice = input("Select an option: ")
            
            if choice == "1":
                speed = client.request_speed()
                print(f"Current speed: {speed} km/h")
                
            elif choice == "2":
                angle = client.request_wheels()
                print(f"Wheels: Angle = {angle}")
                
            elif choice == "3":
                direction, power = client.request_motor()
                dir_text = "Forward" if direction == 1 else "Reverse" if direction == -1 else "Stopped"
                print(f"Motor: Direction = {dir_text}, Power = {power}%")

            elif choice == "0":
                break
            
            #input("\nPress Enter to continue...")
            
    except KeyboardInterrupt:
        print("\nShutting down client...")
    finally:
        client.close()