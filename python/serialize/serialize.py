from enum import IntEnum
import struct
import time
from typing import Any, Dict, List, Tuple, Optional
from dataclasses import dataclass

class MessageType(IntEnum):
    ACK = 100
    NACK = 101
    
    MOVE = 1
    STOP = 2
    GET_STATUS = 3
    SET_SPEED = 4
    GET_SENSORS = 5

class DataType(IntEnum):
    UINT8 = 1
    INT8 = 2
    UINT16 = 3
    INT16 = 4
    UINT32 = 5
    INT32 = 6
    FLOAT = 7
    DOUBLE = 8
    STRING = 9
    BOOL = 10

class BinarySerializer:
    TYPE_FORMATS = {
        DataType.UINT8: ('B', 1),
        DataType.INT8: ('b', 1),
        DataType.UINT16: ('H', 2),
        DataType.INT16: ('h', 2),
        DataType.UINT32: ('I', 4),
        DataType.INT32: ('i', 4),
        DataType.FLOAT: ('f', 4),
        DataType.DOUBLE: ('d', 8),
        DataType.BOOL: ('?', 1),
    }
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._write_buffer = bytearray()
        self._read_buffer = b''
        self._read_offset = 0
    
    def write_uint8(self, value: int) -> 'BinarySerializer':
        return self.write(DataType.UINT8, value)
        
    def write_int8(self, value: int) -> 'BinarySerializer':
        return self.write(DataType.INT8, value)
        
    def write_uint16(self, value: int) -> 'BinarySerializer':
        return self.write(DataType.UINT16, value)
        
    def write_int16(self, value: int) -> 'BinarySerializer':
        return self.write(DataType.INT16, value)
        
    def write_uint32(self, value: int) -> 'BinarySerializer':
        return self.write(DataType.UINT32, value)
        
    def write_int32(self, value: int) -> 'BinarySerializer':
        return self.write(DataType.INT32, value)
        
    def write_float(self, value: float) -> 'BinarySerializer':
        return self.write(DataType.FLOAT, value)
        
    def write_double(self, value: float) -> 'BinarySerializer':
        return self.write(DataType.DOUBLE, value)
        
    def write_bool(self, value: bool) -> 'BinarySerializer':
        return self.write(DataType.BOOL, value)
        
    def write_string(self, value: str) -> 'BinarySerializer':
        encoded = value.encode('utf-8')
        self.write_uint16(len(encoded))
        self._write_buffer.extend(encoded)
        return self
        
    def write(self, data_type: DataType, value: Any) -> 'BinarySerializer':
        if data_type == DataType.STRING:
            return self.write_string(value)
            
        fmt, _ = self.TYPE_FORMATS[data_type]
        self._write_buffer.extend(struct.pack(f'!{fmt}', value))
        return self
    
    def read_uint8(self) -> int:
        return self.read(DataType.UINT8)
        
    def read_int8(self) -> int:
        return self.read(DataType.INT8)
        
    def read_uint16(self) -> int:
        return self.read(DataType.UINT16)
        
    def read_int16(self) -> int:
        return self.read(DataType.INT16)
        
    def read_uint32(self) -> int:
        return self.read(DataType.UINT32)
        
    def read_int32(self) -> int:
        return self.read(DataType.INT32)
        
    def read_float(self) -> float:
        return self.read(DataType.FLOAT)
        
    def read_double(self) -> float:
        return self.read(DataType.DOUBLE)
        
    def read_bool(self) -> bool:
        return self.read(DataType.BOOL)
        
    def read_string(self) -> str:
        length = self.read_uint16()
        string_bytes = self._read_buffer[self._read_offset:self._read_offset + length]
        self._read_offset += length
        return string_bytes.decode('utf-8')
        
    def read(self, data_type: DataType) -> Any:
        if data_type == DataType.STRING:
            return self.read_string()
            
        fmt, size = self.TYPE_FORMATS[data_type]
        value = struct.unpack(f'!{fmt}', self._read_buffer[self._read_offset:self._read_offset + size])[0]
        self._read_offset += size
        return value
    
    def get_buffer(self) -> bytes:
        """Retorna o buffer de escrita como bytes"""
        return bytes(self._write_buffer)
    
    def set_buffer(self, buffer: bytes):
        """Define o buffer de leitura"""
        self._read_buffer = buffer
        self._read_offset = 0

