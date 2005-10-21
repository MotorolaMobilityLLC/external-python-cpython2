""" Python Character Mapping Codec generated from 'VENDORS/APPLE/ICELAND.TXT' with gencodec.py.

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
    0x0081: 0x00c5,	#  LATIN CAPITAL LETTER A WITH RING ABOVE
    0x0082: 0x00c7,	#  LATIN CAPITAL LETTER C WITH CEDILLA
    0x0083: 0x00c9,	#  LATIN CAPITAL LETTER E WITH ACUTE
    0x0084: 0x00d1,	#  LATIN CAPITAL LETTER N WITH TILDE
    0x0085: 0x00d6,	#  LATIN CAPITAL LETTER O WITH DIAERESIS
    0x0086: 0x00dc,	#  LATIN CAPITAL LETTER U WITH DIAERESIS
    0x0087: 0x00e1,	#  LATIN SMALL LETTER A WITH ACUTE
    0x0088: 0x00e0,	#  LATIN SMALL LETTER A WITH GRAVE
    0x0089: 0x00e2,	#  LATIN SMALL LETTER A WITH CIRCUMFLEX
    0x008a: 0x00e4,	#  LATIN SMALL LETTER A WITH DIAERESIS
    0x008b: 0x00e3,	#  LATIN SMALL LETTER A WITH TILDE
    0x008c: 0x00e5,	#  LATIN SMALL LETTER A WITH RING ABOVE
    0x008d: 0x00e7,	#  LATIN SMALL LETTER C WITH CEDILLA
    0x008e: 0x00e9,	#  LATIN SMALL LETTER E WITH ACUTE
    0x008f: 0x00e8,	#  LATIN SMALL LETTER E WITH GRAVE
    0x0090: 0x00ea,	#  LATIN SMALL LETTER E WITH CIRCUMFLEX
    0x0091: 0x00eb,	#  LATIN SMALL LETTER E WITH DIAERESIS
    0x0092: 0x00ed,	#  LATIN SMALL LETTER I WITH ACUTE
    0x0093: 0x00ec,	#  LATIN SMALL LETTER I WITH GRAVE
    0x0094: 0x00ee,	#  LATIN SMALL LETTER I WITH CIRCUMFLEX
    0x0095: 0x00ef,	#  LATIN SMALL LETTER I WITH DIAERESIS
    0x0096: 0x00f1,	#  LATIN SMALL LETTER N WITH TILDE
    0x0097: 0x00f3,	#  LATIN SMALL LETTER O WITH ACUTE
    0x0098: 0x00f2,	#  LATIN SMALL LETTER O WITH GRAVE
    0x0099: 0x00f4,	#  LATIN SMALL LETTER O WITH CIRCUMFLEX
    0x009a: 0x00f6,	#  LATIN SMALL LETTER O WITH DIAERESIS
    0x009b: 0x00f5,	#  LATIN SMALL LETTER O WITH TILDE
    0x009c: 0x00fa,	#  LATIN SMALL LETTER U WITH ACUTE
    0x009d: 0x00f9,	#  LATIN SMALL LETTER U WITH GRAVE
    0x009e: 0x00fb,	#  LATIN SMALL LETTER U WITH CIRCUMFLEX
    0x009f: 0x00fc,	#  LATIN SMALL LETTER U WITH DIAERESIS
    0x00a0: 0x00dd,	#  LATIN CAPITAL LETTER Y WITH ACUTE
    0x00a1: 0x00b0,	#  DEGREE SIGN
    0x00a4: 0x00a7,	#  SECTION SIGN
    0x00a5: 0x2022,	#  BULLET
    0x00a6: 0x00b6,	#  PILCROW SIGN
    0x00a7: 0x00df,	#  LATIN SMALL LETTER SHARP S
    0x00a8: 0x00ae,	#  REGISTERED SIGN
    0x00aa: 0x2122,	#  TRADE MARK SIGN
    0x00ab: 0x00b4,	#  ACUTE ACCENT
    0x00ac: 0x00a8,	#  DIAERESIS
    0x00ad: 0x2260,	#  NOT EQUAL TO
    0x00ae: 0x00c6,	#  LATIN CAPITAL LETTER AE
    0x00af: 0x00d8,	#  LATIN CAPITAL LETTER O WITH STROKE
    0x00b0: 0x221e,	#  INFINITY
    0x00b2: 0x2264,	#  LESS-THAN OR EQUAL TO
    0x00b3: 0x2265,	#  GREATER-THAN OR EQUAL TO
    0x00b4: 0x00a5,	#  YEN SIGN
    0x00b6: 0x2202,	#  PARTIAL DIFFERENTIAL
    0x00b7: 0x2211,	#  N-ARY SUMMATION
    0x00b8: 0x220f,	#  N-ARY PRODUCT
    0x00b9: 0x03c0,	#  GREEK SMALL LETTER PI
    0x00ba: 0x222b,	#  INTEGRAL
    0x00bb: 0x00aa,	#  FEMININE ORDINAL INDICATOR
    0x00bc: 0x00ba,	#  MASCULINE ORDINAL INDICATOR
    0x00bd: 0x03a9,	#  GREEK CAPITAL LETTER OMEGA
    0x00be: 0x00e6,	#  LATIN SMALL LETTER AE
    0x00bf: 0x00f8,	#  LATIN SMALL LETTER O WITH STROKE
    0x00c0: 0x00bf,	#  INVERTED QUESTION MARK
    0x00c1: 0x00a1,	#  INVERTED EXCLAMATION MARK
    0x00c2: 0x00ac,	#  NOT SIGN
    0x00c3: 0x221a,	#  SQUARE ROOT
    0x00c4: 0x0192,	#  LATIN SMALL LETTER F WITH HOOK
    0x00c5: 0x2248,	#  ALMOST EQUAL TO
    0x00c6: 0x2206,	#  INCREMENT
    0x00c7: 0x00ab,	#  LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00c8: 0x00bb,	#  RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00c9: 0x2026,	#  HORIZONTAL ELLIPSIS
    0x00ca: 0x00a0,	#  NO-BREAK SPACE
    0x00cb: 0x00c0,	#  LATIN CAPITAL LETTER A WITH GRAVE
    0x00cc: 0x00c3,	#  LATIN CAPITAL LETTER A WITH TILDE
    0x00cd: 0x00d5,	#  LATIN CAPITAL LETTER O WITH TILDE
    0x00ce: 0x0152,	#  LATIN CAPITAL LIGATURE OE
    0x00cf: 0x0153,	#  LATIN SMALL LIGATURE OE
    0x00d0: 0x2013,	#  EN DASH
    0x00d1: 0x2014,	#  EM DASH
    0x00d2: 0x201c,	#  LEFT DOUBLE QUOTATION MARK
    0x00d3: 0x201d,	#  RIGHT DOUBLE QUOTATION MARK
    0x00d4: 0x2018,	#  LEFT SINGLE QUOTATION MARK
    0x00d5: 0x2019,	#  RIGHT SINGLE QUOTATION MARK
    0x00d6: 0x00f7,	#  DIVISION SIGN
    0x00d7: 0x25ca,	#  LOZENGE
    0x00d8: 0x00ff,	#  LATIN SMALL LETTER Y WITH DIAERESIS
    0x00d9: 0x0178,	#  LATIN CAPITAL LETTER Y WITH DIAERESIS
    0x00da: 0x2044,	#  FRACTION SLASH
    0x00db: 0x20ac,	#  EURO SIGN
    0x00dc: 0x00d0,	#  LATIN CAPITAL LETTER ETH
    0x00dd: 0x00f0,	#  LATIN SMALL LETTER ETH
    0x00df: 0x00fe,	#  LATIN SMALL LETTER THORN
    0x00e0: 0x00fd,	#  LATIN SMALL LETTER Y WITH ACUTE
    0x00e1: 0x00b7,	#  MIDDLE DOT
    0x00e2: 0x201a,	#  SINGLE LOW-9 QUOTATION MARK
    0x00e3: 0x201e,	#  DOUBLE LOW-9 QUOTATION MARK
    0x00e4: 0x2030,	#  PER MILLE SIGN
    0x00e5: 0x00c2,	#  LATIN CAPITAL LETTER A WITH CIRCUMFLEX
    0x00e6: 0x00ca,	#  LATIN CAPITAL LETTER E WITH CIRCUMFLEX
    0x00e7: 0x00c1,	#  LATIN CAPITAL LETTER A WITH ACUTE
    0x00e8: 0x00cb,	#  LATIN CAPITAL LETTER E WITH DIAERESIS
    0x00e9: 0x00c8,	#  LATIN CAPITAL LETTER E WITH GRAVE
    0x00ea: 0x00cd,	#  LATIN CAPITAL LETTER I WITH ACUTE
    0x00eb: 0x00ce,	#  LATIN CAPITAL LETTER I WITH CIRCUMFLEX
    0x00ec: 0x00cf,	#  LATIN CAPITAL LETTER I WITH DIAERESIS
    0x00ed: 0x00cc,	#  LATIN CAPITAL LETTER I WITH GRAVE
    0x00ee: 0x00d3,	#  LATIN CAPITAL LETTER O WITH ACUTE
    0x00ef: 0x00d4,	#  LATIN CAPITAL LETTER O WITH CIRCUMFLEX
    0x00f0: 0xf8ff,	#  Apple logo
    0x00f1: 0x00d2,	#  LATIN CAPITAL LETTER O WITH GRAVE
    0x00f2: 0x00da,	#  LATIN CAPITAL LETTER U WITH ACUTE
    0x00f3: 0x00db,	#  LATIN CAPITAL LETTER U WITH CIRCUMFLEX
    0x00f4: 0x00d9,	#  LATIN CAPITAL LETTER U WITH GRAVE
    0x00f5: 0x0131,	#  LATIN SMALL LETTER DOTLESS I
    0x00f6: 0x02c6,	#  MODIFIER LETTER CIRCUMFLEX ACCENT
    0x00f7: 0x02dc,	#  SMALL TILDE
    0x00f8: 0x00af,	#  MACRON
    0x00f9: 0x02d8,	#  BREVE
    0x00fa: 0x02d9,	#  DOT ABOVE
    0x00fb: 0x02da,	#  RING ABOVE
    0x00fc: 0x00b8,	#  CEDILLA
    0x00fd: 0x02dd,	#  DOUBLE ACUTE ACCENT
    0x00fe: 0x02db,	#  OGONEK
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
    u'\xc5'	#  0x0081 -> LATIN CAPITAL LETTER A WITH RING ABOVE
    u'\xc7'	#  0x0082 -> LATIN CAPITAL LETTER C WITH CEDILLA
    u'\xc9'	#  0x0083 -> LATIN CAPITAL LETTER E WITH ACUTE
    u'\xd1'	#  0x0084 -> LATIN CAPITAL LETTER N WITH TILDE
    u'\xd6'	#  0x0085 -> LATIN CAPITAL LETTER O WITH DIAERESIS
    u'\xdc'	#  0x0086 -> LATIN CAPITAL LETTER U WITH DIAERESIS
    u'\xe1'	#  0x0087 -> LATIN SMALL LETTER A WITH ACUTE
    u'\xe0'	#  0x0088 -> LATIN SMALL LETTER A WITH GRAVE
    u'\xe2'	#  0x0089 -> LATIN SMALL LETTER A WITH CIRCUMFLEX
    u'\xe4'	#  0x008a -> LATIN SMALL LETTER A WITH DIAERESIS
    u'\xe3'	#  0x008b -> LATIN SMALL LETTER A WITH TILDE
    u'\xe5'	#  0x008c -> LATIN SMALL LETTER A WITH RING ABOVE
    u'\xe7'	#  0x008d -> LATIN SMALL LETTER C WITH CEDILLA
    u'\xe9'	#  0x008e -> LATIN SMALL LETTER E WITH ACUTE
    u'\xe8'	#  0x008f -> LATIN SMALL LETTER E WITH GRAVE
    u'\xea'	#  0x0090 -> LATIN SMALL LETTER E WITH CIRCUMFLEX
    u'\xeb'	#  0x0091 -> LATIN SMALL LETTER E WITH DIAERESIS
    u'\xed'	#  0x0092 -> LATIN SMALL LETTER I WITH ACUTE
    u'\xec'	#  0x0093 -> LATIN SMALL LETTER I WITH GRAVE
    u'\xee'	#  0x0094 -> LATIN SMALL LETTER I WITH CIRCUMFLEX
    u'\xef'	#  0x0095 -> LATIN SMALL LETTER I WITH DIAERESIS
    u'\xf1'	#  0x0096 -> LATIN SMALL LETTER N WITH TILDE
    u'\xf3'	#  0x0097 -> LATIN SMALL LETTER O WITH ACUTE
    u'\xf2'	#  0x0098 -> LATIN SMALL LETTER O WITH GRAVE
    u'\xf4'	#  0x0099 -> LATIN SMALL LETTER O WITH CIRCUMFLEX
    u'\xf6'	#  0x009a -> LATIN SMALL LETTER O WITH DIAERESIS
    u'\xf5'	#  0x009b -> LATIN SMALL LETTER O WITH TILDE
    u'\xfa'	#  0x009c -> LATIN SMALL LETTER U WITH ACUTE
    u'\xf9'	#  0x009d -> LATIN SMALL LETTER U WITH GRAVE
    u'\xfb'	#  0x009e -> LATIN SMALL LETTER U WITH CIRCUMFLEX
    u'\xfc'	#  0x009f -> LATIN SMALL LETTER U WITH DIAERESIS
    u'\xdd'	#  0x00a0 -> LATIN CAPITAL LETTER Y WITH ACUTE
    u'\xb0'	#  0x00a1 -> DEGREE SIGN
    u'\xa2'	#  0x00a2 -> CENT SIGN
    u'\xa3'	#  0x00a3 -> POUND SIGN
    u'\xa7'	#  0x00a4 -> SECTION SIGN
    u'\u2022'	#  0x00a5 -> BULLET
    u'\xb6'	#  0x00a6 -> PILCROW SIGN
    u'\xdf'	#  0x00a7 -> LATIN SMALL LETTER SHARP S
    u'\xae'	#  0x00a8 -> REGISTERED SIGN
    u'\xa9'	#  0x00a9 -> COPYRIGHT SIGN
    u'\u2122'	#  0x00aa -> TRADE MARK SIGN
    u'\xb4'	#  0x00ab -> ACUTE ACCENT
    u'\xa8'	#  0x00ac -> DIAERESIS
    u'\u2260'	#  0x00ad -> NOT EQUAL TO
    u'\xc6'	#  0x00ae -> LATIN CAPITAL LETTER AE
    u'\xd8'	#  0x00af -> LATIN CAPITAL LETTER O WITH STROKE
    u'\u221e'	#  0x00b0 -> INFINITY
    u'\xb1'	#  0x00b1 -> PLUS-MINUS SIGN
    u'\u2264'	#  0x00b2 -> LESS-THAN OR EQUAL TO
    u'\u2265'	#  0x00b3 -> GREATER-THAN OR EQUAL TO
    u'\xa5'	#  0x00b4 -> YEN SIGN
    u'\xb5'	#  0x00b5 -> MICRO SIGN
    u'\u2202'	#  0x00b6 -> PARTIAL DIFFERENTIAL
    u'\u2211'	#  0x00b7 -> N-ARY SUMMATION
    u'\u220f'	#  0x00b8 -> N-ARY PRODUCT
    u'\u03c0'	#  0x00b9 -> GREEK SMALL LETTER PI
    u'\u222b'	#  0x00ba -> INTEGRAL
    u'\xaa'	#  0x00bb -> FEMININE ORDINAL INDICATOR
    u'\xba'	#  0x00bc -> MASCULINE ORDINAL INDICATOR
    u'\u03a9'	#  0x00bd -> GREEK CAPITAL LETTER OMEGA
    u'\xe6'	#  0x00be -> LATIN SMALL LETTER AE
    u'\xf8'	#  0x00bf -> LATIN SMALL LETTER O WITH STROKE
    u'\xbf'	#  0x00c0 -> INVERTED QUESTION MARK
    u'\xa1'	#  0x00c1 -> INVERTED EXCLAMATION MARK
    u'\xac'	#  0x00c2 -> NOT SIGN
    u'\u221a'	#  0x00c3 -> SQUARE ROOT
    u'\u0192'	#  0x00c4 -> LATIN SMALL LETTER F WITH HOOK
    u'\u2248'	#  0x00c5 -> ALMOST EQUAL TO
    u'\u2206'	#  0x00c6 -> INCREMENT
    u'\xab'	#  0x00c7 -> LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    u'\xbb'	#  0x00c8 -> RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    u'\u2026'	#  0x00c9 -> HORIZONTAL ELLIPSIS
    u'\xa0'	#  0x00ca -> NO-BREAK SPACE
    u'\xc0'	#  0x00cb -> LATIN CAPITAL LETTER A WITH GRAVE
    u'\xc3'	#  0x00cc -> LATIN CAPITAL LETTER A WITH TILDE
    u'\xd5'	#  0x00cd -> LATIN CAPITAL LETTER O WITH TILDE
    u'\u0152'	#  0x00ce -> LATIN CAPITAL LIGATURE OE
    u'\u0153'	#  0x00cf -> LATIN SMALL LIGATURE OE
    u'\u2013'	#  0x00d0 -> EN DASH
    u'\u2014'	#  0x00d1 -> EM DASH
    u'\u201c'	#  0x00d2 -> LEFT DOUBLE QUOTATION MARK
    u'\u201d'	#  0x00d3 -> RIGHT DOUBLE QUOTATION MARK
    u'\u2018'	#  0x00d4 -> LEFT SINGLE QUOTATION MARK
    u'\u2019'	#  0x00d5 -> RIGHT SINGLE QUOTATION MARK
    u'\xf7'	#  0x00d6 -> DIVISION SIGN
    u'\u25ca'	#  0x00d7 -> LOZENGE
    u'\xff'	#  0x00d8 -> LATIN SMALL LETTER Y WITH DIAERESIS
    u'\u0178'	#  0x00d9 -> LATIN CAPITAL LETTER Y WITH DIAERESIS
    u'\u2044'	#  0x00da -> FRACTION SLASH
    u'\u20ac'	#  0x00db -> EURO SIGN
    u'\xd0'	#  0x00dc -> LATIN CAPITAL LETTER ETH
    u'\xf0'	#  0x00dd -> LATIN SMALL LETTER ETH
    u'\xde'	#  0x00de -> LATIN CAPITAL LETTER THORN
    u'\xfe'	#  0x00df -> LATIN SMALL LETTER THORN
    u'\xfd'	#  0x00e0 -> LATIN SMALL LETTER Y WITH ACUTE
    u'\xb7'	#  0x00e1 -> MIDDLE DOT
    u'\u201a'	#  0x00e2 -> SINGLE LOW-9 QUOTATION MARK
    u'\u201e'	#  0x00e3 -> DOUBLE LOW-9 QUOTATION MARK
    u'\u2030'	#  0x00e4 -> PER MILLE SIGN
    u'\xc2'	#  0x00e5 -> LATIN CAPITAL LETTER A WITH CIRCUMFLEX
    u'\xca'	#  0x00e6 -> LATIN CAPITAL LETTER E WITH CIRCUMFLEX
    u'\xc1'	#  0x00e7 -> LATIN CAPITAL LETTER A WITH ACUTE
    u'\xcb'	#  0x00e8 -> LATIN CAPITAL LETTER E WITH DIAERESIS
    u'\xc8'	#  0x00e9 -> LATIN CAPITAL LETTER E WITH GRAVE
    u'\xcd'	#  0x00ea -> LATIN CAPITAL LETTER I WITH ACUTE
    u'\xce'	#  0x00eb -> LATIN CAPITAL LETTER I WITH CIRCUMFLEX
    u'\xcf'	#  0x00ec -> LATIN CAPITAL LETTER I WITH DIAERESIS
    u'\xcc'	#  0x00ed -> LATIN CAPITAL LETTER I WITH GRAVE
    u'\xd3'	#  0x00ee -> LATIN CAPITAL LETTER O WITH ACUTE
    u'\xd4'	#  0x00ef -> LATIN CAPITAL LETTER O WITH CIRCUMFLEX
    u'\uf8ff'	#  0x00f0 -> Apple logo
    u'\xd2'	#  0x00f1 -> LATIN CAPITAL LETTER O WITH GRAVE
    u'\xda'	#  0x00f2 -> LATIN CAPITAL LETTER U WITH ACUTE
    u'\xdb'	#  0x00f3 -> LATIN CAPITAL LETTER U WITH CIRCUMFLEX
    u'\xd9'	#  0x00f4 -> LATIN CAPITAL LETTER U WITH GRAVE
    u'\u0131'	#  0x00f5 -> LATIN SMALL LETTER DOTLESS I
    u'\u02c6'	#  0x00f6 -> MODIFIER LETTER CIRCUMFLEX ACCENT
    u'\u02dc'	#  0x00f7 -> SMALL TILDE
    u'\xaf'	#  0x00f8 -> MACRON
    u'\u02d8'	#  0x00f9 -> BREVE
    u'\u02d9'	#  0x00fa -> DOT ABOVE
    u'\u02da'	#  0x00fb -> RING ABOVE
    u'\xb8'	#  0x00fc -> CEDILLA
    u'\u02dd'	#  0x00fd -> DOUBLE ACUTE ACCENT
    u'\u02db'	#  0x00fe -> OGONEK
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
    0x00a1: 0x00c1,	#  INVERTED EXCLAMATION MARK
    0x00a2: 0x00a2,	#  CENT SIGN
    0x00a3: 0x00a3,	#  POUND SIGN
    0x00a5: 0x00b4,	#  YEN SIGN
    0x00a7: 0x00a4,	#  SECTION SIGN
    0x00a8: 0x00ac,	#  DIAERESIS
    0x00a9: 0x00a9,	#  COPYRIGHT SIGN
    0x00aa: 0x00bb,	#  FEMININE ORDINAL INDICATOR
    0x00ab: 0x00c7,	#  LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00ac: 0x00c2,	#  NOT SIGN
    0x00ae: 0x00a8,	#  REGISTERED SIGN
    0x00af: 0x00f8,	#  MACRON
    0x00b0: 0x00a1,	#  DEGREE SIGN
    0x00b1: 0x00b1,	#  PLUS-MINUS SIGN
    0x00b4: 0x00ab,	#  ACUTE ACCENT
    0x00b5: 0x00b5,	#  MICRO SIGN
    0x00b6: 0x00a6,	#  PILCROW SIGN
    0x00b7: 0x00e1,	#  MIDDLE DOT
    0x00b8: 0x00fc,	#  CEDILLA
    0x00ba: 0x00bc,	#  MASCULINE ORDINAL INDICATOR
    0x00bb: 0x00c8,	#  RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00bf: 0x00c0,	#  INVERTED QUESTION MARK
    0x00c0: 0x00cb,	#  LATIN CAPITAL LETTER A WITH GRAVE
    0x00c1: 0x00e7,	#  LATIN CAPITAL LETTER A WITH ACUTE
    0x00c2: 0x00e5,	#  LATIN CAPITAL LETTER A WITH CIRCUMFLEX
    0x00c3: 0x00cc,	#  LATIN CAPITAL LETTER A WITH TILDE
    0x00c4: 0x0080,	#  LATIN CAPITAL LETTER A WITH DIAERESIS
    0x00c5: 0x0081,	#  LATIN CAPITAL LETTER A WITH RING ABOVE
    0x00c6: 0x00ae,	#  LATIN CAPITAL LETTER AE
    0x00c7: 0x0082,	#  LATIN CAPITAL LETTER C WITH CEDILLA
    0x00c8: 0x00e9,	#  LATIN CAPITAL LETTER E WITH GRAVE
    0x00c9: 0x0083,	#  LATIN CAPITAL LETTER E WITH ACUTE
    0x00ca: 0x00e6,	#  LATIN CAPITAL LETTER E WITH CIRCUMFLEX
    0x00cb: 0x00e8,	#  LATIN CAPITAL LETTER E WITH DIAERESIS
    0x00cc: 0x00ed,	#  LATIN CAPITAL LETTER I WITH GRAVE
    0x00cd: 0x00ea,	#  LATIN CAPITAL LETTER I WITH ACUTE
    0x00ce: 0x00eb,	#  LATIN CAPITAL LETTER I WITH CIRCUMFLEX
    0x00cf: 0x00ec,	#  LATIN CAPITAL LETTER I WITH DIAERESIS
    0x00d0: 0x00dc,	#  LATIN CAPITAL LETTER ETH
    0x00d1: 0x0084,	#  LATIN CAPITAL LETTER N WITH TILDE
    0x00d2: 0x00f1,	#  LATIN CAPITAL LETTER O WITH GRAVE
    0x00d3: 0x00ee,	#  LATIN CAPITAL LETTER O WITH ACUTE
    0x00d4: 0x00ef,	#  LATIN CAPITAL LETTER O WITH CIRCUMFLEX
    0x00d5: 0x00cd,	#  LATIN CAPITAL LETTER O WITH TILDE
    0x00d6: 0x0085,	#  LATIN CAPITAL LETTER O WITH DIAERESIS
    0x00d8: 0x00af,	#  LATIN CAPITAL LETTER O WITH STROKE
    0x00d9: 0x00f4,	#  LATIN CAPITAL LETTER U WITH GRAVE
    0x00da: 0x00f2,	#  LATIN CAPITAL LETTER U WITH ACUTE
    0x00db: 0x00f3,	#  LATIN CAPITAL LETTER U WITH CIRCUMFLEX
    0x00dc: 0x0086,	#  LATIN CAPITAL LETTER U WITH DIAERESIS
    0x00dd: 0x00a0,	#  LATIN CAPITAL LETTER Y WITH ACUTE
    0x00de: 0x00de,	#  LATIN CAPITAL LETTER THORN
    0x00df: 0x00a7,	#  LATIN SMALL LETTER SHARP S
    0x00e0: 0x0088,	#  LATIN SMALL LETTER A WITH GRAVE
    0x00e1: 0x0087,	#  LATIN SMALL LETTER A WITH ACUTE
    0x00e2: 0x0089,	#  LATIN SMALL LETTER A WITH CIRCUMFLEX
    0x00e3: 0x008b,	#  LATIN SMALL LETTER A WITH TILDE
    0x00e4: 0x008a,	#  LATIN SMALL LETTER A WITH DIAERESIS
    0x00e5: 0x008c,	#  LATIN SMALL LETTER A WITH RING ABOVE
    0x00e6: 0x00be,	#  LATIN SMALL LETTER AE
    0x00e7: 0x008d,	#  LATIN SMALL LETTER C WITH CEDILLA
    0x00e8: 0x008f,	#  LATIN SMALL LETTER E WITH GRAVE
    0x00e9: 0x008e,	#  LATIN SMALL LETTER E WITH ACUTE
    0x00ea: 0x0090,	#  LATIN SMALL LETTER E WITH CIRCUMFLEX
    0x00eb: 0x0091,	#  LATIN SMALL LETTER E WITH DIAERESIS
    0x00ec: 0x0093,	#  LATIN SMALL LETTER I WITH GRAVE
    0x00ed: 0x0092,	#  LATIN SMALL LETTER I WITH ACUTE
    0x00ee: 0x0094,	#  LATIN SMALL LETTER I WITH CIRCUMFLEX
    0x00ef: 0x0095,	#  LATIN SMALL LETTER I WITH DIAERESIS
    0x00f0: 0x00dd,	#  LATIN SMALL LETTER ETH
    0x00f1: 0x0096,	#  LATIN SMALL LETTER N WITH TILDE
    0x00f2: 0x0098,	#  LATIN SMALL LETTER O WITH GRAVE
    0x00f3: 0x0097,	#  LATIN SMALL LETTER O WITH ACUTE
    0x00f4: 0x0099,	#  LATIN SMALL LETTER O WITH CIRCUMFLEX
    0x00f5: 0x009b,	#  LATIN SMALL LETTER O WITH TILDE
    0x00f6: 0x009a,	#  LATIN SMALL LETTER O WITH DIAERESIS
    0x00f7: 0x00d6,	#  DIVISION SIGN
    0x00f8: 0x00bf,	#  LATIN SMALL LETTER O WITH STROKE
    0x00f9: 0x009d,	#  LATIN SMALL LETTER U WITH GRAVE
    0x00fa: 0x009c,	#  LATIN SMALL LETTER U WITH ACUTE
    0x00fb: 0x009e,	#  LATIN SMALL LETTER U WITH CIRCUMFLEX
    0x00fc: 0x009f,	#  LATIN SMALL LETTER U WITH DIAERESIS
    0x00fd: 0x00e0,	#  LATIN SMALL LETTER Y WITH ACUTE
    0x00fe: 0x00df,	#  LATIN SMALL LETTER THORN
    0x00ff: 0x00d8,	#  LATIN SMALL LETTER Y WITH DIAERESIS
    0x0131: 0x00f5,	#  LATIN SMALL LETTER DOTLESS I
    0x0152: 0x00ce,	#  LATIN CAPITAL LIGATURE OE
    0x0153: 0x00cf,	#  LATIN SMALL LIGATURE OE
    0x0178: 0x00d9,	#  LATIN CAPITAL LETTER Y WITH DIAERESIS
    0x0192: 0x00c4,	#  LATIN SMALL LETTER F WITH HOOK
    0x02c6: 0x00f6,	#  MODIFIER LETTER CIRCUMFLEX ACCENT
    0x02c7: 0x00ff,	#  CARON
    0x02d8: 0x00f9,	#  BREVE
    0x02d9: 0x00fa,	#  DOT ABOVE
    0x02da: 0x00fb,	#  RING ABOVE
    0x02db: 0x00fe,	#  OGONEK
    0x02dc: 0x00f7,	#  SMALL TILDE
    0x02dd: 0x00fd,	#  DOUBLE ACUTE ACCENT
    0x03a9: 0x00bd,	#  GREEK CAPITAL LETTER OMEGA
    0x03c0: 0x00b9,	#  GREEK SMALL LETTER PI
    0x2013: 0x00d0,	#  EN DASH
    0x2014: 0x00d1,	#  EM DASH
    0x2018: 0x00d4,	#  LEFT SINGLE QUOTATION MARK
    0x2019: 0x00d5,	#  RIGHT SINGLE QUOTATION MARK
    0x201a: 0x00e2,	#  SINGLE LOW-9 QUOTATION MARK
    0x201c: 0x00d2,	#  LEFT DOUBLE QUOTATION MARK
    0x201d: 0x00d3,	#  RIGHT DOUBLE QUOTATION MARK
    0x201e: 0x00e3,	#  DOUBLE LOW-9 QUOTATION MARK
    0x2022: 0x00a5,	#  BULLET
    0x2026: 0x00c9,	#  HORIZONTAL ELLIPSIS
    0x2030: 0x00e4,	#  PER MILLE SIGN
    0x2044: 0x00da,	#  FRACTION SLASH
    0x20ac: 0x00db,	#  EURO SIGN
    0x2122: 0x00aa,	#  TRADE MARK SIGN
    0x2202: 0x00b6,	#  PARTIAL DIFFERENTIAL
    0x2206: 0x00c6,	#  INCREMENT
    0x220f: 0x00b8,	#  N-ARY PRODUCT
    0x2211: 0x00b7,	#  N-ARY SUMMATION
    0x221a: 0x00c3,	#  SQUARE ROOT
    0x221e: 0x00b0,	#  INFINITY
    0x222b: 0x00ba,	#  INTEGRAL
    0x2248: 0x00c5,	#  ALMOST EQUAL TO
    0x2260: 0x00ad,	#  NOT EQUAL TO
    0x2264: 0x00b2,	#  LESS-THAN OR EQUAL TO
    0x2265: 0x00b3,	#  GREATER-THAN OR EQUAL TO
    0x25ca: 0x00d7,	#  LOZENGE
    0xf8ff: 0x00f0,	#  Apple logo
}