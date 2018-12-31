import time

import math

# from procbridge.procbridge import Client
# from rc_common import netcfg
from procbridge.procbridge import ProcBridge as Client

from drivers.xbox_controller import XboxController, Side


# todo create hot cli interface thing (TUI?, CURSES?, BLESSED?)
# TODO make video game like controls (proper reversing, gear shifting etc.)
from rc_common import netcfg
from rc_common.RC_Commands import Commands


def print_usage():
    print("Use Right Trigger to Move Forward, Left Trigger to Move Backwards")
    print("And Left Joystick to Turn")


def sigmoid(value, minimum, maximum, rate, offset):
    rel_max = maximum - minimum
    return (rel_max / (1 + (math.pow(math.e, (-rate * value + offset))))) + minimum


# MARK - Trigger settings
MIN_SPEED = 0
MAX_SPEED = 90
RATE = 24
OFFSET = 13.3

# MARK - Joystick Settings
TURN_THRESHOLD = 0.4

E_BRAKE_DEFAULT_COOLDOWN = 1.5  # seconds


def get_speed(trigger_value):
    return sigmoid(trigger_value, MIN_SPEED, MAX_SPEED, RATE, OFFSET)


def start():
    controller = XboxController()
    e_brake_enabled = False
    e_brake_cooldown = 0

    previous_time = time.time()

    client = None

    # MARK - Connect
    try:
        pass
        client = Client(netcfg.HOST, netcfg.HDW_PORT)
    except WindowsError:
        print("Error: unable to connect using static ip address")

    print_usage()

    while 1:
        # the triggers are processed with same branch to prevent duplicate controls being sent
        # todo debounce everything
        # print("controller stuff" + str(controller.RIGHT_TRIGGER.value))
        # if e_brake_cooldown <= 0:
        #     e_brake_enabled = False
        # else:
        #     e_brake_cooldown -= time.time() - previous_time
        #     previous_time = time.time()

        if controller.LEFT_JOYSTICK.X > TURN_THRESHOLD:
            print("turning right")
            client.request(Commands.RIGHT)
        elif controller.LEFT_JOYSTICK.X < -TURN_THRESHOLD:
            print("turning left")
            client.request(Commands.LEFT)

        # TODO Add cooldown with e-brake
        # if not e_brake_enabled:
        if controller.is_trigger_pressed(Side.RIGHT):
            speed = get_speed(controller.RIGHT_TRIGGER)
            print("sending speed to move forward " + str(speed))
            client.request(Commands.FORWARD, {"speed": speed})
        elif controller.is_trigger_pressed(Side.LEFT):
            speed = get_speed(controller.LEFT_TRIGGER)
            print("sending speed to move forward " + str(speed))
            client.request(Commands.FORWARD, {"speed": speed})

        # if controller.A:
        #     e_brake_enabled = True
        #     e_brake_cooldown = E_BRAKE_DEFAULT_COOLDOWN

        # print(str(controller.LEFT_JOYSTICK.Y) + " " * 32, end='\r', flush=True)
        # if controller.is_trigger_pressed(Side.RIGHT):
        #     pass
        # print("The Speed would be " + str(get_speed(controller.RIGHT_TRIGGER.value)) + " " * 32 + "\r", end='', flush=True)

        # print("\r", end='', flush=True)
        # print("\r")
        # elif controller.is_trigger_pressed(Side.LEFT):
        #     pass


if __name__ == '__main__':
    start()
