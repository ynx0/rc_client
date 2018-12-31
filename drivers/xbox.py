import math
from procbridge.procbridge import ProcBridge as Client

from drivers.xbox_controller import XboxController, Side
from rc_common import netcfg
from rc_common.RC_Commands import Commands


# todo create hot cli interface thing (TUI?, CURSES?, BLESSED?)
# TODO make video game like controls (proper reversing, gear shifting etc.)

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

STOP_THRESHOLD = 10  # all values below this value send a stop command instead of an infinitesimal speed value



def get_speed(trigger_value):
    return sigmoid(trigger_value, MIN_SPEED, MAX_SPEED, RATE, OFFSET)


def start():
    controller = XboxController()
    # debouncer = ButtonDebouncer(0.15)

    client = None

    # MARK - Connect
    try:
        pass
        client = Client(netcfg.HOST, netcfg.HDW_PORT)
    except WindowsError:
        print("Error: unable to connect using static ip address")

    print_usage()

    while 1:

        # braking
        if controller.A is True:

            print('e-brake enabled')

            print('sending stop command')
            client.request(Commands.STOP)
            continue  # skip all other controls processing


        # turning


        # the triggers are processed with same branch to prevent duplicate controls being sent
        if controller.LEFT_JOYSTICK.X > TURN_THRESHOLD:
            print("turning right")
            client.request(Commands.RIGHT)
        elif controller.LEFT_JOYSTICK.X < -TURN_THRESHOLD:
            print("turning left")
            client.request(Commands.LEFT)

        # forward and backward motion
        forward_speed = get_speed(controller.RIGHT_TRIGGER.value)
        backward_speed = get_speed(controller.LEFT_TRIGGER.value)

        if (controller.is_trigger_pressed(Side.RIGHT) and forward_speed <= STOP_THRESHOLD) \
                or (controller.is_trigger_pressed(Side.LEFT) and backward_speed <= STOP_THRESHOLD):
            # if a trigger is pressed and it is less than the stopping threshold, we gotta stop
            print('stopping')
            client.request(Commands.STOP)
        else:
            # print("sending speed to move forward " + str(speed))
            # target_speed = max(forward_speed, backward_speed)  # only send bigger of either speed
            if forward_speed > backward_speed:
                print('going forward ' + str(forward_speed))
                client.request(Commands.FORWARD, {"speed": forward_speed})
            elif backward_speed > forward_speed:
                print('going backward ' + str(backward_speed))
                client.request(Commands.BACKWARD, {"speed": backward_speed})
            else:
                # Stop pressing down both triggers you buffoon
                pass


if __name__ == '__main__':
    start()
