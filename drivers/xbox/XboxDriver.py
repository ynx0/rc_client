import math

from drivers.Driver import Driver
from drivers.xbox.xbox_controller import XboxController, Side
from rc_common.RC_Commands import Commands


# todo create hot cli interface thing (TUI?, CURSES?, BLESSED?)
# TODO make video game like controls (proper reversing, gear shifting etc.)


class XboxDriver(Driver):
    def __init__(self, name, drv_id, options=None):
        super().__init__(name, drv_id)

        if options is None:  # thank u intellij very cool
            options = {}  # https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments

        # MARK - Trigger settings
        self.MIN_SPEED = options.get('MIN_SPEED', 0)
        self.MAX_SPEED = options.get('MAX_SPEED', 90)
        self.RATE = options.get('RATE', 24)
        self.OFFSET = options.get('OFFSET', 13.3)

        # MARK - Joystick Settings
        self.TURN_THRESHOLD = options.get('TURN_THRESHOLD', 0.4)
        self.STOP_THRESHOLD = options.get('STOP_THRESHOLD', 5)  # uses raw controller values [0, 255]
        # all values below this value send a stop command instead of an smaller and smaller speed value

        # checks
        assert 0 <= self.STOP_THRESHOLD <= 255


        self.controller = XboxController()

    @staticmethod
    def print_usage():
        print("Use Right Trigger to Move Forward, Left Trigger to Move Backwards")
        print("And Left Joystick to Turn")

    @staticmethod
    def sigmoid(value, minimum, maximum, rate, offset):
        rel_max = maximum - minimum
        return (rel_max / (1 + (math.pow(math.e, (-rate * value + offset))))) + minimum

    @staticmethod
    def linear(x, m, b):
        # x is the value to map
        # m is rate of change
        # b is y intercept
        return m * x + b

    def get_speed(self, trigger_value):
        # TRIGGERED REEEEEEEEEEEEEEE
        return self.linear(trigger_value, self.MAX_SPEED, self.MIN_SPEED)
        # return self.sigmoid(trigger_value, self.MIN_SPEED, self.MAX_SPEED, self.RATE, self.OFFSET)

    def start(self):
        # debouncer = ButtonDebouncer(0.15)
        controller = self.controller

        self.print_usage()

        client = self.get_client()

        while 1:
            if not controller.RIGHT_TRIGGER.raw_value == 0:
                print("percent right: {}".format(controller.RIGHT_TRIGGER.value))

            # braking
            if controller.B is True:
                print('e-brake enabled')
                client.request(Commands.STOP)
                continue  # skip all other controls processing

            # turning
            # the triggers are processed with same branch to prevent duplicate controls being sent
            if controller.LEFT_JOYSTICK.X > self.TURN_THRESHOLD:
                print("turning right")
                client.request(Commands.RIGHT)
            elif controller.LEFT_JOYSTICK.X < self.TURN_THRESHOLD * -1:
                print("turning left")
                client.request(Commands.LEFT)

            # forward and backward motion
            forward_speed = self.get_speed(controller.RIGHT_TRIGGER.value)
            backward_speed = self.get_speed(controller.LEFT_TRIGGER.value)

            # we use the raw value because the 
            if controller.RIGHT_TRIGGER.raw_value <= self.STOP_THRESHOLD and not controller.LEFT_TRIGGER.raw_value > 0:  # \
                # if a trigger is pressed and it is less than the stopping threshold, we gotta stop
                # also make sure that the other one is not being pressed so as not to interfere with the controls
                print('stopping')
                client.request(Commands.STOP)

            elif controller.LEFT_TRIGGER.raw_value <= self.STOP_THRESHOLD and not controller.RIGHT_TRIGGER.raw_value > 0:
                # same deal here
                print('stopping')
                client.request(Commands.STOP)
            else:

                if forward_speed > backward_speed:
                    print('going forward ' + str(forward_speed))
                    client.request(Commands.FORWARD, {"speed": forward_speed})
                elif backward_speed > forward_speed:
                    print('going backward ' + str(backward_speed))
                    client.request(Commands.BACKWARD, {"speed": backward_speed})
                else:
                    # Stop pressing down both triggers you buffoon
                    pass
