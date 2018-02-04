import time
import begin
from datetime import datetime

from i2c_lcd import I2cLcd
from weather_handler import AirlyHandler, OpenWeatherHandler


DEFAULT_I2C_ADDR = 0x27

celsius = bytearray([0x08, 0x14, 0x08, 0x03, 0x04, 0x04, 0x04, 0x03])
pm = bytearray([0x1C, 0x12, 0x1C, 0x10, 0x00, 0x1B, 0x15, 0x11])
two = bytearray([0x00, 0x00, 0x08, 0x14, 0x04, 0x08, 0x10, 0x1D])
five = bytearray([0x00, 0x00, 0x1C, 0x10, 0x18, 0x04, 0x04, 0x18])
ten = bytearray([0x00, 0x00, 0x12, 0x15, 0x15, 0x15, 0x15, 0x12])

h = bytearray([0x00, 0x00, 0x11, 0x11, 0x11, 0x1D, 0x15, 0x15])
pa = bytearray([0x00, 0x00, 0x18, 0x08, 0x18, 0x06, 0x0A, 0x0F])


class Display(object):
    def __init__(self, airly_handler, open_weather_handler):
        self.airly_handler = airly_handler
        self.open_weather_handler = open_weather_handler
        self.lcd = I2cLcd(1, DEFAULT_I2C_ADDR, 2, 16)
        self.airly = None
        self.open_weather = None
        self.addCustomChars()

    def addCustomChars(self):
        self.lcd.custom_char(0, celsius)
        self.lcd.custom_char(1, pm)
        self.lcd.custom_char(2, two)
        self.lcd.custom_char(3, five)
        self.lcd.custom_char(4, ten)
        self.lcd.custom_char(5, h)
        self.lcd.custom_char(6, pa)

    def writeDateTime(self, line):
        """Print TIME on first line"""
        self.lcd.move_to(0, line)
        self.addTime()

    def writeTempPm(self, line):
        """Print TEMP PM10 PM25 on second line"""
        self.lcd.move_to(0, line)
        self.addTemp()
        self.addSpace()
        self.addPM10()
        self.addSpace()
        self.addPM25()

    def writeTempHumPress(self, line):
        """Print TEMP PM10 PM25 on second line"""
        self.lcd.move_to(0, line)
        self.addTemp()
        self.addSpace()
        self.addHumidity()
        self.addSpace()
        self.addPressure()

    def addTime(self):
        """HH:MM DD-MM-YYYY"""
        self.lcd.putstr(time.strftime("%H:%M %d-%m-%Y", datetime.now().timetuple()))

    def addTemp(self):
        """(-)temp(C)"""
        self.lcd.putstr(str(self.open_weather.temp))
        self.lcd.putchar(chr(0))

    def addHumidity(self):
        """hum(%)"""
        self.lcd.putstr(str(self.open_weather.humidity))
        self.lcd.putstr("%")

    def addPressure(self):
        """press(hP)(a)"""
        self.lcd.putstr(str(int(self.open_weather.pressure)))
        self.lcd.putchar(chr(5))
        self.lcd.putchar(chr(6))

    def addPM10(self):
        """pm10(pm)(10)"""
        self.lcd.putstr(str(self.airly.pm10))
        self.lcd.putchar(chr(1))
        self.lcd.putchar(chr(4))

    def addPM25(self):
        """pm25(pm)(2.)(5)"""
        self.lcd.putstr(str(self.airly.pm25))
        self.lcd.putchar(chr(1))
        self.lcd.putchar(chr(2))
        self.lcd.putchar(chr(3))

    def addSpace(self):
        """( )"""
        self.lcd.putstr(' ')

    def updateResult(self):
        self.airly = self.airly_handler.getCurrentWeather('50.07874', '20.02901')
        self.open_weather = self.open_weather.getCurrentWeather('50.07874', '20.02901')

    def mainLoop(self):
        while True:
            self.updateResult()
            self.lcd.clear()
            self.writeDateTime(0)
            self.writeTempPm(1)
            time.sleep(15)
            self.writeTempHumPress(1)
            time.sleep(15)


@begin.start
def run(airly_apikey, open_weather_apikey):
    airly_handler = AirlyHandler(airly_apikey)
    open_weather_handler = OpenWeatherHandler(open_weather_apikey)
    display = Display(airly_handler, open_weather_handler)

    display.mainLoop()