@dataclass
class Vector2D:
    x: float
    y: float
    
    def serialize(self, serializer: BinarySerializer):
        serializer.write_float(self.x).write_float(self.y)
    
    @classmethod
    def deserialize(cls, serializer: BinarySerializer) -> 'Vector2D':
        return cls(
            serializer.read_float(),
            serializer.read_float()
        )

@dataclass
class MotorCommand:
    position: Vector2D
    speed: float
    acceleration: float
    
    def serialize(self, serializer: BinarySerializer):
        self.position.serialize(serializer)
        serializer.write_float(self.speed)
        serializer.write_float(self.acceleration)
    
    @classmethod
    def deserialize(cls, serializer: BinarySerializer) -> 'MotorCommand':
        return cls(
            Vector2D.deserialize(serializer),
            serializer.read_float(),
            serializer.read_float()
        )

@dataclass
class SensorData:
    temperature: float
    humidity: float
    distance: float
    battery_level: float
    
    def serialize(self, serializer: BinarySerializer):
        serializer.write_float(self.temperature)
        serializer.write_float(self.humidity)
        serializer.write_float(self.distance)
        serializer.write_float(self.battery_level)
    
    @classmethod
    def deserialize(cls, serializer: BinarySerializer) -> 'SensorData':
        return cls(
            serializer.read_float(),
            serializer.read_float(),
            serializer.read_float(),
            serializer.read_float()
        )

class Message:
    def __init__(self, msg_type: MessageType, payload: Any = None):
        self.type = msg_type
        self.payload = payload
        self.timestamp = int(time.time())
    
    def serialize(self) -> bytes:
        serializer = BinarySerializer()
        
        # Escreve o header
        serializer.write_uint8(self.type)
        serializer.write_uint32(self.timestamp)
        
        # Serializa o payload se existir
        if self.payload is not None:
            if isinstance(self.payload, (Vector2D, MotorCommand, SensorData)):
                payload_data = BinarySerializer()
                self.payload.serialize(payload_data)
                payload_bytes = payload_data.get_buffer()
            elif isinstance(self.payload, str):
                payload_data = BinarySerializer()
                payload_data.write_string(self.payload)
                payload_bytes = payload_data.get_buffer()
            else:
                payload_bytes = b''
                
            serializer.write_uint16(len(payload_bytes))
            serializer._write_buffer.extend(payload_bytes)
        else:
            serializer.write_uint16(0)
        
        return serializer.get_buffer()
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'Message':
        serializer = BinarySerializer()
        serializer.set_buffer(data)
        
        # Lê o header
        msg_type = MessageType(serializer.read_uint8())
        timestamp = serializer.read_uint32()
        payload_size = serializer.read_uint16()
        
        # Lê o payload se existir
        payload = None
        if payload_size > 0:
            payload_data = data[serializer._read_offset:serializer._read_offset + payload_size]
            payload_serializer = BinarySerializer()
            payload_serializer.set_buffer(payload_data)
            
            if msg_type == MessageType.MOVE:
                payload = MotorCommand.deserialize(payload_serializer)
            elif msg_type == MessageType.GET_SENSORS:
                payload = SensorData.deserialize(payload_serializer)
        
        msg = cls(msg_type, payload)
        msg.timestamp = timestamp
        return msg

def example_usage():
    # Comando de movimento
    cmd = MotorCommand(
        position=Vector2D(100.5, 200.75),
        speed=50.0,
        acceleration=10.0
    )
    
    msg = Message(MessageType.MOVE, cmd)
    data = msg.serialize()
    
    # Deserializa
    received_msg = Message.deserialize(data)
    received_cmd = received_msg.payload
    
    print(f"Comando recebido:")
    print(f"Posição: ({received_cmd.position.x}, {received_cmd.position.y})")
    print(f"Velocidade: {received_cmd.speed}")
    print(f"Aceleração: {received_cmd.acceleration}")
    
    #  Dados dos sensores
    sensors = SensorData(
        temperature=25.5,
        humidity=60.0,
        distance=150.5,
        battery_level=85.5
    )
    
    msg = Message(MessageType.GET_SENSORS, sensors)
    data = msg.serialize()
    
    received_msg = Message.deserialize(data)
    received_sensors = received_msg.payload
    
    print(f"\nDados dos sensores:")
    print(f"Temperatura: {received_sensors.temperature}°C")
    print(f"Humidade: {received_sensors.humidity}%")
    print(f"Distância: {received_sensors.distance}cm")
    print(f"Bateria: {received_sensors.battery_level}%")

if __name__ == '__main__':
    example_usage()
