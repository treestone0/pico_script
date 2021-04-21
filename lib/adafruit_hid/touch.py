#  2021 Shuyan Liu
#
# 

"""
`adafruit_hid.touch.Touch`
====================================================

* Author(s): Shuyan Liu
"""
import time

from . import find_device


class Touch:
    """Send USB HID touch reports."""

    def __init__(self, devices, screen_width=1440, screen_height=2560):
        """Create a touch screen object that will send USB touch screnn HID reports.

        Devices can be a list of devices that includes a keyboard device or a keyboard device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._touch_device = find_device(devices, usage_page=0x0D, usage=0x04)
        self._screen_width = screen_width
        self._screen_height = screen_height

        # Reuse this bytearray to send touchscreen reports.
        # report[0] number of fingers, always 1
        # report[1] index of finger, can be any value
        # report[2] buttons pressed, 1st bit: touch?     2nd bit: in range?
        # report[3] x movement, LOW
        # report[4] x movement, HIGH
        # report[5] y movement, LOW
        # report[6] y movement, HIGH
        self.report = bytearray(7)
        self.report[0] = 1
        self.report[1] = 123

        # Do a no-op to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.move()
        except OSError:
            time.sleep(1)
            self.move()

    def press(self):
        self.report[2] = 3
        self._touch_device.send_report(self.report)

    def release(self):
        self.report[2] = 2
        self._touch_device.send_report(self.report)

    def click(self):
        self.press()
        time.sleep(0.1)
        self.release()

    def move(self, x=1, y=1):
        screen_x, screen_y = self._to_screen_coordinate(x, y)
        x_high, x_low = self._to_byte(screen_x)
        y_high, y_low = self._to_byte(screen_y)
        self.report[3] = x_low
        self.report[4] = x_high
        self.report[5] = y_low
        self.report[6] = y_high
        self._touch_device.send_report(self.report)
        
    def pan(self, start_x, start_y, end_x, end_y, input_steps=30):
        steps = float(input_steps)
        step_x = (end_x - start_x) / steps
        step_y = (end_y - start_y) / steps

        current_x = start_x
        current_y = start_y
        self.move(start_x, start_y)
        self.press()
        while steps > 0:
            # TODO: add some shakes here, so that it will not be a straight line
            self.move(current_x, current_y)
            current_x += step_x
            current_y += step_y
            steps -= 1
            time.sleep(20 / 1000.0)
        self.release()

    def click_at(self, x, y):
        self.move(x, y)
        self.click()

    def _get_low_byte(self, value):
        return value & 0xFF

    def _get_high_byte(self, value):
        return value >> 8 & 0xFF

    def _to_byte(self, value):
        result_high = self._get_high_byte(value)
        result_low = self._get_low_byte(value)
        return result_high, result_low

    def _bound(self, x, y):
        bounded_x = max(min(x, self._screen_width), 1)
        bounded_y = max(min(y, self._screen_height), 1)
        return bounded_x, bounded_y

    def _to_screen_coordinate(self, x, y):
        bounded_x, bounded_y = self._bound(x, y)
        screen_x = int(bounded_x * 10000.0 / self._screen_width)
        screen_y = int(bounded_y * 10000.0 / self._screen_height)
        return screen_x, screen_y
