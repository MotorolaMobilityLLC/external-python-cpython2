#!/usr/local/python

# objgraph
#
# Read "nm -o" input (on IRIX: "nm -Bo") of a set of libraries or modules
# and print various interesting listings, such as:
#
# - which names are used but not defined in the set (and used where),
# - which names are defined in the set (and where),
# - which modules use which other modules,
# - which modules are used by which other modules.
#
# Usage: objgraph [-cdu] [file] ...
# -c: print callers per objectfile
# -d: print callees per objectfile
# -u: print usage of undefined symbols
# If none of -cdu is specified, all are assumed.
# Use "nm -o" to generate the input (on IRIX: "nm -Bo"),
# e.g.: nm -o /lib/libc.a | objgraph


import sys
import string
import path
import getopt
import regexp

# Types of symbols.
#
definitions = 'TRGDSBAEC'
externals = 'UV'
ignore = 'Nntrgdsbavuc'

# Regular expression to parse "nm -o" output.
#
matcher = regexp.compile('(.*):\t?........ (.) (.*)$')

# Store "item" in "dict" under "key".
# The dictionary maps keys to lists of items.
# If there is no list for the key yet, it is created.
#
def store(dict, key, item):
	if dict.has_key(key):
		dict[key].append(item)
	else:
		dict[key] = [item]

# Return a flattened version of a list of strings: the concatenation
# of its elements with intervening spaces.
#
def flat(list):
	s = ''
	for item in list:
		s = s + ' ' + item
	return s[1:]

# Global variables mapping defined/undefined names to files and back.
#
file2undef = {}
def2file = {}
file2def = {}
undef2file = {}

# Read one input file and merge the data into the tables.
# Argument is an open file.
#
def readinput(file):
	while 1:
		s = file.readline(200) # Arbitrary, but reasonable limit
		if not s:
			break
		# If you get an exception on this line,
		# it is probably caused by an unexpected input line:
		(ra, rb), (r1a, r1b), (r2a, r2b), (r3a, r3b) = matcher.exec(s)
		fn, name, type = s[r1a:r1b], s[r3a:r3b], s[r2a:r2b]
		if type in definitions:
			store(def2file, name, fn)
			store(file2def, fn, name)
		elif type in externals:
			store(file2undef, fn, name)
			store(undef2file, name, fn)
		elif not type in ignore:
			print fn + ':' + name + ': unknown type ' + type

# Print all names that were undefined in some module and where they are
# defined.
#
def printcallee():
	flist = file2undef.keys()
	flist.sort()
	for file in flist:
		print file + ':'
		elist = file2undef[file]
		elist.sort()
		for ext in elist:
			if len(ext) >= 8:
				tabs = '\t'
			else:
				tabs = '\t\t'
			if not def2file.has_key(ext):
				print '\t' + ext + tabs + ' *undefined'
			else:
				print '\t' + ext + tabs + flat(def2file[ext])

# Print for each module the names of the other modules that use it.
#
def printcaller():
	files = file2def.keys()
	files.sort()
	for file in files:
		callers = []
		for label in file2def[file]:
			if undef2file.has_key(label):
				callers = callers + undef2file[label]
		if callers:
			callers.sort()
			print file + ':'
			lastfn = ''
			for fn in callers:
				if fn <> lastfn:
					print '\t' + fn
				lastfn = fn
		else:
			print file + ': unused'

# Print undefine names and where they are used.
#
def printundef():
	undefs = {}
	for file in file2undef.keys():
		for ext in file2undef[file]:
			if not def2file.has_key(ext):
				store(undefs, ext, file)
	elist = undefs.keys()
	elist.sort()
	for ext in elist:
		print ext + ':'
		flist = undefs[ext]
		flist.sort()
		for file in flist:
			print '\t' + file

# Print warning messages about names defined in more than one file.
#
def warndups():
	savestdout = sys.stdout
	sys.stdout = sys.stderr
	names = def2file.keys()
	names.sort()
	for name in names:
		if len(def2file[name]) > 1:
			print 'warning:', name, 'multiply defined:',
			print flat(def2file[name])
	sys.stdout = savestdout

# Main program
#
def main():
	try:
		optlist, args = getopt.getopt(sys.argv[1:], 'cdu')
	except getopt.error:
		sys.stdout = sys.stderr
		print 'Usage:', path.basename(sys.argv[0]), '[-cdu] [file] ...'
		print '-c: print callers per objectfile'
		print '-d: print callees per objectfile'
		print '-u: print usage of undefined symbols'
		print 'If none of -cdu is specified, all are assumed.'
		print 'Use "nm -o" to generate the input (on IRIX: "nm -Bo"),'
		print 'e.g.: nm -o /lib/libc.a | objgraph'
		return 1
	optu = optc = optd = 0
	for opt, void in optlist:
		if opt == '-u':
			optu = 1
		elif opt == '-c':
			optc = 1
		elif opt == '-d':
			optd = 1
	if optu == optc == optd == 0:
		optu = optc = optd = 1
	if not args:
		args = ['-']
	for file in args:
		if file == '-':
			readinput(sys.stdin)
		else:
			readinput(open(file, 'r'))
	#
	warndups()
	#
	more = (optu + optc + optd > 1)
	if optd:
		if more:
			print '---------------All callees------------------'
		printcallee()
	if optu:
		if more:
			print '---------------Undefined callees------------'
		printundef()
	if optc:
		if more:
			print '---------------All Callers------------------'
		printcaller()
	return 0

# Call the main program.
# Use its return value as exit status.
# Catch interrupts to avoid stack trace.
#
try:
	sys.exit(main())
except KeyboardInterrupt:
	sys.exit(1)
