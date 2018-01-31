import time
import begin
from i2c_lcd import I2cLcd
from weather_clock import RequestHandler
from datetime import datetime

DEFAULT_I2C_ADDR = 0x27

celsius = bytearray([0x08, 0x14, 0x08, 0x03, 0x04, 0x04, 0x04, 0x03])
pm = bytearray([0x1C, 0x12, 0x1C, 0x10, 0x00, 0x1B, 0x15, 0x11])
two = bytearray([0x00, 0x00, 0x08, 0x14, 0x04, 0x08, 0x10, 0x1D])
five = bytearray([0x00, 0x00, 0x1C, 0x10, 0x18, 0x04, 0x04, 0x18])
ten = bytearray([0x00, 0x00, 0x12, 0x15, 0x15, 0x15, 0x15, 0x12])


class Display(object):
    def __init__(self, request_handler):
        self.req_handler = request_handler
        self.lcd = I2cLcd(1, DEFAULT_I2C_ADDR, 2, 16)
        self.result = None
        self.addCustomChars()

    def addCustomChars(self):
        self.lcd.custom_char(0, celsius)
        self.lcd.custom_char(1, pm)
        self.lcd.custom_char(2, two)
        self.lcd.custom_char(3, five)
        self.lcd.custom_char(4, ten)

    def writeDateTime(self):
        self.lcd.move_to(0, 0)
        self.lcd.putstr(time.strftime("%H:%M %d-%m-%Y", datetime.now().timetuple()))

    def writeTempPm(self):
        self.lcd.move_to(0, 1)
        self.lcd.putstr(str(self.result.temperature))
        self.lcd.putchar(chr(0))
        self.lcd.putstr(' ')
        self.lcd.putstr(str(self.result.pm10))
        self.lcd.putchar(chr(1))
        self.lcd.putchar(chr(4))
        self.lcd.putstr(' ')
        self.lcd.putstr(str(self.result.pm25))
        self.lcd.putchar(chr(1))
        self.lcd.putchar(chr(2))
        self.lcd.putchar(chr(3))

    def mainLoop(self):
        while True:
            self.lcd.clear()
            self.writeDateTime()
            self.writeTempPm()

            time.sleep(60)


@begin.start
def run(apikey):
    req_handler = RequestHandler(apikey)
    display = Display(req_handler)

    display.mainLoop()
