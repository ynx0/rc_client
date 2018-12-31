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
            options = {}     # https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments

        # MARK - Trigger settings
        self.MIN_SPEED = options.get('MIN_SPEED', 0)
        self.MAX_SPEED = options.get('MAX_SPEED', 90)
        self.RATE = options.get('RATE', 24)
        self.OFFSET = options.get('OFFSET', 13.3)

        # MARK - Joystick Settings
        self.TURN_THRESHOLD = options.get('TURN_THRESHOLD', 0.4)
        self.STOP_THRESHOLD = options.get('STOP_THRESHOLD',
                                          10)  # all values below this value send a stop command instead of an smaller and smaller speed value

        self.controller = XboxController()

    @staticmethod
    def print_usage():
        print("Use Right Trigger to Move Forward, Left Trigger to Move Backwards")
        print("And Left Joystick to Turn")

    @staticmethod
    def sigmoid(value, minimum, maximum, rate, offset):
        rel_max = maximum - minimum
        return (rel_max / (1 + (math.pow(math.e, (-rate * value + offset))))) + minimum

    def get_speed(self, trigger_value):
        # TRIGGERED REEEEEEEEEEEEEEE
        return self.sigmoid(trigger_value, self.MIN_SPEED, self.MAX_SPEED, self.RATE, self.OFFSET)

    def start(self):
        # debouncer = ButtonDebouncer(0.15)
        controller = self.controller

        self.print_usage()

        client = self.get_client()

        while 1:

            # braking
            if controller.B is True:
                print('e-brake enabled')

                print('sending stop command')
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

            if (controller.is_trigger_pressed(Side.RIGHT) and forward_speed <= self.STOP_THRESHOLD) \
                    or (controller.is_trigger_pressed(Side.LEFT) and backward_speed <= self.STOP_THRESHOLD):
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
