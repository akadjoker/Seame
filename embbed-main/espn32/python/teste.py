from machine import Pin
import time

led = Pin(2, Pin.OUT)    # LED embutido na maioria das ESP32

while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)