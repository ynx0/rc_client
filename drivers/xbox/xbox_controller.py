from enum import Enum, auto
from threading import Thread

import inputs
from inputs import UnpluggedError


# TODO Move all these classes to separate files

# Utility method, based on (https://stackoverflow.com/a/19057494/3807967)
class Range:
    def __init__(self, min_val, max_val):
        self.min = min_val
        self.max = max_val


def normalize(value, old_range: Range, new_range: Range):
    # scale = (new_range.max - new_range.min) / (old_range.max - old_range.min)
    # return (value - old_range.min) * scale
    # new algorithm adapted from https://stats.stackexchange.com/a/178629/144901
    return (new_range.max - new_range.min) * ((value - old_range.min) / (old_range.max - old_range.min)) + new_range.min


class ButtonMap(Enum):
    A = 'BTN_SOUTH'
    B = 'BTN_EAST'
    X = 'BTN_WEST'
    Y = 'BTN_NORTH'
    RIGHT_BUMPER = RB = 'BTN_TR'
    LEFT_BUMPER = LB = 'BTN_TL'
    RJOY_BTN = 'BTN_THUMBR'
    LJOY_BTN = 'BTN_THUMBL'
    START = 'BTN_START'
    SELECT = 'BTN_SELECT'
    DPAD = 'ABS_HAT0'


class AxesMap(Enum):
    JOY_PREAMBLE = 'ABS_'
    LJOY_X = 'ABS_X'
    LJOY_Y = 'ABS_Y'
    RJOY_X = 'ABS_RX'
    RJOY_Y = 'ABS_RY'
    LEFT_TRIGGER = 'ABS_Z'
    RIGHT_TRIGGER = 'ABS_RZ'


class DPAD:
    def __init__(self):
        self.UP = False
        self.DOWN = False
        self.RIGHT = False
        self.LEFT = False


class Side(Enum):
    LEFT = auto()
    RIGHT = auto()


# noinspection PyPep8Naming
class Joystick:
    def __init__(self, side: Side):
        self._side = side
        self.RAW_X = 0
        self.RAW_Y = 0
        # MARK - Normalization
        self.__JOYSTICK_RANGE = Range(-32768, 32767)
        self.__JOY_TARGET_RANGE = Range(-1, 1)

    @property
    def side(self):
        return self._side

    @property
    def X(self):
        return self.__normalize(self.RAW_X)

    @property
    def Y(self):
        return self.__normalize(self.RAW_Y)

    def __normalize(self, value):
        return normalize(value, self.__JOYSTICK_RANGE, self.__JOY_TARGET_RANGE)


class Trigger:
    def __init__(self, side):
        self._side = side
        self.raw_value = 0
        # MARK - Normalization
        self.__TRIGGER_RANGE = Range(0, 255)
        self.__TRIGGER_TARGET_RANGE = Range(0, 1)

    @property
    def side(self):
        return self._side

    @property
    def value(self):
        return self.__normalize(self.raw_value)

    def __normalize(self, value):
        return normalize(value, self.__TRIGGER_RANGE, self.__TRIGGER_TARGET_RANGE)


