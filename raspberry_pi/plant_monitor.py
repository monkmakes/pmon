import serial
import time

class PlantMonitor:
    """A Class for the MonkMakes Plant Monitor"""

    wetness = 0
    temp = 0
    humidity = 0
    ser = None
    delay_period = 0.1

    def __init__(self):
         self.ser = serial.Serial("/dev/serial0", 9600)

    def get_wetness(self):
        self.send("w")
        self._wait_for_message()
        return self.wetness

    def get_temp(self):
        self.send("t")
        self._wait_for_message()
        return self.temp

    def get_humidity(self):
        self.send("h")
        self._wait_for_message()
        return self.humidity

    def led_off(self):
        self.send("l")

    def led_on(self):
        self.send("L")

    def send(self, message):
        self.ser.write(bytes(message+"\n", 'utf-8'))
        time.sleep(self.delay_period)

    def _wait_for_message(self):
        time.sleep(self.delay_period) # give attiny time to respond
        incoming_message = str(self.ser.readline()[:-2].decode("utf-8"))  # rem>
        message_parts = incoming_message.split("=")
        if len(message_parts) == 2:
            code, value = message_parts
            if code == "w":
                self.wetness = float(value)
            elif code == "t":
                self.temp = float(value)
            elif code == "h":
                self.humidity = float(value)
        