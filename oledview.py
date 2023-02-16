from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import ImageFont
import time
import hrcalc
import max30102

font = ImageFont.truetype('./font.ttf', 18)
def stats(oled,hr,spo2,truedata):
    with canvas(oled) as draw:
        draw.rectangle(oled.bounding_box, outline="blue", fill="black")
        if truedata :
            draw.text((2, 5), "心率 %s" %hr, font=font, fill=255)
            draw.text((2, 25), "血氧 %.2f" %spo2, font=font, fill=255)
        else :
            draw.text((5, 20), "请正确放置手指" , font=font, fill=255)

def main():
    serial = i2c(port=1, address=0x3C)
    oled = ssd1306(serial)
    m = max30102.MAX30102()
    while True:
        red, ir = m.read_sequential()
        hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir, red)
        if hr_valid and spo2_valid :
            stats(oled,hr,spo2,truedata = True)
        else :
            stats(oled,hr,spo2,truedata = False)
     
        #time.sleep(1)

if __name__ == "__main__":
    main()
