import board
import common_functions as cf
import digitalio
import random
import sys
import time

time.sleep(3)
actionConfigs, actionPrioritySum, actionLookupTable = cf.prepare("family")
defaultRunTime = int(actionConfigs.get("DEFAULT", "default_runtime"))
defaultOffset = int(actionConfigs.get("DEFAULT", "default_offset"))
print(defaultRunTime, defaultOffset)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

scriptStartTime = time.time()
realRunTime = defaultRunTime + random.randint(-defaultOffset, defaultOffset)
print("adding random offset, realRunTime:", realRunTime)
timeout = time.time() + 60 * realRunTime

while True:
    if time.time() > timeout:
        break

    # random action
    actionSwitch = random.randint(0, actionPrioritySum - 1)

    # fetch action name
    actionName = cf.get_config_name(actionLookupTable, actionSwitch)
    sleepBase = int(actionConfigs.get(actionName, "sleep_base"))
    sleepFactor = int(actionConfigs.get(actionName, "sleep_factor"))

    scriptRunTime = time.time() - scriptStartTime

    print(int(scriptRunTime),
          '\tactionSwitch\t', actionConfigs.get(actionName, "description"), end=' \t[ ', flush=True)

    clickCount = int(actionConfigs.get(actionName, "click"))
    for clickNr in range(clickCount):
        print("click", clickNr, end=' ', flush=True)
        cf.config_click_at(actionConfigs, actionName, led)
        sleepOffset = random.randint(- defaultOffset * sleepFactor, defaultOffset * sleepFactor)
        time.sleep((sleepBase + sleepOffset) / 1000.0)

    panCount = int(actionConfigs.get(actionName, "pan"))
    for panNr in range(panCount):
        print("pan", panNr, end=' ', flush=True)
        cf.config_pan_in_safe_area(actionConfigs, actionName, led)
        sleepOffset = random.randint(- defaultOffset * sleepFactor, defaultOffset * sleepFactor)
        time.sleep((sleepBase + sleepOffset) / 1000.0)

    closeCount = int(actionConfigs.get(actionName, "close"))
    for closeNr in range(closeCount):
        print("close", closeNr, end=' ', flush=True)
        cf.config_click_return(actionConfigs, actionName, led)
        sleepOffset = random.randint(- defaultOffset * sleepFactor, defaultOffset * sleepFactor)
        time.sleep((sleepBase + sleepOffset) / 1000.0)

    sys.stdout.write("]\n")  # move the cursor to the next line
