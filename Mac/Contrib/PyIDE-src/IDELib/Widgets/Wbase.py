import Qd
import Win
import QuickDraw
import Evt
import string
from types import *
from SpecialKeys import *
import sys

WidgetsError = "WidgetsError"

DEBUG = 0

class Widget:
	
	_selectable = 0
	
	def __init__(self, possize):
		self._widgets = []
		self._widgetsdict = {}
		self._possize = possize
		self._bounds = None
		self._visible = 1
		self._enabled = 0
		self._selected = 0
		self._activated = 0
		self._callback = None
		self._parent = None
		self._parentwindow = None
		self._bindings = {}
		self._backcolor = None
	
	def show(self, onoff):
		self.SetPort()
		self._visible = onoff
		print 'Background'
		if self._visible and self._backcolor:
			penstate = Qd.GetPenState()
			Qd.RGBForeColor(self._backcolor)
			Qd.FrameRect(self._bounds)
			Qd.RGBForeColor((0, 0, 0))
			Qd.SetPenState(penstate)
			
		for w in self._widgets:
			w.show(onoff)
		if onoff:
			self.draw()
		else:
			Qd.EraseRect(self._bounds)
	
	def draw(self, visRgn = None):
		if self._visible:
			# draw your stuff here
			pass
	
	def getpossize(self):
		return self._possize
	
	def getbounds(self):
		return self._bounds
	
	def move(self, x, y = None):
		"""absolute move"""
		if y == None:
			x, y = x
		if type(self._possize) <> TupleType:
			raise WidgetsError, "can't move widget with bounds function"
		l, t, r, b = self._possize
		self.resize(x, y, r, b)
	
	def rmove(self, x, y = None):
		"""relative move"""
		if y == None:
			x, y = x
		if type(self._possize) <> TupleType:
			raise WidgetsError, "can't move widget with bounds function"
		l, t, r, b = self._possize
		self.resize(l + x, t + y, r, b)
		
	def resize(self, *args):
		#print "yep.", args
		if len(args) == 1:
			if type(args[0]) == FunctionType or type(args[0]) == MethodType:
				self._possize = args[0]
			else:
				apply(self.resize, args[0])
		elif len(args) == 2:
			self._possize = (0, 0) + args
		elif len(args) == 4:
			self._possize = args
		else:
			raise TypeError, "wrong number of arguments"
		self._calcbounds()
	
	def open(self):
		self._calcbounds()
	
	def close(self):
		#print "xxx Closing Widget"
		del self._callback
		del self._possize
		del self._bindings
		del self._parent
		del self._parentwindow
	
	def bind(self, key, callback):
		"""bind a key or an 'event' to a callback"""
		if callback:
			self._bindings[key] = callback
		elif self._bindings.has_key(key):
			del self._bindings[key]
	
	def adjust(self, oldbounds):
		self.SetPort()
		Win.InvalRect(oldbounds)
		Win.InvalRect(self._bounds)
	
	def _calcbounds(self):
		oldbounds = self._bounds
		pl, pt, pr, pb = self._parent._bounds
		if callable(self._possize):
			width = pr - pl
			height = pb - pt
			self._bounds = Qd.OffsetRect(self._possize(width, height), pl, pt)
		else:
			l, t, r, b = self._possize
			if l < -1:
				l = pr + l
			else:
				l = pl + l
			if t < -1:
				t = pb + t
			else:
				t = pt + t
			if r > 1:
				r = l + r
			else:
				r = pr + r
			if b > 1:
				b = t + b
			else:
				b = pb + b
			self._bounds = (l, t, r, b)
		if oldbounds and oldbounds <> self._bounds:
			self.adjust(oldbounds)
		for w in self._widgets:
			w._calcbounds()
	
	def test(self, point):
		if Qd.PtInRect(point, self._bounds):
			return 1
	
	def click(self, point, modifiers):
		pass
	
	def findwidget(self, point, onlyenabled = 1):
		if self.test(point):
			for w in self._widgets:
				widget = w.findwidget(point)
				if widget is not None:
					return widget
			if self._enabled or not onlyenabled:
				return self
	
	def forall(self, methodname, *args):
		for w in self._widgets:
			rv = apply(w.forall, (methodname,) + args)
			if rv: 
				return rv
		if self._bindings.has_key("<" + methodname + ">"):
			callback = self._bindings["<" + methodname + ">"]
			rv = apply(callback, args)
			if rv: 
				return rv
		if hasattr(self, methodname):
			method = getattr(self, methodname)
			return apply(method, args)
	
	def forall_butself(self, methodname, *args):
		for w in self._widgets:
			rv = apply(w.forall, (methodname,) + args)
			if rv: 
				return rv
	
	def forall_frombottom(self, methodname, *args):
		if self._bindings.has_key("<" + methodname + ">"):
			callback = self._bindings["<" + methodname + ">"]
			rv = apply(callback, args)
			if rv: 
				return rv
		if hasattr(self, methodname):
			method = getattr(self, methodname)
			rv = apply(method, args)
			if rv: 
				return rv
		for w in self._widgets:
			rv = apply(w.forall_frombottom, (methodname,) + args)
			if rv: 
				return rv
	
	def _addwidget(self, key, widget):
		if widget in self._widgets:
			raise ValueError, "duplicate widget"
		if self._widgetsdict.has_key(key):
			self._removewidget(key)
		self._widgets.append(widget)
		self._widgetsdict[key] = widget
		widget._parent = self
		self._setparentwindow(widget)
		if self._parentwindow and self._parentwindow.wid:
			widget.forall_frombottom("open")
			Win.InvalRect(widget._bounds)
	
	def _setparentwindow(self, widget):
		widget._parentwindow = self._parentwindow
		for w in widget._widgets:
			self._setparentwindow(w)
	
	def _removewidget(self, key):
		if not self._widgetsdict.has_key(key):
			raise KeyError, "no widget with key " + `key`
		widget = self._widgetsdict[key]
		for k in widget._widgetsdict.keys():
			widget._removewidget(k)
		if self._parentwindow._currentwidget == widget:
			widget.select(0)
			self._parentwindow._currentwidget = None
		self.SetPort()
		Win.InvalRect(widget._bounds)
		widget.close()
		del self._widgetsdict[key]
		self._widgets.remove(widget)
	
	def __setattr__(self, attr, value):
		if type(value) == InstanceType and HasBaseClass(value, Widget) and	\
				attr not in ("_currentwidget", "_lastrollover", 
					"_parent", "_parentwindow", "_defaultbutton"):
			if hasattr(self, attr):
				raise ValueError, "Can't replace existing attribute: " + attr
			self._addwidget(attr, value)
		self.__dict__[attr] = value
	
	def __delattr__(self, attr):
		if attr == "_widgetsdict":
			raise AttributeError, "cannot delete attribute _widgetsdict"
		if self._widgetsdict.has_key(attr):
			self._removewidget(attr)
			if self.__dict__.has_key(attr):
				del self.__dict__[attr]
		elif self.__dict__.has_key(attr):
			del self.__dict__[attr]
		else:
			raise AttributeError, attr
	
	def __setitem__(self, key, value):
		self._addwidget(key, value)
	
	def __getitem__(self, key):
		if not self._widgetsdict.has_key(key):
			raise KeyError, key
		return self._widgetsdict[key]
	
	def __delitem__(self, key):
		self._removewidget(key)
	
	def SetPort(self):
		self._parentwindow.SetPort()
	
	def __del__(self):
		if DEBUG:
			print "%s instance deleted" % self.__class__.__name__
	
	def _drawbounds(self):
		Qd.FrameRect(self._bounds)


