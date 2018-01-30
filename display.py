from i2c_lcd import I2cLcd
from weather_clock import getData
import time
from datetime import datetime

DEFAULT_I2C_ADDR = 0x27

celsius = bytearray([0x08, 0x14, 0x08, 0x03, 0x04, 0x04, 0x04, 0x03])
pm = bytearray([0x1C, 0x12, 0x1C, 0x10, 0x00, 0x1B, 0x15, 0x11])
two = bytearray([0x00, 0x04, 0x0A, 0x02, 0x04, 0x08, 0x0E, 0x00])
five = bytearray([0x00, 0x07, 0x04, 0x06, 0x01, 0x01, 0x16, 0x10])
ten = bytearray([0x00, 0x12, 0x15, 0x15, 0x15, 0x15, 0x12, 0x00])

class Display(object):
    def __init__(self):
        self.lcd = I2cLcd(1, DEFAULT_I2C_ADDR, 2, 16)
        self.result = None
        self.addCustomChars()
        self.mainLoop()

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
        self.lcd.putstr(self.result.temperature)
        self.lcd.putchar(0)
        self.lcd.putstr(' ')
        self.lcd.putstr(self.result.pm10)
        self.lcd.putchar(4)
        self.lcd.putstr(' ')
        self.lcd.putstr(self.result.pm25)
        self.lcd.putchar(2)
        self.lcd.putchar(3)

    def mainLoop(self):
        """
        __HH:MM_DD-MM-RRRR__ 16
        _+XX(oC)_XXX(pm)(2)(5)_XXX(pm)(10)_ 16
        :return: 
        """
        counter = 0
        while True:
            if counter == 0:
                self.result = getData()
                counter = 5

            if self.result:
                self.writeDateTime()
                self.writeTempPm()

            else:
                print("Result {}".format(self.result))

            time.sleep(60)
            counter -= 1

if __name__ == '__main__':
    display = Display()

