#
# Controller UI Class for Color LCD Display (for M5STACK S3ATOM)
#
# v0.01 2025/8/16  1st release
# v0.02 2025/8/16  
#  Feature: Implement string length limit of 16 characters
#

#
# setup external libraries for LCD Display Controller
#
# Please retrieve the modules st7789py.py, vga1_8x8.py and tft_config.py 
# from repository https://github.com/russhughes/st7789py_mpy/tree/master 
# and place them in the /lib directory.

import tft_config
import st7789py as st7789
import vga1_8x8

LCD_WIDTH_SIZE = 128
LCD_HEIGHT_SIZE = 128

class ControllerUI:

    def __init__(self):
        self.lcd = tft_config.config(tft_config.WIDE)
        self.lcd_clear()
        self.UI_TEXT1_POS = (0, 10)
        self.UI_TEXT2_POS = (0, 20)
        self.UI_TEXT3_POS = (0, 30)

    def lcd_clear(self, color = st7789.BLACK):
        self.lcd.fill(color)

    def lcd_draw_text(self, x, y, text, trancate_16 = True, fg=st7789.WHITE, bg=st7789.BLACK):
        font_height = 8
        self.lcd.fill_rect(x, y, LCD_WIDTH_SIZE, font_height, bg)
        if trancate_16 and len(text) > 16:
           text_tr = text[:4] + '..' + text[-10:]   # reason of -10 ,  16(max len) - 4(prefix) - 2(..) = 10
        else:
           text_tr = text
        self.lcd.text(vga1_8x8, text_tr, x, y, fg, bg)

    def lcd_draw_line(self, x0, y0, x1, y1, color=st7789.WHITE):
        self.lcd.line(x0, y0, x1, y1, color)

    def lcd_fill_rect(self, x, y, w, h, color=st7789.BLACK):
        self.lcd.fill_rect(x, y, w, h, color)

