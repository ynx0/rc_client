# import sys
# from enum import Enum
#
# from rc_common import netcfg
# from rc_common.RC_Commands import Commands
# import msvcrt
# # noinspection PyUnresolvedReferences
# import libs
# from procbridge import Client
# import colorama as clr
# import time
#
#
# # adapted from https://stackoverflow.com/a/34497639/3807967
# class Arrows:
#     LEFT = 75
#     RIGHT = 77
#     UP = 72
#     DOWN = 80
#
#
# class KeyMap:
#     ESC = b'\x1b'
#     CTRLC = b'\x03'
#     ARROW_FLAG = b'\xe0'
#     # weird, check msdn vk ref
#     FKEY_FLAG = '\x00'
#
#
# class Console:
#     CLS = "\x1b[2J\x1b[H"
#     FLUSH_STR = " " * 20
#
#
# class Speed(Enum):
#     DEFAULT_SPEED = 60
#     LOW_SPEED = DEFAULT_SPEED
#     HIGH_SPEED = 70
#
#
# # noinspection PyBroadException,PyTypeChecker
# def start():
#     clr.init()
#     sys.stderr.write(Console.CLS)
#     # print("Starting driver: " + __file__)
#     print("Use the arrow keys to drive the car")
#     print("'s' to stop")
#     print("'e' to exit")
#     print("\n")
#
#     client = None
#     current_speed = Speed.DEFAULT_SPEED
#     # ping_assert(client)
#
#     try:
#         client = Client(netcfg.HOST, netcfg.HDW_PORT)
#     except Exception:
#         print("Error: unable to connect using static ip address")
#
#     print(clr.Style.BRIGHT + clr.Fore.LIGHTWHITE_EX + clr.Back.LIGHTBLACK_EX + "Last action:" + clr.Style.RESET_ALL)
#
#     while True:
#         # delta stuff
#         prev_time = time.time()
#         key = msvcrt.getch()
#         delta = time.time() - prev_time
#
#         if delta <= 0.15:
#             # print("\rChill out dawg")
#             continue
#
#         if key == b's':
#             client.request(Commands.STOP, {})
#             print(clr.Fore.RED + "\rStop The Car" + clr.Style.RESET_ALL + Console.FLUSH_STR, end='', flush=True)
#         elif key == b'e' or key == KeyMap.CTRLC or key == KeyMap.ESC:
#             print('\rshutting down ...')
#             sys.exit(0)
#         elif key == KeyMap.ARROW_FLAG:
#             # this means arrow key
#             arrow = int.from_bytes(msvcrt.getch(), 'little')
#             if arrow == Arrows.RIGHT:
#                 client.request(Commands.RIGHT)
#                 print("\rTurn Right" + Console.FLUSH_STR, end='', flush=True)
#             elif arrow == Arrows.LEFT:
#                 client.request(Commands.LEFT)
#                 print("\rTurn Left" + Console.FLUSH_STR, end='', flush=True)
#             elif arrow == Arrows.UP:
#                 client.request(Commands.FORWARD, {"speed": current_speed.value})
#                 print("\rMove Forward @ PWR: " + str(current_speed.value) + Console.FLUSH_STR, end='', flush=True)
#             elif arrow == Arrows.DOWN:
#                 client.request(Commands.BACKWARD, {"speed": current_speed.value})
#                 print("\rMove Backwards @ PWR: " + str(current_speed.value) + Console.FLUSH_STR, end='', flush=True)
#             else:
#                 print("\rUnknown arrow/keycode" + Console.FLUSH_STR + str(arrow))
#         elif key == b'1':
#             current_speed = Speed.LOW_SPEED
#             print('\rSet Speed to ' + current_speed.value + Console.FLUSH_STR)
#         elif key == b'2':
#             current_speed = Speed.HIGH_SPEED
#             print('\rSet Speed to ' + current_speed.value + Console.FLUSH_STR)
#         else:
#             pass
#
#
# # def ping_assert():
# #     try:
# #         pass  # find some way to ping the car (use mdns?)
# #     except TimeoutError:
# #         print('Error: server on car is not up')
# #         print('Exitting')
# #         sys.exit(-1)
