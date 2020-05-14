# Character set, as importable Python

CH_0        = 0x00
CH_1        = 0x01
CH_2        = 0x02
CH_3        = 0x03
CH_4        = 0x04
CH_5        = 0x05
CH_6        = 0x06
CH_7        = 0x07
CH_8        = 0x08
CH_9        = 0x09

CH_UPPER_A  = 0x0A
CH_UPPER_B  = 0x0B
CH_UPPER_C  = 0x0C
CH_UPPER_D  = 0x0D
CH_UPPER_E  = 0x0E
CH_UPPER_F  = 0x0F
CH_UPPER_G  = 0x10
CH_UPPER_H  = 0x11
CH_UPPER_I  = 0x12
CH_UPPER_J  = 0x13
CH_UPPER_K  = 0x14
CH_UPPER_L  = 0x15
CH_UPPER_M  = 0x16
CH_UPPER_N  = 0x17
CH_UPPER_O  = 0x18
CH_UPPER_P  = 0x19
CH_UPPER_Q  = 0x1A
CH_UPPER_R  = 0x1B
CH_UPPER_S  = 0x1C
CH_UPPER_T  = 0x1D
CH_UPPER_U  = 0x1E
CH_UPPER_V  = 0x1F
CH_UPPER_W  = 0x20
CH_UPPER_X  = 0x21
CH_UPPER_Y  = 0x22
CH_UPPER_Z  = 0x23

CH_LOWER_A  = 0x24
CH_LOWER_B  = 0x25
CH_LOWER_C  = 0x26
CH_LOWER_D  = 0x27
CH_LOWER_E  = 0x28
CH_LOWER_F  = 0x29
CH_LOWER_G  = 0x2A
CH_LOWER_H  = 0x2B
CH_LOWER_I  = 0x2C
CH_LOWER_J  = 0x2D
CH_LOWER_K  = 0x2E
CH_LOWER_L  = 0x2F
CH_LOWER_M  = 0x30
CH_LOWER_N  = 0x31
CH_LOWER_O  = 0x32
CH_LOWER_P  = 0x33
CH_LOWER_Q  = 0x34
CH_LOWER_R  = 0x35
CH_LOWER_S  = 0x36
CH_LOWER_T  = 0x37
CH_LOWER_U  = 0x38
CH_LOWER_V  = 0x39
CH_LOWER_W  = 0x3A
CH_LOWER_X  = 0x3B
CH_LOWER_Y  = 0x3C
CH_LOWER_Z  = 0x3D

CH_PERIOD   = 0x3E
CH_COMMA    = 0x3F
CH_QUESTION = 0x40
CH_EXCLAM   = 0x41
CH_HASH     = 0x42
CH_PERCENT  = 0x43
CH_AMPER    = 0x44
CH_L_AND    = 0x45
CH_L_OR     = 0x46
CH_L_XOR    = 0x47
CH_L_NOT    = 0x48
CH_PAREN_L  = 0x49
CH_PAREN_R  = 0x4A
CH_SQUOTE   = 0x4B
CH_DQUOTE   = 0x4C

CH_TR_RISE  = 0x4D
CH_TR_FALL  = 0x4E
CH_TR_BOTH  = 0x4F

CH_MINUS    = 0x50
CH_PLUS     = 0x51
CH_PLUSMINUS= 0x52
CH_TIMES    = 0x53
CH_DIVIDE   = 0x54
CH_LESS     = 0x55
CH_LESSEQ   = 0x56
CH_EQUAL    = 0x57
CH_GREATEQ  = 0x58
CH_GREATER  = 0x59
CH_NOTEQUAL = 0x5A

CH_LEFT     = 0x5B
CH_RIGHT    = 0x5C
CH_UP       = 0x5D
CH_DOWN     = 0x5E
CH_BACKSLS  = 0x5F
CH_FWDSLS   = 0x60
CH_UNDERSCR = 0x61

CH_LOWER_ALPHA  = 0x62
CH_LOWER_BETA   = 0x63
CH_UPPER_DELTA  = 0x64
CH_LOWER_DELTA  = 0x65
CH_DERIV_DELTA  = 0x66
CH_LOWER_THETA  = 0x67
CH_LOWER_LAMBDA = 0x68
CH_LOWER_MU     = 0x69
CH_LOWER_PI     = 0x6A
CH_LOWER_TAU    = 0x6B
CH_LOWER_PHI    = 0x6C
CH_UPPER_OMEGA  = 0x6D
CH_LOWER_OMEGA  = 0x6E

CH_DEGREE       = 0x6F
CH_FUNCTION     = 0x70
CH_INTEGRAL     = 0x71
CH_SQUARED      = 0x72
CH_CARET        = 0x73
CH_RADICAL      = 0x74
CH_SINE         = 0x75
CH_GROUND       = 0x76
CH_BW           = 0x77
CH_LN           = 0x78
CH_AU           = 0x79
CH_SMILE        = 0x7A
CH_FROWN        = 0x7B
CH_HEART        = 0x7C
CH_50BLOCK      = 0x7D
CH_BLOCK        = 0x7E
CH_SPACE        = 0x7F

