"""Suite Window classes: Classes representing windows
Level 1, version 1

Generated from /Volumes/Moes/Systeemmap/Finder
AETE/AEUT resource version 0/144, language 0, script 0
"""

import aetools
import MacOS

_code = 'fndr'

class Window_classes_Events:

	pass


class clipping_window(aetools.ComponentItem):
	"""clipping window - The window containing a clipping """
	want = 'lwnd'
class _3c_Inheritance_3e_(aetools.NProperty):
	"""<Inheritance> - inherits some of its properties from the window class """
	which = 'c@#^'
	want = 'cwin'

clipping_windows = clipping_window

class container_window(aetools.ComponentItem):
	"""container window - A window that contains items """
	want = 'cwnd'
class button_view_arrangement(aetools.NProperty):
	"""button view arrangement - the property by which to keep icons arranged within a button view window """
	which = 'barr'
	want = 'earr'
class calculates_folder_sizes(aetools.NProperty):
	"""calculates folder sizes - Are folder sizes calculated and displayed in the window? (does not apply to suitcase windows) """
	which = 'sfsz'
	want = 'bool'
class container(aetools.NProperty):
	"""container - the container from which the window was opened """
	which = 'ctnr'
	want = 'obj '
class has_custom_view_settings(aetools.NProperty):
	"""has custom view settings - Does the folder have custom view settings or is it using the default global settings? """
	which = 'cuss'
	want = 'bool'
class item(aetools.NProperty):
	"""item - the item from which the window was opened (always returns something) """
	which = 'cobj'
	want = 'obj '
class previous_list_view(aetools.NProperty):
	"""previous list view - the last non-icon view (by name, by date, etc.) selected for the container (forgotten as soon as the window is closed and only available when the window is open) """
	which = 'svew'
	want = 'enum'
class shows_comments(aetools.NProperty):
	"""shows comments - Are comments displayed in the window? (does not apply to suitcases) """
	which = 'scom'
	want = 'bool'
class shows_creation_date(aetools.NProperty):
	"""shows creation date - Are creation dates displayed in the window? """
	which = 'scda'
	want = 'bool'
class shows_kind(aetools.NProperty):
	"""shows kind - Are document kinds displayed in the window? """
	which = 'sknd'
	want = 'bool'
class shows_label(aetools.NProperty):
	"""shows label - Are labels displayed in the window? """
	which = 'slbl'
	want = 'bool'
class shows_modification_date(aetools.NProperty):
	"""shows modification date - Are modification dates displayed in the window? """
	which = 'sdat'
	want = 'bool'
class shows_size(aetools.NProperty):
	"""shows size - Are file sizes displayed in the window? """
	which = 'ssiz'
	want = 'bool'
class shows_version(aetools.NProperty):
	"""shows version - Are file versions displayed in the window? (does not apply to suitcase windows) """
	which = 'svrs'
	want = 'bool'
class sort_direction(aetools.NProperty):
	"""sort direction - The direction in which the window is sorted """
	which = 'sord'
	want = 'sodr'
class spatial_view_arrangement(aetools.NProperty):
	"""spatial view arrangement - the property by which to keep icons arranged within a spatial view window """
	which = 'iarr'
	want = 'earr'
class uses_relative_dates(aetools.NProperty):
	"""uses relative dates - Are relative dates (e.g., today, yesterday) shown in the window? """
	which = 'urdt'
	want = 'bool'
class view(aetools.NProperty):
	"""view - the current view for the window (icon, name, date, etc.) """
	which = 'pvew'
	want = 'long'

container_windows = container_window

class content_space(aetools.ComponentItem):
	"""content space - All windows, including the desktop window (\xd2Window\xd3 does not include the desktop window) """
	want = 'dwnd'

content_spaces = content_space

class information_window(aetools.ComponentItem):
	"""information window - An information window (opened by \xd2Get Info\xd3) """
	want = 'iwnd'
class comment(aetools.NProperty):
	"""comment - the comment """
	which = 'comt'
	want = 'itxt'
class creation_date(aetools.NProperty):
	"""creation date - the date on which the item was created """
	which = 'ascd'
	want = 'ldt '
class current_panel(aetools.NProperty):
	"""current panel - the current panel in the information window """
	which = 'panl'
	want = 'ipnl'
class icon(aetools.NProperty):
	"""icon - the icon bitmap of the item """
	which = 'iimg'
	want = 'ifam'
class locked(aetools.NProperty):
	"""locked - Is the item locked (applies only to file and application information windows)? """
	which = 'aslk'
	want = 'bool'
