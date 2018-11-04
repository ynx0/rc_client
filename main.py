from drivers import keyboard_cli, keyboard_cli_alt


def main():
    print("Which input method would you like to activate")
    print("1 - Keyboard")
    print("2 - Keyboard Alt")
    choice = input("Choose a number -->")

    if choice == "1":
        print("Starting Driver Keyboard CLI ")
        keyboard_cli.start()
    elif choice == "2":
        print("Starting alt driver cli")
        keyboard_cli_alt.start()
    else:
        print("invalid choice" + choice)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("exitting")
