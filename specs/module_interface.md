# OS-2 module interface

While the OS-2 does not utilize removable plugins, several system blocks are
implemented as self-contained modules. This document describes the interface
between them and the rest of the system.

## Power interface

Several power supplies are provided to modules, on the followings pins:

- GND (many pins, interspersed on connector)
- +55V - high current, bulk unregulated rail (others are sourced from this)
- +15V - medium current, quiet analog rail
- +10.00V - low current (≤10mA), precise reference rail
- +5V - high current, general rali
- -15V - medium current, quiet analog rail
- -55V - medium current, bulk unregulated rail

## On-screen display (OSD) interface

(See also: [On-screen display](./on_screen_display.md))

The following pins go to all vertical, horizontal, and caption modules to
implement the on-screen display:

| Pin           | Direction | Function                                         |
|---------------|-----------|--------------------------------------------------|
| SELECT        | to mod    | Asserts when module should drive CHARn           |
| POS0 – POS2   | to mod    | Selects a character position (0-7)               |
| CHAR0 – CHAR5 | from mod  | Open coll; drives character bits on SELECT       |

This is an asynchronous interface, and modules should respond as quickly as
possible to changes in the input lines. When SELECT is not asserted, the module
should not drive the CHARn lines.

## Signal interface

The signal interface is a differential current-sink interface. It is biased to
+9V by the channel switch circuit and terminated into 120 ohms differential.

Signal level is 0.5V per division, with the center of the display at (ideally)
0V. Because the display measures 10 divisions by 8 divisions, the voltage to
reach the display edges is ±2.5V (horizontally) or ±2.0V (vertically).

| Pin       | Direction | Function              |
|-----------|-----------|-----------------------|
| SIG+      | from mod  | Primary signal, +ve   |
| SIG-      | from mod  | Primary signal, -ve   |
