# OS-2 module interface

While the OS-2 does not utilize removable plugins, several system blocks are
implemented as self-contained modules. This document describes the interface
between them and the rest of the system.

## Power interface

Several power supplies are provided to modules, on the followings pins:

- GND (many pins, interspersed on connector)
- +55V - low current, analog rail
- +24V - high current, bulk unregulated rail
- +15V - medium current, quiet analog rail
- +12V - high current, general rail (relays, etc)
- +10.00V - low current (≤10mA), precise reference rail
- +5V - high current, general rali
- -15V - medium current, quiet analog rail
- -55V - low current, analog rail

## On-screen display (OSD) interface

(See also: [On-screen display](./on_screen_display.md))

The following pins go to all vertical, horizontal, and caption modules to
implement the on-screen display:

| Pin           | Direction | Function                                         |
|---------------|-----------|--------------------------------------------------|
| SELECT        | to mod    | Asserts when module should drive CHARn           |
| POS0 – POS2   | to mod    | Selects a character position (0-7)               |
| CHAR0 – CHAR5 | from mod  | Open coll; drives character bits on SELECT       |
| OSDINTEN      | from mod  | Open coll active low; intensifies character      |
| OSDINVERSE    | from mod  | Open coll active low; inverse video              |

From the moment SELECT or POSn changes, a module has 10µs to respond with the
next character code. When SELECT is not asserted, the module should not drive
the CHARn lines.

Because the OSD interface prefetches one character ahead of the display module,
the normal INTEN signal cannot be used to intensify the character being
requested. Use OSDINTEN (and OSDINVERSE) instead; these are latched for use
in the next cycle.

## Signal interfaces

The signal interface is a differential current-sink interface. It is biased to
a common-mode voltage by the receiver and terminated into 160 ohms differential.

Signal level is 0.5V per division, with the center of the display at (ideally)
0V. Because the display measures 10 divisions by 8 divisions, the voltage to
reach the display edges is ±2.5V (horizontally) or ±2.0V (vertically), or
±16.6mA (horizontally) or ±13.3mA (vertically) current-mode. Common-mode sink
current may be up to 30mA.

Common-mode termination voltages vary to simplify circuit implementation. They
are as follows:

- Primary SIG/TSIG signals from vertical modules terminate into +4.5V. Trigger
    level output LEVEL is included here (it behaves as an extra vertical
    channel) as is OSDV.
- Primary horizontal signals SIG, TSIG terminate into +9V, allowing them to
    be easily developed from the prior +4.5V signals.
- Display switch output SIG terminates into +9V.

An example termination circuit and transmitter for 16.6mApp. To use at 13.3mApp
with the same input voltage, change the 120 ohm gain resistor to 180 ohms. Gain
values are approximate; for applications requiring accurate gain a gain trimpot
is suggested.

```
                   |       |
                   C       C
Vcm + 0.65V ------B-------B
                   E       E
                   |       |
        Vcm --[68]-+       +-[68]-- Vcm
                   |       |      
                   |       |
                   |       |
                   |       |
                   .inputs .
                   .       .
                   backplane   
                   .       .
                   .outputs.
                   |       |
                   +-[150]-+
                   |       |
                   C       C
single:  2Vpp ----B         B---- gnd
diff:    1Vpp      E       E      1Vpp 180°
                   |       |
                   +-[120]-+
                   |       |
                 [1 k]   [1 k]
                   |       |
                 -15V    -15V
```

### Vertical module

User IO:
- BNC input with probe sense ring
- Rotary encoder to select scale multipliers, LEDs to display
- Rotary encoder to select V/div
- Vernier pot and switch
- AC-GND-DC-GND-50 slider
- Invert slider
- ADD 1+2 or 3+4 slider on odd-numbered modules

Trigger signals are buffered duplicates of the primary signals.

