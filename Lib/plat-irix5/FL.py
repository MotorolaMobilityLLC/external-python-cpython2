# Constants used by the FORMS library (module fl).
# This corresponds to "forms.h".
# Recommended use: import FL; ... FL.NORMAL_BOX ... etc.
# Alternate use: from FL import *; ... NORMAL_BOX ... etc.

_v20 = 1
_v21 = 1
##import fl
##try:
##	_v20 = (fl.get_rgbmode is not None)
##except:
##	_v20 = 0
##del fl

NULL = 0
FALSE = 0
TRUE = 1

EVENT = -1

LABEL_SIZE = 64
if _v20:
	SHORTCUT_SIZE = 32
PLACE_FREE = 0
PLACE_SIZE = 1
PLACE_ASPECT = 2
PLACE_MOUSE = 3
PLACE_CENTER = 4
PLACE_POSITION = 5
FL_PLACE_FULLSCREEN = 6
FIND_INPUT = 0
FIND_AUTOMATIC = 1
FIND_MOUSE = 2
BEGIN_GROUP = 10000
END_GROUP = 20000
ALIGN_TOP = 0
ALIGN_BOTTOM = 1
ALIGN_LEFT = 2
ALIGN_RIGHT = 3
ALIGN_CENTER = 4
NO_BOX = 0
UP_BOX = 1
DOWN_BOX = 2
FLAT_BOX = 3
BORDER_BOX = 4
SHADOW_BOX = 5
FRAME_BOX = 6
ROUNDED_BOX = 7
RFLAT_BOX = 8
RSHADOW_BOX = 9
TOP_BOUND_COL = 51
LEFT_BOUND_COL = 55
BOT_BOUND_COL = 40
RIGHT_BOUND_COL = 35
COL1 = 47
MCOL = 49
LCOL = 0
BOUND_WIDTH = 3.0
DRAW = 0
PUSH = 1
RELEASE = 2
ENTER = 3
LEAVE = 4
MOUSE = 5
FOCUS = 6
UNFOCUS = 7
KEYBOARD = 8
STEP = 9
MOVE = 10
FONT_NAME = 'Helvetica'
FONT_BOLDNAME = 'Helvetica-Bold'
FONT_ITALICNAME = 'Helvetica-Oblique'
FONT_FIXEDNAME = 'Courier'
FONT_ICONNAME = 'Icon'
SMALL_FONT = 8.0
NORMAL_FONT = 11.0
LARGE_FONT = 20.0
NORMAL_STYLE = 0
BOLD_STYLE = 1
ITALIC_STYLE = 2
FIXED_STYLE = 3
ENGRAVED_STYLE = 4
ICON_STYLE = 5
BITMAP = 3
NORMAL_BITMAP = 0
BITMAP_BOXTYPE = NO_BOX
BITMAP_COL1 = 0
BITMAP_COL2 = COL1
BITMAP_LCOL = LCOL
BITMAP_ALIGN = ALIGN_BOTTOM
BITMAP_MAXSIZE = 128*128
BITMAP_BW = BOUND_WIDTH
BOX = 1
BOX_BOXTYPE = UP_BOX
BOX_COL1 = COL1
BOX_LCOL = LCOL
BOX_ALIGN = ALIGN_CENTER
BOX_BW = BOUND_WIDTH
BROWSER = 71
NORMAL_BROWSER = 0
SELECT_BROWSER = 1
HOLD_BROWSER = 2
MULTI_BROWSER = 3
BROWSER_BOXTYPE = DOWN_BOX
BROWSER_COL1 = COL1
BROWSER_COL2 = 3
BROWSER_LCOL = LCOL
BROWSER_ALIGN = ALIGN_BOTTOM
BROWSER_SLCOL = COL1
BROWSER_BW = BOUND_WIDTH
BROWSER_LINELENGTH = 128
BROWSER_MAXLINE = 512
BUTTON = 11
NORMAL_BUTTON = 0
PUSH_BUTTON = 1
RADIO_BUTTON = 2
HIDDEN_BUTTON = 3
TOUCH_BUTTON = 4
INOUT_BUTTON = 5
RETURN_BUTTON = 6
if _v20:
	HIDDEN_RET_BUTTON = 7
BUTTON_BOXTYPE = UP_BOX
BUTTON_COL1 = COL1
BUTTON_COL2 = COL1
BUTTON_LCOL = LCOL
BUTTON_ALIGN = ALIGN_CENTER
BUTTON_MCOL1 = MCOL
BUTTON_MCOL2 = MCOL
BUTTON_BW = BOUND_WIDTH
if _v20:
	CHART = 4
	BAR_CHART = 0
	HORBAR_CHART = 1
	LINE_CHART = 2
	FILLED_CHART = 3
	SPIKE_CHART = 4
	PIE_CHART = 5
	SPECIALPIE_CHART = 6
	CHART_BOXTYPE = BORDER_BOX
	CHART_COL1 = COL1
	CHART_LCOL = LCOL
	CHART_ALIGN = ALIGN_BOTTOM
	CHART_BW = BOUND_WIDTH
	CHART_MAX = 128
