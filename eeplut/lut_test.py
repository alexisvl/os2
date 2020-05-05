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

@eeplut.auto
class TestLut(eeplut.Eeplut):
    def __init__(self):
        super().__init__(size_kbits = 512, width_bits = 8)

    def logic_functions(self):
        return [
            self.fn_test,
        ]

    def fn_test(self, inputs):
        return {i: inputs[i + 8] for i in range(8)}