class ClickableWidget(Widget):

	def click(self, point, modifiers):
		pass
	
	def enable(self, onoff):
		self._enabled = onoff
		self.SetPort()
		self.draw()
	
	def callback(self):
		if self._callback:
			return CallbackCall(self._callback, 1)
	

class SelectableWidget(ClickableWidget):

	_selectable = 1
	
	def select(self, onoff, isclick = 0):
		if onoff == self._selected:
			return 1
		if self._bindings.has_key("<select>"):
			callback = self._bindings["<select>"]
			if callback(onoff):
				return 1
		self._selected = onoff
		if onoff:
			if self._parentwindow._currentwidget is not None:
				self._parentwindow._currentwidget.select(0)
			self._parentwindow._currentwidget = self
		else:
			self._parentwindow._currentwidget = None
	
	def key(self, char, event):
		pass
	
	def drawselframe(self, onoff):
		if not self._parentwindow._hasselframes:
			return
		thickrect = Qd.InsetRect(self._bounds, -3, -3)
		state = Qd.GetPenState()
		Qd.PenSize(2, 2)
		if onoff:
			Qd.PenPat(Qd.qd.black)
		else:
			Qd.PenPat(Qd.qd.white)
		Qd.FrameRect(thickrect)
		Qd.SetPenState(state)
	
	def adjust(self, oldbounds):
		self.SetPort()
		if self._selected:
			Win.InvalRect(Qd.InsetRect(oldbounds, -3, -3))
			Win.InvalRect(Qd.InsetRect(self._bounds, -3, -3))
		else:
			Win.InvalRect(oldbounds)
			Win.InvalRect(self._bounds)