| Pin       | Direction | Function                      | Mode                      |
|-----------|-----------|-------------------------------|---------------------------|
| SIG+      | from mod  | Primary signal, +ve           | Differential, +4.5Vcm     |
| SIG-      | from mod  | Primary signal, -ve           | Differential, +4.5Vcm     |
| TSIG+     | from mod  | Trigger signal, +ve           | Differential, +4.5Vcm     |
| TSIG-     | from mod  | Trigger signal, -ve           | Differential, +4.5Vcm     |
| INTEN     | from mod  | Logic, assert to intensify    | Open-coll active low 5V   |
| BLANK     | from mod  | Logic, assert to blank        | Open-cool active low 5V   |
| ACTIVE    | to mod    | Asserts when displaying       | 5V CMOS                   |

ACTIVE is asserted by the display sequencer whenever this module's output is
currently being displayed. It should gate the INTEN signal, such that this
module will not drive INTEN while other modules are active.

### Trigger module

User IO:
- BNC external trigger
- Slider to select source: INT-EXT-LINE
- Rotary encoder to select internal source: CH1-CH2-CH3-CH4-ALL, LEDs to display
- Level pot
- Level slider: rising-falling

| Pin       | Direction | Function              | Mode                      |
|-----------|-----------|-----------------------|---------------------------|
| TSIG1+    | to mod    | Trigger signal, +ve   | Differential, +4.5Vcm     |
| TSIG1-    | to mod    | Trigger signal, -ve   | Differential, +4.5Vcm     |
| TSIG2+    | to mod    | Trigger signal, +ve   | Differential, +4.5Vcm     |
| TSIG2-    | to mod    | Trigger signal, -ve   | Differential, +4.5Vcm     |
| TSIG3+    | to mod    | Trigger signal, +ve   | Differential, +4.5Vcm     |
| TSIG3-    | to mod    | Trigger signal, -ve   | Differential, +4.5Vcm     |
| TSIG4+    | to mod    | Trigger signal, +ve   | Differential, +4.5Vcm     |
| TSIG4-    | to mod    | Trigger signal, -ve   | Differential, +4.5Vcm     |
| DONE      | to mod    | Sweep is complete     | 5V CMOS                   |
| SWEEP     | from mod  | Sweep gate            | 5V CMOS                   |
| INHIBIT   | to mod    | Blocks trigger        | Open-coll active low 5V   |
| LEVEL+    | from mod  | DC trigger level, +ve | Differential, +4.5Vcm     |
| LEVEL-    | from mod  | DC trigger level, -ve | Differential, +4.5Vcm     |
| LINE      | to mod    | Line trigger signal   | 5V CMOS                   |
| SEL0-2    | to mod    | Pre-decode OSD select | 5V CMOS                   |
| LVLEN     | from mod  | Trigger level auto en | 5V CMOS                   |

LEVEL signals use the same specifications as general signals but may be
unterminated. These are used to allow the OSD module to visualize the
trigger onscreen.

SELn lines from the OSD module are connected to the trigger to allow it to
insert trigger symbols into the relevant OSD space.

LVLEN will be driven high for a second or two whenever the level pot is moved
(perhaps also when other controls move) to flash the trigger level on screen
when the selector on the display switch module is set to AUTO.

### Horizontal/sweep module

| Pin       | Direction | Function                      | Mode                          |
|-----------|-----------|-------------------------------|-------------------------------|
| SWEEP     | to mod    | Sweep gate                    | 5V CMOS                       |
| DONE      | from mod  | Sweep is complete             | 5V CMOS                       |
| CH2+      | to mod    | Ch2 for X/Y mode (+ve)        | Differential, +4.5Vcm unterm  |
| CH2-      | to mod    | Ch2 for X/Y mode (-ve)        | Differential, +4.5Vcm unterm  |
| OSDH+     | to mod    | Horiz OSD scan, +ve           | Differential, +4.5Vcm         |
| OSDH-     | to mod    | Horiz OSD scan, -ve           | Differential, +4.5Vcm         |
| SIG+      | from mod  | Primary signal, +ve           | Differential, +9.0Vcm         |
| SIG-      | from mod  | Primary signal, -ve           | Differential, +9.0Vcm         |
| TSIG+     | from mod  | Secondary signal, +ve         | Differential, +9.0Vcm         |
| TSIG-     | from mod  | Secondary signal, -ve         | Differential, +9.0Vcm         |

TSIG is repurposed for rear panel ramp output, if used.

CH2 is an unterminated input bussed with TSIG2 on the trigger module, used to
deliver Ch 2 for use as the horizontal axis in X/Y mode.

