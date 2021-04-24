import board
import common_functions as cf
import digitalio
import random
import sys
import time


def run(app):
    time.sleep(3)
    actionConfigs, actionPrioritySum, actionLookupTable = cf.prepare(app)
    defaultRunTime = int(actionConfigs.get("DEFAULT", "default_runtime"))
    defaultOffset = int(actionConfigs.get("DEFAULT", "default_offset"))
    randomAction = int(actionConfigs.get("DEFAULT", "random_action"))
    print(defaultRunTime, defaultOffset, randomAction)

    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT

    scriptStartTime = time.time()
    realRunTime = defaultRunTime + random.randint(-defaultOffset, defaultOffset)
    print("adding random offset, realRunTime:", realRunTime)
    timeout = time.time() + 60 * realRunTime

    actionSwitch = 0
    while True:
        if time.time() > timeout:
            break

        # random action
        if randomAction is 1:
            actionSwitch = random.randint(0, actionPrioritySum - 1)
        else:
            actionSwitch = (actionSwitch + 1) % actionPrioritySum

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

        closeCount = int(actionConfigs.get(actionName, "close2"))
        for closeNr in range(closeCount):
            print("close2", closeNr, end=' ', flush=True)
            cf.config_click_return2(actionConfigs, actionName, led)
            sleepOffset = random.randint(- defaultOffset * sleepFactor, defaultOffset * sleepFactor)
            time.sleep((sleepBase + sleepOffset) / 1000.0)

        sys.stdout.write("]\n")  # move the cursor to the next line