class _Line(Widget):
	
	def __init__(self, possize, thickness = 1):
		Widget.__init__(self, possize)
		self._thickness = thickness
	
	def open(self):
		self._calcbounds()
		self.SetPort()
		self.draw()
	
	def draw(self, visRgn = None):
		if self._visible:
			Qd.PaintRect(self._bounds)
	
	def _drawbounds(self):
		pass

class HorizontalLine(_Line):
	
	def _calcbounds(self):
		Widget._calcbounds(self)
		l, t, r, b = self._bounds
		self._bounds = l, t, r, t + self._thickness

class VerticalLine(_Line):
	
	def _calcbounds(self):
		Widget._calcbounds(self)
		l, t, r, b = self._bounds
		self._bounds = l, t, l + self._thickness, b


class Frame(Widget):
	
	def __init__(self, possize, pattern = Qd.qd.black, color = (0, 0, 0)):
		Widget.__init__(self, possize)
		self._framepattern = pattern
		self._framecolor = color
	
	def setcolor(self, color):
		self._framecolor = color
		self.draw()
	
	def setpattern(self, pattern):
		self._framepattern = pattern
		self.draw()
		
	def draw(self, visRgn = None):
		if self._visible:
			penstate = Qd.GetPenState()
			Qd.PenPat(self._framepattern)
			Qd.RGBForeColor(self._framecolor)
			Qd.FrameRect(self._bounds)
			Qd.RGBForeColor((0, 0, 0))
			Qd.SetPenState(penstate)


class Group(Widget): pass
	

