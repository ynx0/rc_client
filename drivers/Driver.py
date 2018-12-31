from procbridge import ProcBridge as Client

from rc_common import netcfg


class Driver:

    def __init__(self, name, driver_id):
        self.name = name  # human readable such as "Default Driver"
        self.id = driver_id  # any unique non-space string such as "drv00"

    # all drivers have an entry point, start which usually contains the main infinite loop
    def start(self):
        print("Driver: " + self.name + "@" + self.id)

    @staticmethod
    def get_client() -> Client:
        client = None
        # noinspection PyBroadException
        try:
            client = Client(netcfg.HOST, netcfg.HDW_PORT)
        except Exception:
            print("Error: unable to connect to host {}:{}".format(netcfg.HOST, netcfg.HDW_PORT))

        return client
