""" Python Character Mapping Codec generated from 'VENDORS/APPLE/CENTEURO.TXT' with gencodec.py.

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

### Decoding Map

decoding_map = codecs.make_identity_dict(range(256))
decoding_map.update({
    0x0080: 0x00c4,	#  LATIN CAPITAL LETTER A WITH DIAERESIS
    0x0081: 0x0100,	#  LATIN CAPITAL LETTER A WITH MACRON
    0x0082: 0x0101,	#  LATIN SMALL LETTER A WITH MACRON
    0x0083: 0x00c9,	#  LATIN CAPITAL LETTER E WITH ACUTE
    0x0084: 0x0104,	#  LATIN CAPITAL LETTER A WITH OGONEK
    0x0085: 0x00d6,	#  LATIN CAPITAL LETTER O WITH DIAERESIS
    0x0086: 0x00dc,	#  LATIN CAPITAL LETTER U WITH DIAERESIS
    0x0087: 0x00e1,	#  LATIN SMALL LETTER A WITH ACUTE
    0x0088: 0x0105,	#  LATIN SMALL LETTER A WITH OGONEK
    0x0089: 0x010c,	#  LATIN CAPITAL LETTER C WITH CARON
    0x008a: 0x00e4,	#  LATIN SMALL LETTER A WITH DIAERESIS
    0x008b: 0x010d,	#  LATIN SMALL LETTER C WITH CARON
    0x008c: 0x0106,	#  LATIN CAPITAL LETTER C WITH ACUTE
    0x008d: 0x0107,	#  LATIN SMALL LETTER C WITH ACUTE
    0x008e: 0x00e9,	#  LATIN SMALL LETTER E WITH ACUTE
    0x008f: 0x0179,	#  LATIN CAPITAL LETTER Z WITH ACUTE
    0x0090: 0x017a,	#  LATIN SMALL LETTER Z WITH ACUTE
    0x0091: 0x010e,	#  LATIN CAPITAL LETTER D WITH CARON
    0x0092: 0x00ed,	#  LATIN SMALL LETTER I WITH ACUTE
    0x0093: 0x010f,	#  LATIN SMALL LETTER D WITH CARON
    0x0094: 0x0112,	#  LATIN CAPITAL LETTER E WITH MACRON
    0x0095: 0x0113,	#  LATIN SMALL LETTER E WITH MACRON
    0x0096: 0x0116,	#  LATIN CAPITAL LETTER E WITH DOT ABOVE
    0x0097: 0x00f3,	#  LATIN SMALL LETTER O WITH ACUTE
    0x0098: 0x0117,	#  LATIN SMALL LETTER E WITH DOT ABOVE
    0x0099: 0x00f4,	#  LATIN SMALL LETTER O WITH CIRCUMFLEX
    0x009a: 0x00f6,	#  LATIN SMALL LETTER O WITH DIAERESIS
    0x009b: 0x00f5,	#  LATIN SMALL LETTER O WITH TILDE
    0x009c: 0x00fa,	#  LATIN SMALL LETTER U WITH ACUTE
    0x009d: 0x011a,	#  LATIN CAPITAL LETTER E WITH CARON
    0x009e: 0x011b,	#  LATIN SMALL LETTER E WITH CARON
    0x009f: 0x00fc,	#  LATIN SMALL LETTER U WITH DIAERESIS
    0x00a0: 0x2020,	#  DAGGER
    0x00a1: 0x00b0,	#  DEGREE SIGN
    0x00a2: 0x0118,	#  LATIN CAPITAL LETTER E WITH OGONEK
    0x00a4: 0x00a7,	#  SECTION SIGN
    0x00a5: 0x2022,	#  BULLET
    0x00a6: 0x00b6,	#  PILCROW SIGN
    0x00a7: 0x00df,	#  LATIN SMALL LETTER SHARP S
    0x00a8: 0x00ae,	#  REGISTERED SIGN
    0x00aa: 0x2122,	#  TRADE MARK SIGN
    0x00ab: 0x0119,	#  LATIN SMALL LETTER E WITH OGONEK
    0x00ac: 0x00a8,	#  DIAERESIS
    0x00ad: 0x2260,	#  NOT EQUAL TO
    0x00ae: 0x0123,	#  LATIN SMALL LETTER G WITH CEDILLA
    0x00af: 0x012e,	#  LATIN CAPITAL LETTER I WITH OGONEK
    0x00b0: 0x012f,	#  LATIN SMALL LETTER I WITH OGONEK
    0x00b1: 0x012a,	#  LATIN CAPITAL LETTER I WITH MACRON
    0x00b2: 0x2264,	#  LESS-THAN OR EQUAL TO
    0x00b3: 0x2265,	#  GREATER-THAN OR EQUAL TO
    0x00b4: 0x012b,	#  LATIN SMALL LETTER I WITH MACRON
    0x00b5: 0x0136,	#  LATIN CAPITAL LETTER K WITH CEDILLA
    0x00b6: 0x2202,	#  PARTIAL DIFFERENTIAL
    0x00b7: 0x2211,	#  N-ARY SUMMATION
    0x00b8: 0x0142,	#  LATIN SMALL LETTER L WITH STROKE
    0x00b9: 0x013b,	#  LATIN CAPITAL LETTER L WITH CEDILLA
    0x00ba: 0x013c,	#  LATIN SMALL LETTER L WITH CEDILLA
    0x00bb: 0x013d,	#  LATIN CAPITAL LETTER L WITH CARON
    0x00bc: 0x013e,	#  LATIN SMALL LETTER L WITH CARON
    0x00bd: 0x0139,	#  LATIN CAPITAL LETTER L WITH ACUTE
    0x00be: 0x013a,	#  LATIN SMALL LETTER L WITH ACUTE
    0x00bf: 0x0145,	#  LATIN CAPITAL LETTER N WITH CEDILLA
    0x00c0: 0x0146,	#  LATIN SMALL LETTER N WITH CEDILLA
    0x00c1: 0x0143,	#  LATIN CAPITAL LETTER N WITH ACUTE
    0x00c2: 0x00ac,	#  NOT SIGN
    0x00c3: 0x221a,	#  SQUARE ROOT
    0x00c4: 0x0144,	#  LATIN SMALL LETTER N WITH ACUTE
    0x00c5: 0x0147,	#  LATIN CAPITAL LETTER N WITH CARON
    0x00c6: 0x2206,	#  INCREMENT
    0x00c7: 0x00ab,	#  LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00c8: 0x00bb,	#  RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00c9: 0x2026,	#  HORIZONTAL ELLIPSIS
    0x00ca: 0x00a0,	#  NO-BREAK SPACE
    0x00cb: 0x0148,	#  LATIN SMALL LETTER N WITH CARON
    0x00cc: 0x0150,	#  LATIN CAPITAL LETTER O WITH DOUBLE ACUTE
    0x00cd: 0x00d5,	#  LATIN CAPITAL LETTER O WITH TILDE
    0x00ce: 0x0151,	#  LATIN SMALL LETTER O WITH DOUBLE ACUTE
    0x00cf: 0x014c,	#  LATIN CAPITAL LETTER O WITH MACRON
    0x00d0: 0x2013,	#  EN DASH
    0x00d1: 0x2014,	#  EM DASH
    0x00d2: 0x201c,	#  LEFT DOUBLE QUOTATION MARK
    0x00d3: 0x201d,	#  RIGHT DOUBLE QUOTATION MARK
    0x00d4: 0x2018,	#  LEFT SINGLE QUOTATION MARK
    0x00d5: 0x2019,	#  RIGHT SINGLE QUOTATION MARK
    0x00d6: 0x00f7,	#  DIVISION SIGN
    0x00d7: 0x25ca,	#  LOZENGE
    0x00d8: 0x014d,	#  LATIN SMALL LETTER O WITH MACRON
    0x00d9: 0x0154,	#  LATIN CAPITAL LETTER R WITH ACUTE
    0x00da: 0x0155,	#  LATIN SMALL LETTER R WITH ACUTE
    0x00db: 0x0158,	#  LATIN CAPITAL LETTER R WITH CARON
    0x00dc: 0x2039,	#  SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    0x00dd: 0x203a,	#  SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    0x00de: 0x0159,	#  LATIN SMALL LETTER R WITH CARON
    0x00df: 0x0156,	#  LATIN CAPITAL LETTER R WITH CEDILLA
    0x00e0: 0x0157,	#  LATIN SMALL LETTER R WITH CEDILLA
    0x00e1: 0x0160,	#  LATIN CAPITAL LETTER S WITH CARON
    0x00e2: 0x201a,	#  SINGLE LOW-9 QUOTATION MARK
    0x00e3: 0x201e,	#  DOUBLE LOW-9 QUOTATION MARK
    0x00e4: 0x0161,	#  LATIN SMALL LETTER S WITH CARON
    0x00e5: 0x015a,	#  LATIN CAPITAL LETTER S WITH ACUTE
    0x00e6: 0x015b,	#  LATIN SMALL LETTER S WITH ACUTE
    0x00e7: 0x00c1,	#  LATIN CAPITAL LETTER A WITH ACUTE
    0x00e8: 0x0164,	#  LATIN CAPITAL LETTER T WITH CARON
    0x00e9: 0x0165,	#  LATIN SMALL LETTER T WITH CARON
    0x00ea: 0x00cd,	#  LATIN CAPITAL LETTER I WITH ACUTE
    0x00eb: 0x017d,	#  LATIN CAPITAL LETTER Z WITH CARON
    0x00ec: 0x017e,	#  LATIN SMALL LETTER Z WITH CARON
    0x00ed: 0x016a,	#  LATIN CAPITAL LETTER U WITH MACRON
    0x00ee: 0x00d3,	#  LATIN CAPITAL LETTER O WITH ACUTE
    0x00ef: 0x00d4,	#  LATIN CAPITAL LETTER O WITH CIRCUMFLEX
    0x00f0: 0x016b,	#  LATIN SMALL LETTER U WITH MACRON
    0x00f1: 0x016e,	#  LATIN CAPITAL LETTER U WITH RING ABOVE
    0x00f2: 0x00da,	#  LATIN CAPITAL LETTER U WITH ACUTE
    0x00f3: 0x016f,	#  LATIN SMALL LETTER U WITH RING ABOVE
    0x00f4: 0x0170,	#  LATIN CAPITAL LETTER U WITH DOUBLE ACUTE
    0x00f5: 0x0171,	#  LATIN SMALL LETTER U WITH DOUBLE ACUTE
    0x00f6: 0x0172,	#  LATIN CAPITAL LETTER U WITH OGONEK
    0x00f7: 0x0173,	#  LATIN SMALL LETTER U WITH OGONEK
    0x00f8: 0x00dd,	#  LATIN CAPITAL LETTER Y WITH ACUTE
    0x00f9: 0x00fd,	#  LATIN SMALL LETTER Y WITH ACUTE
    0x00fa: 0x0137,	#  LATIN SMALL LETTER K WITH CEDILLA
    0x00fb: 0x017b,	#  LATIN CAPITAL LETTER Z WITH DOT ABOVE
    0x00fc: 0x0141,	#  LATIN CAPITAL LETTER L WITH STROKE
    0x00fd: 0x017c,	#  LATIN SMALL LETTER Z WITH DOT ABOVE
    0x00fe: 0x0122,	#  LATIN CAPITAL LETTER G WITH CEDILLA
    0x00ff: 0x02c7,	#  CARON
})

### Decoding Table

decoding_table = (
    u'\x00'	#  0x0000 -> CONTROL CHARACTER
    u'\x01'	#  0x0001 -> CONTROL CHARACTER
    u'\x02'	#  0x0002 -> CONTROL CHARACTER
    u'\x03'	#  0x0003 -> CONTROL CHARACTER
    u'\x04'	#  0x0004 -> CONTROL CHARACTER
    u'\x05'	#  0x0005 -> CONTROL CHARACTER
    u'\x06'	#  0x0006 -> CONTROL CHARACTER
    u'\x07'	#  0x0007 -> CONTROL CHARACTER
    u'\x08'	#  0x0008 -> CONTROL CHARACTER
    u'\t'	#  0x0009 -> CONTROL CHARACTER
    u'\n'	#  0x000a -> CONTROL CHARACTER
    u'\x0b'	#  0x000b -> CONTROL CHARACTER
    u'\x0c'	#  0x000c -> CONTROL CHARACTER
    u'\r'	#  0x000d -> CONTROL CHARACTER
    u'\x0e'	#  0x000e -> CONTROL CHARACTER
    u'\x0f'	#  0x000f -> CONTROL CHARACTER
    u'\x10'	#  0x0010 -> CONTROL CHARACTER
    u'\x11'	#  0x0011 -> CONTROL CHARACTER
    u'\x12'	#  0x0012 -> CONTROL CHARACTER
    u'\x13'	#  0x0013 -> CONTROL CHARACTER
    u'\x14'	#  0x0014 -> CONTROL CHARACTER
    u'\x15'	#  0x0015 -> CONTROL CHARACTER
    u'\x16'	#  0x0016 -> CONTROL CHARACTER
    u'\x17'	#  0x0017 -> CONTROL CHARACTER
    u'\x18'	#  0x0018 -> CONTROL CHARACTER
    u'\x19'	#  0x0019 -> CONTROL CHARACTER
    u'\x1a'	#  0x001a -> CONTROL CHARACTER
    u'\x1b'	#  0x001b -> CONTROL CHARACTER
    u'\x1c'	#  0x001c -> CONTROL CHARACTER
    u'\x1d'	#  0x001d -> CONTROL CHARACTER
    u'\x1e'	#  0x001e -> CONTROL CHARACTER
    u'\x1f'	#  0x001f -> CONTROL CHARACTER
    u' '	#  0x0020 -> SPACE
    u'!'	#  0x0021 -> EXCLAMATION MARK
    u'"'	#  0x0022 -> QUOTATION MARK
    u'#'	#  0x0023 -> NUMBER SIGN
    u'$'	#  0x0024 -> DOLLAR SIGN
    u'%'	#  0x0025 -> PERCENT SIGN
    u'&'	#  0x0026 -> AMPERSAND
    u"'"	#  0x0027 -> APOSTROPHE
    u'('	#  0x0028 -> LEFT PARENTHESIS
    u')'	#  0x0029 -> RIGHT PARENTHESIS
    u'*'	#  0x002a -> ASTERISK
    u'+'	#  0x002b -> PLUS SIGN
    u','	#  0x002c -> COMMA
    u'-'	#  0x002d -> HYPHEN-MINUS
    u'.'	#  0x002e -> FULL STOP
    u'/'	#  0x002f -> SOLIDUS
    u'0'	#  0x0030 -> DIGIT ZERO
    u'1'	#  0x0031 -> DIGIT ONE
    u'2'	#  0x0032 -> DIGIT TWO
    u'3'	#  0x0033 -> DIGIT THREE
    u'4'	#  0x0034 -> DIGIT FOUR
    u'5'	#  0x0035 -> DIGIT FIVE
    u'6'	#  0x0036 -> DIGIT SIX
    u'7'	#  0x0037 -> DIGIT SEVEN
    u'8'	#  0x0038 -> DIGIT EIGHT
    u'9'	#  0x0039 -> DIGIT NINE
    u':'	#  0x003a -> COLON
    u';'	#  0x003b -> SEMICOLON
    u'<'	#  0x003c -> LESS-THAN SIGN
    u'='	#  0x003d -> EQUALS SIGN
    u'>'	#  0x003e -> GREATER-THAN SIGN
    u'?'	#  0x003f -> QUESTION MARK
    u'@'	#  0x0040 -> COMMERCIAL AT
    u'A'	#  0x0041 -> LATIN CAPITAL LETTER A
    u'B'	#  0x0042 -> LATIN CAPITAL LETTER B
    u'C'	#  0x0043 -> LATIN CAPITAL LETTER C
    u'D'	#  0x0044 -> LATIN CAPITAL LETTER D
    u'E'	#  0x0045 -> LATIN CAPITAL LETTER E
    u'F'	#  0x0046 -> LATIN CAPITAL LETTER F
    u'G'	#  0x0047 -> LATIN CAPITAL LETTER G
    u'H'	#  0x0048 -> LATIN CAPITAL LETTER H
    u'I'	#  0x0049 -> LATIN CAPITAL LETTER I
    u'J'	#  0x004a -> LATIN CAPITAL LETTER J
    u'K'	#  0x004b -> LATIN CAPITAL LETTER K
    u'L'	#  0x004c -> LATIN CAPITAL LETTER L
    u'M'	#  0x004d -> LATIN CAPITAL LETTER M
    u'N'	#  0x004e -> LATIN CAPITAL LETTER N
    u'O'	#  0x004f -> LATIN CAPITAL LETTER O
    u'P'	#  0x0050 -> LATIN CAPITAL LETTER P
    u'Q'	#  0x0051 -> LATIN CAPITAL LETTER Q
    u'R'	#  0x0052 -> LATIN CAPITAL LETTER R
    u'S'	#  0x0053 -> LATIN CAPITAL LETTER S
    u'T'	#  0x0054 -> LATIN CAPITAL LETTER T
    u'U'	#  0x0055 -> LATIN CAPITAL LETTER U
    u'V'	#  0x0056 -> LATIN CAPITAL LETTER V
    u'W'	#  0x0057 -> LATIN CAPITAL LETTER W
    u'X'	#  0x0058 -> LATIN CAPITAL LETTER X
    u'Y'	#  0x0059 -> LATIN CAPITAL LETTER Y
    u'Z'	#  0x005a -> LATIN CAPITAL LETTER Z
    u'['	#  0x005b -> LEFT SQUARE BRACKET
    u'\\'	#  0x005c -> REVERSE SOLIDUS
    u']'	#  0x005d -> RIGHT SQUARE BRACKET
    u'^'	#  0x005e -> CIRCUMFLEX ACCENT
    u'_'	#  0x005f -> LOW LINE
    u'`'	#  0x0060 -> GRAVE ACCENT
    u'a'	#  0x0061 -> LATIN SMALL LETTER A
    u'b'	#  0x0062 -> LATIN SMALL LETTER B
    u'c'	#  0x0063 -> LATIN SMALL LETTER C
    u'd'	#  0x0064 -> LATIN SMALL LETTER D
    u'e'	#  0x0065 -> LATIN SMALL LETTER E
    u'f'	#  0x0066 -> LATIN SMALL LETTER F
    u'g'	#  0x0067 -> LATIN SMALL LETTER G
    u'h'	#  0x0068 -> LATIN SMALL LETTER H
    u'i'	#  0x0069 -> LATIN SMALL LETTER I
    u'j'	#  0x006a -> LATIN SMALL LETTER J
    u'k'	#  0x006b -> LATIN SMALL LETTER K
    u'l'	#  0x006c -> LATIN SMALL LETTER L
    u'm'	#  0x006d -> LATIN SMALL LETTER M
    u'n'	#  0x006e -> LATIN SMALL LETTER N
    u'o'	#  0x006f -> LATIN SMALL LETTER O
    u'p'	#  0x0070 -> LATIN SMALL LETTER P
    u'q'	#  0x0071 -> LATIN SMALL LETTER Q
    u'r'	#  0x0072 -> LATIN SMALL LETTER R
    u's'	#  0x0073 -> LATIN SMALL LETTER S
    u't'	#  0x0074 -> LATIN SMALL LETTER T
    u'u'	#  0x0075 -> LATIN SMALL LETTER U
    u'v'	#  0x0076 -> LATIN SMALL LETTER V
    u'w'	#  0x0077 -> LATIN SMALL LETTER W
    u'x'	#  0x0078 -> LATIN SMALL LETTER X
    u'y'	#  0x0079 -> LATIN SMALL LETTER Y
    u'z'	#  0x007a -> LATIN SMALL LETTER Z
    u'{'	#  0x007b -> LEFT CURLY BRACKET
    u'|'	#  0x007c -> VERTICAL LINE
    u'}'	#  0x007d -> RIGHT CURLY BRACKET
    u'~'	#  0x007e -> TILDE
    u'\x7f'	#  0x007f -> CONTROL CHARACTER
    u'\xc4'	#  0x0080 -> LATIN CAPITAL LETTER A WITH DIAERESIS
    u'\u0100'	#  0x0081 -> LATIN CAPITAL LETTER A WITH MACRON
    u'\u0101'	#  0x0082 -> LATIN SMALL LETTER A WITH MACRON
    u'\xc9'	#  0x0083 -> LATIN CAPITAL LETTER E WITH ACUTE
    u'\u0104'	#  0x0084 -> LATIN CAPITAL LETTER A WITH OGONEK
    u'\xd6'	#  0x0085 -> LATIN CAPITAL LETTER O WITH DIAERESIS
    u'\xdc'	#  0x0086 -> LATIN CAPITAL LETTER U WITH DIAERESIS
    u'\xe1'	#  0x0087 -> LATIN SMALL LETTER A WITH ACUTE
    u'\u0105'	#  0x0088 -> LATIN SMALL LETTER A WITH OGONEK
    u'\u010c'	#  0x0089 -> LATIN CAPITAL LETTER C WITH CARON
    u'\xe4'	#  0x008a -> LATIN SMALL LETTER A WITH DIAERESIS
    u'\u010d'	#  0x008b -> LATIN SMALL LETTER C WITH CARON
    u'\u0106'	#  0x008c -> LATIN CAPITAL LETTER C WITH ACUTE
    u'\u0107'	#  0x008d -> LATIN SMALL LETTER C WITH ACUTE
    u'\xe9'	#  0x008e -> LATIN SMALL LETTER E WITH ACUTE
    u'\u0179'	#  0x008f -> LATIN CAPITAL LETTER Z WITH ACUTE
    u'\u017a'	#  0x0090 -> LATIN SMALL LETTER Z WITH ACUTE
    u'\u010e'	#  0x0091 -> LATIN CAPITAL LETTER D WITH CARON
    u'\xed'	#  0x0092 -> LATIN SMALL LETTER I WITH ACUTE
    u'\u010f'	#  0x0093 -> LATIN SMALL LETTER D WITH CARON
    u'\u0112'	#  0x0094 -> LATIN CAPITAL LETTER E WITH MACRON
    u'\u0113'	#  0x0095 -> LATIN SMALL LETTER E WITH MACRON
    u'\u0116'	#  0x0096 -> LATIN CAPITAL LETTER E WITH DOT ABOVE
    u'\xf3'	#  0x0097 -> LATIN SMALL LETTER O WITH ACUTE
    u'\u0117'	#  0x0098 -> LATIN SMALL LETTER E WITH DOT ABOVE
    u'\xf4'	#  0x0099 -> LATIN SMALL LETTER O WITH CIRCUMFLEX
    u'\xf6'	#  0x009a -> LATIN SMALL LETTER O WITH DIAERESIS
    u'\xf5'	#  0x009b -> LATIN SMALL LETTER O WITH TILDE
    u'\xfa'	#  0x009c -> LATIN SMALL LETTER U WITH ACUTE
    u'\u011a'	#  0x009d -> LATIN CAPITAL LETTER E WITH CARON
    u'\u011b'	#  0x009e -> LATIN SMALL LETTER E WITH CARON
    u'\xfc'	#  0x009f -> LATIN SMALL LETTER U WITH DIAERESIS
    u'\u2020'	#  0x00a0 -> DAGGER
    u'\xb0'	#  0x00a1 -> DEGREE SIGN
    u'\u0118'	#  0x00a2 -> LATIN CAPITAL LETTER E WITH OGONEK
    u'\xa3'	#  0x00a3 -> POUND SIGN
    u'\xa7'	#  0x00a4 -> SECTION SIGN
    u'\u2022'	#  0x00a5 -> BULLET
    u'\xb6'	#  0x00a6 -> PILCROW SIGN
    u'\xdf'	#  0x00a7 -> LATIN SMALL LETTER SHARP S
    u'\xae'	#  0x00a8 -> REGISTERED SIGN
    u'\xa9'	#  0x00a9 -> COPYRIGHT SIGN
    u'\u2122'	#  0x00aa -> TRADE MARK SIGN
    u'\u0119'	#  0x00ab -> LATIN SMALL LETTER E WITH OGONEK
    u'\xa8'	#  0x00ac -> DIAERESIS
    u'\u2260'	#  0x00ad -> NOT EQUAL TO
    u'\u0123'	#  0x00ae -> LATIN SMALL LETTER G WITH CEDILLA
    u'\u012e'	#  0x00af -> LATIN CAPITAL LETTER I WITH OGONEK
    u'\u012f'	#  0x00b0 -> LATIN SMALL LETTER I WITH OGONEK
    u'\u012a'	#  0x00b1 -> LATIN CAPITAL LETTER I WITH MACRON
    u'\u2264'	#  0x00b2 -> LESS-THAN OR EQUAL TO
    u'\u2265'	#  0x00b3 -> GREATER-THAN OR EQUAL TO
    u'\u012b'	#  0x00b4 -> LATIN SMALL LETTER I WITH MACRON
    u'\u0136'	#  0x00b5 -> LATIN CAPITAL LETTER K WITH CEDILLA
    u'\u2202'	#  0x00b6 -> PARTIAL DIFFERENTIAL
    u'\u2211'	#  0x00b7 -> N-ARY SUMMATION
    u'\u0142'	#  0x00b8 -> LATIN SMALL LETTER L WITH STROKE
    u'\u013b'	#  0x00b9 -> LATIN CAPITAL LETTER L WITH CEDILLA
    u'\u013c'	#  0x00ba -> LATIN SMALL LETTER L WITH CEDILLA
    u'\u013d'	#  0x00bb -> LATIN CAPITAL LETTER L WITH CARON
    u'\u013e'	#  0x00bc -> LATIN SMALL LETTER L WITH CARON
    u'\u0139'	#  0x00bd -> LATIN CAPITAL LETTER L WITH ACUTE
    u'\u013a'	#  0x00be -> LATIN SMALL LETTER L WITH ACUTE
    u'\u0145'	#  0x00bf -> LATIN CAPITAL LETTER N WITH CEDILLA
    u'\u0146'	#  0x00c0 -> LATIN SMALL LETTER N WITH CEDILLA
    u'\u0143'	#  0x00c1 -> LATIN CAPITAL LETTER N WITH ACUTE
    u'\xac'	#  0x00c2 -> NOT SIGN
    u'\u221a'	#  0x00c3 -> SQUARE ROOT
    u'\u0144'	#  0x00c4 -> LATIN SMALL LETTER N WITH ACUTE
    u'\u0147'	#  0x00c5 -> LATIN CAPITAL LETTER N WITH CARON
    u'\u2206'	#  0x00c6 -> INCREMENT
    u'\xab'	#  0x00c7 -> LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    u'\xbb'	#  0x00c8 -> RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    u'\u2026'	#  0x00c9 -> HORIZONTAL ELLIPSIS
    u'\xa0'	#  0x00ca -> NO-BREAK SPACE
    u'\u0148'	#  0x00cb -> LATIN SMALL LETTER N WITH CARON
    u'\u0150'	#  0x00cc -> LATIN CAPITAL LETTER O WITH DOUBLE ACUTE
    u'\xd5'	#  0x00cd -> LATIN CAPITAL LETTER O WITH TILDE
    u'\u0151'	#  0x00ce -> LATIN SMALL LETTER O WITH DOUBLE ACUTE
    u'\u014c'	#  0x00cf -> LATIN CAPITAL LETTER O WITH MACRON
    u'\u2013'	#  0x00d0 -> EN DASH
    u'\u2014'	#  0x00d1 -> EM DASH
    u'\u201c'	#  0x00d2 -> LEFT DOUBLE QUOTATION MARK
    u'\u201d'	#  0x00d3 -> RIGHT DOUBLE QUOTATION MARK
    u'\u2018'	#  0x00d4 -> LEFT SINGLE QUOTATION MARK
    u'\u2019'	#  0x00d5 -> RIGHT SINGLE QUOTATION MARK
    u'\xf7'	#  0x00d6 -> DIVISION SIGN
    u'\u25ca'	#  0x00d7 -> LOZENGE
    u'\u014d'	#  0x00d8 -> LATIN SMALL LETTER O WITH MACRON
    u'\u0154'	#  0x00d9 -> LATIN CAPITAL LETTER R WITH ACUTE
    u'\u0155'	#  0x00da -> LATIN SMALL LETTER R WITH ACUTE
    u'\u0158'	#  0x00db -> LATIN CAPITAL LETTER R WITH CARON
    u'\u2039'	#  0x00dc -> SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    u'\u203a'	#  0x00dd -> SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    u'\u0159'	#  0x00de -> LATIN SMALL LETTER R WITH CARON
    u'\u0156'	#  0x00df -> LATIN CAPITAL LETTER R WITH CEDILLA
    u'\u0157'	#  0x00e0 -> LATIN SMALL LETTER R WITH CEDILLA
    u'\u0160'	#  0x00e1 -> LATIN CAPITAL LETTER S WITH CARON
    u'\u201a'	#  0x00e2 -> SINGLE LOW-9 QUOTATION MARK
    u'\u201e'	#  0x00e3 -> DOUBLE LOW-9 QUOTATION MARK
    u'\u0161'	#  0x00e4 -> LATIN SMALL LETTER S WITH CARON
    u'\u015a'	#  0x00e5 -> LATIN CAPITAL LETTER S WITH ACUTE
    u'\u015b'	#  0x00e6 -> LATIN SMALL LETTER S WITH ACUTE
    u'\xc1'	#  0x00e7 -> LATIN CAPITAL LETTER A WITH ACUTE
    u'\u0164'	#  0x00e8 -> LATIN CAPITAL LETTER T WITH CARON
    u'\u0165'	#  0x00e9 -> LATIN SMALL LETTER T WITH CARON
    u'\xcd'	#  0x00ea -> LATIN CAPITAL LETTER I WITH ACUTE
    u'\u017d'	#  0x00eb -> LATIN CAPITAL LETTER Z WITH CARON
    u'\u017e'	#  0x00ec -> LATIN SMALL LETTER Z WITH CARON
    u'\u016a'	#  0x00ed -> LATIN CAPITAL LETTER U WITH MACRON
    u'\xd3'	#  0x00ee -> LATIN CAPITAL LETTER O WITH ACUTE
    u'\xd4'	#  0x00ef -> LATIN CAPITAL LETTER O WITH CIRCUMFLEX
    u'\u016b'	#  0x00f0 -> LATIN SMALL LETTER U WITH MACRON
    u'\u016e'	#  0x00f1 -> LATIN CAPITAL LETTER U WITH RING ABOVE
    u'\xda'	#  0x00f2 -> LATIN CAPITAL LETTER U WITH ACUTE
    u'\u016f'	#  0x00f3 -> LATIN SMALL LETTER U WITH RING ABOVE
    u'\u0170'	#  0x00f4 -> LATIN CAPITAL LETTER U WITH DOUBLE ACUTE
    u'\u0171'	#  0x00f5 -> LATIN SMALL LETTER U WITH DOUBLE ACUTE
    u'\u0172'	#  0x00f6 -> LATIN CAPITAL LETTER U WITH OGONEK
    u'\u0173'	#  0x00f7 -> LATIN SMALL LETTER U WITH OGONEK
    u'\xdd'	#  0x00f8 -> LATIN CAPITAL LETTER Y WITH ACUTE
    u'\xfd'	#  0x00f9 -> LATIN SMALL LETTER Y WITH ACUTE
    u'\u0137'	#  0x00fa -> LATIN SMALL LETTER K WITH CEDILLA
    u'\u017b'	#  0x00fb -> LATIN CAPITAL LETTER Z WITH DOT ABOVE
    u'\u0141'	#  0x00fc -> LATIN CAPITAL LETTER L WITH STROKE
    u'\u017c'	#  0x00fd -> LATIN SMALL LETTER Z WITH DOT ABOVE
    u'\u0122'	#  0x00fe -> LATIN CAPITAL LETTER G WITH CEDILLA
    u'\u02c7'	#  0x00ff -> CARON
)

### Encoding Map

encoding_map = {
    0x0000: 0x0000,	#  CONTROL CHARACTER
    0x0001: 0x0001,	#  CONTROL CHARACTER
    0x0002: 0x0002,	#  CONTROL CHARACTER
    0x0003: 0x0003,	#  CONTROL CHARACTER
    0x0004: 0x0004,	#  CONTROL CHARACTER
    0x0005: 0x0005,	#  CONTROL CHARACTER
    0x0006: 0x0006,	#  CONTROL CHARACTER
    0x0007: 0x0007,	#  CONTROL CHARACTER
    0x0008: 0x0008,	#  CONTROL CHARACTER
    0x0009: 0x0009,	#  CONTROL CHARACTER
    0x000a: 0x000a,	#  CONTROL CHARACTER
    0x000b: 0x000b,	#  CONTROL CHARACTER
    0x000c: 0x000c,	#  CONTROL CHARACTER
    0x000d: 0x000d,	#  CONTROL CHARACTER
    0x000e: 0x000e,	#  CONTROL CHARACTER
    0x000f: 0x000f,	#  CONTROL CHARACTER
    0x0010: 0x0010,	#  CONTROL CHARACTER
    0x0011: 0x0011,	#  CONTROL CHARACTER
    0x0012: 0x0012,	#  CONTROL CHARACTER
    0x0013: 0x0013,	#  CONTROL CHARACTER
    0x0014: 0x0014,	#  CONTROL CHARACTER
    0x0015: 0x0015,	#  CONTROL CHARACTER
    0x0016: 0x0016,	#  CONTROL CHARACTER
    0x0017: 0x0017,	#  CONTROL CHARACTER
    0x0018: 0x0018,	#  CONTROL CHARACTER
    0x0019: 0x0019,	#  CONTROL CHARACTER
    0x001a: 0x001a,	#  CONTROL CHARACTER
    0x001b: 0x001b,	#  CONTROL CHARACTER
    0x001c: 0x001c,	#  CONTROL CHARACTER
    0x001d: 0x001d,	#  CONTROL CHARACTER
    0x001e: 0x001e,	#  CONTROL CHARACTER
    0x001f: 0x001f,	#  CONTROL CHARACTER
    0x0020: 0x0020,	#  SPACE
    0x0021: 0x0021,	#  EXCLAMATION MARK
    0x0022: 0x0022,	#  QUOTATION MARK
    0x0023: 0x0023,	#  NUMBER SIGN
    0x0024: 0x0024,	#  DOLLAR SIGN
    0x0025: 0x0025,	#  PERCENT SIGN
    0x0026: 0x0026,	#  AMPERSAND
    0x0027: 0x0027,	#  APOSTROPHE
    0x0028: 0x0028,	#  LEFT PARENTHESIS
    0x0029: 0x0029,	#  RIGHT PARENTHESIS
    0x002a: 0x002a,	#  ASTERISK
    0x002b: 0x002b,	#  PLUS SIGN
    0x002c: 0x002c,	#  COMMA
    0x002d: 0x002d,	#  HYPHEN-MINUS
    0x002e: 0x002e,	#  FULL STOP
    0x002f: 0x002f,	#  SOLIDUS
    0x0030: 0x0030,	#  DIGIT ZERO
    0x0031: 0x0031,	#  DIGIT ONE
    0x0032: 0x0032,	#  DIGIT TWO
    0x0033: 0x0033,	#  DIGIT THREE
    0x0034: 0x0034,	#  DIGIT FOUR
    0x0035: 0x0035,	#  DIGIT FIVE
    0x0036: 0x0036,	#  DIGIT SIX
    0x0037: 0x0037,	#  DIGIT SEVEN
    0x0038: 0x0038,	#  DIGIT EIGHT
    0x0039: 0x0039,	#  DIGIT NINE
    0x003a: 0x003a,	#  COLON
    0x003b: 0x003b,	#  SEMICOLON
    0x003c: 0x003c,	#  LESS-THAN SIGN
    0x003d: 0x003d,	#  EQUALS SIGN
    0x003e: 0x003e,	#  GREATER-THAN SIGN
    0x003f: 0x003f,	#  QUESTION MARK
    0x0040: 0x0040,	#  COMMERCIAL AT
    0x0041: 0x0041,	#  LATIN CAPITAL LETTER A
    0x0042: 0x0042,	#  LATIN CAPITAL LETTER B
    0x0043: 0x0043,	#  LATIN CAPITAL LETTER C
    0x0044: 0x0044,	#  LATIN CAPITAL LETTER D
    0x0045: 0x0045,	#  LATIN CAPITAL LETTER E
    0x0046: 0x0046,	#  LATIN CAPITAL LETTER F
    0x0047: 0x0047,	#  LATIN CAPITAL LETTER G
    0x0048: 0x0048,	#  LATIN CAPITAL LETTER H
    0x0049: 0x0049,	#  LATIN CAPITAL LETTER I
    0x004a: 0x004a,	#  LATIN CAPITAL LETTER J
    0x004b: 0x004b,	#  LATIN CAPITAL LETTER K
    0x004c: 0x004c,	#  LATIN CAPITAL LETTER L
    0x004d: 0x004d,	#  LATIN CAPITAL LETTER M
    0x004e: 0x004e,	#  LATIN CAPITAL LETTER N
    0x004f: 0x004f,	#  LATIN CAPITAL LETTER O
    0x0050: 0x0050,	#  LATIN CAPITAL LETTER P
    0x0051: 0x0051,	#  LATIN CAPITAL LETTER Q
    0x0052: 0x0052,	#  LATIN CAPITAL LETTER R
    0x0053: 0x0053,	#  LATIN CAPITAL LETTER S
    0x0054: 0x0054,	#  LATIN CAPITAL LETTER T
    0x0055: 0x0055,	#  LATIN CAPITAL LETTER U
    0x0056: 0x0056,	#  LATIN CAPITAL LETTER V
    0x0057: 0x0057,	#  LATIN CAPITAL LETTER W
    0x0058: 0x0058,	#  LATIN CAPITAL LETTER X
    0x0059: 0x0059,	#  LATIN CAPITAL LETTER Y
    0x005a: 0x005a,	#  LATIN CAPITAL LETTER Z
    0x005b: 0x005b,	#  LEFT SQUARE BRACKET
    0x005c: 0x005c,	#  REVERSE SOLIDUS
    0x005d: 0x005d,	#  RIGHT SQUARE BRACKET
    0x005e: 0x005e,	#  CIRCUMFLEX ACCENT
    0x005f: 0x005f,	#  LOW LINE
    0x0060: 0x0060,	#  GRAVE ACCENT
    0x0061: 0x0061,	#  LATIN SMALL LETTER A
    0x0062: 0x0062,	#  LATIN SMALL LETTER B
    0x0063: 0x0063,	#  LATIN SMALL LETTER C
    0x0064: 0x0064,	#  LATIN SMALL LETTER D
    0x0065: 0x0065,	#  LATIN SMALL LETTER E
    0x0066: 0x0066,	#  LATIN SMALL LETTER F
    0x0067: 0x0067,	#  LATIN SMALL LETTER G
    0x0068: 0x0068,	#  LATIN SMALL LETTER H
    0x0069: 0x0069,	#  LATIN SMALL LETTER I
    0x006a: 0x006a,	#  LATIN SMALL LETTER J
    0x006b: 0x006b,	#  LATIN SMALL LETTER K
    0x006c: 0x006c,	#  LATIN SMALL LETTER L
    0x006d: 0x006d,	#  LATIN SMALL LETTER M
    0x006e: 0x006e,	#  LATIN SMALL LETTER N
    0x006f: 0x006f,	#  LATIN SMALL LETTER O
    0x0070: 0x0070,	#  LATIN SMALL LETTER P
    0x0071: 0x0071,	#  LATIN SMALL LETTER Q
    0x0072: 0x0072,	#  LATIN SMALL LETTER R
    0x0073: 0x0073,	#  LATIN SMALL LETTER S
    0x0074: 0x0074,	#  LATIN SMALL LETTER T
    0x0075: 0x0075,	#  LATIN SMALL LETTER U
    0x0076: 0x0076,	#  LATIN SMALL LETTER V
    0x0077: 0x0077,	#  LATIN SMALL LETTER W
    0x0078: 0x0078,	#  LATIN SMALL LETTER X
    0x0079: 0x0079,	#  LATIN SMALL LETTER Y
    0x007a: 0x007a,	#  LATIN SMALL LETTER Z
    0x007b: 0x007b,	#  LEFT CURLY BRACKET
    0x007c: 0x007c,	#  VERTICAL LINE
    0x007d: 0x007d,	#  RIGHT CURLY BRACKET
    0x007e: 0x007e,	#  TILDE
    0x007f: 0x007f,	#  CONTROL CHARACTER
    0x00a0: 0x00ca,	#  NO-BREAK SPACE
    0x00a3: 0x00a3,	#  POUND SIGN
    0x00a7: 0x00a4,	#  SECTION SIGN
    0x00a8: 0x00ac,	#  DIAERESIS
    0x00a9: 0x00a9,	#  COPYRIGHT SIGN
    0x00ab: 0x00c7,	#  LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00ac: 0x00c2,	#  NOT SIGN
    0x00ae: 0x00a8,	#  REGISTERED SIGN
    0x00b0: 0x00a1,	#  DEGREE SIGN
    0x00b6: 0x00a6,	#  PILCROW SIGN
    0x00bb: 0x00c8,	#  RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00c1: 0x00e7,	#  LATIN CAPITAL LETTER A WITH ACUTE
    0x00c4: 0x0080,	#  LATIN CAPITAL LETTER A WITH DIAERESIS
    0x00c9: 0x0083,	#  LATIN CAPITAL LETTER E WITH ACUTE
    0x00cd: 0x00ea,	#  LATIN CAPITAL LETTER I WITH ACUTE
    0x00d3: 0x00ee,	#  LATIN CAPITAL LETTER O WITH ACUTE
    0x00d4: 0x00ef,	#  LATIN CAPITAL LETTER O WITH CIRCUMFLEX
    0x00d5: 0x00cd,	#  LATIN CAPITAL LETTER O WITH TILDE
    0x00d6: 0x0085,	#  LATIN CAPITAL LETTER O WITH DIAERESIS
    0x00da: 0x00f2,	#  LATIN CAPITAL LETTER U WITH ACUTE
    0x00dc: 0x0086,	#  LATIN CAPITAL LETTER U WITH DIAERESIS
    0x00dd: 0x00f8,	#  LATIN CAPITAL LETTER Y WITH ACUTE
    0x00df: 0x00a7,	#  LATIN SMALL LETTER SHARP S
    0x00e1: 0x0087,	#  LATIN SMALL LETTER A WITH ACUTE
    0x00e4: 0x008a,	#  LATIN SMALL LETTER A WITH DIAERESIS
    0x00e9: 0x008e,	#  LATIN SMALL LETTER E WITH ACUTE
    0x00ed: 0x0092,	#  LATIN SMALL LETTER I WITH ACUTE
    0x00f3: 0x0097,	#  LATIN SMALL LETTER O WITH ACUTE
    0x00f4: 0x0099,	#  LATIN SMALL LETTER O WITH CIRCUMFLEX
    0x00f5: 0x009b,	#  LATIN SMALL LETTER O WITH TILDE
    0x00f6: 0x009a,	#  LATIN SMALL LETTER O WITH DIAERESIS
    0x00f7: 0x00d6,	#  DIVISION SIGN
    0x00fa: 0x009c,	#  LATIN SMALL LETTER U WITH ACUTE
    0x00fc: 0x009f,	#  LATIN SMALL LETTER U WITH DIAERESIS
    0x00fd: 0x00f9,	#  LATIN SMALL LETTER Y WITH ACUTE
    0x0100: 0x0081,	#  LATIN CAPITAL LETTER A WITH MACRON
    0x0101: 0x0082,	#  LATIN SMALL LETTER A WITH MACRON
    0x0104: 0x0084,	#  LATIN CAPITAL LETTER A WITH OGONEK
    0x0105: 0x0088,	#  LATIN SMALL LETTER A WITH OGONEK
    0x0106: 0x008c,	#  LATIN CAPITAL LETTER C WITH ACUTE
    0x0107: 0x008d,	#  LATIN SMALL LETTER C WITH ACUTE
    0x010c: 0x0089,	#  LATIN CAPITAL LETTER C WITH CARON
    0x010d: 0x008b,	#  LATIN SMALL LETTER C WITH CARON
    0x010e: 0x0091,	#  LATIN CAPITAL LETTER D WITH CARON
    0x010f: 0x0093,	#  LATIN SMALL LETTER D WITH CARON
    0x0112: 0x0094,	#  LATIN CAPITAL LETTER E WITH MACRON
    0x0113: 0x0095,	#  LATIN SMALL LETTER E WITH MACRON
    0x0116: 0x0096,	#  LATIN CAPITAL LETTER E WITH DOT ABOVE
    0x0117: 0x0098,	#  LATIN SMALL LETTER E WITH DOT ABOVE
    0x0118: 0x00a2,	#  LATIN CAPITAL LETTER E WITH OGONEK
    0x0119: 0x00ab,	#  LATIN SMALL LETTER E WITH OGONEK
    0x011a: 0x009d,	#  LATIN CAPITAL LETTER E WITH CARON
    0x011b: 0x009e,	#  LATIN SMALL LETTER E WITH CARON
    0x0122: 0x00fe,	#  LATIN CAPITAL LETTER G WITH CEDILLA
    0x0123: 0x00ae,	#  LATIN SMALL LETTER G WITH CEDILLA
    0x012a: 0x00b1,	#  LATIN CAPITAL LETTER I WITH MACRON
    0x012b: 0x00b4,	#  LATIN SMALL LETTER I WITH MACRON
    0x012e: 0x00af,	#  LATIN CAPITAL LETTER I WITH OGONEK
    0x012f: 0x00b0,	#  LATIN SMALL LETTER I WITH OGONEK
    0x0136: 0x00b5,	#  LATIN CAPITAL LETTER K WITH CEDILLA
    0x0137: 0x00fa,	#  LATIN SMALL LETTER K WITH CEDILLA
    0x0139: 0x00bd,	#  LATIN CAPITAL LETTER L WITH ACUTE
    0x013a: 0x00be,	#  LATIN SMALL LETTER L WITH ACUTE
    0x013b: 0x00b9,	#  LATIN CAPITAL LETTER L WITH CEDILLA
    0x013c: 0x00ba,	#  LATIN SMALL LETTER L WITH CEDILLA
    0x013d: 0x00bb,	#  LATIN CAPITAL LETTER L WITH CARON
    0x013e: 0x00bc,	#  LATIN SMALL LETTER L WITH CARON
    0x0141: 0x00fc,	#  LATIN CAPITAL LETTER L WITH STROKE
    0x0142: 0x00b8,	#  LATIN SMALL LETTER L WITH STROKE
    0x0143: 0x00c1,	#  LATIN CAPITAL LETTER N WITH ACUTE
    0x0144: 0x00c4,	#  LATIN SMALL LETTER N WITH ACUTE
    0x0145: 0x00bf,	#  LATIN CAPITAL LETTER N WITH CEDILLA
    0x0146: 0x00c0,	#  LATIN SMALL LETTER N WITH CEDILLA
    0x0147: 0x00c5,	#  LATIN CAPITAL LETTER N WITH CARON
    0x0148: 0x00cb,	#  LATIN SMALL LETTER N WITH CARON
    0x014c: 0x00cf,	#  LATIN CAPITAL LETTER O WITH MACRON
    0x014d: 0x00d8,	#  LATIN SMALL LETTER O WITH MACRON
    0x0150: 0x00cc,	#  LATIN CAPITAL LETTER O WITH DOUBLE ACUTE
    0x0151: 0x00ce,	#  LATIN SMALL LETTER O WITH DOUBLE ACUTE
    0x0154: 0x00d9,	#  LATIN CAPITAL LETTER R WITH ACUTE
    0x0155: 0x00da,	#  LATIN SMALL LETTER R WITH ACUTE
    0x0156: 0x00df,	#  LATIN CAPITAL LETTER R WITH CEDILLA
    0x0157: 0x00e0,	#  LATIN SMALL LETTER R WITH CEDILLA
    0x0158: 0x00db,	#  LATIN CAPITAL LETTER R WITH CARON
    0x0159: 0x00de,	#  LATIN SMALL LETTER R WITH CARON
    0x015a: 0x00e5,	#  LATIN CAPITAL LETTER S WITH ACUTE
    0x015b: 0x00e6,	#  LATIN SMALL LETTER S WITH ACUTE
    0x0160: 0x00e1,	#  LATIN CAPITAL LETTER S WITH CARON
    0x0161: 0x00e4,	#  LATIN SMALL LETTER S WITH CARON
    0x0164: 0x00e8,	#  LATIN CAPITAL LETTER T WITH CARON
    0x0165: 0x00e9,	#  LATIN SMALL LETTER T WITH CARON
    0x016a: 0x00ed,	#  LATIN CAPITAL LETTER U WITH MACRON
    0x016b: 0x00f0,	#  LATIN SMALL LETTER U WITH MACRON
    0x016e: 0x00f1,	#  LATIN CAPITAL LETTER U WITH RING ABOVE
    0x016f: 0x00f3,	#  LATIN SMALL LETTER U WITH RING ABOVE
    0x0170: 0x00f4,	#  LATIN CAPITAL LETTER U WITH DOUBLE ACUTE
    0x0171: 0x00f5,	#  LATIN SMALL LETTER U WITH DOUBLE ACUTE
    0x0172: 0x00f6,	#  LATIN CAPITAL LETTER U WITH OGONEK
    0x0173: 0x00f7,	#  LATIN SMALL LETTER U WITH OGONEK
    0x0179: 0x008f,	#  LATIN CAPITAL LETTER Z WITH ACUTE
    0x017a: 0x0090,	#  LATIN SMALL LETTER Z WITH ACUTE
    0x017b: 0x00fb,	#  LATIN CAPITAL LETTER Z WITH DOT ABOVE
    0x017c: 0x00fd,	#  LATIN SMALL LETTER Z WITH DOT ABOVE
    0x017d: 0x00eb,	#  LATIN CAPITAL LETTER Z WITH CARON
    0x017e: 0x00ec,	#  LATIN SMALL LETTER Z WITH CARON
    0x02c7: 0x00ff,	#  CARON
    0x2013: 0x00d0,	#  EN DASH
    0x2014: 0x00d1,	#  EM DASH
    0x2018: 0x00d4,	#  LEFT SINGLE QUOTATION MARK
    0x2019: 0x00d5,	#  RIGHT SINGLE QUOTATION MARK
    0x201a: 0x00e2,	#  SINGLE LOW-9 QUOTATION MARK
    0x201c: 0x00d2,	#  LEFT DOUBLE QUOTATION MARK
    0x201d: 0x00d3,	#  RIGHT DOUBLE QUOTATION MARK
    0x201e: 0x00e3,	#  DOUBLE LOW-9 QUOTATION MARK
    0x2020: 0x00a0,	#  DAGGER
    0x2022: 0x00a5,	#  BULLET
    0x2026: 0x00c9,	#  HORIZONTAL ELLIPSIS
    0x2039: 0x00dc,	#  SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    0x203a: 0x00dd,	#  SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    0x2122: 0x00aa,	#  TRADE MARK SIGN
    0x2202: 0x00b6,	#  PARTIAL DIFFERENTIAL
    0x2206: 0x00c6,	#  INCREMENT
    0x2211: 0x00b7,	#  N-ARY SUMMATION
    0x221a: 0x00c3,	#  SQUARE ROOT
    0x2260: 0x00ad,	#  NOT EQUAL TO
    0x2264: 0x00b2,	#  LESS-THAN OR EQUAL TO
    0x2265: 0x00b3,	#  GREATER-THAN OR EQUAL TO
    0x25ca: 0x00d7,	#  LOZENGE
}