class HorizontalPanes(Widget):
	
	_direction = 1
	
	def __init__(self, possize, panesizes = None, gutter = 8):
		ClickableWidget.__init__(self, possize)
		self._panesizes = panesizes
		self._gutter = gutter
		self._enabled = 1
		self.setuppanes()
	
	def open(self):
		self.installbounds()
		ClickableWidget.open(self)
	
	def setuppanes(self):
		panesizes = self._panesizes
		total = 0
		if panesizes is not None:
			#if len(self._widgets) <> len(panesizes):
			#	raise TypeError, 'number of widgets does not match number of panes'
			for panesize in panesizes:
				if not 0 < panesize < 1:
					raise TypeError, 'pane sizes must be between 0 and 1, not including.'
				total = total + panesize
			if round(total, 4) <> 1.0:
				raise TypeError, 'pane sizes must add up to 1'
		else:
			step = 1.0 / len(self._widgets)
			panesizes = []
			for i in range(len(self._widgets)):
				panesizes.append(step)
		current = 0
		self._panesizes = []
		self._gutters = []
		for panesize in panesizes:
			if current:
				self._gutters.append(current)
			self._panesizes.append(current, current + panesize)
			current = current + panesize
		self.makepanebounds()
	
	def getpanesizes(self):
		return map(lambda (fr, to): to-fr,  self._panesizes)
	
	boundstemplate = "lambda width, height: (0, height * %s + %d, width, height * %s + %d)"
	
	def makepanebounds(self):
		halfgutter = self._gutter / 2
		self._panebounds = []
		for i in range(len(self._panesizes)):
			panestart, paneend = self._panesizes[i]
			boundsstring = self.boundstemplate % (`panestart`, panestart and halfgutter, 
							`paneend`, (paneend <> 1.0) and -halfgutter)
			self._panebounds.append(eval(boundsstring))
	
	def installbounds(self):
		#self.setuppanes()
		for i in range(len(self._widgets)):
			w = self._widgets[i]
			w._possize = self._panebounds[i]
			#if hasattr(w, "setuppanes"):
			#	w.setuppanes()
			if hasattr(w, "installbounds"):
				w.installbounds()
	
	def rollover(self, point, onoff):
		if onoff:
			orgmouse = point[self._direction]
			halfgutter = self._gutter / 2
			l, t, r, b = self._bounds
			if self._direction:
				begin, end = t, b
			else:
				begin, end = l, r
			
			i = self.findgutter(orgmouse, begin, end)
			if i is None:
				SetCursor("arrow")
			else:
				SetCursor(self._direction and 'vmover' or 'hmover')
	
	def findgutter(self, orgmouse, begin, end):
		tolerance = max(4, self._gutter) / 2
		for i in range(len(self._gutters)):
			pos = begin + (end - begin) * self._gutters[i]
			if abs(orgmouse - pos) <= tolerance:
				break
		else:
			return
		return i
	
	def click(self, point, modifiers):
		# what a mess...
		orgmouse = point[self._direction]
		halfgutter = self._gutter / 2
		l, t, r, b = self._bounds
		if self._direction:
			begin, end = t, b
		else:
			begin, end = l, r
		
		i = self.findgutter(orgmouse, begin, end)
		if i is None:
			return
		
		pos = orgpos = begin + (end - begin) * self._gutters[i]	# init pos too, for fast click on border, bug done by Petr
		
		minpos = self._panesizes[i][0]
		maxpos = self._panesizes[i+1][1]
		minpos = begin + (end - begin) * minpos + 64
		maxpos = begin + (end - begin) * maxpos - 64
		if minpos > orgpos and maxpos < orgpos:
			return
		
		#SetCursor("fist")
		self.SetPort()
		if self._direction:
			rect = l, orgpos - 1, r, orgpos
		else:
			rect = orgpos - 1, t, orgpos, b
		
		# track mouse --- XXX  move to separate method?
		Qd.PenMode(QuickDraw.srcXor)
		Qd.PenPat(Qd.qd.gray)
		Qd.PaintRect(rect)
		lastpos = None
		while Evt.Button():
			pos = orgpos - orgmouse + Evt.GetMouse()[self._direction]
			pos = max(pos, minpos)
			pos = min(pos, maxpos)
			if pos == lastpos:
				continue
			Qd.PenPat(Qd.qd.gray)
			Qd.PaintRect(rect)
			if self._direction:
				rect = l, pos - 1, r, pos
			else:
				rect = pos - 1, t, pos, b
			Qd.PenPat(Qd.qd.gray)
			Qd.PaintRect(rect)
			lastpos = pos
		Qd.PaintRect(rect)
		Qd.PenNormal()
		SetCursor("watch")
		
		newpos = (pos - begin) / float(end - begin)
		self._gutters[i] = newpos
		self._panesizes[i] = self._panesizes[i][0], newpos
		self._panesizes[i+1] = newpos, self._panesizes[i+1][1]
		self.makepanebounds()
		self.installbounds()
		self._calcbounds()
	

class VerticalPanes(HorizontalPanes):

	_direction = 0
	boundstemplate = "lambda width, height: (width * %s + %d, 0, width * %s + %d, height)"


# misc utils

def CallbackCall(callback, mustfit, *args):
	if type(callback) == FunctionType:
		func = callback
		maxargs = func.func_code.co_argcount
	elif type(callback) == MethodType:
		func = callback.im_func
		maxargs = func.func_code.co_argcount - 1
	else:
		if callable(callback):
			return apply(callback, args)
		else:
			raise TypeError, "uncallable callback object"
	
	if func.func_defaults:
		minargs = maxargs - len(func.func_defaults)
	else:
		minargs = maxargs
	if minargs <= len(args) <= maxargs:
		return apply(callback, args)
	elif not mustfit and minargs == 0:
		return callback()
	else:
		if mustfit:
			raise TypeError, "callback accepts wrong number of arguments: " + `len(args)`
		else:
			raise TypeError, "callback accepts wrong number of arguments: 0 or " + `len(args)`


def HasBaseClass(obj, class_):
	try:
		raise obj
	except class_:
		return 1
	except:
		pass
	return 0


_cursors = {
	"watch"	: Qd.GetCursor(QuickDraw.watchCursor).data,
	"arrow"	: Qd.qd.arrow,
	"iBeam"	: Qd.GetCursor(QuickDraw.iBeamCursor).data,
	"cross"	: Qd.GetCursor(QuickDraw.crossCursor).data,
	"plus"		: Qd.GetCursor(QuickDraw.plusCursor).data,
	"hand"	: Qd.GetCursor(468).data,
	"fist"		: Qd.GetCursor(469).data,
	"hmover"	: Qd.GetCursor(470).data,
	"vmover"	: Qd.GetCursor(471).data
}

def SetCursor(what):
	Qd.SetCursor(_cursors[what])
