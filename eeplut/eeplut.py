# eeplut - a Python module to generate EEProm Look-Up Tables from logic
# functions.
#
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

try:
    import intelhex
except ImportError:
    have_intelhex = False
else:
    have_intelhex = True

class Eeplut:
    """EEPLUT base class. To design a LUT, subclass this.
    """
    def __init__(self, *, size_kbits, width_bits):
        """Define the EEPROM (or EPROM/PROM) format.

        - size_kbits: chip size in kilobits (1 kb = 1024 b). Size in bits must
          be a power of two multiplied by width_bits.
        - width_bits: output bus width in bits. Must be a multiple of 8,
          and if not exactly 8, endianness must also be specified.
        """

        if not isinstance(width_bits, int):
            raise TypeError("width_bits must be an integer")
        if not isinstance(size_kbits, int):
            raise TypeError("size_kbits must be an integer")

        if width_bits % 8 != 0 or width_bits < 8:
            raise ValueError("width_bits must be a multiple of 8, >= 8")

        size_bits = 1024 * size_kbits
        if size_bits % width_bits != 0:
            raise ValueError("size must be divisible by bus width")
        address_space = size_bits // width_bits

        if address_space & (address_space - 1) != 0:
            raise ValueError("address space must be a power of two")

        self.size_kbits = size_kbits
        self.width_bits = width_bits
        self.address_space = address_space
        self.address_lines = (address_space - 1).bit_length()

    def export(self, f, *, fmt, endianness=None):
        """Export the LUT to a file.

        - f: file-like output
        - fmt: format. Currently supported: "bin", "hex"
        - endianness: mandatory if output bus is wider than 8. Can be "big" or
          "little".
        """

        if fmt not in ("bin", "hex"):
            raise Exception(f"unsupported format: {fmt!r}")

        if fmt == "hex":
            if not have_intelhex:
                raise Exception("intelhex module required for hex output")

        logic_functions = self.logic_functions()
        inputs_map = self.inputs_map()
        outputs_map = self.outputs_map()

        data = [0] * self.address_space

        for addr in range(self.address_space):
            inputs = {}
            for address_line in range(self.address_lines):
                inputs[inputs_map.get(address_line, address_line)] = (
                    bool(addr & (1 << address_line))
                )

            # TODO: default value
            outputs = {}
            for fun in logic_functions:
                # TODO: weak/strong and validation
                outputs.update(fun(inputs))

            data_value = 0
            for k, v in outputs.items():
                k = outputs_map.get(k, k)
                if not isinstance(k, int):
                    raise ValueError(f"Could not map output {k}")
                if v:
                    data_value |= (1 << k)
            data[addr] = data_value

        # TODO: non-8-bit

        if fmt == "bin":
            f.write(bytes(data))
        elif fmt == "hex":
            ih = intelhex.IntelHex()
            for n, i in enumerate(data):
                ih[n] = i
            ih.write_hex_file(f)

    def inputs_map(self):
        """Implementation may return a dict mapping input signals to names.
        If a signal is not in this dict, it is passed into functions
        numerically.
        """
        return {}

    def outputs_map(self):
        """Implementation may return a dict mapping names to output signals.
        If a signal is not in this dict, it is passed into functions
        numerically.
        """
        return {}

    def logic_functions(self):
        """Implementation should return a list of all logic functions. A logic
        function is either a function or a method on self, working as follows:

        - only argument is a dict of all LUT inputs and their values
        - return is a dict of relevant LUT outputs and their values

        Valid output values are as follows:

        - "L" or "H": like VHDL, "weak" low and high signals. Overridden if
          another logic function defines them strongly.

          If two logic functions define the same signal to opposite weak
          levels, an error results.

        - Anything true, other than aforementioned values: "strong" high
          signal.
        - Anything false: "strong" low signal

          If two logic functions define the same signal strongly (even to the
          same value), an error results.

        Logic functions are executed in the order listed, and one function can
        insert "internally routed" values into `inputs` to pass on to the next.
        """
        return []

    def default_unused_output(self):
        """Override to define the default logic level for outputs present on the
        chip that are not defined.
        """
        return False

def auto(classname, *args, **kwargs):
    """Call with the name of a class to run an automatic conversion if running
    from the root script.

    In other words, in a script defining ExampleLut, add `auto(ExampleLut)` at
    the bottom to make it callable.

    args and kwargs are passed to the constructor.

    Also works as a decorator.
    """

    # TODO: command line options

    import inspect
    if inspect.stack()[1].function == "<module>":
        instance = classname(*args, **kwargs)
        with open("out.hex", "w") as f:
            instance.export(f, fmt="hex")

    return instance