class minimum_size(aetools.NProperty):
	"""minimum size - the smallest memory size with which the application can be launched (only applies to information windows for applications) """
	which = 'mprt'
	want = 'long'
class modification_date(aetools.NProperty):
	"""modification date - the date on which the item was last modified """
	which = 'asmo'
	want = 'ldt '
class physical_size(aetools.NProperty):
	"""physical size - the actual space used by the item on disk """
	which = 'phys'
	want = 'long'
class preferred_size(aetools.NProperty):
	"""preferred size - the memory size with which the application will be launched (only applies to information windows for applications) """
	which = 'appt'
	want = 'long'
class product_version(aetools.NProperty):
	"""product version - the version of the product (visible at the top of the \xd2Get Info\xd3 window) """
	which = 'ver2'
	want = 'itxt'
class size(aetools.NProperty):
	"""size - the logical size of the item """
	which = 'ptsz'
	want = 'long'
class stationery(aetools.NProperty):
	"""stationery - Is the item a stationery pad? """
	which = 'pspd'
	want = 'bool'
class suggested_size(aetools.NProperty):
	"""suggested size - the memory size with which the developer recommends the application be launched """
	which = 'sprt'
	want = 'long'
class version(aetools.NProperty):
	"""version - the version of the file (visible at the bottom of the \xd2Get Info\xd3 window) """
	which = 'vers'
	want = 'itxt'
class warns_before_emptying(aetools.NProperty):
	"""warns before emptying - Display a dialog when emptying the trash (only valid for trash info window)? """
	which = 'warn'
	want = 'bool'

information_windows = information_window

class preferences_window(aetools.ComponentItem):
	"""preferences window - The Finder Preferences window """
	want = 'pwnd'

class view_options_window(aetools.ComponentItem):
	"""view options window - A View Options window """
	want = 'vwnd'

view_options_windows = view_options_window

class window(aetools.ComponentItem):
	"""window - A window """
	want = 'cwin'
class bounds(aetools.NProperty):
	"""bounds - the boundary rectangle for the window """
	which = 'pbnd'
	want = 'qdrt'
class closeable(aetools.NProperty):
	"""closeable - Does the window have a close box? """
	which = 'hclb'
	want = 'bool'
class collapsed(aetools.NProperty):
	"""collapsed - Is the window collapsed (only applies to open non-pop-up windows)? """
	which = 'wshd'
	want = 'bool'
class floating(aetools.NProperty):
	"""floating - Does the window have a title bar? """
	which = 'isfl'
	want = 'bool'
class index(aetools.NProperty):
	"""index - the number of the window in the front-to-back layer ordering """
	which = 'pidx'
	want = 'long'
class modal(aetools.NProperty):
	"""modal - Is the window modal? """
	which = 'pmod'
	want = 'bool'
class name(aetools.NProperty):
	"""name - the name of the window """
	which = 'pnam'
	want = 'itxt'
class popup(aetools.NProperty):
	"""popup - Is the window is a pop-up window? (only applies to open container windows in the Finder and can only be set when the Finder is the front application) """
	which = 'drwr'
	want = 'bool'
class position(aetools.NProperty):
	"""position - the upper left position of the window """
	which = 'posn'
	want = 'QDpt'
class pulled_open(aetools.NProperty):
	"""pulled open - Is the window pulled open (only applies to pop-up windows and can only be set when the Finder is the front application)? """
	which = 'pull'
	want = 'bool'
class resizable(aetools.NProperty):
	"""resizable - Is the window resizable? """
	which = 'prsz'
	want = 'bool'
class titled(aetools.NProperty):
	"""titled - Does the window have a title bar? """
	which = 'ptit'
	want = 'bool'
class visible(aetools.NProperty):
	"""visible - Is the window visible (always true for open Finder windows)? """
	which = 'pvis'
	want = 'bool'
class zoomable(aetools.NProperty):
	"""zoomable - Is the window zoomable? """
	which = 'iszm'
	want = 'bool'
class zoomed(aetools.NProperty):
	"""zoomed - Is the window zoomed? """
	which = 'pzum'
	want = 'bool'
class zoomed_full_size(aetools.NProperty):
	"""zoomed full size - Is the window zoomed to the full size of the screen? (can only be set, not read, and only applies to open non-pop-up windows) """
	which = 'zumf'
	want = 'bool'

