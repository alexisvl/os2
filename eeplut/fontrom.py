# FONT_ROM implementation
# Copyright (C) 2020 Alexis Lockwood, <alexlockwood@fastmail.com>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import eeplut
from PIL import Image
import logging

IMAGE_FILENAME = "charset.png"

COLOR_DESCENDER0 = (255, 255, 255)
COLOR_DESCENDER1 = (255, 0, 0)
COLOR_DESCENDER2 = (0, 255, 0)

# X offset to dot 0, char 0
MAP_XOFFSET = 1

# X stride from dot 0, char 0 to dot 0, char 1
MAP_XSTRIDE = 7

# Number of characters in the X dimension
CHARS_X = 16

MAP_YOFFSET = 0
MAP_YSTRIDE = 11
CHARS_Y = 8

# Number of rows of descender data
DESCENDER_ROWS = 2

# Width of an actual character
CHAR_W = 6
# Height of an actual character
CHAR_H = 8

# Bitmaps for the internal byte array, don't have to match output bits
BV_DOT = 0x1
BV_DESC0 = 0x2
BV_DESC1 = 0x4

@eeplut.auto
class FontRom(eeplut.Eeplut):
    def __init__(self):
        super().__init__(size_kbits = 512, width_bits = 8)

        self.populate_chars()

    def populate_chars(self):
        im = Image.open(IMAGE_FILENAME)

        self.chars = []
        for i in range(CHARS_X * CHARS_Y):
            self.chars.append(bytearray(CHAR_W * CHAR_H))

            charx = i % CHARS_X
            chary = i // CHARS_X

            x0 = MAP_XOFFSET + charx * MAP_XSTRIDE
            y0 = MAP_YOFFSET + chary * MAP_YSTRIDE

            for y in range(CHAR_H + DESCENDER_ROWS):
                for x in range(CHAR_W):
                    pix = im.getpixel((x0 + x, y0 + y))
                    if pix == COLOR_DESCENDER0:
                        value = BV_DOT
                        desc = 0
                    elif pix == COLOR_DESCENDER1:
                        value = BV_DOT | BV_DESC0
                        desc = 1
                    elif pix == COLOR_DESCENDER2:
                        value = BV_DOT | BV_DESC1
                        desc = 2
                    else:
                        continue

                    y_desc = y - desc
                    if y_desc < 0:
                        logging.warning(f"descender maps above char {i} at ({x}, {y})")
                        continue
                    if y_desc >= CHAR_H:
                        logging.warning(f"descender maps below char {i} at ({x}, {y})")
                        continue

                    arr_ind = (y_desc * CHAR_W) + x
                    if self.chars[i][arr_ind]:
                        logging.warning(f"descender clobbers pixel in char {i} at ({x}, {y})")

                    self.chars[i][arr_ind] = value

            for y in range(CHAR_H):
                for x in range(CHAR_W):
                    arr_ind = (y * CHAR_W) + x
                    val = self.chars[i][arr_ind]
                    print(val if val else " ", end='')
                print()
            print()

    def logic_functions(self):
        return [self.fn_font]

    def inputs_map(self):
        return {
            0: "HDOT0",
            1: "HDOT1",
            2: "HDOT2",

            3: "CHAR0",
            4: "CHAR1",
            5: "CHAR2",
            6: "CHAR3",
            7: "CHAR4",
            8: "CHAR5",
            9: "CHAR6",

            10: "LINE0",
            11: "LINE1",
            12: "LINE2",
        }

    def outputs_map(self):
        return {
            "PIX_BLANK": 0,
            "DESCENDER0": 1,
            "DESCENDER1": 2,
        }

    def fn_font(self, inputs):
        hdot = inputs["HDOT0"] | (inputs["HDOT1"] << 1) | (inputs["HDOT2"] << 2)
        char = (
            inputs["CHAR0"]
            | (inputs["CHAR1"] << 1)
            | (inputs["CHAR2"] << 2)
            | (inputs["CHAR3"] << 3)
            | (inputs["CHAR4"] << 4)
            | (inputs["CHAR5"] << 5)
            | (inputs["CHAR6"] << 6)
        )
        line = inputs["LINE0"] | (inputs["LINE1"] << 1) | (inputs["LINE2"] << 2)

        arr_ind = (line * CHAR_W) + hdot

        if hdot >= CHAR_W:
            # unused space
            return {}

        value = self.chars[char][arr_ind]

        return {
            "PIX_BLANK": not (value & BV_DOT),
            "DESCENDER0": value & BV_DESC0,
            "DESCENDER1": value & BV_DESC1,
        }

    def default_unused_output(self):
        return False
