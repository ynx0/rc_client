import sys

import colorama as clr

import drivers.keyboard.KeyboardUtils as KBDUtils
from drivers.Driver import Driver
from drivers.keyboard.KeyboardUtils import Console, KeyDebouncer, KeyControls
from rc_common.RC_Commands import Commands


class Speed:
    LOW_SPEED = 60
    HIGH_SPEED = 70
    DEFAULT_SPEED = LOW_SPEED


class KeyboardDriver(Driver):

    def __init__(self, name, driver_id, keymap: dict):
        super().__init__(name, driver_id)
        self.keymap = keymap
        self.current_speed = Speed.DEFAULT_SPEED
        # debug

    # todo refactor to be (control, key)
    def is_control_activated(self, key, control):
        return key in self.keymap[control]

    @staticmethod
    def print_usage():
        print("Use the arrow keys to drive the car")
        print("'s' to stop")
        print("'e' to exit")
        print("\n")

    def start(self):
        # console initialization stuff
        clr.init()
        sys.stderr.write(Console.CLS)
        self.print_usage()

        # driver specific init code
        client = self.get_client()
        self.current_speed = Speed.DEFAULT_SPEED
        # debouncer = KeyDebouncer(0.15)  # maybe parametrize?

        print(
            clr.Style.BRIGHT + clr.Fore.LIGHTWHITE_EX + clr.Back.LIGHTBLACK_EX + "Last action:" + clr.Style.RESET_ALL)


        while True:
            # debouncing code
            # this basically filters rapid keystrokes/commands to server
            # debouncer.update()
            # if debouncer.should_filter():
            #     print('filtering')
            #     continue  # skip processing any controls


            key = KBDUtils.getch()

            # print('key is ' + str(key))

            # stop
            if self.is_control_activated(key, KeyControls.STOP):
                client.request(Commands.STOP, {})
                print(clr.Fore.RED + "\rStop The Car" + clr.Style.RESET_ALL + Console.FLUSH_STR, end='', flush=True)

            # exit
            elif self.is_control_activated(key, KeyControls.EXIT):
                print('\rshutting down ...')
                sys.exit(0)

            # set speed 1
            elif self.is_control_activated(key, KeyControls.SET_SPEED_1):
                self.current_speed = Speed.LOW_SPEED
                print('\rSet Speed to ' + str(self.current_speed) + Console.FLUSH_STR)

            # set speed 2
            elif self.is_control_activated(key, KeyControls.SET_SPEED_2):
                self.current_speed = Speed.HIGH_SPEED
                print('\rSet Speed to ' + str(self.current_speed) + Console.FLUSH_STR)

            # up
            elif self.is_control_activated(key, KeyControls.UP):
                client.request(Commands.FORWARD, {"speed": self.current_speed})
                print("\rMove Forward @ PWR: " + str(self.current_speed) + Console.FLUSH_STR, end='', flush=True)

            elif self.is_control_activated(key, KeyControls.DOWN):
                client.request(Commands.BACKWARD, {"speed": self.current_speed})
                print("\rMove Backward @ PWR: " + str(self.current_speed) + Console.FLUSH_STR, end='', flush=True)

            elif self.is_control_activated(key, KeyControls.LEFT):
                client.request(Commands.LEFT)
                print("\rTurn Left" + Console.FLUSH_STR, end='', flush=True)

            elif self.is_control_activated(key, KeyControls.RIGHT):
                client.request(Commands.RIGHT)
                print("\rTurn Right" + Console.FLUSH_STR, end='', flush=True)