class XboxController:

    def __init__(self, controller_num=0):
        try:
            self.xbox = inputs.devices.gamepads[controller_num]
        except NameError:
            # todo, have better logic/handling, maybe not error out and use an "initialized variable", and keep polling for xbox?
            raise UnpluggedError("Error: Xbox connected gamepad")

        self.controller_num = controller_num
        self.plugged_in = True
        self.RIGHT_Z = 0
        self.LEFT_Z = 0
        self.A = False
        self.B = False
        self.X = False
        self.Y = False
        self.RIGHT_BUMPER = False
        self.LEFT_BUMPER = False
        self.RJOY_BTN = False
        self.LJOY_BTN = False
        self.START = False
        self.SELECT = False
        self.DPAD = DPAD()
        self.LEFT_JOYSTICK = Joystick(Side.LEFT)
        self.RiGHT_JOYSTICK = Joystick(Side.RIGHT)
        self.LEFT_TRIGGER = Trigger(Side.LEFT)
        self.RIGHT_TRIGGER = Trigger(Side.RIGHT)

        self.event_thread = Thread(target=self.xbox_event_loop, name="Xbox Event Thread")
        self.event_thread.daemon = True  # important, allows program to exit even if this thread is not finished, which is always true so you need this
        self.event_thread.start()

    def xbox_event_loop(self):
        print("Starting")
        while 1:
            if self.is_hardware_pluggedin():
                self.plugged_in = True
                event = None

                try:
                    event = self.xbox.read()[0]
                except UnpluggedError:
                    # this should never happen
                    # but we still need it to be "graceful"
                    self.plugged_in = False

                if event.code is not 'SYN_REPORT':
                    self.handle_event(event)
            else:
                print('Waiting for xbox to reconnect')
                self.plugged_in = False

    def is_hardware_pluggedin(self):
        gamepads = inputs.devices.gamepads
        return len(gamepads) and gamepads[self.controller_num] is not None

    def handle_event(self, event):
        # print("code" + event.code)
        # print(event.code is AxesMap.RIGHT_TRIGGER.value)
        # print("trigger is" + str(self.RIGHT_TRIGGER.raw_value))
        event_code = event.code
        event_value = event.state
        # MARK - Button Handling: ABXY
        if event_code is ButtonMap.A.value:
            self.A = bool(event_value)
        elif event_code is ButtonMap.B.value:
            self.B = bool(event_value)
        elif event_code is ButtonMap.X.value:
            self.X = bool(event_value)
        elif event_code is ButtonMap.Y.value:
            self.Y = bool(event_value)

        # MARK - Bumper Handling
        elif event_code is ButtonMap.RIGHT_BUMPER.value:
            self.RIGHT_BUMPER = bool(event_value)
        elif event_code is ButtonMap.LEFT_BUMPER.value:
            self.LEFT_BUMPER = bool(event_value)

        # MARK - Joystick Click Button Handling
        elif event_code is ButtonMap.RJOY_BTN.value:
            self.RJOY_BTN = bool(event_value)
        elif event_code is ButtonMap.LJOY_BTN.value:
            self.LJOY_BTN = bool(event_value)

        # MARK - Misc Button Handling
        elif event_code is ButtonMap.START.value:
            self.START = bool(event_value)
        elif event_code is ButtonMap.SELECT.value:
            self.SELECT = bool(event_value)

        # MARK - DPAD Handling
        elif event_code.startswith(ButtonMap.DPAD.value):
            self.handle_dpad(event_code, event_value)

        # MARK - Handle Joysticks (RAW_X and RAW_Y axes)
        elif event_code.startswith(
                AxesMap.JOY_PREAMBLE.value) and "Z" not in event_code:  # the code starts with the joystick preamble and is not the z axis
            self.handle_joysticks(event_code, event_value)

        # MARK - Handle Triggers
        elif event_code is AxesMap.LEFT_TRIGGER.value or event_code is AxesMap.RIGHT_TRIGGER.value:
            self.handle_triggers(event_code, event_value)

        else:
            print("Unknown code: " + event_code + " with state: " + str(event_value))

    def handle_dpad(self, code, state):
        if code is "ABS_HAT0Y":
            if state is 1:
                self.DPAD.DOWN = True
            elif state is -1:
                self.DPAD.UP = True
            elif state is 0:
                self.DPAD.UP = False
                self.DPAD.DOWN = False
        elif code is "ABS_HAT0X":
            if state is 1:
                self.DPAD.RIGHT = True
            elif state is -1:
                self.DPAD.LEFT = True
            elif state is 0:
                self.DPAD.LEFT = False
                self.DPAD.RIGHT = False

    def handle_joysticks(self, code, state):
        # Handle Left Joystick
        if code is AxesMap.LJOY_X.value:
            self.LEFT_JOYSTICK.RAW_X = state
        elif code is AxesMap.LJOY_Y.value:
            self.LEFT_JOYSTICK.RAW_Y = state
        # Handle Right Joystick
        elif code is AxesMap.RJOY_X.value:
            self.RiGHT_JOYSTICK.RAW_X = state
        elif code is AxesMap.RJOY_Y.value:
            self.RiGHT_JOYSTICK.RAW_Y = state

    def handle_triggers(self, code, state):
        # print("state is " + str(state))
        # print("Code: " + code + "axesmap" + AxesMap.LEFT_TRIGGER.value)
        # print(code is AxesMap.LEFT_TRIGGER.value)
        if code is AxesMap.LEFT_TRIGGER.value:
            self.LEFT_TRIGGER.raw_value = state
        elif code is AxesMap.RIGHT_TRIGGER.value:
            self.RIGHT_TRIGGER.raw_value = state

    def is_trigger_pressed(self, side: Side):
        if side is Side.LEFT:
            return self.LEFT_TRIGGER.value > 0
        elif side is Side.RIGHT:
            return self.RIGHT_TRIGGER.value > 0

    # def get_trigger(self, side):
    #     if side is Side.LEFT:
    #         return self
    #     elif side is Side.RIGHT:
    #         return self.__get_normalized_trigger(self.RIGHT_TRIGGER)

    # def get_joystick(self, side) -> Joystick:
    #     if side is Side.LEFT:
    #         return self.LEFT_JOYSTICK
    #     elif side is Side.RIGHT:
    #         return self.RiGHT_JOYSTICK
