import sys
sys.path.append('../')
from RC_Commands import Commands
import msvcrt
from procbridge.procbridge import *




# adapted from https://stackoverflow.com/a/34497639/3807967
class Arrows():
    LEFT = 75
    RIGHT = 77
    UP = 72
    DOWN = 80

DEFAULT_SPEED = 50

def start():
    print("Starting driver: " + __file__)
    print("Use the arrow keys to drive the car")
    print("'s' to stop")
    print("'e' to exit")

    host = '192.168.0.125'
    port = 9939
    client = ProcBridge(host, port)

    #ping_assert(client)

    while True:
        key = msvcrt.getch()
        print('key:' + str(key))
        
        if key == b's':
            client.request(Commands.STOP, {})
        elif key == b'e' or key == b'\x03' or key == '\x1b':
            print('shutting down ...')
            client.request(Commands.SHUTDOWN, {})
            sys.exit(0)
        elif key == b'\xe0':
            # this means arrow key
            arrow = int.from_bytes(msvcrt.getch(), 'little')
            if arrow == Arrows.RIGHT:
                client.request(Commands.RIGHT)
            elif arrow == Arrows.LEFT:
                client.request(Commands.LEFT)
            elif arrow == Arrows.UP:
                client.request(Commands.FORWARD, {"speed": DEFAULT_SPEED})
            elif arrow == Arrows.DOWN:
                client.request(Commands.BACKWARD, {"speed" : DEFAULT_SPEED})
            else:
                print("Unknown arrow/keycode" + str(arrow))
        else:
            pass

def ping_assert(client):
    try:
        client.request('ping', {})
    except TimeoutError:
        print('Error: server on car is not up')
        print('Exitting')
        sys.exit(-1)

if __name__ == '__main__':
    start()
