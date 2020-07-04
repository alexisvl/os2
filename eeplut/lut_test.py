# LUT_TEST Implementation
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

#@eeplut.auto
class TestLut8(eeplut.Eeplut):
    def __init__(self):
        super().__init__(size_kbits = 512, width_bits = 8)

    def logic_functions(self):
        return [
            self.fn_test,
        ]

    def fn_test(self, inputs):
        return {i: inputs[i + 8] for i in range(8)}

@eeplut.auto
class TestLut16(eeplut.Eeplut):
    def __init__(self):
        super().__init__(size_kbits = 512, width_bits = 16)

    def logic_functions(self):
        return [
            self.fn_test,
        ]

    def default_unused_output(self):
        return False

    def fn_test(self, inputs):
        # inputs are 0 to 14

        return inputs

#@eeplut.auto
class TestWeakStrong(eeplut.Eeplut):
    # By using weak outputs to fill the EEPROM with 0x55 bytes,
    # then strong outputs to override some, this demo layers weak
    # and strong drivers into a pattern of 55, FF, 55, FF ...

    def __init__(self):
        super().__init__(size_kbits = 1, width_bits = 8)

    def logic_functions(self):
        return [
            self.fn_weak,
            self.fn_strong,
        ]

    def fn_weak(self, inputs):
        return {i: "L" if i % 2 else "H" for i in range(8)}

    def fn_strong(self, inputs):
        if inputs[0]:
            return {i: 1 for i in range(8)}

#@eeplut.auto
class TestWeakConflict(eeplut.Eeplut):
    # Too many weak drivers

    def __init__(self):
        super().__init__(size_kbits = 1, width_bits = 8)

    def logic_functions(self):
        return [
            self.fn1,
            self.fn2,
        ]

    def fn1(self, inputs):
        return {i: "L" for i in range(8)}

    def fn2(self, inputs):
        return {i: "H" for i in range(8)}

#@eeplut.auto
class TestStrongConflict(eeplut.Eeplut):
    # Too many strong drivers

    def __init__(self):
        super().__init__(size_kbits = 1, width_bits = 8)

    def logic_functions(self):
        return [
            self.fn1,
            self.fn2,
        ]

    def fn1(self, inputs):
        return {i: 0 for i in range(8)}

    def fn2(self, inputs):
        return {i: 1 for i in range(8)}