mapping = [
    ("0",   CH_0),
    ("1",   CH_1),
    ("2",   CH_2),
    ("3",   CH_3),
    ("4",   CH_4),
    ("5",   CH_5),
    ("6",   CH_6),
    ("7",   CH_7),
    ("8",   CH_8),
    ("9",   CH_9),

    ("A",   CH_UPPER_A),
    ("B",   CH_UPPER_B),
    ("C",   CH_UPPER_C),
    ("D",   CH_UPPER_D),
    ("E",   CH_UPPER_E),
    ("F",   CH_UPPER_F),
    ("G",   CH_UPPER_G),
    ("H",   CH_UPPER_H),
    ("I",   CH_UPPER_I),
    ("J",   CH_UPPER_J),
    ("K",   CH_UPPER_K),
    ("L",   CH_UPPER_L),
    ("M",   CH_UPPER_M),
    ("N",   CH_UPPER_N),
    ("O",   CH_UPPER_O),
    ("P",   CH_UPPER_P),
    ("Q",   CH_UPPER_Q),
    ("R",   CH_UPPER_R),
    ("S",   CH_UPPER_S),
    ("T",   CH_UPPER_T),
    ("U",   CH_UPPER_U),
    ("V",   CH_UPPER_V),
    ("W",   CH_UPPER_W),
    ("X",   CH_UPPER_X),
    ("Y",   CH_UPPER_Y),
    ("Z",   CH_UPPER_Z),

    ("a",   CH_LOWER_A),
    ("b",   CH_LOWER_B),
    ("c",   CH_LOWER_C),
    ("d",   CH_LOWER_D),
    ("e",   CH_LOWER_E),
    ("f",   CH_LOWER_F),
    ("g",   CH_LOWER_G),
    ("h",   CH_LOWER_H),
    ("i",   CH_LOWER_I),
    ("j",   CH_LOWER_J),
    ("k",   CH_LOWER_K),
    ("l",   CH_LOWER_L),
    ("m",   CH_LOWER_M),
    ("n",   CH_LOWER_N),
    ("o",   CH_LOWER_O),
    ("p",   CH_LOWER_P),
    ("q",   CH_LOWER_Q),
    ("r",   CH_LOWER_R),
    ("s",   CH_LOWER_S),
    ("t",   CH_LOWER_T),
    ("u",   CH_LOWER_U),
    ("v",   CH_LOWER_V),
    ("w",   CH_LOWER_W),
    ("x",   CH_LOWER_X),
    ("y",   CH_LOWER_Y),
    ("z",   CH_LOWER_Z),

    (".",       CH_PERIOD),
    (",",       CH_COMMA),
    ("?",       CH_QUESTION),
    ("!",       CH_EXCLAM),
    ("#",       CH_HASH),
    ("%",       CH_PERCENT),
    ("&",       CH_AMPER),
    ("{and}",   CH_L_AND),
    ("{or}",    CH_L_OR),
    ("{xor}",   CH_L_XOR),
    ("{not}",   CH_L_NOT),
    ("(",       CH_PAREN_L),
    (")",       CH_PAREN_R),
    ("'",       CH_SQUOTE),
    ("\"",      CH_DQUOTE),
    ("{rise}",  CH_TR_RISE),
    ("{fall}",  CH_TR_FALL),
    ("{both}",  CH_TR_BOTH),

    ("-",       CH_MINUS),
    ("+",       CH_PLUS),
    ("±",       CH_PLUSMINUS),
    ("×",       CH_TIMES),
    ("÷",       CH_DIVIDE),
    ("<",       CH_LESS),
    ("≤",       CH_LESSEQ),
    ("=",       CH_EQUAL),
    ("≥",       CH_GREATEQ),
    (">",       CH_GREATER),
    ("≠",       CH_NOTEQUAL),

    ("{left}",  CH_LEFT),
    ("{right}", CH_RIGHT),
    ("{up}",    CH_UP),
    ("{down}",  CH_DOWN),
    ("\\",      CH_BACKSLS),
    ("/",       CH_FWDSLS),
    ("_",       CH_UNDERSCR),

    ("{alpha}", CH_LOWER_ALPHA),
    ("{beta}",  CH_LOWER_BETA),
    ("{Delta}", CH_UPPER_DELTA),
    ("{delta}", CH_LOWER_DELTA),
    ("{deriv}", CH_DERIV_DELTA),
    ("{theta}", CH_LOWER_THETA),
    ("{lambda}",CH_LOWER_LAMBDA),
    ("{mu}",    CH_LOWER_MU),
    ("µ",       CH_LOWER_MU),
    ("{pi}",    CH_LOWER_PI),
    ("{tau}",   CH_LOWER_TAU),
    ("{phi}",   CH_LOWER_PHI),
    ("{Omega}", CH_UPPER_OMEGA),
    ("{omega}", CH_LOWER_OMEGA),

    ("°",       CH_DEGREE),
    ("{func}",  CH_FUNCTION),
    ("{intg}",  CH_INTEGRAL),
    ("²",       CH_SQUARED),
    ("^",       CH_CARET),
    ("{root}",  CH_RADICAL),
    ("{sine}",  CH_SINE),
    ("{gnd}",   CH_GROUND),
    ("{bw}",    CH_BW),
    ("{ln}",    CH_LN),
    ("{au}",    CH_AU),
    ("{:)}",    CH_SMILE),
    ("{:(}",    CH_FROWN),
    ("{<3}",    CH_HEART),
    ("{50block}", CH_50BLOCK),
    ("{block}", CH_BLOCK),
    (" ",       CH_SPACE),
]

def encode(s):
    out = []
    i = 0
    while i < len(s):
        for mnemonic, value in mapping:
            if s.startswith(mnemonic, i):
                out.append(value)
                i += len(mnemonic)
                break
        else:
            raise ValueError(f"cannot convert {s[i]!r}")
    return bytes(out)
