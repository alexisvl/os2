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

import argparse
import datetime
import enum
import inspect
import struct
import sys

SCRIPT=False

try:
    import intelhex
except ImportError:
    have_intelhex = False
else:
    have_intelhex = True

class Format(enum.Enum):
    HEX = 1
    BIN = 2
    C_BYTE = 3
    C_WORD = 4

class Endian(enum.Enum):
    LITTLE = 1
    BIG = 2

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

    def export(self, f, *, fmt: Format, endianness: Endian = None, **kwargs):
        """Export the LUT to a file.

        - f: file-like output
        - fmt: output format
        - endianness: mandatory if output bus is wider than 8
        - kwargs: per-format extra arguments
        """

        if not isinstance(fmt, Format):
            raise TypeError("fmt must be a Format enum value")

        if fmt == Format.HEX:
            if not have_intelhex:
                _die("intelhex module required for hex output")

        logic_functions = self.logic_functions()
        inputs_map = self.inputs_map()
        outputs_map = self.outputs_map()

        data = [None] * self.address_space

        for addr in range(self.address_space):
            inputs = {}
            for address_line in range(self.address_lines):
                inputs[inputs_map.get(address_line, address_line)] = (
                    int(bool(addr & (1 << address_line)))
                )

            outputs = {
                k: None for k in range(self.width_bits)
            }
            for fun in logic_functions:
                fun_outputs = fun(inputs)
                if fun_outputs is None:
                    fun_outputs = {}
                for k, v in fun_outputs.items():
                    kn = outputs_map.get(k, k)
                    if not isinstance(kn, int):
                        raise ValueError(f"Could not map output {k}")

                    if v in ("L", "H"):
                        this_prio = 1
                    else:
                        this_prio = 2

                    if outputs[kn] is None:
                        last_prio = 0
                    elif outputs[kn] in ("L", "H"):
                        last_prio = 1
                    else:
                        last_prio = 2

                    if this_prio > last_prio:
                        outputs[kn] = v
                    else:
                        raise ValueError(
                            f"Output {k} from function {fun.__name__}: "
                            "too many drivers on this net"
                        )

            data_value = 0
            for k, v in outputs.items():
                if v == "L":
                    v_bool = False
                else:
                    v_bool = bool(v)

                if v_bool:
                    data_value |= (1 << k)
            data[addr] = data_value

        stride = self.width_bits // 8
        content = bytearray(self.address_space)
        endian_flag = {
            Endian.BIG: ">",
            Endian.LITTLE: "<",
            None: "<",
        }[endianness]

        struct_def = endian_flag + {
            8: "B", 16: "H", 32: "I", 64: "Q",
        }[self.width_bits]

        for addr in range(self.address_space):
            encoded = struct.pack(struct_def, data[addr])
            content[addr * stride : (addr + 1) * stride] = encoded

        if fmt == Format.BIN:
            f.write(content)
        elif fmt == Format.HEX:
            ih = intelhex.IntelHex()
            for n, i in enumerate(content):
                ih[n] = i
            ih.write_hex_file(f)

        elif fmt == Format.C_BYTE:
            if kwargs.get('ident') is None:
                _die("Format C_BYTE requires identifier (--ident)")

            _write_c(f, content, "unsigned char", kwargs["ident"])

        elif fmt == Format.C_WORD:
            if kwargs.get('ident') is None:
                _die("Format C_WORD requires identifier (--ident)")

            ty = {
                8: "uint8_t", 16: "uint16_t", 32: "uint32_t", 64: "uint64_t",
            }[self.width_bits]

            _write_c(f, data, ty, kwargs["ident"])

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
        return True

def _write_c(f, data, ty, ident):
    """Write out a C resource file.

    f: output file
    data: data to write, must be an iterable of integers
    ty: C type for array
    ident: C identifier for array
    """

    f.write("// This file was autogenerated on ")
    f.write(datetime.datetime.now().ctime())
    f.write("\n\n")

    f.write(f"const {ty} {ident}[] = {{\n")

    for n, i in enumerate(data):
        if n % 16 == 0:
            if n != 0:
                f.write("\n")
            f.write("    ")

        f.write(f"0x{i:X}u,")

        if n % 16 < 15:
            f.write(" ")

    f.write("\n};\n")


def _die(msg):
    if SCRIPT:
        print(f"{sys.argv[0]}: {msg}", file=sys.stderr)
        sys.exit(1)
    else:
        raise Exception(msg)

def _do_auto(instance):
    name = type(instance).__name__

    p = argparse.ArgumentParser(
        description=f"Generate EEPROM LUT for {name}",
    )

    p.add_argument(
        "file", type=str, help="Output filename",
    )

    p.add_argument(
        "--format", "-f",
        choices=("auto", "hex", "bin", "cbyte", "cword"),
        default="auto",
        help="Output format. auto = detect by extension",
    )

    p.add_argument(
        "--endian", "-e",
        choices=("little", "big"),
        default="little",
        help="Output endianness",
    )

    p.add_argument(
        "--ident", type=str,
        help="Identifier name, for formats cbyte and cword",
    )

    args = p.parse_args()

    if args.format == "auto":
        if args.file.endswith(".hex"):
            fmt = Format.HEX
        elif args.file.endswith(".bin"):
            fmt = Format.BIN
        else:
            _die(
                "Cannot guess format from file extension. "
                "Try --format."
            )
    else:
        fmt = {
            "hex": Format.HEX,
            "bin": Format.BIN,
            "cbyte": Format.C_BYTE,
            "cword": Format.C_WORD,
        }[args.format]

    mode = {
        Format.HEX: "w",
        Format.BIN: "wb",
        Format.C_BYTE: "w",
        Format.C_WORD: "w",
    }[fmt]

    endian = {
        "little": Endian.LITTLE,
        "big": Endian.BIG,
    }[args.endian]

    with open(args.file, mode) as f:
        instance.export(
            f,
            fmt=fmt,
            endianness=endian,
            ident=args.ident,
        )

def auto(classname, *args, **kwargs):
    """Call with the name of a class to run an automatic conversion if running
    from the root script.

    In other words, in a script defining ExampleLut, add `auto(ExampleLut)` at
    the bottom to make it callable.

    args and kwargs are passed to the constructor.

    Generally used as a decorator.
    """

    if inspect.stack()[1].function == "<module>":
        global SCRIPT
        SCRIPT=True

        instance = classname(*args, **kwargs)
        _do_auto(instance)
        return instance
    else:
        return classname

def concat(inputs, *keys):
    """Concatenate inputs by key into an integer. Convenience function to
    avoid long strings of bit shifts and ORs:

    concat(inputs, "A", "B", "C") is equivalent to:
    inputs["C"] | (inputs["B"] << 1) | (inputs["C"] << 2)
    """

    v = 0

    for n, i in enumerate(keys):
        v |= inputs[i] << (len(keys) - n - 1)

    return v

def decompose(value, *keys):
    """Decompose an integer value into a dict of outputs by key.
    Convenience function to avoid long sequences of mask and shift.

    decompose(value, "A", "B", "C") is equivalent to:
    {"A": (value & 0x4) >> 2, "B": (value & 0x2) >> 1, "C": value & 0x1}
    """

    outputs = {}

    for n, i in enumerate(keys):
        outputs[i] = 1 if (value & (1 << (len(keys) - n - 1))) else 0

    return outputs
