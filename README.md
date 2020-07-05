# OS-2

![dope ass 90s under construction gif](https://images2.minutemediacdn.com/image/upload/c_fit,f_auto,fl_lossy,q_auto,w_728/v1555999902/shape/mentalfloss/construction_8.gif?itok=i0AHeyO3)

This is my attempt at building an analog oscilloscope.

Bit of a self-indulgent project and I'm just posting it here so I don't hoard
it for myself. Nothing here is probably of use to anybody, and I have no plan
on making it in any way reproducible. License for all design files and
documentation is CC BY-NC-SA, note _non-commercial_. Any code is independently
licensed, typically GPL. If you want to spend a lot of money building something
mildly useful, feel free to build one.

## Specs

- At least 20 MHz bandwidth, maybe more
- Two to four channels
    - 1mV/div to 5V/div
    - AC, DC, GND coupling; 50 ohm or 1M termination
    - Switchable bandwidth limit per channel (if the overall bandwidth is high enough?)
- On-screen display for scale factors (raster scan)
- No software - ROM LUTs and GAL/PALs at most
