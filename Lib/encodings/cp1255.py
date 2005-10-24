""" Python Character Mapping Codec generated from 'MAPPINGS/VENDORS/MICSFT/WINDOWS/CP1255.TXT' with gencodec.py.

"""#"

import codecs

### Codec APIs

class Codec(codecs.Codec):

    def encode(self,input,errors='strict'):

        return codecs.charmap_encode(input,errors,encoding_map)

    def decode(self,input,errors='strict'):

        return codecs.charmap_decode(input,errors,decoding_table)
    
class StreamWriter(Codec,codecs.StreamWriter):
    pass

class StreamReader(Codec,codecs.StreamReader):
    pass

### encodings module API

def getregentry():

    return (Codec().encode,Codec().decode,StreamReader,StreamWriter)


### Decoding Table

decoding_table = (
    u'\x00'	#  0x00 -> NULL
    u'\x01'	#  0x01 -> START OF HEADING
    u'\x02'	#  0x02 -> START OF TEXT
    u'\x03'	#  0x03 -> END OF TEXT
    u'\x04'	#  0x04 -> END OF TRANSMISSION
    u'\x05'	#  0x05 -> ENQUIRY
    u'\x06'	#  0x06 -> ACKNOWLEDGE
    u'\x07'	#  0x07 -> BELL
    u'\x08'	#  0x08 -> BACKSPACE
    u'\t'	#  0x09 -> HORIZONTAL TABULATION
    u'\n'	#  0x0a -> LINE FEED
    u'\x0b'	#  0x0b -> VERTICAL TABULATION
    u'\x0c'	#  0x0c -> FORM FEED
    u'\r'	#  0x0d -> CARRIAGE RETURN
    u'\x0e'	#  0x0e -> SHIFT OUT
    u'\x0f'	#  0x0f -> SHIFT IN
    u'\x10'	#  0x10 -> DATA LINK ESCAPE
    u'\x11'	#  0x11 -> DEVICE CONTROL ONE
    u'\x12'	#  0x12 -> DEVICE CONTROL TWO
    u'\x13'	#  0x13 -> DEVICE CONTROL THREE
    u'\x14'	#  0x14 -> DEVICE CONTROL FOUR
    u'\x15'	#  0x15 -> NEGATIVE ACKNOWLEDGE
    u'\x16'	#  0x16 -> SYNCHRONOUS IDLE
    u'\x17'	#  0x17 -> END OF TRANSMISSION BLOCK
    u'\x18'	#  0x18 -> CANCEL
    u'\x19'	#  0x19 -> END OF MEDIUM
    u'\x1a'	#  0x1a -> SUBSTITUTE
    u'\x1b'	#  0x1b -> ESCAPE
    u'\x1c'	#  0x1c -> FILE SEPARATOR
    u'\x1d'	#  0x1d -> GROUP SEPARATOR
    u'\x1e'	#  0x1e -> RECORD SEPARATOR
    u'\x1f'	#  0x1f -> UNIT SEPARATOR
    u' '	#  0x20 -> SPACE
    u'!'	#  0x21 -> EXCLAMATION MARK
    u'"'	#  0x22 -> QUOTATION MARK
    u'#'	#  0x23 -> NUMBER SIGN
    u'$'	#  0x24 -> DOLLAR SIGN
    u'%'	#  0x25 -> PERCENT SIGN
    u'&'	#  0x26 -> AMPERSAND
    u"'"	#  0x27 -> APOSTROPHE
    u'('	#  0x28 -> LEFT PARENTHESIS
    u')'	#  0x29 -> RIGHT PARENTHESIS
    u'*'	#  0x2a -> ASTERISK
    u'+'	#  0x2b -> PLUS SIGN
    u','	#  0x2c -> COMMA
    u'-'	#  0x2d -> HYPHEN-MINUS
    u'.'	#  0x2e -> FULL STOP
    u'/'	#  0x2f -> SOLIDUS
    u'0'	#  0x30 -> DIGIT ZERO
    u'1'	#  0x31 -> DIGIT ONE
    u'2'	#  0x32 -> DIGIT TWO
    u'3'	#  0x33 -> DIGIT THREE
    u'4'	#  0x34 -> DIGIT FOUR
    u'5'	#  0x35 -> DIGIT FIVE
    u'6'	#  0x36 -> DIGIT SIX
    u'7'	#  0x37 -> DIGIT SEVEN
    u'8'	#  0x38 -> DIGIT EIGHT
    u'9'	#  0x39 -> DIGIT NINE
    u':'	#  0x3a -> COLON
    u';'	#  0x3b -> SEMICOLON
    u'<'	#  0x3c -> LESS-THAN SIGN
    u'='	#  0x3d -> EQUALS SIGN
    u'>'	#  0x3e -> GREATER-THAN SIGN
    u'?'	#  0x3f -> QUESTION MARK
    u'@'	#  0x40 -> COMMERCIAL AT
    u'A'	#  0x41 -> LATIN CAPITAL LETTER A
    u'B'	#  0x42 -> LATIN CAPITAL LETTER B
    u'C'	#  0x43 -> LATIN CAPITAL LETTER C
    u'D'	#  0x44 -> LATIN CAPITAL LETTER D
    u'E'	#  0x45 -> LATIN CAPITAL LETTER E
    u'F'	#  0x46 -> LATIN CAPITAL LETTER F
    u'G'	#  0x47 -> LATIN CAPITAL LETTER G
    u'H'	#  0x48 -> LATIN CAPITAL LETTER H
    u'I'	#  0x49 -> LATIN CAPITAL LETTER I
    u'J'	#  0x4a -> LATIN CAPITAL LETTER J
    u'K'	#  0x4b -> LATIN CAPITAL LETTER K
    u'L'	#  0x4c -> LATIN CAPITAL LETTER L
    u'M'	#  0x4d -> LATIN CAPITAL LETTER M
    u'N'	#  0x4e -> LATIN CAPITAL LETTER N
    u'O'	#  0x4f -> LATIN CAPITAL LETTER O
    u'P'	#  0x50 -> LATIN CAPITAL LETTER P
    u'Q'	#  0x51 -> LATIN CAPITAL LETTER Q
    u'R'	#  0x52 -> LATIN CAPITAL LETTER R
    u'S'	#  0x53 -> LATIN CAPITAL LETTER S
    u'T'	#  0x54 -> LATIN CAPITAL LETTER T
    u'U'	#  0x55 -> LATIN CAPITAL LETTER U
    u'V'	#  0x56 -> LATIN CAPITAL LETTER V
    u'W'	#  0x57 -> LATIN CAPITAL LETTER W
    u'X'	#  0x58 -> LATIN CAPITAL LETTER X
    u'Y'	#  0x59 -> LATIN CAPITAL LETTER Y
    u'Z'	#  0x5a -> LATIN CAPITAL LETTER Z
    u'['	#  0x5b -> LEFT SQUARE BRACKET
    u'\\'	#  0x5c -> REVERSE SOLIDUS
    u']'	#  0x5d -> RIGHT SQUARE BRACKET
    u'^'	#  0x5e -> CIRCUMFLEX ACCENT
    u'_'	#  0x5f -> LOW LINE
    u'`'	#  0x60 -> GRAVE ACCENT
    u'a'	#  0x61 -> LATIN SMALL LETTER A
    u'b'	#  0x62 -> LATIN SMALL LETTER B
    u'c'	#  0x63 -> LATIN SMALL LETTER C
    u'd'	#  0x64 -> LATIN SMALL LETTER D
    u'e'	#  0x65 -> LATIN SMALL LETTER E
    u'f'	#  0x66 -> LATIN SMALL LETTER F
    u'g'	#  0x67 -> LATIN SMALL LETTER G
    u'h'	#  0x68 -> LATIN SMALL LETTER H
    u'i'	#  0x69 -> LATIN SMALL LETTER I
    u'j'	#  0x6a -> LATIN SMALL LETTER J
    u'k'	#  0x6b -> LATIN SMALL LETTER K
    u'l'	#  0x6c -> LATIN SMALL LETTER L
    u'm'	#  0x6d -> LATIN SMALL LETTER M
    u'n'	#  0x6e -> LATIN SMALL LETTER N
    u'o'	#  0x6f -> LATIN SMALL LETTER O
    u'p'	#  0x70 -> LATIN SMALL LETTER P
    u'q'	#  0x71 -> LATIN SMALL LETTER Q
    u'r'	#  0x72 -> LATIN SMALL LETTER R
    u's'	#  0x73 -> LATIN SMALL LETTER S
    u't'	#  0x74 -> LATIN SMALL LETTER T
    u'u'	#  0x75 -> LATIN SMALL LETTER U
    u'v'	#  0x76 -> LATIN SMALL LETTER V
    u'w'	#  0x77 -> LATIN SMALL LETTER W
    u'x'	#  0x78 -> LATIN SMALL LETTER X
    u'y'	#  0x79 -> LATIN SMALL LETTER Y
    u'z'	#  0x7a -> LATIN SMALL LETTER Z
    u'{'	#  0x7b -> LEFT CURLY BRACKET
    u'|'	#  0x7c -> VERTICAL LINE
    u'}'	#  0x7d -> RIGHT CURLY BRACKET
    u'~'	#  0x7e -> TILDE
    u'\x7f'	#  0x7f -> DELETE
    u'\u20ac'	#  0x80 -> EURO SIGN
    u'\ufffe'	#  0x81 -> UNDEFINED
    u'\u201a'	#  0x82 -> SINGLE LOW-9 QUOTATION MARK
    u'\u0192'	#  0x83 -> LATIN SMALL LETTER F WITH HOOK
    u'\u201e'	#  0x84 -> DOUBLE LOW-9 QUOTATION MARK
    u'\u2026'	#  0x85 -> HORIZONTAL ELLIPSIS
    u'\u2020'	#  0x86 -> DAGGER
    u'\u2021'	#  0x87 -> DOUBLE DAGGER
    u'\u02c6'	#  0x88 -> MODIFIER LETTER CIRCUMFLEX ACCENT
    u'\u2030'	#  0x89 -> PER MILLE SIGN
    u'\ufffe'	#  0x8a -> UNDEFINED
    u'\u2039'	#  0x8b -> SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    u'\ufffe'	#  0x8c -> UNDEFINED
    u'\ufffe'	#  0x8d -> UNDEFINED
    u'\ufffe'	#  0x8e -> UNDEFINED
    u'\ufffe'	#  0x8f -> UNDEFINED
    u'\ufffe'	#  0x90 -> UNDEFINED
    u'\u2018'	#  0x91 -> LEFT SINGLE QUOTATION MARK
    u'\u2019'	#  0x92 -> RIGHT SINGLE QUOTATION MARK
    u'\u201c'	#  0x93 -> LEFT DOUBLE QUOTATION MARK
    u'\u201d'	#  0x94 -> RIGHT DOUBLE QUOTATION MARK
    u'\u2022'	#  0x95 -> BULLET
    u'\u2013'	#  0x96 -> EN DASH
    u'\u2014'	#  0x97 -> EM DASH
    u'\u02dc'	#  0x98 -> SMALL TILDE
    u'\u2122'	#  0x99 -> TRADE MARK SIGN
    u'\ufffe'	#  0x9a -> UNDEFINED
    u'\u203a'	#  0x9b -> SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    u'\ufffe'	#  0x9c -> UNDEFINED
    u'\ufffe'	#  0x9d -> UNDEFINED
    u'\ufffe'	#  0x9e -> UNDEFINED
    u'\ufffe'	#  0x9f -> UNDEFINED
    u'\xa0'	#  0xa0 -> NO-BREAK SPACE
    u'\xa1'	#  0xa1 -> INVERTED EXCLAMATION MARK
    u'\xa2'	#  0xa2 -> CENT SIGN
    u'\xa3'	#  0xa3 -> POUND SIGN
    u'\u20aa'	#  0xa4 -> NEW SHEQEL SIGN
    u'\xa5'	#  0xa5 -> YEN SIGN
    u'\xa6'	#  0xa6 -> BROKEN BAR
    u'\xa7'	#  0xa7 -> SECTION SIGN
    u'\xa8'	#  0xa8 -> DIAERESIS
    u'\xa9'	#  0xa9 -> COPYRIGHT SIGN
    u'\xd7'	#  0xaa -> MULTIPLICATION SIGN
    u'\xab'	#  0xab -> LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    u'\xac'	#  0xac -> NOT SIGN
    u'\xad'	#  0xad -> SOFT HYPHEN
    u'\xae'	#  0xae -> REGISTERED SIGN
    u'\xaf'	#  0xaf -> MACRON
    u'\xb0'	#  0xb0 -> DEGREE SIGN
    u'\xb1'	#  0xb1 -> PLUS-MINUS SIGN
    u'\xb2'	#  0xb2 -> SUPERSCRIPT TWO
    u'\xb3'	#  0xb3 -> SUPERSCRIPT THREE
    u'\xb4'	#  0xb4 -> ACUTE ACCENT
    u'\xb5'	#  0xb5 -> MICRO SIGN
    u'\xb6'	#  0xb6 -> PILCROW SIGN
    u'\xb7'	#  0xb7 -> MIDDLE DOT
    u'\xb8'	#  0xb8 -> CEDILLA
    u'\xb9'	#  0xb9 -> SUPERSCRIPT ONE
    u'\xf7'	#  0xba -> DIVISION SIGN
    u'\xbb'	#  0xbb -> RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    u'\xbc'	#  0xbc -> VULGAR FRACTION ONE QUARTER
    u'\xbd'	#  0xbd -> VULGAR FRACTION ONE HALF
    u'\xbe'	#  0xbe -> VULGAR FRACTION THREE QUARTERS
    u'\xbf'	#  0xbf -> INVERTED QUESTION MARK
    u'\u05b0'	#  0xc0 -> HEBREW POINT SHEVA
    u'\u05b1'	#  0xc1 -> HEBREW POINT HATAF SEGOL
    u'\u05b2'	#  0xc2 -> HEBREW POINT HATAF PATAH
    u'\u05b3'	#  0xc3 -> HEBREW POINT HATAF QAMATS
    u'\u05b4'	#  0xc4 -> HEBREW POINT HIRIQ
    u'\u05b5'	#  0xc5 -> HEBREW POINT TSERE
    u'\u05b6'	#  0xc6 -> HEBREW POINT SEGOL
    u'\u05b7'	#  0xc7 -> HEBREW POINT PATAH
    u'\u05b8'	#  0xc8 -> HEBREW POINT QAMATS
    u'\u05b9'	#  0xc9 -> HEBREW POINT HOLAM
    u'\ufffe'	#  0xca -> UNDEFINED
    u'\u05bb'	#  0xcb -> HEBREW POINT QUBUTS
    u'\u05bc'	#  0xcc -> HEBREW POINT DAGESH OR MAPIQ
    u'\u05bd'	#  0xcd -> HEBREW POINT METEG
    u'\u05be'	#  0xce -> HEBREW PUNCTUATION MAQAF
    u'\u05bf'	#  0xcf -> HEBREW POINT RAFE
    u'\u05c0'	#  0xd0 -> HEBREW PUNCTUATION PASEQ
    u'\u05c1'	#  0xd1 -> HEBREW POINT SHIN DOT
    u'\u05c2'	#  0xd2 -> HEBREW POINT SIN DOT
    u'\u05c3'	#  0xd3 -> HEBREW PUNCTUATION SOF PASUQ
    u'\u05f0'	#  0xd4 -> HEBREW LIGATURE YIDDISH DOUBLE VAV
    u'\u05f1'	#  0xd5 -> HEBREW LIGATURE YIDDISH VAV YOD
    u'\u05f2'	#  0xd6 -> HEBREW LIGATURE YIDDISH DOUBLE YOD
    u'\u05f3'	#  0xd7 -> HEBREW PUNCTUATION GERESH
    u'\u05f4'	#  0xd8 -> HEBREW PUNCTUATION GERSHAYIM
    u'\ufffe'	#  0xd9 -> UNDEFINED
    u'\ufffe'	#  0xda -> UNDEFINED
    u'\ufffe'	#  0xdb -> UNDEFINED
    u'\ufffe'	#  0xdc -> UNDEFINED
    u'\ufffe'	#  0xdd -> UNDEFINED
    u'\ufffe'	#  0xde -> UNDEFINED
    u'\ufffe'	#  0xdf -> UNDEFINED
    u'\u05d0'	#  0xe0 -> HEBREW LETTER ALEF
    u'\u05d1'	#  0xe1 -> HEBREW LETTER BET
    u'\u05d2'	#  0xe2 -> HEBREW LETTER GIMEL
    u'\u05d3'	#  0xe3 -> HEBREW LETTER DALET
    u'\u05d4'	#  0xe4 -> HEBREW LETTER HE
    u'\u05d5'	#  0xe5 -> HEBREW LETTER VAV
    u'\u05d6'	#  0xe6 -> HEBREW LETTER ZAYIN
    u'\u05d7'	#  0xe7 -> HEBREW LETTER HET
    u'\u05d8'	#  0xe8 -> HEBREW LETTER TET
    u'\u05d9'	#  0xe9 -> HEBREW LETTER YOD
    u'\u05da'	#  0xea -> HEBREW LETTER FINAL KAF
    u'\u05db'	#  0xeb -> HEBREW LETTER KAF
    u'\u05dc'	#  0xec -> HEBREW LETTER LAMED
    u'\u05dd'	#  0xed -> HEBREW LETTER FINAL MEM
    u'\u05de'	#  0xee -> HEBREW LETTER MEM
    u'\u05df'	#  0xef -> HEBREW LETTER FINAL NUN
    u'\u05e0'	#  0xf0 -> HEBREW LETTER NUN
    u'\u05e1'	#  0xf1 -> HEBREW LETTER SAMEKH
    u'\u05e2'	#  0xf2 -> HEBREW LETTER AYIN
    u'\u05e3'	#  0xf3 -> HEBREW LETTER FINAL PE
    u'\u05e4'	#  0xf4 -> HEBREW LETTER PE
    u'\u05e5'	#  0xf5 -> HEBREW LETTER FINAL TSADI
    u'\u05e6'	#  0xf6 -> HEBREW LETTER TSADI
    u'\u05e7'	#  0xf7 -> HEBREW LETTER QOF
    u'\u05e8'	#  0xf8 -> HEBREW LETTER RESH
    u'\u05e9'	#  0xf9 -> HEBREW LETTER SHIN
    u'\u05ea'	#  0xfa -> HEBREW LETTER TAV
    u'\ufffe'	#  0xfb -> UNDEFINED
    u'\ufffe'	#  0xfc -> UNDEFINED
    u'\u200e'	#  0xfd -> LEFT-TO-RIGHT MARK
    u'\u200f'	#  0xfe -> RIGHT-TO-LEFT MARK
    u'\ufffe'	#  0xff -> UNDEFINED
)

