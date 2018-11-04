from drivers import keyboard_cli


def main():
    print("Which input method would you like to activate")
    print("1 - Keyboard")
    choice = input("Choose a number -->")

    if choice == "1":
        print("Starting Driver Keyboard CLI ")
        keyboard_cli.start()

    else:
        print("invalid choice" + choice)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("exitting")
