from machine import Pin, reset
from time import sleep_ms


class KeyHandler:
    def __init__(self, index, pin_id):
        self.index = index
        self.pin_id = pin_id
        self.pin = Pin(pin_id, Pin.IN)

    def reinit(self):
        self.pin = Pin(self.pin_id, Pin.IN, Pin.PULL_UP)
        self.pin.value(1)

    def read(self):
        return self.pin.value()

    def begin_pulse(self):
        self.pin = Pin(self.pin_id, Pin.OUT)
        self.pin.off()

    def end_pulse(self):
        self.pin.on()
        self.pin = Pin(self.pin_id, Pin.IN)


class Keypad:
    def __init__(self, row_pins, col_pins, keymap):

        self.keymap = keymap

        self.row_pins = []
        for (index, row_pin) in enumerate(row_pins):
            self.row_pins.append(KeyHandler(index, row_pin))

        self.col_pins = []
        for index, col_pin in enumerate(col_pins):
            self.col_pins.append(KeyHandler(index, col_pin))

    def get_keys(self):

        pressed = []

        # Re-intialize the row pins. Allows sharing these pins with other hardware
        for row in self.row_pins:
            row.reinit()

        # check the column pins, which ones are pulled down
        for col in self.col_pins:
            col.begin_pulse()
            for row in self.row_pins:
                row_val = row.read()
                row_col = col.read()
                if row_val == 0:
                    pressed.append(self.keymap[row.index][col.index])
            col.end_pulse()

        return pressed


if __name__ == '__main__':

    print("Keypad example")

    #  Board | Micropython
    D0 = 16  # (also Led2 but inverse)*
    D1 = 5
    D2 = 4
    D3 = 0
    D4 = 2  # (also Led1 but inverse)*
    D5 = 14
    D6 = 12
    D7 = 13
    D8 = 15  # This seems not to be working reliably
    D9 = 3
    D10 = 1

    keypad = Keypad(
        #  rows
        [D4, D5, D6, D7],
        # cols
        [D0, D1, D2, D3],
        # keys map
        [
            ['1', '2', '3', 'A'],
            ['4', '5', '6', 'B'],
            ['7', '8', '9', 'C'],
            ['*', '0', '#', 'D'],
        ]
    )

    while True:
        keys = keypad.get_keys()
        if len(keys) > 0:
            print(keys)
        sleep_ms(300)
