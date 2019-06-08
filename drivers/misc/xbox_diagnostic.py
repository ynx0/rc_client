from drivers.xbox.xbox_controller import XboxController


def main():
    xbox = XboxController()
    while True:
        print(xbox.RIGHT_TRIGGER.raw_value)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping")