windows = window
clipping_window._superclassnames = ['window']
clipping_window._privpropdict = {
	'_3c_Inheritance_3e_' : _3c_Inheritance_3e_,
}
clipping_window._privelemdict = {
}
container_window._superclassnames = ['window']
container_window._privpropdict = {
	'_3c_Inheritance_3e_' : _3c_Inheritance_3e_,
	'button_view_arrangement' : button_view_arrangement,
	'calculates_folder_sizes' : calculates_folder_sizes,
	'container' : container,
	'has_custom_view_settings' : has_custom_view_settings,
	'item' : item,
	'previous_list_view' : previous_list_view,
	'shows_comments' : shows_comments,
	'shows_creation_date' : shows_creation_date,
	'shows_kind' : shows_kind,
	'shows_label' : shows_label,
	'shows_modification_date' : shows_modification_date,
	'shows_size' : shows_size,
	'shows_version' : shows_version,
	'sort_direction' : sort_direction,
	'spatial_view_arrangement' : spatial_view_arrangement,
	'uses_relative_dates' : uses_relative_dates,
	'view' : view,
}
container_window._privelemdict = {
}
content_space._superclassnames = []
content_space._privpropdict = {
}
content_space._privelemdict = {
}
information_window._superclassnames = ['window']
information_window._privpropdict = {
	'_3c_Inheritance_3e_' : _3c_Inheritance_3e_,
	'comment' : comment,
	'creation_date' : creation_date,
	'current_panel' : current_panel,
	'icon' : icon,
	'item' : item,
	'locked' : locked,
	'minimum_size' : minimum_size,
	'modification_date' : modification_date,
	'physical_size' : physical_size,
	'preferred_size' : preferred_size,
	'product_version' : product_version,
	'size' : size,
	'stationery' : stationery,
	'suggested_size' : suggested_size,
	'version' : version,
	'warns_before_emptying' : warns_before_emptying,
}
information_window._privelemdict = {
}
preferences_window._superclassnames = ['window']
preferences_window._privpropdict = {
	'_3c_Inheritance_3e_' : _3c_Inheritance_3e_,
	'current_panel' : current_panel,
}
preferences_window._privelemdict = {
}
view_options_window._superclassnames = ['window']
view_options_window._privpropdict = {
	'_3c_Inheritance_3e_' : _3c_Inheritance_3e_,
	'item' : item,
}
view_options_window._privelemdict = {
}
window._superclassnames = []
window._privpropdict = {
	'bounds' : bounds,
	'closeable' : closeable,
	'collapsed' : collapsed,
	'floating' : floating,
	'index' : index,
	'modal' : modal,
	'name' : name,
	'popup' : popup,
	'position' : position,
	'pulled_open' : pulled_open,
	'resizable' : resizable,
	'titled' : titled,
	'visible' : visible,
	'zoomable' : zoomable,
	'zoomed' : zoomed,
	'zoomed_full_size' : zoomed_full_size,
}
window._privelemdict = {
}

#
# Indices of types declared in this module
#
_classdeclarations = {
	'cwin' : window,
	'cwnd' : container_window,
	'dwnd' : content_space,
	'iwnd' : information_window,
	'lwnd' : clipping_window,
	'pwnd' : preferences_window,
	'vwnd' : view_options_window,
}

_propdeclarations = {
	'appt' : preferred_size,
	'ascd' : creation_date,
	'aslk' : locked,
	'asmo' : modification_date,
	'barr' : button_view_arrangement,
	'c@#^' : _3c_Inheritance_3e_,
	'cobj' : item,
	'comt' : comment,
	'ctnr' : container,
	'cuss' : has_custom_view_settings,
	'drwr' : popup,
	'hclb' : closeable,
	'iarr' : spatial_view_arrangement,
	'iimg' : icon,
	'isfl' : floating,
	'iszm' : zoomable,
	'mprt' : minimum_size,
	'panl' : current_panel,
	'pbnd' : bounds,
	'phys' : physical_size,
	'pidx' : index,
	'pmod' : modal,
	'pnam' : name,
	'posn' : position,
	'prsz' : resizable,
	'pspd' : stationery,
	'ptit' : titled,
	'ptsz' : size,
	'pull' : pulled_open,
	'pvew' : view,
	'pvis' : visible,
	'pzum' : zoomed,
	'scda' : shows_creation_date,
	'scom' : shows_comments,
	'sdat' : shows_modification_date,
	'sfsz' : calculates_folder_sizes,
	'sknd' : shows_kind,
	'slbl' : shows_label,
	'sord' : sort_direction,
	'sprt' : suggested_size,
	'ssiz' : shows_size,
	'svew' : previous_list_view,
	'svrs' : shows_version,
	'urdt' : uses_relative_dates,
	'ver2' : product_version,
	'vers' : version,
	'warn' : warns_before_emptying,
	'wshd' : collapsed,
	'zumf' : zoomed_full_size,
}

_compdeclarations = {
}

_enumdeclarations = {
}
