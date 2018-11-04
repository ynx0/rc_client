import sys
from rc_common import netcfg
from rc_common.RC_Commands import Commands
import msvcrt
from procbridge.procbridge import ProcBridge


# adapted from https://stackoverflow.com/a/34497639/3807967
class Arrows:
    LEFT = 75
    RIGHT = 77
    UP = 72
    DOWN = 80


class Keys:
    ESC = b'\x1b'
    CTRLC = b'\x03'


DEFAULT_SPEED = 50


# noinspection PyBroadException
def start():
    print("Starting driver: " + __file__)
    print("Use the arrow keys to drive the car")
    print("'s' to stop")
    print("'e' to exit")

    # host = '192.168.0.113'  # ip of the raspberry pi
    # port = 9939
    client = None
    # ping_assert(client)

    # print("Connecting using mdns hostname: " + host_mdns)
    # try:
    #     client = ProcBridge(host_mdns, port)
    # except Exception:
    #     print("Error, unable to use mdns, falling back to static ip address: " + host + ":" + str(port))

    try:
        client = ProcBridge(netcfg.HOST, netcfg.HDW_PORT)
    except Exception:
        print("Error: unable to connect using static ip address")

    while True:
        key = msvcrt.getch()
        print('key:' + str(key))

        if key == b's':
            client.request(Commands.STOP, {})
        elif key == b'e' or key == Keys.CTRLC or key == Keys.ESC:
            print('shutting down ...')
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
                client.request(Commands.BACKWARD, {"speed": DEFAULT_SPEED})
            else:
                print("Unknown arrow/keycode" + str(arrow))
        else:
            pass


def ping_assert():
    try:
        pass  # find some way to ping the car (use mdns?)
    except TimeoutError:
        print('Error: server on car is not up')
        print('Exitting')
        sys.exit(-1)


# if __name__ == '__main__':
#     start()
