# OS-2 on-screen display

## Display layout

The display has several areas where on-screen display content is overlayed with
the primary signal display:

```
VERT1   VERT2   VERT3   VERT4


>------- trig  level -------<


DESC1DESC2DESC3         HORIZ
```

All text fields are eight spaces long.

- `VERT1` through `VERT4`: each is "owned" by a different vertical channel
module. It typically displays a scale factor (like "5V") as well as one
of a few icons (a sine wave sign to indicate AC coupling, a ground symbol
for ground coupling, a Tek-style halfwidth BW for bandwidth limiting,
trigger indicators, an ohm sign for 50-ohm termination, an alert sign
for termination overheat or other critical conditions, and a transient
"IDENT" indication when a probe identifier is activated).

- `DESC1` to `DESC3` are arranged so they flow together into a single field,
and exist so that an optional captioning plugin may be used to write user-
specified labels onto the display.

- `HORIZ` displays a horizontal scale factor (like "50µs") and alternative
trigger source icons ("AU" for auto triggering, "LN" for line triggering)
that are not associated with a vertical channel.

- "Trig level" is a dashed line that can be optionally drawn across the display
at the selected trigger point. (Suggested dashed-line implementation: 555
timer, astable, reset line driven by sweep gate. This will reset it on every
sweep so the dashes line up)

All vertical channels should emit a space (0x3F, no lines asserted) for
position 0. The trigger module will insert trigger level symbols on the
relevant channel during the scan sequence.

## Character encoding

The OS-2 character encoding is six bits wide, and is defined as follows:

| Code  | Character |
|-------|-----------|
| 0x00  | 0         |
| 0x01  | 1         |
| 0x02  | 2         |
| 0x03  | 3         |
| 0x04  | 4         |
| 0x05  | 5         |
| 0x06  | 6         |
| 0x07  | 7         |
| 0x08  | 8         |
| 0x09  | 9         |
| 0x0A  | .         |
| 0x0B  | <         |
| 0x0C  | >         |
| 0x0D  | /         |
| 0x0E  | -         |
| 0x0F  | +         |
| 0x10  | ∿ (sine wave) |
| 0x11  | Ω         |
| 0x12  | ground symbol |
| 0x13  | BW (Tek style, combined single width) |
| 0x14  | LN (a la BW, for "LINE") |
| 0x15  | AU (a la BW, for "AUTO") |
| 0x16  | rising edge |
| 0x17  | falling edge |
| 0x18  | both edges |
| 0x19  | alert sign |
| 0x1A  | A         |
| 0x1B  | B         |
| 0x1C  | C         |
| 0x1D  | D         |
| 0x1E  | E         |
| 0x1F  | F         |
| 0x20  | G         |
| 0x21  | H         |
| 0x22  | I         |
| 0x23  | J         |
| 0x24  | K         |
| 0x25  | L         |
| 0x26  | M         |
| 0x27  | N         |
| 0x28  | O         |
| 0x29  | P         |
| 0x2A  | Q         |
| 0x2B  | R         |
| 0x2C  | S         |
| 0x2D  | T         |
| 0x2E  | U         |
| 0x2F  | V         |
| 0x30  | W         |
| 0x31  | X         |
| 0x32  | Y         |
| 0x33  | Z         |
| 0x34  | k         |
| 0x35  | m         |
| 0x36  | µ         |
| 0x37  | n         |
| 0x38  | p         |
| 0x39  | s         |
| 0x3A  | °         |
| 0x3B  | ?         |
| 0x3C  | ♥         |
| 0x3D  | dither block |
| 0x3E  | full block |
| 0x3F  | space     |
