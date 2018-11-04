# base driver class
# to use later


class Driver:

    def __init__(self):
        self.name = "Default Driver"
        self.id = "drv00"  # any unique non-space string

    def start(self):
        print("Driver: " + self.name + "@" + self.id)

