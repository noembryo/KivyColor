# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from io import open

from kivy.config import Config
Config.set("input", "mouse", "mouse,disable_multitouch")
Config.set("graphics", "width", 480)
Config.set("graphics", "height", 200)
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder


__author__ = "noEmbryo"
__version__ = "0.2.0.0"

PYTHON2 = True if sys.version_info < (3, 0) else False


class Base(FloatLayout):
    def __init__(self, **kwargs):
        super(Base, self).__init__(**kwargs)
        self.back_color = 0, 0, 0, 1

    def calc_hex(self, *args):
        hex_number = args[0]
        if len(hex_number) != 6:
            self.warning_popup("Wrong input", "Should be 6 digits!")
            return
        try:
            int("0x" + hex_number, 16)
        except ValueError:
            self.warning_popup("Wrong input", "Should be only HEX digits!")
            return
        step_one = [hex_number[:2], hex_number[2:4], hex_number[4:]]
        to_kivy = [int("0x" + i, 16) * (1 / 255) for i in step_one]
        self.ids.kivy_input.text = ", ".join(["{:.3}".format(i) for i in to_kivy])
        self.back_color = to_kivy + [self.ids.slider.value]

    def calc_kivy(self, *args):
        kivy_number = args[0]
        if "," not in kivy_number:
            self.warning_popup("Wrong input", "Spit numbers with comma")
            return
        step_one = kivy_number.split(",")
        if len(step_one) != 3:
            self.warning_popup("Wrong input", "Input 3 numbers (float)")
            return
        try:
            step_two = [float(i.strip(" -")) for i in step_one]
        except ValueError:
            self.warning_popup("Wrong input", "Input 3 NUMBERS!")
            return
        if len([i for i in step_two if i <= 1]) != 3:
            self.warning_popup("Wrong input", "Input numbers between 0 - 1")
            return
        self.back_color = step_two + [self.ids.slider.value]
        self.ids.hex_input.text = "".join([hex(int(i * 255))[2:] if i else "00"
                                           for i in step_two])

    def on_slider(self, *args):
        if self.ids.hex_input.text:
            self.calc_hex(args[0])
        elif self.ids.kivy_input.text:
            self.calc_kivy(args[1])

    @staticmethod
    def warning_popup(title, text):
        label = Label()
        label.text = text
        popup = Popup(title_align="center", content=label, size_hint=(None, None),
                      size=("300dp", "120dp"))
        popup.title = title
        popup.open()
        Clock.schedule_once(lambda func: popup.dismiss(), 3)


class ColorKivyHex(App):
    def build(self):
        self.use_kivy_settings = False
        if PYTHON2:
            self.load_kv("gui.kv")
        else:
            with open("gui.kv", encoding="utf8") as kv_file:
                Builder.load_string(kv_file.read())
        self.title = "Color: Kivy <> Hex"
        return Base()


if __name__ == "__main__":
    ColorKivyHex().run()
