from lcd_i2c import lcd_byte, lcd_init, lcd_string, LCD_LINE_1, LCD_LINE_2, LCD_CMD
from weather_clock import getData
import time


class DisplayViews(object):
    def __init__(self):
        self.screen = 0

    def mainView(self):
        """
        __HH:MM_DD-MM-RRRR__ 20
        _+XX(oC)_XXX(pm)(2)(5)_XXX(pm)(1)(0)_ 20
        :return: 
        """
        line_1 = ''
        line_2 = ''
        return line_1, line_2


def main():
    lcd_init()
    counter = 0
    result = None

    while True:
        if counter == 0:
            result = getData()
            counter = 5

        if result:
            lcd_string(result.getDateTime(), LCD_LINE_1)
            lcd_string(result.getTempPm(), LCD_LINE_2)

        else:
            print("Result {}".format(result))

        time.sleep(60)
        counter -= 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