SWEEP asserts for the duration of the sweep, and this module will assert DONE
when the sweep terminates; the trigger module may then begin counting its
holdoff and then re-arm.

OSDSIG lines are always summed into SIG but never into TSIG. When idle, the OSD
module will leave them at zero.

### Display sequencer module

User controls:
- Enable Ch1/Ch2/Ch3/Ch4
- Alt/Chop
- OSD on/off
- Trigger level display slider: OFF-AUTO-ON

| Pin       | Direction | Function                      | Mode                      |
|-----------|-----------|-------------------------------|---------------------------|
| SIG1+     | to mod    | Signal input, +ve             | Differential, +4.5Vcm     |
| SIG1-     | to mod    | Signal input, -ve             | Differential, +4.5Vcm     |
| SIG2+     | to mod    | Signal input, +ve             | Differential, +4.5Vcm     |
| SIG2-     | to mod    | Signal input, -ve             | Differential, +4.5Vcm     |
| SIG3+     | to mod    | Signal input, +ve             | Differential, +4.5Vcm     |
| SIG3-     | to mod    | Signal input, -ve             | Differential, +4.5Vcm     |
| SIG4+     | to mod    | Signal input, +ve             | Differential, +4.5Vcm     |
| SIG4-     | to mod    | Signal input, -ve             | Differential, +4.5Vcm     |
| OSDV+     | to mod    | OSD scan input, +ve           | Differential, +4.5Vcm     |
| OSDV-     | to mod    | OSD scan input, -ve           | Differential, +4.5Vcm     |
| LEVEL+    | to mod    | Trigger level input, +ve      | Differential, +4.5Vcm     |
| LEVEL-    | to mod    | Trigger level input, -ve      | Differential, +4.5Vcm     |
| OSDSEL    | from mod  | Asserts when OSD selected     | 5V CMOS                   |
| OSDDONE   | to mod    | Asserted when OSD completes   | 5V CMOS                   |
| SWEEP     | to mod    | Sweep gate                    | 5V CMOS                   |
| DONE      | to mod    | Sweep is done                 | 5V CMOS                   |
| INHIBIT   | from mod  | Trigger inhibit               | Open-coll active low 5V   |
| SIG+      | from mod  | Vertical signal out, +ve      | Differential, +9.0Vcm     |
| SIG-      | from mod  | Vertical signal out, -ve      | Differential, +9.0Vcm     |
| TSIG+     | from mod  | Secondary signal out, +ve     | Differential, +9.0Vcm     |
| TSIG-     | from mod  | Secondary signal out, -ve     | Differential, +9.0Vcm     |
| ADD12     | to mod    | Asserts to sum ch1+ch2        | 5V CMOS                   |
| ADD34     | to mod    | Asserts to sum ch3+ch4        | 5V CMOS                   |
| ALTINTEN  | from mod  | Selects alternate (OSD) inten | 5V CMOS                   |
| LVLEN     | to mod    | Trigger level auto enable     | 5V CMOS                   |
| ACTIVE2-0 | from mod  | Active module indicators      | 5V CMOS

LEVEL is not a critical signal; it should be routed on two of the SSn lines in the
general pinout.

ACTIVEn is decoded into a one-hot signal on the backplane. It indicates which of
the modules is currently being displayed, if any.

### OSD module

Rear-facing module with no user IOs.

| Pin       | Direction | Function                      | Mode                      |
|-----------|-----------|-------------------------------|---------------------------|
| CHAR0-5   | to mod    | Character bus                 | Open-coll active low 5V   |
| POS0-2    | from mod  | Position select bus           | 5V CMOS                   |
| SEL0-2    | from mod  | Source enable lines           | 5V CMOS                   |
| OSDSEL    | to mod    | Asserted to start OSD scan    | 5V CMOS                   |
| OSDDONE   | from mod  | Asserts when finished         | 5V CMOS                   |
| HSCAN+    | from mod  | Horizontal scan, +ve          | Differential, +4.5Vcm     |
| HSCAN-    | from mod  | Horizontal scan, -ve          | Differential, +4.5Vcm     |
| VSCAN+    | from mod  | Vertical scan, +ve            | Differential, +4.5Vcm     |
| VSCAN+    | from mod  | Vertical scan, -ve            | Differential, +4.5Vcm     |
| BEAMINHIB | from mod  | Asserts to inhibit beam       | Open-coll active low 5V   |