CHOICE = 42
NORMAL_CHOICE = 0
CHOICE_BOXTYPE = DOWN_BOX
CHOICE_COL1 = COL1
CHOICE_COL2 = LCOL
CHOICE_LCOL = LCOL
CHOICE_ALIGN = ALIGN_LEFT
CHOICE_BW = BOUND_WIDTH
CHOICE_MCOL = MCOL
CHOICE_MAXITEMS = 128
CHOICE_MAXSTR = 64
CLOCK = 61
SQUARE_CLOCK = 0
ROUND_CLOCK = 1
CLOCK_BOXTYPE = UP_BOX
CLOCK_COL1 = 37
CLOCK_COL2 = 42
CLOCK_LCOL = LCOL
CLOCK_ALIGN = ALIGN_BOTTOM
CLOCK_TOPCOL = COL1
CLOCK_BW = BOUND_WIDTH
COUNTER = 25
NORMAL_COUNTER = 0
SIMPLE_COUNTER = 1
COUNTER_BOXTYPE = UP_BOX
COUNTER_COL1 = COL1
COUNTER_COL2 = 4
COUNTER_LCOL = LCOL
COUNTER_ALIGN = ALIGN_BOTTOM
if _v20:
	COUNTER_BW = BOUND_WIDTH
else:
	DEFAULT = 51
	RETURN_DEFAULT = 0
	ALWAYS_DEFAULT = 1
DIAL = 22
NORMAL_DIAL = 0
LINE_DIAL = 1
DIAL_BOXTYPE = NO_BOX
DIAL_COL1 = COL1
DIAL_COL2 = 37
DIAL_LCOL = LCOL
DIAL_ALIGN = ALIGN_BOTTOM
DIAL_TOPCOL = COL1
DIAL_BW = BOUND_WIDTH
FREE = 101
NORMAL_FREE = 1
SLEEPING_FREE = 2
INPUT_FREE = 3
CONTINUOUS_FREE = 4
ALL_FREE = 5
INPUT = 31
NORMAL_INPUT = 0
if _v20:
	FLOAT_INPUT = 1
	INT_INPUT = 2
	HIDDEN_INPUT = 3
	if _v21:
		MULTILINE_INPUT = 4
		SECRET_INPUT = 5
else:
	ALWAYS_INPUT = 1
INPUT_BOXTYPE = DOWN_BOX
INPUT_COL1 = 13
INPUT_COL2 = 5
INPUT_LCOL = LCOL
INPUT_ALIGN = ALIGN_LEFT
INPUT_TCOL = LCOL
INPUT_CCOL = 4
INPUT_BW = BOUND_WIDTH
INPUT_MAX = 128
LIGHTBUTTON = 12
LIGHTBUTTON_BOXTYPE = UP_BOX
LIGHTBUTTON_COL1 = 39
LIGHTBUTTON_COL2 = 3
LIGHTBUTTON_LCOL = LCOL
LIGHTBUTTON_ALIGN = ALIGN_CENTER
LIGHTBUTTON_TOPCOL = COL1
LIGHTBUTTON_MCOL = MCOL
LIGHTBUTTON_BW1 = BOUND_WIDTH
LIGHTBUTTON_BW2 = BOUND_WIDTH/2.0
LIGHTBUTTON_MINSIZE = 12.0
MENU = 41
TOUCH_MENU = 0
PUSH_MENU = 1
MENU_BOXTYPE = BORDER_BOX
MENU_COL1 = 55
MENU_COL2 = 37
MENU_LCOL = LCOL
MENU_ALIGN = ALIGN_CENTER
MENU_BW = BOUND_WIDTH
MENU_MAX = 300
POSITIONER = 23
NORMAL_POSITIONER = 0
POSITIONER_BOXTYPE = DOWN_BOX
POSITIONER_COL1 = COL1
POSITIONER_COL2 = 1
POSITIONER_LCOL = LCOL
POSITIONER_ALIGN = ALIGN_BOTTOM
POSITIONER_BW = BOUND_WIDTH
ROUNDBUTTON = 13
ROUNDBUTTON_BOXTYPE = NO_BOX
ROUNDBUTTON_COL1 = 7
ROUNDBUTTON_COL2 = 3
ROUNDBUTTON_LCOL = LCOL
ROUNDBUTTON_ALIGN = ALIGN_CENTER
ROUNDBUTTON_TOPCOL = COL1
ROUNDBUTTON_MCOL = MCOL
ROUNDBUTTON_BW = BOUND_WIDTH
SLIDER = 21
VALSLIDER = 24
VERT_SLIDER = 0
HOR_SLIDER = 1
VERT_FILL_SLIDER = 2
HOR_FILL_SLIDER = 3
VERT_NICE_SLIDER = 4
HOR_NICE_SLIDER = 5
SLIDER_BOXTYPE = DOWN_BOX
SLIDER_COL1 = COL1
SLIDER_COL2 = COL1
SLIDER_LCOL = LCOL
SLIDER_ALIGN = ALIGN_BOTTOM
SLIDER_BW1 = BOUND_WIDTH
SLIDER_BW2 = BOUND_WIDTH*0.75
SLIDER_FINE = 0.05
SLIDER_WIDTH = 0.08
TEXT = 2
NORMAL_TEXT = 0
TEXT_BOXTYPE = NO_BOX
TEXT_COL1 = COL1
TEXT_LCOL = LCOL
TEXT_ALIGN = ALIGN_LEFT
TEXT_BW = BOUND_WIDTH
TIMER = 62
NORMAL_TIMER = 0
VALUE_TIMER = 1
HIDDEN_TIMER = 2
TIMER_BOXTYPE = DOWN_BOX
TIMER_COL1 = COL1
TIMER_COL2 = 1
TIMER_LCOL = LCOL
TIMER_ALIGN = ALIGN_CENTER
TIMER_BW = BOUND_WIDTH
TIMER_BLINKRATE = 0.2
