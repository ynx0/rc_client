from drivers.keyboard.KeyboardDriver import KeyboardDriver
from drivers.keyboard.KeyboardUtils import KeyControls, KeyList, Arrows
from drivers.xbox.XboxDriver import XboxDriver

default_keymap = {
    KeyControls.STOP: [b's'],
    KeyControls.EXIT: [b'e', KeyList.ESC, KeyList.CTRLC],
    # directions
    KeyControls.UP: [Arrows.UP],
    KeyControls.DOWN: [Arrows.DOWN],
    KeyControls.LEFT: [Arrows.LEFT],
    KeyControls.RIGHT: [Arrows.RIGHT],
    # speed controls
    KeyControls.SET_SPEED_1: [b'1'],
    KeyControls.SET_SPEED_2: [b'2'],
}

alt_keymap = {
    KeyControls.STOP: [b's'],
    KeyControls.EXIT: [b'e', KeyList.ESC, KeyList.CTRLC],
    # directions
    KeyControls.UP: [b'i'],
    KeyControls.DOWN: [b','],
    KeyControls.LEFT: [b'j'],
    KeyControls.RIGHT: [b'l'],
    # speed controls
    KeyControls.SET_SPEED_1: [b'1'],
    KeyControls.SET_SPEED_2: [b'2'],
}


# todo iterate through directories and programmatically create this list
def main():
    print("Which input method would you like to activate")
    print("1 - Keyboard")
    print("2 - Keyboard Alt")
    print("3 - Xbox")
    choice = input("Choose a number -->")

    if choice == "1":
        print("Starting Driver Keyboard CLI ")
        kbd_cli = KeyboardDriver("Keyboard Driver", "kbd_drv00", default_keymap)
        kbd_cli.start()
    elif choice == "2":
        print("Starting alt driver cli")
        kbd_alt = KeyboardDriver("Keyboard Driver Alt", "kbd_drv01_alt", alt_keymap)
        kbd_alt.start()
    elif choice == "3":
        print("Starting Xbox Controller")
        xbox_drv = XboxDriver("Xbox Driver", "xbox_00", {
            'STOP_THRESHOLD': 1
        })
        xbox_drv.start()
    else:
        print("invalid choice" + choice)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("exitting")
