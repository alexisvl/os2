# OS-2 on-screen display

## Display layout

The display has several areas where on-screen display content is overlayed with
the primary signal display:

```
VERT1   VERT2   VERT3   VERT4


>------- trig  level -------<


DESC1DESC2              HORIZ
```

All text fields are eight spaces long.

- `VERT1` through `VERT4`: each is "owned" by a different vertical channel
module. It typically displays a scale factor (like "5V") as well as one
of a few icons (a sine wave sign to indicate AC coupling, a ground symbol
for ground coupling, a Tek-style halfwidth BW for bandwidth limiting,
trigger indicators, an ohm sign for 50-ohm termination, an alert sign
for termination overheat or other critical conditions, and a transient
"IDENT" indication when a probe identifier is activated).

- `DESC1` and `DESC2` are arranged so they flow together into a single field,
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
| 0x0D  | -         |
| 0x0E  | ∿ (sine wave) |
| 0x0F  | ground symbol |
| 0x10  | BW (Tek style, combined single width) |
| 0x11  | A         |
| 0x12  | B         |
| 0x13  | C         |
| 0x14  | D         |
| 0x15  | E         |
| 0x16  | F         |
| 0x17  | G         |
| 0x18  | H         |
| 0x19  | I         |
| 0x1A  | J         |
| 0x1B  | K         |
| 0x1C  | L         |
| 0x1D  | M         |
| 0x1E  | N         |
| 0x1F  | O         |
| 0x20  | P         |
| 0x21  | Q         |
| 0x22  | R         |
| 0x23  | S         |
| 0x24  | T         |
| 0x25  | U         |
| 0x26  | V         |
| 0x27  | W         |
| 0x28  | X         |
| 0x29  | Y         |
| 0x2A  | Z         |
| 0x2B  | k         |
| 0x2C  | m         |
| 0x2D  | µ         |
| 0x2E  | n         |
| 0x2F  | p         |
| 0x30  | Ω         |
| 0x31  | s         |
| 0x32  | alert sign |
| 0x33  | rising edge |
| 0x34  | falling edge |
| 0x35  | both edges |
| 0x36  | LN (a la BW, for "LINE") |
| 0x37  | AU (a la BW, for "AUTO") |
| 0x38  | /         |
| 0x3E  | ♥         |
| 0x3F  | space     |

Codepoints `0x39` through `0x3E` are unspecified.
