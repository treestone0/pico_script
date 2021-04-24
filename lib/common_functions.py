from adafruit_hid.touch import Touch
from configparser import ConfigParser
import random
import time
import usb_hid

step_duration = 10  # 10ms each step
device_direction = 'middle'
record_direction = 'middle'
scree_width = 1440
scree_height = 2560


def prepare(app_name):
    # 1. deal with hardware config file
    hardware_config = ConfigParser()
    hardware_config.read("../config/config.ini")
    current_device = hardware_config.get("DEFAULT", "currentDevice")
    global scree_width, scree_height, device_direction
    scree_width = int(hardware_config.get(current_device, "width"))
    scree_height = int(hardware_config.get(current_device, "height"))
    device_direction = hardware_config.get(current_device, "direction")
    print(scree_width, scree_height, device_direction)

    # 2. deal with app related config file
    action_configs = ConfigParser()
    action_configs.read("../config/" + current_device + "/" + app_name + "_config.ini")
    global record_direction
    record_direction = action_configs.get("DEFAULT", "record_direction")
    print(record_direction)

    # 3. prepare action lookup table
    action_priority_sum = 0
    action_lookup_table = {}
    for config in action_configs.sections():
        # print(config)
        priority_begin = action_priority_sum
        action_priority_sum += int(action_configs.get(config, "priority"))
        priority_end = action_priority_sum
        action_lookup_table.update({(priority_begin, priority_end): config})
        # print(action_lookup_table)

    return action_configs, action_priority_sum, action_lookup_table


def get_config_name(action_lookup_table, action_switch):
    for key in action_lookup_table:
        if key[0] <= action_switch < key[1]:
            return action_lookup_table[key]


def blick(led, times, duration):
    for i in range(times):
        led.value = True
        time.sleep(duration)
        led.value = False
        time.sleep(duration)


def config_click_at(action_configs, action_name, led):
    x = int(action_configs.get(action_name, "x"))
    y = int(action_configs.get(action_name, "y"))
    default_offset = int(action_configs.get(action_name, "default_offset"))
    random_shift1 = random.randint(-default_offset, default_offset)
    random_shift2 = random.randint(-default_offset, default_offset)
    touch = Touch(usb_hid.devices, scree_width, scree_height)
    touch.click_at(x + random_shift1, y + random_shift2)
    blick(led, 2, 0.1)


def config_click_return(action_configs, action_name, led):
    x = int(action_configs.get(action_name, "close_x"))
    y = int(action_configs.get(action_name, "close_y"))
    default_offset = int(action_configs.get(action_name, "default_offset"))
    random_shift1 = random.randint(-default_offset, default_offset)
    random_shift2 = random.randint(-default_offset, default_offset)
    touch = Touch(usb_hid.devices, scree_width, scree_height)
    touch.click_at(x + random_shift1, y + random_shift2)
    blick(led, 3, 0.1)


def config_click_return2(action_configs, action_name, led):
    x = int(action_configs.get(action_name, "close2_x"))
    y = int(action_configs.get(action_name, "close2_y"))
    default_offset = int(action_configs.get(action_name, "default_offset"))
    random_shift1 = random.randint(-default_offset, default_offset)
    random_shift2 = random.randint(-default_offset, default_offset)
    touch = Touch(usb_hid.devices, scree_width, scree_height)
    touch.click_at(x + random_shift1, y + random_shift2)
    blick(led, 3, 0.1)


def pan_in_safe_area(min_x, min_y, max_x, max_y, input_steps=40, dist_threshold=300):
    start_x = random.randint(min(min_x, max_x), max(min_x, max_x))
    start_y = random.randint(min(min_y, max_y), max(min_y, max_y))
    end_x = random.randint(min(min_x, max_x), max(min_x, max_x))
    end_y = random.randint(min(min_y, max_y), max(min_y, max_y))
    while True:
        distance2 = (end_y - start_y) * (end_y - start_y) + (end_x - start_x) * (end_x - start_x)
        if distance2 < dist_threshold * dist_threshold:
            start_x = random.randint(min(min_x, max_x), max(min_x, max_x))
            start_y = random.randint(min(min_y, max_y), max(min_y, max_y))
            end_x = random.randint(min(min_x, max_x), max(min_x, max_x))
            end_y = random.randint(min(min_y, max_y), max(min_y, max_y))
        else:
            break
    touch = Touch(usb_hid.devices, scree_width, scree_height)
    touch.pan(start_x, start_y, end_x, end_y, input_steps)


def config_pan_in_safe_area(action_configs, action_name, led):
    min_x = int(action_configs.get(action_name, "min_x"))
    min_y = int(action_configs.get(action_name, "min_y"))
    max_x = int(action_configs.get(action_name, "max_x"))
    max_y = int(action_configs.get(action_name, "max_y"))
    default_touch_time = int(action_configs.get(action_name, "default_touch_time"))
    default_offset = int(action_configs.get(action_name, "default_offset"))
    random_steps = default_touch_time + random.randint(-default_offset, default_offset)
    led.value = True
    pan_in_safe_area(min_x, min_y, max_x, max_y, random_steps)
    led.value = False