### Encoding Map

encoding_map = {
    0x0000: 0x00,	#  NULL
    0x0001: 0x01,	#  START OF HEADING
    0x0002: 0x02,	#  START OF TEXT
    0x0003: 0x03,	#  END OF TEXT
    0x0004: 0x04,	#  END OF TRANSMISSION
    0x0005: 0x05,	#  ENQUIRY
    0x0006: 0x06,	#  ACKNOWLEDGE
    0x0007: 0x07,	#  BELL
    0x0008: 0x08,	#  BACKSPACE
    0x0009: 0x09,	#  HORIZONTAL TABULATION
    0x000a: 0x0a,	#  LINE FEED
    0x000b: 0x0b,	#  VERTICAL TABULATION
    0x000c: 0x0c,	#  FORM FEED
    0x000d: 0x0d,	#  CARRIAGE RETURN
    0x000e: 0x0e,	#  SHIFT OUT
    0x000f: 0x0f,	#  SHIFT IN
    0x0010: 0x10,	#  DATA LINK ESCAPE
    0x0011: 0x11,	#  DEVICE CONTROL ONE
    0x0012: 0x12,	#  DEVICE CONTROL TWO
    0x0013: 0x13,	#  DEVICE CONTROL THREE
    0x0014: 0x14,	#  DEVICE CONTROL FOUR
    0x0015: 0x15,	#  NEGATIVE ACKNOWLEDGE
    0x0016: 0x16,	#  SYNCHRONOUS IDLE
    0x0017: 0x17,	#  END OF TRANSMISSION BLOCK
    0x0018: 0x18,	#  CANCEL
    0x0019: 0x19,	#  END OF MEDIUM
    0x001a: 0x1a,	#  SUBSTITUTE
    0x001b: 0x1b,	#  ESCAPE
    0x001c: 0x1c,	#  FILE SEPARATOR
    0x001d: 0x1d,	#  GROUP SEPARATOR
    0x001e: 0x1e,	#  RECORD SEPARATOR
    0x001f: 0x1f,	#  UNIT SEPARATOR
    0x0020: 0x20,	#  SPACE
    0x0021: 0x21,	#  EXCLAMATION MARK
    0x0022: 0x22,	#  QUOTATION MARK
    0x0023: 0x23,	#  NUMBER SIGN
    0x0024: 0x24,	#  DOLLAR SIGN
    0x0025: 0x25,	#  PERCENT SIGN
    0x0026: 0x26,	#  AMPERSAND
    0x0027: 0x27,	#  APOSTROPHE
    0x0028: 0x28,	#  LEFT PARENTHESIS
    0x0029: 0x29,	#  RIGHT PARENTHESIS
    0x002a: 0x2a,	#  ASTERISK
    0x002b: 0x2b,	#  PLUS SIGN
    0x002c: 0x2c,	#  COMMA
    0x002d: 0x2d,	#  HYPHEN-MINUS
    0x002e: 0x2e,	#  FULL STOP
    0x002f: 0x2f,	#  SOLIDUS
    0x0030: 0x30,	#  DIGIT ZERO
    0x0031: 0x31,	#  DIGIT ONE
    0x0032: 0x32,	#  DIGIT TWO
    0x0033: 0x33,	#  DIGIT THREE
    0x0034: 0x34,	#  DIGIT FOUR
    0x0035: 0x35,	#  DIGIT FIVE
    0x0036: 0x36,	#  DIGIT SIX
    0x0037: 0x37,	#  DIGIT SEVEN
    0x0038: 0x38,	#  DIGIT EIGHT
    0x0039: 0x39,	#  DIGIT NINE
    0x003a: 0x3a,	#  COLON
    0x003b: 0x3b,	#  SEMICOLON
    0x003c: 0x3c,	#  LESS-THAN SIGN
    0x003d: 0x3d,	#  EQUALS SIGN
    0x003e: 0x3e,	#  GREATER-THAN SIGN
    0x003f: 0x3f,	#  QUESTION MARK
    0x0040: 0x40,	#  COMMERCIAL AT
    0x0041: 0x41,	#  LATIN CAPITAL LETTER A
    0x0042: 0x42,	#  LATIN CAPITAL LETTER B
    0x0043: 0x43,	#  LATIN CAPITAL LETTER C
    0x0044: 0x44,	#  LATIN CAPITAL LETTER D
    0x0045: 0x45,	#  LATIN CAPITAL LETTER E
    0x0046: 0x46,	#  LATIN CAPITAL LETTER F
    0x0047: 0x47,	#  LATIN CAPITAL LETTER G
    0x0048: 0x48,	#  LATIN CAPITAL LETTER H
    0x0049: 0x49,	#  LATIN CAPITAL LETTER I
    0x004a: 0x4a,	#  LATIN CAPITAL LETTER J
    0x004b: 0x4b,	#  LATIN CAPITAL LETTER K
    0x004c: 0x4c,	#  LATIN CAPITAL LETTER L
    0x004d: 0x4d,	#  LATIN CAPITAL LETTER M
    0x004e: 0x4e,	#  LATIN CAPITAL LETTER N
    0x004f: 0x4f,	#  LATIN CAPITAL LETTER O
    0x0050: 0x50,	#  LATIN CAPITAL LETTER P
    0x0051: 0x51,	#  LATIN CAPITAL LETTER Q
    0x0052: 0x52,	#  LATIN CAPITAL LETTER R
    0x0053: 0x53,	#  LATIN CAPITAL LETTER S
    0x0054: 0x54,	#  LATIN CAPITAL LETTER T
    0x0055: 0x55,	#  LATIN CAPITAL LETTER U
    0x0056: 0x56,	#  LATIN CAPITAL LETTER V
    0x0057: 0x57,	#  LATIN CAPITAL LETTER W
    0x0058: 0x58,	#  LATIN CAPITAL LETTER X
    0x0059: 0x59,	#  LATIN CAPITAL LETTER Y
    0x005a: 0x5a,	#  LATIN CAPITAL LETTER Z
    0x005b: 0x5b,	#  LEFT SQUARE BRACKET
    0x005c: 0x5c,	#  REVERSE SOLIDUS
    0x005d: 0x5d,	#  RIGHT SQUARE BRACKET
    0x005e: 0x5e,	#  CIRCUMFLEX ACCENT
    0x005f: 0x5f,	#  LOW LINE
    0x0060: 0x60,	#  GRAVE ACCENT
    0x0061: 0x61,	#  LATIN SMALL LETTER A
    0x0062: 0x62,	#  LATIN SMALL LETTER B
    0x0063: 0x63,	#  LATIN SMALL LETTER C
    0x0064: 0x64,	#  LATIN SMALL LETTER D
    0x0065: 0x65,	#  LATIN SMALL LETTER E
    0x0066: 0x66,	#  LATIN SMALL LETTER F
    0x0067: 0x67,	#  LATIN SMALL LETTER G
    0x0068: 0x68,	#  LATIN SMALL LETTER H
    0x0069: 0x69,	#  LATIN SMALL LETTER I
    0x006a: 0x6a,	#  LATIN SMALL LETTER J
    0x006b: 0x6b,	#  LATIN SMALL LETTER K
    0x006c: 0x6c,	#  LATIN SMALL LETTER L
    0x006d: 0x6d,	#  LATIN SMALL LETTER M
    0x006e: 0x6e,	#  LATIN SMALL LETTER N
    0x006f: 0x6f,	#  LATIN SMALL LETTER O
    0x0070: 0x70,	#  LATIN SMALL LETTER P
    0x0071: 0x71,	#  LATIN SMALL LETTER Q
    0x0072: 0x72,	#  LATIN SMALL LETTER R
    0x0073: 0x73,	#  LATIN SMALL LETTER S
    0x0074: 0x74,	#  LATIN SMALL LETTER T
    0x0075: 0x75,	#  LATIN SMALL LETTER U
    0x0076: 0x76,	#  LATIN SMALL LETTER V
    0x0077: 0x77,	#  LATIN SMALL LETTER W
    0x0078: 0x78,	#  LATIN SMALL LETTER X
    0x0079: 0x79,	#  LATIN SMALL LETTER Y
    0x007a: 0x7a,	#  LATIN SMALL LETTER Z
    0x007b: 0x7b,	#  LEFT CURLY BRACKET
    0x007c: 0x7c,	#  VERTICAL LINE
    0x007d: 0x7d,	#  RIGHT CURLY BRACKET
    0x007e: 0x7e,	#  TILDE
    0x007f: 0x7f,	#  DELETE
    0x00a0: 0xa0,	#  NO-BREAK SPACE
    0x00a1: 0xa1,	#  INVERTED EXCLAMATION MARK
    0x00a2: 0xa2,	#  CENT SIGN
    0x00a3: 0xa3,	#  POUND SIGN
    0x00a5: 0xa5,	#  YEN SIGN
    0x00a6: 0xa6,	#  BROKEN BAR
    0x00a7: 0xa7,	#  SECTION SIGN
    0x00a8: 0xa8,	#  DIAERESIS
    0x00a9: 0xa9,	#  COPYRIGHT SIGN
    0x00ab: 0xab,	#  LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00ac: 0xac,	#  NOT SIGN
    0x00ad: 0xad,	#  SOFT HYPHEN
    0x00ae: 0xae,	#  REGISTERED SIGN
    0x00af: 0xaf,	#  MACRON
    0x00b0: 0xb0,	#  DEGREE SIGN
    0x00b1: 0xb1,	#  PLUS-MINUS SIGN
    0x00b2: 0xb2,	#  SUPERSCRIPT TWO
    0x00b3: 0xb3,	#  SUPERSCRIPT THREE
    0x00b4: 0xb4,	#  ACUTE ACCENT
    0x00b5: 0xb5,	#  MICRO SIGN
    0x00b6: 0xb6,	#  PILCROW SIGN
    0x00b7: 0xb7,	#  MIDDLE DOT
    0x00b8: 0xb8,	#  CEDILLA
    0x00b9: 0xb9,	#  SUPERSCRIPT ONE
    0x00bb: 0xbb,	#  RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00bc: 0xbc,	#  VULGAR FRACTION ONE QUARTER
    0x00bd: 0xbd,	#  VULGAR FRACTION ONE HALF
    0x00be: 0xbe,	#  VULGAR FRACTION THREE QUARTERS
    0x00bf: 0xbf,	#  INVERTED QUESTION MARK
    0x00d7: 0xaa,	#  MULTIPLICATION SIGN
    0x00f7: 0xba,	#  DIVISION SIGN
    0x0192: 0x83,	#  LATIN SMALL LETTER F WITH HOOK
    0x02c6: 0x88,	#  MODIFIER LETTER CIRCUMFLEX ACCENT
    0x02dc: 0x98,	#  SMALL TILDE
    0x05b0: 0xc0,	#  HEBREW POINT SHEVA
    0x05b1: 0xc1,	#  HEBREW POINT HATAF SEGOL
    0x05b2: 0xc2,	#  HEBREW POINT HATAF PATAH
    0x05b3: 0xc3,	#  HEBREW POINT HATAF QAMATS
    0x05b4: 0xc4,	#  HEBREW POINT HIRIQ
    0x05b5: 0xc5,	#  HEBREW POINT TSERE
    0x05b6: 0xc6,	#  HEBREW POINT SEGOL
    0x05b7: 0xc7,	#  HEBREW POINT PATAH
    0x05b8: 0xc8,	#  HEBREW POINT QAMATS
    0x05b9: 0xc9,	#  HEBREW POINT HOLAM
    0x05bb: 0xcb,	#  HEBREW POINT QUBUTS
    0x05bc: 0xcc,	#  HEBREW POINT DAGESH OR MAPIQ
    0x05bd: 0xcd,	#  HEBREW POINT METEG
    0x05be: 0xce,	#  HEBREW PUNCTUATION MAQAF
    0x05bf: 0xcf,	#  HEBREW POINT RAFE
    0x05c0: 0xd0,	#  HEBREW PUNCTUATION PASEQ
    0x05c1: 0xd1,	#  HEBREW POINT SHIN DOT
    0x05c2: 0xd2,	#  HEBREW POINT SIN DOT
    0x05c3: 0xd3,	#  HEBREW PUNCTUATION SOF PASUQ
    0x05d0: 0xe0,	#  HEBREW LETTER ALEF
    0x05d1: 0xe1,	#  HEBREW LETTER BET
    0x05d2: 0xe2,	#  HEBREW LETTER GIMEL
    0x05d3: 0xe3,	#  HEBREW LETTER DALET
    0x05d4: 0xe4,	#  HEBREW LETTER HE
    0x05d5: 0xe5,	#  HEBREW LETTER VAV
    0x05d6: 0xe6,	#  HEBREW LETTER ZAYIN
    0x05d7: 0xe7,	#  HEBREW LETTER HET
    0x05d8: 0xe8,	#  HEBREW LETTER TET
    0x05d9: 0xe9,	#  HEBREW LETTER YOD
    0x05da: 0xea,	#  HEBREW LETTER FINAL KAF
    0x05db: 0xeb,	#  HEBREW LETTER KAF
    0x05dc: 0xec,	#  HEBREW LETTER LAMED
    0x05dd: 0xed,	#  HEBREW LETTER FINAL MEM
    0x05de: 0xee,	#  HEBREW LETTER MEM
    0x05df: 0xef,	#  HEBREW LETTER FINAL NUN
    0x05e0: 0xf0,	#  HEBREW LETTER NUN
    0x05e1: 0xf1,	#  HEBREW LETTER SAMEKH
    0x05e2: 0xf2,	#  HEBREW LETTER AYIN
    0x05e3: 0xf3,	#  HEBREW LETTER FINAL PE
    0x05e4: 0xf4,	#  HEBREW LETTER PE
    0x05e5: 0xf5,	#  HEBREW LETTER FINAL TSADI
    0x05e6: 0xf6,	#  HEBREW LETTER TSADI
    0x05e7: 0xf7,	#  HEBREW LETTER QOF
    0x05e8: 0xf8,	#  HEBREW LETTER RESH
    0x05e9: 0xf9,	#  HEBREW LETTER SHIN
    0x05ea: 0xfa,	#  HEBREW LETTER TAV
    0x05f0: 0xd4,	#  HEBREW LIGATURE YIDDISH DOUBLE VAV
    0x05f1: 0xd5,	#  HEBREW LIGATURE YIDDISH VAV YOD
    0x05f2: 0xd6,	#  HEBREW LIGATURE YIDDISH DOUBLE YOD
    0x05f3: 0xd7,	#  HEBREW PUNCTUATION GERESH
    0x05f4: 0xd8,	#  HEBREW PUNCTUATION GERSHAYIM
    0x200e: 0xfd,	#  LEFT-TO-RIGHT MARK
    0x200f: 0xfe,	#  RIGHT-TO-LEFT MARK
    0x2013: 0x96,	#  EN DASH
    0x2014: 0x97,	#  EM DASH
    0x2018: 0x91,	#  LEFT SINGLE QUOTATION MARK
    0x2019: 0x92,	#  RIGHT SINGLE QUOTATION MARK
    0x201a: 0x82,	#  SINGLE LOW-9 QUOTATION MARK
    0x201c: 0x93,	#  LEFT DOUBLE QUOTATION MARK
    0x201d: 0x94,	#  RIGHT DOUBLE QUOTATION MARK
    0x201e: 0x84,	#  DOUBLE LOW-9 QUOTATION MARK
    0x2020: 0x86,	#  DAGGER
    0x2021: 0x87,	#  DOUBLE DAGGER
    0x2022: 0x95,	#  BULLET
    0x2026: 0x85,	#  HORIZONTAL ELLIPSIS
    0x2030: 0x89,	#  PER MILLE SIGN
    0x2039: 0x8b,	#  SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    0x203a: 0x9b,	#  SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    0x20aa: 0xa4,	#  NEW SHEQEL SIGN
    0x20ac: 0x80,	#  EURO SIGN
    0x2122: 0x99,	#  TRADE MARK SIGN
}