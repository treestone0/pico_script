import time
import usb_hid
from adafruit_hid.touch import Touch


def run():
    time.sleep(5)

    touch = Touch(usb_hid.devices, 1440, 2560)

    while True:
        touch.click_at(1331, 2451)  # start
        time.sleep(3)

        touch.click_at(1180, 66)  # >>
        time.sleep(110)

        touch.click_at(324, 2288)  # replay
        time.sleep(5)