SELn are binary outputs; these are decoded to individual enable lines on the
backplane.

### Deflection amplifier module

User IO:
    - BNC jack with 1V/div output

| Pin       | Direction | Function                      | Mode                      |
|-----------|-----------|-------------------------------|---------------------------|
| SIG+      | to mod    | Signal to display             | Differential, +9.0Vcm     |
| SIG-      | to mod    | Signal to display             | Differential, +9.0Vcm     |

### Cathode control module

Front-facing module with controls:

- Brightness, main
- Brightness, OSD
- Focus
- Astig
- Rotation

| Pin       | Direction | Function                          | Mode                      |
|-----------|-----------|-----------------------------------|---------------------------|
| INTEN     | to mod    | Asserts to intensify beam         | Open-coll active low 5V   |
| INHIB     | to mod    | Inhibits beam (overrides INTEN)   | Open-coll active low 5V   |
| ALTINTEN  | to mod    | Selects alternate (OSD) intensity | 5V CMOS

# General pinout

The same pinout is allocated different variant IOs depending on the module.

| Pin (C)   | Function      | Pin (B)   | Function      | Pin (A)   | Function      |
|-----------|---------------|-----------|---------------|-----------|---------------|
| C1        | g             | B1        | g             | A1        | g             |
| C2        | SIG+          | B2        | g             | A2        | TSIG+         |
| C3        | SIG-          | B3        | g             | A3        | TSIG-         |
| C4        | g             | B4        | g             | A4        | g             |
| C5        | IN1+          | B5        | g             | A5        | SS0           |
| C6        | IN1-          | B6        | g             | A6        | SS1           |
| C7        | g             | B7        | IN2+          | A7        | g             |
| C8        | g             | B8        | IN2-          | A8        | g             |
| C9        | IN3+          | B9        | g             | A9        | SS2           |
| C10       | IN3-          | B10       | g             | A10       | SS3           |
| C11       | g             | B11       | IN4+          | A11       | g             |
| C12       | g             | B12       | IN4-          | A12       | g             |
| C13       | IN5+          | B13       | g             | A13       | SS4           |
| C14       | IN5-          | B14       | g             | A14       | SS5           |
| C15       | g             | B15       | g             | A15       | g             |
| C16       | SA0           | B16       | SA1           | A16       | SA2           |
| C17       | SA3           | B17       | SA4           | A17       | g             |
| C18       | SA5           | B18       | SA6           | A18       | SA7           |
| C19       | g             | B19       | SA8           | A19       | SA9           |
| C20       | SA10          | B20       | g             | A20       | SA11          |
| C21       | SA12          | B21       | SA13          | A21       | SA14          |
| C22       | SA15          | B22       | g             | A22       | g             |
| C23       | CHAR2         | B23       | CHAR1         | A23       | CHAR0         |
| C24       | CHAR5         | B24       | CHAR4         | A24       | CHAR3         |
| C25       | POS0          | B25       | POS1          | A25       | POS2          |
| C26       | g             | B26       | g             | A26       | +24V          |
| C27       | g             | B27       | +55V          | A27       | +24V          |
| C28       | g             | B28       | +15V          | A28       | +12V          |
| C29       | +10.00V       | B29       | g             | A29       | +12V          |
| C30       | g             | B30       | g             | A30       | +5V           |
| C31       | -55V          | B31       | -15V          | A31       | +5V           |
| C32       | g             | B32       | g             | A32       | g             |

- SSn lines are "sweep synchronous". They are located in places where toggling
during a sweep could impose noise on the display, so they should only toggle
between sweeps. Example signals to allocate here are SWEEP, DONE, SELECT (for
OSD).

- SAn lines are "sweep asynchronous". They are separated well from the analog
signal pins, and may toggle during sweep. These are generally used for all logic
signals not otherwise allocated to SSn.

- POSn, CHARn are the OSD IO lines bussed to all modules.
